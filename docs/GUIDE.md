# Guide: a multi-round interface project

## 1. Begin with the goal and real project

A useful opening prompt is:

```text
Use ui-spec: init. This is an existing research workspace.
Keep its framework and working API. Inspect its routes, user tasks and current
screens. Establish a coherent UI direction and implement the first useful slice.
```

The agent reads all eight common references, then the code, project instructions and accepted decisions. It identifies how people start, what they work on and how the task continues. Product UI Experience Alignment establishes the intended experience from real tasks, content and operating conditions. A product name opens research into relevant pages, flows and qualities; an open brief prompts the agent to find mature patterns and implementations. Reference research and resource selection develop together.

Explicit goals for artistry, visual impact or differentiation remain delivery
requirements alongside usability and truthful behavior. The product category
informs tasks and conditions; visual form can be researched independently while
preserving understandable objects, actions, results and continuation.

For consequential choices, use [evidence-driven deep visual exploration](DEEP-VISUAL-EXPLORATION.md). Weigh impact, uncertainty and potential improvement. Search both target-experience references and adoptable resources; actually inspect distinguishing details and operation, and challenge an early favorite with a materially different candidate. High-leverage unknowns may justify many iterations; familiar, already-validated UI need not. State what was seen and what could still change the decision. Source counts do not establish design confidence.

Mature implementations supply general UI by default, at the highest appropriate reuse level. The agent trials consequential choices with the project's content, fonts, theme and states before expanding integration. Optional shape resolves material open directions through a recommendation and focused choice or representative preview; clear direction supports direct progress. The following collection/detail examples assume that this direction has been selected for the actual task.

Existing instructions, design documents and tests remain useful. The optional templates are a starting point when equivalent records are absent.

## 2. Review a named scope

```text
The workspace navigation and collection/detail layout are approved at the
current preview. Keep the typography and spacing. The empty state still needs
revision; prioritize that and the saved-search flow next.
```

Approval belongs to the named scope and reference. The agent records it with the current source reference and keeps the empty state pending. A new commit can preserve the approved direction, while an intentional change to accepted appearance or behavior returns the affected scope to review.

A recorded approval is not a request to duplicate the application. Reusable components remain the implementation; fixtures and data adapters make the reference reproducible. Git and scoped evidence identify the reviewed result.

## 3. Iterate by value

A user can simply say `Approved, continue`. The agent identifies the reviewed
scope, inherits its direction and selects the next valuable increment. Detailed
instructions remain welcome when the user has a specific preference.


```text
Use ui-spec: iterate. Continue the saved-search journey and address the empty
state. Reuse the approved shell and inspect both the narrow and wide views.
```

The next round checks where the user starts, what the action means, which conditions apply, where the result appears, and how the user returns or retries. If two routes express the same task, the agent considers consolidating them. If the journey is broken by a missing control, repairing the control outranks drawing another page.

New components are selected by actual role and local trial. A coherent layout or functional block can carry several related decisions; supplementary components and assets fill specific needs. Configuration, composition and focused extension preserve the selected implementation's useful visual and interaction relationships. Custom work addresses demonstrated gaps.

## 4. Inspect rendered evidence

A useful round report contains the working preview entry, scope, actual resources adopted, relevant adaptations, observed checks and remaining conditions. The agent opens the captures and uses the interface. Reference qualities, the original resource demo, the local trial and the assembled result each receive the observation needed for their role. A source may have been researched without being adopted; a successful local trial still needs review in the full composition.

Three independent comparisons matter:

| Comparison | Questions |
|---|---|
| Across viewports | Are text, controls, composition, density and content access appropriate? |
| Across related pages | Do shared headers, navigation, content origins and interaction conventions remain stable? |
| Across states | Do selection, focus, input and visual continuity survive changes? |

Language/theme/role variants extend the matrix where supported. A compact sign-in view, a long article and an operational workspace use different composition and scrolling rules.

Review experience validity and expressive completion separately. Check the
promised visual direction after the first action, with populated results, long
content and repeated use. When implementing selected or approved design work,
inspect source fidelity as well: comparable-image differences can diagnose a
specific reproduction target, while actual viewing establishes perceptual quality.

## 5. Run a broader audit

```text
Use ui-spec: audit. Reconcile the implemented routes and overlays with the
user journey inventory. Review all primary views and critical states, fix
shared causes, and return the remaining coverage with evidence.
```

The agent records coverage against the actual route and state inventory. Dynamic records use representative short, typical, long, empty and permission-related shapes. A full-page screenshot supplements, rather than replaces, a true viewport capture; internal scroll areas need real-scroll checkpoints.

The optional [manifest checker](MANIFEST.md) can find missing declared cases and incomplete evidence records. It does not perform the visual review itself.

## 6. Finish by connecting

```text
The listed SPEC scope is approved. Use ui-spec: finish.
Reuse the accepted components, implement the real data and permission boundaries,
and complete task and visual regression against the approved reference.
```

Finish follows six connected activities: reconcile the accepted scope and current system; establish contracts; sequence complete outcomes; connect; verify both tracks; deliver. The agent follows each meaningful action into the real implementation: request, authorization, validation, persistence, result and recovery. It connects complete vertical slices. Account or resource access is enforced by the trusted service. A static article index may simply need verified content, routing and deployment build behavior.

For an unreleased development build, work continues directly in the current source and data model. For an operating system, actual user data and compatibility obligations inform the plan. Engineering scope comes from those facts.

The agent verifies real data and equivalent visual states, then reports approval, connection, verification and release separately. Credentials and publishing authority are specific dependencies; other independent work continues.

## 7. Continue after a new requirement

A new language, theme, product capability or user role may reopen a bounded slice. Update the relevant brief, shared tokens and matrix, then iterate. The project keeps one current source direction and recoverable Git history.

## Working with other skills

UI Spec Studio coordinates the lifecycle. An installed design, accessibility, animation, framework or testing skill can provide specialized help for a slice. Load it explicitly when useful and reconcile it with the approved brief. Treat style preferences from a specialist as candidates, while project truth and accessibility obligations retain priority.

Source references are material to evaluate. Installing or invoking a referenced third-party skill is a separate operation under the host's permissions.

## User feedback and working depth

A statement such as “too empty” or “the page jumps” is enough to start a diagnosis.
The agent identifies the relevant visual or interaction relationship, inspects the
actual result and tests a bounded repair. You review the effect. Common design
principles are already part of the skill's working foundation.

For a planning-only request, shape delivers decision support. For a design/build
request, it continues when enough direction exists. Use a focused choice when an
unresolved high-impact experience direction or consequential commitment needs the
user's intent; routine reversible design choices can be shown directly.

The same project can contain approved screens, pending states and connected
features. Treat each scope's evidence separately. The current operation describes
what the agent is doing, rather than declaring uniform project maturity.

## Use ecosystem resources without managing the search

```text
Continue with the next useful UI increment. Find strong existing implementations
for its important visual and interaction needs, trial the most suitable choices
with our content and states, and adapt them to the accepted direction. Preserve
what makes them useful, then verify the composed result.
```

The same behavior is part of ordinary `continue` requests. The agent can use the
[resource map](../skills/ui-spec/references/resource-catalog.md), official indexes,
exported configurations, actual demos/source and available tools. It chooses the
reuse level and reports consequential decisions with the working result. Packages,
licensed source, exports and feasible implementation ports all provide adoption
paths. Integration code connects them to the product. Research and trial time are
judged by their contribution to final quality and avoided rework.

For targeted inspection, the installed optional helper works from any directory:

```bash
python <skill-dir>/scripts/find_resources.py --need motion --stack vue --json
python <skill-dir>/scripts/find_resources.py --id fontsource --json
```

Discovery leads retain their source and review date. Demo inspection and actual
project checks are recorded separately. Existing approved resources remain useful
while their conditions fit; a new requirement can justify a fresh comparison.
See [the resource workflow](RESOURCE-REUSE.md) for examples and maintenance.

If an important source needs normal account access, an official client or an
authorized export, the agent first uses available evidence and then requests the
specific material needed: source, action, state or interval, and the decision it
will support. You may supply a recording or permitted resource package; the agent
continues the inspection, comparison and adaptation. Unresolved quality gaps stay
explicit, with their impact and feasible choices.

## Confirm a consequential direction

For a substantial redesign, the agent first identifies how people will use the
product and what is already accepted. It preserves business/engineering assets
while assessing visual candidates against the new target. When several plausible
models would materially change the experience, it offers a recommendation, a
small set of distinct options and useful references or previews.

You can choose the experience that matches your intent. Component details remain
agent work. Clear existing intent or explicit delegation supports direct progress;
one-shot recommendations retain their provisional scope. The preview is delivered
with a [design/resource record](DESIGN-DECISIONS.md) linking consequential sources
to actual surfaces and observed results. Try the [worked study](../examples/product-intent/README.md).

## Design with visual assets

The seventh common reference brings assets into the initial professional context.
The agent identifies material that carries meaning, identity or composition, then
researches mature candidates and chooses an appropriate production route. Asset
findings can improve the layout. Important identity directions use comparable
previews; normal adaptation follows the accepted direction.

[The asset guide](VISUAL-ASSETS.md) covers marks/icons, type/glyphs, images,
spatial work and dynamic assets. Masters, exports and placements remain linked.
The [review fixture](../examples/asset-review/README.md) demonstrates a scoped,
actual-browser check of image variants, small icons, motion and unavailable media.

## Give a professional product an expressive direction

```text
Keep the research workspace's reliable tasks and data. Develop a distinctive
artistic direction that remains visible in the populated input, results and
navigation. Research functional references, cross-domain visual work and mature
implementations together. Show meaningful options where direction is still open,
then trial the defining assets with real components and carry the chosen direction
through the working journey.
```

The agent develops an art direction specific enough to change subject,
composition, typography, material or motion. Options use representative content
and comparable production care. Familiar task relationships can survive changes
to position and form; real operation establishes that they do.

A visual system gives expressive titles, reading text, main assets, controls and
motion distinct roles within one coherent language. Actual assets and mature UI
resources carry those decisions into the product. A specific reading, input or
runtime problem calls for a targeted repair, followed by checks of both use and
the retained direction. The [art-direction guide](ART-DIRECTION.md) explains this
method, including source fidelity and separate product, demonstration and authored
output boundaries.

## Design content with the screen

When adding or revising a page, establish the audience's next question and the fact owner before writing visible strings. Study comparable product wording where it helps, then decide headings, labels, help, status, tone and actual placement with the layout. Use short, typical and long strings in each supported language. Run the task, including failure and recovery, to verify that copy matches actual behavior. The [content reference](../skills/ui-spec/references/content-design.md) provides the shared judgment method; a [working example](../examples/content-review/README.md) covers localized local-save states.

## Observe the frame, the change and the journey

[Product alignment and active exploration](PRODUCT-ALIGNMENT.md) are part of ordinary design work. The agent turns uncertain product relationships into research questions, then follows useful clues: play a demo, scroll a region, change a tab, open and close a panel, or compare a variant. Inspect composition, states and relationships at the depth each decision needs. Routine members of a researched component family can inherit the established rule.

Attribute evidence to its actual subject: hosting page, player, demonstrated product or edited content. Pair design-reference questions with implementation candidates and use each to improve the other. Important choices show what was viewed, what it means for the current task and which actual implementation carries the relationship.

For changing UI, follow the trigger, first feedback, progression and settled outcome. Extend the window for return, interruption, repetition, waiting or loop boundaries when useful. Choose live interaction, video and ordered frames by the question and host capabilities; distinguish capture, actual viewing, supported conclusions and approval.

Give motion a semantic role: what relationship forms, what updates and where
attention settles. Deterministic timelines can support repeatable authored-output
or regression comparisons under recorded conditions; normal runtime still needs
its own interaction and pacing evidence. Check encoded playback for timed works,
and preserve meaning and identity in reduced-motion or static presentations.

Use the local trial to resolve consequential resource fit before broad integration. Revisit the same questions with real content, matching interaction stages and useful viewing conditions. Begin with the normal-scale whole, examine composition, functional regions and consequential details, then return to the complete result. Choose perceptual dimensions that can change a decision and connect visible facts to likely effects, explanatory hypotheses and actual resource/adaptation choices.

When adaptations change type, material, space or state behavior, recheck the affected relationship and its neighbors. Review the assembled product across related views and continuous use; detail crops and enlarged frames support their stated scope. A mismatch can reopen resource selection, adaptation, content structure or the experience target. Carry unresolved evidence gaps into the next relevant check. The [visual observation method](VISUAL-INSPECTION.md) supplies the inspection details.
