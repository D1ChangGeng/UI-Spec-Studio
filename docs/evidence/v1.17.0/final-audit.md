# v1.17.0 final release audit

Audit scope: the completed working-tree implementation, preserved study outputs,
frozen independent reviews, and the final mixed-findings synthesis. This is a
read-only implementation/evidence audit; the only written artifact is this report.
The review did not alter runtime guidance, tests, applications, captured media,
reviewer outputs, Git refs or publication state.

**Finding: no new implementation blocker was found within the inspected scope.**
The release still needs the maintainer's final source gates and the existing
remote CI/publication/readback sequence. Those are pending release steps, not
failures of the inspected method or a claim that publication has already occurred.

## Identity and observed checks

The local parent commit is `9cc2470e21b626c56dd293274277d9809c13defb`.
The candidate declares version `1.17.0`. The audit independently executed the
following bounded checks against the working files; no broad browser suite was
repeated.

| Check performed by this audit | Observed result |
|---|---|
| Current installed runtime versus registered condition C | All 37 files and their SHA-256 identities match exactly. |
| New inverse continuity layer versus actual baseline Git blobs | All 37 recovered v1.16.1 runtime files match the baseline byte-for-byte. |
| Historical evidence preservation | All 198 files listed by the new continuity ledger retain their declared SHA-256 identities. |
| Participant and reviewer archive payloads | 2,210 unique payloads verified across nine two-stage participant archives and three final review archives; every indexed payload is included by the full-source packaging policy. |
| Capture bundles | Every declared bundle SHA-256 matched its actual bytes. |
| Review freeze/unblinding | Each of the three original report and structured-review hashes matches its unblinding record. |
| Reviewed product source versus participant archives | All 84 reviewer input file references across initial/final states match the corresponding archived application identities. |
| Selected gallery provenance | All 18 images match the SHA-256 of their exact frozen review source, without image processing. Desktop images are 1440×900; narrow images are 390×844. |
| Bundled fonts | Exactly the two declared Inter WOFF2 files occur in archived study applications; each has its SIL Open Font License notice. No font enters the installed Skill or shared examples/publication assets. |

These checks concern source and evidence identity, not perceptual quality or the
truth of a participant's professional interpretation. The package file count was
1,159 during the first identity sweep; the subsequently added gallery, review
navigation and this audit are final reporting additions. The maintained release
inventory must be regenerated after all final documents are present.

The audit read the preserved [final suite log](logs/unit-final-rerun.txt):
**283 tests passed**. This was an existing maintainer execution, not a new suite
run by this reviewer. The preceding `unit-final.txt` remains present with its
old blanket-font assertion failure. The revised test retains an exact two-file
allowlist plus license checks and continues to exclude fonts from the portable
Skill. Its changed responsibility is described in the version review.

## Requirement coverage and semantic continuity

The audit compared the actual baseline-to-candidate changes in the installed
entry, workflow, analysis, sourcing, evidence map, optional record profile,
verification and templates, together with the maintainer model/writing updates.
The [semantic review](semantic-review.md) separates changed meaning from byte
restoration; the [continuity ledger](continuity.json) supports historical identity.

| User requirement group | Implementation assessed |
|---|---|
| 01–03: complete goal, formal increment and four work objects | The entry defines a coherent, quality-assessable increment on the current product. Overall goal, current UI, formal SPEC and internal work have separate responsibilities. Original representative-content, meaningful-path and product/demo/authored boundaries remain. |
| 04–06: minimum sufficient closure and dynamic complexity | Analysis gives necessary experience relationships, contextual reviewability, six qualitative factors, and visible-surface versus quality-bearing-object reasoning. No component/page count or numeric score determines a boundary. |
| 07–09: active scope judgment, init planning and formal semantics | Keep/split/merge/redraw have conditions and preservation duties. Init presents provisional candidates and a first priority. Research, repair, new turns and another iterate invocation do not automatically create a new formal SPEC. |
| 10–12: equal standing, continuous product and three scopes | Formal standing does not depend on area. Inherit/Extend/Adapt/Revisit describe work on the same UI. Research, primary implementation and regression remain independently meaningful. |
| 13–15: quality ownership, first result and feedback | Sourcing and verification connect target quality, observed reference, implementation, current result and remaining gap. A representative first closure needs inheritable quality. Trials and implementation can revise the boundary while retaining old responsibility. |
| 16–18: conversation delivery, product content and validation | The same current information supports the three views and user-facing findings. Saved files do not substitute for delivery. Product UI serves actual user tasks. Local quality and related-product effects require distinct evidence. |
| 19–20: integrate without another management lifecycle | Rules sit in their existing responsible references. Shape, audit and finish retain their roles. Routine decisions use existing authority; no new state machine, approval stage, fixed research quota or mechanical maturity gate was added. |
| 21–22: actual experiment and integrated capability | The registered study exercises all three requested method conditions across three families and a continuation, covering the requested six task dimensions. It is explicitly exploratory, with one sample per cell and no generalized winner claim. |

Still-valid professional guidance remains in the installed package. Changes are
predominantly additions; the entry definition and operation summaries receive
specific semantic refinements. The original eight common-reference reading
contract, intent research, temporal inspection, art direction, mature-resource
adoption, assets, content, accessibility, performance and integration methods
remain available. No detail was relocated exclusively into maintainer documents
as a substitute for runtime guidance.

The new historical reconstruction layer restores v1.16.1 before the older
v1.16/v1.15 checks run. The older ledger hashes and evidence are preserved. The
old inspector-identity assertion now names and checks the recovered historical
version, while the candidate has its own exact identity and behavior tests.
This is a version-boundary correction rather than acceptance of arbitrary bytes.

## Neutral inspector and compatibility

`check_design_evidence.py` adds optional `product_context`, `candidate_specs`
and `formal_specs` declarations. The inspected implementation describes supplied
text and literal IDs, resolves declared objects/decisions/related SPECs, and
reports malformed or ambiguous references as structural observations. It neither
writes project records nor chooses the number, sequence, merge, split, completion
or quality of SPECs. `scope_judgment` explicitly remains `not_assessed`.

All three projections use the same declarations and return deep copies. Missing
optional SPEC fields do not create required planning tasks. Legacy
`ui-spec-evidence/1` records remain readable without migration. The format and
CLI exit semantics remain unchanged: readable records can have findings and exit
0, while unreadable inputs exit 2. No aggregate pass/completion score was added.
The new tests cover partial/legacy data, duplicate namespaces, unresolved IDs,
malformed declarations, read-only behavior and shared object references.

## Packaging, replay and third-party boundaries

The complete archive explicitly includes study-only logs, CSV/JSONL, module
scripts, licensed WOFF2, WebM, JPEG and ZIP evidence under `docs/evidence` and
`docs/experiments`. The installed runtime remains 37 files. The checked package
inclusion matches every participant and reviewer archive index; it does not
silently discard the font, capture or original log needed to inspect a result.

The replay helper checks canonical relative paths, contained archive reads and
per-file SHA-256 before writing a new output, and refuses an existing destination.
The documentation distinguishes restored source/evidence from a restored Agent
session, browser profile or running server. Original host paths are identified
as provenance requiring deliberate adaptation. `.gitattributes` prevents text
normalization of raw study/review/shared-input bytes on different checkout systems.

The two actual font files retain their OFL notices. Existing Bootstrap/Pico and
other adopted-source notices remain beside the archived applications. Shared
Modern Web Guidance is separately attributed to its source/documentation license,
with the frozen text, package provenance, Apache license and third-party notices
retained. The study guide's terms are not presented as replaced by the repository's
MIT license. This review verifies declared packaging and notice preservation;
it does not claim a universal rights audit of every external source.

## Experimental interpretation and release claims

The inspected final [results](../../experiments/adaptive-granularity/RESULTS.md)
correctly count nine independent participant threads and eighteen task stages,
not eighteen independent runs. Same-Agent continuations and retained initial
outputs support inspection of product evolution. Preparation registration keeps
its original `prepared_not_run` status; actual execution is recorded separately.
The protocol states common ceilings, shared tools/reference inputs and the lack
of exact token/active-compute accounting. T1 host interruptions are retained and
exclude an efficiency ranking. Condition C's richer record structure is not
misrepresented as proof of better UI.

Three fresh Agent reviewers inspected anonymous shuffled products before the
condition synthesis. They are neither human participants nor the owner. Final
source identities and frozen report hashes are preserved. The final synthesis
accurately carries these important mixed findings from the original reports:

- T1: C retained note-save failure priority and Retry during appearance-setting
  failure; A/B did not. B's density select lacked a viewed focus cue. C's visible
  error banner also consumed additional narrow reading space.
- T2: C held the tested 40 px upward wheel gesture, while A/B resumed following.
  C still had no Stop inside the narrow source modal and its desktop close control
  could scroll away. A had a settled paragraph-return gap; B had blank reserved
  space during the tested restart path. C's response workload differs from A/B's
  optional long-answer mode, limiting attribution.
- T3: A/C lost focused Save to BODY after a failed keyboard save; B retained it.
  Drafts and prior stored content remained, and retry was reachable. Collection
  layout and transition choices show different tradeoffs, not an aesthetic winner.

The original harness failures and corrected reruns remain distinguishable from
application defects. Captured frames, actually viewed frames, sampled temporal
sequences, assertions and owner acceptance are not collapsed into one result.
The gallery offers equal desktop/narrow coverage of each cell and links back to
all findings; it does not erase the frozen defects through post-review repairs.
The review/release prose makes no unsupported visual superiority, efficiency,
production acceptance, physical-device smoothness or statistical-effect claim.

## Remaining release steps and audit limits

The maintainer still owns final working-tree/source gates, final inventory and
archive generation, the reviewed commit/ref update, the existing remote CI jobs,
release creation and exact tag/asset/install readback. The intermediate unreferenced
remote tree reported by the maintainer is not publication evidence. This audit
neither performs those steps nor reports them as complete.

No additional broad browser tests were requested or rerun. Existing browser and
README evidence retains its own recorded conditions; this audit reviewed source,
reports and identities rather than claiming another independent pixel assessment.
One sample per condition/family, supplied references, a single model configuration,
bounded continuations, Agent reviewers and missing token accounting constrain the
study. Repeated broad-brief work, longer evolution and actual human observation
remain future evidence needs. They do not prevent publishing a compatible method
update with the explicit limits documented here.

Recorded at 2026-10-29T22:07:13.948818+00:00.
