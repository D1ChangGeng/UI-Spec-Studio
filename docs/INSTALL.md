# Installation and invocation

## Standard Skills CLI

Run installation from the project that should use the skill. Use a Node.js version supported by the selected Skills CLI; the release smoke test uses Node 24 and skills 1.7.4. Network access is required to obtain the CLI; the installed skill's core instructions run without a separate service.

From the source repository:

```bash
npx skills add D1ChangGeng/UI-Spec-Studio --list
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec -a codex
```

For a local extracted or cloned repository:

```bash
npx skills add /absolute/path/to/ui-spec-studio --skill ui-spec -a codex
```

Other explicit targets:

```bash
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec -a claude-code -a opencode
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec -a cursor
npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec -a codex -g
```

`-g` selects user-wide installation; the default is the current project. `--copy` requests real copies instead of symlinks. `-y` accepts the installer's prompts; use it when the displayed source and targets are already understood. Installation does not publish a new npm package: `skills` is the existing installer, and this repository supplies skill files.

The current supported-agent list and directory mapping belong to the [installer documentation](https://github.com/vercel-labs/skills#supported-agents). Select a target actually supported by your installed CLI and host version.

## Offline copy from the source bundle

With Python 3.10 or newer:

```bash
python /absolute/path/to/ui-spec-studio/tools/install_local.py \
  --target /absolute/path/to/project/.agents/skills/ui-spec
```

For a Claude Code project, use the host's project skill directory:

```bash
python /absolute/path/to/ui-spec-studio/tools/install_local.py \
  --target /absolute/path/to/project/.claude/skills/ui-spec
```

Windows PowerShell uses the same single-line command with quoted Windows paths. `py -3` can replace `python` when appropriate. The destination is explicit, existing installations are preserved, and the complete skill folder is copied. The standalone ZIP can also be extracted so that the destination contains `ui-spec/SKILL.md`, `references/`, `scripts/`, `assets/` and `LICENSE`.

Inspect an existing installation before updating it. Use the standard installer for managed updates, or intentionally replace your own reviewed copy. Start a new agent session when the host discovers skills only at session startup.

## Verify discovery and use

```bash
npx skills list
```

Then ask the coding agent:

```text
Use the ui-spec skill. Read its entry point and tell me which operation
matches this repository's current state, then carry out the requested work.
```

The agent should read SKILL.md and all eight common references for substantive work,
then use the operation appropriate to the project's current state. Integration is
required for real behavior work. Reading and skill activation remain host-mediated.

Host-specific examples may include `$ui-spec` or `/ui-spec`, depending on the host. `init`, optional `shape`, `iterate`, `audit` and `finish` are instructions passed to the skill, not commands to execute in your shell.

## Updates and removal

Use the commands supported by your current Skills CLI:

```bash
npx skills check
npx skills update
npx skills remove ui-spec
```

Inspect scope before updating or removing a global installation. Consult `npx skills --help` and the [official CLI guide](https://skills.sh/docs/cli) for version-specific options.

## Optional project records

After installation, the agent may use its resolved skill directory:

```bash
python <skill-dir>/scripts/prepare.py --project-root /path/to/project
python <skill-dir>/scripts/check_manifest.py --project-root /path/to/project --view overview
```

`prepare.py` creates only missing `.ui-spec` records and leaves existing project files intact. Keep evidence containing private application data in the authorized project or evidence store. The default local evidence directory is Git-ignored.

## Runtime capabilities

The agent needs project read/write and execution capabilities to implement a runnable UI. Real visual review needs browser and image-inspection capabilities. Temporal review uses available live interaction, video playback or ordered-frame inspection; the observed conditions determine what can be concluded. Active reference research needs authorized browsing and interaction, network access or already available primary material. Playback, recording, network/media inspection and traces depend on the actual host tools and permissions; the Skill selects methods by the evidence question and describes remaining gaps. The optional checker needs Python 3.10+.

A standard skill format is a portability mechanism. Actual host invocation, browser availability and quality depend on the installed agent. See [evaluation status](EVALUATION.md) for the tests actually performed on this release.

## Sources

- [Agent Skills format](https://agentskills.io/specification)
- [Skills CLI repository](https://github.com/vercel-labs/skills)
- [Skills CLI documentation](https://skills.sh/docs/cli)

## Fixed version

```bash
npx skills add https://github.com/D1ChangGeng/UI-Spec-Studio/tree/v1.17.0 --skill ui-spec
```

Inspect installed files before applying upgrades to a customized local copy. The
portable skill directory contains the full runtime text and helpers; user guides
and maintainer tooling live in the complete repository bundle.

## Optional local resource lookup

The installed skill includes its self-contained discovery catalog and a read-only
standard-library helper:

```bash
python <skill-dir>/scripts/find_resources.py --list-filters
python <skill-dir>/scripts/find_resources.py --need controls --stack vue --json
python <skill-dir>/scripts/find_resources.py --id fontsource --json
```

The helper performs local filtering only. It returns dated source leads with
adoption cautions. Current external documents, demos, installation and project
acceptance use the host's available tools and the task's permissions.

## Content and UX writing

The installed Skill includes the common [content design method](../skills/ui-spec/references/content-design.md), a focused [source map](../skills/ui-spec/references/content-sources.md) and an optional [decision template](../skills/ui-spec/assets/templates/content-decisions.md). User-facing copy, localization and typography are part of ordinary design rounds. A runnable example is included in the complete repository source under `examples/content-review/`.

## Experience research and visual exploration

The installed Skill carries intent analysis, experience-based evidence planning,
deep exploration and visual judgment through its eight common references. It
combines text, visual and behavioral evidence, compares meaningful alternatives,
and chooses continued research, local trials or wider implementation from what
the evidence supports. The [research guide](EXPERIENCE-RESEARCH.md) explains the
method, the [alignment guide](PRODUCT-ALIGNMENT.md) connects it to product choices,
and the [visual guide](VISUAL-INSPECTION.md) explains inspection.
The complete source bundle includes `examples/temporal-review/`
and its browser capture tool; these development fixtures are separate from the
portable Skill's optional standard-library helpers.

## Optional design evidence views

The installed bundle includes a planned, unfilled
`assets/templates/design-evidence.json` and a read-only helper. Copy a template
only when the project chooses this format; `prepare.py` does not create it.
Use the project root as the evidence/implementation path boundary.

```bash
python <skill-dir>/scripts/check_design_evidence.py --project-root <project> --view overview
python <skill-dir>/scripts/check_design_evidence.py --project-root <project> --view execution --changed <object-id>
```

[Format and limits](../skills/ui-spec/references/evidence-records.md) explain
all fields and paths. A successful exit means declaration consistency, not
actual observation, approval, complete coverage or design quality.

## Structural inspector output migration (1.15)

Both inspectors now return `record_readability` and scoped structural observations,
not `ok`, PASS, satisfied coverage or completion gates. Exit 0 means inspection ran,
even with findings; exit 2 means input could not be read. Manifest `--mode` aliases
remain presentation-only. See [the boundary and migration guide](STRUCTURAL-INSPECTION.md).
Unfilled templates contain no inferred viewport/locale/theme or research action.
`check_file_integrity.py` independently compares a requested local SHA-256; its
match/mismatch applies only to those bytes.
