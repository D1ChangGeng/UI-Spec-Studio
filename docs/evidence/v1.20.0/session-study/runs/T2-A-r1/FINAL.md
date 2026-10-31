<!-- Derived navigation copy; never use as an original participant export. -->

> Repository navigation copy. The participant report is retained byte for byte in [FINAL.md.txt](FINAL.md.txt) and the workspace overlay archives. Only local artifact link destinations below are adapted for this repository.

# Meridian — composer and reading continuity delivered

The running application increment is complete in this work package, with rebuilt production output in `app/dist/` and the original dependency lockfile retained. The mature assistant-ui workspace remains the visual and behavioral foundation.

## What changed

- **Recognizable attachments.** Selected files now use the actual filename-bearing assistant-ui ComposerAttachmentChip from the same pinned source revision. Short names are visible; long names disclose fully on hover, keyboard focus or touch. The disclosure accurately states that only filenames are retained. Removal returns focus to the composer.
- **Bounded composer growth.** Files wrap within a scrollable 112px region. The textarea grows naturally to `min(12rem,25dvh)`, then scrolls internally, keeping the action row available.
- **Reading continuity.** The source runtime uses its supported bottom-follow configuration. Scrolling away holds the reading position while text grows; Return to latest resumes following; scrolling away again pauses it. Stop restores input focus and settles already-received renderer text.
- **Task controls in Chinese.** The relevant composer, disclosure, message edit, retry, send and stop labels follow the supplied language condition. Some inherited shell/sidebar labels remain English.
- **Build compatibility.** The TypeScript 7 path configuration and Vite declarations are repaired without changing dependencies.

The synthetic adapter remains unchanged: fixed long local responses, first-attempt failure for `[fail]`, successful retry, abortable chunks, filename-only attachments, and in-memory history that resets on reload.

## Run the product

From this package:

```bash
cd /workspace/scratch/708e8b7f118e/ui-study/worksets/w05/app
npm run dev -- --host 127.0.0.1 --port 4405
```

Open [light English](http://127.0.0.1:4405/?theme=light&lang=en) or [dark Chinese](http://127.0.0.1:4405/?theme=dark&lang=zh) in a browser on the executor host. The connected user browser cannot access that executor-local address. The preview server used for verification was stopped at handoff as required by RUN-CONTROL.md.

The rebuilt static output can also be served with:

```bash
python3 -m http.server 4405 --bind 127.0.0.1 --directory dist
```

## Verification and visual review

The production build and TypeScript check pass. The following actual browser checks and their original logs are retained:

| Verification | Result | Evidence |
| --- | --- | --- |
| English compose, filenames, long draft, reading hold/return, stop, retry, repeated question, synthetic IME event, Shift+Enter and viewport overflow | 19 checks passed | `evidence/final-confirmed/results.json` |
| Chinese streaming, manual reading hold, return, keyboard Stop and failure/retry | 5 core checks passed | `evidence/variants/results.json` |
| Editing/cancel, retained main draft, reduced motion and expanded Chinese layouts | 9 checks passed | `evidence/details-release/results.json` |
| Final touch disclosure, outside dismissal, focus disclosure, Escape and removal-focus return | 5 checks passed | `evidence/touch-complete/results.json` |
| Final production build / TypeScript | Passed | `evidence/commands/031-build-complete/`, `032-typecheck-complete/` |

The earlier Chinese edit-harness timeout, incorrect selector attempt, failed touch attempts and source-configuration trial remain recorded; they are not erased by the passing final checks.

I personally inspected all six initial and all six settled expanded-composer views at 1440×900, 1280×600 and 390×844 in light/en and dark/zh, plus selected ordered streaming, disclosure and editing frames. Actual view-image responses are saved. Representative captures: [compact English](artifacts/evidence/settled-final/light-en-1280x600.png), [compact Chinese](artifacts/evidence/settled-final/dark-zh-1280x600.png), [mobile Chinese](artifacts/evidence/settled-final/dark-zh-390x844.png), and [touch filename disclosure](artifacts/evidence/touch-complete/01-touch.png).

In the English controlled episode, scrollTop stayed at 26 while visible answer length grew from 1088 to 1980 characters. Return then reached and continued following the bottom. After a second scroll-away, the position again held. After Stop settled, two samples remained at 4491 characters with textarea focus. This supports the intended reading behavior; it is not a human user study.

## Source decisions and limits

The final source audit confirms **32 of 35 manifest-listed mature files remain byte-identical**. Three existing components are adapted, and the new chip is selectively copied from the exact upstream revision `ff654d8156680b839774296ef644b57ab1078425`. MIT and font notices remain. Independent AI Elements attachment variants and a complete chatbot were inspected as references; their code was not adopted. HuggingChat reached a sign-in wall, so its authenticated composing/streaming behavior remains unobserved.

The main design tradeoff is space: at 1280×600, four identifiable filenames and six draft lines create a 309px composer, approximately 39px taller than the anonymous-tile baseline, leaving about 203px of reading area below the header. Long draft and file growth are bounded, but this is not a density improvement.

No outstanding defect was observed in the final targeted checks. Verification is limited to Chromium, emulated viewport/touch and a synthetic IME event. Physical mobile keyboards, screen readers, other engines and natural-time video playback were not tested. The inherited production bundle still triggers Vite's size warning at about 1.29MB minified JavaScript.

The complete rationale, source relationships, preserved failures and inspection boundaries are in [SPEC.md](artifacts/SPEC.md.txt), [ADOPTION.md](artifacts/ADOPTION.md.txt), and [VISUAL-REVIEW.md](artifacts/VISUAL-REVIEW.md.txt). The [final source audit](artifacts/evidence/provenance-complete/source-audit.json) records exact original and current hashes.

