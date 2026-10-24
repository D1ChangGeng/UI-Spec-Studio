# UI Spec Studio

**Build on what works. Design what makes it yours.**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/studio-compact-dark.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/studio-compact-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/studio-dark.svg">
  <img src="docs/assets/studio-light.svg" alt="Three connected decisions: study mature design sources, select a fitting foundation, and realize an editable result." width="1100">
</picture>

[简体中文](README.zh-CN.md) · [Guide](docs/GUIDE.md) · [Skill source](skills/ui-spec/SKILL.md) · [Releases](https://github.com/D1ChangGeng/UI-Spec-Studio/releases)

A portable [Agent Skill](https://agentskills.io/specification) for **product interfaces, READMEs, documentation, diagrams and other screen-based work**. It helps agents study mature design foundations, adapt them to a task and verify the finished result.

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

## Design from an informed starting point

**Understand the task → explore real work → compare and select → adapt → inspect.**

Design theory explains *why* a composition works; the existing design ecosystem offers *what* can be studied and reused. The agent examines both while the direction is still open. New references can improve the design hypothesis, and the rendered result tests whether the choice was sound.

Reuse happens at the **highest appropriate level**: a whole-page foundation or design system, a functional block, a component family or a focused visual technique. The goal is to inherit coherent decisions—information hierarchy, proportion, typography, state and interaction—then adapt them to the current task. Original design work concentrates on the product's distinctive needs and the connections between its parts.

[Resource discovery method](skills/ui-spec/references/component-sourcing.md) · [37 dated resource leads](skills/ui-spec/references/resource-catalog.md) · [Design decision record](docs/DESIGN-DECISIONS.md) · [Resource reuse guide](docs/RESOURCE-REUSE.md)

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

| Studied foundation | What this README adopts | What was adapted here |
|---|---|---|
| [Vercel Skills CLI README](https://github.com/vercel-labs/skills/blob/main/README.md) | Immediate purpose, copyable install command and a route to deeper reference | The `ui-spec` install and first Agent instruction lead the reading path |
| [Typst README](https://github.com/typst/typst/blob/main/README.md) | A concrete visual example alongside an explanation of its mechanism | An editable editorial plate illustrates source → decision → result; the method stays in selectable text |
| [GitHub's Markdown and image guidance](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github) | Native headings, links, code blocks and theme-aware imagery | Four light/dark and wide/narrow SVG variants, with a readable text equivalent |
| Existing UI Spec Studio art direction | Restrained color roles and editorial typography | A resource-led illustration generated from the repository's editable source |

The relationships and documentation patterns are adapted as **design references**. The illustration and Markdown are maintained in this repository. The [README design record](docs/design/README-SPEC.md) tracks candidate sources, implementation choices, render checks and the limits of the evidence.

A separate [research-product example](examples/product-intent/README.md) shows page-level design transfer in an application context, including the [selected source and retained relationships](examples/product-intent/FOUNDATION.md).

## Continue through to a real result

`init → iterate → finish` is the main path. Optional **shape** resolves a consequential open direction; **audit** examines quality or coverage at any point. These describe work intentions rather than shell commands.

Each round gives the agent a useful scope to implement and inspect. An accepted design can continue into working product behavior, or into a document's actual publishing boundary. The agent carries forward decisions, evaluates the affected views and states, and keeps source evidence distinct from owner approval.

Before substantive work, the agent reads **six common references in full**: [workflow](skills/ui-spec/references/workflow.md), [analysis](skills/ui-spec/references/analysis.md), [visual principles](skills/ui-spec/references/principles.md), [resource discovery](skills/ui-spec/references/component-sourcing.md), [interaction](skills/ui-spec/references/interaction-and-variants.md) and [verification](skills/ui-spec/references/verification.md). [Integration](skills/ui-spec/references/integration.md) applies when connecting real behavior. The host remains responsible for tool access, execution and context management.

## Install, inspect, maintain

```bash
# Install for Codex in the current project
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec -a codex

# Pin the published skill release
npx skills add https://github.com/D1ChangGeng/UI-Spec-Studio/tree/v1.4.0 --skill ui-spec
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
