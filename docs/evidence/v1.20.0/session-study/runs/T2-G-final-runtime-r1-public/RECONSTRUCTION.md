# Reconstruct the delivered workspace

This coordinator navigation page supplements the unchanged [primary report](FINAL.md.txt). The recorded source and all retained evidence are reconstructed from the registered inputs and immutable overlay archives. From the repository root, choose a fresh output directory and run:

```sh
python3 docs/evidence/v1.20.0/session-study/support/continuation/replay_snapshot.py --repo . --cell T2-G-final-runtime-r1 --snapshot-directory docs/evidence/v1.20.0/session-study/runs/T2-G-final-runtime-r1-public --output /tmp/ui-spec-T2-G-final-runtime-r1-public
```

The helper verifies every published workspace byte. [snapshot.json](snapshot.json) records source identities and exclusions; [product-evidence.json](product-evidence.json) links the exact input/overlay archives, original product captures and actual viewing exports. Follow the participant's preview command from the reconstructed workspace.

## Private original network records

The application, frozen method/roles, screenshots, actual image returns, reports and unaffected evidence are unchanged original bytes. A [declared privacy projection](../../coordination/recovery-0830/T2-G-privacy-projection.json) replaces session-bearing values in 314 captured network metadata/body files. The unchanged affected originals are separately delivered to the repository owner in `T2-G-original-network-evidence-private.zip` (SHA-256 `24fce5f54c8e14fd6a271980b849dc95a1212cd169f2a9650abbedb5edd8dfb2`). They are excluded from public GitHub distribution.

With that private ZIP, verify the complete original workspace without writing or printing session values:

```sh
python3 docs/evidence/v1.20.0/session-study/support/recovery/restore_private_originals.py --public-workspace /tmp/ui-spec-T2-G-final-runtime-r1-public --private-archive /private/path/T2-G-original-network-evidence-private.zip
```

Add `--output /private/fresh-directory` only when an actual private reconstruction is needed. The [original reconstruction audit](../../engineering/recovery-0830/T2-G-complete-originals-reconstruction.json) verifies all 1,931 original files: 1,617 public originals plus 314 private originals. The public projection is never described as an unmodified raw network return.
