#!/usr/bin/env python3
"""Write a navigable, explicitly derived index over actual retained records."""
from pathlib import Path
import argparse, json

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);a=p.parse_args()
    study=a.repo/'docs/evidence/v1.20.0/session-study';plan=json.loads((study/'registration.json').read_text())
    rows=[];done=0;children=0
    for cell in plan['cells']:
        name=cell['id'];runpath=study/'runs'/name/'run.json'
        if runpath.exists():
            run=json.loads(runpath.read_text());done+=1;children+=len(run['children'])
            state=f"[Completed record](runs/{name}/run.json) · [product](runs/{name}/FINAL.md)";count=str(len(run['children']))
        elif (study/'coordination'/f'{name}-completion.json').exists():state='Actual completion received; indexing pending';count='Pending index'
        elif (study/'coordination'/f'{name}-spawn.json').exists():state='Dispatched; no retained final completion yet';count='Pending completion'
        else:state='Not dispatched';count='—'
        rows.append(f"| {name} | {cell['condition']} | {state} | {count} |")
    text=f'''# v1.20.0 session study evidence

This is a derived navigation index. Actual independent agents perform the work;
the unavailable native Codex role environment is simulated. The repository owner
[explicitly authorized this substitute](owner-authorization.json). Read the
[acceptance contract](../../../experiments/adaptive-research/SESSION-SIMULATION.md)
for the boundary. Native role binding, resolved models/effort, tokens, billing,
context pressure and a human acceptance panel remain unverified.

## Execution inventory

{done} of {len(plan['cells'])} registered primary executions currently have completed
records, with {children} completed child records. This count is execution coverage,
not a product-quality score or release status. Independent review and the final
release decision have their own records. Every planned cell remains visible.

| Cell | Condition | Retained status | Completed children |
| --- | --- | --- | ---: |
'''+ '\n'.join(rows)+'''

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
  audits are labeled separately. The T1-C prompt audit retains its one-final-LF
  difference; substantive prompt and role bytes were not silently altered.
- [Engineering evidence](engineering/index.json), including original failures,
  source checks, browser observations and the narrowly scoped installation test.

Original Markdown report bytes are retained as `.md.txt` exports and inside the
immutable workspace ZIPs. Each `FINAL.md` is explicitly a derived repository
navigation copy whose local link destinations are adapted. The first evidence
checkpoint's CI/local link-check failure and the successful packaging correction
remain retained; no frozen candidate code or validator was changed for that fix.

The available export boundary excludes hidden reasoning, an inaccessible native
engine transcript, unrelated session data, dependency caches, and external
browser/Python/font binaries. Their relevant identities and exclusions are
documented. No unavailable metric is inferred from duration or tool counts.

## Reconstruct a completed product

From the source repository or extracted source distribution, choose a completed
cell and a new output directory:

```sh
python3 docs/evidence/v1.20.0/session-study/support/replay_snapshot.py \\
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
'''
    (study/'README.md').write_text(text)
    print(json.dumps({'indexed_cells':done,'completed_children':children,'planned_cells':len(plan['cells'])}))
if __name__=='__main__':main()
