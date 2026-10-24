"""Structural authoring contracts and local safety; these do not measure model quality."""
from __future__ import annotations
import ast
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

from test_tools import ROOT, load, sample, prepare, checker, package, validator


class ContractTests(unittest.TestCase):
    def test_common_references_are_direct_and_complete(self):
        entry = (ROOT / "skills/ui-spec/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("read all seven common references in full", entry)
        for name in validator.COMMON:
            self.assertIn(f"references/{name}.md", entry)
            self.assertGreater((ROOT / f"skills/ui-spec/references/{name}.md").stat().st_size, 500)

    def test_optional_shape_and_integration_are_expressed(self):
        entry = (ROOT / "skills/ui-spec/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("optional `shape`", entry)
        self.assertIn("required for `finish`", entry)
        self.assertIn("The host controls activation", entry)

    def test_all_python_sources_parse(self):
        for path in package.source_files(ROOT):
            if path.suffix == ".py":
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_helper_phase_supports_shape(self):
        with tempfile.TemporaryDirectory() as td:
            data = json.loads((ROOT / "skills/ui-spec/assets/templates/manifest.json").read_text())
            data["phase"] = "shape"
            self.assertTrue(checker.validate(data, Path(td))["ok"])

    def test_preparation_preflights_all_records(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root / ".ui-spec/manifest.json").mkdir(parents=True)
            with self.assertRaises(ValueError):
                prepare.prepare(root)
            self.assertFalse((root / ".ui-spec/brief.md").exists())

    def test_external_design_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as other:
            root = Path(td); design = Path(other) / "DESIGN.md"; design.write_text("private")
            (root / "DESIGN.md").symlink_to(design)
            with self.assertRaisesRegex(ValueError, "inside the project"):
                prepare.prepare(root)
            self.assertFalse((root / ".ui-spec/manifest.json").exists())

    def test_invalid_version_cannot_escape_output(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root / "VERSION").write_text("../escape")
            with self.assertRaises(ValueError):
                package.build(root)

    def test_content_inventory_matches_archives(self):
        with tempfile.TemporaryDirectory() as td:
            result = package.build(ROOT, Path(td))
            inventory = json.loads(result[2].read_text())
            with zipfile.ZipFile(result[0]) as archive:
                for item in inventory["files"]:
                    data = archive.read("ui-spec-studio/" + item["path"])
                    self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])
                    self.assertEqual(len(data), item["bytes"])
                self.assertTrue(all(i.compress_type == zipfile.ZIP_STORED for i in archive.infolist()))

    def test_checksum_manifest_covers_release_artifacts(self):
        with tempfile.TemporaryDirectory() as td:
            result = package.build(ROOT, Path(td))
            for line in result[-1].read_text().splitlines():
                digest, name = line.split("  ")
                self.assertEqual(digest, hashlib.sha256((Path(td) / name).read_bytes()).hexdigest())

    def test_invalid_frontmatter_returns_errors(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for source in package.source_files(ROOT):
                target = root / source.relative_to(ROOT); target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            entry = root / "skills/ui-spec/SKILL.md"
            entry.write_text(entry.read_text(encoding="utf-8").replace('name: ui-spec', 'name: "unterminated'), encoding="utf-8")
            self.assertTrue(validator.validate(root))

    def test_version_metadata_matches_release_notes(self):
        version = (ROOT / "VERSION").read_text().strip()
        self.assertTrue((ROOT / f"docs/releases/v{version}.md").is_file())
        for filename in ("README.md", "README.zh-CN.md"):
            self.assertIn(f"tree/v{version}", (ROOT / filename).read_text(encoding="utf-8"))

    def test_standalone_bundle_has_all_reference_files(self):
        with tempfile.TemporaryDirectory() as td:
            result = package.build(ROOT, Path(td))
            with zipfile.ZipFile(result[1]) as archive:
                for name in (*validator.COMMON, "integration", "examples", "sources"):
                    self.assertIn(f"ui-spec/references/{name}.md", archive.namelist())
