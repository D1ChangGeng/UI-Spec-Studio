# Installation and invocation

## Primary: lightweight release installer (cache-safe fallback)

The official npm package `ui-spec-studio` is being prepared as the long-term, version-independent entry point. **Do not use its `npx` package-name command until the first registry publish is verified.** During bootstrap, use the exact tagged release URL below. Reusing GitHub's mutable `latest/download` tarball URL can return an older cached npm package even after a new GitHub release.

Once the verified npm package becomes public, the recommended command will become:

```powershell
npx --yes ui-spec-studio@latest install --agent codex --global
```

See [npm publication and verification](NPM-DISTRIBUTION.md) for the authorization-dependent rollout.

Run this from the consumer project. Node.js 20+ and network access to download the small release-hosted npm tarball are required; the installer has no required npm dependencies and never clones the GitHub repository. When online, npm may install its optional, version-pinned `@clack/prompts` terminal UI dependency; offline/headless execution retains deterministic command output.

```bash
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz install --agent codex
```

This **one command** installs the portable `ui-spec` Skill (all its references, scripts, templates and assets) and the separately implemented native Codex adapter with its four roles. Codex adapter setup also requires Python **3.11+**, because it safely validates and merges native TOML configuration. The roles are available for on-demand use; no agent is invoked by installation.

The same installer selects other supported Harness locations without installing Codex-specific roles:

```bash
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz install --agent claude-code
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz install --agent cursor
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz install --agent opencode
```

The default scope is the current directory. Use `--project /absolute/path` to select another consumer project or `--global` to install to the host's user scope; never combine them. `--dry-run` previews the exact destination and checks the Codex adapter without writing. Use `--upgrade` only after inspecting an existing managed copy. `status` and `uninstall` use the same `--agent` and scope options.

```bash
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz install --agent codex --dry-run
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz status --agent codex
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz install --agent codex --upgrade
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz uninstall --agent codex
```

### Existing installation / migration

To recover specifically from the older `Existing unowned Skill directory` message without deleting your data, execute the `v1.20.3` tagged tarball rather than the cached mutable `latest` alias:

```powershell
npx --yes "https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz" install --agent codex --global --migrate
```

The `--global` target is `~/.agents/skills/ui-spec`, and the installer backs up older valid Skill copies and Windows Junctions before replacing them. For diagnostics, run the identical pinned package with `--version`. Never copy the Markdown link syntax `[URL](URL)` into PowerShell; paste a plain URL or quoted URL.

If the target already contains a copy installed by `npx skills add`, the wizard detects the old `SKILL.md` (including Windows symlinks/junctions) and presents a real choice: **adopt identical files**, **back up and upgrade**, or **leave unchanged**. There is no implicit overwrite. A migrated original is saved outside any Harness Skill scanning directory, in the host's `ui-spec-studio/backups/` area, and is automatically restored when the managed Skill is uninstalled.

```bash
# Non-interactive, explicit and reversible migration
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz install --agent codex --migrate --no-tui
# Preview without changing files
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz install --agent codex --migrate --dry-run
# Chinese prompt labels
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz install --agent codex --lang zh
```

In non-interactive mode, an existing unmanaged Skill requires `--migrate` or, only if every file is byte-identical, `--adopt`. `--yes` alone never authorizes a replacement. A file-integrity mismatch in a managed Skill remains a hard stop. The wizard uses real file and adapter operations; npm downloads the release tarball **before** the installer starts, so it does not falsely display simulated network-download percentages.

The installer embeds a deterministic SHA-256 manifest of every packaged file, installs only the Skill files (plus a small ownership receipt), refuses unowned or locally edited Skill folders, and stages upgrades before swapping. Native role configuration remains owned and protected by its dedicated Harness adapter. If an adapter fails while installing a new Skill folder, the installer rolls back that Skill folder. Use a new terminal/Agent session where Skill discovery is cached.

The GitHub source repository contains multiple gigabytes of historical evidence. **Do not use `npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec` as the recommended install:** current Skills CLI versions may clone that complete repository into a temporary directory before copying the requested Skill.

## Standard Skills CLI compatibility: portable Skill only

For a host that already manages Skill installation through the [Skills CLI](https://skills.sh/docs/cli), install the independent release ZIP (not the source repository) explicitly:

```bash
npx skills add https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-1.20.3.zip --skill ui-spec -a codex
```

This installs the **portable Skill alone**, not the four Codex native agents. The Codex adapter is separately available as `ui-spec-codex-1.20.2.zip` for manual installation. Do not use both installers against an already managed Skill directory without first examining ownership receipts; neither will silently take over a copy managed by the other.

For a fixed independent-installer version rather than the latest release:

```bash
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz install --agent codex
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
npx --yes https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz install --agent codex
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
