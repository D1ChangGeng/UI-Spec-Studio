"""Structural guardrails for historically recovered methods, not model-quality tests."""
from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/evidence/v1.13.0/lineage.json"


def heading_section(source: str, heading: str) -> str:
    match = re.search(r"(?m)^(#{2,3}) " + re.escape(heading) + r"\s*$", source)
    if not match:
        raise AssertionError(f"Missing current section: {heading}")
    level = len(match.group(1))
    tail = source[match.end():]
    next_section = re.search(r"(?m)^#{1," + str(level) + r"} ", tail)
    return tail[:next_section.start()] if next_section else tail


class ContentIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(LEDGER.read_text(encoding="utf-8"))

    def test_historical_data_has_source_identity(self):
        rows = self.data["historical_measurements"]
        self.assertGreaterEqual(len(rows), 12)
        self.assertEqual(rows[0][0], "v1.1.0")
        self.assertEqual(rows[-1][0], "v1.12.1")
        self.assertEqual(len({r[0] for r in rows}), len(rows))
        self.assertEqual(len(self.data["budget_history"]), 3)

    def test_restored_specificity_is_in_installed_sections(self):
        ids = set()
        for item in self.data["restored"]:
            self.assertNotIn(item["id"], ids)
            ids.add(item["id"])
            self.assertTrue(item["source_tag"].startswith("v1."))
            self.assertIn(item["source_tag"], item["source_url"])
            self.assertEqual(item["disposition"], "restored_with_current_methods")
            self.assertTrue(item["current_path"].startswith("skills/ui-spec/references/"))
            source = (ROOT / item["current_path"]).read_text(encoding="utf-8")
            section = heading_section(source, item["current_heading"])
            self.assertGreaterEqual(len(item["required_details"]), 3)
            for detail in item["required_details"]:
                self.assertIn(detail, section, item["id"])
        self.assertGreaterEqual(len(ids), 11)

    def test_byte_ceiling_is_not_a_release_gate(self):
        pub = (ROOT / "tests/test_publication.py").read_text(encoding="utf-8")
        validator = (ROOT / "tools/validate_package.py").read_text(encoding="utf-8")
        self.assertNotIn("self.assertLess(total,144*1024", pub)
        self.assertNotIn("Keep the entry below 500 lines", validator)
        maintainer = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("shared byte/word budget", maintainer)


if __name__ == "__main__":
    unittest.main()
