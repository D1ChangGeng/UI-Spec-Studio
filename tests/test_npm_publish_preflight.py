"""The publish gate must never infer "new version" from arbitrary npm output."""
from __future__ import annotations

import importlib.util
import io
from pathlib import Path
import unittest
from unittest import mock
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("npm_preflight_under_test", ROOT / "tools/npm_publish_preflight.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

VERSION = "1.20.5"
INTEGRITY = "sha512-example-for-test"


def version_metadata(integrity: str = INTEGRITY) -> dict:
    return {
        "name": module.PACKAGE,
        "version": VERSION,
        "repository": {"url": module.REPOSITORY},
        "dist": {"integrity": integrity},
    }


class NpmPublishPreflightTests(unittest.TestCase):
    def test_definite_absence_is_only_allowed_publish_case(self):
        self.assertEqual(module.inspect(VERSION, INTEGRITY, read=lambda _: None), "NOT_PUBLISHED")

    def test_same_version_and_archive_is_noop(self):
        self.assertEqual(
            module.inspect(VERSION, INTEGRITY, read=lambda _: version_metadata()),
            "ALREADY_PUBLISHED_MATCH",
        )

    def test_mismatched_sha512_blocks_a_publish(self):
        with self.assertRaisesRegex(module.RegistryProbeError, "SHA-512"):
            module.inspect(VERSION, INTEGRITY, read=lambda _: version_metadata("sha512-conflict"))

    def test_package_identity_conflict_fails_closed(self):
        wrong = version_metadata()
        wrong["repository"]["url"] = "https://github.com/other/repo"
        with self.assertRaisesRegex(module.RegistryProbeError, "identity conflict"):
            module.inspect(VERSION, INTEGRITY, read=lambda _: wrong)

    def test_incomplete_metadata_not_treated_as_unpublished(self):
        with self.assertRaises(module.RegistryProbeError):
            module.inspect(VERSION, INTEGRITY, read=lambda _: {})

    def test_http_404_is_definite_unpublished_state(self):
        error = HTTPError("https://registry.npmjs.org", 404, "Not Found", {}, None)
        with mock.patch.object(module, "urlopen", side_effect=error):
            self.assertIsNone(module.public_version_metadata(VERSION))

    def test_http_500_does_not_permit_publish(self):
        error = HTTPError("https://registry.npmjs.org", 500, "Upstream down", {}, None)
        with mock.patch.object(module, "urlopen", side_effect=error):
            with self.assertRaisesRegex(module.RegistryProbeError, "HTTP 500"):
                module.public_version_metadata(VERSION)

    def test_network_errors_do_not_permit_publish(self):
        with mock.patch.object(module, "urlopen", side_effect=URLError("offline")):
            with self.assertRaisesRegex(module.RegistryProbeError, "Unable"):
                module.public_version_metadata(VERSION)

    def test_version_does_not_admit_ranges_or_path_injection(self):
        with self.assertRaisesRegex(module.RegistryProbeError, "Invalid"):
            module.public_version_metadata("../../1.20.5")

    def test_release_workflow_uses_preflight_and_no_placeholder_auth(self):
        workflow = (ROOT / ".github/workflows/npm-publish.yml").read_text(encoding="utf-8")
        self.assertIn("python tools/npm_publish_preflight.py --tarball dist/ui-spec-installer.tgz", workflow)
        self.assertNotIn('npm view "ui-spec-studio@$version" dist.integrity', workflow)
        # setup-node registry-url writes an empty NODE_AUTH_TOKEN placeholder;
        # an OIDC-only publish job must not generate such a token configuration.
        publish_job = workflow.split("\n  publish:", 1)[1]
        self.assertNotIn("registry-url:", publish_job)
        self.assertIn("id-token: write", publish_job)
        self.assertIn("npm publish ./dist/ui-spec-installer.tgz --access public", publish_job)


if __name__ == "__main__":
    unittest.main()
