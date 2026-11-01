# SPEC 01 — Compose, identify files, and keep reading

## Overview

Meridian remains a working local conversation workspace with deterministic synthetic responses and filename-only attachment metadata. The overall product goal is to ask, review a long answer, inspect selected filenames, reread while text arrives, and continue without losing input or reading position.

The current foundation is assistant-ui's complete cloud template at `ff654d8156680b839774296ef644b57ab1078425`, its actual Thread/composer/sidebar, base-ui controls, Inter and IBM Plex Mono. This increment retains that family. No original replacement design is authorized or planned.

One formal increment owns the coupled composer/attachment/reading experience. Composer height, attachment layout, thread geometry, scroll-follow intent and focus share a continuous task and must be reviewed together. Remote history, model service, uploads and file-content reading stay outside the supplied contract.

## Evidence map and current questions

| Scale | Object and question | Evidence / next action |
| --- | --- | --- |
| L0 | Can a researcher recognize and continue the current conversation? | Supplied task/input; seeded baseline desktop screenshot. Preserve the source shell and reading measure. |
| L1 | Ask → partial answer → scroll away → return → stop/retry → follow up | Run through visible controls with timestamped scroll and content observations. |
| L2 | Does growing input preserve usable answer space at 1280×600? | Baseline compact-expanded screenshot: six lines plus four tiles occupy the lower 270 px. Trial a source-backed filename treatment and bounded growth. |
| L3 | Can four local files be distinguished and removed? | Baseline tiles are visually identical. Compare assistant-ui composer chips, existing File component, and independently authored AI Elements inline/list attachments. |
| L4 | Are type, surface and action hierarchy preserved in light English and dark Chinese? | Baseline captures viewed personally; final viewport and focus captures required. Keep source tokens, radius, font roles and send/stop hierarchy. |
| L5 | Do actual runtime controls preserve abort, retry, IME handling, focus and manual scroll intent? | Source/runtime inspection and dedicated Playwright episodes against the owned Vite application. Build success alone is insufficient. |

## Initial decisions and limitations

1. Keep the supplied mature Thread and composer. Its 44rem measure, quiet border, independent action row and bottom docking fit this task in the observed desktop baseline.
2. Attachment identity is an observed gap: four document tiles look the same at 1280×600 until individually hovered/focused. A filename-bearing mature source is the next trial; no visual rewrite is justified.
3. Keep assistant-ui as the owner of thread, composer, cancel, retry and scroll state. Do not force-scroll to satisfy a test. Confirm its reading behavior before changing configuration.
4. Current web guidance was retrieved for IME-safe submit and initial scrolling. Source ComposerInput already calls `isCompositionKey`; initial-scroll CSS is unnecessary because the runtime owns this behavior.
5. Research sources are references until actual code, trial and assembled viewing establish adoption. The evidence directory retains original web exports and command captures.

## Verification boundary

Inspect 1440×900 and 1280×600 in light/en and dark/zh, plus 390×844 supplementary views. Exercise one-line, six-line and long mixed-language drafts; short and long filenames; send/cancel; scrolling away during growth; return-to-latest; first failure and successful retry; focus and repeat-question continuity. Static image viewing, controlled timestamped episode checks, and natural-time playback must be reported separately.

## Source records

- Supplied provenance: SOURCE-MANIFEST.json and FONT-SOURCES.json.
- Baseline: evidence/baseline/ and evidence/view-baseline-*.json.
- Research: evidence/web-001.json, evidence/web-002.json, evidence/public/.
- Current guidance: evidence/commands/001-guidance-search and 002-guidance-retrieve.

Owner approval of the final product is pending. Execution authority covers the supplied task and source-supported adaptation only.

## Settled design and verification outcome

The final increment adopts the exact pinned ComposerAttachmentChip within the existing attachment component. It preserves source typography, surfaces and action hierarchy while making each filename visible. Full names use the source Tooltip with explicit accessible description and focus/touch activation. The attachment region wraps and scrolls above 112px; textarea growth is bounded by min(12rem,25dvh). These are coupled composer and reading decisions within this single SPEC, not separate visual replacements.

The thread now uses the runtime's supported bottom anchor with autoScroll. A manual scroll-away pauses following, Return to latest resumes it, and a second scroll-away pauses again. The failed dynamic anchor trial is preserved. Stop aborts the supplied adapter, flushes already-received smoothing and restores composer focus. The adapter, long example, first-failure/retry rule and in-memory history contract remain unchanged.

At 1280×600, four identifiable files plus six draft lines produce a 309px composer versus roughly 270px in the baseline. About 203px of reading remains above it below the header. This is a deliberate identity/space tradeoff. Very long drafts and additional files stay reachable via their bounded scroll regions. No density improvement is claimed.

The English controlled episode passed 19 checks in evidence/final-confirmed/results.json. The Chinese streaming/failure episode passed its five main checks; a later edit-harness timeout is retained and corrected by the nine passing checks in evidence/details-release/results.json. The final five touch/focus/dismissal checks pass in evidence/touch-complete/results.json. Final build and TypeScript checks pass in command records 031 and 032. All six viewport/theme/locale initial views were personally inspected; selected final expanded and episode views were inspected separately. See VISUAL-REVIEW.md for exact viewing boundaries and ADOPTION.md for source relationships and retained failed attempts.

Remaining limits: Chromium-only automation, emulated touch/viewport, synthetic IME event, no screen-reader or physical mobile keyboard check, and no natural-time video playback. HuggingChat's authenticated task episode was blocked by sign-in. The inherited ~1.29MB minified JS chunk triggers Vite's size warning. Some upstream shell labels remain English. These limits do not change the preserved local synthetic service boundary.
