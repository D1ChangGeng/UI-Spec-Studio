# UI Spec Studio CLI

**Official npm installer for the `ui-spec` Agent Skill.**

The `ui-spec-studio` package is a small, self-contained distribution. It installs only the portable `ui-spec` Skill and optional native Harness integrations. It does **not** download the multi-gigabyte UI Spec Studio GitHub source repository.

## Install

```powershell
npx --yes ui-spec-studio@latest install --agent codex --global
```

An interactive terminal can also start the wizard directly:

```powershell
npx --yes ui-spec-studio@latest
```

The wizard identifies the Harness, project/user scope, existing Skill files, and native adapter; it then shows actual integrity checks, file-copy progress and completion information.

## Existing Skills CLI installations

An earlier `npx skills add` installation may have an unowned directory or a Windows Junction at `~/.agents/skills/ui-spec`. The wizard can adopt a byte-identical copy or back up and replace a different one; an original backup is restored on uninstall.

For non-interactive, explicit backup-and-migrate:

```powershell
npx --yes ui-spec-studio@latest install --agent codex --global --migrate --no-tui
```

No command implicitly overwrites an unowned Skill, including a command run with `--yes`. The installer never modifies a symlink's external target.

## Other commands

```powershell
npx --yes ui-spec-studio@latest --version
npx --yes ui-spec-studio@latest status --agent codex --global
npx --yes ui-spec-studio@latest install --agent codex --global --upgrade
npx --yes ui-spec-studio@latest uninstall --agent codex --global
```

Supported Harnesses: Codex, Claude Code, Cursor, and OpenCode. Codex installs its four native roles through its independently owned adapter. Model choice, permissions and runtime tool access remain the responsibility of the actual Harness.

The installer requires Node.js 20+. Installing the Codex native adapter requires Python 3.11+.

## Source, security and documentation

- [GitHub repository](https://github.com/D1ChangGeng/UI-Spec-Studio)
- [Full installation guide](https://github.com/D1ChangGeng/UI-Spec-Studio/blob/main/docs/INSTALL.md)
- [Official npm publishing and provenance policy](https://github.com/D1ChangGeng/UI-Spec-Studio/blob/main/docs/NPM-DISTRIBUTION.md)
- [Versioned releases](https://github.com/D1ChangGeng/UI-Spec-Studio/releases)

Only use this package name after its official registry publication has been verified. Publication ownership and package provenance are separate from GitHub Release asset availability. The release package includes the applicable MIT license.
