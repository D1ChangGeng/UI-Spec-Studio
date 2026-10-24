"""Deterministic tool tests. Evidence fixtures here are not actual UI reviews."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prepare = load("prepare", "skills/ui-spec/scripts/prepare.py")
checker = load("checker", "skills/ui-spec/scripts/check_manifest.py")
package = load("bundle", "tools/package.py")
installer = load("local_install", "tools/install_local.py")
validator = load("validator", "tools/validate_package.py")
publisher = load("publisher", "tools/publish.py")


def sample() -> dict:
    return {
        "schema_version": 1, "project": "Test fixture", "phase": "iterate", "revision": "code-1",
        "design_revision": "design-1", "design_system_path": None,
        "viewports": [{"id": "desktop", "width": 1440, "height": 900}],
        "variants": [{"id": "default", "locale": "en", "theme": "light"}],
        "routes": [{"id": "home", "path": "/", "purpose": "Read the guide", "primary_state": "ready",
                    "states": ["ready", "error"], "critical_states": []}],
        "journeys": [{"id": "read", "routes": ["home"], "outcome": "Read the guide and use its links"}],
        "requirements": [], "checks": [
            {"id": "home-visual", "kind": "visual", "route": "home", "state": "ready", "viewport": "desktop",
             "variant": "default", "status": "pass", "revision": "code-1", "reviewer": "unit-test-fixture",
             "inspected": True, "evidence": ["evidence/test-only.txt"]},
            {"id": "read-journey", "kind": "journey", "journey": "read", "variant": "default", "status": "pass",
             "revision": "code-1", "reviewer": "unit-test-fixture", "outcome": "Synthetic fixture outcome",
             "evidence": ["evidence/test-only.txt"]}],
        "approvals": [], "connections": [], "exceptions": []}


def finish(data: dict, mode: str = "static") -> None:
    data["phase"] = "finish"
    data["approvals"] = [{"routes": ["home"], "revision": "design-1", "by": "test-fixture",
                          "reference": "Synthetic approval for deterministic testing"}]
    data["checks"].append({"id": "home-integrated", "kind": "integration", "route": "home", "status": "pass",
                           "revision": "code-1", "reviewer": "unit-test-fixture", "outcome": "Synthetic connection result",
                           "data_mode": mode, "evidence": ["evidence/test-only.txt"]})
    data["connections"] = [{"route": "home", "mode": mode, "owner": "Test boundary", "contract": "Test contract",
                            "check_ids": ["home-integrated"]}]


class TempCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)


class PrepareTests(TempCase):
    def test_creates_only_small_records(self):
        result = prepare.prepare(self.root, "Example")
        self.assertEqual(len(result["created"]), 3)
        self.assertFalse((self.root / "DESIGN.md").exists())
        self.assertEqual(json.loads((self.root / ".ui-spec/manifest.json").read_text())["project"], "Example")

    def test_preserves_existing_records(self):
        prepare.prepare(self.root)
        brief = self.root / ".ui-spec/brief.md"
        brief.write_text("User-owned decisions")
        result = prepare.prepare(self.root, "Another")
        self.assertEqual(result["created"], [])
        self.assertEqual(brief.read_text(), "User-owned decisions")

    def test_reuses_design_reference(self):
        (self.root / "DESIGN.md").write_text("Existing design")
        prepare.prepare(self.root)
        data = json.loads((self.root / ".ui-spec/manifest.json").read_text())
        self.assertEqual(data["design_system_path"], "DESIGN.md")

    def test_requires_existing_project(self):
        with self.assertRaises(FileNotFoundError):
            prepare.prepare(self.root / "absent")

    def test_rejects_symlink_state_dir(self):
        other = self.root / "other"
        other.mkdir()
        (self.root / ".ui-spec").symlink_to(other, target_is_directory=True)
        with self.assertRaises(ValueError):
            prepare.prepare(self.root)

    def test_rejects_symlink_record(self):
        (self.root / ".ui-spec").mkdir()
        (self.root / "user-file").write_text("private")
        (self.root / ".ui-spec/brief.md").symlink_to(self.root / "user-file")
        with self.assertRaises(ValueError):
            prepare.prepare(self.root)
        self.assertEqual((self.root / "user-file").read_text(), "private")


class ManifestTests(TempCase):
    def setUp(self):
        super().setUp()
        (self.root / "evidence").mkdir()
        (self.root / "evidence/test-only.txt").write_text("Synthetic unit-test evidence; not a rendered UI.")
        self.data = sample()

    def check(self, mode="review"):
        return checker.validate(self.data, self.root, mode)

    def test_complete_review(self):
        result = self.check()
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["coverage"]["required"], 2)
        self.assertIn("does not run a browser", result["limits"])

    def test_draft_reports_pending(self):
        for check in self.data["checks"]:
            check["status"] = "planned"
        result = self.check("draft")
        self.assertTrue(result["ok"])
        self.assertEqual(len(result["coverage"]["pending"]), 2)
        self.assertFalse(self.check()["ok"])

    def test_empty_inventory_only_draft(self):
        data = json.loads((ROOT / "skills/ui-spec/assets/templates/manifest.json").read_text())
        self.assertTrue(checker.validate(data, self.root, "draft")["ok"])
        self.assertFalse(checker.validate(data, self.root, "review")["ok"])

    def test_secondary_viewport_required(self):
        self.data["viewports"].append({"id": "wide", "width": 2560, "height": 1440})
        self.assertIn("visual:home:ready:wide:default", self.check()["coverage"]["pending"])

    def test_secondary_variant_required(self):
        self.data["variants"].append({"id": "dark", "locale": "en", "theme": "dark"})
        self.assertEqual(len(self.check()["coverage"]["pending"]), 2)

    def test_critical_state_required(self):
        self.data["routes"][0]["critical_states"] = ["error"]
        self.assertIn("critical:home:error:default", self.check()["coverage"]["pending"])

    def test_critical_state_can_use_one_viewport(self):
        self.data["routes"][0]["critical_states"] = ["error"]
        c = copy.deepcopy(self.data["checks"][0]);c.update(id="error-visual", state="error")
        self.data["checks"].append(c)
        self.assertTrue(self.check()["ok"])

    def test_explicit_requirement(self):
        self.data["requirements"] = [{"route": "home", "state": "error", "viewport": "desktop", "variant": "default"}]
        self.assertFalse(self.check()["ok"])

    def test_unknown_reference(self):
        self.data["checks"][0]["route"] = "missing"
        self.assertFalse(self.check()["ok"])

    def test_duplicate_ids(self):
        self.data["routes"].append(copy.deepcopy(self.data["routes"][0]))
        self.assertFalse(self.check()["ok"])

    def test_duplicate_targets(self):
        c = copy.deepcopy(self.data["checks"][0]);c["id"]="duplicate"
        self.data["checks"].append(c)
        self.assertFalse(self.check()["ok"])

    def test_stale_evidence(self):
        self.data["revision"] = "code-2"
        self.assertFalse(self.check()["ok"])

    def test_missing_evidence(self):
        self.data["checks"][0]["evidence"] = ["missing.png"]
        self.assertFalse(self.check()["ok"])

    def test_empty_evidence(self):
        (self.root / "empty.png").touch()
        self.data["checks"][0]["evidence"] = ["empty.png"]
        self.assertFalse(self.check()["ok"])

    def test_visual_requires_inspection(self):
        self.data["checks"][0]["inspected"] = False
        self.assertFalse(self.check()["ok"])

    def test_reviewer_required(self):
        del self.data["checks"][0]["reviewer"]
        self.assertFalse(self.check()["ok"])

    def test_absolute_evidence_rejected(self):
        self.data["checks"][0]["evidence"] = [str(self.root / "evidence/test-only.txt")]
        self.assertFalse(self.check()["ok"])

    def test_escaping_symlink_evidence_rejected(self):
        with tempfile.TemporaryDirectory() as ext:
            p = Path(ext) / "secret";p.write_text("not evidence")
            (self.root / "linked.txt").symlink_to(p)
            self.data["checks"][0]["evidence"] = ["linked.txt"]
            self.assertFalse(self.check()["ok"])

    def test_blocked_is_pending(self):
        self.data["checks"][0].update(status="blocked", reason="Browser unavailable")
        self.assertFalse(self.check()["ok"])

    def test_waiver_needs_explicit_reference(self):
        self.data["checks"][0]["status"] = "waived"
        self.assertFalse(self.check()["ok"])
        self.data["exceptions"] = [{"target": "visual:home:ready:desktop:default", "reason": "Synthetic exclusion",
                                    "approved_by": "fixture", "reference": "Fixture decision"}]
        self.assertTrue(self.check()["ok"])

    def test_finish_requires_approval_and_connection(self):
        self.assertFalse(self.check("finish")["ok"])

    def test_finish_static_service_local(self):
        for mode in ("static", "service", "local"):
            with self.subTest(mode=mode):
                data = sample();finish(data, mode)
                result = checker.validate(data, self.root, "finish")
                self.assertTrue(result["ok"], result)

    def test_finish_fixture_is_not_integration(self):
        finish(self.data, "fixture")
        self.assertFalse(self.check("finish")["ok"])

    def test_approved_design_can_differ_from_code(self):
        finish(self.data)
        self.assertNotEqual(self.data["revision"], self.data["design_revision"])
        self.assertTrue(self.check("finish")["ok"])

    def test_wrong_approval_revision(self):
        finish(self.data);self.data["approvals"][0]["revision"]="other"
        self.assertFalse(self.check("finish")["ok"])

    def test_wrong_connection_mode(self):
        finish(self.data);self.data["connections"][0]["mode"]="service"
        self.assertFalse(self.check("finish")["ok"])

    def test_wrong_connection_check(self):
        finish(self.data);self.data["connections"][0]["check_ids"]=["home-visual"]
        self.assertFalse(self.check("finish")["ok"])

    def test_finish_requires_journey(self):
        finish(self.data);self.data["journeys"]=[];self.data["checks"].pop(1)
        self.assertFalse(self.check("finish")["ok"])

    def test_malformed_fields_report_errors(self):
        for field, value in (("phase", []), ("routes", "wrong"), ("schema_version", True)):
            with self.subTest(field=field):
                data=copy.deepcopy(self.data);data[field]=value
                self.assertFalse(checker.validate(data,self.root)["ok"])
        self.data["routes"][0]["primary_state"] = []
        self.assertFalse(self.check()["ok"])

    def test_cli_json_and_exit_codes(self):
        path=self.root / "manifest.json";path.write_text(json.dumps(self.data))
        script=ROOT / "skills/ui-spec/scripts/check_manifest.py"
        result=subprocess.run([sys.executable,str(script),"--project-root",str(self.root),"--manifest","manifest.json",
                               "--mode","review","--json"],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertTrue(json.loads(result.stdout)["ok"])
        path.write_text("not JSON")
        result=subprocess.run([sys.executable,str(script),"--project-root",str(self.root),"--manifest","manifest.json"],
                               capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertNotIn("Traceback", result.stderr)


class DistributionTests(TempCase):
    def test_package_structure(self):
        self.assertEqual(validator.validate(ROOT), [])

    def test_install_preserves_existing(self):
        target=self.root / "ui-spec";target.mkdir();(target/"SKILL.md").write_text("user")
        with self.assertRaises(FileExistsError):
            installer.install(target)
        self.assertEqual((target/"SKILL.md").read_text(),"user")

    def test_installed_scripts_work_from_other_project(self):
        for hostpath in (".agents/skills/ui-spec", ".claude/skills/ui-spec"):
            with self.subTest(hostpath=hostpath):
                project=self.root / hostpath.split('/')[0].strip('.');project.mkdir()
                target=project / hostpath
                installer.install(target)
                self.assertTrue((target / "references/integration.md").is_file())
                self.assertTrue((target / "LICENSE").is_file())
                result=subprocess.run([sys.executable,str(target/"scripts/prepare.py"),"--project-root",str(project)],
                                      cwd=self.root,capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)
                result=subprocess.run([sys.executable,str(target/"scripts/check_manifest.py"),"--project-root",str(project),"--mode","draft"],
                                      cwd=self.root,capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)

    def test_install_rejects_nested_target(self):
        with self.assertRaises(ValueError):
            installer.install(ROOT / "skills/ui-spec/nested-install")

    def test_reproducible_archives(self):
        first=package.build(ROOT,self.root / "one")
        second=package.build(ROOT,self.root / "two")
        self.assertEqual([p.read_bytes() for p in first],[p.read_bytes() for p in second])
        with zipfile.ZipFile(first[1]) as z:
            self.assertIn("ui-spec/SKILL.md",z.namelist())
            self.assertIn("ui-spec/LICENSE",z.namelist())
            self.assertTrue(all("__pycache__" not in p for p in z.namelist()))

    def test_package_excludes_secrets_and_symlinks(self):
        (self.root / "README.md").write_text("readme")
        (self.root / ".env").write_text("private")
        (self.root / "tools").mkdir()
        (self.root / "tools/helper.py").write_text("pass")
        (self.root / "tools/link.py").symlink_to(self.root/".env")
        names=[p.relative_to(self.root).as_posix() for p in package.source_files(self.root)]
        self.assertEqual(names,["README.md","tools/helper.py"])

    def test_publish_plan_is_nonmutating(self):
        with mock.patch.object(publisher,"command",side_effect=AssertionError("unexpected command")):
            plan=publisher.plan("D1ChangGeng","ui-spec-studio")
        self.assertEqual(plan["tag"],"v"+(ROOT/"VERSION").read_text().strip())
        self.assertIn("skills/ui-spec/SKILL.md",plan["source_files"])

    def test_publish_rejects_bad_destination(self):
        with self.assertRaises(ValueError):
            publisher.plan("bad/owner","repo")
        with self.assertRaises(ValueError):
            publisher.plan("owner","../repo")


if __name__ == "__main__":
    unittest.main()
