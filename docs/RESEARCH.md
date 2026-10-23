# Research and design rationale

Initial design research: **2026-10-23**. Format and distribution guidance rechecked on **2026-10-24**. Repositories evolve; inspect current files and licenses when updating a source-specific recommendation.

## What informed this skill

| Source | Observed focus | Application here |
|---|---|---|
| [Emil Kowalski — design engineering](https://github.com/emilkowalski/skills/blob/main/skills/emil-design-eng/SKILL.md) | Interface polish, purposeful motion, interaction frequency, continuity and small component details | A task-sensitive interaction review and motion checks; project-specific decisions determine exact timing and styling. |
| [Emil Kowalski — picking a UI library](https://github.com/emilkowalski/skills/blob/main/skills/pick-ui-library/SKILL.md) | Match the problem and existing dependencies before choosing another library | Component roles, incumbent reuse and bounded candidate comparison. |
| [Impeccable](https://github.com/pbakaus/impeccable/blob/main/.agents/skills/impeccable/SKILL.md) | Product/design context, distinct surface purposes, critique/audit/refinement commands and rendered inspection | Separate analysis lenses, surface-sensitive rules and an audit operation that participates in each round. |
| [Impeccable — shape](https://github.com/pbakaus/impeccable/blob/main/.agents/skills/impeccable/reference/shape.md) | Establish UX intent and constraints before choosing visual form | User outcomes, page responsibilities and the brief that directs a runnable slice. |
| [Leonxlnx — Taste Skill](https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md) | Subject-specific art direction, meaningful imagery, page/app distinctions and browser look-and-fix work | Deliberate direction, content-led composition, honest asset selection and visual iteration. |
| [Agent Skills specification](https://agentskills.io/specification) | Named SKILL.md entry, optional scripts/references/assets and progressive disclosure | A compact entry, six common required references and specialized supporting material. |
| [Vercel Skills CLI](https://github.com/vercel-labs/skills) | Git repository/local-path installation and explicit skill/agent selection | Familiar `npx skills add` distribution without a custom installer service. |
| [W3C Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) and [WAI APG](https://www.w3.org/WAI/ARIA/apg/) | Content accessibility across viewing conditions and semantic interaction patterns | Reachable content, zoom/reflow checks, keyboard/focus and native-affordance requirements. |
| [Playwright screenshots](https://playwright.dev/docs/screenshots) | Viewport, full-page and element capture capabilities | Evidence types distinguished by what they actually show. |

## Original synthesis

The **init / iterate / finish lifecycle with optional shape and reusable audit**, the page/state coverage format and the actual integration completion gate are this project's synthesis. They are not represented as a prescribed workflow from any cited author.

The design is grounded in repeated practical concerns: page proliferation without coherent tasks, shared-shell movement during navigation, viewport-preview confusion, local animation discontinuity, imbalanced composition, and a gap between approved prototypes and real behavior. Those concerns become general checks rather than a specific project's colors, fonts, page names, frameworks or commerce rules.

## Why these choices

**Small public interface, complete execution.** Three main operations, optional shape and a reusable audit make the work easy to resume. Research, review, visual audit, approval and integration regression remain explicit activities within them. An independent audit supports existing-project diagnosis.

**A floor and a direction.** Legibility, truthful content, accessible operation and continuity are shared obligations. Density, palette, materials, stylistic novelty, ornament and motion strength are choices tied to the subject and task. A compact form's optical center and a long document's flow can both be appropriate.

**A connected screen system.** Pages are justified by user outcomes and state transitions. Return and recovery paths can form cycles. Global navigation, development preview access and actual task access have distinct roles.

**Open component ecosystem.** Capability, framework fit, behavior, accessibility, performance and license determine selection. A design kit is a visual reference; a primitive provides behavior; an effect provides presentation. Their roles are recorded accurately.

**Evidence without false certification.** The optional checker establishes record consistency, not taste or real-world effectiveness. Visual inspection, host behavior and service integration require their own tests.

**Integration is part of completion.** An approved design is a reference for real code, data and state behavior. The skill carries the project through that work and its regression, while respecting publishing and real-world action authorization.

## Source boundaries and licensing

The skill text, templates and Python tools are original to this repository. Source projects are linked for methodological attribution; their scripts, images, fonts and skill bundles are not redistributed here. There is no endorsement or affiliation claim.

At review time, Emil's skills and Taste Skill declared MIT licenses; Impeccable declared Apache-2.0. If a future contribution copies code or material, preserve the relevant license notices and identify the actual copied portion. Component and asset licenses must be checked at selection time.

## Verification status

Research establishes what the cited sources describe. Local package tests establish the mechanics they exercise. Model-level effectiveness and actual product outcomes have their own evidence boundaries; see [assurance](EVALUATION.md). This release uses logical scenario analysis and deterministic engineering tests, with comparative model research available as an optional extension.

## Common professional context

The six-reference reading contract is this project's cost/quality decision. Its
short, related references support unforeseen design judgments without requiring
a model to predict every missing knowledge area. Integration remains a specialized
requirement. The Agent Skills format supports linking these resources; it does not
guarantee runtime activation, retention or comprehension.

The [writing standard](WRITING.md) uses final-state, task-oriented language informed
by [no-negative-echo](https://github.com/LB623/no-negative-echo). The accepted model
and file-level review are documented separately from runtime instructions.
