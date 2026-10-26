"""Static exploration-method contracts; these are not model-behavior evidence."""
from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/ui-spec"


class DeepExplorationContractTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    def test_entry_names_a_decision_loop_not_a_search_quota(self):
        entry = self.read("skills/ui-spec/SKILL.md")
        for phrase in (
            "Evidence-Driven Deep Visual Exploration",
            "design impact",
            "specific uncertainty",
            "potential upside",
            "question → discovery → actual viewing/operation",
            "no fixed site, candidate, step or time quota",
            "materially different",
        ):
            self.assertIn(phrase.lower(), entry.lower())
        self.assertLess(entry.index("Calibrate design decisions"), entry.index("Start from mature design work"))

    def test_all_five_evidence_dimensions_have_a_runtime_home(self):
        source = self.read("skills/ui-spec/references/component-sourcing.md").lower()
        verification = self.read("skills/ui-spec/references/verification.md").lower()
        for dimension in (
            "coverage breadth", "inspection depth", "temporal coverage",
            "relevance", "reliability",
        ):
            self.assertIn(dimension, source)
            self.assertIn(dimension, verification)

    def test_comparison_access_and_actual_adoption_are_distinct(self):
        sourcing = self.read("skills/ui-spec/references/component-sourcing.md")
        self.assertIn("Challenge the early favorite", sourcing)
        self.assertIn("authorized alternative demonstrations", sourcing)
        self.assertIn("implementation/production route", sourcing)
        entry = self.read("skills/ui-spec/SKILL.md")
        self.assertIn("studied, compared, trialed and actually adopted", entry)
        self.assertIn("Never infer unseen qualities", entry)

    def test_decision_records_can_explain_an_alternative_and_gap(self):
        for path in (
            "skills/ui-spec/assets/templates/design-decisions.md",
            "skills/ui-spec/assets/templates/resource-adoption.md",
            "skills/ui-spec/assets/templates/review.md",
        ):
            text = self.read(path).lower()
            self.assertIn("alternative", text)
            self.assertIn("gap", text)
            self.assertIn("actual", text)

    def test_guidance_is_accessible_without_a_ninth_common_reference(self):
        entry = self.read("skills/ui-spec/SKILL.md")
        self.assertIn("read all eight common references in full", entry)
        for path in ("README.md", "README.zh-CN.md", "docs/GUIDE.md",
                     "docs/ART-DIRECTION.md", "docs/PRODUCT-ALIGNMENT.md"):
            self.assertIn("DEEP-VISUAL-EXPLORATION.md", self.read(path))
        guide = self.read("docs/DEEP-VISUAL-EXPLORATION.md")
        self.assertIn("覆盖广度", guide)
        self.assertIn("何时继续探索", guide)

    def test_methods_and_actual_effects_have_separate_evidence(self):
        assurance = self.read("docs/EVALUATION.md")
        self.assertIn("Method/package mechanics", assurance)
        self.assertIn("Agent behavior in a fresh task", assurance)
        self.assertIn("Design result and user experience", assurance)
        self.assertIn("Structural tests", self.read("skills/ui-spec/references/verification.md"))


if __name__ == "__main__":
    unittest.main()
