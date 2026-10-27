# UI Spec Studio 1.15.0 — structural observation and revisable design knowledge

## Delivered responsibility boundary

The map records current understanding. Structural inspectors report representations.
The Agent judges task applicability, evidence sufficiency and actual next work.
Independent visual, interactive, functional, performance and engineering checks
support results only within their exercised scope. **A structural report never
certifies professional correctness, readiness or completion.**

This is an explicit correction of some mechanical policy in v1.14.0, not a removal
of evidence-driven professional guidance. The exact baseline commit is
`fec7cde99be02c134481733e9f9bd3064ffa871a`. Its distributed source archive hash is
`b4565471660ff2546689ed16718023548493e8f07df59a4148c93572296c50fe`.

## Requirement-to-implementation and proof scope

| Requirement | Delivered implementation | Relevant proof |
|---|---|---|
| Four separate responsibilities | Entry, evidence map/action/profile and user guide | Source review, not proof of model behavior |
| Remove professional mechanical adjudication | Replaced evidence helper predicates with field, ID and reference observations | Single-candidate, acquired/observed, domain/role, version and action permutation tests |
| Separate theoretical and declared absence | Versioned 16-category vocabulary, explicit tag matching, separate unlisted declared targets | Fixtures show absent tags remain applicability-unassessed hints |
| Neutral outputs | `record_readability`, findings, declarations and relation candidates; no aggregate approval flag | CLI and report-contract tests |
| Manifest results and exceptions separate | Non-waived checks, waived checks and exception declarations in different collections | Waiver/missing/planned/failed fixtures and target matching |
| Query mode not project stage | overview/checks/connections; old draft/review/finish aliases only select presentation | Empty inventory, blocked checks and absent approval never trigger completion gates |
| Preserve independently scoped engineering assertions | Separate file-digest comparator; existing browser/package/asset/content/temporal gates unchanged | Byte match/mismatch and release gate source checks |
| Scoped history and applicability | Revision declarations kept, no global freshness veto; relation traversal lists candidates only | Backend snapshot change and dependency-cycle tests |
| Three maintained record layers | Current root records, meaningful revisions and linked raw archive; historical object references supported | Archive not loaded as current decisions; returned views cannot mutate source |
| Both design lines remain revisable | Experience/research/judgment and source/trial/implementation/verification described together | Installed method and decision-template review |
| Unconfirmed initialization | Empty environment/scope collections; detected DESIGN.md explicitly uninspected | Preparation and path safety tests |
| Neutral resource lookup | No-match query observation, catalog notes identified as source material | CLI no generated next_action test |
| Meaningful preservation | Every previous runtime file tracked; old professional content retained or explicitly reallocated | [Continuity ledger](evidence/v1.15.0/continuity.json) and historical restoration guards |

## What changed in the code

In v1.14.0 `check_design_evidence.py` enforced two named alternatives, observed
matching-domain/role/current-global-revision evidence, and expand/finish restrictions
for high-impact gaps. Those are professional questions, not structural facts. The
new helper exposes the declared values and links without judging their adequacy.
Missing optional explanatory fields are observations, not commands to populate them.
An empty but readable planning record has no research conclusion.

The manifest previously combined some waived checks into `satisfied` and used
review/finish to enforce recorded approval, integration and completion. These gates
are removed. Explicit targets, matching records, exceptions and inventory-derived
combinations are distinct. Multiple check IDs can preserve scoped revision history.
Both tools exit 0 when inspection ran, including reports with findings, and exit 2
when input cannot be read. Consumers must migrate away from `ok` or satisfied counts.
The [migration guide](STRUCTURAL-INSPECTION.md) documents the intentional output change.

Byte identity is checked only by the independent `check_file_integrity.py`, which
can return match/mismatch for the named file. Local path and symlink safety remain
shared mechanics. Neither helper reads the referenced media's content, fetches a
URL, chooses actions, schedules work or writes/approves records. Invalid JSON,
duplicate JSON keys and non-JSON numeric constants are read problems; malformed
record fields remain readable data with accurately located observations.

## Preservation and deliberate replacement

No byte or line cap was added. The six design scales, transverse relations,
coverage challenge, mature-resource chain, seven decision relations, non-linear
facts, visual/temporal practice and evidence-guided Agent responsibilities remain.
The previous eleven restored professional sections are still regression-checked.

Boundary-related text is edited where its old description would contradict the
new helper, rather than retained as a second active instruction. In particular,
`evidence-records.md` now explains the neutral record/report contract and delegates
evidence and action interpretation to the Agent. `evidence-actions.md` retains
its action principles and explains that they are not executable predicates.
Current model/revision/archive guidance is added without deleting unrelated design
knowledge. The [continuity ledger](evidence/v1.15.0/continuity.json) identifies every
runtime disposition and relevant source/destination obligations.

The original v1.14 preservation check is now evaluated against a frozen, digest-checked
copy of its actual 34-file runtime. This permits legitimate boundary corrections
without falsifying or weakening the earlier historical record. That snapshot is
maintenance evidence, outside the installed skill; it is not active instructions.
The existing v1.13 three-arm experiment inputs remain exact and pending, not relabelled
as new model runs. Existing historical evidence files remain unchanged.

## Actual testing and limitations

Executed commands and results are recorded separately in
[engineering-checks.json](evidence/v1.15.0/engineering-checks.json). The first complete
system-Python run exercised 224 tests; 221 passed and three package assertions
reported the new review/continuity documents had not yet been written. Earlier
virtual-environment runs hit process-start timeouts; those attempts are not reported
as passes. The available standard-library system Python 3.13.5 ran the boundary
suite without changing test timeouts or relaxing assertions.

Final structure, link, catalog, artwork, tests, reproducible package and installed
helper checks retain their exact executed outcomes. Existing browser fixtures
remain independent assertion tests. Publication verification still requires the
unchanged four-platform test matrix, install, rendered README, browser scenarios,
release-asset readback and published-tag install. This source report does not
predeclare remote CI or publication success.

**Independent Agent comparisons and blind final-UI quality trials were not executed
by this maintenance test suite.** Synthetic structural fixtures are not Agent runs.
A maintainer's scoped README application, where performed and actually inspected,
is identified separately; it cannot establish cross-model effectiveness or a
measured improvement in user-facing application quality. The tool boundary can be
verified without claiming that still-open empirical result.

## Final local checks and bounded self-application

The first locally frozen candidate ran **229 tests with all assertions passing** on Python
3.13.5. Package/link, resource-catalog and README-artwork checks completed. A real
copy installation contained **37 byte-matching runtime files** and exercised the
installed preparation, manifest, evidence, resource-lookup and independent digest
tools. This is installation/helper evidence, not host-model invocation.

The final local README matrix ran English/Chinese, light/dark, and 390/768/1440px.
All twelve changed-section crops were actually viewed. An observed narrow-screen
paragraph grouping issue was corrected by separating the inspector/history paragraph
from the Agent/view explanation; the original native design remained. See the
[decision](evidence/v1.15.0/readme-decision.md) and
[viewed evidence record](evidence/v1.15.0/readme-local-review.json). This scoped
maintainer self-application does not replace an independent Agent comparison.

## Remote Windows source-read correction

The first main-branch candidate, `e9e90de9fe8e52b5cf719d83f0383b553909e49d`,
passed the Linux and macOS unit jobs but the Windows job reported two Unicode
read errors in the new continuity test. The test read UTF-8 reference text
using the Windows cp1252 default; inspector boundary cases themselves ran
successfully. The failed job is preserved as an actual result, not a transient
success or an accepted waiver.

The correction explicitly uses UTF-8 for every text read in
`tests/test_boundary_release.py` and adds a regression assertion for that test
and the relevant installed script readers. No runtime instruction, inspector,
permission, workflow gate or existing assertion was weakened. The corrected
local suite ran **230 tests, all passing**. A new complete remote workflow is
required for publication; the [correction record](evidence/v1.15.0/windows-source-read-fix.json)
identifies the failure, exact changes and executed local check. Earlier local
logs remain evidence for the earlier candidate and are not rewritten.
