# Reproduce and inspect the campaign

The registered briefs, complete skill revisions, assignment, runtime lock and review rubric define the comparison. Each frozen application is preserved with its own build, source notices, command records and self-check evidence. Independent acceptance results and temporal captures are a separate evidence layer. A model's own checklist is never substituted for the independent result.

## Open a frozen output

Archives are split into byte-aligned parts to fit the publication transport. Each run's `archives/<run-id>.manifest.json` gives the ordered parts, exact sizes, SHA-256 hashes and the complete archive hash. Concatenate the listed parts in that order, verify the archive SHA-256, then extract the resulting `.tar.gz` into a new directory. Do not extract over a working project. The manifest also identifies original absolute `node_modules` links that were intentionally omitted from extraction.

The extracted layout contains:

- `frozen/FROZEN.json`: file identities, scope and immutable-input checks at the participant's final state.
- `frozen/app/`: the unmodified application, its original evidence and already built `dist/`.
- `independent-evaluation/`: the common acceptance observations, screenshots, continuous video and timestamped samples, plus asset/network diagnostics.

Serve `frozen/app/dist/` through a local HTTP server to inspect the captured product. A service backend or external account is not needed. The behavior is supplied by each task's immutable local fixture. Original retained paths in command logs identify the host used for the actual run; they are historical facts, not portable commands.

## Re-run the common checks

Create a separate runtime directory, place `runtime-package-lock.json` there as `package-lock.json`, recover its root `packages[""].dependencies` into a matching `package.json`, and run `npm ci`. The lock pins Playwright1.51.1 and the application dependencies. The observed browser was Chromium134.0.6998.35, Playwright build1161, headless atDPR1. Install the matching browser with the pinned Playwright package if it is not already available.

Set `UI_EVAL_RUNTIME` to that runtime directory and `UI_EVAL_CHROMIUM` to the matching Chromium executable. Then run:

```sh
node evaluate.mjs /absolute/path/to/frozen/app T1 /absolute/path/to/new-observations
node temporal.mjs /absolute/path/to/frozen/app T1 /absolute/path/to/new-observations/temporal
node diagnostics.mjs /absolute/path/to/frozen/app T1 /absolute/path/to/new-observations/diagnostics
```

Use the run's actual family, `T1`, `T2` or `T3`. Keep `fixtures/` beside these evaluation scripts. The first script exercises the ten registered acceptance groups; the second records a short natural-clock scripted episode with timestamped image samples; the third checks external asset dependency and requested resource sizes. Sample capture changes timing, so these recordings do not establish FPS or device performance. A fresh output folder preserves the original observations.

To rebuild an application, create its `node_modules` link to the separate runtime, retain any locally vendored dependencies and their notices, and use the application's own package scripts. Do not install into the shared runtime while reproducing a particular application. Source-specific dependencies and patches are documented in the original handover and command records.

## Evidence and interpretation

`PROTOCOL.md` records the pre-execution question, treatment and inference limits. Harness corrections preserve the original affected observations and identify changes to evaluator setup. A correction to the test runner does not authorize repairing a frozen application. Anonymous review scores are ordinal and stay separate from functional group outcomes. No numerical aesthetic total is defined.

The archive preserves captured original-demo evidence and model-authored viewing attestations. It cannot supply a full tool/conversation export that this harness did not expose. A retained screenshot proves capture; a viewing claim remains a claim unless directly evidenced. No participant had access to the hidden comparison rubric or other outputs by instruction; filesystem separation was not an operating-system security boundary.
