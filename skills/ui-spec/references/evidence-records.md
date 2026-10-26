# Optional local evidence-record profile

Use this profile only when a project benefits from machine-readable checks and
views. The [design map](evidence-map.md) defines the professional relationships;
existing Markdown, design notes or project records can satisfy them without JSON.
Do not duplicate the authoritative facts in several formats. The
[template](../assets/templates/design-evidence.json) is a valid **unfilled draft**,
not a completed design map or evidence of research. `prepare.py` does not create
it automatically.

## Run the read-only helper

```bash
python <skill-dir>/scripts/check_design_evidence.py --project-root . \
  --record .ui-spec/design-evidence.json --view overview
python <skill-dir>/scripts/check_design_evidence.py --project-root . \
  --record .ui-spec/design-evidence.json --view detail
python <skill-dir>/scripts/check_design_evidence.py --project-root . \
  --record .ui-spec/design-evidence.json --view execution --changed typography
```

The helper prints JSON to stdout, reads local files only and makes no network
requests or writes. Exit 0 means the declared record is structurally consistent;
1 reports inconsistencies; 2 reports input/read problems. All record reports include
the evidence limits. It neither calls tools for the agent nor schedules work,
advances statuses, creates approvals or rates visual quality.

## Small core, richer facts when available

The root has `format: "ui-spec-evidence/1"`, an explicit current source/product
`revision`, and `objects`/`decisions` lists. Add `conditions`, `evidence`,
`relations`, `coverage_challenges` and `required_checks` as needed. A new record
can be structurally valid while all research is pending. For a light correction,
prefer the existing short prose decision over adopting JSON merely to run a tool.

| Entry | Core fields and meaning |
|---|---|
| Object | `id`, `level` L0–L5, `title`; optional `parent` for containment only. L5 may describe a realization linked to several higher-scale decisions. |
| Condition | `id`, `description` naming the relevant state/view/locale/theme/content/input/version combination. Separate conditions where claims differ. |
| Evidence | `id`, `kind`, `role`, `location`, `status`, `objects`, `conditions`; an observed item also has `observation` identifying what was actually inspected. |
| Decision | `id`, `objects`, `purpose`, `question`, evidence references and `next_action`; progressively add judgment, alternatives, choice, implementation, gaps, checks and approval. |

Evidence `kind` is `text`, `visual`, `temporal`, `implementation` or `runtime`.
Its `role` is `reference`, `candidate`, `demo`, `trial` or `integrated`; status
is `acquired` or `observed`. A local location is `{"path":"relative/file"}`;
a remote location is `{"url":"https://…"}`. Only local files are checked.
Use project-relative POSIX paths with no parent traversal or symlinks. A local
`sha256`, when supplied, is compared with actual bytes. Source rights and factual
truth still require their own review.

Observed temporal evidence additionally describes the actual `window` and
`method`, including playback, live operation or ordered sampling limits.
Current-project evidence has `product_revision` matching the subject checked;
external references retain their own revision as source information. A still
must not be relabeled temporal to evade the method's observation requirement.
The helper cannot detect dishonest declarations or judge whether sampling was
adequate for the claimed motion.

Optional `relations` identify `from`, `to`, and `type`: `affects`, `depends_on`,
`appears_in`, `precedes`, `transitions_to` or `shares`. The `--changed` report
follows declared dependency/shared-use and ancestor relationships. It reports
candidate review scope only; time ordering by itself is not a causal invalidation
edge. Cyclic dependencies can be legitimate; containment cycles are rejected.

## Decisions and actual progress

A `comparison` can be planned or compared. A compared record identifies distinct
named `alternatives`, observed supporting `evidence` and a `rationale` describing differences
and conditions. The helper cannot assess whether two named options actually
have meaningful visual differences. An inherited supported choice need not claim
a new comparison.

`implementation` has state `proposed`, `trialed` or `adopted`, actual `paths`
and relevant `evidence`. Trialed/adopted declarations need existing paths and
source references. A trial also needs observed evidence with the current project revision and trial role. Their existence cannot prove that an import was used, the
application ran, or the candidate's visible quality survived adaptation.

A `check` has a domain (`visual`, `temporal`, `engineering`, `task`), objects,
conditions, status (`planned`, `pass`, `fail`, `blocked`, `waived`) and evidence.
Passing current-project claims additionally identify `revision`, a `finding`
and `role` (`trial` or `integrated`, default integrated). For every declared
object-condition pair, the helper requires an observed item in the matching
role, current revision and evidence domain. Visual claims need visual evidence;
temporal claims need temporal evidence; engineering claims accept implementation
or runtime evidence; task claims require runtime evidence. This is a declaration
consistency check, not authentication of that evidence.

`required_checks` optionally names object/condition/domain triples that the
project has explicitly committed to, with an optional `role` (default integrated). A trial pass cannot satisfy an integrated requirement. Unchecked requirements are reported in
`pending_coverage`; claiming `finish` for a dependent object while those checks
remain unresolved is inconsistent. Only declared requirements are checked:
Coverage Discovery & Challenge must still discover missing obligations.
A waived check remains an exception, never a passing observation.

Owner `approval` is separate: pending, provisional or approved. Approved records
need source and scope. Exceptions on checks or gaps need `by`, `source`, `reason`
and `scope`; these fields identify a claim of authority but cannot verify it.
Normal security, permissions and legitimate resource-use obligations still apply.

## Gaps and the next action

A gap has `id`, `question`, `impact` (low/standard/high), `status`
(open/blocked/resolved/waived) and optionally its affected `objects` (otherwise
the decision's objects). Open or blocked high-impact gaps have a concrete
`next_action` explanation. Resolved gaps refer to `resolution_evidence`.
Exceptions use the scoped authorization record above.

The decision's `next_action` names a `kind`, `reason` and optional affected
`objects`. Kinds are research, inspect, compare, trial, implement, expand,
verify, revise, ask or finish. Expansion/finish need explicit judgment and
choice and cannot overlap an unresolved high-impact gap or its declared dependency/containing-scope impacts. Supported independent
progress names its separate objects and `independent_reason`. Use `trial` for a
reversible investigation rather than labeling unsupported broad work an
implementation to evade the action rule. The helper cannot infer the actual
size or effects of work from its declared label.

A coverage discovery records `discovery`, `reason`, disposition include/exclude/open,
related evidence/objects and an action for an open question. It can document a
relevant reference feature or a task-derived omission; it does not force adopting
all reference-product features.

## Three views and their limits

Overview projects objects, discoveries and decision questions. Detail projects
full decisions, evidence, conditions and relations. Execution projects source
locations, scoped checks, approvals, gaps and next action. All use the same
record without writing derived reports back into the source. Inspection counts
are structural counts, not a coverage percentage or aesthetic score.

After a change, retain old observations and approval scope but update current
revision/check applicability. Passing stale evidence is rejected by this profile;
manual carry-forward needs a new scoped explanation and the appropriate evidence,
not merely replacing a revision string. Actual execution traces, image viewing,
semantic comparison and real product judgment remain outside this helper.
