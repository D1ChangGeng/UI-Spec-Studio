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
sys.path.insert(0, str(ROOT / "skills/ui-spec/scripts"))


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
    """Declared record tests, deliberately not phase-completion or design tests."""
    def setUp(self):
        super().setUp()
        (self.root / "evidence").mkdir()
        (self.root / "evidence/test-only.txt").write_text("Synthetic test marker, not visual evidence.")
        self.data = sample()

    def check(self, view="overview"):
        return checker.inspect_record(self.data, self.root, view)

    def codes(self, result=None):
        return [x["code"] for x in (result or self.check())["structural_findings"]]

    def test_record_readability_does_not_certify_quality(self):
        result=self.check()
        self.assertEqual(result["record_readability"], "readable")
        self.assertNotIn("ok", result)
        self.assertNotIn("coverage", result)
        self.assertEqual(len(result["declared_check_records"]), 2)

    def test_planned_is_recorded_not_completed(self):
        for check in self.data["checks"]: check["status"]="planned"
        self.assertEqual(len(self.check()["declared_check_records"]), 2)
        for mode in ("draft", "review", "finish"):
            self.assertEqual(checker.validate(self.data,self.root,mode)["record_readability"],"readable")

    def test_empty_inventory_readable_in_every_view(self):
        data=json.loads((ROOT / "skills/ui-spec/assets/templates/manifest.json").read_text())
        for view in ("overview", "checks", "connections"):
            result=checker.inspect_record(data,self.root,view)
            self.assertEqual(result["record_readability"],"readable")
            self.assertFalse(result["structural_findings"])

    def test_secondary_viewport_is_inventory_projection_not_requirement(self):
        self.data["viewports"].append({"id":"wide","width":2560,"height":1440})
        result=self.check()
        self.assertIn("visual:home:ready:wide:default",[x["target"] for x in result["inventory_combinations"]["unlisted"]])
        self.assertFalse(result["unlisted_declared_items"])
        self.assertEqual(result["inventory_combinations"]["task_applicability"],"not_assessed")

    def test_secondary_variant_is_projection_only(self):
        self.data["variants"].append({"id":"dark","locale":"en","theme":"dark"})
        self.assertFalse(self.check()["structural_findings"])
        self.assertTrue(self.check()["inventory_combinations"]["unlisted"])

    def test_critical_state_does_not_create_completion_gate(self):
        self.data["routes"][0]["critical_states"]=["error"]
        result=self.check("connections")
        self.assertIn("critical:home:error:default",[x["target"] for x in result["inventory_combinations"]["unlisted"]])
        self.assertFalse(result["structural_findings"])

    def test_critical_state_matching_is_status_independent(self):
        self.data["routes"][0]["critical_states"]=["error"]
        c=copy.deepcopy(self.data["checks"][0]);c.update(id="error-visual",state="error",status="fail")
        self.data["checks"].append(c)
        row=next(x for x in self.check()["inventory_combinations"]["items"] if x["target"].startswith("critical:"))
        self.assertEqual(row["check_record_fields"],["$.checks[2]"])

    def test_explicit_unlisted_requirement(self):
        self.data["requirements"]=[{"route":"home","state":"error","viewport":"desktop","variant":"default"}]
        self.assertEqual(len(self.check()["unlisted_declared_items"]),1)
        self.assertFalse(self.check()["structural_findings"])

    def test_unknown_reference(self):
        self.data["checks"][0]["route"]="missing"
        self.assertIn("unresolved_reference",self.codes())

    def test_duplicate_ids(self):
        self.data["routes"].append(copy.deepcopy(self.data["routes"][0]))
        self.assertIn("duplicate_id",self.codes())

    def test_multiple_results_per_target_remain_distinct_records(self):
        c=copy.deepcopy(self.data["checks"][0]);c.update(id="retest",status="fail",revision="r2")
        self.data["checks"].append(c)
        result=self.check()
        self.assertEqual(len(result["declared_check_records"]),3)
        self.assertFalse(result["structural_findings"])

    def test_global_revision_change_does_not_invalidate_history(self):
        self.data["revision"]="code-2"
        result=self.check()
        self.assertFalse(result["structural_findings"])
        self.assertIn("code-1",[x["declared_revision"] for x in result["revision_declarations"]])

    def test_missing_file_is_reported_without_rewriting_status(self):
        self.data["checks"][0]["evidence"]=["missing.png"]
        result=self.check()
        self.assertIn("local_file_reference",self.codes(result))
        self.assertEqual(result["declared_check_records"][0]["declared_status"],"pass")

    def test_empty_file_reported_as_zero_bytes(self):
        (self.root / "empty.png").touch();self.data["checks"][0]["evidence"]=["empty.png"]
        result=self.check()
        self.assertEqual(result["file_observations"][0]["bytes"],0)
        self.assertEqual(result["file_observations"][0]["content_inspection"],"not_performed")

    def test_uninspected_file_not_certified(self):
        self.data["checks"][0]["inspected"]=False
        self.assertFalse(self.check()["structural_findings"])
        self.assertFalse(self.check()["declared_check_records"][0]["record"]["inspected"])

    def test_missing_reviewer_is_field_observation_only(self):
        del self.data["checks"][0]["reviewer"]
        result=self.check()
        self.assertIn({"path":"$.checks[0].reviewer","presence":"not_declared"},result["field_observations"])
        self.assertFalse(result["structural_findings"])

    def test_absolute_path_not_inspected(self):
        self.data["checks"][0]["evidence"]=[str(self.root / "evidence/test-only.txt")]
        self.assertIn("path_not_inspected",self.codes())

    def test_symlink_path_not_inspected(self):
        try: (self.root / "linked").symlink_to(self.root / "evidence/test-only.txt")
        except (OSError,NotImplementedError): self.skipTest("Symlinks unavailable")
        self.data["checks"][0]["evidence"]=["linked"]
        self.assertIn("path_not_inspected",self.codes())

    def test_blocked_state_does_not_change_query_exit_semantics(self):
        self.data["checks"][0].update(status="blocked",reason="No browser")
        self.assertFalse(self.check("finish")["structural_findings"])

    def test_waiver_and_exception_are_separate_from_check_results(self):
        self.data["checks"][0]["status"]="waived"
        self.data["exceptions"]=[{"target":"visual:home:ready:desktop:default","reason":"Fixture scope","approved_by":"fixture","reference":"fixture"}]
        result=self.check()
        self.assertEqual(len(result["declared_check_records"]),1)
        self.assertEqual(len(result["declared_waived_check_records"]),1)
        self.assertEqual(len(result["declared_exceptions"]),1)
        self.assertNotIn("satisfied",json.dumps(result))

    def test_finish_alias_does_not_require_approval_or_connection(self):
        result=self.check("finish")
        self.assertEqual(result["query_view"],"connections")
        self.assertEqual(result["declared_approvals"],[])
        self.assertEqual(result["structural_findings"],[])

    def test_connections_resolve_any_status_without_certifying(self):
        for mode in ("static","service","local"):
            data=sample();finish(data,mode);data["checks"][-1]["status"]="fail"
            result=checker.inspect_record(data,self.root,"connections")
            self.assertFalse(result["structural_findings"])
            self.assertEqual(result["declared_check_records"][-1]["declared_status"],"fail")

    def test_connection_unknown_check_is_unresolved_reference(self):
        finish(self.data);self.data["connections"][0]["check_ids"]=["missing"]
        self.assertIn("unresolved_reference",self.codes())

    def test_approval_revision_is_not_globally_compared(self):
        finish(self.data);self.data["approvals"][0]["revision"]="old-accepted-design"
        self.assertFalse(self.check("connections")["structural_findings"])

    def test_malformed_fields_are_reported_not_crashes(self):
        for field in ("viewports","variants","routes","journeys","checks","exceptions"):
            data=sample();data[field]={}
            self.assertTrue(checker.inspect_record(data,self.root)["structural_findings"])

    def test_unknown_view_is_input_error(self):
        with self.assertRaises(ValueError): self.check("launch")

    def test_cli_findings_exit_zero_without_pass(self):
        self.data["checks"][0]["route"]="unknown"
        (self.root / "record.json").write_text(json.dumps(self.data))
        run=subprocess.run([sys.executable,str(ROOT / "skills/ui-spec/scripts/check_manifest.py"),"--project-root",str(self.root),"--manifest","record.json","--mode","finish"],capture_output=True,text=True,timeout=10)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn("Structure inspection completed",run.stdout)
        self.assertNotIn("PASS",run.stdout)

    def test_cli_unreadable_returns_two(self):
        (self.root / "bad.json").write_text("{bad")
        run=subprocess.run([sys.executable,str(ROOT / "skills/ui-spec/scripts/check_manifest.py"),"--project-root",str(self.root),"--manifest","bad.json","--json"],capture_output=True,text=True,timeout=10)
        self.assertEqual(run.returncode,2)
        self.assertEqual(json.loads(run.stdout)["record_readability"],"unreadable")

    def test_no_mutation(self):
        before=copy.deepcopy(self.data)
        for view in ("overview","checks","connections"): self.check(view)
        self.assertEqual(self.data,before)


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
