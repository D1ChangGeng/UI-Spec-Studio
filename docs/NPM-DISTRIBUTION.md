# Official npm CLI distribution

## Current authoritative status

**Current verified official release: `ui-spec-studio@1.20.5`.** The package was published directly from the verified GitHub Actions OIDC Trusted Publisher on 2026-11-02, with signed build provenance and public SHA-512 parity against the immutable GitHub Release asset. The same [npm workflow](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/runs/41429988499) passed its second attempt after the initial post-publish CLI read returned stale npm `latest` metadata. The initial manual-bootstrap release `1.20.3` remains independently verified. On 2026-11-02, GitHub Actions [npm candidate verification](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/runs/41397846037) independently confirmed the public registry package identity, byte-for-byte SHA-512 parity with the **v1.20.3 GitHub Release** installer, successful `npx --yes ui-spec-studio@latest` installation, all 37 Skill files, four Codex roles, and reversible migration/restoration of an unmanaged copy.

The initial npm first-publish command succeeded but its immediate `npm view` returned a transient 404 while the registry processed the new package. A subsequent public readback and actual `npx` execution succeeded. **Do not republish the same package version.** `tools/bootstrap-npm.ps1` now detects an already-published byte-identical version and accepts it without a registry write. After a new first publish, it retries registry verification and distinguishes accepted publication from eventual public readback.

The permanent, version-independent user command is:

```powershell
npx --yes ui-spec-studio@latest
```

A fixed GitHub Release URL remains an immutable fallback. Do not use `releases/latest/download/ui-spec-installer.tgz` as an npm package specifier: npm may reuse stale cached bytes for its unchanged URL.

```powershell
npx --yes "https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/v1.20.6/ui-spec-installer.tgz" install --agent codex --global --migrate
```

### Legacy Windows installation migration

From the user's Windows PowerShell, for an existing old Codex Skill in the home directory:

```powershell
npx --yes ui-spec-studio@latest install --agent codex --global --migrate --lang zh
```

This downloads only the small, verified installer tarball—not the 2 GB repository—and backs up the previous Skill before migration. `--global` selects `~/.agents/skills/ui-spec`. The previous copy is restored on unified-installer uninstall. Literal Markdown hyperlink syntax must not be pasted into PowerShell.

## One-time npm owner bootstrap (completed)

The npm account owner has successfully published `ui-spec-studio@1.20.3`. The first publication required interactive npm authentication; it has **already succeeded**. No second `npm publish` is necessary or appropriate. Never post or share npm credentials, cookies or 2FA codes in the repository, a chat, or CI logs.

The [bootstrap/verification script](../tools/bootstrap-npm.ps1) checks the pinned GitHub release archive against both SHA-256 and the public npm SHA-512, verifies package identity, and safely recognizes a previously published version. `-DryRun` never logs in or publishes. After a successful first publish, a transient registry 404 is treated as **verification pending**, not as a failed publication. It does not clone the GitHub repository.

For a read-only verification of the already-published version, you may inspect and run the script's dry run:

```powershell
$script = Join-Path $env:TEMP "ui-spec-npm-bootstrap.ps1"
Invoke-WebRequest "https://raw.githubusercontent.com/D1ChangGeng/UI-Spec-Studio/main/tools/bootstrap-npm.ps1" -OutFile $script
Get-Content $script
& $script -DryRun
```

The script is intentionally not `irm | iex`: inspect the downloaded file before running it. It can verify an already published matching version idempotently; it will refuse an unexpected npm owner, archive or repository identity. The first `npm publish` action is complete.

### Trusted publisher connection — successfully validated

Now that `ui-spec-studio@1.20.3` is publicly registered and its `dist.integrity` matches the verified release tarball, **the package owner has configured npm Trusted publishing (OIDC) and the first GitHub Actions OIDC publish succeeded for `1.20.5`**. The setup previously showed `Pending validation` with a November 4 deadline, but the signed new-version publication was accepted before that deadline. The following setup remains applicable if a publisher needs to be recreated:

1. On npmjs.com, open `ui-spec-studio → Settings → Trusted publishing` and add **GitHub Actions**.
2. GitHub user/organization: **D1ChangGeng**; repository: **UI-Spec-Studio**; workflow filename: **npm-publish.yml**; environment: blank unless subsequently configured.
3. Choose **Allow direct npm publish**; staged-only authorization cannot run this repository's current direct-release job. Complete the first trusted publish within the npm configuration's activation window.
4. Confirm the package's repository metadata points to `https://github.com/D1ChangGeng/UI-Spec-Studio`.
5. No long-lived `NPM_TOKEN` is needed; `.github/workflows/npm-publish.yml` uses GitHub's `id-token: write` OIDC permission in its publish job.

The OIDC publication has now succeeded; the package owner can separately review npm's more restrictive 2FA/token publishing access options without altering the now-tested GitHub Actions OIDC workflow.

## The v1.20.4 GitHub Release and OIDC preflight repair

The immutable v1.20.4 GitHub Release was successfully created and validated, but the npm publish job stopped **before** executing `npm publish`: a malformed npm CLI preflight interpreted a nonempty lookup result as a conflicting remote archive. This was not a confirmed OIDC authentication failure and is not grounds to republish or move the v1.20.4 Git tag. The v1.20.5 release replaces that unreliable query with exact public HTTP version metadata and blocks on unknown states. The publish job also avoids setup-node's placeholder `_authToken` configuration, which can prevent OIDC authentication. This acceptance was subsequently fulfilled by actual OIDC publication of `1.20.5` and a successful verified second workflow attempt.

## Verified-release automation after bootstrap

`.github/workflows/npm-publish.yml` has two paths:

- **Candidate:** on installer-related pull requests and explicit workflow dispatch, it verifies package identity, portable files, the deterministic build, a real local `npx` invocation, the installer tests, registry status, and the PowerShell first-publish dry run. It uploads the small `official-npm-installer-candidate` artifact.
- **Production:** on a successful **Validate and release** workflow run for a main-branch push, it checks the exact validated head SHA, requires the same published version tag and a public GitHub Release, checks the npm package identity, and then uses OIDC to publish the deterministic tarball. Already published byte-identical versions are accepted without republishing. Unexpected version identity or archive conflicts are rejected.

After an OIDC `npm publish` completes, the workflow performs a **read-only, bounded public-registry readback** with fresh HTTPS requests. It requires both the exact published version SHA-512 to match the deterministic installer and the public `latest` dist-tag to point to that version before continuing to real `npx` migration smoke tests. Transient 404/replication delays are retried. If the retries are exhausted, CI reports `PUBLIC_READBACK_PENDING` rather than claiming the registry rejected the already-accepted publish; **do not republish that version**. Conflicting identity or SHA-512 remains a hard failure. The readback does not authenticate or mutate npm.

The post-publish public `npx` smoke can temporarily observe an older npm CLI `@latest` response even after the exact-version registry metadata and dist-tags have converged. The smoke performs **bounded retries** with a **fresh isolated npm cache per attempt** for both the `npm view` read and actual `npx --version` resolution. Only the expected package, repository, SHA-512 and resolved CLI version permit the subsequent installation, migration and uninstall checks. If propagation does not converge, CI reports an explicit pending state and requires investigation rather than a second `npm publish`.

The npm name is already bootstrapped. For a new GitHub version, the automated production path still requires a correctly configured npm OIDC Trusted publisher. An existing version with exactly matching bytes is a no-op. A manually dispatched publish remains available as an authorized recovery path; it enforces the same exact tag, public release, package identity, and archive checksum safety.

Automatic npm publication should never be treated as an excuse to bypass `Validate and release` or publish from an unrelated branch. For a subsequent release, update `VERSION` through the usual guarded release process; the successful main-branch release then triggers npm promotion. OIDC must already be trusted and permitted to publish directly.

## Official user installation (published and verified)

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

### Release acceptance and outstanding authorization

The official public installer is now the primary entry point in both READMEs. The release's acceptance conditions are:

1. Public npm registry reports the expected `ui-spec-studio@VERSION` and `dist-tags.latest`, and the published `repository` identity is correct.
2. The public npm tarball integrity matches the reviewed GitHub candidate (or any explicitly reviewed alternative with provenance).
3. On a clean project, `npx --yes ui-spec-studio@latest` installs the complete 37-file Skill and correct native Harness adapters.
4. On Windows, the **npm-named** command safely migrates an older unowned Codex Skill with original backup and uninstall restoration.
5. Cross-platform installer and actual terminal UX CI passes; the install path never clones the full repository.
6. Both READMEs and `docs/INSTALL.md` use the same canonical npm entry point.

**First OIDC publication acceptance completed:** `1.20.5` was published by the trusted GitHub Actions workflow with signed provenance; the independent public `npx` smoke returned PASS for 37 Skill files, native roles, reversible migration and restore. Retain the actual [publication logs](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/runs/41429988499) and [GitHub Release](https://github.com/D1ChangGeng/UI-Spec-Studio/releases/tag/v1.20.5) as evidence. A mere `npm pack --dry-run` or green skipped publish job is never sufficient.
