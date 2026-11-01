<!-- Derived navigation copy; never use as an original participant export. -->

> Repository navigation copy. The participant report is retained byte for byte in [FINAL.md.txt](FINAL.md.txt) and the workspace overlay archives. Only local artifact link destinations below are adapted for this repository; directory links lead to the complete-workspace reconstruction instructions.

# Meridian conversation workspace — completed local increment

The runnable application now supports a compact growing composer, identifiable filename attachments with complete-name disclosure, and controlled reading while a long answer arrives. The final browser run passed **59 of 59 checks**, with **36 captures and no page errors**. Production build and TypeScript checks passed. Primary implementation and final visual judgment remained with the main designer.

## What changed

The supplied assistant-ui visual foundation is retained: its shell, 672px desktop composer, typography, rounded surfaces and icon action hierarchy. Document attachments now compose the supplied File and Dialog elements. Each shows a filename; activating it opens the full name and a clear statement that only filename metadata is attached. Sent files wrap, and multiple draft files remain horizontally scrollable. Escape restores disclosure focus; removing a file returns focus to the message input.

At compact viewport heights, the textarea grows to four lines (96px) and scrolls internally. In the measured 1280×600 six-line/four-file state, the composer is 219px high and retains every character and attachment. Taller viewports preserve the source's larger input allowance.

The existing viewport now uses supported bottom anchoring. Scrolling away holds the reader's position while content grows. “Return to latest” immediately reaches the current end and resumes following. Stop returns focus to the composer and stops visible text: disabling the source markdown reveal buffer fixes the brief post-abort text growth found during verification. Retry, repeat submission, edit cancellation and update continue through the original runtime. Task controls and disclosures support English and Chinese.

## Run and inspect

From `/workspace/scratch/708e8b7f118e/ui-study/worksets/w13/app`:

```sh
npm ci
npm run dev -- --host 127.0.0.1 --port 4413
```

Open `http://127.0.0.1:4413/?theme=light&lang=en` or `http://127.0.0.1:4413/?theme=dark&lang=zh`. The built application is also retained in `app/dist`; `npm run preview -- --host 127.0.0.1 --port 4413` serves it. The bounded verification server was stopped at close.

The application uses the supplied deterministic synthetic responder. Add `[fail]` to exercise its fail-once/retry path. It does not call a model, read uploaded file contents, or persist remote history. The exact long-answer adapter and package lockfile remain unchanged; their hashes are retained in `evidence/protected-final.json`.

## Verification and evidence

The final static matrix covers 1440×900, 1280×600 and 390×844 in light/English and dark/Chinese. Both compact desktop episodes exercise keyboard submission, multiline input, one and several files, complete filename disclosure, focus return, streaming, manual reading, deliberate latest, Stop, failure/retry, long mixed-language drafts, repeated send, edit cancel and update. English reading position stayed at 0 while content height grew 1297→1555; Chinese stayed at 285 while height grew 1889→2559. Both latest checks reached a zero distance from the bottom and continued following. No page or thread horizontal overflow remained in the final six-condition matrix.

Main evidence:

- `evidence/final-003/results.json`: measurements and all 59 checks.
- `evidence/final-003/`: 36 screenshots, two recorded episode videos and two traces.
- `evidence/commands/021-final-build`, `022-final-typecheck`, `023-final-browser`: original command captures.
- `VISUAL-REVIEW.md`: exact personally inspected states and observation limits.
- `ADOPTION.md`: candidate comparison, source boundaries, rejected trials and repairs.
- `SPEC.md`: the coupled experience specification and settled decisions.
- `DELEGATION.json` and `evidence/research/REPORT.md`: fresh researcher request, actual capacity failure and successful ID, concise findings and original evidence.

The adopted source is assistant-ui cloud template revision `ff654d8156680b839774296ef644b57ab1078425`, with its original license and source manifest retained. No dependency was added. TypeScript compatibility repairs remove obsolete baseUrl and provide Vite client declarations. A source-family large bundle warning remains; it is not a failed build.

## Remaining limits

Public demo browsers failed certificate validation, and an ordinary verified retrieval returned 403. No security setting was weakened. Independent implementations, including Vercel AI Elements, were researched through primary documentation/source but were not visually trialed; that research gap remains explicit. The actual integrated local source was rendered and inspected.

The 390px checks use browser emulation. Physical mobile keyboards, native touch, Chinese IME composition and screen-reader use were not verified. Localization covers this task's controls rather than every upstream utility label. Recordings are retained, but visual review used ordered frames and controlled measurements rather than natural-speed playback. No subjective motion-smoothness or owner-acceptance claim is made.

All failed attempts and their corrections are preserved. The child prompt export records a terminal-newline discrepancy rather than claiming byte equality; requested model and fresh context are known, while resolved backend identity, tokens and cost are not exposed. Work stayed within the registered 1,800-second substantive bound; actual timing is in `evidence/WORK-TIMING.json`.
