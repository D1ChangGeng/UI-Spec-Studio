"""Structural authoring contracts and local safety; these do not measure model quality."""
from __future__ import annotations
import ast
import copy
import hashlib
import json
import re
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

from test_tools import ROOT, load, sample, prepare, checker, package, validator


class ContractTests(unittest.TestCase):
    def test_common_references_are_direct_and_complete(self):
        entry = (ROOT / "skills/ui-spec/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("read all eight common references in full", entry)
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
            self.assertEqual(checker.validate(data, Path(td))["record_readability"], "readable")

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
            with self.assertRaisesRegex(ValueError, "symlink|inside the project"):
                prepare.prepare(root)
            self.assertFalse((root / ".ui-spec/manifest.json").exists())

    def test_invalid_version_cannot_escape_output(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root / "VERSION").write_text("../escape")
            with self.assertRaises(ValueError):
                package.build(root)

    def test_content_inventory_matches_archives(self):
        with tempfile.TemporaryDirectory() as td:
            result = package.build(ROOT, Path(td), include_evidence=False)
            inventory_path = next(path for path in result if path.name == "contents.json")
            inventory = json.loads(inventory_path.read_text())
            with zipfile.ZipFile(result[0]) as archive:
                for item in inventory["files"]:
                    data = archive.read("ui-spec-studio/" + item["path"])
                    self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])
                    self.assertEqual(len(data), item["bytes"])
                self.assertTrue(all(i.compress_type == zipfile.ZIP_STORED for i in archive.infolist()))

    def test_checksum_manifest_covers_release_artifacts(self):
        with tempfile.TemporaryDirectory() as td:
            result = package.build(ROOT, Path(td), include_evidence=False)
            for line in result[-1].read_text().splitlines():
                digest, name = line.split("  ")
                self.assertEqual(digest, hashlib.sha256((Path(td) / name).read_bytes()).hexdigest())

    def test_invalid_frontmatter_returns_errors(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for source in package.source_files(ROOT):
                rel = source.relative_to(ROOT)
                if rel.parts[:2] in (('docs', 'evidence'), ('docs', 'experiments')):
                    continue
                target = root / rel; target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            entry = root / "skills/ui-spec/SKILL.md"
            entry.write_text(entry.read_text(encoding="utf-8").replace('name: ui-spec', 'name: "unterminated'), encoding="utf-8")
            self.assertIn("Invalid scalar: name", validator.validate(root))

    def test_version_metadata_matches_release_notes(self):
        version = (ROOT / "VERSION").read_text().strip()
        self.assertTrue((ROOT / f"docs/releases/v{version}.md").is_file())
        for filename in ("README.md", "README.zh-CN.md"):
            self.assertIn(f"releases/download/v{version}/ui-spec-installer.tgz", (ROOT / filename).read_text(encoding="utf-8"))

    def test_official_npm_is_first_documented_install_command(self):
        # Prevent stale GitHub-tarball-first READMEs after npm is public.
        for filename in ("README.md", "README.zh-CN.md", "docs/INSTALL.md", "docs/NPM-DISTRIBUTION.md"):
            body = (ROOT / filename).read_text(encoding="utf-8")
            first = re.search(r"```(?:bash|powershell)\s*\n([^\r\n]+)", body)
            self.assertIsNotNone(first, f"No installation code block in {filename}")
            self.assertEqual(first.group(1).strip(), "npx --yes ui-spec-studio@latest", filename)

    def test_primary_distribution_urls_are_version_consistent(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        url = re.compile(
            r"https://github\.com/D1ChangGeng/UI-Spec-Studio/releases/download/"
            r"(v\d+\.\d+\.\d+)/"
            r"(ui-spec(?:-codex)?-\d+\.\d+\.\d+\.zip|ui-spec-installer\.tgz)"
        )
        for filename in ("README.md", "README.zh-CN.md", "docs/INSTALL.md", "docs/NPM-DISTRIBUTION.md"):
            body = (ROOT / filename).read_text(encoding="utf-8")
            links = url.findall(body)
            self.assertTrue(links, f"No release links found in {filename}")
            for tag, asset in links:
                self.assertEqual(tag, "v" + version, f"Outdated release link in {filename}")
                if asset != "ui-spec-installer.tgz":
                    self.assertIn(version, asset, f"ZIP filename and release tag differ in {filename}")

    def test_standalone_bundle_has_all_reference_files(self):
        with tempfile.TemporaryDirectory() as td:
            result = package.build(ROOT, Path(td), include_evidence=False)
            with zipfile.ZipFile(result[1]) as archive:
                for name in (*validator.COMMON, "integration", "examples", "sources"):
                    self.assertIn(f"ui-spec/references/{name}.md", archive.namelist())
