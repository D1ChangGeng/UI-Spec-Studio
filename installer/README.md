# UI Spec Studio

Use the UI Spec Studio Skill with **Codex, Claude Code, Cursor or OpenCode**.

## Install

```powershell
npx --yes ui-spec-studio@latest
```

Choose your tool and whether to install for the current project or all projects under your user account.

To install directly for Codex:

```powershell
npx --yes ui-spec-studio@latest install --agent codex --global --lang zh
```

## Already have UI Spec Studio?

The installer lets you keep the current version or back it up and update. When you choose backup and update, uninstalling restores the previous installation.

For a terminal without interactive prompts, explicitly allow the backup:

```powershell
npx --yes ui-spec-studio@latest install --agent codex --global --migrate --no-tui
```

Existing files are never replaced without your choice or an explicit migration option.

## Check, update or uninstall

```powershell
npx --yes ui-spec-studio@latest status --agent codex --global
npx --yes ui-spec-studio@latest install --agent codex --global --upgrade
npx --yes ui-spec-studio@latest uninstall --agent codex --global
```

**Requirements:** Node.js 20 or newer. Codex role setup also requires Python 3.11 or newer.

For more help, run `npx --yes ui-spec-studio@latest --help --lang zh`.

[Installation guide](https://github.com/D1ChangGeng/UI-Spec-Studio/blob/main/docs/INSTALL.md) · [简体中文说明](https://github.com/D1ChangGeng/UI-Spec-Studio/blob/main/README.zh-CN.md)
