# T3: independent product-output review

The original anonymous report was frozen before its condition map was published.
Application source matches every file in [the input identity](input-identities.json).
This is an Agent review of sampled operation and rendered pixels, not owner acceptance.

- [Original report, exact text](original/REVIEW.md.original.txt)
- [Structured original findings](original/review.json)
- [Original evidence index and hashes](archive-index.json)
- [Post-freeze condition map](unblinding.json)
- [Balanced study gallery](../../GALLERY.md)

All original captures and failures remain in the indexed bundles. Restore them with
`tools/replay_granularity_run.py` using this review directory and a new destination;
the default final stage restores the review files. Original host paths in scripts
remain provenance and need deliberate environment adaptation for a new run.
