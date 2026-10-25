# Guide: a multi-round interface project

## 1. Begin with the goal and real project

A useful opening prompt is:

```text
Use ui-spec: init. This is an existing research workspace.
Keep its framework and working API. Inspect its routes, user tasks and current
screens. Establish a coherent UI direction and implement the first useful slice.
```

The agent reads all eight common references, then the code, project instructions and accepted decisions. It identifies how people start, what they work on and how the task continues. Product UI Experience Alignment establishes the intended experience from real tasks, content and operating conditions. If the user supplies a product name, the agent expands it into relevant pages, flows and qualities; otherwise it proactively finds mature patterns, design systems and implementation sources. Both entry points establish a primary model through actual exploration. When material alternatives remain open, optional shape presents a reasoned recommendation and a focused choice or representative preview. An implementation request with clear direction continues into a meaningful slice. The following collection/detail examples assume that this direction has been selected for the actual task.

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

New components are selected by actual role. An accessible popover primitive, an icon set and a decorative background can come from different sources while sharing the project's tokens and behavior.

## 4. Inspect rendered evidence

A useful round report contains the working preview entry, scope, selected components when new, observed checks, captures and pending review items. The agent opens the captures and uses the interface.

Three independent comparisons matter:

| Comparison | Questions |
|---|---|
| Across viewports | Are text, controls, composition, density and content access appropriate? |
| Across related pages | Do shared headers, navigation, content origins and interaction conventions remain stable? |
| Across states | Do selection, focus, input and visual continuity survive changes? |

Language/theme/role variants extend the matrix where supported. A compact sign-in view, a long article and an operational workspace use different composition and scrolling rules.

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
for its important visual and interaction needs, adapt the most suitable parts to
the accepted direction, and verify the composed result.
```

The same behavior is part of ordinary `continue` requests. The agent can use the
[resource map](../skills/ui-spec/references/resource-catalog.md), official indexes,
exported configurations, actual demos/source and available tools. It chooses the
reuse level and reports only consequential decisions with the working result.

For targeted inspection, the installed optional helper works from any directory:

```bash
python <skill-dir>/scripts/find_resources.py --need motion --stack vue --json
python <skill-dir>/scripts/find_resources.py --id fontsource --json
```

Discovery leads retain their source and review date. Demo inspection and actual
project checks are recorded separately. Existing approved resources remain useful
while their conditions fit; a new requirement can justify a fresh comparison.
See [the resource workflow](RESOURCE-REUSE.md) for examples and maintenance.

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

## Design content with the screen

When adding or revising a page, establish the audience's next question and the fact owner before writing visible strings. Study comparable product wording where it helps, then decide headings, labels, help, status, tone and actual placement with the layout. Use short, typical and long strings in each supported language. Run the task, including failure and recovery, to verify that copy matches actual behavior. The [content reference](../skills/ui-spec/references/content-design.md) provides the shared judgment method; a [working example](../examples/content-review/README.md) covers localized local-save states.

## Observe the frame, the change and the journey

[Product alignment and active exploration](PRODUCT-ALIGNMENT.md) are part of ordinary design work. The agent turns uncertain product relationships into research questions, then follows useful clues: play a demo, scroll a region, change a tab, open and close a panel, or compare a variant. Inspect composition, states and relationships at the depth each decision needs. Routine members of a researched component family can inherit the established rule.

Attribute evidence to its actual subject: hosting page, player, demonstrated product or edited content. Separate design references from implementation resources, and use the observed relationship to find an appropriate reusable foundation. Important choices show what was viewed, what it suggests for the current task and which part the implementation inherits.

For changing UI, follow the trigger, first feedback, progression and settled outcome. Extend the window for return, interruption, repetition, waiting or loop boundaries when useful. Choose live interaction, video and ordered frames by the question and host capabilities; distinguish capture, actual viewing, supported conclusions and approval.

Build a runnable slice once the important choices have evidence and an adaptation path. Revisit the same questions with the product's real content, matching interaction stages and useful viewing conditions. Review the assembled product across its related views and states. Carry unresolved evidence gaps into the next relevant check. The [visual observation method](VISUAL-INSPECTION.md) supplies the inspection details.
