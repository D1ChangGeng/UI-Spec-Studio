# Multiscale design evidence and decisions

Use the **Multiscale Design Evidence & Decision Model** to connect intended
experience, discovered coverage, inspected evidence, professional judgment,
mature-resource adoption and actual verification. This is a working map of
consequential design decisions inside the existing operations, not another
project lifecycle. Maintain it in the project's design records; the
[decision template](../assets/templates/design-decisions.md) is one possible form.
Read the [action rules](evidence-actions.md) when choosing what to do with a
consequential gap. Plain language, linked notes and existing task records can
express the same relationships as an optional structured record.

## Contents

[Minimum contract](#the-minimum-contract-and-its-scale) · [Design scales](#six-design-scales-with-cross-scale-navigation) · [Formal increments](#connect-formal-increments-to-the-current-product) · [Transverse relationships](#four-transverse-relationships) · [Coverage](#coverage-discovery--challenge) · [Decision units](#design-decision-unit) · [Three views](#one-record-three-useful-views) · [Tool boundary](#tool-boundary) · [Current model and history](#current-model-meaningful-revisions-and-evidence-archive)

## The minimum contract and its scale

For an important choice, another reviewer should be able to follow **purpose →
question → actual evidence and its limits → judgment and alternatives → chosen
source/adaptation → inspected result → remaining question and next action**.
Unknown information stays explicitly unknown. A pending trial can have a clear
purpose and candidate without an invented result. Add detail where impact,
uncertainty or plausible improvement warrants it, not to fill every column.

A low-impact correction within an inspected, accepted family can use a few lines:
what changes, which existing decision applies, why its conditions still hold,
what was inspected, and the remaining action. A new region generally needs state,
reference, comparison and trial detail. Full-product alignment, a new interaction
model, distinctive art direction or a high-impact asset calls for deeper coverage
and cross-scale relationships. A small favicon may need more study than a large
conventional panel. Unchanged routine instances can inherit a supported rule
when applicability is explained; inherited evidence does not become a new run.

## Six design scales, with cross-scale navigation

| Scale | Responsibility | Questions and useful evidence |
|---|---|---|
| **L0 Product Experience Alignment** | People, intended work, familiar experience, quality and independent expression | What must this product achieve and inherit, why, and where should it differ? Connect explicit user intent, audience evidence, observed reference scope and aesthetic commitments. |
| **L1 Experience Journeys & Interaction Model** | Entry, object, action/result loop, continuation, return and recovery | How does a person finish and resume actual work? Observe connected operations, interruptions, outcomes and context retention rather than only a landing state. |
| **L2 Page & Interface Architecture** | Navigation, work areas, pages, auxiliary panels, overlays and responsive organization | Which surfaces own which tasks, and how do shared anchors and spatial relationships change? Examine complete pages and transitions under relevant conditions. |
| **L3 Functional Regions & Component System** | Business objects, input regions, lists, controls, state families and reusable blocks | What is inside each region, how does it work, and which mature structures can carry its responsibilities? Inspect original demos and linked component states. |
| **L4 Visual Composition & Perceptual Detail** | Type, space, color, material, light, borders, shape, icon weight, imagery, spatial assets and motion craft | Which observed relationships create the intended quality? Inspect actual use size, useful details and temporal behavior, then return to the composition. |
| **L5 Implementation & Quality Assurance** | Actual resource/variant, configuration, adaptation, code/assets, trials and integrated checks | What was really used, what survived adaptation, and under which conditions was the result verified? Connect source identities to running or rendered outputs. |

L0–L4 describe useful design scales; **L5 is a realization and assurance link
for decisions at every scale**, not a claim that implementation is a smaller
visual object beneath every pixel. A shared input can appear on several pages,
and one design system can serve many decisions. Use containment where meaningful
and cross-links for participation, dependency and evidence. Do not force a tree
to duplicate shared objects or turn each CSS property into a decision unit.

An incorrectly dominant button can originate in L4 contrast, L3 action roles,
or L1 task ordering. Trace the issue upward to its purpose before changing
local values. Conversely, an L0 identity choice can require a new L4 font and
then L5 checks of wrapping, loading and every dependent core region. The map
helps select the right repair scale; professional analysis determines the cause.

## Connect formal increments to the current product

Keep the complete **Overall Product Goal**, the actual **Current Product UI**,
the **Formal UI SPEC** undertaking a cohesive design increment, and its
**Internal Research & Implementation Work** distinguishable in existing records.
These working objects are different from the map/inspector/Agent/verification
responsibilities described below. The goal preserves the intended whole; the
current UI carries accumulated results; a formal SPEC owns a quality objective;
internal activity develops and verifies it.

Connect each formal SPEC to the relevant L0–L5 objects and transverse
relationships. One SPEC can address several scales and objects; several SPECs
can progressively act on the same page, component family or shared system.
The page tree describes the interface's organization, not a compulsory hierarchy
of formal iterations. A shared typography SPEC can connect a product identity,
several reading regions, type details and their implementation checks. A
continuous interaction SPEC can connect a composer, messages, scroll state and
their temporal relationship. Preserve shared object identity across both.

Record the substance needed to understand the current increment: its experience
objective and quality responsibility, necessary objects/relations, research,
primary implementation and regression scopes, applicable inherited decisions,
actual result, remaining gaps and relationship to later work. Plain prose or
links in established records are sufficient. Keep candidate SPECs provisional
and distinct from formal work actually undertaken; an idea in the candidate
structure is not an implementation, approval or completed result.

Use **Inherit, Extend, Adapt and Revisit** to explain how work relates to the
same current product when useful. A component, artistic background or motion
increment has the same formal standing as a page increment; their actual
dependencies and inherited design choices still differ. Research and resources
can change those relationships. When boundaries change, link the prior goal and
open quality gaps to their current responsibility and explain the reason and
affected scope. Preserve the original evidence; avoid leaving displaced issues
only in a historical SPEC that appears complete.

The map supports the Agent's [experience-closure judgment](analysis.md#choose-a-bounded-increment).
Its relationships do not calculate scope, create formal increments or determine
when work is sufficiently mature. Internal searches, trials, fixes and commits
can remain within one SPEC without each acquiring a new lifecycle.

## Four transverse relationships

**State and time:** connect initial, focus, selection, expansion, pending,
confirmed, failed, return and interrupted states as relevant. Name trigger,
preconditions, first feedback, changing anchors and settled/return outcomes.
A panel opening can affect reading width, input, focus, scroll and neighboring
weight together. Follow the [temporal method](verification.md#inspect-a-time-bounded-visual-episode),
including meaningful intermediate states; static endpoints do not cover the
intervening relationship.

**Conditions and variants:** preserve the relevant version/platform, role or
plan, viewport and pixel scale, theme, language, content length, font readiness,
input mode and runtime/network conditions. Select a risk-relevant matrix; retain
an explicitly required exhaustive matrix. Explain sampled or excluded conditions.
Do not manufacture the full Cartesian product or silently count it as inspected.

**Dependencies and shared use:** identify shared tokens, fonts, assets, shells,
state owners and component families. Record which visible relationships depend
on them. A font change affects wrapping and button widths; a background change
affects foreground contrast and attention. Review changed relationships and their
dependents at intended scale, including states and journeys. Dependency links
are review aids, not an automatic assertion that every neighbor is defective.

**Evidence and realization:** link the actual user requirement, document,
viewed frame/interval, operable demo, resource source, local trial, code/asset
and resulting verification. One artifact may support several narrow claims,
but each claim keeps its object, conditions, method and limitations. Distinguish
what a source states, what was seen, what is inferred and what remains unknown.

## Coverage Discovery & Challenge

Treat the initial map as a hypothesis about coverage. A filled map only says
something about the objects it currently contains; it cannot certify that the
right objects were discovered.

Start from the person's complete task: arrive, act, see progress/result, continue,
return and recover. Independently inspect mature references' actual navigation,
help/tutorial flows, accessible demonstrations and relevant historical versions.
Use these observations to challenge the task-derived inventory. For each material
new object or relationship, decide **include**, **exclude with a reason**, or
**leave open with a question and next evidence route**. Preserve the source that
revealed it. This is relevance assessment, not a demand to copy every feature of
a larger reference product.

A conversation brief may initially expose only sidebar, messages and composer.
A demonstrated file-processing failure, source-inspection return, project scope
or mobile input state may reveal additional necessary coverage. A large
reference's team administration can be excluded from an explicitly personal
product, with that scope reason recorded. Conversely, a special current-product
need missing from the main reference warrants another relevant reference, not
silent deletion from the map.

Revisit coverage after discoveries, a major candidate change, trial findings
or integration differences. Ask which important relationship has no observation,
which assumption could hide an entire task family, and what evidence could
falsify the current scope. A newly discovered gap can be more valuable than an
extra screenshot of an already well-understood state. Keep unresolved coverage
visible rather than converting inventory completion into product completeness.

## Design Decision Unit

A **Design Decision Unit (DDU)** is a consequential choice, not necessarily one
component. Group related details when they support one decision; split choices
when they have different evidence, owners, constraints or reversal costs. Keep
a stable name or ID where several pages or records refer to the same choice.

A decision unit is not automatically a formal SPEC. A SPEC can draw on several
decisions and shared objects, and a supported decision can be inherited by
several increments. Grouping the work answers which experience goal can be
properly realized and reviewed together; grouping decisions answers which
choice and supporting evidence need to remain understandable.

| Relation | Record the useful substance |
|---|---|
| Purpose | User outcome, intended perceptual quality and parent experience goal |
| Research question | What needs deciding and what finding could change the choice |
| Evidence | Actual sources and viewed/operated portions, conditions, limitations and contrary observations |
| Professional judgment | Visible relationship, likely effect, causal hypothesis and current-product fit; distinguish inference from fact |
| Candidates and choice | Meaningfully different alternatives, comparable conditions, tradeoffs and provisional/selected direction |
| Implementation and adaptation | Target-quality source, actual implementation/variant, retained mechanisms, changes and local source/asset location |
| Verification and action | Claim-specific checked result, open gaps, dependency impact and next useful action |

Populate these relations as work occurs. In early research, pending candidates
and missing observations are useful information. At handover, unresolved relations
remain explicit. A link or plausible description without an actually inspected
subject cannot support a claim of visual understanding. Use concrete next
questions instead of writing confident conclusions into empty slots.

## States are scoped facts, not a single progress ladder

| State | What it establishes | What remains separate |
|---|---|---|
| To research | A relevant question/object is identified | Evidence and a supported choice |
| Acquired | A document, URL, image, video or source was obtained | Its contents or pixels actually being inspected |
| Observed | The stated portion was actually read, viewed or operated | Untested conditions and inferred effects |
| Compared | Meaningful alternatives were examined under stated conditions | Current-project fit and user preference |
| Trialed | A candidate was run and inspected in current-project conditions | Broad adoption and assembled-page quality |
| Adopted | Concrete implementation or material is in actual use | Proven quality under all claimed conditions |
| Verified | A specific claim was checked with an appropriate method/result | Other dimensions, conditions and user approval |
| Blocked | A named capability/access/resource is missing | Permission to assert an unseen result |
| Confirmed exception | An authorized adjustment has reason and exact scope | Evidence that the waived result itself passed |

Keep research facts, implementation facts, verification results and owner
approval distinct. States can coexist: an adopted resource may have a failed
narrow-state check and a pending temporal check. Observation of a rejected
candidate remains true. A code review can verify an import without verifying
animation quality. An installation entry is not adoption; a captured video is
not playback; a favorable professional judgment is not the user's approval.

Evidence is revision- and condition-bound. Preserve historical observations
when code, content, font, theme or operating assumptions change, but reopen
affected claims until they are rechecked or explicitly carried forward with a
justified applicability argument. Do not overwrite a failure with a pass merely
because the inventory or declaration changed. A parent's result summarizes
its scoped claims and open gaps; child completion never automatically approves
the page, journey or product.

## One record, three useful views

**Overview** exposes the intended experience, important journeys/surfaces,
coverage rationale, high-impact decisions and unanswered questions. **Design
Detail** follows a selected object/decision into real views, relevant perceptual
analysis, materially different candidates, temporal evidence and adaptation.
**Execution & Assurance** exposes the adopted locations, supported claims,
remaining dependencies and next action. Reuse the same IDs and underlying facts;
views filter information rather than keep three separately edited reports.

For formal increments, Overview also shows the complete goal, current product
foundation, active SPEC, provisional later candidates and important dependencies.
Design Detail exposes the active increment's quality responsibility, scope
rationale, actual references and realization. Execution & Assurance connects
its implementation and associated regression evidence to remaining goals and
gaps. Show the decision-useful portions in the conversation at init, a formal
SPEC's start or material adjustment, significant findings and delivery. A saved
record supports traceability; it does not substitute for presenting the actual
design result to the user.

For a large task, show a concise overview with representative visuals and
clickable evidence locations; expand important details when they are needed.
For a focused correction, a short decision entry and the actual preview may
suffice. Keep long discovery logs behind the record. Users should be able to
inspect what changed in the design, not need to reconstruct your internal
reasoning or manually select routine components.

Project evidence and conversation output are two expressions of the same current
understanding. Internal professional work produces the evidence; the model keeps
its actual scope and interpretation; the conversation selectively presents the
changes with design significance. Apply the [event-driven disclosure method](workflow.md#make-consequential-design-work-observable)
to choose what is useful now. A research finding may need only Design Detail;
delivery can draw on the important parts of all three views. No message needs to
reproduce every view, and no separate event document, disclosure field or report
database is required.

Keep a shown artifact's identity and claim legible: a target reference, original
candidate demo, project trial and integrated UI support different conclusions.
Relate the actual displayed result to its current implementation and remaining
quality gap. Disclosure records availability, not that the user examined or
approved it. Preserve actual user decisions in their existing scoped authority
record. When new evidence changes a publicly shown choice, update the current
model and expose the consequential correction; retain the earlier output as
history without leaving both conclusions active. An unresolved gap continues
to guide the current SPEC's action even after it has been shown to the user.

## Tool boundary

The optional [structured profile](evidence-records.md) and
[structural inspector](../scripts/check_design_evidence.py) describes IDs, field
shapes, declared state labels, reference resolution, local file metadata and
explicit target-to-record links. It reports theoretical categories not explicitly
tagged and paths reachable through declared relations. It does not evaluate
evidence adequacy, candidate differences, source/check compatibility, version
applicability or whether an action is justified. Readability and structural
observations stay separate; neither authorizes progress or certifies completion.
The Agent interprets these facts using the actual task, professional knowledge
and real evidence. Existing project records remain sufficient when they express
the same design relationships.

Where formal SPEC declarations are present, the inspector may describe their
literal object and decision references, candidate/formal distinction and supplied
scope relationships. It does not select a partition, infer inheritance, rank
increment importance, require a new SPEC or certify closure and visual quality.
Formal identity, structural record completeness, actual implementation and
observed product quality remain separate observations.

## Theory, declarations and task-specific applicability

The theoretical design vocabulary is a set of professional observation lenses,
not a universal inventory every product must implement. It includes all six
scales and relevant typography, assets, states, motion, accessibility, responsive
conditions, recovery, performance and operating content. A reading tool may have
no form flow; a conversational application may need deep attachment and long-text
work; a brand page may need photography or spatial composition instead.

Distinguish **within-declaration absence** from **candidate unrepresented coverage**.
A component ID referenced by L5 but not present is mechanically unresolved. An L3
region with no listed state link or an L4 asset with no listed source is a record
observation. A theoretical category with no explicit tag is only a prompt: the
same subject may be addressed in prose, by a shared decision or outside this record.
The inspector cannot determine necessity, representation equivalence or completeness.

Use real tasks, actual references and professional judgment to include, exclude,
combine, split or investigate the candidate. Keep the reason for consequential
scope choices; do not add fictitious objects or busywork to silence hints. A single
source can adequately support a narrow inherited change; a two-name comparison
can remain superficial. Counts cannot decide either case.

## Four independent responsibilities

The **map** is the current design understanding, not the product itself. The
**inspector** observes representations, not the professional truth of their links.
The **Agent** owns evidence interpretation, source choice and actual execution.
**Independent verification and acceptance** support specific outcomes through
actual visual viewing, continuous use, browser/function tests, timing measurements,
engineering checks and authorized user decisions. A passed browser assertion
proves its own condition; a reviewed image supplies scoped visual evidence; owner
approval supplies preference or authorization. Keep these results separate.

## Current model, meaningful revisions and evidence archive

Prioritize a **Current Design Model** with intended experience, active choices,
actual adoption, implementation relationships, current constraints and open
questions. One canonical current choice should be easy to identify. Do not leave
several incompatible conclusions looking simultaneously authoritative.

Preserve **Meaningful Revisions** when new observations change understanding or
implementation. Record what changed, why, the affected objects/conditions and the
judgment now in use. Ordinary Git history, a short linked revision note or optional
`revisions` entries suffice. Routine tool calls do not each require a revision.

An **Evidence Archive** retains source snapshots, original captures, media,
code identities, execution traces and prior design records in authorized storage.
Link rather than re-copy them. Keep archived judgments identifiable as historical;
current views need not load every old candidate or superseded assumption.

A formal boundary change belongs in meaningful revisions when it alters a
commitment or responsibility. Keep its prior and current purpose, reason,
affected objects and open issues traceable without logging every search. Update
the current product view and revisable candidate structure together. Scope
reorganization can be complete while the associated design work remains open;
record both facts accurately.

For example, a single-line composer may have passed its former layout check.
Adding several attachments can expose wrapping and focus problems. Keep the old
observation intact, update the current object's conditions and open questions,
explain the revision, and inspect the changed layout. The new issue does not erase
the historical test, and the old pass does not certify the expanded use case.

## Local change and revisable state

Research facts (acquired/observed/compared), implementation facts
(proposed/trialed/adopted), verification records (planned/executed/issues/results),
issue disposition (open/blocked/resolved/exception) and owner decisions
(pending/provisional/approved) can coexist. They are neither one irreversible
maturity ladder nor a mechanical instruction to enter another stage. A statement
is conditioned on its object, source identity, use and observer; its recorded
label does not authenticate the event.

A project snapshot identifies a whole record. Applicability follows the actual
changed component, font, asset, content, service adapter and conditions. Do not
invalidate all visual history because unrelated backend code changed. Conversely,
do not relabel an old capture with a new version to imply renewed observation.
The Agent assesses whether a prior result remains applicable, needs a scoped
carry-forward explanation, or requires a new check. `--changed` offers only
relation-derived review candidates; omitted links can hide other impacts.

Experience understanding → product research → evidence → professional judgment
and mature-source discovery → comparison → trial/adaptation → implementation →
verification remain two revisable lines of work. Either can correct the other:
trial findings may revise the model, and new product evidence may change resource
selection. No structural flag, stage label or past approval freezes those choices.


## Connect visual-craft discovery to current decisions

For an important resource choice, link the perceptual goal to the actual reference, the specific candidate and source variant, original-demo observation, local trial, adopted location/configuration and integrated-use finding. Record the resolved relationships that motivated selection and which survived adaptation. This extends the existing decision unit; it does not require a new record for every CSS property or a fixed number of candidates.

Keep reuse scope, observed visual completeness, functional responsibility and final perceived fit distinct in professional reasoning. A background can connect L0 identity, L2 composition, L4 material/motion and L5 configuration/performance. A primitive may connect interaction semantics without claiming to carry that background or the page's visual craft. New sources can revise earlier targets, and local failures can reopen source selection.

Use the current model for actual adopted choices, meaningful revisions for replacements and their reasons, and the archive for original observations. A catalog entry is a discovery lead, not a project adoption record. Structural inspectors describe only declared fields, IDs, references and relationships: they neither rate visual completeness nor judge reuse suitability, research sufficiency or the next action. All such judgments remain with the Agent and scoped actual verification.

## Carry visual provenance without multiplying records

Apply the [default-deny source policy](component-sourcing.md#default-deny-original-ui-construction) to design responsibilities at every visible scale. Link **target quality → mature design source → actual implementation/configuration → retained relationships in the current UI → remaining gap** within the existing decision unit. One mature page, block, component family or established system can carry several related decisions; inherited child elements can refer to that same source. Do not create an obligatory record for every element, color value or CSS declaration.

Keep Resource Acquisition, Resource Adoption and Craft Retention as distinct facts. Source possession supports acquisition; an actual placement or call site supports adoption; viewed comparison under relevant conditions supports retained quality. Record meaningful lost or replaced relationships even when the original file/name remains. Functional dependencies cover their real scope without being presented as the visual foundation for unrelated composition, typography or material.

For faithful design translation, identify the complete user-supplied/confirmed design and its specified scope, then link fidelity evidence. For an original W1–W3 responsibility, preserve the concrete necessity, actual mature candidates and limits, narrow original boundary, retained source, real user authorization and verification in the same decision. Existing approval may already provide the required authority; presentation alone does not. A declaration or inspector-resolved reference cannot judge qualification or confer permission.

Keep unresolved sourcing and temporary technical probes identifiable, with the next discovery, trial, adaptation or scoped decision that can change their status. When source fit changes the formal SPEC boundary, preserve the original quality obligation and its current responsible increment. These are extensions of existing current-model relationships, not a new schema, approval state machine or quality certification mechanism.
