# Verification: coverage, inspection and honest evidence

## Contents

- [Coverage and assurance](#build-the-coverage-inventory-from-reality)
- [Viewing conditions and actual interaction](#capture-the-actual-viewing-condition)
- [Temporal visual inspection](#inspect-a-time-bounded-visual-episode)
- [Tools for the question](#choose-methods-for-the-evidence-question)
- [Findings, comparison and status](#findings-and-repair)
- [Judgment at three scales](#read-the-result-at-three-scales)
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

## Capture the actual viewing condition

Set the CSS viewport directly. Record viewport, pixel ratio, browser, locale/theme, content, revision and zoom. Distinguish browser/text enlargement from image scaling; inspect the actual route or independently sized frame at useful scale.

For steady states, wait for intended content, fonts and images; keep data and animation phase comparable. For loading/transitions, begin before the event and retain progression. Capture the whole content viewport, including shell, background and surrounding space; browser chrome is optional.

Use **viewport evidence** for composition/scroll boundaries and **content evidence** for documents or scroll checkpoints. Inspect internal scroll regions without resizing the viewport. Exercise sticky controls, overlays, short heights and intended horizontal scrolling. Full-document captures can place fixed overlays incidentally; check covered text in an actual viewport before diagnosing loss.

Record video dimensions/scaling separately from the viewport. [Playwright video](https://playwright.dev/docs/videos) can scale output and needs context closure to finish writing. Preserve useful resolution, with full-size stills for small type or optical detail.

## View the images and use the interface

Open required images and relevant video/ordered frames. Generated files, DOM snapshots and successful capture commands establish availability; visual inspection requires viewing pixels. Review composition, scale, hierarchy, type, whitespace, materials, clipping, assets and persistent controls.

Run tasks through real affordances: navigation, keyboard focus, input retention, loading, errors and recovery. Compare related pages' anchors and visual language under corresponding conditions; page responsibilities can justify different compositions.

Use geometry, contrast, accessibility, console/network evidence and image differences to locate causes or verify measured properties. Pixels support perceived balance, material and motion judgments; user comprehension requires user observation.

Attribute observations to **carrier page, player, depicted product UI or its displayed work/content**. Carrier DOM/requests explain its page/player; the depicted application needs corresponding evidence. Identify edited promotion, authored demo or actual operation, retaining source/version and conditions. Edited media supports displayed relationships; response, failure and completion require runtime evidence.

## Inspect a time-bounded visual episode

Observe **pre-trigger state → action → first feedback → progression → settled result** in references, candidates, trials and runtime. Existing demos expose a selected flow; authorized operations can fill consequential return, interruption or recovery gaps. Use playback, live observation or suitable media analysis; acquisition alone leaves content uninspected.

Choose the window from the behavior:

| Design object | Observation window | Extend it when needed |
|---|---|---|
| Micro-interaction or local transition | Before input through acknowledgment, motion and a readable settled state | Reverse, interrupt or repeat while the object is changing |
| Loop, dynamic background or spatial scene | Enough progression to reveal its cycle, changing emphasis and seam or return | Inspect peak reach/brightness, interacting cycles and relevant views; nonperiodic motion needs representative intervals |
| Scroll-driven change | Relevant entry, hold and exit at known scroll positions and direction | Reverse direction; inspect sticky, local and horizontal regions where relationships change |
| Asynchronous task | Before intent through waiting, intermediate feedback and the valid outcome or recovery state | Exercise early/late response, failure, cancellation and new intent during pending work |
| Navigation or connected journey | Linked episodes covering departure, transition, arrival and continuation/return | Preserve object, focus, scroll and shared-shell context across the boundaries |

When supported, view at normal speed, pause/replay or enlarge relevant frames, then return to normal speed to judge rhythm. Apply the [seven temporal qualities](interaction-and-variants.md#read-motion-through-perceptible-qualities) to the object and its surroundings, including hidden/replacement intervals.

Start before the trigger. Retain frame order, actual timestamps/event offsets, cadence, actions/states and clock source; use capture-time brackets when presentation instants are unknown. Planned screenshot delays do not establish actual intervals.

Tie episodes and extracted frames to runs/recordings, marking resets, reruns and edits. Use keyframes/contact sheets to compare events; open important frames at useful size and intervening intervals for continuity. Retain connecting state, order and gaps across journeys.

Let behavior determine duration, change speed sampling density, and design impact analysis depth. Extend coverage for seams, flashes, overlap, jumps or late updates; mark omissions. Sparse samples support observed states; endpoints leave transitions unknown. Without playback, inspect ordered frames and retain playback-dependent claims as pending. Distinguish acquisition, actual inspection and sufficient support for a conclusion. Metadata or a preview frame establishes neither playback nor continuity.

Separate natural-time observation from controlled probes. Frame stepping, slowed playback and a [simulated clock](https://playwright.dev/docs/clock) expose ordering and intermediate geometry, not unmodified pacing or smoothness. Record time controls. Natural-time captures still reflect sampling, overhead and environment; frame-delivery measurements need runtime traces.

Check capture settings before relying on a temporal record. [Disabling animations for a Playwright screenshot](https://playwright.dev/docs/api/class-page#page-screenshot-option-animations) can fast-forward finite animations and reset infinite ones. Such output can support a declared static comparison, while natural progression needs a separate run with the intended motion enabled. Record relevant masks, injected styles and diagnostic overlays: these alter what can be observed. For a focus/caret question, preserve the indicator being examined.

Locate the visible change within its interval: a card shifts relative to its stationary action during reversal, or a moving highlight obscures a label. Correlate state events, layout, animation ownership or traces to test the cause. Missing frames may reflect capture; investigate before blaming rendering. After repair, inspect the interval and replay the complete episode and return.

## Findings and repair

Connect the viewed state/interval, phenomenon, task/perceptual effect, intent, cause to test, repair and recheck. Prioritize blocked tasks, hidden controls, shared defects and consequential composition/continuity problems.

Locate the quality gap before extending implementation: replace an unsuitable source; repair adaptation that lost valuable relationships; review content and structure when real content exposes a gap; reconcile conflicting resources with the design language; revisit the target when it mismatches the task. Then correct the responsible asset, token, component, timing, state or data contract and recheck affected journeys. Keep observation and causal inference distinct.

New evidence can improve the SPEC. If the target remains unattainable, state the gap, effect and viable options for the consequential user decision. Integration progress does not establish quality acceptance; preserve the agreed standard until its scope or direction is explicitly revised.

## Comparing SPEC and connected product

Compare equivalent content, viewports, font readiness, themes, locales and states. Align episodes by meaningful events and object identity; explain latency/data differences. Tie reviewed evidence to its revision, retaining reproducible fixtures beside real-service checks. Improve the reference when new evidence justifies it.

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

## Read the result at three scales

**Whole surface:** identify task, dominant subject, information order, visual mass and character. Judge discoverability without the designer's explanation.

**Relationships:** inspect grouping, alignment, proportions, image/text balance and shared anchors. Follow the explained relationship and stable areas through transitions.

**Details:** inspect glyphs, copy, edges, icon weight, surfaces, controls, focus and timed feedback at use size against the craft target.

“The summary is separated from the items by most of the viewport” describes an observation. “The gap weakens their grouping” is an interpretation to assess against the task. Anchor both to actual evidence; an unseen interaction or audience response remains a separate question.

## Diagnose and improve the strongest relationship

Identify the weak relationship before tuning parameters. Repair structure or meaning, then detail. Compare equivalent conditions; group related changes when their effects remain attributable.

Compare design maturity through the task's important qualities: readable type, optical balance, coherent materials, state clarity and continuity. A different appearance can meet the target better. Review correctness, accessibility, communication and craft separately; similarity percentages or an averaged quality score cannot establish these relationships.

## Verify the publishing medium

For documentation, inspect hierarchy, selectable text, copyable commands, links, alt text, image width, narrow code/table handling and declared variants in supported markup. Check hidden content through the actual scroll/disclosure mechanism. A local approximation identifies its renderer; the publishing host needs its own readback and visible inspection.

For diagrams, confirm relationship/data semantics. For timed output, inspect readable holds, intermediate changes and final playback. For generated assets, inspect delivered bytes as well as editable sources. Match claims to the output and environment observed.

## Retain lessons with boundaries

Retain a lesson's problem, mechanism, conditions, editable realization, evidence and limits. Keep project preferences local; propose portable examples through authorized maintenance. Explanatory examples support future decisions, while model improvement needs its own evidence.

## Validate resource adoption in context

Verify the [four observation objects](component-sourcing.md#confirm-consequential-parts-in-a-local-trial): reference, original candidate demo, current-project trial and assembled journey. Match conclusions to the object actually inspected. Trial consequential parts before broader integration, using the fonts, language, content, theme and states that could change the choice. Recheck combined attention, runtime cost, cleanup and service boundaries after composition.

Keep researched, compared, trialled, adopted and inspected status distinct. Retain source/revision, settings, relevant views or episodes, changed scope and unresolved conditions. Motion claims require viewed process evidence; supplied recordings and downloaded source still require inspection. Record/retrieval tests establish their own mechanics.

## Verify the design decision chain

Check product model, primary action, continuation, alternatives and selection authority. Existing UI needs target-based fit; provisional choices retain their status.

Re-answer research questions beside the preview with current content, comparable scale/density and corresponding interaction phases. Trace the desired quality to the adopted implementation, adaptation and observed result. Exercise first use, active work and resume. Fixture results, product acceptance, agent evaluation and user research retain separate scope.

## Inspect inherited design value

Inspect which mature layout, visual and interaction mechanisms survive in the final code/assets and runtime. Explain retained, changed and authored responsibilities; a package name or reference attribution establishes neither adopted scope nor quality. A behavior primitive supports its implemented behavior, while the authored visual surface needs its own basis and verification.

Compare local craft and whole-page hierarchy, proportions, reading rhythm and continuity. Broaden revalidation when adaptation rewrites core layout, state or motion mechanisms. Upstream maturity supports retained work; current-product evidence supports the changed result. Judge reuse by high-impact responsibilities fulfilled, not dependency totals or code share.

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
