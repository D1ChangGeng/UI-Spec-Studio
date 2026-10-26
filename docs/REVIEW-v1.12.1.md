# UI Spec Studio 1.12.1 review

## Patch scope

This patch completes the Ubuntu browser-job mirror correction discovered during
the 1.12.0 publication readback. Both browser jobs also inspect the runner's
`/etc/apt/apt-mirrors.txt`. The existing precise replacement preserves URI scheme,
suites, components, keyrings, priorities and unrelated repositories. Timeouts,
assertions, permissions, pinned Actions and release dependencies retain their
existing values.

The [1.12.0 review](REVIEW-v1.12.0.md) describes the intent-grounded research and
evidence-driven design changes, independent applications, README work and their
limits. This patch changes only the skill's version metadata. Its behavior,
references, templates, scripts and 29-file distribution structure retain that
reviewed implementation. The earlier applications used the recorded 1.12.0 input;
they are not reported as new applications of a different input.

## Observed failure and correction

The first source's scenario job was cancelled twice during slow Azure Ubuntu
dependency downloads, before scenario assertions ran. A following direct-source
URI correction completed all eight jobs and published 1.12.0 from
`843a2f7cd0a03bea291fa70fa48370f75be16ec9`. Its release tool read back the asset
checksums, and its published-tag installation passed. The
[prior-release observation](evidence/v1.12.1/prior-release-observation.json)
identifies that completed run and its actual evidence boundaries.

Inspection of that successful run nevertheless found `file:/etc/apt/apt-mirrors.txt`
and actual Azure requests in both browser jobs. The command's successful exit
did not establish mirror replacement: it had covered `.list` and `.sources` files
but omitted the runner's indirect mirrorlist. Improved transfer speed in that run
therefore cannot be attributed to the attempted replacement.

The patch adds the observed mirrorlist path to the two existing file loops.
The [recovery record](evidence/v1.12.1/ci-dependency-recovery.json) preserves the
failed attempts, first revision and corrected scope. The
[independent review](evidence/v1.12.1/ci-mirror-review.json) verifies the two-line
workflow change and its boundaries. Local checks execute the actual substitution
against direct source formats, plain and weighted mirrorlist entries and near-miss
URIs. They establish the transformation's scope; the subsequent CI request hosts
establish whether it acts on that runner's real dependency sources.

## Retained evidence and current checks

The original source audit and fresh-context applications retain their frozen
identities under `evidence/v1.12.0/`. The
[patch identity comparison](evidence/v1.12.1/patch-source-identity.json) checks every
runtime file and permits only the `1.12.0` → `1.12.1` metadata substitution in
SKILL.md. The eight common references remain 146,719 bytes under the unchanged
147,456-byte budget, and the entry remains 166 lines.

Current installation examples pin 1.12.1. The bilingual README changes only that
version token; its existing layout, method text and artwork retain the inspected
design. Local and actual-host publication checks cover the updated source. The
[local visual record](evidence/v1.12.1/readme-local-review.json) identifies direct
inspection of the changed installation area. Earlier full-matrix
observations retain their original source and capture conditions.

Structural checks, the complete unit suite, deterministic packaging, installation,
README rendering and four browser scenarios retain separate evidence scopes.
The [engineering record](evidence/v1.12.1/engineering-checks.json) identifies
executed local checks. Captured temporal media are not treated as viewed motion
evidence. The earlier research proposal did not integrate its proposed React
resource or a production model, storage or document-processing backend.

## Publication identity

Version 1.12.0 and its published assets remain intact. This corrected source uses
the new 1.12.1 tag and release notes. The existing workflow must complete all
required jobs before publishing, then download and compare its assets and install
the published tag. The final Actions run, exact tag commit, public release state
and independent downloaded-asset checks identify the actual publication result;
this source review does not predeclare that later result.
