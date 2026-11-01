# Final reviewer evidence handoff

The [core reviewer index](indexed-core/review.json) contains the sixteen original
products, seventy-four actual original image-view exports and the reviewer's final
`accept_limited` judgment. The two supplementary replacement products remain
separate in [supplementary-evidence.json](supplementary-evidence.json), pointing to
the unchanged supplementary report, records and view export inventory. They were
not rebound into the original registration.

Reviewer-authored fields are preserved: `condition_blind=false`,
`reviewed_at=2026-11-01T13:31:03.329069+00:00`, all four final-runtime cells have
`accepted_with_limits`, and no product was repaired. Accepted subsets and exclusions
remain exactly as authored, including the unresolved horizontal keyboard-table
scope. FINAL SHA-256 is
`26db378718dd0f7b36ade2a4238558a06947d6045fd4e2a33a6a9850a72fcae0`.
The original declaration SHA-256 is
`46a7964cb188d704932108513b3bce163beaa5ee600c96abe003278b2a8aa234`.

## Explicit schema projection

[declaration-projection.json](indexed-core/declaration-projection.json) records
all seventeen deterministic transformations with original and projected values.
Twelve ordered text lists are joined with a single newline: top-level scope and
limitations, final-runtime scope and limitations, and scope/limitations for each
of four per-cell declarations. Every original string remains in order.

Five no-repair verification lists are mapped to retained byte REFs: 28 top-level
final-runtime items and 6, 7, 8 and 8 per-cell items, totaling 57 entries. Every
original `kind` and absolute source path is preserved alongside the repository REF.
These are actual verification supporting the reviewer's no-repair disposition,
not product repairs. The original declaration remains byte-identical in the
[snapshot raw export](cohort-01/raw/REVIEW-DECLARATION.json) and is embedded unchanged
in the core index. Original product findings records are also retained; their
structured findings are serialized without content rewriting for the schema field.

## Preservation and proofs

The [snapshot](cohort-01/snapshot.json) retains 162,727 eligible files, representing
845,925,163 bytes. Of these, 162,185 byte-identical files reuse existing immutable
product snapshots; 542 other reviewer files are archived. All owned stateful test
copies are preserved, including any directory named `disposable`. Actual dependency,
git, bytecode and pytest caches are excluded. The one old supplied-input review-pack
symlink is recorded literally without traversal and restored with its exact target;
original products and PNGs remain independently retained through their frozen records.

- [Full reconstruction command](reconstruction-check/command.json) and
  [original stdout](reconstruction-check/stdout.txt): all 162,727 files match and
  the literal symlink target is restored after byte checks.
- [Consistency command](consistency-check/command.json) and
  [original stdout](consistency-check/stdout.txt): participant/view/reference checks
  pass for sixteen core products, two separate supplementary rows and 186 repository
  REFs. Eligible source inventory matches the frozen snapshot; every text/list and
  verification-REF projection matches the original declaration.
- [Frozen cohort readback](frozen-cohort-readback.json): all twelve files named in
  the initial, supplementary and final reviewer freeze manifests remain unchanged.
- [Index command](index-command/command.json) retains actual index stdout/stderr.

The final condition-disclosure follow-up and terminal completion remain exact
coordination exports under `continuation-2100/coordination/`. No reviewer judgment,
product, runtime, strict checker, release decision, commit or remote action was
changed by this preservation work. Final release/engineering acceptance remains
the coordinator's separate responsibility.
