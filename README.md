# UI Spec Studio

**A design practice for your agent.**

<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="docs/assets/studio-compact-dark.svg">
  <source media="(max-width: 600px)" srcset="docs/assets/studio-compact-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/studio-dark.svg">
  <img src="docs/assets/studio-light.svg" alt="From meaning to form: connect user intent, designed relationships and a working result." width="1100">
</picture>

[简体中文](README.zh-CN.md) · [Start here](docs/GUIDE.md) · [Inside the skill](skills/ui-spec/SKILL.md) · [Releases](https://github.com/D1ChangGeng/UI-Spec-Studio/releases)

Turn a product goal into a coherent, reviewable interface—and carry the accepted experience into real use. UI Spec Studio is a portable [Agent Skill](https://agentskills.io/specification) for product screens, documentation, READMEs, diagrams and other screen-based work.

## Start with one command

```bash
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec
```

Then ask your coding agent:

```text
Use ui-spec. Understand this project and build the first useful UI SPEC.
I have a goal but no visual direction. Recommend a direction and show the result.
```

You can bring a detailed reference or just a goal. The agent develops the direction, chooses the next useful increment, makes it, inspects it and continues from your feedback.

Already have an accepted design? Ask it to `finish` the real integration. [Installation and host options →](docs/INSTALL.md)

## Design is a chain of decisions

**Meaning → concept → representation → visual language → implementation → evidence.**

Before choosing a card, table, diagram or animation, establish what the person needs to understand. Develop a concept that belongs to the subject. Make its relationships controllable in code. Judge the actual result.

| Capability | What the agent works out |
|---|---|
| **Understand** | User tasks, content meaning, page responsibilities and the information needed to act |
| **Compose** | A grounded direction, suitable representations, typography, color, space, imagery and attention over time |
| **Build** | Components, media and editable controls that carry the intended design into the actual delivery format |
| **Inspect** | Whole-surface meaning, structural relationships and details, followed by causal repair and real task verification |

[Read the professional model](docs/PROFESSIONAL-MODEL.md) · [Explore conditional techniques](skills/ui-spec/references/patterns.md)

## One continuous practice

**init → iterate → finish**

Use **shape** when an important direction is open. Use **audit** whenever the current scope needs examination. These are intent labels; ordinary language is enough.

**Begin.** The agent reads the product and existing implementation, inherits what is already decided and selects a useful next outcome.

**Continue.** Say “approved, continue.” Each round can develop a page, connect a journey, refine a component family or repair a shared problem. The agent owns routine analysis, component research and rendered checks.

**Connect.** Finish reconciles the approved design with real content, services, permissions and persistence. It verifies meaning, structure, visual fidelity and behavior/timing. Static artifacts finish against their own publishing boundary.

```text
This feels too low. Inspect the complete composition and fix the cause.

Keep the accepted direction. Continue with the next valuable user task.

The reviewed scope is approved. Connect it to the real product and verify both
its design and its actual behavior.
```

## A complete professional foundation

The agent reads **six common references in full** before substantive work:

[Workflow](skills/ui-spec/references/workflow.md) · [Analysis](skills/ui-spec/references/analysis.md) · [Visual principles](skills/ui-spec/references/principles.md) · [Components & media](skills/ui-spec/references/component-sourcing.md) · [Interaction](skills/ui-spec/references/interaction-and-variants.md) · [Verification](skills/ui-spec/references/verification.md)

[Integration](skills/ui-spec/references/integration.md) becomes required for real behavior. Techniques and examples add depth where useful. Existing context can be reused when complete and current.

The skill supplies professional methods and a reading contract. Your host supplies activation, tools, execution and context management. Routine design decisions stay with the agent; consequential commitments stay within the user's authority.

## Open to the right medium

Use the current project and the means that fit its task: native controls, component systems, icons, actual imagery, authored graphics, data visualization or specialist tools. React/Vue Bits, Magic UI, Lucide and other sources are candidates—not a prescribed stack. Existing verified choices are a starting point; new choices are inspected for fit, behavior, performance and licensing.

A research workspace, a focused form and a publication deserve different compositions. Shared principles support quality; the subject and accepted brief define the style.

### This README is one worked example

Its reading path moves from purpose to installation, first use, deeper methods and evidence. Essential instructions remain native text. The editorial artwork has editable source, light/dark versions and a distinct narrow composition. [See its design brief and verification conditions.](docs/design/README-SPEC.md)

## Install where you work

```bash
# Project install for a specific host
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec -a codex

# Fixed release
npx skills add https://github.com/D1ChangGeng/UI-Spec-Studio/tree/v1.2.0 --skill ui-spec
```

Claude Code and OpenCode are also tested installer targets. The core is Markdown; optional record helpers use Python 3.10+ and its standard library. [Offline installation and updates](docs/INSTALL.md).

## Inspect the evidence

The release pipeline checks package integrity, local references, helper behavior, reproducible archives and standard installer paths. Publication checks cover the bilingual README, generated assets and browser rendering. Release assets include source, the standalone skill and checksums.

These establish the checks actually exercised. Design quality and real integration are reviewed in each consuming project. [Assurance boundaries](docs/EVALUATION.md) · [CI runs](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/workflows/validate.yml) · [Change log](CHANGELOG.md)

<details>
<summary><strong>For maintainers: model, writing and release tools</strong></summary>

[Understanding model](docs/MODEL.md) · [Writing standard](docs/WRITING.md) · [v1.2 review](docs/REVIEW-v1.2.0.md) · [Research](docs/RESEARCH.md) · [Coverage records](docs/MANIFEST.md) · [Publishing](docs/PUBLISHING.md)

```bash
python tools/validate_package.py
python tools/readme_art.py --check
python -m unittest discover -s tests -v
python tools/package.py
```

See [contribution guidance](CONTRIBUTING.md) and [security policy](SECURITY.md).

</details>

Original methods and tooling, informed by [credited design and production references](skills/ui-spec/references/sources.md). [MIT License](LICENSE).
