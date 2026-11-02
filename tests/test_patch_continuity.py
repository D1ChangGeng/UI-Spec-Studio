"""Patch-only Skill metadata must not weaken historical byte identity."""
from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import unittest

from source_continuity import runtime_v119


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/ui-spec/SKILL.md")
LEDGER = Path("docs/evidence/v1.20.0/continuity.json")


class PatchContinuityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for path in [SKILL, LEDGER]:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, dest)
        shutil.copyfile(ROOT / "VERSION", self.root / "VERSION")
        self.original_skill = (self.root / SKILL).read_bytes()
        self.base_version = (self.root / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(self.base_version, "1.20.4")
        self.expected = runtime_v119(ROOT, SKILL.as_posix())

    def replace_version(self, new_version: str):
        before = ('  version: "' + self.base_version + '"\n').encode()
        after = ('  version: "' + new_version + '"\n').encode()
        self.assertEqual(self.original_skill.count(before), 1)
        (self.root / SKILL).write_bytes(self.original_skill.replace(before, after, 1))
        (self.root / "VERSION").write_text(new_version + "\n", encoding="utf-8")

    def test_current_patch_metadata_recovers_exact_prior_bytes(self):
        self.assertEqual(runtime_v119(self.root, SKILL.as_posix()), self.expected)

    def test_later_patch_metadata_remains_reconstructable(self):
        self.replace_version("1.20.14")
        self.assertEqual(runtime_v119(self.root, SKILL.as_posix()), self.expected)

    def test_other_minor_version_not_normalized(self):
        self.replace_version("1.21.0")
        with self.assertRaisesRegex(ValueError, "Current source differs"):
            runtime_v119(self.root, SKILL.as_posix())

    def test_any_other_unreviewed_change_is_rejected(self):
        (self.root / SKILL).write_bytes(self.original_skill + b"\nUnreviewed change\n")
        with self.assertRaisesRegex(ValueError, "Current source differs"):
            runtime_v119(self.root, SKILL.as_posix())

    def test_version_and_skill_metadata_must_agree(self):
        (self.root / "VERSION").write_text("1.20.5\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Current source differs"):
            runtime_v119(self.root, SKILL.as_posix())


if __name__ == "__main__":
    unittest.main()
