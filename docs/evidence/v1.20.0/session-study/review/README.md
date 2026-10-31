# Independent product review — in progress

The actual independent reviewer `/root/independent_product_reviewer` began in a fresh context with anonymous frozen products, their tasks and mature foundations. Condition labels, method files and producer judgments were withheld. Isolation is instructional on a shared host. This is an independent Agent judgment, not a human usability panel or native Codex validation.

## Frozen first cohort

The first cohort contains P03, P06, P09, P10 and P16. Its original judgments are immutable. Later products and any final-runtime acceptance will have separate records; this checkpoint does not approve the release.

| Anonymous product | Scoped independent finding |
| --- | --- |
| P03 | Exercised settings behavior and long bilingual values supported; some narrow navigation inefficiency remains. |
| P06 | Exercised settings behavior and narrow hierarchy supported; newer unsaved edits receive less visual emphasis than in P03. |
| P16 | Core save/recovery behavior supported; full narrow and long-value requirements remain deficient. |
| P09 | Exercised composer, attachment disclosure and reading continuity supported; additional attachments require internal scrolling. |
| P10 | Full task scope unsupported as delivered: streaming return-to-latest and narrow outer overflow defects are confirmed; immediate stop-text stability remains unresolved. |

Read the [complete original cohort report](cohort-01/raw/BLIND-REVIEW-2026-10-31-cohort-01.md.txt), [structured product records](cohort-01/raw/products-cohort-01.json), [reviewer freeze](cohort-01/raw/cohort-01-FREEZE.json) and [actual final notification](../coordination/current-independent-review-cohort-01-completion.json). Original Markdown bytes are exported as `.md.txt` data; the archives preserve their original names and contents.

The reviewer personally viewed 30 original product PNGs and separately captured and viewed targeted interactions. The review retains its failed assistant-text selector measurement and corrected follow-up. These records preserve both negative product results and reviewer measurement failures.

Representative corroborating captures:

- [P10 after return-to-latest while streaming](cohort-01/raw/evidence/behavior-003/P10-return-latest-after-2550ms.png).
- [P10 after a horizontal wheel gesture in the narrow reading area](cohort-01/raw/evidence/behavior-003/P10-narrow-after-reading-horizontal-wheel.png).
- [P09 under the comparable return-to-latest observation](cohort-01/raw/evidence/behavior-003/P09-return-latest-after-2550ms.png).
- [P16 long bilingual values in the narrow layout](cohort-01/raw/evidence/behavior-001/P16-narrow-dark-zh-long-top.png).

## Original evidence and reconstruction

The [cohort snapshot](cohort-01/snapshot.json) identifies all 258 retained files, their SHA-256 values, exact available tool outputs, source scripts, command captures, screenshots and traces. Its archive reconstruction [passed](cohort-01/reconstruction-check/stdout.txt) for every original file. Disposable application copies are excluded because their unchanged frozen sources remain in the product snapshots; no browser profiles, credentials or hidden reasoning are included.

From the repository or extracted full source distribution:

```sh
python3 docs/evidence/v1.20.0/session-study/support/continuation/replay_review.py \
  --repo . \
  --snapshot docs/evidence/v1.20.0/session-study/review/cohort-01/snapshot.json \
  --output /tmp/ui-spec-review-cohort-01
```

This verifies the delivered bytes. It does not rerun the reviewer or certify UI quality.
