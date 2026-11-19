"""Patch-only Skill metadata must not weaken historical byte identity."""
from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import unittest

from source_continuity import runtime_v119, runtime_v120


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/ui-spec/SKILL.md")
LEDGER = Path("docs/evidence/v1.20.0/continuity.json")


class PatchContinuityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        dest_ledger = self.root / LEDGER
        dest_ledger.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / LEDGER, dest_ledger)
        self.base_version = "1.20.6"
        v120_skill = runtime_v120(ROOT, SKILL.as_posix())
        patched_skill = v120_skill.replace(
            b'  version: "1.20.0"\n',
            ('  version: "' + self.base_version + '"\n').encode("utf-8"),
            1,
        )
        dest_skill = self.root / SKILL
        dest_skill.parent.mkdir(parents=True, exist_ok=True)
        dest_skill.write_bytes(patched_skill)
        (self.root / "VERSION").write_text(self.base_version + "\n", encoding="utf-8")
        self.original_skill = (self.root / SKILL).read_bytes()
        self.assertRegex(self.base_version, r"^1\.20\.[1-9][0-9]*$")
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
        next_patch = 1 + int(self.base_version.split(".")[-1])
        self.replace_version(f"1.20.{next_patch}")
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
        next_patch = 1 + int(self.base_version.split(".")[-1])
        (self.root / "VERSION").write_text(f"1.20.{next_patch}\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Current source differs"):
            runtime_v119(self.root, SKILL.as_posix())


if __name__ == "__main__":
    unittest.main()
