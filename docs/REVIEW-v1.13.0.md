# UI Spec Studio v1.13.0 — historical content integrity audit

## Answer and scope

**A real compression incentive existed, and some consequential instruction
specificity was weakened.** This review does not equate a falling byte count
with a lost capability, nor does it treat a retained heading or keyword as
proof that the associated skill survived. It compares released files and
restores concrete rules within the installed references while preserving
subsequent correct design developments.

The measurable history uses the available public release tags **v1.1.0 through
v1.12.1**. The changelog describes an earlier locally delivered v1.0.0, but
a public v1.0.0 Git tag was not retrievable for this audit. Thus v1.1.0 is the
first tag used for source comparisons, not a claim about the original design's
entire pre-release history.

Source inspection focused on changes in the eight professional references,
especially **v1.4–v1.6**, **v1.6–v1.7** and **v1.11–v1.12**. The [lineage
ledger](evidence/v1.13.0/lineage.json) identifies exact historical tags, source
sections, detailed reinstatements and the resulting installed paths. The
[permanent procedure](CONTENT-INTEGRITY.md) defines how subsequent revisions
must review their own deltas. No claim is made that every prose sentence of
every historic commit has undergone human semantic certification.

## Byte-level history

Numbers below are bytes in the tagged repository's skill directory and its
then-required six, seven or eight common reference files. The comparison is
between actual Git trees, not normalized or shortened summaries.

| Tag | Required references | References (bytes) | SKILL.md (bytes) | Entire skill (bytes) |
|---|---:|---:|---:|---:|
| v1.1.0 | 6 | 43,710 | 8,795 | 87,918 |
| v1.2.0 | 6 | 67,006 | 10,501 | 122,790 |
| v1.3.0 | 6 | 75,933 | 11,900 | 209,576 |
| v1.4.0 | 6 | 96,368 | 15,278 | 239,901 |
| v1.5.0 | 7 | 118,045 | 16,635 | 274,642 |
| v1.6.0 | 8 | 146,333 | 19,209 | 322,212 |
| v1.7.0 | 8 | 142,429 | 21,157 | 323,438 |
| v1.8.0 | 8 | 145,011 | 21,425 | 330,111 |
| v1.9.0 | 8 | 143,387 | 22,543 | 332,839 |
| v1.10.0 | 8 | 145,332 | 23,329 | 337,769 |
| v1.11.0 | 8 | 145,472 | 23,883 | 345,161 |
| v1.12.0 | 8 | 146,719 | 27,786 | 353,835 |
| v1.12.1 | 8 | 146,719 | 27,786 | 353,835 |

This gives a more precise explanation than “the Skill kept getting shorter”.
The full package and entry generally **grew**. However the required
professional references nearly stopped growing after v1.6.0 despite new
methods. Individual files contracted during expansion: from v1.6.0 to
v1.12.1, workflow fell 15,264 → 11,344 bytes; component sourcing
17,102 → 18,373, after intermediate expansion; interaction 17,531 →
15,275. The total common reference content remained between 142,429 and
146,719 bytes from v1.6.0 onwards.

More importantly, [v1.5.0's test](https://github.com/D1ChangGeng/UI-Spec-Studio/blob/v1.5.0/tests/test_publication.py)
set **128 KiB** as a hard aggregate requirement. [v1.6.0's test](https://github.com/D1ChangGeng/UI-Spec-Studio/blob/v1.6.0/tests/test_publication.py)
raised this to **144 KiB** after adding a reference. The [v1.12.1
test](https://github.com/D1ChangGeng/UI-Spec-Studio/blob/v1.12.1/tests/test_publication.py)
still enforced it. Later [maintainer instructions](https://github.com/D1ChangGeng/UI-Spec-Studio/blob/v1.12.1/AGENTS.md)
repeatedly reinforced that budget. This is a documented cause of sustained
pressure to shorten the very files intended to accumulate professional
knowledge. It does not establish the author's motivation for any particular
deleted line.

## What changed in substantive capability

The high-risk comparisons were made at the level of a working decision, its
scope, execution conditions and how an agent could verify the outcome.

| Historical source | Observed weakness by v1.12.1 | Restored responsibility |
|---|---|---|
| v1.1–v1.6 analysis: *Lead users with different levels of direction* | Named subsection disappeared; general initiative survived, but goal-only, partial and detailed-brief distinctions were less explicit | Analysis now directly explains those three levels, binding references, low-impact decisions and when a material user choice is needed |
| v1.5 principles: *A positive craft target* | Retained craft language was more abstract about how to intensify/quiet a design without losing its core idea | Principles restores a positive, inspectable outcome, identity-bearing priority and controlled expressive refinement |
| v1.5 principles: external strengths, interaction model and mature inheritance | Several linked, concrete source-to-composition mechanisms were collapsed into one short craft section | Principles restores semantic/visual ownership, composition conflicts, typography dependencies and assembled-frame checks |
| v1.6 workflow: *init* and *iterate* | Stages remained but detailed project inventory, realistic copy extremes, selected source settings and assembled verification weakened | Workflow now spells out those conditions while keeping current evidence-led trial and adaptation |
| v1.6 sourcing: seven access mechanisms | A route-specific table became a shorter list that omitted important completeness, transmission and variant checks | Sourcing restores a mapping from acquisition routes to what each can establish and what must be checked |
| v1.6 sourcing: five reuse operations | The explicit direct/adapt/compose/technique/original distinction and project responsibilities became abbreviated | Sourcing restores all five operations with retained mature value and new obligations |
| v1.6 interaction: concurrent motion and status | Some false-sequence and interleaved-input cases were no longer as explicit | Interaction now distinguishes acknowledgment, real pending result, concurrent movement and misleading completion |
| v1.6 verification: three observation scales | Whole/relationship/detail questions collapsed into a short combined sentence | Verification restores the distinct observation targets and judgment-versus-automation boundary |

The [machine-readable ledger](evidence/v1.13.0/lineage.json) expands these
comparisons into 11 independently tracked restoration sites. A restored
section is a **new integration of old detail and current methods**, not a
mechanical reversion of an entire file.

## Where shortening did not show equivalent damage

A renamed heading can preserve or improve an instruction. The earlier
“Eight lenses” model evolved to nine experience dimensions, and temporal
verification acquired additional explicit evidence requirements. The
content-design reference retained the same main sections and similar
operative wording in the sampled v1.6.0 → v1.12.1 comparison. The
visual-assets reference also retained its specialist structure and grew
slightly. These observations do **not** certify sentence-by-sentence
equivalence; they explain why the audit did not restore the entire
historical corpus indiscriminately.

Content copied into the repository's human-oriented research guides may
be useful as context, but it does not independently count as a capability
preserved in the installed Skill. Accordingly the actual restorations
were made in the required reference files.

## Permanent repair

- Removed the 144 KiB aggregate test in `tests/test_publication.py` and the
  hard 500-line entry gate in `tools/validate_package.py`. The entry still
  serves navigation; longer methods remain organized in installed references.
- Replaced the budget language in `AGENTS.md` and amended `docs/WRITING.md`
  so knowledge fidelity precedes concision; documented conditions for
  justified deletion, relocation and equivalence.
- Added a permanent [continuity procedure](CONTENT-INTEGRITY.md), a tagged
  [capability lineage](evidence/v1.13.0/lineage.json) and
  `tests/test_content_integrity.py` to guard multiple concrete historical
  details within their actual installed sections.
- Restored material in six required references without discarding subsequent
  experience research, high-intensity exploration, reuse-first selection,
  perceptual inspection, responsive performance, content or art direction.

The eight required references now total **158,212 bytes** in the reviewed
candidate, compared with **146,719 bytes** at v1.12.1. That increase is not
itself a quality score: the value lies in restored conditional and executable
detail and the removal of a misleading release incentive.

## How to verify this change

The release workflow remains subject to the existing structure, link, cross-OS
Python tests, repository and fixed-tag installation, bilingual GitHub README
rendering, and product/asset/content/temporal browser fixtures. The new
structural test checks the historical ledger against current installed
section content and detects unintended removal of the restored detail.
Its assertions are not a substitute for human semantic analysis or a
fresh-context model-behavior comparison.

[Earlier applications](REVIEW-v1.12.0.md) remain evidence for their actual
v1.12.0 input. They are not silently relabeled as v1.13.0 agent runs.
Similarly, this source document does not predeclare a CI result, public
tag or an actual consuming product's acceptance. Inspect the final
[Actions workflow](https://github.com/D1ChangGeng/UI-Spec-Studio/actions/workflows/validate.yml)
and [GitHub release](https://github.com/D1ChangGeng/UI-Spec-Studio/releases)
to establish those separate facts.

## Long-term acceptance criterion

A revision can make prose shorter, but must demonstrate that important
design decisions remain at least as actionable under their relevant
conditions. If validity cannot be established, retain the earlier
detail or mark the need for review. The skill's knowledge is cumulative,
while its organization and reading strategy can evolve with capability.
