# Installation and invocation

## Official npm installer (recommended)

The official `ui-spec-studio` npm package was first publicly verified at version `1.20.3`, through registry readback, the actual npm-named CLI and SHA-512 comparison with the immutable GitHub Release. The `latest` dist-tag resolves the currently published version; each newer version, including `1.20.5`, requires its own release and public integrity acceptance. The **canonical, version-independent** terminal entry point is:

```powershell
npx --yes ui-spec-studio@latest
```

The installer selects a coding Harness interactively; without `--global`, the default scope is the current project. The archive contains only the portable `ui-spec` Skill and the necessary native Harness integration, not the several-gigabyte GitHub source repository. Node.js 20+ is required; the Codex native adapter additionally requires Python 3.11+. The optional `@clack/prompts` dependency provides the interactive terminal presentation, while non-TTY sessions keep machine-readable output.

For explicit Harness-specific project installation:

```powershell
npx --yes ui-spec-studio@latest install --agent codex
npx --yes ui-spec-studio@latest install --agent claude-code
npx --yes ui-spec-studio@latest install --agent cursor
npx --yes ui-spec-studio@latest install --agent opencode
```

The Codex adapter installs four native roles: `ui_researcher`, `ui_integrator`, `ui_challenger`, and `ui_experience_observer`. They are registered but not launched by installation.

Use `--global` for the host's **user scope** or `--project PATH` for a specific consumer project; never combine them. `--dry-run` previews the action without writing; `status` and `uninstall` must use the same Harness and scope as the original installation:

```powershell
npx --yes ui-spec-studio@latest install --agent codex --global --dry-run
npx --yes ui-spec-studio@latest status --agent codex --global
npx --yes ui-spec-studio@latest install --agent codex --global --upgrade
npx --yes ui-spec-studio@latest uninstall --agent codex --global
```

### Existing Skills CLI installation / migration

An older installation in `C:\Users\<username>\.agents\skills\ui-spec` may have no unified-installer ownership receipt. This is normal if it was installed with `npx skills add`; **do not manually delete the directory**. On Windows, to migrate it into a managed user-scoped Codex installation:

```powershell
npx --yes ui-spec-studio@latest install --agent codex --global --migrate --lang zh
```

The default interactive workflow also offers to **adopt** a byte-identical Skill, **back up and migrate** an older or edited Skill, or **keep it unchanged**. `--migrate` explicitly authorizes a backup first; `--yes` alone does not authorize replacement. Windows Junctions and POSIX symlinks are treated as links: the installer migrates the Skill location without altering its backing source. Uninstall restores the original copy or link.

A safe preview is available:

```powershell
npx --yes ui-spec-studio@latest install --agent codex --global --migrate --dry-run
```

The packaged manifest verifies every file with SHA-256, staged files are checked before replacement, and native Harness registrations remain separately guarded. Do not run the same installer in multiple terminals against the same Skill directory.

### Immutable GitHub Release fallback

If npm registry resolution is unavailable, use the **specific public release**, not the mutable `releases/latest/download/ui-spec-installer.tgz` URL. npm can reuse stale cached bytes for an unchanged tarball URL:

```powershell
npx --yes "https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.5/ui-spec-installer.tgz" install --agent codex --global --migrate
```

The fixed-version release is a standard npm-executable tarball. Avoid `npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec` as the recommended installation; some Skills CLI versions first clone the entire multi-gigabyte repository.

## Standard Skills CLI compatibility: portable Skill only

For a host that already manages Skill installation through the [Skills CLI](https://skills.sh/docs/cli), install the independent release ZIP (not the source repository) explicitly:

```bash
npx skills add https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.5/ui-spec-1.20.5.zip --skill ui-spec -a codex
```

This installs the **portable Skill alone**, not the four Codex native agents. The Codex adapter is separately available as `ui-spec-codex-1.20.5.zip` for manual installation. Do not use both installers against an already managed Skill directory without first examining ownership receipts; neither will silently take over a copy managed by the other.

For a fixed independent-installer version rather than the latest release:

```bash
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.5/ui-spec-installer.tgz install --agent codex
```

The GitHub fallback package is a standard npm executable tarball. The **separately named official npm distribution** requires npm registry ownership and a one-time bootstrap; GitHub repository permission alone does not authorize npm publication. Other Harness adapter modules can be declared in `installer/harnesses.json` and bundled under `integrations/` without adding host-specific logic to the Skill instructions.

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

Use the same standalone installer for its own managed installations: `status`, `install --upgrade` and `uninstall`. They preserve unowned and modified user files. If a previous copy was installed through Skills CLI, use that CLI's `check`, `update` and `remove` commands for **that** copy; do not mix ownership records or manually overwrite a configuration.

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
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.5/ui-spec-installer.tgz install --agent codex
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

## Optional adaptive research support

The portable Skill still works with a single agent. See [the Codex adapter](../integrations/codex/README.md) for explicit installation of all four roles, natural delegation, model/GUI limitations and safe upgrade/uninstall. Role installation does not install or authenticate Codex and does not change permissions. See [the current development review](REVIEW-v1.20.0.md) before treating this candidate as validated.

When the host does not load the installed project registrations, the adapter's optional Python 3.11+ launcher registers the installed roles for one Codex invocation:

```bash
python integrations/codex/launch.py --project /path/to/product
```

The launcher enables native multi-agent support for that invocation and preserves the host's model, authentication and sandbox choices. `--dry-run` prints the exact argument array without starting Codex or writing files; `--` forwards native Codex arguments. The adapter guide documents file checks, rejected conflicting options and the requirement for a native custom-role selector in the chosen host/model interface.
