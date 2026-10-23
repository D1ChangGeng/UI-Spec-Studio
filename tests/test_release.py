"""Release boundary tests with an explicit simulated remote; no network operations."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_under_test", ROOT / "tools/publish.py")
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)
SHA = "a" * 40


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "VERSION").write_text("1.1.0\n")
        (self.root / "docs/releases").mkdir(parents=True)
        (self.root / "docs/releases/v1.1.0.md").write_text("Release notes")
        (self.root / "dist").mkdir()
        self.assets = [self.root / "dist/test.zip", self.root / "dist/SHA256SUMS.txt"]
        for file in self.assets:
            file.write_text("deterministic test asset", encoding="utf-8")
        self.dirty = False
        self.identity = "D1ChangGeng/UI-Spec-Studio"
        self.head = SHA
        self.remote_head = SHA
        self.tag_head = SHA
        self.tag_exists = True
        self.existing = False
        self.draft = True
        self.corrupt = False
        self.commands = []
        for patcher in (
            mock.patch.object(publisher, "ROOT", self.root),
            mock.patch.object(publisher, "validate", return_value=[]),
            mock.patch.object(publisher, "build", return_value=self.assets),
            mock.patch.object(publisher.shutil, "which", return_value="tool"),
            mock.patch.object(publisher, "command", side_effect=self.run_command),
        ):
            patcher.start(); self.addCleanup(patcher.stop)

    def run_command(self, args, cwd, check=True):
        self.commands.append(args)
        result = ""
        code = 0
        if args[:3] == ["git", "status", "--porcelain"]:
            result = " M file" if self.dirty else ""
        elif args[:2] == ["git", "rev-parse"]:
            result = self.head
        elif args[:3] == ["gh", "repo", "view"]:
            result = self.identity
        elif args[:2] == ["gh", "api"]:
            if args[2].endswith("/git/refs"):
                self.tag_exists = True
                result = "{}"
            elif args[2].endswith("/v1.1.0"):
                result = self.tag_head
                code = 0 if self.tag_exists else 1
            else:
                result = self.remote_head
        elif args[:3] == ["gh", "release", "view"]:
            code = 0 if self.existing else 1
            result = json.dumps({"isDraft": self.draft, "tagName": "v1.1.0", "url": "https://example.test/release"})
        elif args[:3] == ["gh", "release", "create"]:
            self.existing = True
        elif args[:3] == ["gh", "release", "download"]:
            out = Path(args[args.index("--dir") + 1])
            for asset in self.assets:
                shutil.copyfile(asset, out / asset.name)
            if self.corrupt:
                (out / self.assets[0].name).write_text("changed")
        elif args[:3] == ["gh", "release", "edit"]:
            self.draft = False
        return subprocess.CompletedProcess(args, code, result, "")

    def publish(self):
        return publisher.publish("D1ChangGeng", "UI-Spec-Studio")

    def test_clean_draft_is_read_back_before_publication(self):
        result = self.publish()
        self.assertEqual(result["asset_readback"], "sha256-verified")
        download = next(i for i, a in enumerate(self.commands) if a[:3] == ["gh", "release", "download"])
        edit = next(i for i, a in enumerate(self.commands) if a[:3] == ["gh", "release", "edit"])
        self.assertLess(download, edit)

    def test_dirty_checkout_is_preserved(self):
        self.dirty = True
        with self.assertRaisesRegex(ValueError, "clean committed"):
            self.publish()
        self.assertFalse(any(a[0] == "gh" for a in self.commands))

    def test_repository_identity_is_checked(self):
        self.identity = "someone/other"
        with self.assertRaisesRegex(ValueError, "identity"):
            self.publish()

    def test_remote_commit_is_checked(self):
        self.remote_head = "b" * 40
        with self.assertRaisesRegex(ValueError, "Current commit"):
            self.publish()

    def test_exact_head_required(self):
        self.head = "main"
        with self.assertRaisesRegex(ValueError, "exact Git"):
            self.publish()

    def test_conflicting_tag_is_preserved_before_release_write(self):
        self.tag_head = "b" * 40
        with self.assertRaisesRegex(ValueError, "different commit"):
            self.publish()
        self.assertFalse(any(a[:3] == ["gh", "release", "create"] for a in self.commands))

    def test_corrupt_asset_keeps_draft(self):
        self.corrupt = True
        with self.assertRaisesRegex(ValueError, "asset readback"):
            self.publish()
        self.assertTrue(self.draft)
        self.assertFalse(any(a[:3] == ["gh", "release", "edit"] for a in self.commands))

    def test_published_matching_release_is_idempotent(self):
        self.existing = True; self.draft = False
        self.assertEqual(self.publish()["commit"], SHA)
        self.assertFalse(any(a[:3] in (["gh", "release", "create"], ["gh", "release", "edit"]) for a in self.commands))

    def test_existing_draft_is_verified_and_published(self):
        self.existing = True
        self.assertEqual(self.publish()["tag"], "v1.1.0")
        self.assertFalse(self.draft)

    def test_version_paths_are_validated(self):
        (self.root / "VERSION").write_text("../../elsewhere")
        with self.assertRaisesRegex(ValueError, "VERSION"):
            publisher.plan("D1ChangGeng", "UI-Spec-Studio")

    def test_release_notes_are_required(self):
        (self.root / "docs/releases/v1.1.0.md").unlink()
        with self.assertRaisesRegex(ValueError, "release notes"):
            self.publish()

    def test_missing_tool_is_reported(self):
        with mock.patch.object(publisher.shutil, "which", return_value=None):
            with self.assertRaisesRegex(RuntimeError, "Install"):
                self.publish()

    def test_new_tag_is_created_before_draft(self):
        self.tag_exists = False
        self.assertEqual(self.publish()["commit"], SHA)
        tag_create = next(i for i, a in enumerate(self.commands) if a[:2] == ["gh", "api"] and a[2].endswith("/git/refs"))
        draft_create = next(i for i, a in enumerate(self.commands) if a[:3] == ["gh", "release", "create"])
        self.assertLess(tag_create, draft_create)
        self.assertIn("--verify-tag", self.commands[draft_create])
