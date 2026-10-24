# Assurance and evidence

## Release assurance model

This release is assessed through source review, logical scenario analysis and
deterministic engineering checks. These establish different facts:

| Evidence | What it supports |
|---|---|
| File-by-file review | Responsibilities, writing quality, causal clarity and useful execution guidance |
| Logical scenarios | Whether the documented rules lead to coherent behavior in representative situations |
| Unit and failure-path tests | The exact optional-helper and release-tool behaviors exercised |
| Package/link checks | Portable structure, version agreement and resolvable local references |
| Repeated builds and inventory hashes | Reproducible distribution bytes and identifiable source content |
| Standard Skills CLI smoke checks | Discovery/installation, installed file identity and helper execution |
| Actual product browser review | Visual quality and task behavior in the observed UI scope |
| Real integration tests | The authority, persistence and outcomes exercised in that environment |

The final two rows belong to consuming product tasks. Host-model understanding
and comparative design quality need their own observations. Large comparative
agent campaigns are optional research, rather than a release prerequisite.

## Run deterministic checks

```bash
python tools/validate_package.py
python -m unittest discover -s tests -v
python tools/package.py
```

The source includes tests for preparation safety, preserving existing files,
coverage requirements, stale/missing evidence, scoped approval and real connection
records, local path boundaries, installed helpers, version handling, content
inventories, reproducible archives and release readback/failure behavior.

The original 1.0.0 bundle's 47 tests were rerun successfully before changes. The
current test count and output are provided by the test command and each CI run.
A fixture named as test evidence is synthetic; its purpose is record validation.

## CI and installation

The workflow runs Python 3.10/3.13 on Linux and Python 3.13 on Windows/macOS. Its
installation job uses Node 24 and Skills CLI 1.7.4 in disposable projects. It tests
the local checkout and, on main pushes, the exact committed GitHub source, for
Codex, Claude Code and OpenCode installer targets. Installed bytes are compared
with the source; copied helper scripts execute from the new project directory.

This checks the installer, not a model session in each host. Read the Actions run
for executed jobs, logs, failures and any skips. Merely including a workflow is
not evidence that its jobs passed. The release job requires the test and install
jobs, then verifies downloaded asset bytes before publishing its draft release.

## Logical scenario review

The [file review](REVIEW.md) includes reasoning paths for users with open or precise
direction, continuation, subjective feedback, shared-shell changes, integration,
static products and unavailable verification capabilities. Scenarios are inspected
for contradictions, excessive process, lost requirements and role overreach.
Their expected behavior is distinct from a measured model outcome.

## Acceptance in a real project

Use the skill's verification reference: declare scope, inspect actual viewports,
complete tasks, review variants and transitions, repair causes and recheck affected
surfaces. At finish, verify both the accepted design and actual business outcomes.
Report approval, connection, verification and release separately.

Project evidence containing private data stays within its authorized location.
Publishing this skill does not publish a consuming project's screenshots or data.

## v1.2 publication and professional content

The professional expansion is reviewed as a connected model: content meaning,
concept, representation, concrete visual grammar, material/medium, timing,
observation and editable realization. Conditional patterns include both useful
applications and circumstances that call for another approach. This is source and
logical review, not a model-quality benchmark.

The publication job generates Chromium captures for the English and Chinese
READMEs at 390×844, 768×1024 and 1440×1000 in light and dark. It checks local
Markdown rendering, then the actual GitHub host on main pushes. Reports identify
the renderer and source commit. The job checks image loading/selection, native
installation text, disclosure behavior and document overflow; visual judgment is
performed separately by looking at the captures.

`tools/readme_art.py --check` verifies deterministic source artwork. Package tests
check its inclusion, inert SVG, image alternatives and source references. Optional
preview dependencies are isolated from the standard-library skill helpers. The
README design record states the observation conditions and evidence limits.

## Resource discovery assurance (1.3)

The local lookup and generated map have deterministic regression coverage for
schema, need/stack/form filters, exact item identity, empty results, provenance,
date preservation, installed execution and archive inclusion. The standard
installer smoke check also runs the installed lookup from its new project.

Release work rechecks selected primary access mechanisms and exercises catalog
queries. Those observations validate retrieval paths and source interpretation,
not every candidate's runtime or visual quality. [The resource review](REVIEW-v1.3.0.md)
connects accepted requirements to code and documentation. The actual CI result
identifies executed jobs; source presence alone does not establish a passing run.
