<!-- Derived navigation copy; never use as an original participant export. -->

> Repository navigation copy. The participant report is retained byte for byte in [FINAL.md.txt](FINAL.md.txt) and the workspace overlay archives. Only local artifact link destinations below are adapted for this repository; directory links lead to the complete-workspace reconstruction instructions.

[Reconstruct the complete delivered workspace](RECONSTRUCTION.md).

# Meridian — composer and reading continuity

Implemented the coupled composer, attachment and reading-continuity increment in the supplied application. The runnable source, frozen lockfile and rebuilt production `app/dist/` are retained in this work package. The temporary verification servers were stopped after testing. The assistant-ui visual foundation and local synthetic-response contract remain intact.

## What changed

- Attachments now use the supplied named-file family. Short names stay compact; long names truncate within the composer strip and open in the supplied dialog with their complete text. Removal remains a separate action. The dialog explicitly states that file contents are never read or sent.
- The source viewport now uses its native bottom-following variant with immediate scrolling. Manual scrolling suspends following; “Return to latest” resumes it during active growth. This replaces the initial top-anchor behavior, which jumped once without continuing to follow.
- Composer growth retains the existing automatic sizing and 192px maximum. At 1280×600, six lines and three attachments measure 256px high, compared with the original 270px tile state; the action row remains visible.
- Removing an attachment or stopping generation returns focus to the composer without moving the reading position. The source text-reveal option now settles immediately when generation ends, so received text stops revealing after cancellation.
- Relevant composer, attachment, disclosure, return, retry and edit controls have Chinese labels in the Chinese condition. Existing surrounding English header/sidebar copy is retained.

No new dependency or original visual construction exception was introduced. Four copied source files were adapted, with one small project-owned focus utility. Exact source changes, licenses and hashes are recorded in [ADOPTION.md](artifacts/ADOPTION.md.txt) and evidence/source-integrity-final.json.

## Verification and actual visual review

I personally opened the final 1440×900, 1280×600 and 390×844 views in light/en and dark/zh, including expanded input, full-filename disclosure, mobile attachment overflow, streaming return, stopped output and editing. The source reading measure, typography, surfaces and action hierarchy remain coherent. All six primary views have no document-level horizontal overflow.

Controlled UI checks exercised one-line and six-line input, Shift+Enter, long mixed-language drafts, several real filenames, keyboard disclosure/Escape, removal, send, manual scroll during growth, draft growth while reading above latest, return, stop, injected failure/retry, repeated questions and edit/update. In the final active-return samples, the bottom gap remained zero while content height increased. Dedicated early cancellation left 211 rendered characters unchanged across 700ms in each language and restored input focus.

`npm run build` succeeded. A final check served the rebuilt production artifact and verified first-failure/retry in both languages: all seven sections and the final bullet rendered, with no page errors. The broad check and targeted rechecks retain their real failures and corrections: focus loss, buffered text reveal, rejected scroll trials, a missing hover step in the edit test, and a late Chinese cancellation assertion. The dedicated early-cancel test closes that last assertion at the correct boundary; historical failures were not relabeled as passes. No page errors were reported in the broad browser run.

## Research and provenance

Independent research compared the original AI Elements named inline/list demos, pinned Vercel chatbot source, and an actually operated signed-out ChatGPT composer-growth episode. I personally inspected the pivotal captured images. Named inline files fit the short composer better than tall list rows or anonymous image tiles. The existing assistant-ui File and Dialog family was selected for integration; the independent examples remain comparison references. External streaming behavior was not observed, and blocked sources remain documented.

## Run

From this work package:

```bash
cd app
python3 -m http.server 4408 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:4408/?theme=light&lang=en` or `http://127.0.0.1:4408/?theme=dark&lang=zh` in an executor-reachable browser. The connected user browser cannot reach this executor's localhost. For development, run `npm run dev -- --host 127.0.0.1 --port 4408`.

## Handover and limits

- [SPEC.md](artifacts/SPEC.md.txt) is the current design model and explains the consequential tradeoffs.
- [VISUAL-REVIEW.md](artifacts/VISUAL-REVIEW.md.txt) records the primary designer's actual observations and evidence scope.
- [ADOPTION.md](artifacts/ADOPTION.md.txt) and [CHILD-01-REPORT.md](artifacts/CHILD-01-REPORT.md.txt) retain source decisions and independent comparisons.
- [DELEGATION.json](artifacts/DELEGATION.json) and evidence/coordination retain the actual child dispatch, canonical ID, final notification and report reference. Backend identities, native role bindings, total tokens and billed cost remain unknown.
- evidence/commands, evidence/screenshots, view-001.json through view-038.json, final-checks.json, recheck-final.json and cancel-boundary.json retain original outputs and corrections.

The requested local task loop is working under the exercised conditions. Natural-speed playback, physical mobile keyboard behavior, screen-reader usage and other browser engines remain unverified. Some surrounding labels remain English. The build retains a large-chunk warning (about 1.29MB minified JavaScript); no performance claim is made. This remains a deterministic local application with filename metadata, in-memory threads and no real model/upload service. Owner acceptance is pending.
