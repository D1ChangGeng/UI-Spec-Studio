# 1.7 review: visual reasoning and continuous experience

Reviewed on 2026-10-26 (Asia/Tokyo). The published baseline is v1.6.0,
commit `ec4dc67dba09d49a36bc9025bf8f916cfa855c4a`. The existing uncommitted
visual-observation draft and temporal example were preserved and completed.

## Capability and responsibility

Visual Reasoning & Visual Inspection now connects research, resource selection,
composition, asset production, implementation and acceptance. Temporal Visual
Inspection follows an episode with a starting context, trigger, meaningful
progression and endpoint. The task determines the observation window, including
reversal, repeated input, loop seams, asynchronous outcomes and connected return
where they affect the design.

The eight common references retain their responsibilities and the existing
144 KiB combined-content cap. The working path remains `init → iterate → finish`,
with optional `shape` and continuous `audit`. The [visual guide](VISUAL-INSPECTION.md)
connects the public explanation to the runtime methods.

| Responsible source | Decision supported |
|---|---|
| Skill entry and workflow | Make actual viewing part of each consequential design decision |
| Analysis and visual principles | Relate visible relationships to perception, product intent and a testable cause |
| Resource discovery and assets | Inspect exact candidates, inherit useful qualities, then inspect their composed placement |
| Interaction and variants | Diagnose seven temporal qualities through actual change and complete state paths |
| Verification | Choose observation windows and capture conditions; distinguish recorded, viewed and measured evidence |
| Integration | Compare meaningful task events and actual results at their real boundary |
| Existing optional records | Link decisions to viewed frames/intervals, changes and the actual review/approval scope |

Positive observations can justify adoption and preservation. A visual finding can
also reopen a resource or composition choice. Source-resource quality, combined
quality and delivered-runtime quality each retain their own observation.
Professional interpretation, tested implementation cause and actual user response
remain distinct.

## Evidence collection and inspection

The [temporal note fixture](../examples/temporal-review/README.md) records natural-time
interaction episodes, ordered full-viewport screenshots, actual capture-time
brackets, event/state observations and viewport-sized videos. Its real save
boundary is browser Storage; the 900 ms delay and injected failure are identified
as authored test conditions. The recorder leaves visual review pending so the
capture result cannot stand in for pixel inspection.

First visual inspection found missing Chinese glyphs in the local browser.
The affected captures were excluded from Chinese typography conclusions. Existing
Noto CJK fonts were configured for the browser and the affected runs repeated.
This correction belongs to the viewing environment; the actual rendered result
is checked again before extending the visual conclusion.

## Findings that changed the implementation

Actual visual inspection, visible-control interaction and implementation analysis
contributed different parts of these corrections:

| Observed relationship or failure | Correction and recheck |
|---|---|
| The card's identity and stationary controls remain legible during sampled forward, reverse and interrupted turns. | Preserve the shared card object, its container and external controls; inspect intermediate frames as well as the two faces. |
| A paused decorative dot changed position after visiting Saved note and returning. | Preserve its paused phase across the hidden view; compare actual transforms and the returned frame. |
| A save can finish for the submitted version while a newer draft is being edited. | Preserve both versions and identify which one reached Storage; check the saved view and the retained draft. |
| The original native 600-character bound silently cut off longer input. | Keep the full draft, expose its count and limit, and prevent an over-limit save without discarding text. |
| Opening Saved note during a save showed an empty-state instruction while work was pending. | Carry pending and outcome feedback into that view; distinguish an existing saved snapshot from the first in-flight save. |
| An unreadable stored record was presented alongside an instruction to save first. | Identify the record as unavailable, explain the valid recovery path and return to the visible recovery control. |
| Returning to editing focused the header instead of the work area. | Focus the textarea on a normal return and the recovery control when that is the next valid action. |
| Clearing from Saved note could fail with its feedback and retry hidden in the editor. | Reveal and focus the existing recovery surface on failure; preserve the original data until a native removal succeeds. |
| The Chinese README rendered literal emphasis delimiters in its new section. | Move the parenthetical translation outside the emphasis delimiters and rerender the actual Markdown. |

The research question beside its editable note, restrained main action, stationary
flip controls and separate decorative region were useful relationships to retain.
The sampled narrow composition puts the question before its editor. These are
observations about this authored example, not a universal layout prescription.

## Independent forward application

A separate fresh-context agent received the skill and a frozen, pre-fix copy of
the three-file prototype. The task asked it to use ui-spec to assess whether a
personal research-note interface and its actual operation were coherent before
expansion, identify confirmed issues and relationships worth retaining, and give
one actionable improvement pass in a 1,200–1,800-character Chinese report. It was
asked to use the prototype, keep the review read-only and state evidence and
unconfirmed conditions. No expected diagnosis or intended repair was supplied.
After the agent independently identified missing CJK glyphs, the available font
configuration was supplied as an environment correction.

The agent read all eight common references and integration, used the actual
interface and produced a report, an evidence index, three reproduction scripts
and screenshot/state records. It independently identified silent truncation,
cross-view pending/error ambiguity and lost return focus/position. It also explained
the value of question/editor proximity, stationary card controls and submitted
version versus draft separation. Those findings informed the corrections above.

| Original prototype file | SHA-256, unchanged through the independent review |
|---|---|
| `index.html` | `114a1cf9d8842383bdcba7ff9cc81fe673298f419dec7af2d67faf5936991ea7` |
| `styles.css` | `348497479c56add26ed4a93ec27ab0dca56e102c44d6352e12c61b9f3c761789` |
| `app.js` | `8fe4952610ab37faed3f249875a8e091b4cb45a3a1812963ab6bd5c634c131a6` |

This application used Chromium 143, local HTTP and real browser Storage at DPR 1,
with 1365×900 and 390×844 views plus 320×568 and 280×568 narrow checks. It viewed
58 ordered frames across decoration, interrupted flipping and save-while-editing
contact sheets, and selected full-size frames and task states. The screenshot
brackets include capture overhead. No video playback or frame-delivery measurement
was performed. Some auxiliary captures were not individually viewed; a rerun of
the focus/scroll script replaced same-condition images, of which the final
keyboard-scroll image was reopened. The report retains that distinction.

This is one scoped application to an authored local prototype. It demonstrates
the observed use of the method and its concrete findings. It does not establish
comparative model performance, general product quality or user acceptance.

## Validation record

The local package/link check, deterministic README-art check and generated
resource-map check passed. The unit suite passed 153 tests, including four new
tests of temporal capture-summary arithmetic and invalid ordering. These test
helper behavior; they do not turn a visual observation into an automated score.

The local README renderer was exercised in English and Chinese, light and dark,
at 390×844, 768×1024 and 1440×1000. All 24 final viewport/full-document PNGs were
opened, with six additional readable crops for the changed Chinese section.
The missing-glyph run was excluded. The final CJK glyphs and emphasis render
correctly, the narrow install entry remains visible and the section/table
hierarchy remains readable in the inspected conditions. Actual GitHub rendering
is a separate publication-job artifact for the source commit, with its own
renderer and environment recorded.

The final local temporal run passed 23 grouped runtime checks and produced
23 recorded episodes/state probes, 236 chronological PNGs and two viewport-sized
WebMs. The held over-limit probes inspect the resulting input state; event-driven
episodes also cover their triggers and progression. Chromium 143.0.7499.0 ran at
DPR 1 with English/light at 1280×900 and Chinese/dark at 390×844. Browser time ran
normally and screenshot animations were allowed. Storage persistence and reload
were verified at the actual browser boundary.

All 17 chronological contact sheets in the earlier reviewed run were opened.
For the final source, the desktop and narrow first-save, existing-save and
clear-failure sequences were reopened; the narrow unreadable-record and
saved-view-return sequences were also reopened. Selected original-size frames
confirmed long-input feedback, visible clear recovery and the distinction between
pending and persisted snapshots. The review did not individually open every one
of the final 236 PNGs or play the two recordings at natural speed.

The report identifies actual action/capture brackets, browser/font conditions
and source identity. The local report records the baseline Git commit with a dirty
worktree; these content hashes identify the captured implementation precisely:

| Captured file | SHA-256 |
|---|---|
| `examples/temporal-review/app.js` | `8cb00044e3c1ed0939a2ec1ae5f37e792b3f3beaf33518db6df2f4bc731710a0` |
| `examples/temporal-review/index.html` | `25045f01f6214aedad57af2bbe9dfdbc6b5183c29dd74e7696313f9852af2327` |
| `examples/temporal-review/styles.css` | `7eee394aca570e9a0d7754cde2401be9de2d0970ac5a6165705e28069c0eb231` |
| `tools/validate_temporal.py` | `e1761aeb89245b506b63a7dff6205fcdcf51c74afa53bc90e86cc1079a287a54` |

The example README received one subsequent prose clarification about the labelled
first-save snapshot; the captured runtime sources remained unchanged. No recording
was treated as viewed merely because its file existed.

The required Actions jobs execute platform tests, local and exact-commit Skills
CLI installation, local and live GitHub publication capture, and product, asset,
content and temporal browser checks. Their run and artifacts are associated with
the exact source commit. The release job verifies the tag and downloaded archive
bytes before publication and then installs the published version. Read the actual
run conclusion and release identity alongside this source review.

## Evidence boundaries

The automated temporal report intentionally leaves visual review pending.
Engineering assertions establish the state, identity, geometry and persistence
properties they execute. Opened images establish observations of those samples
and their visible relationships. Contact sheets preserve sequence but do not
replace original-size typography review or natural-speed playback.

The reviewed evidence does not certify video pacing, presented-frame delivery,
field responsiveness, target-device smoothness, screen-reader behavior, a complete
locale/theme/viewport matrix, production service integration or real-user
comprehension. No external component adoption was executed in this authored
fixture. Resource discovery methods and their source/composition/runtime checks
must be applied to the actual candidate and consuming product. Design approval
keeps the scope the user actually granted.
