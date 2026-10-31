"""Supply integrity and failure boundaries; real rendering remains a CI gate."""
from __future__ import annotations

from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import stat
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock
import urllib.error
import zipfile

from test_tools import ROOT, load

provisioner = load("preview_provisioner_test", "tools/provision_preview_browser.py")


class Response(io.BytesIO):
    status = 200

    def geturl(self):
        return "https://official.example.test/archive.zip"


class PreviewProvisioningTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def asset(self, data):
        return {"name": "test", "urls": ["https://official.example.test/archive.zip"],
                "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

    def archive(self, name="browser", mode=stat.S_IFREG | 0o755):
        path = self.root / "fixture.zip"
        with zipfile.ZipFile(path, "w") as archive:
            info = zipfile.ZipInfo(name)
            # Keep the adversarial archive name despite host separator normalization.
            info.filename = name
            info.external_attr = mode << 16
            archive.writestr(info, b"fixture executable bytes")
        with zipfile.ZipFile(path) as archive:
            self.assertEqual(archive.infolist()[0].orig_filename, name)
        return path

    def test_verified_download_records_actual_digest_and_source(self):
        data = self.archive().read_bytes()
        destination = self.root / "download.zip"
        record = {}
        with mock.patch.object(provisioner.urllib.request, "urlopen", return_value=Response(data)):
            provisioner.download_verified(self.asset(data), destination, record)
        self.assertEqual(destination.read_bytes(), data)
        self.assertEqual(record["attempts"][0]["status"], "verified")
        self.assertEqual(record["attempts"][0]["sha256"], hashlib.sha256(data).hexdigest())

    def test_corrupt_same_length_response_is_rejected_and_not_installed(self):
        good = b"reviewed archive bytes"
        destination = self.root / "download.zip"
        record = {}
        with mock.patch.object(provisioner.urllib.request, "urlopen",
                               side_effect=lambda *a, **k: Response(b"x" * len(good))):
            with self.assertRaises(provisioner.ProvisionError):
                provisioner.download_verified(self.asset(good), destination, record)
        self.assertFalse(destination.exists())
        self.assertFalse(destination.with_suffix(".partial").exists())
        self.assertTrue(all(item["status"] == "failed" for item in record["attempts"]))

    def test_truncated_response_is_rejected(self):
        destination = self.root / "download.zip"
        with mock.patch.object(provisioner.urllib.request, "urlopen",
                               side_effect=lambda *a, **k: Response(b"partial")):
            with self.assertRaises(provisioner.ProvisionError):
                provisioner.download_verified(self.asset(b"partial and complete"), destination, {})
        self.assertFalse(destination.exists())

    def test_unavailable_official_source_uses_verified_fallback(self):
        data = b"same reviewed archive bytes"
        asset = self.asset(data)
        asset["urls"].append("https://mirror.example.test/archive.zip")
        record = {}
        with mock.patch.object(provisioner.urllib.request, "urlopen", side_effect=[
            urllib.error.URLError("source temporarily unavailable"), Response(data),
        ]):
            provisioner.download_verified(asset, self.root / "download.zip", record)
        self.assertEqual([item["status"] for item in record["attempts"]], ["failed", "verified"])
        self.assertEqual(record["source_url"], asset["urls"][1])

    def test_archive_keeps_binary_bytes(self):
        destination = self.root / "extracted"
        destination.mkdir()
        provisioner.extract_archive(self.archive("nested/browser"), destination)
        self.assertEqual((destination / "nested/browser").read_bytes(), b"fixture executable bytes")

    def test_path_escape_absolute_and_windows_traversal_are_rejected(self):
        # Windows normalizes ZIP separators on read; this remains actual traversal.
        for name in ("../escape", "/escape", "C:/escape", "nested\\..\\..\\escape"):
            with self.subTest(name=name):
                with self.assertRaises(provisioner.ProvisionError):
                    provisioner.extract_archive(self.archive(name), self.root / "extracted")
                self.assertFalse((self.root / "extracted").exists())

    def test_archive_link_is_rejected_before_any_extraction(self):
        with self.assertRaises(provisioner.ProvisionError):
            provisioner.extract_archive(self.archive("link", stat.S_IFLNK | 0o777), self.root / "out")
        self.assertFalse((self.root / "out").exists())

    def test_existing_installation_is_preserved(self):
        sentinel = self.root / "keep.txt"
        sentinel.write_text("user-owned", encoding="utf-8")
        with mock.patch.object(provisioner, "verify_playwright"), \
                mock.patch.object(provisioner.sys, "platform", "linux"), \
                mock.patch.object(provisioner.platform, "machine", return_value="x86_64"):
            with self.assertRaisesRegex(provisioner.ProvisionError, "fresh --output-dir"):
                provisioner.provision(self.root, {"artifacts": []})
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "user-owned")

    def test_registry_mismatch_is_rejected(self):
        registry = self.root / "browsers.json"
        registry.write_text(json.dumps({"browsers": [
            {"name": "chromium-headless-shell", "browserVersion": "999.0.0.0"},
            {"name": "ffmpeg", "revision": "1011"},
        ]}), encoding="utf-8")
        distribution = SimpleNamespace(version=provisioner.PLAYWRIGHT_VERSION,
                                       locate_file=lambda _: registry)
        with mock.patch.object(provisioner.metadata, "distribution", return_value=distribution):
            with self.assertRaisesRegex(provisioner.ProvisionError, "registry differs"):
                provisioner.verify_playwright()

    def test_failed_provision_writes_failure_evidence_without_success_outputs(self):
        report = self.root / "report.json"
        outputs = self.root / "github-output"
        with mock.patch.object(provisioner, "provision", side_effect=provisioner.ProvisionError("failed pin")), \
                redirect_stdout(io.StringIO()):
            result = provisioner.main(["--output-dir", str(self.root / "browsers"),
                                       "--report", str(report), "--github-output", str(outputs)])
        self.assertEqual(result, 1)
        self.assertEqual(json.loads(report.read_text(encoding="utf-8"))["status"], "failed")
        self.assertFalse(outputs.exists())

    def test_workflow_preserves_real_gates_with_explicit_verified_browser(self):
        workflow = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        for script in ("preview_readme.py", "validate_scenario.py", "validate_assets.py",
                       "validate_content.py", "validate_temporal.py"):
            commands = [line for line in workflow.splitlines() if "run: python tools/" + script in line]
            self.assertTrue(commands)
            self.assertTrue(all('--browser-path "${{ steps.browser.outputs.browser_path }}"' in line
                                for line in commands))
        self.assertIn('--live-commit "$GITHUB_SHA"', workflow)
        self.assertIn("PLAYWRIGHT_BROWSERS_PATH: ${{ steps.browser.outputs.browsers_path }}", workflow)
        self.assertNotIn("--no-video", workflow)


if __name__ == "__main__":
    unittest.main()
