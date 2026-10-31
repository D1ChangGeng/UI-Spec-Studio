# Actual status — adaptive research study

Observed on 2026-11-01 Asia/Tokyo. **The candidate is not released. Fresh independent Codex campaign runs and accepted UI comparisons in this continuation remain 0.**

## Source and engineering progress

Continue from [PR #4](https://github.com/D1ChangGeng/UI-Spec-Studio/pull/4) and `work/v1.20.0-recovery-20261101`; the r2 migration has already been integrated. Do not reapply the development package over this branch.

The immutable `8f3cbef07f526a30fe23bcb5e160342d78d3ff25` snapshot passed [push validation](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/runs/41222879561) and [PR validation](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/runs/41222883976). Each completed seven validation jobs; the Python 3.13 Ubuntu log reports **461 tests / OK**, and Windows reports **461 tests / OK (6 platform-specific skips)**. The separate [recovery run](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/runs/41222879554) passed exact-commit remote installation, live GitHub README rendering, source/distribution capture and runtime-availability reporting. The release job was skipped. The [engineering evidence record](../../evidence/v1.20.0/engineering-8f3cbef.json) preserves run/job identities, read-back source blobs, extracted log results and server-reported artifact digests.

These are engineering, installation and authored-browser-fixture results. Later changes need checks on their own exact commit; neither this snapshot nor the preserved earlier 456-test result certifies untested bytes. See the current PR checks and [review fixes](REVIEW-FIXES-20261101.md).

## Historical activity and current evidence

The [resumption record](RESUMPTION-20261101.md) preserves a historical supplement with four trace-only cells and 19,106 derived action metadata events. That supplement lacks complete raw run ledgers, product outputs, screenshots and matched arms. It cannot establish an accepted campaign or final visual quality. Historical activity is not relabeled as a fresh execution.

Do not count unit-test subprocess doubles, installer checks, code-review agents, the main assistant's review or previous-version media as study participants. No model ranking, UI-quality gain, natural-time motion result, main-context saving or product acceptance is asserted.

## Current execution boundary

The current editing session has no usable local command-execution environment. ACS filesystem access is available, but no eligible online native Harness was observed. The connected browser's policy blocks access to the required Codex host; that path was not bypassed. These observations supersede the initial development session's broad descriptions of connector availability.

The Codex connector's [actual task response](https://github.com/D1ChangGeng/UI-Spec-Studio/pull/4#issuecomment-6545796480) requests an environment for this repository. GitHub code review and CI are available independently; neither supplies an authenticated native study participant with verified browser/tool and role inheritance.

Continue in a provisioned Codex execution environment. Verify native role binding and browser access, freeze the matched inputs and run the registered study. All four roles remain installed by default after an explicit install; actual invocation remains conditional and independently evidenced.

The runner records process start, raw JSONL, runtime identity, wall time and return code only after executing the configured CLI. Exit zero establishes process completion. Inspect the actual candidates, main-agent decisions, mature-source adoption and rendered products before a release decision; missing observations and costs remain unknown.

Conditions and task materials are in [PROTOCOL.md](PROTOCOL.md), [plan.example.json](plan.example.json) and `tasks/`. The example matrix is not an executed registration. Current observations and the preserved initial report are in [execution-status.json](execution-status.json).
