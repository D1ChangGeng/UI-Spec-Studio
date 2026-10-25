# Verification: coverage, inspection and honest evidence

## Contents

- [Coverage and assurance](#build-the-coverage-inventory-from-reality)
- [Viewing conditions and actual interaction](#capture-the-actual-viewing-condition)
- [Temporal visual inspection](#inspect-a-time-bounded-visual-episode)
- [Findings, comparison and status](#findings-and-repair)
- [Judgment at three scales](#read-the-result-at-three-scales)
- [Publishing and resource adoption](#verify-the-publishing-medium)
- [Decision, asset and content evidence](#verify-the-design-decision-chain)
- [Performance and operational change](#measure-performance-across-the-complete-task)

## Build the coverage inventory from reality

Reconcile routes, navigation, roles, overlays, runtime states and UX records. Include every implemented in-scope page family; missing legitimate entries are findings. State how dynamic data shapes, lengths and permissions are sampled.

Keep the complete inventory separate from the current verification scope. A round checks its changed scope and affected dependants; final acceptance reconciles the full approved inventory. State that scope when reporting coverage.

Declare supported viewports and theme/locale combinations from target use. Inspect every route's primary state at every declared viewport and variant. Exercise each additional critical state in every declared variant, extending viewport coverage where layout or risk differs. Preserve user-requested exhaustive coverage and record approved exclusions with their reasons. Include short heights and actual narrow-input conditions where supported; fixed dimensions are project choices.

Include transitions and journeys whose quality exists across time. Name the trigger, meaningful intermediate states, completion or stopping condition, and return/recovery path. A state inventory locates scenes; temporal coverage connects them.

## Match assurance to impact

Check local changes in their surrounding layout, shared changes across dependants, and journeys through transitions/recovery. Integration needs visual and business-boundary evidence. Choose depth from consequence, variability and decision value.

Explain sampling and remaining conditions. Package/tool tests, logical scenarios, visual inspection, interaction execution, user research and real integration establish different facts. Large comparative model evaluations are separate research.

## Capture the actual viewing condition

Set the browser's CSS viewport directly. Record viewport, device pixel ratio, browser, locale/theme, content identity, source revision and relevant zoom. Distinguish browser/text enlargement from a fitted preview canvas or scaled screenshot display. View the actual route or independently sized frame at a useful inspection scale.

For steady-state comparisons, wait for the intended state, fonts and images; hold data and animation phase comparable. For loading or transition observations, begin before the event and retain the arrival process. Capture the whole content viewport, including shell, background and surrounding space; browser chrome is optional.

Use **viewport evidence** for visible composition and scroll boundaries, and **content evidence** for a document or real-scroll checkpoints. Internal scrolling needs its own checkpoints. Keep viewport dimensions unchanged while inspecting long content. Observe sticky controls, overlays, short-height states and intentional horizontal scrolling directly. Full-document captures can retain a fixed overlay at an incidental scroll position; inspect the actual viewport or another checkpoint before calling its covered text missing.

Record video dimensions/scaling separately from the viewport. [Playwright video](https://playwright.dev/docs/videos) can scale output and needs context closure to finish writing. Preserve useful resolution, with full-size stills for small type or optical detail.

## View the images and use the interface

Open the required images and observe the relevant video or ordered frames with available viewing tools. A generated file, DOM snapshot or successful capture command establishes availability; inspection requires actually viewing its pixels. Review composition, scale, hierarchy, type, whitespace, materials, clipping, assets and persistent controls.

Run tasks through real affordances. Observe navigation, keyboard focus, input retention, loading, errors and recovery. Switch related pages under comparable conditions to judge anchors and visual language. Their individual compositions may differ with their responsibilities.

Use geometry, contrast checks, accessibility inspection, console/network results and screenshot differences to locate or substantiate findings. Use visible output to judge perceived balance, material and motion. Technical measurements explain their measured properties; user comprehension requires user observation.

## Inspect a time-bounded visual episode

Observe change as an episode with visible starting context, trigger, progression and endpoint. Apply it to external candidates, assembled designs and actual runtime, establishing each result at its own boundary.

Choose the window from the behavior:

| Design object | Observation window | Extend it when needed |
|---|---|---|
| Micro-interaction or local transition | Before input through acknowledgment, motion and a readable settled state | Reverse, interrupt or repeat while the object is changing |
| Loop, dynamic background or spatial scene | Enough progression to reveal its cycle, changing emphasis and seam or return | Inspect peak reach/brightness, interacting cycles and relevant views; nonperiodic motion needs representative intervals |
| Asynchronous task | Before intent through waiting, intermediate feedback and the valid outcome or recovery state | Exercise early/late response, failure, cancellation and new intent during pending work |
| Navigation or connected journey | Linked episodes covering departure, transition, arrival and continuation/return | Preserve object, focus, scroll and shared-shell context across the boundaries |

Observe live progression or natural-speed playback for rhythm and continuity, then pause, slow or examine neighboring frames to locate a problem. Apply the [seven temporal qualities](interaction-and-variants.md#read-motion-through-perceptible-qualities) to the affected object and surrounding content, including its hidden or replacement intervals.

Choose recording or a consecutive capture sequence capable of resolving the relevant change. Start capture before the trigger. Retain frame order, actual timestamps or offsets from a named event, capture cadence and meaningful actions/states. Identify the clock or source of those times; when only capture start/end times are known, retain that interval rather than assigning an exact presentation instant. A planned delay between screenshot calls is not the actual sampling interval.

Keep each episode tied to its run and identify resets, reruns or edited joins. Preserve the link between extracted frames and their source recording. Keyframes and contact sheets help compare events; open important frames at usable size and examine the intervening interval when judging continuity. For a long journey, retain the order and state connecting shorter episodes and identify unobserved intervals.

Select sampling density and duration from motion speed, event uncertainty and the question. Increase coverage where a seam, flash, overlap, jump or late update may fall between samples. Mark gaps and omitted intervals. Sparse samples establish their observed states; endpoints alone leave the transition unknown. If a viewer cannot play video, inspect an ordered frame sequence and state that scope, keeping playback-dependent judgments pending. Do not report watching a clip from its filename, metadata or a single preview frame.

Keep natural-time observation separate from controlled-time probes. Frame stepping, slowed playback and a [simulated clock](https://playwright.dev/docs/clock) help expose state ordering and intermediate geometry; they do not establish unmodified runtime pacing or smoothness. Record how time was controlled. A natural-time sequence still reflects its capture overhead, sampling and environment; measured frame delivery requires the corresponding runtime trace.

Check capture settings before relying on a temporal record. [Disabling animations for a Playwright screenshot](https://playwright.dev/docs/api/class-page#page-screenshot-option-animations) can fast-forward finite animations and reset infinite ones. Such output can support a declared static comparison, while natural progression needs a separate run with the intended motion enabled. Record relevant masks, injected styles and diagnostic overlays: these alter what can be observed. For a focus/caret question, preserve the indicator being examined.

For a finding, point to the interval and the visual change: for example, the card shifts relative to its stationary action during reversal, or a background highlight obscures a label midway through a loop. Then correlate the episode with state events, layout, animation ownership or performance traces to test the cause. A missing captured frame can belong to capture rather than rendering; investigate before assigning blame. Recheck the affected interval after repair, then replay the complete episode and connected return path.

## Findings and repair

Connect page/state/view or time interval, observed phenomenon, user impact, design intent, evidence, likely cause, repair and retest. Keep observation and causal inference distinguishable. Prioritize task blockers, hidden controls, shared defects and consequential composition/continuity problems before minor detail.

Repair at the responsible layer: source selection, asset, content, token, shell, component, timing, state ownership or data contract. Check affected neighbors and journeys. Preserve approved context and unrelated work. New visual evidence can improve the SPEC as well as its implementation.

## Comparing SPEC and connected product

Compare equivalent content, viewports, font readiness, themes, locales and states. For temporal work, align episodes by meaningful events and object identity; explain genuine latency or data differences. Retain reviewed evidence tied to its revision and keep reproducible fixtures alongside real-service checks. The reference records design intent and evidence; it remains open to justified improvement.

## Status meanings

- `planned`: declared coverage, not yet executed.
- `pass`: the specified check was executed, inspected where visual, and has evidence.
- `fail`: an observed issue remains.
- `blocked`: a required capability, resource or permission is unavailable.
- `waived`: an explicitly accepted exception with reason, scope and approver.

Distinguish captured, visually inspected and interaction-verified scope in the evidence. A browser without a usable image/video viewer supports capture and runtime checks while the corresponding visual judgment remains unverified. State the precise missing capability and continue independent work. Keep evidence tied to its inspected revision; after a change, recapture affected views and episodes before extending the claim. Reconcile the current revision before carrying an earlier approval forward.

## Decide when to present the round

Present when the task is inspectable, required checks complete, blockers resolved and uncertainty scoped. Design review can proceed while integration is pending. Show candidates, episodes or before/after views for consequential choices. Agent judgment and user approval retain separate provenance.

## Lightweight checker

`python <skill-dir>/scripts/check_manifest.py --project-root . --mode review`

The optional checker validates declared coverage and evidence references; `--mode finish` also checks recorded approvals and integration cases. It does not launch browsers, inspect pixels, verify identity or certify quality. Use an adequate existing project matrix instead of duplicating it.

## Primary references

- [Playwright screenshots](https://playwright.dev/docs/screenshots), [emulation](https://playwright.dev/docs/emulation) and [visual comparisons](https://playwright.dev/docs/test-snapshots) support reproducible browser conditions.
- [Chrome animation inspection](https://developer.chrome.com/docs/devtools/css/animations) supports replay, slowing and timeline inspection for supported animation mechanisms; check tool/version coverage.
- [Chrome runtime performance](https://developer.chrome.com/docs/devtools/performance/reference) relates interactions, frames, rendering and network activity to a recorded interval.
- [W3C reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) and [WAI interaction patterns](https://www.w3.org/WAI/ARIA/apg/) support accessible layout and behavior checks.

These sources describe capabilities and conditions. Actual use, visual judgment and project outcomes retain their own evidence.

## Read the result at three scales

**Whole surface:** identify the task, dominant subject, information order, visual mass and intended character. Judge what the screen makes discoverable without the designer's explanation.

**Relationships:** inspect grouping, alignment, proportions, image/text balance and shared anchors. During transitions, follow the relationship being explained and the areas expected to remain stable.

**Details:** inspect real glyphs, copy, edges, icon weight, surfaces, native controls, focus and timed feedback at their use size. Compare with the product's craft target.

“The summary is separated from the items by most of the viewport” describes an observation. “The gap weakens their grouping” is an interpretation to assess against the task. Anchor both to actual evidence; an unseen interaction or audience response remains a separate question.

## Diagnose and improve the strongest relationship

Identify the consequential weak relationship before choosing a parameter. Repair structure or meaning at its source, then refine detail. Compare under equivalent conditions, isolating causal groups where useful; related changes can be batched when their effects remain attributable.

Use a positive reference to explain a mechanism and its conditions. Preserve identity while adapting it. Review correctness/accessibility, communication, coherence and craft without averaging away failures. Scope observed improvements; aesthetic quality has no universal numeric pass score.

## Verify the publishing medium

For documentation, inspect hierarchy, selectable text, copyable commands, links, alt text, image width, narrow code/table handling and declared variants in supported markup. Check hidden content through the actual scroll/disclosure mechanism. A local approximation identifies its renderer; the publishing host needs its own readback and visible inspection.

For diagrams, confirm relationship/data semantics. For timed output, inspect readable holds, intermediate changes and final playback. For generated assets, inspect delivered bytes as well as editable sources. Match claims to the output and environment observed.

## Retain lessons with boundaries

Retain a lesson's problem, mechanism, conditions, editable realization, evidence and limits. Keep project preferences local; propose portable examples through authorized maintenance. Explanatory examples support future decisions, while model improvement needs its own evidence.

## Validate resource adoption in context

Separate discovery, item assessment and project acceptance. Documentation supplies leads/contracts; viewed demonstrations support visual claims about a specific item; the assembled product needs its own inspection. Record exact revision, variant, settings, rights and relevant episode. A static gallery image supports its depicted state, while motion or interaction claims require corresponding observation.

Check adopted items with their dependants for combined attention, runtime cost, cleanup and service boundaries. Keep mocked record/retrieval checks distinct from actual browsing, rendering and integration.

## Verify the design decision chain

Check product model, primary action, continuation, meaningful alternatives and selection authority. Existing UI reuse needs approval or target-based fit; a provisional choice retains that status.

Open the decision record beside the preview. Trace convention/source to adopted mechanism, code and observed result; reconcile retained, replaced and authored work. Exercise first use, active work and resume. An authored fixture establishes its own paths; original-product acceptance, independent agent evaluation and user research remain separate.

## Inspect inherited design value

Compare inherited hierarchy, proportions, reading rhythm and state continuity with actual output. Explain reuse scope, adaptations and original contributions. Attribution establishes origin; real tasks and visual inspection establish retained value. Distinguish a static port, runtime integration and accepted product.

## Verify assets from master to placement

Follow source/permission, transformation, derivative and actual placement. Inspect delivered bytes using the [asset-family checks](visual-assets.md#accept-the-asset-in-use): small-size silhouette/weight, type coverage, image crop/alpha/color, spatial material/export fidelity and temporal states.

Record CSS size, density, theme, viewport, content and load conditions. Exercise relevant blocked-resource, quiet, offscreen and renderer-limited states. Separate isolated craft, assembled visual quality and engineering cost. A large source preview or file signature cannot establish small-size readability, editable geometry or runtime behavior.

A bounded browser fixture can validate integration paths when specialist production is unavailable. Identify which routes were researched, executed or remain pending; retain that scope when reporting results.

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
