# Continuation evidence: source reading during streaming

## Scope and execution

The same local application was exercised over HTTP at `http://127.0.0.1:8767/app/` using the supplied Chromium 143/Playwright environment, 1440×900 desktop and 390×844 phone viewport emulation, scale 1, English UI. The prior reviewed color/type/layout direction and supplied reference observations were inherited; this round changed source association, scroll ownership, focused-reader controls and return behavior.

- `check.py`, `run-1.log`, `checks.json`: **17 passing checks** covering opening during a long stream, linked paragraph/excerpt, scroll hold, composer growth, Stop/Continue/Retry with the panel present, return, latest following, phone modal controls, themes, Escape/focus, overflow and console errors. Ordered frame capture-time brackets are in the JSON.
- `recovery_check.py`, `recovery-run-1.log`, `recovery-checks.json`: **7 passing checks** covering closing during streaming at an actual nonzero offset (169px before and after), focus return, actual simulated failure with the source still present, successful panel retry without duplicate follow-up, focus after DOM replacement, and errors.
- `passage_check.py`, `passage-run.log`, `passage-checks.json`: **2 passing checks** covering Show paragraph in the desktop reader and explicit phone return to its marked answer passage.

The footer's final wording clarifies that its controls operate on the latest answer. That copy change does not change the tested state/scroll mechanisms. Original source snapshots from before this continuation are preserved as `before-*`; the pre-focus-fallback implementation is `run-1-app.js`. No failing check occurred in these continuation runs. The earlier certificate/harness failures remain in the original evidence directory and were not relabeled or overwritten.

## Viewed pixels and observations

Viewed desktop open-while-streaming, expanded composer, stopped state, dark panel, simulated failure with source retained, and recovered state; phone active source, stopped source, return, dark source, and Show paragraph return. The green inset marks visibly pair the answer paragraph with the source excerpt. On phones, the source passage occupies the scrolling body while the Answer return and response controls stay in fixed chrome. The wide composer can grow while the reference remains readable beside it.

Browser assertions are distinct from those pixel observations. Ordered stills sample state and timing; continuous video, frame-rate quality, real users, assistive technology, physical mobile keyboards, Safari and Firefox were not evaluated. Synthetic note paragraph mapping is authored fixture data, not real citation-range retrieval.

## Replay

With the existing cell-root server running on port 8767:

```sh
FONTCONFIG_FILE=/workspace/scratch/43b440780c87/preview-fontconfig.xml PLAYWRIGHT_BROWSERS_PATH=/workspace/scratch/43b440780c87/playwright-cache /workspace/scratch/43b440780c87/test-env/bin/python evidence/continuation/check.py
```

Use new output names for subsequent runs to retain historical evidence. This local browser/server requires the authorized elevated socket environment described in TOOLING.md.
