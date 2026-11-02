"""Read-only npm OIDC publication readback tests; all registry responses are mocked."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest import mock
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("npm_readback_under_test", ROOT / "tools/npm_registry_readback.py")
readback = importlib.util.module_from_spec(spec)
spec.loader.exec_module(readback)
VERSION = "1.20.4"
INTEGRITY = "sha512-expected-value"


def metadata(integrity: str = INTEGRITY, repo: str = readback.REPOSITORY) -> dict:
    return {
        "name": readback.NAME,
        "version": VERSION,
        "repository": {"url": repo},
        "dist": {"integrity": integrity},
    }


class NpmRegistryReadbackTests(unittest.TestCase):
    def test_exact_version_checksum_and_latest_are_required(self):
        urls = []

        def fetch(url):
            urls.append(url)
            return {"latest": VERSION} if url.endswith("/dist-tags") else metadata()

        with mock.patch("builtins.print") as printer:
            readback.wait_for_readback(VERSION, INTEGRITY, fetch=fetch, pause=lambda _: None)
        self.assertEqual(len(urls), 2)
        self.assertIn(f"/{readback.NAME}/{VERSION}", urls[0])
        self.assertIn("PUBLIC_REGISTRY_INTEGRITY_VERIFIED", printer.call_args_list[0].args[0])

    def test_transient_version_404_retries_without_any_publish(self):
        seen = []
        pauses = []

        def fetch(url):
            if url.endswith("/dist-tags"):
                return {"latest": VERSION}
            seen.append(url)
            if len(seen) < 3:
                raise readback.ReadbackPending("Public registry HTTP 404")
            return metadata()

        readback.wait_for_readback(VERSION, INTEGRITY, attempts=3, fetch=fetch, pause=pauses.append)
        self.assertEqual(len(seen), 3)
        self.assertEqual(pauses, [2, 4])

    def test_stale_latest_dist_tag_is_pending_not_success(self):
        latest_calls = []

        def fetch(url):
            if url.endswith("/dist-tags"):
                latest_calls.append(url)
                return {"latest": "1.20.3" if len(latest_calls) < 2 else VERSION}
            return metadata()

        delays = []
        readback.wait_for_readback(VERSION, INTEGRITY, attempts=2, fetch=fetch, pause=delays.append)
        self.assertEqual(delays, [2])

    def test_wrong_archive_integrity_is_permanent_conflict(self):
        def fetch(url):
            return metadata("sha512-unexpected") if not url.endswith("/dist-tags") else {"latest": VERSION}

        delays = []
        with self.assertRaisesRegex(readback.IntegrityConflict, "SHA-512"):
            readback.wait_for_readback(VERSION, INTEGRITY, attempts=9, fetch=fetch, pause=delays.append)
        self.assertEqual(delays, [])

    def test_wrong_repository_is_rejected(self):
        with self.assertRaisesRegex(readback.IntegrityConflict, "repository"):
            readback.verify_once(VERSION, INTEGRITY, lambda _: metadata(repo="https://example.com/other"))

    def test_unexpected_version_is_rejected(self):
        wrong = metadata()
        wrong["version"] = "1.20.3"
        with self.assertRaisesRegex(readback.IntegrityConflict, "version"):
            readback.verify_once(VERSION, INTEGRITY, lambda _: wrong)

    def test_pending_at_retry_limit_does_not_claim_success(self):
        delays = []

        def fetch(_):
            raise readback.ReadbackPending("Public registry HTTP 404")

        with self.assertRaisesRegex(readback.ReadbackPending, "404"):
            readback.wait_for_readback(VERSION, INTEGRITY, attempts=2, fetch=fetch, pause=delays.append)
        self.assertEqual(delays, [2])

    def test_real_http_404_is_classified_as_pending(self):
        error = HTTPError("https://registry.npmjs.org", 404, "not found", {}, None)
        with mock.patch.object(readback, "urlopen", side_effect=error):
            with self.assertRaises(readback.ReadbackPending):
                readback.fetch_json("https://registry.npmjs.org/ui-spec-studio/1.20.4")

    def test_workflow_runs_bounded_readback_before_public_cli_smoke(self):
        yaml = (ROOT / ".github/workflows/npm-publish.yml").read_text(encoding="utf-8")
        command = "python tools/npm_registry_readback.py --tarball dist/ui-spec-installer.tgz"
        self.assertIn(command, yaml)
        self.assertLess(yaml.index(command), yaml.index("python tools/official_npm_smoke.py --require-published"))
        self.assertIn("id-token: write", yaml)
        self.assertNotIn("npm view \"ui-spec-studio@$version\" version dist.integrity --json --prefer-online", yaml)


if __name__ == "__main__":
    unittest.main()
