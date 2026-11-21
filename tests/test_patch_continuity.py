"""Patch-only Skill metadata must not weaken historical byte identity."""
from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import unittest

from source_continuity import runtime_v119, runtime_v120


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/ui-spec/SKILL.md")
LEDGER_V120 = Path("docs/evidence/v1.20.0/continuity.json")
LEDGER_V121 = Path("docs/evidence/v1.21.0/continuity.json")


class PatchContinuityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        ledger_dest = self.root / LEDGER_V120
        ledger_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / LEDGER_V120, ledger_dest)
        skill_dest = self.root / SKILL
        skill_dest.parent.mkdir(parents=True, exist_ok=True)
        skill_dest.write_bytes(runtime_v120(ROOT, SKILL.as_posix()))
        (self.root / "VERSION").write_text("1.20.6\n", encoding="utf-8")
        self.original_skill = (self.root / SKILL).read_bytes()
        self.base_version = (self.root / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(self.base_version, r"^1\.20\.[1-9][0-9]*$")
        self.expected = runtime_v119(ROOT, SKILL.as_posix())

    def replace_version(self, new_version: str):
        before = ('  version: "' + self.base_version + '"\n').encode("utf-8")
        after = ('  version: "' + new_version + '"\n').encode("utf-8")
        self.assertEqual(self.original_skill.count(before), 1)
        (self.root / SKILL).write_bytes(self.original_skill.replace(before, after, 1))
        (self.root / "VERSION").write_text(new_version + "\n", encoding="utf-8")

    def test_current_patch_metadata_recovers_exact_prior_bytes(self):
        self.assertEqual(runtime_v119(self.root, SKILL.as_posix()), self.expected)

    def test_later_patch_metadata_remains_reconstructable(self):
        for candidate in ("1.20.2", f"1.20.{1 + int(self.base_version.split('.')[-1])}", "1.20.12"):
            with self.subTest(version=candidate):
                self.replace_version(candidate)
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


class PatchContinuityV121Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for path in [SKILL, LEDGER_V120, LEDGER_V121]:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, dest)
        shutil.copyfile(ROOT / "VERSION", self.root / "VERSION")
        self.original_skill = (self.root / SKILL).read_bytes()
        self.base_version = (self.root / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(self.base_version, r"^1\.21\.(0|[1-9][0-9]*)$")
        self.expected_v120 = runtime_v120(ROOT, SKILL.as_posix())
        self.expected_v119 = runtime_v119(ROOT, SKILL.as_posix())

    def replace_version(self, new_version: str):
        before = ('  version: "' + self.base_version + '"\n').encode("utf-8")
        after = ('  version: "' + new_version + '"\n').encode("utf-8")
        self.assertEqual(self.original_skill.count(before), 1)
        (self.root / SKILL).write_bytes(self.original_skill.replace(before, after, 1))
        (self.root / "VERSION").write_text(new_version + "\n", encoding="utf-8")

    def test_current_v121_recovers_exact_v120_and_v119_bytes(self):
        self.assertEqual(runtime_v120(self.root, SKILL.as_posix()), self.expected_v120)
        self.assertEqual(runtime_v119(self.root, SKILL.as_posix()), self.expected_v119)

    def test_v121_patch_metadata_remains_reconstructable(self):
        for candidate in ("1.21.1", "1.21.12"):
            with self.subTest(version=candidate):
                self.replace_version(candidate)
                self.assertEqual(runtime_v120(self.root, SKILL.as_posix()), self.expected_v120)
                self.assertEqual(runtime_v119(self.root, SKILL.as_posix()), self.expected_v119)

    def test_other_minor_version_not_normalized(self):
        self.replace_version("1.22.0")
        with self.assertRaisesRegex(ValueError, "Current source differs"):
            runtime_v120(self.root, SKILL.as_posix())
        with self.assertRaisesRegex(ValueError, "Current source differs"):
            runtime_v119(self.root, SKILL.as_posix())

    def test_body_drift_in_skill_is_rejected(self):
        (self.root / SKILL).write_bytes(self.original_skill + b"\nUnreviewed body drift\n")
        with self.assertRaisesRegex(ValueError, "Current source differs"):
            runtime_v120(self.root, SKILL.as_posix())
        with self.assertRaisesRegex(ValueError, "Current source differs"):
            runtime_v119(self.root, SKILL.as_posix())

    def test_version_and_skill_metadata_must_agree(self):
        (self.root / "VERSION").write_text("1.21.1\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Current source differs"):
            runtime_v120(self.root, SKILL.as_posix())
        (self.root / "VERSION").write_text("1.21.0\n", encoding="utf-8")
        (self.root / SKILL).write_bytes(
            self.original_skill.replace(b'  version: "1.21.0"\n', b'  version: "1.21.1"\n', 1)
        )
        with self.assertRaisesRegex(ValueError, "Current source differs"):
            runtime_v120(self.root, SKILL.as_posix())


if __name__ == "__main__":
    unittest.main()

