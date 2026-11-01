# Reconstruct the delivered workspace

This coordinator navigation page supplements the unchanged [primary report](FINAL.md.txt). The recorded source and all retained evidence are reconstructed from the registered inputs and immutable overlay archives. From the repository root, choose a fresh output directory and run:

```sh
python3 docs/evidence/v1.20.0/session-study/support/continuation/replay_snapshot.py --repo . --cell T4-F-integrator-r1 --snapshot-directory docs/evidence/v1.20.0/session-study/runs/T4-F-integrator-r1-recovery --output /tmp/ui-spec-T4-F-integrator-r1-public
```

The helper verifies every published workspace byte. [snapshot.json](snapshot.json) records source identities and exclusions; [product-evidence.json](product-evidence.json) links the exact input/overlay archives, original product captures and actual viewing exports. Follow the participant's preview command from the reconstructed workspace.
