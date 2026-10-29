# Optional local evidence-record profile

Use this profile when a project benefits from machine-readable **structural
observations**. Existing Markdown and project records can carry the same design
relationships. The [map](evidence-map.md) organizes them; the
[action method](evidence-actions.md) guides the Agent's professional decisions.
JSON is optional. Neither a schema nor a tool return decides research sufficiency,
implementation readiness, design correctness or task completion.

## Read-only use and report semantics

```bash
python <skill-dir>/scripts/check_design_evidence.py --project-root . \
  --record .ui-spec/design-evidence.json --view overview
python <skill-dir>/scripts/check_design_evidence.py --project-root . \
  --record .ui-spec/design-evidence.json --view detail
python <skill-dir>/scripts/check_design_evidence.py --project-root . \
  --record .ui-spec/design-evidence.json --view execution --changed typography
```

The report describes the supplied file and declared snapshot. `record_readability:
readable` means JSON was read, not that its shape, professional content or quality
is sound. `structural_findings` separately identifies wrong shapes, ambiguous IDs,
unresolved references, graph cycles and local-path facts. Missing optional fields
are `field_observations`, not instructions to fill every field. A readable empty
map can have no structural findings while no design work has happened.

Exit `0` means inspection ran, including reports with findings; exit `2` means an
input/read problem prevented it. Neither exit value rates design work. There is
no aggregate `ok`, pass, readiness or satisfied result. Integrations should read
specific facts for their own purposes rather than use an inspector as a launch
or finish gate. The older Python function name `validate` remains an alias to
this report, not to its former acceptance behavior.

| Report relation | Precisely what it represents |
|---|---|
| `record_source` | Input path, declared format/revision and origin, not authenticated source truth |
| `object_inventory`, `counts` | Explicit object IDs, L0–L5 labels, category tags and record counts |
| `field_observations`, `structural_findings` | Field presence/shape and directly inspectable structural problems |
| `reference_observations` | ID lookup within the declared current record scope |
| `file_observations` | Local path type/size or remote URL syntax; remote URLs are never fetched |
| `declared_check_records` | Checks and their author-declared statuses; the inspector did not execute them |
| `declared_exception_records` | Waiver declarations, kept separate from non-waived checks |
| `declared_item_records` | Literal links between explicitly listed check targets and check/exception records |
| `unlisted_declared_items` | Explicitly listed targets for which neither type of record was found |
| `candidate_unrepresented_categories` | Theoretical categories with no explicit current-object tag; applicability is unassessed |
| `revision_declarations` | Declared snapshot, source, object and check identities without global invalidation |
| `declared_actions` | Agent-written action text, returned without selection, validation or execution |
| `declared_relation_review_candidates` in the view | Objects reachable through listed relations, not proven impacts or required rechecks |

A planned or failed check is still a check record. A waived target can have only
an exception record; it is not converted to a successful observation. A missing
record is not automatically missing research: equivalent work may be recorded
elsewhere. The Agent establishes relevance and examines the actual material.

## Small core and optional detail

The profile uses `format: "ui-spec-evidence/1"`. `revision` labels the current
record snapshot when known; null or omission preserves an unrecorded identity.
Use `record_origin` to distinguish an unfilled template, an initialized working
record and an authored project model. The [empty template](../assets/templates/design-evidence.json)
contains no invented objects, candidate or next action and is not created by
`prepare.py` automatically.

Collections are added according to need. Their ID and reference shapes support
lookup; they are not a demand for every theoretical design dimension.

| Entry | Fields and intended professional meaning |
|---|---|
| Object | `id`, L0–L5 `level`, `title`; optional `parent`, `revision`, `categories` and project-specific detail |
| Condition | `id`, `description`; distinguish relevant state, viewport, theme, locale, content, role, platform and version |
| Evidence | `id`, `kind`, `role`, `location`, `status`, linked `objects` and `conditions`; actual inspected portion belongs in `observation` |
| Decision | `id`, `objects`, `purpose`, `question`; add judgment, evidence, candidates, choice, implementation, gaps, checks, approval and Agent-authored action as work occurs |
| Revision | Meaningful change: `id`, `summary`, `reason`, affected current `objects`, evidence, `current_judgment`, optional prior snapshot location and `historical_objects` |
| Archive | `id`, `location`, `revision`, `description` linking an earlier record or raw evidence; content is not loaded into current decisions |

The root `objects`/`decisions` collections express the **current model**.
`revisions` explains important changes. `archive` points to original evidence and
prior snapshots. These are optional ordinary records, not transactions or a new
lifecycle. Store large media and full histories in authorized project locations;
links avoid duplicating them. Historical object identifiers need not still be
present in the current model, so use `historical_objects` for that purpose.

## Optional formal-increment declarations

Keep the complete product goal, current product UI, formal design increments and
their internal research/implementation work distinguishable in the same current
model. Existing prose or project records can express these relationships without
adopting additional JSON fields. The optional declarations below extend
`ui-spec-evidence/1` compatibly; older records remain readable.

| Optional entry | Declared meaning and structural lookup |
|---|---|
| `product_context` | `overall_goal` and `current_ui` describe the complete goal and current implementation; these are author-supplied text, not verified product facts |
| `candidate_specs` | Revisable possible increments, each identified by `id`; their presence does not begin formal work or fix an implementation order |
| `formal_specs` | Actual formal increments, each identified by `id`; `purpose`, `quality_goals` and other narrative detail describe the author's intended responsibility |
| Object references within a SPEC | `objects`, `research_objects`, `implementation_objects` and `regression_objects` refer to existing object IDs; the three scopes can differ |
| Decision references within a SPEC | `decisions` refers to existing decision IDs, keeping actual evidence, implementation and remaining gaps at their current responsible records |
| Related increment references | `related_specs` refers to candidate/formal SPEC IDs; the links describe declared association without deciding order, dependency or scope suitability |

A formal SPEC can link several L0–L5 objects and cross-component relationships;
several SPECs can link the same page, component family or shared system. Keep the
design-object map and formal work boundaries distinct. Search, trial, repair and
reinspection inside a SPEC do not require additional SPEC records. New formal
increments have a distinct design purpose and review boundary; the Agent judges
that distinction from the actual work.

After a consequential boundary change, update the current scope and explain the
reason, affected goals, inheritance and unresolved responsibility in meaningful
revisions. Keep original findings and evidence traceable through existing decisions
and archives. Moving a goal to another increment does not establish its completion.
Candidate plans can change as research and resource trials reveal better boundaries.

Overview, Detail and Execution present these same declarations with candidate and
formal increments distinguishable. The inspector describes supplied fields and
resolves declared references; it neither creates a plan nor certifies a minimum
sufficient experience closure, research depth, visual quality or completion.
Missing optional fields are not a request to fill them. There are no automatic
SPEC status transitions, count targets or new approval stages.

## Source and file facts

Evidence kinds commonly include text, visual, temporal, implementation and
runtime. Source roles commonly include reference, candidate, demo, trial and
integrated result. They remain separate from acquired/observed status. The
inspector presents declared values; professional meaning and matching a claim
to evidence belong to the Agent. Custom descriptive states are not progression
commands. A single candidate, a text/visual pairing or a high-impact open issue
never produces a mechanical recommendation or veto.

Use `{"path":"relative/file"}` or `{"url":"https://…"}` for locations.
Paths are project-relative POSIX paths with no parent traversal or symlinks.
File metadata is observed; the file's pixels, source use or factual content are
not. Remote references remain unfetched. Source rights and real authorization
are separate facts. Optional declared `sha256` text is not compared here.

For a separately needed byte-identity assertion, use the independent tool:

```bash
python <skill-dir>/scripts/check_file_integrity.py --project-root . \
  --path .ui-spec/evidence/capture.png --sha256 <expected-sha256>
```

This command returns match/mismatch for those bytes only; exit 0/1 corresponds
to that explicit assertion and exit 2 to inability to check. It cannot establish
that the image was viewed, its contents are truthful or a UI is well designed.

## Records are not independent verification

The Agent describes actual temporal observation with its window, method and
sampling limitations. A still cannot establish an unseen transition. Evidence
used to judge visual quality needs an actually viewed subject; an original demo
and an integrated page are different subjects. These are professional duties,
not predicates the structural inspector evaluates.

A `comparison` may record state, named alternatives, evidence and rationale.
There is no mechanical two-name minimum: names alone cannot establish real
visual differences. The Agent decides when meaningful alternatives are needed,
when existing verified work suffices, and what observation would change a choice.
An `implementation` can record proposed/trialed/adopted state, paths and evidence.
A located source file does not establish that the app uses it or retains its craft.

Checks commonly declare domain, objects, conditions, role, status, revision,
finding and evidence. A record's `pass`, `fail` or `blocked` remains the author's
statement about a scoped external check; it is not the inspector's verdict.
`required_checks` can explicitly list object/condition/domain/role targets.
Matching uses literal addresses, not sufficiency, evidence-type or version rules.
The default role `integrated` is a documented matching convention, not an
assertion that an unlabelled observation was actually integrated. Inspectors
never aggregate declared passes into design completion.

Approval has its own source and scope; exceptions have their own decision,
reason and authority. Missing provenance can be visible as an undeclared field;
its authenticity and consequence require independent judgment. A waiver can
change an authorized scope without making missing observation real. Normal host
permissions, security and resource-use obligations remain in force.

## Theory is not applicability

The [bundled category vocabulary](../assets/design-coverage-categories.json)
provides theoretical prompts, including content, assets, responsive variants,
recovery, performance and operational use. Matching only counts explicit
`objects[].categories` tags. No tag does not prove no corresponding design work:
prose, shared components and archived material may contain it. Unknown project
categories remain visible; not every project needs all catalog categories.

A broken ID reference is **within-declaration missing information**. A catalog
category with no tag is **candidate unrepresented coverage**. Do not convert the
second into the first. The Agent chooses include, exclude, combine, split or
further research using the actual task and observed mature products.

## Relations, revision and current applicability

Relations name `from`, `to` and a type. Change lookup follows child-to-parent
containment, affects/appears_in, reverse depends_on, and bidirectional shares.
It does not traverse precedes/transitions_to as proof of causal impact. Cycles
terminate safely; a containment cycle is reported as a graph fact. Unresolved
`--changed` IDs are listed rather than causing a work blockade.

A global snapshot change does not mechanically invalidate prior observations.
Keep local source/asset/condition identity with the actual checked subject.
Old results remain historical facts. The Agent decides which observations still
apply, which need a scoped carry-forward explanation and which need new viewing
or testing. Changing an unrelated backend implementation need not erase all
visual findings; changing a font can affect several dependent layouts.

Overview, Detail and Execution are projections of the same **current** records.
Revision summaries and archive references stay recognizable as history; the
inspector does not load them as competing current choices or rewrite any status.
Update the current judgment after meaningful new evidence and link why it changed.
A record listing a future action does not prove that action was performed.
