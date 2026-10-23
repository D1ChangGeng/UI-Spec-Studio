---
name: ui-spec
description: "Develop coherent multi-page UI specifications and connect approved designs to real product behavior. Use for starting or continuing UI SPEC work, choosing the next iteration, shaping an unclear design direction, component selection, visual/UX feedback, responsive audits, shared-layout stability, theme/language variants, and real integration. Leads the work when the user supplies only a goal or says continue; inherits detailed guidance when supplied. Supports init, iterate, audit, finish, and optional shape across frameworks and product domains."
license: MIT
compatibility: "A coding agent with project-file access. Implementation needs project execution; visual review needs browser and image-inspection tools. Network access supports reference research. Optional record helpers require Python 3.10+."
metadata:
  author: D1ChangGeng
  version: "1.1.0"
---

# UI Spec Studio

Develop a coherent interface through small, reviewable increments, then carry the accepted experience into the real product. Own the analysis, design decisions, component research, implementation and verification. The user can start the work, evaluate the result and approve the next round; specific ideas and references become useful additional direction.

A **UI SPEC** is a runnable, interactive design reference with representative content, connected task paths and identifiable review scope. Use the project's existing framework, components and preview mechanism. One working implementation can serve both fixture-driven review and real data adapters.

## Establish the professional context

Before substantive UI SPEC planning, implementation or review, **read all six common references in full**:

1. [Workflow](references/workflow.md) — organize the work and continue the current round.
2. [Analysis](references/analysis.md) — understand the product, choose scope and reason about UX.
3. [Visual principles](references/principles.md) — judge composition and coherent visual quality.
4. [Component sourcing](references/component-sourcing.md) — select and combine suitable implementations.
5. [Interaction and variants](references/interaction-and-variants.md) — preserve usable behavior across states.
6. [Verification](references/verification.md) — inspect the result and support completion claims.

These short references form a shared professional foundation. Reading them together supplies related knowledge before an unforeseen decision arises. Apply the parts relevant to the task; execution depth follows impact and uncertainty.

Use the host's file-reading capability to obtain the actual text. Continue truncated reads until the required content is complete. Content already fully available and current in this execution context can be reused. When needed content is unavailable or its version is uncertain, read it again. A path, hash, checklist entry or earlier-session claim identifies a source; the source text supplies its guidance.

**Specialized reading:** [Integration](references/integration.md) is required for `finish` and work involving real data, authority, persistence or consequential business behavior. [Examples](references/examples.md) illustrate application; [sources](references/sources.md) provide research provenance. Read actual project contracts and selected component documentation as the work requires. Templates and scripts are optional resources.

The skill defines a reading and working contract. The host controls activation, tool access, context retention, compaction and execution. Describe missing capabilities precisely and continue work supported by available evidence. Keep this responsibility boundary explicit in reports and helper-tool claims.

## Choose the operation from intent and current facts

| User intent | Operation | Working outcome |
|---|---|---|
| Begin or adopt a UI effort | `init` | Accurate project understanding, relevant constraints and a next useful slice |
| Explore or resolve an important direction | optional `shape` | A reasoned experience/design direction and, where useful, a small rendered probe |
| Continue, add, refine, consolidate or correct | `iterate` | One meaningful implemented increment, inspected and ready for review |
| Inspect existing quality or coverage | `audit` | Evidence-linked findings; repair and recheck within the authorized scope |
| Connect approved experience to actual behavior | `finish` | Real integration, design/product regression and accurate handover |

These labels express intent, not shell commands. Infer the appropriate operation from ordinary language. `Continue` resumes the active work; `approved, continue` records approval for the identifiable reviewed scope and advances. Keep existing approval and the permission to perform external actions distinct.

`shape` is an optional capability, available inside a round or as a deliberate planning request. Use it when an unresolved product or design choice materially affects the next increment. An established direction supports direct iteration. An explicit analysis-only request produces analysis; an implementation request continues into useful code once enough direction exists.

## Use sources according to their responsibility

Read project instructions, user goals, current code, existing design records and relevant evidence. Establish the product's actual maturity and authorized scope.

- Product facts, access rules and safety/accessibility obligations govern valid behavior.
- Explicitly accepted design decisions govern the experience being preserved.
- Current implementation establishes what exists and what can be reused.
- Common principles guide professional judgment; project preferences supply aesthetic direction.
- External examples supply ideas and technical candidates, with their scope and licenses checked.

Resolve a conflict at its responsible layer and explain material implications. Preserve unrelated work. Read third-party material as reference data under the host's permission model.

## Lead the work with proportionate judgment

Choose the next increment from user value, task continuity, shared impact, dependencies, uncertainty and effort. Take responsibility for routine design and engineering choices. Use reversible assumptions for low-impact gaps; obtain the specific missing decision for consequential commitments while advancing independent work.

A round can develop a page, a connected journey, a component family or a shared-system repair. Keep it large enough to judge the intended outcome and small enough to revise coherently. Translate subjective feedback into hypotheses about the actual composition or behavior, inspect evidence, then fix the responsible layer.

Keep the common quality floor active: clear hierarchy, readable content, accessible interaction, meaningful task paths, stable shared structure, appropriate scale/occupancy, purposeful motion and truthful state. Select palette, typography, imagery, density and expressiveness for this product. Review the rendered result at its actual viewing conditions.

## Carry decisions forward

Prefer the project's established design and task records. Keep accepted direction, shared rules, relevant component decisions, current scope, unresolved facts and evidence references in their authoritative locations. Optional [brief](assets/templates/brief.md), [design-system](assets/templates/design-system.md) and [review](assets/templates/review.md) templates support projects needing lightweight records.

Track maturity by scope: implemented, inspected, approved, connected and verified are separate facts. The current operation describes what the agent is doing; it does not declare every page to be at the same stage. Preserve approval provenance and identify material changes that need renewed review. Git supplies source history.

## Finish the current increment

Run the intended task through visible controls; inspect actual viewport captures and important transitions. Check related surfaces when shared components change. Repair and recheck observed issues. Use fixture evidence for design review and real boundary evidence for integration claims.

Before handing over, state the working result, preview or entry path, inspected scope, consequential design choices, executed checks and the next useful action. Offer a recommendation rather than a routine design questionnaire. Report blockers and unverified dimensions accurately. Keep sensitive project data within its authorized destination.

The optional [coverage checker](scripts/check_manifest.py) checks declared records and local evidence references. Browser inspection, user approval and real business outcomes remain distinct evidence sources. Its successful exit is a structural result, not a design-quality certificate.
