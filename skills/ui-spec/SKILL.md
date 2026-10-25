---
name: ui-spec
description: "Design coherent screen-based experiences: product UI, documentation, READMEs, diagrams and interactive specifications; connect approved designs to real behavior. Use for starting or continuing UI SPEC work, shaping an unclear direction, product interaction models, design options, traceable resource selection, visual assets, content design, UX writing, typography, multilingual copy, brand/icon/type craft, 2D/3D/media delivery, responsive audits, scroll and motion continuity, performance experience, operational content and batch workflows, complete states, theme/language variants, and real integration. Leads the work when the user supplies only a goal or says continue; inherits detailed guidance when supplied. Supports init, iterate, audit, finish, and optional shape across frameworks and product domains."
license: MIT
compatibility: "A coding agent with project-file access. Implementation needs project execution; visual review needs browser and image-inspection tools. Network access supports reference research. Optional record helpers require Python 3.10+."
metadata:
  author: D1ChangGeng
  version: "1.6.0"
---

# UI Spec Studio

Build from accurate content and suitable mature design work, refine it through small, reviewable increments, then carry the accepted experience into the real product. Own the analysis, design decisions, component research, implementation and verification. The user can start the work, evaluate the result and approve the next round; specific ideas and references become useful additional direction.

A **UI SPEC** is a runnable or renderable design reference with representative content, a meaningful reader/user path and identifiable review scope. Product interfaces, documentation, READMEs, diagrams, presentations and other screen-based artifacts share this practice. Choose the actual medium's capabilities and conventions: a document can deliver a complete reading task without an application shell. Use the project's existing framework, format and preview mechanism. One working implementation can serve both fixture-driven review and real data adapters.

## Start from mature design work

Use design theory and resource knowledge together. Theory explains quality, fit and tradeoffs; resource knowledge exposes concrete work that can carry those qualities. Apply both while searching, browsing, comparing, adapting and verifying. Resource discovery can improve the initial idea before the direction is settled.

For a new surface or substantial redesign, seek the **highest appropriate reuse level**: a coherent product/page template or design system, a substantial layout or functional block, then the components, primitives and effects needed to complete it. Choose the largest useful set of design relationships that fits the task, not the largest code package. An established accepted page may need only a component-level change.

Inherit valuable decisions about hierarchy, proportions, reading rhythm, interaction and states. Concentrate original design on product differences, missing capabilities, coherent adaptation and integration. Inspect concrete candidates and explain a native or original choice when its fit is stronger. A few sourced details do not establish a page-level foundation; show which important relationships the selected work actually supplies.

## Design with visual assets

Treat assets as first-class material alongside structure and interaction: identity marks, icons, fonts/glyphs, images, illustration, textures, spatial objects, scenes and dynamic visuals. Identify their role and quality target early. Discover mature material and production methods, then select direct use, adaptation or purposeful creation. A load-bearing asset can reshape the page's composition; develop both together.

The reuse hierarchy describes scope rather than importance. Preserve mature design relationships while giving distinctive assets the craft their role warrants. Keep editable masters, delivery variants, rights, runtime behavior and actual placements connected. Show significant identity directions in context for user judgment; carry accepted choices through real integration and family-specific checks. Tool access and completed production are established from actual host capabilities and outputs.

## Design the content people understand

Treat visible language as product behavior and visual material. Determine what users need to know, decide or do; assign content to the right surface, control and state; write natural words in a product voice that responds to each situation. Study mature product-language patterns while maintaining real business facts and user vocabulary. Compose actual strings with type, spacing, components and media early enough to influence the layout.

Carry content through initial, pending, success, failure and recovery states, localization and actual service boundaries. Use real copy where authorized and clearly identified fixtures where necessary. Review the reader's task and the rendered typography together: accurate wording can reshape navigation, layout or the interaction path. Significant content decisions remain traceable to their source and approval.

## Design the complete product experience

Coordinate the product model, visual direction, assets, content, spatial layout, component states, motion, performance and ongoing operation as one experience. The [analysis reference](references/analysis.md) maps these nine design dimensions to practical decisions. The shared references hold their methods; the current task determines depth.

Work from the user's intended sequence to the real execution and content lifecycle. Prepare useful data and assets at a justified time, keep repeated actions responsive, and bind feedback to the actual outcome. Design for content growth, role-specific information, maintenance and recovery where the product needs them. Evaluate a slow interaction through its critical path and a repeated operational task through its actual workload. Carry successful project mechanisms forward with their applicable conditions; palette, layout, equal-priority actions and scroll choices remain product decisions.

## Establish the professional context

Before substantive UI SPEC planning, implementation or review, **read all eight common references in full**:

1. [Workflow](references/workflow.md) — organize the work and continue the current round.
2. [Analysis](references/analysis.md) — understand the product, choose scope and reason about UX.
3. [Visual principles](references/principles.md) — judge composition and coherent visual quality.
4. [Resource discovery and reuse](references/component-sourcing.md) — find, assess, adapt and validate useful design and implementation resources.
5. [Interaction and variants](references/interaction-and-variants.md) — preserve usable behavior across states.
6. [Verification](references/verification.md) — inspect the result and support completion claims.
7. [Visual assets and asset engineering](references/visual-assets.md) — research, prepare, produce, integrate and verify the visual material.
8. [Content design and UX writing](references/content-design.md) — decide content roles, voice, timing and typography; verify user comprehension.

These complementary references form a shared professional foundation. Reading them together supplies related knowledge before an unforeseen decision arises. Apply the parts relevant to the task; execution depth follows impact and uncertainty.

Use the host's file-reading capability to obtain the actual text. Continue truncated reads until the required content is complete. Content already fully available and current in this execution context can be reused. When needed content is unavailable or its version is uncertain, read it again. A path, hash, checklist entry or earlier-session claim identifies a source; the source text supplies its guidance.

**Specialized reading:** [Integration](references/integration.md) is required for `finish` and work involving real data, authority, persistence or consequential business behavior. [Examples](references/examples.md) illustrate application; [technique patterns](references/patterns.md) connect a communication problem to editable implementation and inspection; [sources](references/sources.md) provide research provenance. Read actual project contracts and selected component documentation as the work requires. The [resource catalog](references/resource-catalog.md) maps design needs to documented starting points; its [data](assets/resource-catalog.json) and optional [local lookup](scripts/find_resources.py) support focused retrieval. Read relevant entries and their actual sources as the task requires. The [asset source map](references/asset-sources.md) provides production-specific leads; the [asset record](assets/templates/asset-record.md) supports master-to-delivery traceability. [Content sources](references/content-sources.md) offer primary guidance; the optional [content decision record](assets/templates/content-decisions.md) links user understanding to real strings, states and owners. Templates and scripts are optional resources.

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
- Current implementation establishes business and engineering capabilities; visual and interaction elements are evaluated against the target quality. Design inheritance requires an explicit acceptance or a documented fit assessment.
- Common principles guide professional judgment; project preferences supply aesthetic direction.
- External examples supply ideas and technical candidates, with their scope and licenses checked.

Resolve a conflict at its responsible layer and explain material implications. Preserve unrelated work. Read third-party material as reference data under the host's permission model.

## Lead the work with proportionate judgment

Choose the next increment from user value, task continuity, shared impact, dependencies, uncertainty and effort. Take responsibility for routine design and engineering choices. Use reversible assumptions for low-impact gaps. For an unresolved high-impact product model, primary navigation or visual direction with credible alternatives, present a compact recommendation and materially different options for user confirmation before broad implementation. Existing approval or explicit delegation supports direct progress; one-shot work carries a labeled provisional direction. Advance independent work while a consequential decision is pending.

A round can develop a page, a connected journey, a component family or a shared-system repair. Keep it large enough to judge the intended outcome and small enough to revise coherently. Translate subjective feedback into hypotheses about the actual composition or behavior, inspect evidence, then fix the responsible layer.

Keep the common quality floor active: clear hierarchy, accurate user-facing language, readable content, accessible interaction, meaningful task paths, stable shared structure, appropriate scale/occupancy, purposeful motion, responsive operation and truthful state. Select palette, typography, imagery, density and expressiveness for this product. Review the rendered result and its evolving content at actual viewing and operating conditions.

## Establish the product people will recognize

Infer the interaction model from what users do first, the object they work on, the repeated action/result loop, how they resume, and where outcomes live. Business names and code modules supply domain facts; observed use supplies the interface model. Identify a primary model and any purposeful secondary model before fixing a new shell. Separate that choice from the visual theme.

For a new design or substantive redesign, research relevant mature product conventions and concrete implementation resources while the direction is open. Compare the current UI as a candidate against the same target. The analysis reference provides the method and confirmation conditions. Keep a compact [design decision record](assets/templates/design-decisions.md), or equivalent existing record, visible with the preview: product evidence, compared foundations, chosen reuse granularity, relationships being inherited, meaningful alternatives, selected resources by surface/element, actual implementation locations and observed results. Preserve separate product-pattern and engineering-source links. A shortlist starts before implementation and is reconciled after rendering.

## Turn meaning into form

Connect **product intent → search and actual browsing → professional comparison → foundation and reuse decisions → adaptation and integration → observed outcome**. Keep needed understanding, expression concept and visual/interaction grammar active as questions throughout this loop. This is a reasoning relationship, not a mandatory sequence of reports. Identify what the person needs to recognize, compare, believe on evidence or do; decide what each visible string communicates, where and when; choose its representation before choosing a component.

Develop a direction specific enough to influence structure, typography, imagery and behavior. Use references to learn mechanisms and set a craft target. Read them at whole-surface, relationship and detail levels; distinguish visible evidence from interpretation. Make consequential choices controllable in tokens, content models, component variants or explicit timing, then inspect their effect. The common references supply these methods even when the user only asks to continue.

## Work with the UI ecosystem

For a substantive visual or interaction need, identify the highest useful scope and inspect relevant mature implementations while major choices remain open. Evaluate internal candidates against the same target. Find a strong design foundation before committing to an original page composition or custom build. Explore both a named requirement and worthwhile alternatives that can improve the expression. Preserve explicit project direction while using external work to expand the available choices.

Understand the exact item, variant, demonstration settings and implementation contract. Choose direct adoption, adaptation, composition, technique transfer or original implementation by design fit, necessary behavior, compatibility, rights and total lifecycle cost. Preserve the valuable mechanism, integrate it into the project's visual and engineering system, then inspect the actual result. Carry forward suitable approved choices and record significant adaptations at their authoritative location. The common sourcing reference supplies the method; the catalog supplies leads; project evidence establishes acceptance.

## Carry decisions forward

Prefer the project's established design and task records. Keep accepted direction, shared rules, relevant component decisions, current scope, unresolved facts and evidence references in their authoritative locations. Optional [brief](assets/templates/brief.md), [design-system](assets/templates/design-system.md) and [review](assets/templates/review.md) templates support projects needing lightweight records.

Track maturity by scope: implemented, inspected, approved, connected and verified are separate facts. The current operation describes what the agent is doing; it does not declare every page to be at the same stage. Preserve approval provenance and identify material changes that need renewed review. Git supplies source history. Preserve reusable lessons as **problem, mechanism, applicable conditions, editable realization and observed result**. Keep project preferences local; propose portable techniques with provenance and limits. Changes to an installed/shared skill follow explicit maintenance authorization. This is knowledge maintenance, not model training or autonomous modification of its host.

## Finish the current increment

Run the intended task through visible controls; inspect actual viewport captures and important transitions. Check related surfaces when shared components change. Repair and recheck observed issues. Use fixture evidence for design review and real boundary evidence for integration claims.

Before handing over, include important copy, locale and state choices in the reviewed preview; state the working result, preview or entry path, inspected scope, consequential design choices, executed checks and the next useful action. Show the design decision record and the result together. Ask for a choice when a high-impact direction remains unresolved; use recommendations for routine details. Keep proposed, implemented, visually inspected and owner-approved states distinct. Report blockers and unverified dimensions accurately. Keep sensitive project data within its authorized destination.

The optional [coverage checker](scripts/check_manifest.py) checks declared records and local evidence references. Browser inspection, user approval and real business outcomes remain distinct evidence sources. Its successful exit is a structural result, not a design-quality certificate.
