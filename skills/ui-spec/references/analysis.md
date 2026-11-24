# Analysis: decide what is worth building

## Contents

- [Establish the product's target experience](#establish-the-products-target-experience)
- [Nine dimensions, one coherent experience](#nine-dimensions-one-coherent-experience)
- [Formulate an inspectable aesthetic direction and reference craft breakdown](#formulate-an-inspectable-aesthetic-direction-and-reference-craft-breakdown)
- [Plan evidence around the experience](#plan-evidence-around-the-experience)
- [Use theory to investigate real design work](#use-theory-to-investigate-real-design-work)
- [Recognize the product through its use](#recognize-the-product-through-its-use)
- [Establish the reuse boundary for this assignment](#establish-the-reuse-boundary-for-this-assignment)
- [Confirm consequential direction with useful options](#confirm-consequential-direction-with-useful-options)
- [Lead users at different levels of design direction](#lead-users-at-different-levels-of-design-direction)
- [Reason about uncertainty](#reason-about-uncertainty)
- [Define each surface by responsibility](#define-each-surface-by-responsibility)
- [Choose a bounded increment](#choose-a-bounded-increment)
- [Govern the multi-SPEC horizon and retire obsolete scope](#govern-the-multi-spec-horizon-and-retire-obsolete-scope)
- [Design the understanding before the arrangement](#design-the-understanding-before-the-arrangement)
- [Choose a representation before a component](#choose-a-representation-before-a-component)
- [Organize actions, content and operating life](#organize-actions-content-and-operating-life)
- [Read references as mechanisms and carry decisions forward](#read-references-as-mechanisms-and-carry-decisions-forward)
- [Coordinate auxiliary research](#coordinate-auxiliary-research)

## Establish the product's target experience

Begin **Intent-Grounded Experience Research** with the user's intended work and quality. Use **Product UI Experience Alignment** to connect that understanding to mature evidence, adopted implementations and verified use. Keep explicit aesthetic goals alongside behavior, accessibility and business requirements. Artistic impact remains a delivery requirement in professional software; task familiarity concerns recognizable objects, actions and outcomes, while composition and material can develop an independent identity.

Treat a product name as a compressed experience description. Unpack the relevant application, website, task, information structure, visual character and continuous interaction. “Like a conversational AI product” might concern task entry, attachments, history, answer reading or a companion workspace. Examine what the user expects to inherit and where independent expression is welcome; do useful research before asking about consequential ambiguities.

Establish **this user's intent** from stated preferences, references and prior choices; investigate **audience expectations** through research, tutorials and established practice; verify **reference-product facts** through documentation and observation. Keep these three bases distinct. A group's habits do not establish personal preference; recollection may refer to an earlier version. Select version, platform, role and plan by the intended experience, retaining uncertain attribution as a research question.

Form revisable experience hypotheses from the brief, product context and design knowledge. Separate confirmed goals, supported conventions, assumptions and questions whose answer could alter the interaction model, page structure, art direction or resource choice. Without a named reference, seek mature task-level and cross-domain evidence proactively. Preserve proven semantics and suitable assets in upgrades; test novel combinations in context.

Maintain an **Experience Alignment Model** as a concise account of the primary task/objects, familiar relationships worth inheriting, defining visual and temporal qualities, independent expression and unresolved judgments. Explain why those relationships matter and what would validate them. Its form follows the task; update existing records as evidence changes the account. Judge qualities and fit rather than resemblance percentages.

## Nine dimensions, one coherent experience

Use these dimensions together, grounded in user outcomes, authoritative facts, inclusive use and observation. Focus depth on questions that can change the result. The dimensions identify objects; the eight common references supply methods.

| Dimension | What to establish | Effect on the work |
|---|---|---|
| Product and interaction model | People, primary objects, recognizable task loop, real choices, roles and outcomes | Choose a meaningful surface and its operating relationships |
| Visual design and art direction | Hierarchy, character, material, composition and craft target | Establish a coherent direction and compare mature foundations |
| Visual assets and asset engineering | Identity, type, imagery, spatial/dynamic material, production and delivery | Let suitable assets shape the concept and reach the final placement |
| Content design and typography | Needed understanding, factual authority, voice, placement, language and text weight | Compose real messages with the reading and action path |
| Layout and spatial composition | Proportions, stable anchors, responsive behavior, motion envelope and content growth | Allocate space and choose scroll ownership by task |
| Components and interaction states | Semantics, actual choice space, materials, input methods and complete states | Preserve understandable and accessible behavior |
| Motion and interaction continuity | Object identity, transitions, timing, interruption and feedback | Express real changes while retaining orientation and control |
| Performance and experience engineering | Input-to-result path, readiness, scheduling, loading, resource cost and recovery | Improve repeated work and verify gains under stated conditions |
| Operational UX and sustainable content | Content sources, editing roles, templates/overrides, bulk work and lifecycle | Keep routine maintenance efficient and published results reliable |

Follow cross-dimensional effects: content reshapes navigation, assets affect composition, latency changes preparation, and maintenance changes editing flows. Use [content](content-design.md), [principles](principles.md), [assets](visual-assets.md), [interaction](interaction-and-variants.md), [verification](verification.md) and [integration](integration.md) together.

## Formulate an inspectable aesthetic direction and reference craft breakdown

Before searching implementation libraries, decompose top-tier product, editorial and cross-domain visual references into **concrete, inspectable craft mechanisms**. Doing this first ensures your taste bar governs multi-tier component discovery rather than letting the first convenient package dictate a generic default aesthetic.

Extract six structural and perceptual specifications from observed references:

| Craft layer | Concrete mechanism to extract before sourcing |
|---|---|
| **Spatial skeleton & occupancy** | How canvas, navigation chrome, primary work region and negative space proportion themselves at desktop and mobile (`390px`) first screens—including reading measure and column rhythm. |
| **Typographic pairing & tension** | Display, body and tabular/mono font roles, size jumps, weight contrast, tracking and line-height cadence that carry editorial or utilitarian voice. |
| **Surface luminance ladder** | Distinct elevation steps (canvas → raised panel → inset control → overlay) calibrated separately for light and dark themes using cohesive neutral tinting rather than raw black/white inversion. |
| **Hairline, shadow & radius grammar** | Border contrast, directional top-edge highlights, ambient-plus-contact shadow hierarchy and concentric corner nesting (`R_outer = R_inner + padding`). |
| **Signature focal craft moment** | The deliberate visual centerpiece—tactile material, crisp editorial typography, spatial lighting or purposeful motion choreography—that separates the surface from an interchangeable template. |
| **Motion & responsiveness character** | Easing curves or spring weight, shared-anchor continuity, interruptibility and reduced-motion poise. |

Derive the overarching concept from audience, subject, emotion, task and available visual material using [art direction and expressive contrast](principles.md#art-direction-and-expressive-contrast); let defining assets ([visual assets](visual-assets.md)) participate while composition is still fluid. When a brief asks for “refined,” “tactile,” “expressive” or “mature” UI, translate each adjective into the visible/interactive relationship it requires, then turn it into a concrete **resource question**: which mature page, block, visual component or asset already resolves this relationship? Keep **reuse scope**, **observed visual completeness** and **functional dependencies** distinct—do not infer visual quality from the tech stack or product category. Let an initial craft question open discovery rather than lock one mechanism prematurely (for example, testing whether moving light around stable content, editorial typography or a photographic subject best carries the goal), allowing a strong mature resource to elevate the initial hypothesis.

## Plan evidence around the experience

Map the important **parts, states and relationships** across the task: pages, regions, working objects, transitions, content growth and device conditions. Prioritize questions that could change the product model or overall direction, then investigate consequential structures and details. Findings at any scale can reopen another scale. A companion panel changes input continuity, reading width, focus and layout; evidence about the panel alone leaves those relationships open.

| Question | Useful evidence | What to establish |
|---|---|---|
| Why and how people use it | Product/help material, research, tutorials and relevant feedback | Meaning, task, roles, conditions and familiar working patterns |
| How the task and information connect | Actual use, complete pages and connected flows | Entry, objects, navigation, continuation, result and recovery |
| What creates perceived quality | Real renders, comparable work, detail views and design systems | Composition, hierarchy, type, material, assets and optical relationships |
| How change is experienced | Operable demos, recordings and viewed sequences | State feedback, timing, continuity, interruption and repeated input |
| What can carry the target into this project | Original demos, source/docs, rights and local trials | Actual reuse, adaptation, retained quality and operating cost |

Use **text, visual and behavioral evidence** together. Text explains purpose and conditions; rendered views support appearance; operation and time sequences support interaction. Follow a documented mechanism to its observable interface, and investigate a visual discovery through its semantics and implementation. Retain date/version, platform, role and viewing conditions where they change applicability. Promotional editing, isolated stills and source code each support their own scope.

For consequential choices, organize coverage and decisions through the [design evidence map](evidence-map.md): **L0** intended experience, **L1** journeys, **L2** page/region architecture, **L3** functional regions/components, **L4** perceptual relationships and **L5** realization/assurance linked at every scale, with state/time, conditions, shared dependencies and evidence tracked as cross-links rather than forced into a single tree. Run **Coverage Discovery & Challenge** from both directions—derive coverage from user tasks, then challenge it against real mature-product navigation, tutorials, states and continuous use, recording *include*, *exclude with reason* or *open question* decisions so a self-consistent initial list never disguises omitted flows. Group consequential choices into **Design Decision Units** (purpose, question, actual evidence, judgment, materially different alternatives, implementation/adaptation, verification/next action) sized by impact and uncertainty rather than per CSS property; a verified routine family can inherit a short scoped decision under matching conditions.

## Use theory to investigate real design work

Turn hypotheses into questions that can change a choice. Apply the [perceptual method](principles.md#inspect-from-whole-to-detail-and-back) from normal-scale whole through structure and detail, then back to use. Explain which relationships produce the impression and which causes need testing. A bright panel may outweigh the task; retained selection may preserve orientation. Find mature implementations that can preserve the useful relationship and test it in context.

Let each observation determine a useful next action: explore a newly important font, inspect a hidden state, compare another interaction model or trial a mechanism. Product, component, asset and design-language research can change one another. Keep reference, original demo, local trial and journey evidence distinct; [verification](verification.md) owns observation conditions and claim limits.

## Recognize the product through its use

Identify the first meaningful action, primary object, repeated action/result loop, continuation and durable outcome. Product names, feature inventories and engineering labels describe capabilities; the user's working relationships determine the interaction model. A “research workbench” can center on conversation, documents or tasks. Observe flows and read capability contracts before choosing the surface.

Describe use concretely: “ask, examine a sourced answer and continue the thread,” or “edit a record and return to the filtered collection.”

| Model candidate | Strong user-level signals | Consequences to investigate |
|---|---|---|
| Conversational assistant | Intent starts in a composer; responses lead to follow-ups | Threads, readable answers, persistent input, generation/stop/retry, sources/artifacts |
| Document / information space | People create, organize, edit and revisit durable objects | Collections, editing, search, linking and object continuity |
| Task / operational system | People prioritize, assign and advance work items | Lists/boards, status, filters, detail, progress and repeated operations |
| Canvas / editor | People directly manipulate an artifact | Selection, tools, properties, undo and spatial continuity |
| Discovery / decision flow | People search, compare and commit | Collections, comparison, detail, consequences and recovery |
| Reading / publication | People follow an argument or locate an answer | Narrative order, headings, evidence and a useful next action |

Treat these as hypotheses; include other models when needed. A hybrid identifies its primary loop and each secondary surface's purpose, task and state owner. Product model, local page shape and visual language remain separate choices. Compare starting points, actions, results, continuation and recovery under relevant conditions; retain the sources and states actually examined.

## Establish the reuse boundary for this assignment

Identify the request as a local improvement, visual refresh, interaction redesign or combined redesign; clarify only a consequential ambiguity. Preserve business rules, data contracts, permissions and necessary capabilities. Evaluate existing presentation and external candidates against the same target using [component sourcing](component-sourcing.md); catalog leads always require project verification.

Code establishes current capability; explicit acceptance establishes approved design. Link visual inheritance to that acceptance or a current fit assessment. Keep suitable internal work and change its presentation where the task benefits. Scope framework and architecture changes to the required experience.

## Confirm consequential direction with useful options

Check whether credible alternatives would change the primary action, information architecture, enduring working object or overall identity. When unresolved choices reshape substantial work, offer a small set of distinct directions, a recommendation and the practical tradeoff before extending the shell or page family. One well-supported direction may suffice.

Compare the same task and content at comparable completion. Hold incidental styling steady for interaction-model comparisons; for art direction, show material differences in assets, composition or motion. Use actual renders or runnable fragments, including populated core use. Color swaps or unequal polish cannot establish a fair direction comparison. The user resolves consequential open choices; routine implementation remains agent work.

Established intent, approval or delegated autonomy supports direct progress. One-shot work retains its assumptions, unresolved alternatives and pending owner acceptance. Prototype preference and formal approval keep their actual scope. Continue independent work while a significant choice is pending.

## Lead users at different levels of design direction

A goal-only request calls for agent-led product analysis: infer plausible tasks and interaction models, research comparable flows, explain the strongest reviewable direction and preserve the uncertainty that could change it. A named reference may express an exact interaction, a visual quality, a familiar product model or a technical constraint. Determine which parts are binding rather than treating every visible detail or the product name as an instruction to copy its shell.

For a detailed brief, preserve stated priorities, accepted decisions and supplied materials; investigate gaps that affect delivery without asking the user to repeat established direction. For a partially directed request, make low-impact reversible decisions, present concise evidence-backed alternatives only where a different choice would materially affect the product, and continue independent work. Ask for an unavailable fact or authorized asset when it determines a consequential commitment. User input selects the desired outcome; professional analysis, ordinary sourcing, component choices and implementation detail remain agent responsibilities.

Contrast the current user's stated expectation with audience conventions and the reference product's actually observed version and behavior. If the evidence revises the original experience hypothesis, explain which task, navigation, status, content or aesthetic decision changes before expanding implementation.

## Reason about uncertainty

Match evidence to uncertainty: task/content research for product questions, viewed compositions/sequences for visual questions and isolated trials for implementation fit. Consequential commitments require authoritative facts or authorization. Test reversible assumptions visibly and resolve constraints that could invalidate broad work early.

Allocate exploration by **design impact, current uncertainty and potential improvement**. A defining font, background, 3D asset or interaction may warrant many independent sources and sustained, hundred-step or hour-scale research. These are available capabilities, not quotas. Small size does not imply low impact; routine work with demonstrated fit can move directly to adaptation. Keep effort within the user's scope and execution constraints while preserving unresolved quality gaps.

Use evidence maturity to choose the next action:

| Next action | Evidence needed and question it answers |
|---|---|
| Continue research | A high-impact goal, interpretation, state or alternative remains unsupported, or discoveries could materially improve the choice |
| Run a bounded local trial | The target and candidate have a credible basis; current-project composition, behavior or cost is the uncertainty the trial can resolve |
| Expand implementation | Important qualities and materially different alternatives have been examined, consequential trials demonstrate fit and adaptation is clear |

Judge target understanding, appropriate evidence, explored directions, comparison quality, implementation basis and remaining uncertainty together. Repeated similar results support convergence only after consequential questions and alternative directions have been examined. An unmet explicit art/experience goal remains a reason to investigate. Search effort alone cannot settle it.

If access or fit remains unresolved, choose alternative evidence, focused user assistance, a bounded trial or scoped design revision by its likely learning value. Original construction requires a qualifying [W1–W3 exception](component-sourcing.md#closed-original-construction-allowlist) with actual authorization; learning value and search failure do not supply that authority. State consequential limitations and preserve the actual quality target. New evidence or an unsuccessful trial can reopen understanding and selection at any stage.

## Define each surface by responsibility

Establish audience/role, job, main action, content/states, entry, continuation, shared shell and data owner. Merge surfaces where task, authority and lifecycle are shared; distinguish responsibilities through meaningful navigation, URLs and task-local actions.

A state graph or brief transition account can expose control, precondition, destination, retained context and result. Include return, retry, cancellation and recovery. Preview state selection establishes appearance; actual controls establish continuity. For example, sign-in may retain a draft and return target before resuming a server-validated save.

## Choose a bounded increment

Choose an outcome that can run, be inspected and be revised coherently: a page, journey, family or systemic repair. Weigh task/accessibility blockers, shared defects, missing paths and design-affecting integration against explicit goals, reach, dependencies and learning value. “Continue” resumes from accepted scope, incomplete journeys and observed defects; state the useful next outcome briefly.

### Find the minimum sufficient experience closure

Use **Minimum Sufficient Experience Closure** to define a formal SPEC: include the coupled design objects and relationships needed to understand, realize and judge one cohesive experience or visual-quality goal, while preserving focus for deep research and craft. “Minimum” excludes unrelated independent responsibilities—not small area or code size. “Sufficient” covers this goal's necessary relationships—not the entire product lifecycle.

Distinguish the **Visible Surface**, its **Visual Quality-Bearing Objects** and the **Experience-Cohesive SPEC** connecting them. A conversation workspace's quality may lie in continuous coordination across a growing composer, changing message height, streamed content and scroll following—so a SPEC owning that continuity keeps those state, space and time relations together even when component files differ. Conversely, a signature background art study can stand as its own formal SPEC while returning to the workspace for foreground legibility and motion verification.

| Boundary factor | Consequence for scope |
|---|---|
| Visual complexity | High-craft typography, material, lighting or asset work may warrant its own increment even in a small object; a large conventional region may inherit a verified system. |
| State and time complexity | Include trigger, changing states, async feedback, interruption, reversal and recovery needed to judge the episode. |
| Cross-component dependency | Keep coupled size, position, focus, scroll and state mechanisms together regardless of module boundaries. |
| Research uncertainty | Focus investigation on unresolved high-impact questions; settle product-level direction before locking local slices. |
| Mature-resource fit | A cohesive mature block or template can unify related responsibilities; unrelated craft sources may separate cleanly. |
| Quality impact & verification | Give defining qualities a scope where actual contextual renders or continuous episodes—not just a distant full-page screenshot—can prove them. |

Weigh these factors as professional judgment; page area, component count, feature count, search steps or complexity scores never determine formal standing.

### Keep, split, merge or redraw with evidence

| Choice | When it helps | What to preserve and explain |
|---|---|---|
| **Keep** | Cohesive goal, understood relations, fitting mature work and adequate depth for owned qualities. | State the closure and observation conditions; a larger well-supported scope can be appropriate. |
| **Split** | Independent goals each require concentrated research, craft or verification that combining would dilute. | Retain the overall product goal, explain each slice's experience value/dependencies and keep deferred goals visible. |
| **Merge** | Separately planned objects share the state, spatial or temporal mechanism creating the intended experience. | Own and inspect the coupled relation together (e.g., composer-to-streaming continuity, or card flip + data readiness + neighboring layout). |
| **Redraw** | Research, source discovery, trials or integration expose a missed relation or mixed responsibilities. | Record what changed, why, affected goals/quality gaps, current responsibility and effect on later candidates. |

For example, a conventional settings page built on an already inspected system can stay one SPEC, whereas a specialized permission workflow or dense typography problem can split it; an entire fitting mature workspace implementation can unify a formerly split plan once its adaptation and verification needs are understood. Explain the concrete quality risk when revising an unsuitable single-iteration scope. Routine evidence-supported adjustments use existing authority; material shifts to accepted commitments are surfaced to the user while independent authorized work continues. Repartitioning never marks unfinished quality complete.

### Connect source responsibility, three scopes and quality ownership

Before formal visual implementation, connect each owned quality to the mature source that carries it—preserving coherent page/block/system provenance rather than stripping simple CSS pieces out to hand-build them. Source discoveries can merge or narrow a SPEC while keeping the complete goal and any unresolved source gap explicit under [default-deny sourcing](component-sourcing.md#preserve-unresolved-responsibilities). Keep three overlapping scopes distinguishable: **Research & Observation Scope** (broader products/states studied for context), **Primary Design & Implementation Scope** (the increment's promised objects and relationships) and **Integration & Regression Scope** (neighboring regions, shared systems and journeys checked for side effects).

State the increment's concrete visual and interaction quality obligations with review conditions that actually reveal them, tracing **target quality → real visual reference → mature resource, faithful authorized design translation or qualifying authorized W1–W3 implementation → actual presentation in the current product → remaining quality gap**. For a new product, choose a first closure that demonstrates core experience and visual direction at a caliber worth inheriting—keeping unfinished features visibly truthful and never letting an exploratory rough probe silently become the shared foundation.

### Govern the multi-SPEC horizon and retire obsolete scope

Over multi-month product evolution spanning dozens of increments, manage candidate and past SPECs as a **living horizon** over one evolving product rather than a static initial plan or an append-only archive of historical rounds. Use descriptive dispositions to make each increment's current role clear across sessions and engineers:

| Disposition | Meaning in the living horizon |
|---|---|
| `candidate` | A proposed future closure whose scope, dependencies and priority remain revisable as evidence develops. |
| `active` | A formal UI SPEC currently owning research, implementation or verification work on the product. |
| `completed` | A delivered increment whose design commitments and adopted work remain active in the current product. |
| `superseded` | A prior SPEC whose direction, interaction model or shared foundation has been deliberately replaced by a newer increment. |
| `consolidated` | A formerly separate SPEC merged into a unified workflow or shared foundation increment. |
| `retired` | An increment whose UI surface or product capability has been removed from the active product. |

These dispositions are descriptive planning facts kept in the project's existing design records—never a rigid ticket state machine, a SPEC-count quota or a structural inspector gate.

**Sequence by user value, dependency and leverage.** Order candidate SPECs using three complementary criteria alongside user urgency:

- **Cross-SPEC dependency:** place shared application shells, primary navigation frames, semantic token or typography systems and blocking domain contracts ahead of downstream consuming routes when leaving them unresolved would force systemic rework across many surfaces.
- **Risk-reduction leverage:** when a shared visual system, mature component family or complex interaction pattern carries high uncertainty, validate it first on one representative high-signal anchor slice with realistic content and states before expanding across remaining routes.
- **Parallelizable boundaries:** identify independent candidate increments with disjoint surfaces, non-overlapping source modules and stable shared contracts that can advance concurrently across engineers or isolated worktrees without artificial serialization. Name the shared interface boundary before parallel work begins so concurrent increments do not drift apart.

When a foundational SPEC changes an assumption relied upon by queued candidates—such as navigation depth, typography measure, theme structure or state ownership—re-check only the affected candidate boundaries and dependencies instead of discarding or rewriting the entire horizon.

**Reprioritize on evidence and retire obsolete scope safely.** Concrete triggers that warrant reshaping the horizon include shifted product priorities, newly surfaced backend or service constraints, discovery of a mature resource that cleanly unifies several planned slices, or operational evidence from live use. Whenever superseding an earlier SPEC, consolidating two workflows or retiring an obsolete UI surface, apply a three-part safety rule:

1. **Account for valid user task paths:** establish where every still-valid user task, entry point, deep link or recovery path moves in the successor surface, or confirm explicit product removal of that capability.
2. **Transfer or explicitly close owned obligations:** trace every visual quality commitment and unresolved debt item owned by the departing SPEC—either transfer it to the successor SPEC with unbroken provenance and reopen triggers, or close it as obsolete with the concrete product cause recorded in `Meaningful Revisions` ([Current model, meaningful revisions and evidence archive](evidence-map.md#current-model-meaningful-revisions-and-evidence-archive)).
3. **Remove orphaned UI from the active product:** delete dead navigation entries, stale internal links, orphaned controls and contradictory copy from the `Current Product UI` so the live interface never contradicts its active architecture.

## Design the understanding before the arrangement

Identify arrival knowledge, the next needed understanding, supporting evidence and reasonable action. Give regions communication roles: orient, explain, compare, substantiate, decide, act or recover. Choose words, imagery, diagrams or manipulation by the question answered. A README may place fit, installation and use before architecture; a workspace may pair action and evidence.

Compose representative content early. Preserve factual and authored meaning while improving order, names, units, expression and localization. Keep facts, hypotheses, illustrative values and promises distinguishable.

## Choose a representation before a component

Match the person's cognitive operation to a useful form; inspect mature examples before selecting an implementation.

| Needed understanding or operation | Candidate representation | Check before choosing |
|---|---|---|
| Compare properties across objects | Aligned table, comparison rows or coordinated small multiples | Comparable units/order, missing values and narrow-screen reading |
| Find an item in a collection | List/grid with filters and selection | Distinguishing attributes, density and retained query context |
| Understand dependencies or transitions | Diagram, timeline or explicit state presentation | Correct direction, guards, cycles and a readable alternative |
| Inspect the basis for a claim | Claim/evidence pairing, citation or coordinated panes | Provenance, visible association, permissions and return |
| See how a parameter changes a result | Direct manipulation with timely feedback | Safe bounds, authority, latency and reversibility |
| Learn a sequence | Ordered steps, worked example or progressive disclosure | Prerequisites, exceptions, recovery and actual ordering needs |

These are candidates, with fit established through content and use. A strong resource can refine the representation. A graph earns its complexity when topology aids the task. Distinguish categories, quantities, sequence and uncertainty; preserve units, scale, baseline and missingness. Label simulated charts as fixtures.

## Organize actions, content and operating life

- **Objects, actions and real choices:** associate recognized objects, information, actions and feedback; preserve object identity through movement, expansion and return. Inventory actual choices (alternatives need selection, a single valid value needs clear display, an earlier choice needs a summary and permitted revision) and establish primary/secondary, peer, sequential or consequential weight before styling.
- **Content authority with the product model:** establish fact ownership and needed understanding at every step; study mature product language alongside visual references while aligning consequential terms with their business owner ([content method](content-design.md)).
- **Operating life and maintenance:** establish content owners, update cadence, repeated workload and templates-vs.-overrides behavior (exposing effective content and blast radius). Derive batch work from real scale, selection and recovery, expressing authoritative state appropriately for consumers vs. operators ([integration](integration.md)).

## Read references as mechanisms and carry decisions forward

Explain visual impressions through observed attention, proportion, material and rhythm while keeping inferred causes and audience effects labeled as hypotheses. For an opening companion panel, inspect width, retained input/selection, reading measure, focus and transition—preserving the continuity relationship through suitable mature resources verified under current content.

Preserve authoritative boundaries: intent sets the goal, approval sets accepted design, source/runtime establishes capability and tests cover their exercised checks. Connect consequential choices to intent, evidence, inferred mechanism, adopted source, tradeoff and recheck, keeping representative viewed frames or intervals beside the preview and exposing adjustable controls via canonical tokens, content, variants, composition, focal points and timing.

## Coordinate auxiliary research

When a high-impact unknown warrants independent multi-tier discovery, deeper perceptual/temporal capture or an adversarial challenge to a leading direction, apply [delegation guidance](delegation.md). Frame coherent questions that protect coupled experience relationships, keep research breadth distinct from formal SPEC boundaries, and retain product-level synthesis, scope decisions and final source selection in the main agent.
