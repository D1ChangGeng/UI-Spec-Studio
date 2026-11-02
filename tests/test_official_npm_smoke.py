"""Public npm CLI smoke retries stale latest, never published bytes or owner identity."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "official_npm_smoke_under_test", ROOT / "tools/official_npm_smoke.py"
)
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)
VERSION = "1.20.5"


def metadata(version: str = VERSION, *, repo: str = smoke.EXPECTED_REPO) -> dict:
    return {
        "name": smoke.NAME,
        "version": version,
        "repository": {"url": repo},
        "dist": {"integrity": "sha512-test-integrity"},
    }


def response(version=VERSION, repo=smoke.EXPECTED_REPO):
    return subprocess.CompletedProcess(
        args=["npm", "view"], returncode=0,
        stdout=json.dumps(metadata(version, repo=repo)), stderr=""
    )


class OfficialNpmSmokePropagationTests(unittest.TestCase):
    def test_registered_old_latest_is_retried_only_when_required(self):
        delays = []
        with mock.patch.object(smoke, "invoke", side_effect=[
            response("1.20.3"), response("1.20.3"), response(VERSION)
        ]) as invoke:
            data = smoke.latest_metadata("npm", VERSION, require_published=True,
                                         attempts=3, pause=delays.append)
        self.assertEqual(data["version"], VERSION)
        self.assertEqual(delays, [2, 4])
        self.assertEqual(invoke.call_count, 3)
        caches = [item.kwargs["env"]["NPM_CONFIG_CACHE"] for item in invoke.call_args_list]
        self.assertEqual(len(set(caches)), 3)
        self.assertTrue(all(item.kwargs["env"]["NPM_CONFIG_PREFER_ONLINE"] == "true"
                            for item in invoke.call_args_list))

    def test_candidate_with_published_older_version_stays_skip(self):
        with mock.patch.object(smoke, "invoke", return_value=response("1.20.3")) as invoke:
            data = smoke.latest_metadata("npm", VERSION, require_published=False,
                                         pause=lambda _: self.fail("Unnecessary retry"))
        self.assertEqual(data["version"], "1.20.3")
        invoke.assert_called_once()

    def test_transient_404_is_retried_when_post_publish_required(self):
        not_found = subprocess.CompletedProcess(["npm"], 1, "", "npm error E404")
        with mock.patch.object(smoke, "invoke", side_effect=[not_found, response()]) as invoke:
            data = smoke.latest_metadata("npm", VERSION, require_published=True,
                                         attempts=2, pause=lambda _: None)
        self.assertEqual(data["version"], VERSION)
        self.assertEqual(invoke.call_count, 2)

    def test_unregistered_candidate_stays_skip(self):
        not_found = subprocess.CompletedProcess(["npm"], 1, "", "npm error E404")
        with mock.patch.object(smoke, "invoke", return_value=not_found) as invoke:
            self.assertIsNone(smoke.latest_metadata("npm", VERSION,
                              require_published=False, pause=lambda _: self.fail("Unexpected delay")))
        invoke.assert_called_once()

    def test_wrong_package_identity_is_hard_failure_without_retry(self):
        with mock.patch.object(smoke, "invoke",
                               return_value=response(repo="https://github.com/other/repo")) as invoke:
            with self.assertRaisesRegex(RuntimeError, "Untrusted npm package identity"):
                smoke.latest_metadata("npm", VERSION, require_published=True,
                                      pause=lambda _: self.fail("Must fail immediately"))
        invoke.assert_called_once()

    def test_unexpected_network_error_is_hard_failure(self):
        network_fail = subprocess.CompletedProcess(["npm"], 1, "", "npm error ECONNRESET")
        with mock.patch.object(smoke, "invoke", return_value=network_fail):
            with self.assertRaisesRegex(RuntimeError, "another reason"):
                smoke.latest_metadata("npm", VERSION, require_published=True,
                                      pause=lambda _: self.fail("Must not retry non-404 failures"))

    def test_stale_latest_timeout_never_claims_success_or_replication_failure(self):
        with mock.patch.object(smoke, "invoke", return_value=response("1.20.3")) as invoke:
            with self.assertRaisesRegex(RuntimeError, "OFFICIAL_NPM_LATEST_READBACK_PENDING"):
                smoke.latest_metadata("npm", VERSION, require_published=True,
                                      attempts=2, pause=lambda _: None)
        self.assertEqual(invoke.call_count, 2)

    def test_npx_latest_version_is_verified_with_fresh_cache_each_retry(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            old = subprocess.CompletedProcess(["npx"], 0, "ui-spec-studio 1.20.3\n", "")
            current = subprocess.CompletedProcess(["npx"], 0, f"ui-spec-studio {VERSION}\n", "")
            with mock.patch.object(smoke, "invoke", side_effect=[old, current]) as invoke:
                env = smoke.resolve_npx_latest("npx", base, VERSION, attempts=2,
                                               pause=lambda _: None)
            self.assertEqual(env["NPM_CONFIG_CACHE"], str(base / "npm-cache-2"))
            self.assertNotEqual(invoke.call_args_list[0].kwargs["env"]["NPM_CONFIG_CACHE"],
                                invoke.call_args_list[1].kwargs["env"]["NPM_CONFIG_CACHE"])
            self.assertTrue(all(item.args[0][:3] == ["npx", "--yes", f"{smoke.NAME}@latest"]
                                for item in invoke.call_args_list))

    def test_npx_latest_wrong_version_is_hard_failure_after_bounded_wait(self):
        with tempfile.TemporaryDirectory() as td:
            old = subprocess.CompletedProcess(["npx"], 0, "ui-spec-studio 1.20.3\n", "")
            with mock.patch.object(smoke, "invoke", return_value=old) as invoke:
                with self.assertRaisesRegex(RuntimeError, "OFFICIAL_NPX_LATEST_READBACK_PENDING"):
                    smoke.resolve_npx_latest("npx", Path(td), VERSION,
                                             attempts=2, pause=lambda _: None)
            self.assertEqual(invoke.call_count, 2)

    def test_no_retry_when_published_version_resolves(self):
        with tempfile.TemporaryDirectory() as td:
            current = subprocess.CompletedProcess(["npx"], 0, f"ui-spec-studio {VERSION}\n", "")
            with mock.patch.object(smoke, "invoke", return_value=current) as invoke:
                smoke.resolve_npx_latest("npx", Path(td), VERSION,
                                         pause=lambda _: self.fail("Unexpected delay"))
            invoke.assert_called_once()


if __name__ == "__main__":
    unittest.main()
