# Official npm CLI distribution

## Current authoritative status

The canonical npm package is **ui-spec-studio**. The GitHub release v1.20.3 is published; the official npm registry **must be checked independently** before claiming that `npx --yes ui-spec-studio@latest` works. A 2026-11-02 GitHub Actions registry probe returned E404 for `ui-spec-studio`. That observation does **not** create or reserve the npm name. No GitHub connector permission can take ownership of an npm package on behalf of an unrelated npm account.

The versioned GitHub release fallback is independently executable, but the mutable `releases/latest/download/ui-spec-installer.tgz` URL can resolve to stale npm cache content. Do not make the mutable GitHub URL the primary `npx` package specifier again.

### Recovery while npm registration remains pending

From the user's Windows PowerShell, for an existing old Codex Skill in the home directory:

```powershell
npx --yes "https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.3/ui-spec-installer.tgz" install --agent codex --global --migrate --lang zh
```

This downloads only the small, verified installer tarball—not the 2 GB repository—and backs up the previous Skill before migration. `--global` selects `~/.agents/skills/ui-spec`. The previous copy is restored on unified-installer uninstall. Literal Markdown hyperlink syntax must not be pasted into PowerShell.

## One-time npm owner bootstrap

npm requires the first publish to be performed by an **authorized npm account**. Configuring GitHub OIDC trusted publishing requires the npm package to exist first. Run the first publish locally with npm login/2FA, then configure a trusted publisher. Never post or share npm credentials or 2FA codes in the repository, a chat, or CI logs.

A first-publication bootstrap script is available in [tools/bootstrap-npm.ps1](../tools/bootstrap-npm.ps1). It performs release-asset download, SHA-256 check, npm package metadata verification, an explicit check for an already-registered package, account login when necessary, a human confirmation prompt, `npm publish`, and registry integrity readback. Its `-DryRun` mode performs **no registry write and no account login**. It does not clone the GitHub repository.

Download the short script *as a maintainer*, inspect it, and run it in your own PowerShell session:

```powershell
$script = Join-Path $env:TEMP "ui-spec-npm-bootstrap.ps1"
Invoke-WebRequest "https://raw.githubusercontent.com/D1ChangGeng/UI-Spec-Studio/main/tools/bootstrap-npm.ps1" -OutFile $script
Get-Content $script
& $script -DryRun
& $script
```

The script is intentionally not `irm | iex`: publication requires the owner to review what runs. It publishes the **already released v1.20.3 archive**, with an explicit confirmation. If PowerShell's execution policy blocks a downloaded script, review your environment's policy before running it; do not weaken it system-wide. If the npm name is occupied, **stop**: do not install or publish a package with unexpected ownership.

Equivalent manual path after verifying the release checksum and npm package identity:

```powershell
npm login --registry https://registry.npmjs.org/
npm publish .\ui-spec-installer.tgz --access public
npm view ui-spec-studio@1.20.3 name version dist.integrity repository --json --prefer-online
```

The manual command expects the locally downloaded **v1.20.3** installer tarball. Publishing from a full repository folder, a different archive, or a cached `latest` tarball is not equivalent.

### One-time trusted publisher connection

Once `ui-spec-studio@1.20.3` is actually registered and its `dist.integrity` matches the verified release tarball:

1. On npmjs.com, open `ui-spec-studio → Settings → Trusted publishing` and add **GitHub Actions**.
2. GitHub user/organization: **D1ChangGeng**; repository: **UI-Spec-Studio**; workflow filename: **npm-publish.yml**; environment: blank unless subsequently configured.
3. Choose **Allow direct npm publish**; staged-only authorization cannot run this repository's current direct-release job. Complete the first trusted publish within the npm configuration's activation window.
4. Confirm the package's repository metadata points to `https://github.com/D1ChangGeng/UI-Spec-Studio`.
5. No long-lived `NPM_TOKEN` is needed; `.github/workflows/npm-publish.yml` uses GitHub's `id-token: write` OIDC permission in its publish job.

Only after this connection is active should the package owner consider npm's "require 2FA and disallow tokens" publishing restriction. Restricting tokens must not break the necessary one-time bootstrap.

## Verified-release automation after bootstrap

`.github/workflows/npm-publish.yml` has two paths:

- **Candidate:** on installer-related pull requests and explicit workflow dispatch, it verifies package identity, portable files, the deterministic build, a real local `npx` invocation, the installer tests, registry status, and the PowerShell first-publish dry run. It uploads the small `official-npm-installer-candidate` artifact.
- **Production:** on a successful **Validate and release** workflow run for a main-branch push, it checks the exact validated head SHA, requires the same published version tag and a public GitHub Release, checks the npm package identity, and then uses OIDC to publish the deterministic tarball. Already published byte-identical versions are accepted without republishing. Unexpected version identity or archive conflicts are rejected.

Until the npm name has been bootstrapped, the automated production path **skips registry writes** and records `NPM_BOOTSTRAP_REQUIRED`. A manually dispatched publish remains available as an authorized recovery path; it enforces the same exact tag, public release, package identity, and archive checksum safety.

Automatic npm publication should never be treated as an excuse to bypass `Validate and release` or publish from an unrelated branch. For a subsequent release, update `VERSION` through the usual guarded release process; the successful main-branch release then triggers npm promotion. OIDC must already be trusted and permitted to publish directly.

## Official user installation after npm registry readback

```powershell
# Stable, version-independent, interactive installation:
npx --yes ui-spec-studio@latest

# Explicit global Codex installation / reversible legacy migration:
npx --yes ui-spec-studio@latest install --agent codex --global --migrate --lang zh

# Inspect actual installed version and target:
npx --yes ui-spec-studio@latest --version
npx --yes ui-spec-studio@latest status --agent codex --global
```

`@latest` is npm's distribution tag, not a mutable GitHub asset URL; it provides standard version resolution. It still resolves through npm's ordinary registry/cache rules, so verifying a new release means comparing `npm view ui-spec-studio version dist-tags --json --prefer-online` with the actual CLI version. `npx --yes` suppresses npm's download prompt only: it **does not** authorize destructive Skill migration. Unmanaged copies still require an interactive choice or explicit `--migrate`.

### Final acceptance before promoting README to the official npm name

Do not replace the pinned GitHub Release in README until all of these are observed:

1. Public npm registry reports the expected `ui-spec-studio@VERSION` and `dist-tags.latest`, and the published `repository` identity is correct.
2. The public npm tarball integrity matches the reviewed GitHub candidate (or any explicitly reviewed alternative with provenance).
3. On a clean project, `npx --yes ui-spec-studio@latest` installs the complete 37-file Skill and correct native Harness adapters.
4. On Windows, the **npm-named** command safely migrates an older unowned Codex Skill with original backup and uninstall restoration.
5. Cross-platform installer and actual terminal UX CI passes; the install path never clones the full repository.
6. Both READMEs and `docs/INSTALL.md` use the same canonical npm entry point.

A green GitHub Release, a successful `npm pack --dry-run`, or an unregistered package name is not proof of npm ownership or an official npm installation.
