"""Permanent v1.22.0 sustainable long-term loop release, continuity and inspector tests."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None

from source_continuity import (
    predecessor_runtime,
    runtime_v116,
    runtime_v1161,
    runtime_v117,
    runtime_v118,
    runtime_v119,
    runtime_v120,
    runtime_v121,
)
from test_tools import ROOT, package

FORBIDDEN_VERDICT_KEYS = {"ok", "pass", "satisfied", "ready", "complete", "stale", "veto"}
TWELVE_BYTE_LOCKED_FILES = {
    "skills/ui-spec/scripts/prepare.py",
    "skills/ui-spec/scripts/structural_records.py",
    "skills/ui-spec/scripts/check_manifest.py",
    "skills/ui-spec/scripts/check_design_evidence.py",
    "skills/ui-spec/scripts/check_file_integrity.py",
    "skills/ui-spec/scripts/find_resources.py",
    "skills/ui-spec/assets/design-coverage-categories.json",
    "skills/ui-spec/assets/resource-catalog.json",
    "skills/ui-spec/assets/templates/manifest.json",
    "skills/ui-spec/assets/templates/design-evidence.json",
    "skills/ui-spec/references/delegation.md",
    "skills/ui-spec/references/resource-catalog.md",
}


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def norm_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def heading_section(source: str, heading: str, *, level: int | None = None) -> str:
    match = re.search(r"(?m)^(#{2,3}) " + re.escape(heading) + r"\s*$", source)
    if not match:
        raise AssertionError(f"Missing section heading: {heading!r}")
    found_level = len(match.group(1))
    if level is not None and found_level != level:
        raise AssertionError(f"Heading {heading!r} has level H{found_level}, expected H{level}")
    tail = source[match.end():]
    nxt = re.search(r"(?m)^#{1," + str(found_level) + r"} ", tail)
    return tail[:nxt.start()] if nxt else tail


def collect_forbidden_keys(node: object, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(node, dict):
        for key, value in node.items():
            key_str = str(key)
            if key_str.lower() in FORBIDDEN_VERDICT_KEYS:
                hits.append(f"{path}.{key_str}")
            hits.extend(collect_forbidden_keys(value, f"{path}.{key_str}"))
    elif isinstance(node, list):
        for index, item in enumerate(node):
            hits.extend(collect_forbidden_keys(item, f"{path}[{index}]"))
    return hits


class SustainableLoopContinuityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(
            (ROOT / "docs/evidence/v1.22.0/continuity.json").read_text(encoding="utf-8")
        )

    def test_exact_38_file_inventory_and_dispositions(self):
        current = {
            p.relative_to(ROOT).as_posix()
            for p in package.source_files(ROOT)
            if p.is_relative_to(ROOT / "skills/ui-spec")
        }
        declared = [row["path"] for row in self.ledger["files"]]
        self.assertEqual(len(declared), 38)
        self.assertEqual(len(declared), len(set(declared)))
        self.assertEqual(current, set(declared))
        modified = [row for row in self.ledger["files"] if row["disposition"] != "unchanged"]
        unchanged = [row for row in self.ledger["files"] if row["disposition"] == "unchanged"]
        self.assertEqual(len(modified), 15)
        self.assertEqual(len(unchanged), 23)
        self.assertEqual(
            sum(1 for row in modified if row["disposition"] == "append-only"),
            9,
        )
        self.assertEqual(
            sum(1 for row in modified if row["disposition"] == "scoped-revision"),
            6,
        )

    def test_nine_hop_reverse_continuity_chain_reconstructs_cleanly(self):
        self.assertEqual(
            self.ledger["baseline_commit"],
            "12d6ec7814c5d4da87bdd947272f4dfe2f8f8821",
        )
        self.assertEqual(self.ledger["candidate_version"], "1.22.0")
        for row in self.ledger["files"]:
            rel = row["path"]
            with self.subTest(path=rel):
                live = (ROOT / rel).read_bytes()
                self.assertEqual(sha256_bytes(live), row["current_sha256"])
                self.assertEqual(len(live), row["current_bytes"])
                prior_v121 = runtime_v121(ROOT, rel)
                self.assertEqual(sha256_bytes(prior_v121), row["prior_sha256"])
                self.assertEqual(len(prior_v121), row["prior_bytes"])
                if rel == "skills/ui-spec/references/delegation.md":
                    # delegation.md was introduced in v1.21.0 and has no pre-v1.21 predecessor.
                    continue
                # Walk every predecessor hop down to v1.15.0 in memory (9-hop chain).
                for fn in (
                    runtime_v120,
                    runtime_v119,
                    runtime_v118,
                    runtime_v117,
                    runtime_v1161,
                    runtime_v116,
                    predecessor_runtime,
                ):
                    restored = fn(ROOT, rel)
                    self.assertIsInstance(restored, bytes)
                    self.assertGreater(len(restored), 0)

    def test_twelve_byte_locked_files_match_v121(self):
        by_path = {row["path"]: row for row in self.ledger["files"]}
        self.assertEqual(len(TWELVE_BYTE_LOCKED_FILES), 12)
        for rel in sorted(TWELVE_BYTE_LOCKED_FILES):
            row = by_path[rel]
            with self.subTest(path=rel):
                self.assertEqual((ROOT / rel).read_bytes(), runtime_v121(ROOT, rel))
                self.assertEqual(row["disposition"], "unchanged")
                self.assertEqual(row["inverse_edits"], [])

    def test_frozen_historical_evidence_digests_remain_identical(self):
        rows = self.ledger["historical_evidence_unchanged"]
        self.assertEqual(len(rows), 18)
        paths = [row["path"] for row in rows]
        self.assertEqual(len(rows), len(set(paths)))
        self.assertIn("docs/evidence/v1.21.0/continuity.json", paths)
        for row in rows:
            with self.subTest(path=row["path"]):
                self.assertEqual(sha256_bytes((ROOT / row["path"]).read_bytes()), row["sha256"])


class SustainableLoopRuntimeContractTests(unittest.TestCase):
    def test_skill_entry_and_no_version_changelog_narration(self):
        skill_bytes = (ROOT / "skills/ui-spec/SKILL.md").read_bytes()
        self.assertLess(len(skill_bytes), 25_000)
        skill_text = skill_bytes.decode("utf-8")
        parts = skill_text.split("---", 2)
        self.assertEqual(len(parts), 3)
        frontmatter, body = parts[1], parts[2]
        self.assertIn('version: "1.22.0"', frontmatter)
        body_norm = norm_ws(body)
        self.assertIn("read all eight common references in full", body)
        self.assertLess(
            body.index("Start from mature design work"),
            body.index("Choose the operation"),
        )
        for pattern in (
            r"continuation\s+baseline",
            r"overall\s+product\s+goal",
            r"current\s+design\s+model",
            r"current\s+product\s+ui",
            r"(superseded|consolidated|retired)",
            r"(brownfield|drift|hotfix)",
            r"(debt|open\s+obligation)",
        ):
            self.assertRegex(body_norm, pattern)

        # Runtime skill Markdown bodies stay in final-state language without version/internal-code narration.
        for path in sorted((ROOT / "skills/ui-spec").rglob("*.md")):
            raw = path.read_text(encoding="utf-8")
            check_body = raw.split("---", 2)[2] if path.name == "SKILL.md" else raw
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertNotRegex(check_body, r"\bv1\.2[12](?:\.\d+)?\b")
                self.assertNotRegex(check_body, r"\b1\.22\.0\b")
                self.assertNotRegex(check_body, r"\bFM[1-5]\b")
                self.assertNotRegex(check_body, r"\bINV-(?:0[1-9]|1[01])\b")
                self.assertNotIn("no-negative-echo", check_body.lower())

    def test_five_long_term_loop_reference_anchors_and_contracts(self):
        wf = (ROOT / "skills/ui-spec/references/workflow.md").read_text(encoding="utf-8")
        wf_sec = norm_ws(
            heading_section(wf, "Re-enter and hand off across sessions without losing direction", level=2)
        )
        for token in ("overall product goal", "current design model", "current product ui", "reopen"):
            self.assertIn(token, wf_sec)
        self.assertRegex(wf_sec, r"(settled|re-?litigat)")
        self.assertRegex(wf_sec, r"(interrupted|mid[\s-]?spec)")

        an = (ROOT / "skills/ui-spec/references/analysis.md").read_text(encoding="utf-8")
        outer_an = heading_section(an, "Choose a bounded increment", level=2)
        self.assertIn("### Govern the multi-SPEC horizon and retire obsolete scope", outer_an)
        an_sec = norm_ws(
            heading_section(an, "Govern the multi-SPEC horizon and retire obsolete scope", level=3)
        )
        for disp in ("candidate", "active", "completed", "superseded", "consolidated", "retired"):
            self.assertIn(disp, an_sec)
        self.assertRegex(an_sec, r"(orphan|dead[\s-]?end|obligation|transfer)")

        integ = (ROOT / "skills/ui-spec/references/integration.md").read_text(encoding="utf-8")
        in_sec = norm_ws(
            heading_section(integ, "Reconcile ongoing engineering and contract drift between rounds", level=2)
        )
        for pat in (
            r"compatible",
            r"(authoritative|contract|schema|api|permission)",
            r"(hotfix|ad[\s-]hoc|unreviewed)",
            r"(pivot|meaningful revision)",
        ):
            self.assertRegex(in_sec, pat)

        cs = (ROOT / "skills/ui-spec/references/component-sourcing.md").read_text(encoding="utf-8")
        cs_sec = norm_ws(
            heading_section(cs, "Migrate shared foundations across existing surfaces in stages", level=2)
        )
        for pat in (r"anchor", r"(coexist|bridge)", r"(w1|default-deny)", r"(decommission|retir|legacy)"):
            self.assertRegex(cs_sec, pat)

        pr = norm_ws((ROOT / "skills/ui-spec/references/principles.md").read_text(encoding="utf-8"))
        self.assertRegex(pr, r"(staged\s+migration|token\s+alias)")
        self.assertRegex(pr, r"(seam|coexist)")

        iv = norm_ws((ROOT / "skills/ui-spec/references/interaction-and-variants.md").read_text(encoding="utf-8"))
        self.assertRegex(iv, r"(coexist|migrat|bridge|legacy)")
        self.assertRegex(iv, r"(focus|keyboard|overlay|portal)")

        vf = (ROOT / "skills/ui-spec/references/verification.md").read_text(encoding="utf-8")
        vf_sec = norm_ws(
            heading_section(vf, "Scope regression across shared migrations and evolving code", level=3)
        )
        for pat in (r"primary", r"seam", r"extrem"):
            self.assertRegex(vf_sec, pat)

        em = (ROOT / "skills/ui-spec/references/evidence-map.md").read_text(encoding="utf-8")
        outer_em = heading_section(em, "Current model, meaningful revisions and evidence archive", level=2)
        self.assertIn("### Compact active records without evaporating open obligations", outer_em)
        em_sec = norm_ws(
            heading_section(em, "Compact active records without evaporating open obligations", level=3)
        )
        for pat in (
            r"visual.*debt|craft.*debt",
            r"(probe|bridge).*debt",
            r"(integration|contract).*debt",
            r"verification.*debt",
        ):
            self.assertRegex(em_sec, pat)

        ea = norm_ws((ROOT / "skills/ui-spec/references/evidence-actions.md").read_text(encoding="utf-8"))
        self.assertIn("reopen", ea)
        self.assertRegex(ea, r"(active\s+debt|open\s+obligation|provisional\s+bridge|brownfield\s+drift)")

        er = norm_ws((ROOT / "skills/ui-spec/references/evidence-records.md").read_text(encoding="utf-8"))
        self.assertIn("historical_objects", er)
        self.assertRegex(er, r"(superseded|consolidated|retired|horizon)")

    def test_four_updated_templates_carry_optional_long_term_fields(self):
        expectations = {
            "brief.md": r"(continuation\s+baseline|spec\s+horizon|re-ent(?:er|ry)|handover)",
            "design-decisions.md": r"(meaningful\s+revision|open\s+obligation|active\s+debt|reopen\s+trigger)",
            "design-system.md": r"(migration\s+wave|staged\s+migration|coexistence\s+bridge|legacy\s+decommission)",
            "review.md": r"(proportional\s+regression|seam|open\s+obligation|active\s+debt|handover)",
        }
        for name, pat in expectations.items():
            with self.subTest(template=name):
                text = norm_ws((ROOT / "skills/ui-spec/assets/templates" / name).read_text(encoding="utf-8"))
                self.assertRegex(text, pat)


class SustainableLoopCodexAndDocsSyncTests(unittest.TestCase):
    def test_codex_adapter_v122_manifest_hashes_and_schema(self):
        manifest = json.loads((ROOT / "integrations/codex/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.22.0")
        expected_roles = {
            "ui_researcher",
            "ui_integrator",
            "ui_challenger",
            "ui_experience_observer",
        }
        self.assertEqual(set(manifest["roles"]), expected_roles)
        for role_name in sorted(expected_roles):
            entry = manifest["roles"][role_name]
            role_path = ROOT / "integrations/codex" / entry["path"]
            raw = role_path.read_bytes()
            with self.subTest(role=role_name):
                self.assertRegex(entry["sha256"], r"^[0-9a-f]{64}$")
                self.assertEqual(sha256_bytes(raw), entry["sha256"])
                decoded = raw.decode("utf-8")
                if tomllib is not None:
                    parsed = tomllib.loads(decoded)
                    self.assertEqual(set(parsed.keys()), {"name", "description", "developer_instructions"})
                    self.assertEqual(parsed["name"], role_name)
                    instructions = parsed["developer_instructions"]
                else:
                    # Python 3.10 stdlib fallback: verify exact 3 top-level keys outside triple-quoted block.
                    stripped_block = re.sub(r'"""[\s\S]*?"""', '""', decoded)
                    top_keys = re.findall(r"(?m)^([A-Za-z0-9_-]+)\s*=", stripped_block)
                    self.assertEqual(set(top_keys), {"name", "description", "developer_instructions"})
                    self.assertEqual(len(top_keys), 3)
                    name_match = re.search(r'(?m)^name\s*=\s*"([^"]+)"\s*$', stripped_block)
                    self.assertIsNotNone(name_match)
                    self.assertEqual(name_match.group(1), role_name)
                    inst_match = re.search(
                        r'developer_instructions\s*=\s*"""([\s\S]*?)"""', decoded
                    )
                    self.assertIsNotNone(inst_match)
                    instructions = inst_match.group(1)
                lower = instructions.casefold()
                self.assertIn("main agent", lower)
                self.assertTrue(
                    "all eight common references" in lower or "full eight-reference foundation" in lower,
                    role_name,
                )
                self.assertIn("delegation.md", instructions)

    def test_maintainer_docs_and_release_surfaces_are_synchronized(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("shared byte/word budget", agents)
        self.assertIn("## Version 1.21: wide high-craft discovery, deep reuse and taste calibration", agents)
        self.assertIn("## Version 1.22: sustainable long-term product and engineering loop", agents)

        model = (ROOT / "docs/MODEL.md").read_text(encoding="utf-8")
        self.assertIn("UI Spec Studio 1.22", model)
        self.assertRegex(model, r"(?m)^##\s+28\.")

        writing = (ROOT / "docs/WRITING.md").read_text(encoding="utf-8")
        heading_section(writing, "Write for long-term continuation and brownfield evolution", level=2)

        guide = (ROOT / "docs/GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("REVIEW-v1.22.0.md", guide)
        self.assertIn("Continuation Baseline", guide)

        review = (ROOT / "docs/REVIEW-v1.22.0.md").read_text(encoding="utf-8")
        for token in ("CONTENT-INTEGRITY.md", "H01", "H11", "continuity.json", "38"):
            self.assertIn(token, review)

        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertRegex(changelog, r"(?m)^##\s+1\.22\.0\b")
        self.assertRegex(changelog, r"(?m)^##\s+1\.21\.0\b")

        release_note = (ROOT / "docs/releases/v1.22.0.md").read_text(encoding="utf-8")
        self.assertIn("Version 1.22.0", release_note)
        self.assertIn("REVIEW-v1.22.0.md", release_note)

        readme_en = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/REVIEW-v1.22.0.md", readme_en)
        self.assertIn("docs/releases/v1.22.0.md", readme_en)

        readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
        self.assertIn("docs/REVIEW-v1.22.0.md", readme_zh)
        self.assertIn("docs/releases/v1.22.0.md", readme_zh)

    def test_antigravity_installer_harness_registration_and_paths(self):
        registry = json.loads((ROOT / "installer/harnesses.json").read_text(encoding="utf-8"))
        self.assertIn("antigravity", registry["harnesses"])
        antigravity = registry["harnesses"]["antigravity"]
        self.assertEqual(antigravity["project_skill_dir"], ".agents/skills/ui-spec")
        self.assertEqual(antigravity["user_skill_dir"], ".gemini/config/skills/ui-spec")
        self.assertEqual(antigravity["user_base"], "home")

        experience = (ROOT / "installer/lib/experience.mjs").read_text(encoding="utf-8")
        self.assertIn("antigravity: 'Antigravity'", experience)

        cli = (ROOT / "installer/bin/ui-spec.mjs").read_text(encoding="utf-8")
        self.assertIn("Antigravity", cli)

        pkg = json.loads((ROOT / "installer/package.json").read_text(encoding="utf-8"))
        self.assertIn("Antigravity", pkg["description"])
        self.assertIn("antigravity", pkg["keywords"])


class SustainableLoopNeutralInspectorFixtureTests(unittest.TestCase):
    def test_multi_round_compacted_brownfield_record_with_untouched_inspector(self):
        inspector = ROOT / "skills/ui-spec/scripts/check_design_evidence.py"
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td)
            for rel, body in (
                ("src/tokens/semantic-bridge.css", "[data-legacy] { --bg: var(--surface-canvas); }\n"),
                ("src/routes/OrdersPage.tsx", "export function OrdersPage() { return null; }\n"),
                ("src/routes/BillingLegacyPage.tsx", "export function BillingLegacyPage() { return null; }\n"),
                (".ui-spec/evidence/orders-anchor.png", "png-placeholder"),
                (".ui-spec/evidence/seam-billing.png", "png-placeholder"),
                (".ui-spec/archive/round-02-retired-export.md", "# Archived round 2 comparison\n"),
            ):
                fp = proj / rel
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(body, encoding="utf-8")

            record = {
                "format": "ui-spec-evidence/1",
                "record_origin": "project_working_record",
                "revision": "r12",
                "product_context": {
                    "overall_goal": "Operational orders and billing workspace with staged warm-neutral token migration.",
                    "current_ui": "Orders migrated on wave 1; Billing legacy route bridges semantic tokens cleanly.",
                },
                "candidate_specs": [
                    {
                        "id": "SPEC-14",
                        "status": "candidate",
                        "purpose": "Migrate Billing route onto wave-2 mature table and remove legacy CSS bridge.",
                        "boundary_reason": "Independent billing workflow sequenced after Orders anchor validation.",
                        "relationship": "depends_on SPEC-12 bridge and decommissions legacy billing styles",
                        "quality_goals": ["Preserve settled typography and header origin across billing views"],
                        "objects": ["obj-billing-seam"],
                        "related_specs": ["SPEC-12"],
                        "revision": "r12",
                    }
                ],
                "formal_specs": [
                    {
                        "id": "SPEC-11",
                        "status": "completed",
                        "purpose": "Establish shared warm-neutral navigation shell and token foundation.",
                        "boundary_reason": "Shared shell foundation inherited without relitigation.",
                        "relationship": "completed foundation consumed by SPEC-12",
                        "quality_goals": ["Stable shell geometry across migrated and legacy routes"],
                        "objects": ["obj-shell"],
                        "decisions": ["dec-orders-migration"],
                        "related_specs": ["SPEC-12"],
                        "revision": "r11",
                    },
                    {
                        "id": "SPEC-12",
                        "status": "active",
                        "purpose": "Wave-1 Orders anchor migration with scoped coexistence bridge and hotfix craft repair.",
                        "boundary_reason": "Minimum sufficient experience closure for anchor slice and seam parity.",
                        "relationship": "active primary migration wave consolidating SPEC-10 and retiring SPEC-04",
                        "quality_goals": [
                            "Preserve landed bulk-refund permission hotfix while restoring mature table craft",
                            "Keep focus, overlay stacking and theme parity across Orders-to-Billing seam",
                        ],
                        "objects": ["obj-orders-anchor", "obj-token-bridge"],
                        "research_objects": ["obj-orders-anchor"],
                        "implementation_objects": ["obj-orders-anchor", "obj-token-bridge"],
                        "regression_objects": ["obj-shell", "obj-billing-seam"],
                        "decisions": ["dec-orders-migration"],
                        "related_specs": ["SPEC-11", "SPEC-14"],
                        "revision": "r12",
                    },
                ],
                "objects": [
                    {
                        "id": "obj-shell",
                        "level": "L2",
                        "title": "Shared app shell and navigation landmarks",
                        "parent": None,
                        "categories": ["layout", "navigation"],
                        "revision": "r11",
                    },
                    {
                        "id": "obj-token-bridge",
                        "level": "L4",
                        "title": "Scoped semantic token alias bridge (temporary wave-1 compatibility layer)",
                        "parent": "obj-shell",
                        "categories": ["tokens", "migration-bridge"],
                        "revision": "r12",
                    },
                    {
                        "id": "obj-orders-anchor",
                        "level": "L3",
                        "title": "Orders anchor slice with cursor pagination and bulk-refund permission state",
                        "parent": "obj-shell",
                        "categories": ["table", "brownfield-hotfix"],
                        "revision": "r12",
                    },
                    {
                        "id": "obj-billing-seam",
                        "level": "L3",
                        "title": "Billing legacy route meeting wave-1 navigation and token bridge seam",
                        "parent": "obj-shell",
                        "categories": ["seam", "legacy-consumer"],
                        "revision": "r12",
                    },
                ],
                "conditions": [
                    {
                        "id": "cond-desktop-light",
                        "description": "Desktop 1440px light theme with populated live cursor-paginated rows",
                        "revision": "r12",
                    },
                    {
                        "id": "cond-narrow-dark",
                        "description": "Narrow 390px dark theme with long localized labels",
                        "revision": "r12",
                    },
                ],
                "relations": [
                    {"type": "depends_on", "from": "obj-orders-anchor", "to": "obj-token-bridge"},
                    {"type": "affects", "from": "obj-token-bridge", "to": "obj-billing-seam"},
                    {"type": "shares", "from": "obj-orders-anchor", "to": "obj-shell"},
                ],
                "evidence": [
                    {
                        "id": "ev-orders-anchor",
                        "kind": "rendered_screenshot",
                        "role": "integrated",
                        "status": "inspected",
                        "observation": "Orders anchor renders mature table craft while preserving landed bulk-refund permission guard.",
                        "window": "settled_render",
                        "method": "local_browser_capture",
                        "objects": ["obj-orders-anchor", "obj-token-bridge"],
                        "conditions": ["cond-desktop-light"],
                        "location": {"path": ".ui-spec/evidence/orders-anchor.png"},
                        "revision": "r12",
                    },
                    {
                        "id": "ev-seam-billing",
                        "kind": "rendered_screenshot",
                        "role": "integrated",
                        "status": "inspected",
                        "observation": "Transition between Orders and legacy Billing keeps header origin and focus ring consistent.",
                        "window": "route_transition",
                        "method": "local_browser_capture",
                        "objects": ["obj-billing-seam", "obj-shell"],
                        "conditions": ["cond-desktop-light"],
                        "location": {"path": ".ui-spec/evidence/seam-billing.png"},
                        "revision": "r12",
                    },
                ],
                "coverage_challenges": [
                    {
                        "discovery": "Inter-round backend commit added cursor pagination and bulk-refund guard hotfix.",
                        "disposition": "reconciled_in_active_spec",
                        "reason": "Preserved functional/accessibility fix and repaired table spacing on top.",
                        "objects": ["obj-orders-anchor"],
                        "evidence": ["ev-orders-anchor"],
                        "next_action": "Finish real API error recovery wiring in SPEC-12 finish.",
                    }
                ],
                "required_checks": [],
                "decisions": [
                    {
                        "id": "dec-orders-migration",
                        "objects": ["obj-orders-anchor", "obj-token-bridge", "obj-billing-seam"],
                        "evidence": ["ev-orders-anchor", "ev-seam-billing"],
                        "purpose": "Adopt wave-1 mature table and semantic token bridge without breaking legacy Billing seam.",
                        "question": "Can wave-1 Orders adopt new semantic tokens while Billing remains stable until wave 2?",
                        "judgment": "Anchor slice and desktop seam hold; four explicit debt obligations stay open until resolved.",
                        "choice": "Keep scoped CSS alias bridge under W1-W3 integration rules and decommission in SPEC-14.",
                        "revision": "r12",
                        "next_action": {
                            "kind": "continue_finish",
                            "reason": "Wire live bulk-refund API error recovery and inspect narrow dark extremum.",
                            "objects": ["obj-orders-anchor", "obj-billing-seam"],
                        },
                        "comparison": {
                            "state": "compared",
                            "alternatives": ["big-bang 20-route rewrite", "staged anchor slice with scoped alias bridge"],
                            "evidence": ["ev-orders-anchor"],
                            "rationale": "Staged anchor slice limits blast radius while proving mature craft first.",
                            "revision": "r12",
                        },
                        "implementation": {
                            "state": "implemented",
                            "evidence": ["ev-orders-anchor"],
                            "paths": [
                                "src/tokens/semantic-bridge.css",
                                "src/routes/OrdersPage.tsx",
                                "src/routes/BillingLegacyPage.tsx",
                            ],
                            "revision": "r12",
                        },
                        "approval": {
                            "status": "approved_in_scope",
                            "source": "owner_review_round_11",
                            "scope": "wave-1 Orders anchor and temporary semantic bridge",
                            "revision": "r12",
                        },
                        "checks": [
                            {
                                "domain": "visual",
                                "status": "observed",
                                "finding": "Desktop light Orders anchor and Billing seam align cleanly.",
                                "role": "integrated",
                                "objects": ["obj-orders-anchor", "obj-billing-seam"],
                                "conditions": ["cond-desktop-light"],
                                "evidence": ["ev-orders-anchor", "ev-seam-billing"],
                                "revision": "r12",
                            }
                        ],
                        "gaps": [
                            {
                                "id": "debt-visual-01",
                                "status": "open",
                                "impact": "medium",
                                "question": "Visual & Craft Debt: long localized currency badge crowds narrow Orders row.",
                                "objects": ["obj-orders-anchor"],
                                "resolution_evidence": [],
                                "next_action": "Tighten badge wrapping token before closing SPEC-12.",
                            },
                            {
                                "id": "debt-bridge-02",
                                "status": "open",
                                "impact": "medium",
                                "question": "Provisional Probe & Migration Bridge Debt: semantic-bridge.css awaits SPEC-14 legacy decommission.",
                                "objects": ["obj-token-bridge"],
                                "resolution_evidence": [],
                                "next_action": "Delete bridge after SPEC-14 migrates Billing.",
                            },
                            {
                                "id": "debt-integration-03",
                                "status": "open",
                                "impact": "high",
                                "question": "Integration & Contract Debt: bulk-refund partial-failure retry still uses local fixture.",
                                "objects": ["obj-orders-anchor"],
                                "resolution_evidence": [],
                                "next_action": "Connect authoritative refund endpoint during finish.",
                            },
                            {
                                "id": "debt-verification-04",
                                "status": "open",
                                "impact": "medium",
                                "question": "Verification Scope Debt: narrow dark extremum (cond-narrow-dark) not yet inspected on Billing seam.",
                                "objects": ["obj-billing-seam"],
                                "resolution_evidence": [],
                                "next_action": "Capture and inspect 390px dark seam before wave-2 kickoff.",
                            },
                        ],
                    }
                ],
                "revisions": [
                    {
                        "id": "rev-r12-compaction",
                        "summary": "Compacted closed rounds 1-10 candidate comparisons and retired SPEC-04 export screen.",
                        "reason": "Keep Current Design Model proportional to O(active product + open obligations).",
                        "historical_objects": ["obj-legacy-csv-export-r02", "obj-old-filter-bar-r07"],
                        "archive_ref": ".ui-spec/archive/round-02-retired-export.md",
                    }
                ],
                "archive": [
                    {
                        "id": "arch-r02",
                        "path": ".ui-spec/archive/round-02-retired-export.md",
                        "summary": "Cold archived round-2 candidate comparisons (loaded on demand only).",
                    }
                ],
            }

            record_path = proj / ".ui-spec/design-evidence.json"
            record_path.parent.mkdir(parents=True, exist_ok=True)
            record_path.write_text(json.dumps(record, indent=2), encoding="utf-8")

            for view in ("overview", "detail", "execution"):
                res = subprocess.run(
                    [
                        sys.executable,
                        "-B",
                        str(inspector),
                        "--project-root",
                        str(proj),
                        "--record",
                        ".ui-spec/design-evidence.json",
                        "--view",
                        view,
                        "--changed",
                        "obj-token-bridge",
                    ],
                    cwd=proj,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    check=False,
                )
                with self.subTest(view=view):
                    self.assertEqual(res.returncode, 0, res.stderr + res.stdout)
                    payload = json.loads(res.stdout)
                    self.assertEqual(payload["record_readability"], "readable")
                    self.assertEqual(payload["structural_findings"], [])
                    self.assertEqual(collect_forbidden_keys(payload), [])
                    candidates = payload["view"]["declared_relation_review_candidates"]
                    self.assertEqual(
                        candidates["object_ids"],
                        ["obj-billing-seam", "obj-orders-anchor", "obj-shell", "obj-token-bridge"],
                    )
                    self.assertEqual(candidates["decision_ids"], ["dec-orders-migration"])
                    self.assertEqual(len(payload["view"]["meaningful_revisions"]), 1)
                    self.assertEqual(len(payload["view"]["evidence_archive_references"]), 1)


if __name__ == "__main__":
    unittest.main()
