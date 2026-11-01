# v1.20.0 evidence delivery and reconstruction

## Delivery scope

This directory retains the owner-authorized study using actual independent session agents. [The live inventory](README.md) identifies which registered cells currently have complete retained records. [The release decision](../release-decision.json) is the authority for whether final acceptance has been recorded; a reconstruction success is an integrity result, not a product-quality judgment.

The complete candidate fingerprint is `eb7752a1b0eb4af180e9bb4bd0922587a3c9c96744e24ec8cf299517516e8759`. The unchanged [registration](registration.json) has SHA-256 `3072de1df10611c922273e62ae3c6e66dfd2790627727e265410075b1ee43ab6`. It freezes all 18 task/condition cells, complete input file maps, methods, role instructions, exact primary prompts and declared execution conditions.

| Material | Where to begin | What it establishes |
| --- | --- | --- |
| Frozen experiment inputs | `registration.json`, `inputs/`, `prompts/` | Exact source bytes supplied to each independent primary. |
| Actual participation | Each `runs/*/run.json` and its referenced coordination exports | Original dispatch identities, completed children, retained work and the actual declared model requests. |
| Runnable products | Each `snapshot.json`, input ZIPs and workspace-overlay archives | Complete included workspace files, original names, byte hashes and recorded modes. Dependency caches and external runtime are separately scoped. |
| Product images and behavior | Each `product-evidence.json` | Original PNG captures, actual view exports and command outputs. Capture, viewing, exercised behavior and quality judgment remain distinct. |
| Product reasoning | Each `FINAL.md.txt`, `VISUAL-REVIEW.md.txt` and original workspace archives | The participant's original reports. `FINAL.md` is a labeled repository-navigation copy. |
| Independent review | [Review index](review/README.md) and `review/recovered-reviewer/` | Immutable anonymous judgments, original viewing/behavior evidence and full reviewer-workspace reconstruction. |
| Engineering checks | [Engineering index](engineering/index.json), `engineering/commands/`, `engineering/recovery-0830/` | Exact tested candidate, stdout/stderr, browser-fixture evidence, failures and successful follow-ups. |
| Recovery history | `incomplete-attempts/`, `coordination/recovery-0830/` | Surviving originals and explicitly unavailable attempts. These do not silently increase completed-run coverage. |

The complete source release archive includes these public files. The small portable Skill and standalone adapter archives serve installation; they do not contain the experiment corpus.

## Reconstruct an ordinary completed product

Run from the repository root or the extracted complete source archive. Choose a fresh output directory:

```sh
python3 docs/evidence/v1.20.0/session-study/support/continuation/replay_snapshot.py \
  --repo . \
  --cell T1-G-final-runtime-r1 \
  --output /tmp/ui-spec-replay-T1-G
```

The helper verifies the frozen inputs and overlay archives, restores the recorded paths and modes, applies the actual deletions, and checks every resulting file against the final snapshot. Follow that product's retained preview command from the reconstructed workspace. Replace the original absolute work-package prefix with the chosen output directory; the original reports deliberately preserve their historical paths.

Some records use an explicitly named snapshot directory. For the bounded integrator:

```sh
python3 docs/evidence/v1.20.0/session-study/support/continuation/replay_snapshot.py \
  --repo . \
  --cell T4-F-integrator-r1 \
  --snapshot-directory docs/evidence/v1.20.0/session-study/runs/T4-F-integrator-r1-recovery \
  --output /tmp/ui-spec-replay-T4-integrator
```

The per-product reconstruction page and run record identify the exact current directory. Do not infer a current run from an older completion message or a similarly named partial attempt.

## T2-G: public projection and private original network records

The T2-G research captured anonymous session-bearing values in public-page HTTP responses. Their public delivery is an explicit projection. Application source, method/role inputs, PNGs, image-tool returns and unaffected records remain unchanged. Exactly 314 network JSON/body files have declared value substitutions; no redacted network record is called an unchanged original.

Reconstruct the public workspace:

```sh
python3 docs/evidence/v1.20.0/session-study/support/continuation/replay_snapshot.py \
  --repo . \
  --cell T2-G-final-runtime-r1 \
  --snapshot-directory docs/evidence/v1.20.0/session-study/runs/T2-G-final-runtime-r1-public \
  --output /tmp/ui-spec-replay-T2-G-public
```

The repository owner received `T2-G-original-network-evidence-private.zip` separately through a private file delivery. Its SHA-256 is `24fce5f54c8e14fd6a271980b849dc95a1212cd169f2a9650abbedb5edd8dfb2`, and its size is 640,430 bytes. It contains the 314 unchanged original network files, a full original-workspace hash inventory and a readme.

To restore into a fresh private directory:

```sh
python3 docs/evidence/v1.20.0/session-study/support/recovery/restore_private_originals.py \
  --public-workspace /tmp/ui-spec-replay-T2-G-public \
  --private-archive /path/to/T2-G-original-network-evidence-private.zip \
  --output /tmp/ui-spec-replay-T2-G-original
```

The [complete-originals audit](engineering/recovery-0830/T2-G-complete-originals-reconstruction.json) verified all 1,931 original files: 1,617 unchanged public files plus 314 privately retained originals. The helper verifies the same original hashes and does not print session values. [The projection manifest](coordination/recovery-0830/T2-G-privacy-projection.json) records the precise relationship. Public consumers can reproduce the product without those session values; access to the complete unchanged network originals remains private.

## Reconstruct independent review evidence

The latest frozen review snapshot points to its prior immutable snapshot. Hash/member inventories may be split into small verified JSON parts; every entry remains available.

For the two currently frozen recovery cohorts:

```sh
python3 docs/evidence/v1.20.0/session-study/support/continuation/replay_review.py \
  --repo . \
  --snapshot docs/evidence/v1.20.0/session-study/review/recovered-reviewer/cohort-02/snapshot.json \
  --output /tmp/ui-spec-independent-review
```

This reconstruction verified all 46,071 files, including exercised reviewer application copies. The cumulative correspondence links 13 products and 45 original-capture view exports. Additional reviewer captures and unsuccessful probes remain separately retained. Later cohorts and final-runtime disposition will be linked from the review index without rewriting the earlier blind judgments.

## Interpretation and unavailable evidence

These are actual independent session executions with simulated native-role instructions. The host does not authenticate native Codex role binding, resolved backend model/effort identity, native token use, billing or main-context pressure. Their unavailable values remain null. Shared-host instructional isolation is weaker than separate security sandboxes, and this independent agent review is not a human usability panel.

The frozen 30-minute substantive bound is distinct from the coordinator's dispatch-to-export interval. Capacity waits can include ongoing primary work, and delivery latency is not measured engine time. Actual attempt logs and timing qualifications are retained rather than normalized into invented efficiency figures.

Historical unavailable native archives and interrupted workspaces remain explicitly unavailable. The later T3-C 09:56 execution retains 36 surviving original exports and its actual completion notification, but its missing application and command records are not reconstructed or counted as complete. A new execution must use fresh frozen inputs.

The later T3-G 10:50 attempt has a different status: its complete 9,233-file original workspace is retained and reconstructable, but the product task remained incomplete after a 1,309.5-second image-view call stall. Its [preservation page](incomplete-attempts/T3-G-final-runtime-r1-interrupted-1050/README.md) gives the reconstruction command. Actual unsuccessful work is retained without being counted as a completed product. A fresh execution and its explicit physical-path mapping are separately recorded. This public/private delivery describes what is actually retained; it does not turn missing history or unfinished work into completed original evidence.
