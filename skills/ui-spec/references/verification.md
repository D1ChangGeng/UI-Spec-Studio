# Verification: coverage, inspection and honest evidence

## Contents

- [Coverage and assurance](#build-the-coverage-inventory-from-reality)
- [Evidence sufficiency](#judge-evidence-for-the-decision)
- [Viewing conditions and actual interaction](#capture-the-actual-viewing-condition)
- [Temporal visual inspection](#inspect-a-time-bounded-visual-episode)
- [Tools for the question](#choose-methods-for-the-evidence-question)
- [Findings, comparison and status](#findings-and-repair)
- [Multiscale judgment](#inspect-from-whole-to-detail-and-back)
- [Publishing and resource adoption](#verify-the-publishing-medium)
- [Decision, asset and content evidence](#verify-the-design-decision-chain)
- [Performance and operational change](#measure-performance-across-the-complete-task)

## Build the coverage inventory from reality

Reconcile routes, navigation, roles, overlays, runtime states and UX records. Include every in-scope page family; missing entries are findings. State how data shapes, lengths and permissions are sampled.

Report scope: a round checks changes and affected dependants; final acceptance reconciles the full approved inventory.

Declare supported viewports and theme/locale combinations from target use. Inspect every route's primary state at every declared viewport and variant. Exercise each additional critical state in every declared variant, extending viewport coverage where layout or risk differs. Preserve user-requested exhaustive coverage and record approved exclusions with their reasons. Include short heights and actual narrow-input conditions where supported; fixed dimensions are project choices.

Include temporal relationships: trigger, meaningful progression, stopping condition and return/recovery. State inventories locate scenes; episodes connect them.

## Match assurance to impact

Check local changes in context, shared changes across dependants and journeys through transitions/recovery. Integration needs visual and business evidence; depth follows consequence, variability and decision value.

Explain sampling and remaining conditions. Package checks, scenarios, viewed pixels, executed interactions, user research and real integration establish different facts; comparative model evaluations are separate research.

## Judge evidence for the decision

Choose the next observation by the unresolved experience question. Assess these dimensions together, at the scope of the proposed decision:

| Dimension | What sufficiency means |
|---|---|
| Coverage breadth | Important parts, states, views, alternative directions and relationships have a relevant basis |
| Inspection depth | The consequential composition, type, material, proportions and details have actually been examined |
| Temporal coverage | The observed process covers the behavior claimed, with gaps and sampling limits retained |
| Evidence relevance | Conditions and subject answer this product's question, including its user's intended version or platform |
| Evidence reliability | Origin, date/revision, platform, role/plan, editing and viewing conditions support the conclusion |

Quantity cannot compensate for a missing dimension. Multiple reposts share an origin; a detailed still leaves movement unresolved. Separate actual observation, source statements, professional inference and missing evidence. Corroborate consequential claims through appropriate text, renders or operation; preserve conflicts for investigation rather than silently merging versions or users.

Before broader implementation, revisit target understanding, explored alternatives, the observed reason for selection, implementation fit and uncertainty that could overturn it. A bounded trial can resolve fit without claiming the target is already met. After integration, check experience alignment, visual craft, distinctive expression and engineering reliability on the real task; carry residual gaps at their own scope. The [analysis](analysis.md) and [sourcing](component-sourcing.md) methods guide whether further discovery or trial is valuable.

## Capture the actual viewing condition

Set the CSS viewport directly; record viewport, pixel ratio, browser, locale/theme, content, revision and zoom. Distinguish browser/text enlargement from image scaling; inspect the actual route or independently sized frame at useful scale.

Wait for intended content, fonts and images for steady states; keep data and animation phase comparable. Begin loading/transition capture before the event. Include shell, background and surrounding space in the whole viewport; browser chrome is optional.

Use **viewport evidence** for composition/scroll boundaries and **content evidence** for documents or scroll checkpoints. Inspect internal regions without resizing the viewport; exercise sticky controls, overlays, short heights and intended horizontal scrolling. Full-document capture can place fixed overlays incidentally; check an actual viewport before diagnosing loss.

Record video dimensions/scaling separately. [Playwright video](https://playwright.dev/docs/videos) can scale output and needs context closure to finish writing. Retain full-size stills for small type or optical detail.

Record display scaling. Fitted pages/contact sheets support overview; reading and optical judgments need intended use scale. Retain crop location and neighbors; return from enlargement to normal scale to judge its effect.

## View the images and use the interface

Open required images and relevant video/ordered frames. Files, DOM snapshots and capture commands establish availability; visual inspection requires viewing pixels. Select perceptual dimensions from the actual subject and task.

Run tasks through real affordances: navigation, keyboard focus, input retention, loading, errors and recovery. Compare related pages' anchors and visual language under corresponding conditions; page responsibilities can justify different compositions.

Use geometry, contrast, accessibility, console/network evidence and image differences to locate causes or verify measured properties. Pixels support perceived balance, material and motion judgments; user comprehension requires user observation.

Attribute observations to **carrier page, player, depicted product UI or its displayed work/content**. Carrier DOM/requests explain its page/player; the depicted application needs corresponding evidence. Identify edited promotion, authored demo or actual operation, retaining source/version and conditions. Edited media supports displayed relationships; response, failure and completion require runtime evidence.

## Inspect a time-bounded visual episode

Observe **pre-trigger state → action → first feedback → progression → settled result** in references, candidates, trials and runtime. Demos expose a selected flow; authorized operations can fill return, interruption or recovery gaps. Playback, live observation or media analysis supplies inspection; acquisition alone does not.

Choose the window from the behavior:

| Design object | Observation window | Extend it when needed |
|---|---|---|
| Micro-interaction or local transition | Before input through acknowledgment, motion and a readable settled state | Reverse, interrupt or repeat while the object is changing |
| Loop, dynamic background or spatial scene | Enough progression to reveal its cycle, changing emphasis and seam or return | Inspect peak reach/brightness, interacting cycles and relevant views; nonperiodic motion needs representative intervals |
| Scroll-driven change | Relevant entry, hold and exit at known scroll positions and direction | Reverse direction; inspect sticky, local and horizontal regions where relationships change |
| Asynchronous task | Before intent through waiting, intermediate feedback and the valid outcome or recovery state | Exercise early/late response, failure, cancellation and new intent during pending work |
| Navigation or connected journey | Linked episodes covering departure, transition, arrival and continuation/return | Preserve object, focus, scroll and shared-shell context across the boundaries |

When supported, view normally, pause/replay or enlarge relevant frames, then return to normal speed to judge rhythm. Apply the [seven temporal qualities](interaction-and-variants.md#read-motion-through-perceptible-qualities), including hidden/replacement intervals and surrounding elements.

Retain frame order, actual timestamps/event offsets, cadence, actions/states and clock source; use capture-time brackets when presentation instants are unknown. Planned screenshot delays do not establish actual intervals.

Tie episodes/frames to runs or recordings; mark resets, reruns and edits. Contact sheets locate events; open important frames at useful size and connecting intervals for continuity. Retain state, order and gaps across journeys.

Let behavior determine duration, change speed sampling density, and design impact analysis depth. Extend for seams, flashes, overlap, jumps or late updates; mark omissions. Sparse samples establish sampled states, not intervening continuity. Without playback, inspect ordered frames and leave playback-dependent claims pending. Acquisition, actual inspection and sufficient support remain distinct; metadata or a poster establishes neither playback nor continuity.

For reproducible authored timelines or regression probes, fix source, stage/viewport, content, fonts, assets, initial state and relevant seeds; seek explicit times when supported. Record controlled clocks/mechanisms and remaining nondeterminism. Compare progression, reset and loop seams through contact sheets and full playback. Frame stepping, slowed playback and a [simulated clock](https://playwright.dev/docs/clock) reveal ordering/geometry; natural-time observation separately establishes experienced pacing. Capture overhead and environment still apply; frame-delivery claims need runtime traces.

Check capture settings. [Disabling screenshot animations](https://playwright.dev/docs/api/class-page#page-screenshot-option-animations) can fast-forward finite animations and reset infinite ones: use that output for declared static comparison, with motion enabled in a separate natural-progression run. Record masks, injected styles and overlays that alter evidence; preserve the indicator when examining focus/caret.

Locate the change within its interval, such as a reversing card shifting against its stationary action. Test causes with state, layout, animation ownership or traces; missing frames may reflect capture. After repair, reinspect the interval and complete episode/return.

## Findings and repair

Connect the viewed state/interval, phenomenon, task/perceptual effect, intent, cause to test, repair and recheck. Prioritize blocked tasks, hidden controls, shared defects and consequential composition/continuity problems.

Locate the gap: unsuitable source, damaged adaptation, content/structure mismatch, conflicting resources or an unworkable target. Correct the responsible asset, token, component, timing, state or data contract and recheck affected journeys. Preserve the accepted art direction while resolving concrete reading, operation or runtime problems; change its scope explicitly when necessary. Keep observation and causal inference distinct.

New evidence can improve the SPEC. If the target remains unattainable, state the gap, effect and viable options for the consequential user decision. Integration progress does not establish quality acceptance; preserve the agreed standard until its scope or direction is explicitly revised.

## Comparing SPEC and connected product

Distinguish **Source Fidelity** from **Perceptual Quality**. Fidelity protects an identified approved design or adopted source: structure, assets, type, proportion, material and behavior. Perceptual review judges the actual composition, craft and continuous experience. Reference-informed original work can inherit maturity with an independent appearance.

For strict restoration, identify the exact target/revision and intended differences; match content, viewport, pixel ratio/zoom, browser/rendering conditions, fonts, themes, locales and event phase. Use overlays, regional differences or pixel metrics to locate deviations, with task-justified tolerances and disclosed masks. Diagnose rendering variation; a similarity score cannot certify design quality.

Align episodes by meaningful events/object identity; explain latency/data differences. Keep reproducible fixtures beside real-service evidence. Revise an approved target explicitly when new evidence warrants it.

## Status meanings

- `planned`: declared coverage, not yet executed.
- `pass`: the specified check was executed, inspected where visual, and has evidence.
- `fail`: an observed issue remains.
- `blocked`: a required capability, resource or permission is unavailable.
- `waived`: an explicitly accepted exception with reason, scope and approver.

Distinguish capture, visual inspection and interaction verification. Without a usable image/video viewer, capture/runtime checks can proceed while visual judgment remains pending. State the missing capability and continue independent work. After changes, recapture affected views/episodes before extending claims; reconcile revisions before carrying approval forward.

## Decide when to present the round

Present inspectable work with required checks complete, blockers resolved and uncertainty scoped. Design review can precede integration. Show consequential candidates, episodes or before/after views; keep agent judgment and user approval separate.

## Lightweight checker

`python <skill-dir>/scripts/check_manifest.py --project-root . --mode review`

This optional checker validates declared coverage/evidence; `--mode finish` also checks approval and integration records. It cannot launch browsers, view pixels, verify identity or certify quality. Reuse adequate project matrices.

## Choose methods for the evidence question

Begin with visible behavior; use host-supported inspection to resolve a named uncertainty, then interpret the result in the rendered experience. Verify tool/version coverage and permissions before use.

| Question | Useful capability and its boundary |
|---|---|
| Which resource arrived, and what requested it? | [Network](https://developer.chrome.com/docs/devtools/network/) exposes observed requests, types, content and initiators |
| What happened to playback? | [Media](https://developer.chrome.com/docs/devtools/media-panel) exposes player properties, events, messages and playback/buffering timelines |
| How does a supported animation progress? | [Animations](https://developer.chrome.com/docs/devtools/css/animations) supports pause, replay and timeline inspection; verify the rendering mechanism's coverage |
| Which action/state/request preceded the change? | [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer) correlates captured action snapshots, filmstrip, console and network evidence |
| Did the runtime deliver frames and respond as intended? | [Performance traces](https://developer.chrome.com/docs/devtools/performance/reference) support measured timing; captured filmstrips retain their sampling limits |

Use scripts within authorized page/resource access. Data changes, messages and transactions retain their authorization; private media/traces stay in authorized destinations. Capabilities supply evidence, not automatic access or conclusions. [Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) and [interaction patterns](https://www.w3.org/WAI/ARIA/apg/) guide accessibility checks.

## Inspect from whole to detail and back

Use the [multiscale method](principles.md) at normal use scale: whole impression, composition, consequential regions/details, then whole task. Retain neighbors and context. After correction, recheck hierarchy across affected states, pages and episodes; an enlarged difference matters when it changes the intended-size result.

“The summary is separated by most of the viewport” is observed; “the gap weakens grouping” is an interpretation. Test causes through comparison or implementation evidence. Unseen interaction and audience response remain unverified.

### Preserve three distinct levels of visual observation

**Whole surface:** identify the primary task, dominant subject, information order, total visual mass and intended character. Check whether the user's next meaningful action and reading path are discoverable without explanation from the designer.

**Relationships:** inspect grouping, alignment, comparison structure, proportions, image/text balance, shared shell and spatial anchors. For a transition, inspect which relation it reveals, what stays stable and whether other areas move unexpectedly.

**Details:** inspect actual typography and copy, image boundaries and crops, icon weight, material edges, focus visibility, native controls and timed feedback. Judge the details against the selected craft target rather than unrelated stylistic preferences, then return to the full composition to see whether the improvement holds.

Assess task correctness and accessible operation, communication clarity, identity/coherence and implementation craft as complementary obligations rather than a weighted score that can hide a critical failure. Automated geometry, console, network and accessibility checks establish their measured properties; source images, actual human-visible rendering and meaningful task operation are still needed to judge the visual result.

## Diagnose and improve the strongest relationship

Identify the weak relationship before tuning parameters. Repair structure or meaning, then detail. Compare equivalent conditions; group related changes when their effects remain attributable.

Assess **experience validity** and **expressive completion** independently: can people understand and complete the task reliably, and does the promised art direction appear with mature assets, composition, detail and motion? Strength in one cannot compensate for a gap in the other. Inspect first encounter, populated core work, long content, repeated use and related views. A different appearance can meet the quality target; names or averaged scores cannot establish it.

## Verify the publishing medium

For documentation, inspect hierarchy, selectable text, copyable commands, links, alt text, image width, narrow code/table handling and declared variants in supported markup. Check hidden content through the actual scroll/disclosure mechanism. A local approximation identifies its renderer; the publishing host needs its own readback and visible inspection.

A working product needs semantic controls, actual content/state and boundary checks. A product demonstration needs an accurate representative flow and disclosed staging. Authored visual work can use fixed layers/stage/timing; inspect fidelity, holds, transitions, resets/seams and final encoded playback. A video of a UI does not establish its operability. Verify diagram semantics and generated assets' delivered bytes alongside editable sources; match claims to the observed medium.

## Retain lessons with boundaries

Retain a lesson's problem, mechanism, conditions, editable realization, evidence and limits. Keep project preferences local; propose portable examples through authorized maintenance. Explanatory examples support future decisions, while model improvement needs its own evidence.

## Validate resource adoption in context

Inspect the [four objects](component-sourcing.md#confirm-consequential-parts-in-a-local-trial) separately: reference, original demo, current-project trial and assembled journey. Trial consequential parts before expansion under the content, fonts, language, theme and states that could change fit; recheck combined attention, cost, cleanup and service boundaries.

Keep research, comparison, trial, adoption and inspection distinct. Retain source/revision, settings, viewed states/episodes, changes and gaps. Supplied files need inspection; record/retrieval checks establish only their mechanics.

## Verify the design decision chain

Connect user intent, experience hypothesis, research question, product/user evidence, viewed relationships, candidate comparison, adopted implementation and result. Check primary action, continuation and selection authority; provisional choices retain their status.

Re-answer research questions beside the preview with current content, comparable scale/density and corresponding interaction phases. Trace the desired quality to the adopted implementation, adaptation and observed result. Exercise first use, active work and resume. Fixture results, product acceptance, agent evaluation and user research retain separate scope.

## Inspect inherited design value

Identify retained, changed and authored mechanisms in code/assets and runtime. Attribution or a package name proves neither adopted scope nor quality; authored surfaces need their own basis. Compare local craft, whole-page hierarchy, proportions, reading rhythm and continuity. Revalidate rewritten layout/state/motion; upstream maturity covers retained mechanisms. Judge reuse by consequential responsibilities fulfilled, not dependency totals or code share.

## Verify assets from master to placement

Follow source/permission, transformation, derivative and actual placement. Inspect delivered bytes using the [asset-family checks](visual-assets.md#accept-the-asset-in-use): small-size silhouette/weight, type coverage, image crop/alpha/color, spatial material/export fidelity and temporal states.

Record CSS size, density, theme, viewport, content and load conditions. Exercise relevant blocked-resource, quiet, offscreen and renderer-limited states. Separate isolated craft, assembled visual quality and engineering cost. A large source preview or file signature cannot establish small-size readability, editable geometry or runtime behavior.

A browser fixture can validate integration paths when specialist production is unavailable. Report researched, executed and pending routes separately.

## Verify meaning and actual words in context

Inspect headings, navigation, labels, help, validation, status, empty, error and confirmation copy through the task. Check information at decision points and the outcome each phrase promises against its authoritative source. Include delayed, denied, partial, unknown and failed results. Review supported locales with realistic text, viewports and themes.

Check names, labels, associations, announcements, clipping, line breaks and focus. Visual review establishes reading rhythm and balance; actual user comprehension needs its own observation. Compare terminology and cross-step information responsibility, diagnose the responsible content/structure/localization/authority layer, then recheck the journey.

## Measure performance across the complete task

Choose measures from the operation people need to finish. Record task, initial data/cache, device/browser, network, workload and revision. Separate immediate feedback, usable content and authoritative completion, then trace the relevant dependency. A responsive acknowledgment can coexist with a slow service result.

| Experience question | Useful observation | Interpretation boundary |
|---|---|---|
| Is input acknowledged promptly? | Input delay, handler work and the next relevant presented frame | Responsiveness covers a different boundary from service completion |
| When is the next action possible? | Marks from entry/input to usable content or confirmed outcome | Name local readiness, server acceptance or completed work explicitly |
| Does motion remain smooth? | Natural-time observation plus frame timing, long tasks and dropped/presented frames | A screenshot, sampled clip or average rate can hide a stall |
| Does the task remain stable? | Layout shifts plus focus, object and scroll continuity | Layout metrics cover only their defined shifts |
| What does preparation cost? | Requests, bytes, duplicate work, concurrency, decoding and sustained resource use | Compare saved waiting with unused work |
| Are stressed results correct? | Object state, response ownership, partial outcomes and recovery | Optimizations preserve the required business result |

Use field observations where available and controlled runs for diagnosis/regression. [User-centric metrics](https://web.dev/articles/user-centric-performance-metrics) frame experience measures; [INP](https://web.dev/articles/optimize-inp) concerns responsiveness. Task-specific [performance measures](https://developer.mozilla.org/en-US/docs/Web/API/Performance/measure) need explicit endpoints. Automation elapsed time and double-animation-frame samples retain those labels; they are not field INP. Video encoding rate is also distinct from application frame delivery.

Compare equivalent before/after tasks; repeat samples where variability affects the decision. Include cold/warm, realistic volume, rapid operations and relevant slow/failing boundaries. Check expiration and changed inputs when preparing or caching results. Set budgets from product needs and target devices. Report both measured benefit and cost; simulated latency, capture overhead and desktop emulation keep their limits.

## Exercise motion, growth and operational change

Use the temporal method to check full relevant motion, reverse/interrupted paths and reduced motion. Inspect object identity, face visibility, focus, hit regions and peak overlap. Vary response arrival before, during and after transition; the visible result must follow current valid state.

Exercise expansion, late assets/fonts, new records, long text and permission changes in actual scrolling regions. Inspect lower content, sticky controls, overlays, keyboard reveal and return position. Compare readable material across ready/loading/failure states. A collapsed resolved choice preserves its meaning and any permitted revision path.

For operating workflows, change a shared template and an overridden item, then inspect consuming surfaces and locales. Exercise selection across filters/pages, mixed batch outcomes, interruption and scoped retry. Confirm completed work remains and counts match actual items. Compare customer/operator views for consistent facts and appropriate action. Derive repeated-task efficiency from observed work and recovery at representative scale.

## Verify the map and the scope of each claim

Use [the evidence map](evidence-map.md) to reconcile coverage, source roles, decisions, actual implementation and checked conditions. Acquired/observed/compared, trialed/adopted, verified and owner-approved describe different facts; blocked and confirmed exceptions do not become passes. Keep outcome and evidence scope for each claim, including failures and conditions still unexamined. A parent page or journey needs its own assembled observation.

Check both directions: a decision should resolve to the evidence and actual adopted location that supports it; a changed source, condition or shared dependency should lead back to affected claims. Reference-product appearance, candidate-demo quality, local fit and integrated behavior have distinct subjects. Old evidence stays historical when applicability changes; establish a current recheck or a justified carry-forward scope.

The optional [read-only record checker](../scripts/check_design_evidence.py) implements the [structured profile](evidence-records.md). It can flag missing local files, inconsistent IDs, stale claims, unsupported object/condition declarations and action/gap contradictions. It does not observe media, authenticate user approval or certify truthful research, behavior or aesthetics. A structurally valid record may describe incomplete work.

## Review action follow-through separately from declarations

Use [the action rules](evidence-actions.md) to determine whether a consequential gap actually led to suitable research, comparison, trial or repair. Link the resulting artifact/tool trace and decision change, not just a planned next step. Keep three conclusions separate: Skill content integrity, Agent behavior effectiveness and actual UI quality. A deterministic fixture demonstrates its authored conditions; only fresh Agent runs with auditable outputs support behavior comparisons. Preserve pending experiments as pending.
