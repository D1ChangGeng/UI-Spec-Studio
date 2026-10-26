# Matched Agent experiment: structure and action coupling

## Current status and purpose

**Prepared, not executed.** The preparation tool never invokes a model, searches,
browses, generates a UI or evaluates outcomes. Six task families × three arms
are input cells, not eighteen observed results. All outcomes stay unreported
until real fresh-context runs and their artifacts exist.

The exact v1.13.0 baseline already includes deep evidence research, maturity
judgment and reuse-first behavior. This comparison measures the incremental
benefit and cost of an explicit multiscale structure and additional action
coupling, not evidence-driven versus evidence-free design.

## Three controlled instruction arms

- **baseline:** the full 29-file v1.13.0 skill, exact hashes checked against the
  recorded public tag and commit.
- **structure:** the same baseline plus an entry instruction and the multiscale
  map's structural content. The new action-module pointer and optional checker
  section are withheld so the added action treatment cannot leak into this arm.
- **structure-action:** the exact structure arm plus an entry instruction and
  the additional evidence-to-action module.

These are **instruction-only ablations**, not byte-identical versions of the
complete v1.14.0 distribution. They isolate the added modules from changed helper
and public documentation effects. The production skill's integration across the
eight references requires a separate actual-application check. Baseline text is
never rewritten to make it artificially weak. Every applied overlay and output
file is hashed. The structure arm retains baseline action guidance as well as
next-action fields; the tested difference is the added explicit constraint.

## Prepare immutable input folders

Provide an extracted or checked-out v1.13.0 `skills/ui-spec` directory locally.
The tool reads it, verifies the complete file identity, then writes to a new
output directory. It does not overwrite an existing output or alter the input.

```bash
python tools/prepare_design_experiment.py --baseline /path/to/v1.13.0/skills/ui-spec --output /path/to/new-experiment
```

Each cell contains one skill snapshot and the same task text used by the other
arms. Source treatment provenance and `prepared_not_run` status are retained.
The operator must freeze the task's project, reference version, media, business
facts and authorized resource routes identified in `tasks.json` **before** runs.
A prepared cell does not certify that those prerequisites have been met.

Keep this protocol, arm identity, other arms, evaluation criteria and previous
results outside the participant's workspace/context. Provide only its skill,
matched task inputs and ordinary prompt. Start a fresh agent session per cell;
do not reuse caches, generated candidates or conversation history across arms.

## Comparable run conditions

Record model identity and version, harness identity/version, prompt and skill
hashes, tool/browser/network access, available user assistance, machine/runtime,
initial repo revision, relevant fonts/media, configured resource limits and
actual start/end times. Hold these constant within a paired comparison. Randomize
arm execution order. Use seeds when genuinely supported and record repeats when
sampling variability matters. Repetitions cannot be fabricated by replaying logs.

Use matched opportunity and a predeclared practical budget, not a mandatory
search/tool count. Allow research and implementation to use the budget differently
and measure both costs. Separate fixed-material and live-web cohorts; live-source
changes or authentication differences must be logged and may invalidate a pair.
Use authorized accounts/materials and scoped user assistance only. Preserve runs
that fail or time out; never silently select only favorable samples.

The six prompts cover whole-product alignment, blocked primary access, small
high-impact assets, complex temporal behavior, expressive professional design,
and a supported low-impact edit. The last task checks whether the model can
stop unnecessary research and finish a small change reliably.

## Evidence required from a real run

Retain the ordinary task, actual initial inputs, skill identity, tool trajectory,
source/material provenance, observed media intervals, implementation diff,
resource adoptions, executed commands, rendered output, meaningful interaction
recordings and final claims. Redact secrets/private inputs with an explicit
record of the resulting evidence limits. Logged screenshots or downloaded files
must not automatically count as actually viewed or understood.

Compare declared observations and adoption against the tool trace and actual
source paths. A named package in a dependency file does not prove it carries the
visible interface. An output's statement that research happened is evidence of
what the agent said, not proof that it did that work. Keep process artifacts and
final product review separately available to reviewers.

## Evaluate behavior and actual outcome separately

| Dimension | Observations to record |
|---|---|
| Coverage discovery | Relevant initially omitted states/relationships found; justified exclusions; unresolved blind spots |
| Evidence truth | Claim-to-tool/source agreement; acquired versus viewed media; correct version and subject |
| Action effectiveness | Which consequential gap changed the next operation or dependent scope; whether that operation actually happened |
| Mature adoption | Original demo, local trial, source/code actually used, retained design mechanism and integration result |
| Perceptual result | Whole/page/component craft, text, material, optical relationships, populated states and continuous use |
| Efficiency | Actual effort, tokens/tools where measurable, writing overhead, rework and completion of the user's task |
| Convergence | Supported low-impact change finished with appropriate checks, rather than needless expansion |

Have an independent reviewer inspect anonymized outputs under the same content,
viewports, themes and interaction scripts without knowing arm labels. Reveal
process evidence separately to assess traceability and action. Use anchored,
explainable comparisons and retain disagreements; a universal aesthetic score
cannot substitute for inspected relationships. Owner preference is additional
scoped evidence, not interchangeable with engineering tests.

Predeclare which outcomes are primary, how incomplete runs will be handled and
what comparisons the sample can support. Report paired outcomes with uncertainty;
a small convenience sample does not establish all-model effectiveness. Do not
infer better UI from a longer map, more searches or a passing record checker.
No claim of improvement is warranted when only structure preparation ran.

## Boundary of this release

The current session has local execution and repository/CI access, but no
registered UI Spec Studio project with an authorized independent-agent runner
was identified. Existing unrelated ACS projects were not repurposed. Therefore
the package can ship tested structural mechanics and reproducible experiment
inputs while leaving empirical effectiveness **unverified**. Any maintainer
self-application is separately labeled and cannot replace these comparisons.
