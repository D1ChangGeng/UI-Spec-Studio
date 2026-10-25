# Versioned release procedure

The distribution source is `D1ChangGeng/UI-Spec-Studio`. The standard Skills CLI
installs its skill directory directly from GitHub. The project requires no separate
npm package publication.

## Prepare the version

Update VERSION, SKILL.md metadata, CHANGELOG, fixed-version install examples and
`docs/releases/v<version>.md` together. Review the runtime references and public
wrappers using [the writing standard](WRITING.md). Preserve the source and approved
scope of the change in an ordinary Git commit.

```bash
python tools/validate_package.py
python -m unittest discover -s tests -v
python tools/package.py
```

The build produces a full source ZIP, standalone skill ZIP, per-file content
inventory and SHA-256 checksums in `dist/`. ZIP entries use fixed timestamps,
permissions, order and stored bytes; `.gitattributes` keeps source line endings
consistent across platforms.

## Automated publication

A main-branch push changing VERSION runs validation, installation, publication-render
and the product, asset, content and temporal scenario checks.
The release job has repository-content write permission; ordinary validation jobs
have read-only permissions. External Actions are pinned to reviewed commit SHAs.

After gates pass, the release tool:

1. Checks a clean checkout, repository identity, exact remote commit and tag safety.
2. Validates source, reruns unit tests and builds release assets.
3. Creates a draft release for the exact commit, or inspects an existing release.
4. Downloads every expected asset and compares SHA-256 with the built files.
5. Publishes the verified draft and reads its resulting tag/status/URL.

An existing published release is accepted only when its tag and assets match.
Conflicting tags or assets remain preserved for inspection. Changes to released
source use a new version. A failed operation reports its error and leaves the
actual remote state available to inspect.

The workflow can also be dispatched from main with `publish_release` enabled.
Ordinary commits that leave VERSION unchanged still run validation and installation.
A correction to an unpublished version can complete its release after every gate
passes: a missing version tag activates publication. Existing published tags and
assets retain the release tool's identity and checksum protections.

## Manual publication from an authorized checkout

Use Git and an authenticated GitHub CLI with access to the existing repository.
Credentials stay with GitHub CLI or its configured environment.

```bash
python tools/publish.py
python tools/publish.py --owner D1ChangGeng --name UI-Spec-Studio --execute
```

The default prints the plan. `--execute` performs the release steps above; commit
and push the intended source beforehand. Inspect a partial draft or conflicting
existing release before retrying.

## Verify what users receive

```bash
npx skills add D1ChangGeng/UI-Spec-Studio --list
npx skills add https://github.com/D1ChangGeng/UI-Spec-Studio/tree/v1.7.0 --skill ui-spec
```

Read back the repository commit, tag, Actions result and release assets. Keep
installation success distinct from host-agent invocation and product UI quality.
The content inventory and checksums support byte-level inspection of each release.

## Publication assets

Regenerate original README artwork with `python tools/readme_art.py` and verify
it with `--check`. The local preview is an explicitly identified approximation;
main-push CI also opens the actual GitHub rendering for the source commit. Download
the publication-evidence Actions artifact to inspect the recorded frames. Keep
these browser conditions separate from package and installation claims.

## Resource catalog consistency

Edit `skills/ui-spec/assets/resource-catalog.json` as the maintained source, then
regenerate its readable map with `python tools/catalog_docs.py`. The test suite
checks its exact correspondence and installed lookup. Preserve historical research
dates; append scoped new observations when independently rechecked.

The product-intent job executes the authored scenario through local HTTP, stores
its captures and report, and verifies real browser local storage. Its result is
a required release gate alongside the existing tests and publication checks.

The scenario gate also runs the asset-review fixture. Keep asset evidence scoped
to actual files, viewing conditions and input paths. Public bundles carry only
approved-to-distribute source and outputs; project-specific restricted masters
remain in their authorized destinations.

The content-review fixture additionally exercises both locales, real browser-local
read/write/delete boundaries, draft continuity, accessible state/focus behavior,
failure recovery, content growth and text-spacing adaptation. The gate requires
real persistence. A routed in-memory preview is recorded as limited and remains
ineligible for the real-storage release gate.

The temporal-review fixture captures meaningful interaction episodes and stores
ordered visual evidence with source identity and event/capture timing. The scenario
gate checks its declared state and continuity contracts. Reviewers open the relevant
frames or clips and record visual findings separately. Preserve natural-time and
controlled-time evidence labels; source presence, a completed capture or a successful
assertion does not by itself establish motion quality.
