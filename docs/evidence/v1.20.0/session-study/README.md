# v1.20.0 session study evidence

This is a derived navigation index. Actual independent agents perform the work;
the unavailable native Codex role environment is simulated. The repository owner
[explicitly authorized this substitute](owner-authorization.json). Read the
[acceptance contract](../../../experiments/adaptive-research/SESSION-SIMULATION.md)
for the boundary. Native role binding, resolved models/effort, tokens, billing,
context pressure and a human acceptance panel remain unverified.

## Execution inventory

6 of 18 registered primary executions currently have completed
records, with 3 completed child records. This count is execution coverage,
not a product-quality score or release status. Independent review and the final
release decision have their own records. Every planned cell remains visible.

| Cell | Condition | Retained status | Completed children |
| --- | --- | --- | ---: |
| T1-A-r1 | A | [Completed record](runs/T1-A-r1/run.json) · [product](runs/T1-A-r1/FINAL.md) | 0 |
| T1-B-r1 | B | [Completed record](runs/T1-B-r1/run.json) · [product](runs/T1-B-r1/FINAL.md) | 1 |
| T1-C-r1 | C | [Completed record](runs/T1-C-r1/run.json) · [product](runs/T1-C-r1/FINAL.md) | 1 |
| T1-G-final-runtime-r1 | G-final-runtime | Not dispatched | — |
| T2-A-r1 | A | [Completed record](runs/T2-A-r1/run.json) · [product](runs/T2-A-r1/FINAL.md) | 0 |
| T2-B-r1 | B | [Completed record](runs/T2-B-r1/run.json) · [product](runs/T2-B-r1/FINAL.md) | 1 |
| T2-C-r1 | C | Dispatched; no retained final completion yet | Pending completion |
| T2-G-final-runtime-r1 | G-final-runtime | Not dispatched | — |
| T3-A-r1 | A | Dispatched; no retained final completion yet | Pending completion |
| T3-B-r1 | B | Dispatched; no retained final completion yet | Pending completion |
| T3-C-r1 | C | Not dispatched | — |
| T3-G-final-runtime-r1 | G-final-runtime | Not dispatched | — |
| T2-D-r1 | D | Not dispatched | — |
| T2-E-challenger-r1 | E-challenger | Not dispatched | — |
| T2-E-observer-r1 | E-observer | Not dispatched | — |
| T4-F-main-r1 | F-main | [Completed record](runs/T4-F-main-r1/run.json) · [product](runs/T4-F-main-r1/FINAL.md) | 0 |
| T4-F-integrator-r1 | F-integrator | Not dispatched | — |
| T4-G-final-runtime-r1 | G-final-runtime | Not dispatched | — |

## What is retained

- [Frozen registration](registration.json), exact dispatched primary prompts,
  original task/application/method/role input archives and [environment](environment.json).
- Each completed run's original delivered source, reports, command output,
  actual retained tool returns, PNGs, failed attempts and corrections. Complete
  workspace hashes and modes are in `snapshot.json`; input plus every overlay
  ZIP reconstruct the captured workspace. `reconstruction-check/` retains the
  actual byte comparison result.
- The primary's actual image-view exports and an explicit final-product image
  index. Capturing an image does not establish that anyone viewed it. Capture
  lineage distinguishes earlier unchanged layouts from later affected states.
- Spawn and final-notification exports under `coordination/`. These are faithful
  available conversation exports, not fabricated native engine events. Derived
  audits are labeled separately. The T1-C and T2-B prompt audits retain their one-final-LF
  difference; substantive prompt and role bytes were not silently altered.
- [Engineering evidence](engineering/index.json), including original failures,
  source checks, browser observations and the narrowly scoped installation test.

Original Markdown report bytes are retained as `.md.txt` exports and inside the
immutable workspace ZIPs. Each `FINAL.md` is explicitly a derived repository
navigation copy whose local link destinations are adapted. The first evidence
checkpoint's CI/local link-check failure and the successful packaging correction
remain retained; no frozen candidate code or validator was changed for that fix. The first failed
standalone harness is likewise retained byte for byte as `.py.txt` data, so its
real SyntaxError is not misclassified as executable distribution source. The
failed and corrected packaging checks remain in the engineering record.

The available export boundary excludes hidden reasoning, an inaccessible native
engine transcript, unrelated session data, dependency caches, and external
browser/Python/font binaries. Their relevant identities and exclusions are
documented. No unavailable metric is inferred from duration or tool counts.

## Reconstruct a completed product

From the source repository or extracted source distribution, choose a completed
cell and a new output directory:

```sh
python3 docs/evidence/v1.20.0/session-study/support/continuation/replay_snapshot.py \
  --repo . --cell T1-A-r1 --output /tmp/ui-spec-T1-A-replay
```

The helper verifies all reconstructed file bytes against the snapshot and
restores the recorded modes. Follow that product's retained preview command.
T1/T4 use a static server. T2 retains built `app/dist` as well as source and the
dependency lockfile; the dependency cache is excluded. T3 retains its complete
native wiki foundation and startup script. Use a disposable copy for tests that
change wiki files and a fresh browser context for browser-local persistence.

The coordinator helpers document evidence handling; they are not a substitute
for rerunning independent agents or reproducing a resolved native model.

## Continuation and retained incomplete attempts

The next coordinator recovered the original worksets and the same pinned browser, Python and CJK font. All eleven previously untouched worksets matched the frozen input hashes. The local five-product checkpoint was saved to GitHub as `a729b667882daf1810c3c914f8d7c045bbaa6670`, with the identical source tree.

T2-C and T3-A had delivered files but no available primary terminal-notification export. Their complete observed workspaces are retained under `incomplete-attempts/`, with original coordination, explicit status, reports, all captured files and successful byte-for-byte reconstruction checks (377 and 9,526 files). They are not counted as completed experiments. Their original live directories were preserved separately and the registered paths restored from unchanged frozen inputs for new independent attempts. The continuation replay helper supports oversized original trace files through verified byte pieces; no trace content was discarded.

The continuation parameterized coordinator helpers are in `support/continuation/`; candidate runtime, tests, installed Skill, adapter and frozen registration remain unchanged.
