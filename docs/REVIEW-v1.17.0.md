# v1.17.0 review: adaptive formal increments

## Design outcome

The runtime now organizes its existing professional methods around coherent,
quality-assessable design increments. It retains the complete goal and the same
evolving product, with candidate planning, formal work and internal execution
kept distinguishable. The ordinary operations remain init, optional shape,
iterate, audit and finish.

| User requirement | Responsible installed guidance and implementation |
|---|---|
| Formal definition and four work objects | SKILL.md; workflow init/iterate |
| Minimum sufficient experience closure | analysis.md: scope, six factors and four decisions |
| Visible surface versus actual quality-bearing relationships | analysis.md; evidence-map.md |
| Revisable init plan and meaningful first result | workflow.md; analysis.md |
| New SPEC versus internal research, repair and refinement | SKILL.md; workflow.md; verification.md |
| Equal formal standing and continuous product inheritance | workflow.md; evidence-map.md |
| Research, implementation and regression as different scopes | analysis.md; component-sourcing.md; verification.md |
| Actual quality ownership and adoption chain | component-sourcing.md; verification.md; decision template |
| High-quality first slice and truthful unfinished functionality | analysis.md; workflow.md |
| Research/resource/implementation feedback can change scope | analysis.md; component-sourcing.md; workflow.md |
| Useful conversation delivery from the same three views | SKILL.md; workflow.md; evidence-map.md; review template |
| Product task content versus internal design documentation | SKILL.md; workflow.md; verification.md |
| Local-quality and related-product verification | verification.md; review template |
| Neutral optional declaration support | evidence-records.md; check_design_evidence.py |
| No extra lifecycle, quotas or mechanical quality gates | All responsible runtime rules and inspector behavior tests |

## Continuity and compatibility

Development starts from main commit
`9cc2470e21b626c56dd293274277d9809c13defb`, retaining the post-release empirical
addenda as well as the published v1.16.1 runtime. The new continuity ledger
restores every prior runtime byte before the existing v1.16.1 and v1.16 historical
checks run. No prior ledger, tag or evidence is reclassified as a new result.
The semantic change record explains definition refinements separately from
byte-level restoration.

The optional `ui-spec-evidence/1` profile accepts `product_context`,
`candidate_specs` and `formal_specs`. A SPEC can declare links to multiple
objects and decisions, and several SPECs can reference the same object. Research,
implementation and regression references remain separate declarations.
Older records require no migration. Candidate and formal records are shown
separately in all three views; no statuses or state transitions are added.
Duplicate or unresolved references are structural findings and still produce
exit 0 for a readable record. Source declarations are not authenticated facts.

The full source archive now includes CSV/JSONL study records, module scripts,
text logs, licensed WOFF2 replay fonts, WebM recordings, JPEG contact sheets and exact capture bundles specifically under
`docs/evidence` and `docs/experiments`. The portable Skill keeps its existing
37-file footprint; study applications and fonts are not installed as Skill assets.
This prevents a recorded experiment from losing its runtime font or raw data
when users download the source release.

The first final suite exposed an old full-source "no fonts" assertion. Its
distribution contract is now explicitly scoped: only the two licensed Inter WOFF2
files in the archived study apps are allowed, with their SIL license text checked;
the Skill, publication assets and shared examples remain font-free. The original
failure is retained in [the original log](evidence/v1.17.0/logs/unit-final.txt). JPEG contact sheets are also retained
under the evidence-only archive policy. These packaging changes do not change the
frozen participant runtime.

Raw study archives, shared input copies and review records disable Git text
conversion in `.gitattributes`, so a platform checkout does not normalize an
original log or source byte sequence. Snapshot restoration and release-inclusion
checks verify the stored bytes independently of professional quality judgments.

The raw archive paths also retain original whitespace without Git whitespace
linting. The [original scan](evidence/v1.17.0/logs/raw-whitespace-scan.txt) identifies
trailing spaces and final blank lines in fetched HTML and actual test logs. Those
bytes are evidence, so they are preserved; authored runtime, tooling and release
documentation retain normal whitespace checking.

## Verification evidence

The release's exact evidence is recorded under `docs/evidence/v1.17.0/`.
Mechanical test results, browser fixture observations, real Agent applications,
independent Agent visual judgments and owner acceptance remain separate claims.
See the [application study](experiments/adaptive-granularity/RESULTS.md) for executed
cells, original failures, actual changes and the limitations on interpretation.

All nine fresh participant runs completed both task stages; three fresh reviewers
then inspected anonymous product packets. The review reports were frozen before
condition synthesis, and all 84 supplied application-file references still match
their participant snapshots. Results are mixed: C retained save-error priority
and near-bottom manual scrolling in the tested cases, but still lacked narrow
source transport and lost focused Save on a card write failure. The source does
not claim a universal winner, human acceptance or measured motion smoothness.
The [gallery](experiments/adaptive-granularity/GALLERY.md) contains 18 byte-identical
review frames. The [final independent audit](evidence/v1.17.0/final-audit.md)
records source, archive, compatibility and claim checks; the
[final source gates](evidence/v1.17.0/final-source-gates.json) record local validation.
Remote CI, tag, release-asset and published-install results are separately available
in the release's GitHub Actions run after publication.

The runtime does not acquire additional host permissions. The existing GitHub
workflow controls publication only after its ordinary cross-platform, installation,
README and browser scenario gates. Publishing the reviewed source is separate
from claiming generalized design-effectiveness improvement.
