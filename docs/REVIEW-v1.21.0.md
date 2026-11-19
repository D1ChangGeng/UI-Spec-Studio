# v1.21.0 review — Wide High-Craft Discovery, Deep Reuse & Taste Calibration

**Baseline:** `v1.20.6` (`cf899f14826456ceed697176cefa73e36b93fb7d`; runtime source lineage recovered to `v1.20.0`, `eb91a3839ae964e20ae9b2888fecf8100b493d04`, via [the v1.21.0 continuity ledger](evidence/v1.21.0/continuity.json)).

## Summary of systemic tuning

Version `1.21.0` tunes the entire `ui-spec` Skill and its optional four-role Codex adapter across four connected dimensions while preserving the eight-common-reference full-reading contract, default-deny original UI construction (closed `W1`–`W3` allowlist), neutral read-only helpers, and exact historical continuity:

1. **Wide high-grade UI resource discovery**
   - Expanded [`skills/ui-spec/assets/resource-catalog.json`](../skills/ui-spec/assets/resource-catalog.json) from **37** to **80** live-verified entries (+43 entries reviewed on `2026-11-18`; all 37 original `2026-10-24` entries preserved verbatim; `80/80` carry neutral descriptive `craft_profile` blocks; `0` duplicate IDs/URLs; `0` ranking or quality-score keys).
   - Regenerated [`skills/ui-spec/references/resource-catalog.md`](../skills/ui-spec/references/resource-catalog.md) with deduplicated craft-profile disclaimers via hardened [`tools/catalog_docs.py`](../tools/catalog_docs.py).
   - Fixed [`skills/ui-spec/scripts/find_resources.py`](../skills/ui-spec/scripts/find_resources.py) so concrete code-stack filters (`react`, `vue`, `svelte`, `solid`, `web-components`, `vanilla-web`, etc.) include `framework-neutral`, `multi-framework` and `multi-runtime` resources; added word-boundary ASCII token matching with safe singular/plural handling (for ASCII alpha words of length >= 4), full-text matching across `adoption_notes` and `craft_profile`, and `total_matches`/`truncated` fields while keeping alphabetical, read-only, neutral behavior.
   - Added a **4-tier discovery architecture** (Tier 1 curated design-craft registries/galleries -> Tier 2 production design systems & accessible primitives -> Tier 3 specialist motion/shader/chart/3D/editor craft ecosystems -> Tier 4 open GitHub/web exploration & reference deconstruction) and the **Generic-Default Rejection Floor** in [`skills/ui-spec/references/component-sourcing.md`](../skills/ui-spec/references/component-sourcing.md), plus expanded specialist leads in [`asset-sources.md`](../skills/ui-spec/references/asset-sources.md) and [`sources.md`](../skills/ui-spec/references/sources.md).

2. **Deep reuse and craft-elevating improvement**
   - Explicitly codified **five permitted deep-reuse operations** in `component-sourcing.md` with clear boundary criteria against prohibited original UI construction (`W1`–`W3` closed allowlist):
     1. *Source-Preserving De-Templating*
     2. *Canonical Token-Plane & Multi-Source Cascade Harmonization*
     3. *Adopted-Component Rendering-Fidelity & Ergonomic Repair*
     4. *Source-Derived Architectural Porting & Weight-Stripping* (strictly gated on inspected upstream source code, derivative-permitting license with preserved attribution/notices, and checking that no leaner native-stack equivalent fits)
     5. *Craft-Elevating State & Accessibility Completion*
   - Added four concrete deep-reuse recipes to [`patterns.md`](../skills/ui-spec/references/patterns.md) and linked real-product adoption/harmonization records through [`examples.md`](../skills/ui-spec/references/examples.md), [`integration.md`](../skills/ui-spec/references/integration.md), and [`evidence-records.md`](../skills/ui-spec/references/evidence-records.md).

3. **UI design taste and aesthetic discrimination**
   - Added **6 diagnostic AI-slop failure signatures** (with zero dogmatic aesthetic bans), **6 operational craft calibrations** (typographic optical tuning, proportion/rhythm, surface depth & hairline contrast, color restraint & semantic polarity, visual density & focal hierarchy, asset/icon stroke alignment), and **source-preserving de-genericization** in [`principles.md`](../skills/ui-spec/references/principles.md).
   - Added dedicated optical dark/light re-authoring, tactile motion personality and micro-interaction craft in [`interaction-and-variants.md`](../skills/ui-spec/references/interaction-and-variants.md), editorial copy craft in [`content-design.md`](../skills/ui-spec/references/content-design.md), and asset-to-interface cohesion in [`visual-assets.md`](../skills/ui-spec/references/visual-assets.md).
   - Added an inspectable aesthetic direction & 6-layer reference craft breakdown in [`analysis.md`](../skills/ui-spec/references/analysis.md), the **Taste-Critique -> Upgrade -> Re-Inspect** loop and dual-track `audit` in [`workflow.md`](../skills/ui-spec/references/workflow.md), and **Target-Demo vs. Integrated-App Visual Delta**, empirical regression guardrails, and Taste & Craft-Defect Audit in [`verification.md`](../skills/ui-spec/references/verification.md).

4. **Whole-Skill structural consolidation & Codex role alignment**
   - Extracted nine scattered v1.20 delegation sections into one dedicated conditional reference, [`skills/ui-spec/references/delegation.md`](../skills/ui-spec/references/delegation.md) (`17,387` bytes), increasing the portable Skill inventory from **37** to **38** files while reducing [`SKILL.md`](../skills/ui-spec/SKILL.md) by **53.1%** (`45,550 -> 21,374` bytes) and reducing the eight common references' combined footprint slightly (`276,039 -> 272,534` bytes, `-3,505` bytes) despite major substantive additions.
   - Removed maintainer comparative-benchmark text leaked into runtime verification instructions, unified repeated historical strata, and aligned all H2 tables of contents and local anchors.
   - Upgraded all four Codex roles (`ui_researcher.toml`, `ui_integrator.toml`, `ui_challenger.toml`, `ui_experience_observer.toml`), `AGENTS-snippet.md`, `README.md`, and `manifest.json` (`1.21.0`) with matching SHA-256 digests and unconditional eight-common-reference reading.

## Portable Skill size and inventory metrics

| Scope | v1.20.6 (`HEAD`) | v1.21.0 | Delta |
| --- | ---: | ---: | ---: |
| Portable Skill files (`skills/ui-spec/`) | 37 | 38 | +1 (`references/delegation.md`) |
| `SKILL.md` entry spine | 45,550 B | 21,374 B | -24,176 B (-53.1%) |
| 8 common references combined | 276,039 B | 272,534 B | -3,505 B (-1.3%) |
| Conditional `references/delegation.md` | — | 17,387 B | +17,387 B |
| `assets/resource-catalog.json` | 48,532 B (37 entries) | 138,947 B (80 entries) | +90,415 B (+43 entries) |
| `references/resource-catalog.md` | 38,529 B | 87,576 B | +49,047 B |
| Total portable Skill bytes | 644,657 B | 792,148 B | +147,491 B |

## Content-integrity audit & disposition (per `docs/CONTENT-INTEGRITY.md`)

An independent read-only content-integrity review audited every modified runtime file against `v1.20.6`, the 11 tracked `v1.13.0` lineage items, and the 8 newline-sensitive `v1.15.0` transfer obligations.

| Area / Material change | Classification | Disposition and verification |
| --- | --- | --- |
| Nine scattered v1.20 subagent/delegation tails across `SKILL.md`, `workflow.md`, `analysis.md`, `component-sourcing.md`, `verification.md`, `evidence-map.md`, `evidence-actions.md`, `integration.md` | **Moved to an installed source** | Consolidated cleanly into [`skills/ui-spec/references/delegation.md`](../skills/ui-spec/references/delegation.md) with explicit dispatch trigger in `SKILL.md`. |
| Redundant geological version-strata prose and duplicate framing across `SKILL.md`, `workflow.md`, `analysis.md`, `component-sourcing.md`, `verification.md` | **Equivalent** | Folded into unified causal final-state guidance; all 11/11 `v1.13` lineage items and 8/8 `v1.15` transfer strings preserved. |
| Maintainer comparative-campaign language previously inside runtime `verification.md` | **Reasonably superseded** | Kept strictly in maintainer docs (`docs/EVALUATION.md`, `AGENTS.md`); runtime instructions remain consumer-facing. |
| Codex role instructions temporarily narrowing reading scope in `ui_researcher.toml`, `ui_challenger.toml`, `ui_experience_observer.toml` | **Capability loss — restored** | Reviewer Finding #1: restored unconditional reading of all eight common references across all Codex roles and refreshed `integrations/codex/manifest.json` SHA-256 hashes before freezing continuity. |
| Operation 4 porting wording in `component-sourcing.md` and `delegation.md` potentially ambiguous under default-deny | **Capability loss — tightened** | Reviewer Finding #2: strictly required inspected upstream source code, derivative-permitting license with preserved attribution/notices, verification that no leaner native-stack equivalent fits, and explicit main-agent assignment for delegated porting; clarified `"as final visual surfaces"` boundary. |
| Omitted operational guardrails during prose consolidation: non-self-modification/model-training boundary (`SKILL.md`), bounded refinement stop rule (`workflow.md`), video-operability & diagram/asset medium matching (`verification.md`) | **Capability loss — restored** | Reviewer Finding #3: restored all three exact behavioral boundaries before generating `docs/evidence/v1.21.0/continuity.json`. |
| H2 TOC label mismatch in `principles.md` L5 | **Editorial defect — fixed** | Reviewer Finding #4: synced TOC label to exact H2 heading; automated anchor verification confirms 0 broken links/anchors. |
| `catalog_docs.py` L69 missing fallback when `craft_profile.reviewed_on` is absent; `find_resources.py` singular query (`chart`/`card`/`table`) missing plural tags | **Tooling defect — fixed** | Reviewer Finding #5: hardened `profile.get("reviewed_on", x["reviewed_on"])` and added safe ASCII plural matching `(?:e?s)?` restricted to alpha words >= 4 chars (preventing `ai`/`ui`/`3d` over-matching and rejecting substring false positives such as `editable` / `tailark`). |

## Verification scope and evidence boundaries

- **Deterministic engineering checks (executed in this workspace):** package validation (`tools/validate_package.py`), catalog map parity (`tools/catalog_docs.py --check`), README SVG determinism (`tools/readme_art.py --check`), complete unit test suite (`python3 -m unittest discover -s tests -v`), deterministic distribution build (`tools/package.py`), and local installer smoke check (`tools/installer_smoke.py`). These verify file integrity, schema/lookup mechanics, continuity reconstruction to `v1.20.0` (and chained prior versions), Codex adapter packaging, and link/anchor consistency.
- **Bounded single-agent forward-application smoke check (separately reported):** a read-only consuming-agent probe reading the live `v1.21.0` Skill and executing `find_resources.py` on a concrete product brief checks workflow coherence, 4-tier discovery, deep-reuse/W1–W3 discipline, and operational taste calibration. It is a single bounded text/tool observation—never a runnable product build, comparative model campaign, or quality benchmark.
- **Not executed in this environment (explicitly unverified here):**
  - Chromium browser fixtures (`tools/validate_scenario.py`, `tools/validate_assets.py`, `tools/validate_content.py`, `tools/validate_temporal.py`, README GitHub-host render captures) — Playwright/Chromium are not installed in this remote container and must run in CI before tagging/publishing.
  - Controlled multi-model comparative campaigns (`v1.20.x` vs. `v1.21.0`), native Codex CLI/Cloud runtime telemetry, live npm Trusted Publisher OIDC publication, and independent human owner visual acceptance.
- **Historical evidence preservation:** all files under `docs/evidence/v1.8.0..v1.20.0/` and `docs/experiments/` remain byte-for-byte unchanged and hashed in `docs/evidence/v1.21.0/continuity.json`.
