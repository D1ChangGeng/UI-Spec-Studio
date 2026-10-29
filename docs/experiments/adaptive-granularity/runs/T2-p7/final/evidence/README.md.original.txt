# Meridian evidence

## Executed application checks

All application runs used actual HTTP at `http://127.0.0.1:8767/app/`, Chromium headless shell 143.0.7499.4, Playwright 1.57.0, device scale 1, English UI, and the supplied font configuration. Desktop: 1440×900. Phone emulation: 390×844. No physical phone or virtual keyboard was used.

- `verification.json`, `verification-run-2.log`, `verify.py`: **32 passed checks**. Core conversation, stop/continue, retry, repeated questions, source/reading continuity, attachments, storage reload, thread search/switching, themes, mobile modal, growth, reduced motion, console and network destinations. `frames` records monotonic capture-time brackets for ordered stills.
- `focus-review.json`, `focus-review.log`, `focus_review.py`: **12 passed checks** after the keyboard refinement. Retry/Continue focus, completion focus return, interrupted reload, truthful completion labels, mobile dark failure, source-close reachability, attachment removal, and storage-unavailable behavior.
- `drawer-review.json`, `drawer-review.log`, `drawer_review.py`: **3 passed checks** after compact navigation became a side drawer. Bounds, Escape/focus/draft retention, and theme switching.
- `draft-review.json`, `draft-review.log`, `draft_review.py`: **1 passed check** after adding unsent drafts to history. The draft resumes after New research.

The later changes are scoped: focus/copy, phone-navigation geometry, and inclusion of unsent drafts in history. The unchanged conversation/stream/persistence claims from the main run remain applicable. Each JSON record retains the source hashes that were current for that run.

## Original failures preserved

- `verification-run-1.log`, `run-1/verification.json`, `run-1/*.png`: the first runner passed seven checks and then failed because string-based `wait_for_function` polling invoked eval blocked by the app's CSP. The app CSP was retained. The wait was changed to a locator assertion. This was a test-harness failure, not a passing application check.
- `research-browser.json`: initial public reference navigation failed with `ERR_CERT_AUTHORITY_INVALID`. `original-retry.json` records the separate successful read with test-browser certificate verification disabled. No input was submitted to the public page.
- `v1-desktop-dark.png`: first theme-transition capture showed mixed old button surfaces and newly changed text. Button color/background transitions were removed; reviewed final dark captures show coherent settled roles. The old capture remains historical.

## Actual pixel inspection

Viewed the supplied reference's conversation, document, and active captures; the successfully retrieved original assistant-ui carrier/example image; all eight `v1-*` captures; the four `episode-0*` pending/streaming/stopped/completed stills; final desktop empty/source/dark/failure views; final mobile empty/answer/source/dark/multiline/history views; focused mobile light/dark failures; focused desktop source; and final light/dark navigation drawer images, including the populated draft drawer.

Visual observation: the answer and composer share a bounded measure; the original editorial heading treatment carries into answers; source notes have a distinct secondary surface; phone source reading keeps a visible close control; light/dark text and controls remain coherent after the repair. The source-return reading offset was separately measured at 180px before and after in the desktop run. During streaming with the reader held at 120px, the measured offset stayed 120px.

The ordered stills show sampled states and their sequence. They are not continuous-video playback, frame-rate measurement, actual user comprehension, or owner acceptance. No formal full accessibility audit, assistive-technology test, physical mobile keyboard, Safari, or Firefox check is claimed.

## Replay

From the cell root, start a static server:

```sh
/workspace/scratch/43b440780c87/test-env/bin/python -m http.server 8767 --bind 127.0.0.1
```

Then run a saved runner (local sockets and browser launch require the authorized escalated environment):

```sh
FONTCONFIG_FILE=/workspace/scratch/43b440780c87/preview-fontconfig.xml PLAYWRIGHT_BROWSERS_PATH=/workspace/scratch/43b440780c87/playwright-cache /workspace/scratch/43b440780c87/test-env/bin/python evidence/verify.py
```

Use new log/output filenames for future runs if preserving historical captures.
