"""Guard the accuracy and separation of v1.14.0 post-release evidence."""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "docs/evidence/v1.14.0/empirical-findings.json"

class V114EmpiricalEvidence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_fixed_release_identity_and_method_arm(self):
        r = self.e["release"]
        self.assertEqual(r["tag"], "v1.14.0")
        self.assertEqual(r["commit"], "fec7cde99be02c134481733e9f9bd3064ffa871a")
        self.assertEqual(r["production_method"], "structure-and-action")
        self.assertEqual(r["experimental_arm_correspondence"], "structure-action")
        self.assertIs(r["byte_identical_to_ablation"], False)
        self.assertIs(r["original_tag_immutable"], True)
        self.assertIs(r["assets_unchanged_expected"], True)

    def test_real_runs_and_locked_agent_judgments_unchanged(self):
        s = self.e["study"]
        self.assertEqual((s["task_count"], s["arm_count"], s["real_agent_runs"], s["locked_task_judgments"]), (6,3,18,12))
        self.assertEqual(sum(len(task["blind"]) for task in self.e["tasks"].values()), 12)
        self.assertEqual(len(self.e["locked_review_hashes"]), 3)
        self.assertTrue(all(len(x["sha256"]) == 64 for x in self.e["locked_review_hashes"]))
        self.assertEqual([x["strength"] for x in self.e["tasks"]["T02"]["blind"]], ["moderate","moderate"])
        self.assertEqual([x["tiers"][0] for x in self.e["tasks"]["T01"]["blind"]],
                         [["baseline","structure"],["baseline","structure"]])
        self.assertTrue(self.e["tasks"]["T06"]["pixel_identical_across_3_arms_for_8_conditions"])

    def test_owner_and_blind_sources_are_separate(self):
        owner = self.e["owner_assessment"]
        self.assertIs(owner["positive_acceptance_for_version"], True)
        self.assertIs(owner["blind"], False)
        self.assertEqual(owner["preferred_arm"], "structure-action")
        self.assertIs(owner["per_task_scores_supplied"], False)
        self.assertIs(owner["do_not_modify_original_anonymous_review"], True)
        self.assertIn("视觉观感更好", owner["verbatim"])
        self.assertTrue(self.e["boundary"]["owner_and_blind_evaluations_are_distinct"])

    def test_docs_state_post_release_not_unrun(self):
        release = (ROOT / "docs/releases/v1.14.0.md").read_text(encoding="utf-8")
        review = (ROOT / "docs/REVIEW-v1.14.0.md").read_text(encoding="utf-8")
        report = (ROOT / "docs/experiments/design-evidence/RESULTS-v1.14.0.md").read_text(encoding="utf-8")
        for doc in (release, review, report):
            self.assertIn("post-release" if doc is release else "Post-release" if doc is review else "发布后", doc)
        self.assertIn("匿名", report)
        self.assertIn("产品所有者", report)
        protocol = (ROOT / "docs/experiments/design-evidence/PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("**Prepared, not executed.**", protocol)

if __name__ == "__main__":
    unittest.main()
