# Reconstruct the delivered source workspace

This is a coordinator navigation page for directory links in the original participant report. The original report is retained unchanged in [FINAL.md.txt](FINAL.md.txt). Its linked source directories are:

- `app/wiki`

The complete source is retained through frozen inputs and immutable overlay archives. From the repository root, choose a fresh output directory and run:

```sh
python3 docs/evidence/v1.20.0/session-study/support/continuation/replay_snapshot.py --repo . --cell T3-A-r1 --snapshot-directory docs/evidence/v1.20.0/session-study/runs/T3-A-r1 --output /tmp/ui-spec-T3-A-r1-replay
```

The helper verifies every reconstructed byte and restores recorded file modes. [snapshot.json](snapshot.json) lists all original workspace paths and hashes; [product-evidence.json](product-evidence.json) identifies the required inputs and overlays. Follow the participant preview command in the final report. These directory links are not claims that the small direct-export folder contains the entire application.
