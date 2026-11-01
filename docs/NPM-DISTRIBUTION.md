# Official npm CLI distribution

## Status and boundary

The canonical npm package name reserved for UI Spec Studio's installer design is **`ui-spec-studio`**. A GitHub Actions registry probe reported that name was unregistered on 2026-11-02. **Unregistered is not owned or published**. The named command must not be presented as a working installation method until the package is claimed by its authorized npm account and the registry is independently read back.

This distribution keeps the 37-file portable `ui-spec` Skill and the Codex adapter in the same deterministic, small, prebuilt npm tarball that GitHub Releases publishes. It never clones the multi-GB source repository.

### Official user experience after successful npm publication

```powershell
# Stable, version-resolving, ordinary install (interactive on a TTY)
npx --yes ui-spec-studio@latest install --agent codex --global

# Simplest interactive entry; pick a Harness and scope from the terminal menu
npx --yes ui-spec-studio@latest

# Explicit, unattended migration of an existing unowned Skill with a backup
npx --yes ui-spec-studio@latest install --agent codex --global --migrate --no-tui

# Confirm the package actually executed and report the installed state
npx --yes ui-spec-studio@latest --version
npx --yes ui-spec-studio@latest status --agent codex --global
```

`@latest` is an npm distribution tag rather than a GitHub mutable asset URL. It allows users to omit fixed semver while keeping normal npm registry resolution. Running `npx --yes ...` only suppresses npm's download confirmation. It **does not** authorize overwriting a previously unowned Skill; interactive migration consent or explicit `--migrate` is still required.

The installer includes optional, pinned `@clack/prompts` terminal components. The actual source code, Codex role files and Clack UI dependency must be distributed separately from the repository's historical experiments. In non-TTY, CI and offline mode, a deterministic machine-readable fallback is retained.

### Current recovery until npm publication is verified

```powershell
npx --yes "https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.2/ui-spec-installer.tgz" install --agent codex --global --migrate
```

Use the above **already published tag** for emergency recovery until v1.20.3 and the npm package have been formally published. Avoid reusing the GitHub `releases/latest/download/ui-spec-installer.tgz` URL as a npm package specifier: npm may reuse its earlier cached tarball for this unchanged URL. A previous error message reading `Existing unowned Skill directory; refusing to overwrite` originated in v1.20.1, not the current migration-aware installer. Never paste literal Markdown hyperlink notation `[url](url)` into PowerShell.

## One-time npm package bootstrap: account holder action

npm does not allow establishing an OIDC trusted publisher until the npm package exists. Therefore **the initial registration is an interactive npm-account action**; GitHub repository write access does not grant npm registry ownership.

1. Use the `official-npm-installer-candidate` artifact from the green `.github/workflows/npm-publish.yml` workflow for the exact commit and VERSION being released. It contains only `ui-spec-installer.tgz`, not the full repository.
2. Download that small artifact through GitHub Actions and extract the zip to get `ui-spec-installer.tgz`. Alternatively, after the first `v1.20.3` GitHub release exists, download that release's `ui-spec-installer.tgz` directly.
3. With your own authorized npm account and 2FA enabled, run in PowerShell:

```powershell
npm login --registry https://registry.npmjs.org
npm publish .\ui-spec-installer.tgz --access public
npm view ui-spec-studio version dist-tags --json --prefer-online
```

4. Confirm the result is actually `ui-spec-studio@1.20.3` and the installer's README/metadata identifies `D1ChangGeng/UI-Spec-Studio`. Inspect the package files before publishing; npm package names are first-come, first-served and the account must have the right to claim that name.
5. On npmjs.com, open the package's **Settings → Trusted publishing** and configure the GitHub Actions publisher with:

   - GitHub user or organization: `D1ChangGeng`
   - Repository: `UI-Spec-Studio`
   - Workflow filename: `npm-publish.yml`
   - Environment name: none, unless the workflow is changed to use one
   - Allowed action: **Direct npm publish**

   Trusted publisher setup should be performed shortly before the next publish to comply with npm's activation window.
6. For subsequent versions, after the source and GitHub release are verified, explicitly trigger `Official npm CLI candidate and trusted publication` through GitHub Actions → `Run workflow` on `main` with `publish = true`. The workflow has `id-token: write`, checks the tag/commit identity, builds the same deterministic artifact, verifies existing registry versions before writing, and uses npm's OIDC authentication. No long-lived `NPM_TOKEN` should be stored in the repository.

If a registry name is already owned by another user when bootstrap is attempted, **stop**. Do not publish someone else's package or silently substitute a misleading name; review and change the canonical name before offering users a new command.

## Release acceptance

Before changing the primary README installation command to npm, require:

- npm `ui-spec-studio@VERSION` package genuinely present on the public registry;
- registry-reported tarball integrity matching the candidate GitHub archive (or separately reviewed provenance);
- `npx --yes ui-spec-studio@latest --version` reporting the expected package;
- a new real project installation and Windows legacy Skill migration via the npm-named command;
- a complete cross-platform installer test gate, and no full-repo clone from the user's installation path.

Do not equate a successful `npm pack --dry-run` or GitHub Release upload with an actual npm publish. Maintain one canonical npm package, one registry distribution channel, a separately owned Codex adapter, and a portable Skill.
