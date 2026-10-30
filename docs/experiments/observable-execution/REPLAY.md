# Replay the actual study artifacts

The run archives preserve applications, exact outward message files and the source
available at each message. They are experimental outputs with their observed gaps;
freezing or packaging them does not certify product quality.

## Restore an application

From the full source distribution or this repository:

```bash
python tools/replay_granularity_run.py docs/experiments/observable-execution/runs/T1-k2 /tmp/index-k2
cd /tmp/index-k2/app
npm ci
npm run dev -- --host 127.0.0.1 --port 8080
```

The replay tool verifies every original application file before writing into a
new destination. `--stage initial` restores the corresponding starter. Select a
different published run directory to inspect another cell. T1 uses the preserved
lockfile and Node 24; its optional mature candidates retain the original Magic UI
MIT license in each T1 run and in `t1-input.zip`. Retain that notice with derivative
copies. Installing dependencies requires network access.

T2 and T3 are browser-native fixtures. After restoring their snapshot:

```bash
python -m http.server 8080 --bind 127.0.0.1 --directory /tmp/fieldnote-copy/app
```

Open `http://127.0.0.1:8080`. Use a fresh browser profile or clear only this local
origin when comparing runs; otherwise retained browser data can change a state.
The applications remain local examples, not deployed products or production data.

## Inspect what was actually shown

`outward/message-NNN.json` preserves the exact text, channel, recorder timestamp
and original source hashes. Its adjacent source ZIP is the application at that
moment. `received-relays.jsonl` identifies messages actually relayed to the
coordinator. A few early receipts omit a terminal newline in displayed text;
`relay-text-comparison.json` retains that distinction. No retrospective message
has been inserted to fill a missing event. The unrecorded startup reported in
T3-s8 is identified as a later participant report.

The `sandbox:` references inside original messages identify the execution
workspace and are intentionally not rewritten as if they had been different
messages. To inspect their media now, extract `participant-evidence*.zip` (all
parts when split); its
member paths and SHA-256 values are listed in `archive-index.json`. Scripts,
measurements, failed checks and original captures remain available. Other authored
notes are preserved in `participant-notes.zip`. Capture alone is not evidence
that every frame or every natural-speed episode was actually viewed.

The original recorder did not snapshot referenced media at emission. In C/T1,
`message-004` points to a generic image later overwritten during palette repair.
Current archived pixels must not be treated as immutable early pixels. See the
[specific limitation and recorder correction](INSTRUMENTATION.md). The original
messages and common input recorder remain unchanged.

## Inspect the separate correction

`continuations/T2-k2/` preserves an additional, non-comparative correction after
independent feedback. Its `app-initial.zip` is the exact original C endpoint;
`app-final.zip` is the repaired application. Extract either archive into a new
directory and run the browser-native application with the HTTP command above.
`archive-index.json` identifies every member and hash; `validation.json` records
the completed independent archive readback. Outward media ZIPs preserve the
referenced images using the recorder actually supplied to this continuation.

The [continuation report](CONTINUATION.md) explains the additional time, specific
repair, separate independent operation and remaining limits. It is not a replacement
for the original C application or an additional original comparison cell.

## Method and environment

`inputs/runtime-s8.zip`, `runtime-v5.zip` and `runtime-k2.zip` contain the full
supplied methods, with hashes in `registration.json`. C matches the published
37-file runtime. B is the visibility comparison, with one additional experimental
reference; it is not the released standalone Skill.

`TASK.md` and `ENVIRONMENT.md` in each run preserve the actual task and host setup.
The common task dispatcher additionally specified the work directory, local port,
Chinese output, no subdelegation and a nominal maximum window (T1: 24 minutes;
T2: 18; T3: 10). The original task dispatch is not reconstructed as an exact
transcript where it was not separately archived. First/last recorded message
times establish a communication span, not the full agent execution time.

All cells share the same task family inputs, node dependency lock, browser and
guidance text. Local operation used Chrome for Testing 156 and Playwright 1.57;
the release CI's bundled Chromium version is a separate environment. See
`environment.json`, the common-input README and the explicit registration
correction for their provenance and limits.

Independent product review uses frozen anonymous copies before method labels and
participant prose are revealed. Its observations are separate from participant
claims and from source-integrity tests. This is one execution per cell with shared
host load, common reporting overhead and rolling starts. It cannot establish a
population-wide visual-quality improvement or isolate every causal factor.
