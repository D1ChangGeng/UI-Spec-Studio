# UI Spec Studio

**Build on what works. Design what makes it yours.**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/studio-compact-dark.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/studio-compact-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/studio-dark.svg">
  <img src="docs/assets/studio-light.svg" alt="Three connected decisions: study mature design sources, select a fitting foundation, and realize an editable result." width="1100">
</picture>

[简体中文](README.zh-CN.md) · [Guide](docs/GUIDE.md) · [Skill source](skills/ui-spec/SKILL.md) · [Releases](https://github.com/D1ChangGeng/UI-Spec-Studio/releases)

A portable [Agent Skill](https://agentskills.io/specification) for **product interfaces, READMEs, documentation, diagrams and other screen-based work**. Understand the intended experience, investigate real evidence, compare mature work and carry its quality into a verified result.

## Start in your project

```bash
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec
```

Then give your coding agent a goal; a finished design brief is optional:

```text
Use ui-spec. Understand this project, its audience and the experience they expect.
Research the important questions, compare mature references and implementations,
and build the first reviewable SPEC. Show the result and the evidence behind it.
```

After reviewing, **“Approved, continue”** carries the accepted direction into the next useful work. **“Use ui-spec: finish”** connects an accepted design to its actual content, behavior and delivery boundary. [Installation and agent options](docs/INSTALL.md) · [Multi-round guide](docs/GUIDE.md)

## Give each increment enough room for quality

A **formal UI SPEC** is a coherent design increment in the evolving product, with a clear experience goal and an actual result to review. Keep the complete product goal, then choose the scope that allows its important qualities to receive sufficient research, implementation and verification.

- A conventional settings page can fit one SPEC when a mature system already supports its relationships.
- Composer growth, streamed answers and reading-position control can belong together when their continuous coordination is the goal.
- A shared typography change can be one SPEC spanning several pages, with their wrapping and hierarchy checked together.

The agent explains a revisable candidate plan at `init`, then keeps, splits, merges or redraws boundaries as evidence develops. Each increment builds on the current product. Research, candidate replacement and repairs serving its existing goal remain within that SPEC; unresolved quality stays visible when scope changes.

You receive the working result, important design choices, actual adopted resources and observed gaps. The first increment should establish a representative experience worth inheriting; later work can add, replace, simplify or reconsider it.

[Multi-round use](docs/GUIDE.md) · [v1.17 review](docs/REVIEW-v1.17.0.md) · [Experiment record](docs/experiments/adaptive-granularity/RESULTS.md)

## See the design take shape

Important design events become visible as the work develops: a consequential finding or resource choice, the first meaningful local result, a material mismatch and the delivered increment. The agent shows the actual object and its evidence, explains the decision and continues authorized work.

A source demo, project trial and integrated interface keep their own identities. Early previews expose what the current product already carries and what still needs correction. The same current design record supports the conversation and later work; routine searches and edits remain autonomous.

[Observable design execution](docs/OBSERVABLE-EXECUTION.md) · [v1.18 review](docs/REVIEW-v1.18.0.md)

## Understand the experience before choosing the design

“Like this product” can describe a familiar way of working, information structure, visual character or interaction detail. The agent develops a revisable interpretation, using your stated intent, relevant user experience and the reference product's actual behavior as distinct evidence.

Research follows the **task, pages, states and their relationships**. Product documentation and user material explain meaning; rendered interfaces reveal visual craft; actual operation and continuous media reveal behavior over time. The useful version, platform and conditions follow the intended experience. Findings can change the product model, search direction or chosen resource.

[Experience research and evidence planning](docs/EXPERIENCE-RESEARCH.md) · [Product alignment](docs/PRODUCT-ALIGNMENT.md)

## Visual material is part of the design

Identity, icons, type, illustration, imagery, spatial graphics and dynamic assets
work with layout and interaction. Research suitable material, choose a production
route, keep editable masters and delivery variants connected, then inspect the
actual placement, loading and quiet states. A strong asset can reshape the whole
composition. [Asset practice](docs/VISUAL-ASSETS.md) · [Browser review fixture](examples/asset-review/README.md)

## Carry reference quality into the implementation

**Target quality → mature implementation → local trial → focused adaptation → verified product experience.**

**Product UI Experience Alignment** gives the work its goal: design maturity suited to the current users, tasks, content and operating conditions. A named reference supplies an entry point; an open brief prompts the agent to find one. Research identifies useful relationships in composition, type, component detail, state feedback and continuous interaction, while the current product develops its own expression.

**Mature implementations are the default source for general UI.** Pair reference research with resource selection at the highest appropriate level: page, design system, layout, block, component, asset or motion. Inspect consequential candidates in their original demos, then trial them with the project's content, fonts, theme and states before broad integration. Configure, compose and extend the selected implementation while preserving the relationships that earned adoption. Custom work addresses demonstrated gaps.

Review the assembled interface and continuous task again. The adoption record shows which implementation actually carries the intended quality, what changed and what was verified; studying a source and using it are recorded separately. [Product alignment and exploration](docs/PRODUCT-ALIGNMENT.md) · [Resource reuse guide](docs/RESOURCE-REUSE.md)

[37 dated resource leads](skills/ui-spec/references/resource-catalog.md) · [Design decision record](docs/DESIGN-DECISIONS.md)

## Reuse visual craft, not only functionality

A functional component library can supply reliable controls without resolving the page's typography, material or motion. Study mature pages, blocks, visual components and assets at the scope the task needs. Judge their **observed visual completeness** separately from how much functionality they cover.

Use craft knowledge to find and compare better sources, then retain their useful relationships through configuration, composition and focused adaptation. External demos provide the main positive examples; named libraries are starting points, not a closed list or quality guarantee. Professional software can keep a distinctive artistic identity throughout real work.

[Role/scope lookup and three scoped applications](docs/REVIEW-v1.16.1.md)

[Visual-craft reuse](docs/VISUAL-CRAFT-REUSE.md) · [Finesse research and boundaries](docs/FINESSE-ADAPTATION.md) · [Scoped application evidence](docs/REVIEW-v1.16.0.md)

## Give familiar work an independent visual language

**Art Direction** coordinates subject, type, composition, material and motion around the product's intended character. Professional tools can carry strong artistic expression. Explicit aesthetic goals remain delivery requirements alongside clear tasks, accurate states and reliable use.

For **Expressive Contrast**, study functional experience, cross-domain expression and actual implementation resources together. Compare meaningful directions through equally resolved previews, then translate the choice into a role-based visual system. Mature resources and focused asset production carry that language into populated inputs, navigation, results and repeated work.

Review **experience validity** and **expressive completion** independently. Source fidelity protects selected or approved design details; perceptual inspection judges the rendered result. Authored timelines can support repeatable frame comparisons, while working products need actual interaction and runtime evidence. [Art direction and expressive design](docs/ART-DIRECTION.md)

## Connect design decisions across scales

A **multiscale design evidence map** links product goals, journeys, pages,
functional regions, perceptual details and actual implementation. Challenge
initial coverage against user tasks and real references; keep evidence,
adoption, verification conditions and owner approval distinct.

The Agent uses important gaps and actual evidence to choose research, comparison
or local trials, and scopes implementation commitments accordingly. Use the same
records for **Overview · Design Detail · Execution & Assurance**. Existing
Markdown records work.

The structural inspector describes what is represented; the Agent
judges applicability and next steps, and actual use verifies the result. Declared
results, exceptions and absent records remain separate. Current choices link to
meaningful revisions and original evidence without turning history into a second
current model.

[Structural boundaries and migration](docs/STRUCTURAL-INSPECTION.md) ·
[Method and examples](docs/DESIGN-EVIDENCE.md) ·
[Comparative experiment protocol](docs/experiments/design-evidence/PROTOCOL.md)

## Explore until the important choices have evidence

**Evidence-driven exploration** connects a question to search, actual observation, comparison and the next useful question. Research effort follows design impact, uncertainty and potential improvement. A defining font, background or interaction can warrant sustained work across many independent sources; an established component can proceed with focused validation.

Inspect materially different candidates and seek alternatives that could change the initial choice. Follow useful clues through playback, scrolling, state changes, source research and local trials. When access is incomplete, pursue legitimate alternative evidence and request focused user assistance where needed. Keep observed facts, source descriptions, professional judgments and remaining gaps identifiable.

**Human-centered Visual Inspection & Perceptual Design Analysis** turns real viewing into design judgment. Start at normal scale with the whole impression and attention hierarchy; examine composition, functional regions and consequential component or asset details; then return to the whole. Choose relevant dimensions such as type, optical balance, color, material and motion to explain how the relationships create quality and which mature implementation can carry it.

Review spans **the frame, the changing interaction and the connected journey**. Temporal Visual Inspection follows the trigger, first feedback, transition and settled outcome. Normal-speed observation establishes the overall experience; useful detail views and replay explain it before another contextual review. The behavior and decision determine depth.

Judge evidence through coverage, detail, time, relevance and reliability. Continue where a gap or a better candidate could change the choice; trial a supported direction; expand after consequential fit is demonstrated. Search counts and elapsed time describe effort, while the decision rests on what the evidence establishes.

[Research method](docs/EXPERIENCE-RESEARCH.md) · [Visual observation](docs/VISUAL-INSPECTION.md) · [Temporal example](examples/temporal-review/README.md)

## Words are part of the interface

The agent designs **what people need to understand, where the message belongs, how it sounds and how it reads on screen**. Content design and UX writing connect accurate product facts, user vocabulary, action labels, dynamic feedback, localization and typography with the existing page and visual system. A line of copy can change layout or a task path; the rendered result can improve the wording.

[Content design guide](docs/CONTENT-DESIGN.md) · [Working bilingual example](examples/content-review/README.md)

## Design for actual use and continued operation

Connect the product model, visual material, content, layout, component states and motion with **responsive tasks and maintainable content**. Trace repeated actions from input to usable result and confirmed completion; choose preparation, concurrency and caching by their actual benefit and validity. Keep object and scroll continuity through change. Design shared content, individual overrides and batch recovery around the work the product really supports.

[Complete experience model](docs/EXPERIENCE-QUALITY.md) · [Runtime and operational integration](skills/ui-spec/references/integration.md) · [Verification methods](skills/ui-spec/references/verification.md)

## One method, different surfaces

The principles transfer; the **medium determines the realization and verification**.

| Surface | The user's primary experience | What a finished SPEC must establish |
|---|---|---|
| **Product UI** | Start, complete and resume a task | Usable states, stable layout, meaningful actions and real outcomes |
| **READMEs & docs** | Understand a tool, copy a command, find the next answer | Reading order, native text and links, host rendering, image/theme and narrow-width behavior |
| **Diagrams & data views** | Trace relationships, interpret values or compare alternatives | Correct semantics and encoding, readable labels, source mapping and accessible equivalents |
| **Slides & visual media** | Follow an explanation through space and time | Clear attention sequence, editable assets and verified output at its intended size or playback conditions |

The [professional model](docs/PROFESSIONAL-MODEL.md) and [conditional techniques](skills/ui-spec/references/patterns.md) connect these decisions to typography, composition, color, imagery, interaction and timing.

## This README evolves through UI SPECs

This repository's own front page is a **reading and publishing surface**, rather than an application screen. Its first task is helping a new reader judge fit and try the skill. Its visual treatment carries that purpose without replacing native Markdown content.

The design borrows **relationships and publishing techniques**, with the full adoption record in the [README design specification](docs/design/README-SPEC.md):

- **[Vercel Skills CLI](https://github.com/vercel-labs/skills/blob/main/README.md) — start with an action.** Its quick install and deeper reference path inform the placement of our first command and Agent instruction.
- **[Typst](https://github.com/typst/typst/blob/main/README.md) — show the idea, then explain it.** An editable editorial plate makes the source → decision → result relationship visible; the method remains in readable text.
- **[GitHub's Markdown guidance](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github) — use the host's own strengths.** Native headings, links and code blocks are paired with four theme/viewport-aware SVG variants.
- **Existing UI Spec Studio artwork — inherit a coherent identity.** Its restrained palette and editorial typography carry forward into the new resource-led composition.

These are design-reference adaptations. The illustration and Markdown are maintained in this repository; the [design record](docs/design/README-SPEC.md) links candidate sources, implementation, render checks and evidence limits.

A separate [research-product example](examples/product-intent/README.md) shows page-level design transfer in an application context, including the [selected source and retained relationships](examples/product-intent/FOUNDATION.md).

## Continue through to a real result

`init → iterate → finish` is the main path. Optional **shape** resolves a consequential open direction; **audit** examines quality or coverage at any point. These describe work intentions rather than shell commands.

Each formal SPEC gives the agent a coherent experience scope to implement and inspect. Research and repairs can continue inside it across several execution rounds. An accepted design can continue into working product behavior, or into a document's actual publishing boundary. The agent carries forward applicable decisions, evaluates the increment and affected product relationships, and keeps source evidence distinct from owner approval.

Before substantive work, the agent reads **eight common references in full**: [workflow](skills/ui-spec/references/workflow.md), [analysis](skills/ui-spec/references/analysis.md), [visual principles](skills/ui-spec/references/principles.md), [resource discovery](skills/ui-spec/references/component-sourcing.md), [interaction](skills/ui-spec/references/interaction-and-variants.md), [verification](skills/ui-spec/references/verification.md), [visual assets](skills/ui-spec/references/visual-assets.md), and [content & UX writing](skills/ui-spec/references/content-design.md). [Integration](skills/ui-spec/references/integration.md) applies when connecting real behavior. The host remains responsible for tool access, execution and context management.

## Install, inspect, maintain

```bash
# Install for Codex in the current project
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec -a codex

# Pin the published skill release
npx skills add https://github.com/D1ChangGeng/UI-Spec-Studio/tree/v1.18.0 --skill ui-spec
```

The installer is also exercised with Claude Code and OpenCode targets. Core guidance is Markdown; optional record helpers require Python 3.10+ and the standard library. [Offline installation and updates](docs/INSTALL.md).

Package checks cover references, helpers, installation paths and reproducible archives. The publication checks exercise the bilingual README, its responsive images and rendered layouts. A consuming project's design quality and connected behavior have their own verification evidence. [Assurance scope](docs/EVALUATION.md) · [CI](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/workflows/validate.yml) · [Changelog](CHANGELOG.md)

<details>
<summary><strong>Maintainer references and local checks</strong></summary>

[Content integrity audit](docs/REVIEW-v1.13.0.md) · [Continuity procedure](docs/CONTENT-INTEGRITY.md) · [Understanding model](docs/MODEL.md) · [Writing standard](docs/WRITING.md) · [Research sources](docs/RESEARCH.md) · [README design record](docs/design/README-SPEC.md) · [Publication process](docs/PUBLISHING.md) · [Contribution guide](CONTRIBUTING.md) · [Security](SECURITY.md)

```bash
python tools/validate_package.py
python tools/readme_art.py --check
python tools/catalog_docs.py --check
python -m unittest discover -s tests -v
python tools/package.py
```

</details>

[MIT License](LICENSE) · [Design and research acknowledgments](skills/ui-spec/references/sources.md)
