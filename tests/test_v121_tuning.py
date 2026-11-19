"""Deterministic regression checks for v1.21.0 wide discovery, deep reuse, taste calibration, consolidation and continuity."""
from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None

from source_continuity import runtime_v120
from test_tools import ROOT, load, package, validator

finder = load("find_resources_v121", ROOT / "skills/ui-spec/scripts/find_resources.py")
catalog_docs = load("catalog_docs_v121", ROOT / "tools/catalog_docs.py")


def _slugify(heading: str) -> str:
    text = heading.strip().lower()
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[^\w\s-]", "", text)
    return text.replace(" ", "-")


class V121ContinuityTests(unittest.TestCase):
    def test_v121_continuity_round_trip_to_v120(self):
        ledger_path = ROOT / "docs/evidence/v1.21.0/continuity.json"
        self.assertTrue(ledger_path.is_file())
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        self.assertEqual(ledger["candidate_version"], "1.21.0")
        self.assertEqual(ledger["prior_runtime_version"], "1.20.0")
        self.assertEqual(len(ledger["files"]), 37)
        added = [row["path"] for row in ledger["added_files"]]
        self.assertEqual(added, ["skills/ui-spec/references/delegation.md"])
        for row in ledger["added_files"]:
            actual = (ROOT / row["path"]).read_bytes()
            self.assertEqual(hashlib.sha256(actual).hexdigest(), row["current_sha256"])
            self.assertEqual(len(actual), row["current_bytes"])

        for row in ledger["files"]:
            restored = runtime_v120(ROOT, row["path"])
            self.assertEqual(hashlib.sha256(restored).hexdigest(), row["prior_sha256"], row["path"])
            self.assertEqual(len(restored), row["prior_bytes"], row["path"])

    def test_v121_continuity_rejects_tampered_and_unknown_paths(self):
        with self.assertRaises(ValueError):
            runtime_v120(ROOT, "skills/ui-spec/references/delegation.md")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "docs/evidence/v1.21.0").mkdir(parents=True)
            (root / "skills/ui-spec").mkdir(parents=True)
            shutil.copyfile(
                ROOT / "docs/evidence/v1.21.0/continuity.json",
                root / "docs/evidence/v1.21.0/continuity.json",
            )
            tampered = (ROOT / "skills/ui-spec/SKILL.md").read_bytes() + b"\n# tamper\n"
            (root / "skills/ui-spec/SKILL.md").write_bytes(tampered)
            with self.assertRaisesRegex(ValueError, "Current source differs"):
                runtime_v120(root, "skills/ui-spec/SKILL.md")

    def test_historical_continuity_ledgers_remain_unchanged(self):
        ledger = json.loads((ROOT / "docs/evidence/v1.21.0/continuity.json").read_text(encoding="utf-8"))
        by_path = {row["path"]: row["sha256"] for row in ledger["historical_evidence_unchanged"]}
        self.assertGreaterEqual(len(by_path), 7000)
        for prior in (
            "docs/evidence/v1.15.0/continuity.json",
            "docs/evidence/v1.16.1/continuity.json",
            "docs/evidence/v1.17.0/continuity.json",
            "docs/evidence/v1.18.0/continuity.json",
            "docs/evidence/v1.19.0/continuity.json",
            "docs/evidence/v1.20.0/continuity.json",
        ):
            self.assertIn(prior, by_path)
            actual = hashlib.sha256((ROOT / prior).read_bytes()).hexdigest()
            self.assertEqual(actual, by_path[prior], prior)


class V121CatalogAndLookupTests(unittest.TestCase):
    def test_catalog_has_80_neutral_live_verified_entries(self):
        data = finder.load_catalog()
        resources = data["resources"]
        self.assertEqual(len(resources), 80)
        self.assertEqual(data["snapshot_date"], "2026-10-24")
        self.assertEqual(data["catalog_updated_on"], "2026-11-18")
        self.assertEqual(sum(1 for r in resources if r["reviewed_on"] == "2026-10-24"), 37)
        self.assertEqual(sum(1 for r in resources if r["reviewed_on"] == "2026-11-18"), 43)

        ids = [r["id"] for r in resources]
        self.assertEqual(len(ids), len(set(ids)))

        forbidden = {"score", "rank", "rating", "recommended", "priority", "tier", "weight"}
        for r in resources:
            self.assertIn("craft_profile", r, f"Missing craft_profile on {r['id']}")
            self.assertFalse(forbidden.intersection(r.keys()), r["id"])
            profile = r["craft_profile"]
            self.assertFalse(forbidden.intersection(profile.keys()), r["id"])
            for field in ("roles", "reuse_scopes", "visual_forms"):
                self.assertTrue(profile.get(field), f"{r['id']}.craft_profile.{field} empty")

        expected_md = catalog_docs.render(data)
        actual_md = (ROOT / "skills/ui-spec/references/resource-catalog.md").read_text(encoding="utf-8")
        self.assertEqual(actual_md, expected_md)

    def test_catalog_docs_handles_missing_profile_reviewed_on(self):
        data = copy.deepcopy(finder.load_catalog())
        data["resources"][0]["craft_profile"].pop("reviewed_on", None)
        rendered = catalog_docs.render(data)
        self.assertIn(data["resources"][0]["name"], rendered)

    def test_find_resources_code_stack_includes_neutral_and_multi(self):
        data = finder.load_catalog()
        for stack in ("react", "vue", "svelte", "solid", "web-components"):
            matches = finder.match_resources(data, stack=stack)
            matched_stacks = {s for item in matches for s in item["stacks"]}
            self.assertTrue(
                {"framework-neutral", "multi-framework", "multi-runtime"}.intersection(matched_stacks),
                f"Expected neutral/multi-framework leads for --stack {stack}",
            )
        # Reference and design-tool stay exact (do not pull multi-framework code libs)
        ref_matches = finder.match_resources(data, stack="reference")
        self.assertTrue(ref_matches)
        self.assertTrue(all("reference" in item["stacks"] for item in ref_matches))

    def test_find_resources_word_boundary_and_safe_plural(self):
        data = finder.load_catalog()
        # Singular query matches pluralized tags/descriptions
        chart_ids = {r["id"] for r in finder.match_resources(data, "chart")}
        charts_ids = {r["id"] for r in finder.match_resources(data, "charts")}
        self.assertTrue(chart_ids)
        self.assertTrue(charts_ids.issubset(chart_ids))

        # Word-boundary guard: 'table' must not match 'editable'; 'ai' must not match 'tailark' or 'detail'
        table_matches = finder.match_resources(data, "table")
        self.assertTrue(table_matches)
        for item in table_matches:
            blob = " ".join([
                item["id"], item["name"], item["use_for"], item["access"], item["adoption_notes"],
                *item["needs"], *item["forms"], *item["stacks"], *item["aliases"],
                *item.get("craft_profile", {}).get("roles", []),
                *item.get("craft_profile", {}).get("reuse_scopes", []),
                *item.get("craft_profile", {}).get("visual_forms", []),
            ]).casefold()
            self.assertRegex(blob, r"(?<![a-z0-9])tables?(?![a-z0-9])", item["id"])

        ai_matches = finder.match_resources(data, "ai")
        ai_ids = {r["id"] for r in ai_matches}
        self.assertNotIn("tailark", ai_ids)

    def test_find_resources_cli_json_reports_totals_truncation_and_neutrality(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "skills/ui-spec/scripts/find_resources.py"), "--stack", "react", "--limit", "5", "--json"],
            capture_output=True, text=True, check=True,
        )
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["count"], 5)
        self.assertGreater(payload["total_matches"], 5)
        self.assertTrue(payload["truncated"])
        self.assertEqual(payload["catalog_updated_on"], "2026-11-18")
        self.assertEqual(payload["ordering"], "alphabetical; no design-quality ranking")
        self.assertFalse({"ok", "pass", "recommended", "score"}.intersection(payload.keys()))
        names = [(r["name"].casefold(), r["id"]) for r in payload["results"]]
        self.assertEqual(names, sorted(names))


class V121SkillConsolidationAndGuidanceTests(unittest.TestCase):
    def test_portable_skill_has_38_files_and_delegation_in_zip(self):
        portable = [
            p for p in (ROOT / "skills/ui-spec").rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
        ]
        self.assertEqual(len(portable), 38)
        with tempfile.TemporaryDirectory() as td:
            outputs = package.build(ROOT, Path(td), include_evidence=False)
            with zipfile.ZipFile(outputs[1]) as archive:
                names = set(archive.namelist())
                self.assertEqual(len(names), 38)
                self.assertIn("ui-spec/references/delegation.md", names)
                self.assertFalse(any("__pycache__" in n or n.endswith(".pyc") for n in names))

    def test_all_local_links_and_anchors_in_skill_resolve(self):
        skill_root = ROOT / "skills/ui-spec"
        link_re = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
        heading_re = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)

        slug_cache: dict[Path, set[str]] = {}
        for md in skill_root.rglob("*.md"):
            slugs = {_slugify(m.group(1)) for m in heading_re.finditer(md.read_text(encoding="utf-8"))}
            slug_cache[md.resolve()] = slugs

        for md in sorted(skill_root.rglob("*.md")):
            text = md.read_text(encoding="utf-8")
            # Strip fenced code blocks before checking markdown links
            stripped = re.sub(r"```.*?```", "", text, flags=re.S)
            for match in link_re.finditer(stripped):
                target = match.group(1).strip()
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                if target.startswith("#"):
                    anchor = target[1:]
                    self.assertIn(anchor, slug_cache[md.resolve()], f"Broken internal anchor {target} in {md}")
                    continue
                path_part, _, anchor = target.partition("#")
                resolved = (md.parent / path_part).resolve()
                self.assertTrue(resolved.exists(), f"Broken link {target} in {md}")
                if anchor and resolved in slug_cache:
                    self.assertIn(anchor, slug_cache[resolved], f"Broken anchor {target} in {md}")

    def test_core_v121_method_contracts_and_restored_guardrails(self):
        entry = (ROOT / "skills/ui-spec/SKILL.md").read_text(encoding="utf-8")
        self.assertLess(len(entry.encode("utf-8")), 25_000)
        self.assertIn("references/delegation.md", entry)
        self.assertIn("knowledge maintenance, not model training or autonomous modification of its host", entry)

        sourcing = (ROOT / "skills/ui-spec/references/component-sourcing.md").read_text(encoding="utf-8")
        self.assertIn("## Multi-tier high-craft discovery and generic-default rejection", sourcing)
        self.assertIn("### Generic-default rejection floor", sourcing)
        self.assertIn("### Five permitted deep-reuse operations", sourcing)
        self.assertIn("### Permitted deep adaptation vs. prohibited original construction", sourcing)
        self.assertIn("inspected upstream source code", sourcing)
        self.assertIn("W1", sourcing)
        self.assertIn("W3", sourcing)

        principles = (ROOT / "skills/ui-spec/references/principles.md").read_text(encoding="utf-8")
        self.assertIn("## Diagnostic generic-UI and AI-slop failure signatures", principles)
        self.assertIn("## Six operational craft calibrations", principles)
        self.assertIn("## Source-preserving de-genericization and visual harmonization", principles)

        workflow = (ROOT / "skills/ui-spec/references/workflow.md").read_text(encoding="utf-8")
        self.assertIn("Small differences outside the agreed quality responsibility do not require unbounded refinement.", workflow)

        verification = (ROOT / "skills/ui-spec/references/verification.md").read_text(encoding="utf-8")
        self.assertIn("## Empirical regression guardrails", verification)
        self.assertIn("## Target-demo vs. integrated-app visual delta and craft retention", verification)
        self.assertIn("## Taste and craft-defect audit", verification)
        self.assertIn("A video of a UI does not establish its operability", verification)
        # Ensure maintainer comparative-benchmark text stays out of runtime instructions
        for leaked in ("three-arm", "blind cohort", "preregistration"):
            self.assertNotIn(leaked, verification.casefold())

        delegation = (ROOT / "skills/ui-spec/references/delegation.md").read_text(encoding="utf-8")
        self.assertIn("as final visual surfaces", delegation)
        self.assertIn("inspected upstream source code", delegation)


class V121CodexAdapterTests(unittest.TestCase):
    def test_codex_manifest_hashes_and_unconditional_eight_reference_contract(self):
        codex_dir = ROOT / "integrations/codex"
        manifest = json.loads((codex_dir / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.21.0")
        self.assertEqual(
            set(manifest["roles"].keys()),
            {"ui_researcher", "ui_integrator", "ui_challenger", "ui_experience_observer"},
        )
        for role_name, meta in manifest["roles"].items():
            role_path = codex_dir / meta["path"]
            raw = role_path.read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), meta["sha256"], role_name)
            decoded = raw.decode("utf-8")
            instructions = tomllib.loads(decoded)["developer_instructions"] if tomllib is not None else decoded
            lower = instructions.casefold()
            self.assertTrue(
                "all eight common references" in lower or "full eight-reference foundation" in lower,
                role_name,
            )
            self.assertIn("delegation.md", instructions, role_name)


if __name__ == "__main__":
    unittest.main()
