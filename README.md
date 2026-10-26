# UI Spec Studio

**Build on what works. Design what makes it yours.**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/studio-compact-dark.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/studio-compact-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/studio-dark.svg">
  <img src="docs/assets/studio-light.svg" alt="Three connected decisions: study mature design sources, select a fitting foundation, and realize an editable result." width="1100">
</picture>

[简体中文](README.zh-CN.md) · [Guide](docs/GUIDE.md) · [Skill source](skills/ui-spec/SKILL.md) · [Releases](https://github.com/D1ChangGeng/UI-Spec-Studio/releases)

A portable [Agent Skill](https://agentskills.io/specification) for **product interfaces, READMEs, documentation, diagrams and other screen-based work**. It helps agents carry mature design quality into the current product through active visual research, actual resource adoption, focused adaptation and verified implementation.

## Start in your project

```bash
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec
```

Then give your coding agent a goal; a finished design brief is optional:

```text
Use ui-spec. Understand this project and its audience.
Find strong existing design references, choose a suitable foundation,
and build the first reviewable SPEC. Show the result and your decisions.
```

After reviewing, **“Approved, continue”** advances the next useful increment. **“Use ui-spec: finish”** connects an accepted design to its actual content, behavior and delivery boundary. [Installation and agent options](docs/INSTALL.md) · [Multi-round guide](docs/GUIDE.md)

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

## Give familiar work an independent visual language

**Art Direction** coordinates subject, type, composition, material and motion around the product's intended character. Professional tools can carry strong artistic expression. Explicit aesthetic goals remain delivery requirements alongside clear tasks, accurate states and reliable use.

For **Expressive Contrast**, study functional experience, cross-domain expression and actual implementation resources together. Compare meaningful directions through equally resolved previews, then translate the choice into a role-based visual system. Mature resources and focused asset production carry that language into populated inputs, navigation, results and repeated work.

Review **experience validity** and **expressive completion** independently. Source fidelity protects selected or approved design details; perceptual inspection judges the rendered result. Authored timelines can support repeatable frame comparisons, while working products need actual interaction and runtime evidence. [Art direction and expressive design](docs/ART-DIRECTION.md)

## Explore deeply where the decision matters

**Evidence-Driven Deep Visual Exploration** means the agent does not treat its first attractive candidate—or its existing design vocabulary—as sufficient evidence. For influential choices, it weighs design impact, what remains unknown and whether better sources could materially improve the outcome. A defining font, background, asset or motion can warrant sustained research even when small; established low-impact UI can advance quickly.

Research couples **target-experience quality** with **actual implementation resources**, crossing product, editorial, artistic, spatial and motion domains as the evidence warrants. Each observation generates a better question: search → view or operate → explain the perceptual relationship → compare a substantially different candidate → update selection or research. Breadth, detail, temporal coverage, relevance and reliability matter more than search counts.

Important choices should withstand a credible alternative at comparable completeness. Keep retrieved, actually viewed, locally trialed and adopted evidence distinct. Research converges when the choice has a sound basis and a feasible adoption path—not after a fixed number of sites or steps. [Deep exploration and decision confidence](docs/DEEP-VISUAL-EXPLORATION.md)

## Explore what the interface reveals

**Active Visual Exploration & Design Reconnaissance** turns research questions into actions: play a relevant demo, scroll through a layout, open a panel, switch states or compare component settings. New clues can change the search. Attribute each observation to its subject: the hosting page, media player, demonstrated application or content inside that application.

**Human-centered Visual Inspection & Perceptual Design Analysis** turns real viewing into design judgment. Start at normal scale with the whole impression and attention hierarchy; examine composition, functional regions and consequential component or asset details; then return to the whole. Choose relevant dimensions such as type, optical balance, color, material and motion to explain how the relationships create quality and which mature implementation can carry it.

Review spans **the frame, the changing interaction and the connected journey**. Temporal Visual Inspection follows the trigger, first feedback, transition and settled outcome. Normal-speed observation establishes the overall experience; useful detail views and replay explain it before another contextual review. The behavior and decision determine depth.

Recorded evidence, actual viewing and support for a dynamic conclusion are separate facts. Code, state and runtime measurements help explain causes and verify behavior. Research converges when consequential decisions have adequate evidence and a workable adaptation path. [Visual observation guide](docs/VISUAL-INSPECTION.md) · [Temporal review example](examples/temporal-review/README.md)

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

## This README is a UI SPEC

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

Each round gives the agent a useful scope to implement and inspect. An accepted design can continue into working product behavior, or into a document's actual publishing boundary. The agent carries forward decisions, evaluates the affected views and states, and keeps source evidence distinct from owner approval.

Before substantive work, the agent reads **eight common references in full**: [workflow](skills/ui-spec/references/workflow.md), [analysis](skills/ui-spec/references/analysis.md), [visual principles](skills/ui-spec/references/principles.md), [resource discovery](skills/ui-spec/references/component-sourcing.md), [interaction](skills/ui-spec/references/interaction-and-variants.md), [verification](skills/ui-spec/references/verification.md), [visual assets](skills/ui-spec/references/visual-assets.md), and [content & UX writing](skills/ui-spec/references/content-design.md). [Integration](skills/ui-spec/references/integration.md) applies when connecting real behavior. The host remains responsible for tool access, execution and context management.

## Install, inspect, maintain

```bash
# Install for Codex in the current project
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec -a codex

# Pin the published skill release
npx skills add https://github.com/D1ChangGeng/UI-Spec-Studio/tree/v1.12.0 --skill ui-spec
```

The installer is also exercised with Claude Code and OpenCode targets. Core guidance is Markdown; optional record helpers require Python 3.10+ and the standard library. [Offline installation and updates](docs/INSTALL.md).

Package checks cover references, helpers, installation paths and reproducible archives. The publication checks exercise the bilingual README, its responsive images and rendered layouts. A consuming project's design quality and connected behavior have their own verification evidence. [Assurance scope](docs/EVALUATION.md) · [CI](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/workflows/validate.yml) · [Changelog](CHANGELOG.md)

<details>
<summary><strong>Maintainer references and local checks</strong></summary>

[Understanding model](docs/MODEL.md) · [Writing standard](docs/WRITING.md) · [Research sources](docs/RESEARCH.md) · [README design record](docs/design/README-SPEC.md) · [Publication process](docs/PUBLISHING.md) · [Contribution guide](CONTRIBUTING.md) · [Security](SECURITY.md)

```bash
python tools/validate_package.py
python tools/readme_art.py --check
python tools/catalog_docs.py --check
python -m unittest discover -s tests -v
python tools/package.py
```

</details>

[MIT License](LICENSE) · [Design and research acknowledgments](skills/ui-spec/references/sources.md)
