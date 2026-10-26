"""Authored declaration/path fixtures; these are not Agent behavior or visual-quality tests."""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/ui-spec/scripts/check_design_evidence.py"
spec = importlib.util.spec_from_file_location("design_evidence_checker", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def sample() -> dict:
    return {
        "format": checker.FORMAT, "revision": "fixture-r1",
        "objects": [{"id": "goal", "level": "L0", "title": "Synthetic task"},
                    {"id": "panel", "level": "L2", "title": "Synthetic panel", "parent": "goal"},
                    {"id": "font", "level": "L4", "title": "Synthetic typography"},
                    {"id": "independent", "level": "L3", "title": "Unrelated supported change"}],
        "conditions": [{"id": "wide", "description": "Fixture wide/light/English/open state"},
                       {"id": "narrow", "description": "Fixture narrow/dark/Chinese/open state"}],
        "relations": [{"from": "font", "to": "panel", "type": "affects"}],
        "evidence": [{"id": "E1", "kind": "visual", "role": "integrated", "status": "observed",
                      "location": {"path": "evidence.txt"}, "objects": ["panel"], "conditions": ["wide"],
                      "product_revision": "fixture-r1", "observation": "Authored test declaration; no real visual inspection claimed"}],
        "decisions": [{"id": "D1", "objects": ["panel"], "purpose": "Synthetic readable panel",
                       "question": "Can the fixture record support this scoped declaration?",
                       "judgment": "Authored declaration for testing only", "choice": "Synthetic candidate",
                       "evidence": ["E1"], "checks": [{"domain": "visual", "status": "pass", "objects": ["panel"],
                          "conditions": ["wide"], "revision": "fixture-r1", "evidence": ["E1"],
                          "finding": "Synthetic fixture declaration, not a product-quality result"}],
                       "gaps": [], "next_action": {"kind": "verify", "reason": "Inspect remaining real conditions separately"}}],
        "coverage_challenges": [], "required_checks": []}


class DesignEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "evidence.txt").write_text("Synthetic local-file marker; no pixel validation", encoding="utf-8")
        (self.root / "component.py").write_text("# synthetic implementation fixture\n", encoding="utf-8")
        self.data = sample()
        self.decision = self.data["decisions"][0]
        self.evidence = self.data["evidence"][0]
        self.check = self.decision["checks"][0]

    def tearDown(self):
        self.temp.cleanup()

    def result(self):
        return checker.validate(self.data, self.root)

    def assert_bad(self, phrase):
        result = self.result()
        self.assertFalse(result["ok"], result)
        self.assertIn(phrase, "\n".join(result["errors"]))

    def gap(self):
        self.decision["gaps"] = [{"id": "G1", "impact": "high", "status": "open", "question": "Unseen panel transition",
                                   "next_action": "Inspect the actual open-close episode with long content"}]

    def test_scoped_declaration_is_structurally_valid(self):
        result = self.result()
        self.assertTrue(result["ok"], result)
        self.assertIn("not truth", result["limits"][0])

    def test_empty_planning_template_stays_valid_draft(self):
        template = json.loads((ROOT / "skills/ui-spec/assets/templates/design-evidence.json").read_text())
        result = checker.validate(template, self.root)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["counts"]["evidence"], 0)

    def test_root_must_be_object(self):
        self.assertFalse(checker.validate([], self.root)["ok"])

    def test_duplicate_objects(self):
        self.data["objects"].append(copy.deepcopy(self.data["objects"][0]))
        self.assert_bad("Duplicate id")

    def test_unknown_level(self):
        self.data["objects"][0]["level"] = "L6"
        self.assert_bad("L0–L5")

    def test_unknown_parent(self):
        self.data["objects"][1]["parent"] = "missing"
        self.assert_bad("Unknown parent")

    def test_containment_cycle(self):
        self.data["objects"][0]["parent"] = "panel"
        self.assert_bad("Containment cycle")

    def test_dependency_cycle_is_not_containment_cycle(self):
        self.data["relations"].append({"from": "panel", "to": "font", "type": "affects"})
        self.assertTrue(self.result()["ok"])
        self.assertEqual(checker.project_view(self.data, "overview", ["font"])["review_candidates_after_change"], ["font", "goal", "panel"])

    def test_unknown_evidence_reference(self):
        self.decision["evidence"] = ["missing"]
        self.assert_bad("Unknown reference")

    def test_missing_local_artifact(self):
        self.evidence["location"] = {"path": "missing.png"}
        self.assert_bad("E1")

    def test_parent_escape_rejected(self):
        self.evidence["location"] = {"path": "../evidence.txt"}
        self.assert_bad("inside the project")

    def test_absolute_and_windows_paths_rejected(self):
        for path in ("/etc/passwd", "C:/private.txt", "folder\\file.txt"):
            with self.subTest(path=path):
                self.evidence["location"] = {"path": path}
                self.assertFalse(self.result()["ok"])

    def test_symlink_rejected_even_if_internal(self):
        try:
            (self.root / "alias.txt").symlink_to(self.root / "evidence.txt")
        except (OSError, NotImplementedError):
            self.skipTest("Host cannot create test symlinks")
        self.evidence["location"] = {"path": "alias.txt"}
        self.assert_bad("symlinks")

    def test_digest_match_and_mismatch(self):
        self.evidence["sha256"] = hashlib.sha256((self.root / "evidence.txt").read_bytes()).hexdigest()
        self.assertTrue(self.result()["ok"])
        self.evidence["sha256"] = "0" * 64
        self.assert_bad("digest differs")

    def test_remote_url_not_fetched_or_certified(self):
        self.evidence["location"] = {"url": "https://example.invalid/reference"}
        result = self.result()
        self.assertTrue(result["ok"])
        self.assertTrue(any("remote availability" in x for x in result["warnings"]))

    def test_credentials_and_file_urls_rejected(self):
        for url in ("https://person:secret@example.invalid", "file:///etc/passwd", "javascript:alert(1)"):
            with self.subTest(url=url):
                self.evidence["location"] = {"url": url}
                self.assert_bad("Invalid remote")

    def test_acquisition_does_not_support_visual_pass(self):
        self.evidence["status"] = "acquired"
        self.assert_bad("Pass lacks observed")

    def test_observation_needs_actual_portion(self):
        del self.evidence["observation"]
        self.assert_bad("inspected portion")

    def test_documentation_cannot_stand_in_for_visual_observation(self):
        self.evidence["kind"] = "text"
        self.assert_bad("matching-domain")

    def test_demo_cannot_stand_in_for_integrated_result(self):
        self.evidence["role"] = "demo"
        self.assert_bad("matching-domain")

    def test_missing_condition_is_not_covered_by_another_view(self):
        self.check["conditions"].append("narrow")
        self.assert_bad("condition")

    def test_condition_object_pairs_do_not_use_cartesian_union(self):
        self.decision["objects"].append("independent")
        self.check["objects"].append("independent")
        self.check["conditions"].append("narrow")
        other = copy.deepcopy(self.evidence)
        other.update(id="E2", objects=["independent"], conditions=["narrow"])
        self.data["evidence"].append(other)
        self.check["evidence"].append("E2")
        self.assert_bad("Pass lacks observed")

    def test_parent_not_passed_from_child(self):
        self.decision["objects"].append("goal")
        self.check["objects"] = ["goal"]
        self.assert_bad("Pass lacks observed")

    def test_check_cannot_expand_decision_scope(self):
        self.check["objects"] = ["goal"]
        self.assert_bad("broadens")

    def test_stale_product_revision_rejected(self):
        self.data["revision"] = "fixture-r2"
        self.assert_bad("stale")

    def test_stale_capture_not_fixed_by_relabeling_check(self):
        self.check["revision"] = self.data["revision"] = "fixture-r2"
        self.assert_bad("revision evidence")

    def test_temporal_claim_needs_window_and_method(self):
        self.check["domain"] = self.evidence["kind"] = "temporal"
        self.assert_bad("window")
        self.evidence.update(window="Synthetic pre-trigger through reversal and settled result", method="Authored ordered-frame declaration with gaps")
        self.assertTrue(self.result()["ok"])

    def test_pending_check_is_not_pass(self):
        self.check.update(status="planned", evidence=[])
        self.assertTrue(self.result()["ok"])

    def test_required_state_record_exposes_pending_coverage(self):
        self.data["required_checks"] = [{"object": "panel", "condition": "narrow", "domain": "visual"}]
        result = self.result()
        self.assertTrue(result["ok"])
        self.assertEqual(len(result["pending_coverage"]), 1)
        self.decision["next_action"]["kind"] = "finish"
        self.assert_bad("required condition")

    def test_adopted_dependency_needs_real_location(self):
        self.decision["implementation"] = {"state": "adopted", "paths": [], "evidence": ["E1"]}
        self.assert_bad("actual local paths")

    def test_existing_location_does_not_certify_adoption(self):
        self.decision["implementation"] = {"state": "adopted", "paths": ["component.py"], "evidence": ["E1"]}
        self.assertTrue(self.result()["ok"])
        self.assertTrue(any("actual use" in x for x in self.result()["limits"]))

    def test_high_gap_requires_concrete_next_action(self):
        self.gap(); del self.decision["gaps"][0]["next_action"]
        self.assert_bad("evidence-producing action")

    def test_blocked_gap_still_limits_dependent_expansion(self):
        self.gap(); self.decision["gaps"][0]["status"] = "blocked"
        self.decision["next_action"]["kind"] = "expand"
        self.assert_bad("unresolved high-impact gap")

    def test_independent_supported_work_continues(self):
        self.gap()
        self.decision["next_action"].update(kind="expand", objects=["independent"], independent_reason="No shared dependency with the missing panel observation")
        self.assertTrue(self.result()["ok"])

    def test_independent_claim_needs_reason(self):
        self.gap(); self.decision["next_action"].update(kind="expand", objects=["independent"])
        self.assert_bad("dependency explanation")

    def test_bounded_trial_can_resolve_gap(self):
        self.gap(); self.decision["next_action"].update(kind="trial", reason="Run a bounded episode to inspect the hypothesis")
        self.assertTrue(self.result()["ok"])

    def test_resolved_gap_needs_evidence(self):
        self.gap(); self.decision["gaps"][0]["status"] = "resolved"
        self.assert_bad("Reference list is empty")

    def test_waiver_is_not_a_pass(self):
        self.check.update(status="waived", evidence=[])
        self.assert_bad("exception record")
        self.check["exception"] = {"by": "synthetic owner", "source": "fixture authorization", "reason": "Fixture-only exclusion", "scope": "wide visual check"}
        result = self.result(); self.assertTrue(result["ok"])
        self.assertTrue(any("authenticity" in x for x in result["warnings"]))
        self.assertEqual(self.check["status"], "waived")

    def test_approval_is_separate_and_needs_source(self):
        self.decision["approval"] = {"status": "approved"}
        self.assert_bad("Approval needs")

    def test_comparison_requires_distinct_named_alternatives(self):
        self.decision["comparison"] = {"state": "compared", "alternatives": ["A", "A"], "evidence": ["E1"], "rationale": "Synthetic comparison"}
        self.assert_bad("distinct named alternatives")

    def test_comparison_acquisition_is_not_observation(self):
        self.decision["checks"] = []
        self.data["evidence"][0]["status"] = "acquired"
        self.decision["comparison"] = {"state": "compared", "alternatives": ["A", "B"],
                                       "evidence": ["E1"], "rationale": "Synthetic"}
        self.assert_bad("observed support")

    def test_trial_needs_trial_not_reference_or_installed_path(self):
        self.decision["implementation"] = {"state": "trialed", "paths": ["component.py"], "evidence": ["E1"]}
        self.assert_bad("current-project trial")

    def test_declared_dependency_propagates_high_gap(self):
        self.gap(); self.decision["gaps"][0]["objects"] = ["font"]
        self.decision["next_action"]["kind"] = "expand"
        self.assert_bad("unresolved high-impact gap")

    def test_trial_pass_does_not_close_integrated_requirement(self):
        self.data["evidence"][0]["role"] = "trial"
        self.check["role"] = "trial"
        self.data["required_checks"] = [{"object":"panel", "condition":"wide", "domain":"visual"}]
        self.decision["next_action"]["kind"] = "finish"
        self.assert_bad("required condition")

    def test_parent_finish_cannot_hide_child_required_check(self):
        self.data["required_checks"] = [{"object":"panel", "condition":"narrow", "domain":"visual"}]
        self.decision["next_action"].update(kind="finish", objects=["goal"])
        self.assert_bad("required condition")

    def test_malformed_nested_fields_return_diagnostics(self):
        for table, key in (("objects","level"), ("evidence","kind"), ("decisions","checks")):
            for value in ({}, ["unexpected"], 7):
                data = copy.deepcopy(self.data); data[table][0][key] = value
                with self.subTest(table=table,key=key,value=value):
                    self.assertFalse(checker.validate(data,self.root)["ok"])

    def test_open_discovery_needs_an_evidence_route(self):
        self.data["coverage_challenges"] = [{"discovery": "Fixture reference shows a recovery state", "reason": "Might affect task scope", "disposition": "open"}]
        self.assert_bad("next action")

    def test_exclusion_retains_reason(self):
        self.data["coverage_challenges"] = [{"discovery": "Reference team administration", "reason": "Explicitly personal product", "disposition": "exclude"}]
        self.assertTrue(self.result()["ok"])

    def test_three_views_share_ids_and_do_not_mutate(self):
        original = copy.deepcopy(self.data)
        for view in ("overview", "detail", "execution"):
            result = checker.project_view(self.data, view, ["font"])
            self.assertEqual(result["decisions"][0]["id"], "D1")
            self.assertEqual(result["affected_decisions"], ["D1"])
        self.assertEqual(self.data, original)

    def test_unknown_changed_object_rejected(self):
        with self.assertRaises(ValueError):
            checker.project_view(self.data, "overview", ["missing"])

    def test_cli_is_read_only_and_reports_limits(self):
        (self.root / "record.json").write_text(json.dumps(self.data))
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        run = subprocess.run([sys.executable, str(SCRIPT), "--project-root", str(self.root), "--record", "record.json", "--view", "execution"], capture_output=True, text=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(json.loads(run.stdout)["limits"])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})

    def test_cli_malformed_input_no_traceback(self):
        (self.root / "bad.json").write_text("{invalid")
        run = subprocess.run([sys.executable, str(SCRIPT), "--project-root", str(self.root), "--record", "bad.json"], capture_output=True, text=True, timeout=10)
        self.assertEqual(run.returncode, 2)
        self.assertNotIn("Traceback", run.stderr)


if __name__ == "__main__":
    unittest.main()
