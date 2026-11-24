# Verification: coverage, inspection and honest evidence

## Contents

- [Build the coverage inventory from reality](#build-the-coverage-inventory-from-reality)
- [Verify the increment and its product relationships](#verify-the-increment-and-its-product-relationships)
- [Scope regression across shared migrations and evolving code](#scope-regression-across-shared-migrations-and-evolving-code)
- [Inspect and show the first reviewable result](#inspect-and-show-the-first-reviewable-result)
- [Judge evidence for the decision](#judge-evidence-for-the-decision)
- [Capture the actual viewing condition](#capture-the-actual-viewing-condition)
- [View the images and use the interface](#view-the-images-and-use-the-interface)
- [Inspect a time-bounded visual episode](#inspect-a-time-bounded-visual-episode)
- [Choose methods for the evidence question](#choose-methods-for-the-evidence-question)
- [Inspect from whole to detail and back](#inspect-from-whole-to-detail-and-back)
- [Findings and repair](#findings-and-repair)
- [Comparing SPEC and connected product](#comparing-spec-and-connected-product)
- [Status meanings and presentation readiness](#status-meanings-and-presentation-readiness)
- [Empirical regression guardrails](#empirical-regression-guardrails)
- [Target-demo vs. integrated-app visual delta and craft retention](#target-demo-vs-integrated-app-visual-delta-and-craft-retention)
- [Verify assets, content, publishing and operational change](#verify-assets-content-publishing-and-operational-change)
- [Measure performance across the complete task](#measure-performance-across-the-complete-task)
- [Keep evidence maps, records and scoped assertions independent](#keep-evidence-maps-records-and-scoped-assertions-independent)
- [Taste and craft-defect audit](#taste-and-craft-defect-audit)

## Build the coverage inventory from reality

Reconcile routes, navigation, roles, overlays, runtime states and UX records. Include every in-scope page family; missing entries are findings. State how data shapes, lengths and permissions are sampled.

Report scope: a round checks changes and affected dependants; final acceptance reconciles the full approved inventory. Declare supported viewports and theme/locale combinations from target use. Inspect every route's primary state at every declared viewport and variant. Exercise each additional critical state in every declared variant, extending viewport coverage where layout or risk differs. Preserve user-requested exhaustive coverage and record approved exclusions with their reasons. Include short heights and actual narrow-input conditions where supported; fixed dimensions are project choices.

Include temporal relationships: trigger, meaningful progression, stopping condition and return/recovery. State inventories locate scenes; episodes connect them.

## Verify the increment and its product relationships

Treat the formal SPEC as a design increment in the current product. Identify its experience goal, consequential visual responsibilities and actual review entry, then distinguish two verification obligations:

- **Current SPEC quality:** inspect the concrete relationships this increment promises through relevant detail, whole context and complete behavior. A page-level overview can leave an input's typography, material or changing geometry unexamined; a local screenshot can leave continuous motion and shared state unexamined.
- **Related-product integrity:** inspect existing regions, shared systems, states and journeys affected by the change. A strong isolated component never proves that reading width, focus, scrolling, foreground legibility or the product's visual language still work together.

Keep research/observation scope, primary design/implementation scope and integration/regression scope distinguishable. Broad research does not broaden promised implementation, and a narrow implementation change can require wider regression across shared dependants without automatically repeating unrelated product studies.

For a composer-height change, observe text growth, send, response growth and user-controlled scrolling alongside neighboring reading space. For a shared font change, inspect dependent pages' wrapping, hierarchy, control geometry and locales rather than only a specimen. For motion, observe trigger, preparation, progression, settling, reversal and interruption, including coupled neighbors. For a dynamic background, verify moving emphasis alongside foreground reading/input legibility. Trace each important quality through observed reference, actual mature implementation (or faithful authorized design translation / qualifying authorized W1–W3 work), current rendered result and remaining difference.

### Scope regression across shared migrations and evolving code

In long-lived products undergoing [staged shared-foundation migrations](component-sourcing.md#migrate-shared-foundations-across-existing-surfaces-in-stages) or [ongoing engineering co-evolution](integration.md#reconcile-ongoing-engineering-and-contract-drift-between-rounds), replace both impossible whole-application re-audits and silent neighbor breakage with **dependency-scoped proportional regression**:

1. **Derive blast radius from actual shared dependencies:** inspect which surfaces share the changed font metrics, semantic surface or contrast tokens, shared shell geometry, overlay/portal stacking layer, scroll container, navigation chrome or control primitive. Scope regression from real dependency coupling rather than fixed route quotas or blanket version invalidation.
2. **Inspect three targeted scopes proportionally:**
   - **Primary changed slice:** perform full perceptual, state, content and temporal verification for the active SPEC's own promised qualities.
   - **Migration seam transitions:** exercise real navigation and cross-component transitions where migrated and unmigrated surfaces meet, confirming shared navigation anchor stability, theme/locale/reduced-motion parity, single keyboard/focus ownership and clean overlay/portal layering.
   - **Representative high-risk extremum consumers:** inspect downstream surfaces that stress the changed shared dependency hardest—such as high data density tables or dense workbenches, narrow or short viewports, long or mixed-script localized text, and dark/light or reduced-motion variants—where token contrast, wrapping or container overflow breaks first.
3. **Verify brownfield hotfix craft repairs and clean surface retirement:** when repairing visual craft on top of an emergency engineering or accessibility hotfix, confirm that the preserved functional, accessibility or security fix still passes alongside the restored visual craft, token role and mature-source provenance. When a SPEC supersedes or retires an obsolete surface, verify that zero dead navigation entries, stale internal links, orphaned controls or contradictory copy remain in the active product UI.
4. **Keep unmigrated and uninspected scope explicit:** record remaining not-yet-migrated routes, active compatibility bridges and deferred viewport or variant checks honestly as open horizon items or [Verification Scope Debt](evidence-map.md#compact-active-records-without-evaporating-open-obligations) rather than implying uninspected pages passed.

## Inspect and show the first reviewable result

When an important visual object or connected interaction first supports meaningful review, inspect it in the current project and present the actual result in the conversation early enough to correct consequential relationships before broad dependent work inherits them. Partial implementations can support useful review when working scope and open conditions are explicit; research-only tasks show the inspected comparison or proposal honestly without implying a runnable app.

Use the [four evidence roles](component-sourcing.md#confirm-consequential-parts-in-a-local-trial)—**Target Reference**, **Candidate Demo**, **Local Trial** and **Integrated UI**—to make the subject unambiguous. Place the current result beside the target relationship or comparison, explain what is already visible and retain material gaps. Show a real preview, image or episode through the host's supported surface, reusing captures gathered for design work rather than building a parallel presentation deck. Choose evidence by the promised quality: useful-scale images establish typography, composition and material, while growth, scrolling, dragging and asynchronous transitions require continuous operation or playback. Presenting an early result creates an opportunity to inspect—never completed verification or user approval.

## Judge evidence for the decision

Match assurance depth to impact, variability and decision value. Keep distinct claims honest: static fixtures, viewed pixels, executed interactions, real boundary checks and owner acceptance each establish only their own scope. Assess five sufficiency dimensions together:

| Dimension | What sufficiency means |
|---|---|
| Coverage breadth | Important parts, states, views, alternative directions and relationships have a relevant basis |
| Inspection depth | Consequential composition, type, material, proportions and details have actually been examined |
| Temporal coverage | The observed process covers the behavior claimed, with gaps and sampling limits retained |
| Evidence relevance | Conditions and subject answer this product's question, including target version and platform |
| Evidence reliability | Origin, date/revision, platform, role/plan, editing and viewing conditions support the conclusion |

Quantity never compensates for a missing dimension: repeated reposts share one lineage, and a sharp still leaves motion unresolved. Separate actual observation, source statements, professional inference and missing evidence; preserve conflicts for investigation instead of silently merging versions. Before expanding implementation, confirm target understanding, materially different alternatives, observed selection rationale, local trial fit and remaining risks; after integration, inspect experience alignment, visual craft, distinctive expression and reliability on the real task.

## Capture the actual viewing condition

Set the CSS viewport directly; record viewport, pixel ratio, browser, locale/theme, content, revision and zoom. Distinguish browser/text enlargement from image scaling; inspect the actual route or independently sized frame at useful scale.

Wait for intended content, fonts and images for steady states; keep data and animation phase comparable. Begin loading/transition capture before the event. Include shell, background and surrounding space in the whole viewport; browser chrome is optional.

Use **viewport evidence** for composition/scroll boundaries and **content evidence** for documents or scroll checkpoints. Inspect internal regions without resizing the viewport; exercise sticky controls, overlays, short heights and intended horizontal scrolling. Full-document capture can place fixed overlays incidentally; check an actual viewport before diagnosing loss.

Record video dimensions/scaling separately. [Playwright video](https://playwright.dev/docs/videos) can scale output and needs context closure to finish writing. Retain full-size stills for small type or optical detail. Record display scaling: contact sheets locate events, while reading and optical judgments require intended use scale, preserving crop context and returning to normal scale to judge effect.

**Preserve immutable capture history.** Write early-trial and post-fix screenshots to distinct filenames (for example, `composer-trial-desktop.png` and `composer-post-fix-desktop.png`) instead of overwriting earlier captures on disk, keeping before/after visual deltas auditable throughout iteration and review.

## View the images and use the interface

Open required images and relevant video/ordered frames. Files, DOM snapshots and capture commands establish availability; visual inspection requires actually viewing pixels. Select perceptual dimensions from the actual subject and task.

Run tasks through real affordances: navigation, keyboard focus, input retention, loading, errors and recovery. Compare related pages' anchors and visual language under corresponding conditions; page responsibilities can justify different compositions. Use geometry, contrast, accessibility, console/network evidence and image differences to diagnose causes or verify measured properties—pixels establish perceived balance, material and motion, while audience comprehension requires real user observation.

Attribute external observations to **carrier page, player, depicted product UI or displayed work/content**. Carrier DOM/requests explain its page or player, not the depicted application. Identify edited promotion, authored demo or live operation with source/version and conditions; response, failure and completion require runtime evidence.

## Inspect a time-bounded visual episode

Observe **pre-trigger state → action → first feedback → progression → settled result** in references, candidates, trials and runtime. Demos expose a selected flow; authorized operations can fill return, interruption or recovery gaps. Playback, live observation or media analysis supplies inspection; file acquisition alone does not.

| Design object | Observation window | Extend it when needed |
|---|---|---|
| Micro-interaction or local transition | Before input through acknowledgment, motion and a readable settled state | Reverse, interrupt or repeat while the object is changing |
| Loop, dynamic background or spatial scene | Enough progression to reveal its cycle, changing emphasis and seam or return | Inspect peak reach/brightness, interacting cycles and relevant views; nonperiodic motion needs representative intervals |
| Scroll-driven change | Relevant entry, hold and exit at known scroll positions and direction | Reverse direction; inspect sticky, local and horizontal regions where relationships change |
| Asynchronous task | Before intent through waiting, intermediate feedback and the valid outcome or recovery state | Exercise early/late response, failure, cancellation and new intent during pending work |
| Navigation or connected journey | Linked episodes covering departure, transition, arrival and continuation/return | Preserve object, focus, scroll and shared-shell context across the boundaries |

When supported, view normally, pause/replay or enlarge key frames, then return to normal speed to judge rhythm using the [seven temporal qualities](interaction-and-variants.md#read-motion-through-perceptible-qualities), including hidden/replacement intervals and neighbors. Retain frame order, actual timestamps/event offsets, cadence, actions/states and clock source (planned screenshot delays never establish actual intervals). Tie frames/episodes to runs and mark resets or edits; open pivotal frames at useful size rather than relying solely on contact sheets. Extend sampling whenever seams, flashes, overlap, jumps or late updates appear; sparse samples establish sampled states, not intervening continuity, and metadata or a poster proves neither playback nor continuity.

For reproducible authored timelines or regression probes, fix source, stage/viewport, content, fonts, assets, initial state and seeds; seek explicit times when supported and record controlled clocks or remaining nondeterminism. Frame stepping, slowed playback and a [simulated clock](https://playwright.dev/docs/clock) reveal ordering and geometry, while natural-time observation separately establishes experienced pacing and runtime traces establish frame delivery. Check capture settings: [disabling screenshot animations](https://playwright.dev/docs/api/class-page#page-screenshot-option-animations) can fast-forward finite animations and reset infinite ones, so keep motion enabled in a separate natural-progression run. Record masks, injected styles or overlays and keep focus/caret indicators visible when inspecting them. After repairing an interval defect, reinspect both the interval and complete return episode.

## Choose methods for the evidence question

Begin with visible behavior; use host-supported inspection to resolve a named uncertainty, then interpret the result in the rendered experience. Verify tool/version coverage and permissions before use.

| Question | Useful capability and its boundary |
|---|---|
| Which resource arrived, and what requested it? | [Network](https://developer.chrome.com/docs/devtools/network/) exposes observed requests, types, content and initiators |
| What happened to playback? | [Media](https://developer.chrome.com/docs/devtools/media-panel) exposes player properties, events, messages and playback/buffering timelines |
| How does a supported animation progress? | [Animations](https://developer.chrome.com/docs/devtools/css/animations) supports pause, replay and timeline inspection; verify rendering-mechanism coverage |
| Which action/state/request preceded the change? | [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer) correlates captured action snapshots, filmstrip, console and network evidence |
| Did the runtime deliver frames and respond as intended? | [Performance traces](https://developer.chrome.com/docs/devtools/performance/reference) support measured timing; captured filmstrips retain sampling limits |

Stay within authorized page/resource access and preserve sensitive traces inside authorized destinations. [Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) and [interaction patterns](https://www.w3.org/WAI/ARIA/apg/) guide accessibility checks.

## Inspect from whole to detail and back

Apply the [multiscale perceptual method](principles.md#inspect-from-whole-to-detail-and-back) at normal use scale: whole impression, composition, consequential regions/details, then whole task. Retain neighbors and context; after a repair, recheck hierarchy across affected states, pages and episodes. Keep observed facts (“the summary sits a full viewport away”) distinct from interpretations (“the gap weakens grouping”) and verify causes through comparison or implementation evidence.

### Preserve three distinct levels of visual observation

**Whole surface:** identify the primary task, dominant subject, information order, total visual mass and intended character. Check whether the user's next meaningful action and reading path are discoverable without explanation from the designer.

**Relationships:** inspect grouping, alignment, comparison structure, proportions, image/text balance, shared shell and spatial anchors. For a transition, inspect which relation it reveals, what stays stable and whether other areas move unexpectedly.

**Details:** inspect actual typography and copy, image boundaries and crops, icon weight, material edges, focus visibility, native controls and timed feedback. Judge the details against the selected craft target rather than unrelated stylistic preferences, then return to the full composition to see whether the improvement holds.

Assess task correctness and accessible operation, communication clarity, identity/coherence and implementation craft as complementary obligations rather than a weighted score that hides a critical failure. Automated geometry, console, network and accessibility checks establish measured properties; source images, actual human-visible rendering and meaningful task operation remain essential to judge the visual result.

Assess **experience validity** and **expressive completion** independently: can people understand and complete the task reliably, and does the promised art direction materialize with mature assets, composition, detail and motion across first encounter, populated core work, long content, repeated use and related views? Strength in one never compensates for a gap in the other.

## Findings and repair

Connect viewed state/interval, phenomenon, task/perceptual effect, intent, cause to test, repair and recheck. Prioritize blocked tasks, hidden controls, shared defects and consequential composition, craft or continuity failures. Locate the weak relationship before tweaking local coordinates—repair structure, meaning or source selection before tuning parameters.

Identify the responsible layer: unsuitable source, damaged adaptation, content/structure mismatch, conflicting resources or an unworkable target. Preserve accepted art direction while repairing concrete legibility, operational or runtime problems; make any necessary direction change explicit. When a finding materially alters design judgment, surface it via [event-driven disclosure](workflow.md#make-consequential-design-work-observable), keep uncertain causes separate from visible facts, execute the repair and reinspect both the target scope and affected neighbors. Keep findings active in the Current Design Model until evidence or an explicit scope decision resolves them; when splitting or redrawing an active SPEC, carry open findings and their actual conditions into the receiving increment rather than letting a new SPEC label erase them. Retain reusable lessons as *problem, mechanism, conditions, editable realization, evidence and limits* while keeping project preferences local.

## Comparing SPEC and connected product

Distinguish **Source Fidelity** from **Perceptual Quality**. Fidelity protects an identified approved design or adopted mature source (structure, assets, type, proportion, material, behavior); perceptual review judges actual composition, craft and continuous experience. Authorized original work carries its own quality and fidelity boundary; reference study alone supplies neither authorization nor implementation adoption.

For strict restoration, match target/revision, content, viewport, pixel ratio/zoom, browser rendering, fonts, themes, locales and event phase. Use overlays, regional diffs or pixel metrics with disclosed masks to locate deviations—never to certify design quality. Align episodes by meaningful events and object identity, keeping reproducible fixtures beside real-service evidence.

## Status meanings and presentation readiness

- `planned`: declared coverage, not yet executed.
- `pass`: specified check executed, visually inspected where applicable, with evidence.
- `fail`: observed issue remains open.
- `blocked`: required capability, resource or permission is unavailable.
- `waived`: explicitly accepted exception with reason, scope and approver.

Distinguish capture, pixel viewing and interaction testing. Without image/video viewing, runtime checks may run while visual judgment stays explicitly pending. After code or asset edits, recapture affected views/episodes before extending claims.

For formal delivery, present operable/renderable work in its product context with required checks complete, blockers resolved and uncertainty scoped. Keep Overview, Design Detail and Execution & Assurance aligned in both records and conversation handover (inherited foundation, consequential resource choice, local and related-product checks, representative before/after frames or episodes, open gaps and next useful increment). Earlier work can be shown provisionally with unfinished scope explicit.

## Empirical regression guardrails

Verify these recurring high-impact failure points explicitly whenever the surface includes interactive controls, async flows, overlays, 3D/motion transitions or narrow viewports:

1. **Keyboard focus return after interruption, failure and dismissal:** after clicking Stop, triggering a Save failure or dismissing a modal/dialog/drawer, verify `document.activeElement` lands on a meaningful visible trigger, error recovery control or active input—never stranded on `BODY`, `null` or a hidden/disabled button.
2. **Mid-transition `inert` and `aria-hidden` synchronization:** during card flips, drawers, accordions and pane swaps, verify hidden faces and offscreen containers toggle `inert` / `aria-hidden` in lockstep with live visual geometry so keyboard Tab order and pointer hits cannot fall through to obscured controls mid-animation.
3. **Narrow-viewport (`390px`) first-screen ergonomics and overflow affordances:** verify primary content or the main editor begins cleanly inside the first screen (`y`-position not pushed off-screen by stacked banners/hero chrome); verify horizontal-scrolling tables expose clear visual scroll affordances and keyboard horizontal scrolling; verify sticky headers and fixed toasts never occlude navigation controls or first visible reading lines.
4. **Immutable visual evidence filenames:** save initial trial captures and post-fix captures under distinct filenames so earlier evidence is never overwritten and visual regressions or upgrades remain directly comparable.

## Target-demo vs. integrated-app visual delta and craft retention

Verify **Resource Acquisition**, **Resource Adoption** and **Craft Retention** at their separate boundaries across the [four evidence objects](component-sourcing.md#confirm-consequential-parts-in-a-local-trial): **Target Reference → Candidate Original Demo → Local Project Trial → Integrated Product Journey**. An installed package, copied file, attribution notice or attractive demo screenshot proves neither call-site adoption nor retained visual quality in the running app. Conversely, an attractive screenshot of newly hand-authored code does not prove mature source adoption.

Inspect original source settings before editing them, then compare the candidate demo side-by-side against the local trial and integrated UI under matched fonts, real content density, theme, viewport and temporal phase, auditing these specific optical and structural deltas:

- **Rendered font metrics and fallbacks:** verify intended webfonts loaded (no silent fallback to Arial/system sans shifting measure, button widths or line wraps).
- **Text rasterization sharpness:** inspect tight crops on resting interactive cards, modals and animated panels to catch **resting 3D transform blur** (subpixel fuzziness caused by lingering `transform-style: preserve-3d`, unflattened `rotateY(0deg)` / `translateZ(0)` or permanent GPU layer promotion on static text).
- **Surface luminance, hairlines and light direction:** verify elevation steps, subtle 1px hairlines, glow/backdrop filters and directional shadows survived integration rather than being erased by a page background, reset or `overflow: hidden` wrapper.
- **Concentric radii and spacing cadence:** confirm nested borders follow concentric radius geometry (`R_outer = R_inner + padding`) and internal spacing/padding rhythm was not collapsed or distorted by global overrides.
- **Motion easing and state ownership:** confirm original easing/spring physics, state transitions and focus/scroll behavior survived wiring to real handlers without duplicate listeners or displaced state owners.
- **Mobile first-screen ergonomics:** verify the adopted block or page retains readable proportions and primary-task visibility at `390px` width.

**Check for negative whole-product integration effects.** Adding more mature resources can still degrade whole-product coherence through competing focal points, clashing typography or material grammar, fractured spacing, motion/listener interference, bundle cost or maintenance burden. Retain any counterexample and repair composition, harmonization or source selection rather than chasing higher dependency counts. Report setup, adaptation, defect repairs and maintenance obligations honestly without inventing hours saved.

For W1–W3 work, verify exact qualification, scoped user authorization, retained mature foundation and independent craft/behavior evidence; neither a successful render nor a JSON declaration retroactively authorizes original construction. For provisional technical probes, confirm their research findings stay distinct from formal visual delivery until replaced by mature work or covered by an authorized exception.

## Verify assets, content, publishing and operational change

- **Visual assets:** trace source/rights → transformation → derivative → actual placement using [asset-family checks](visual-assets.md#accept-the-asset-in-use) (small-size silhouette/weight, glyph coverage, crop/alpha/color, spatial material fidelity, temporal states) under actual CSS size, density, theme, blocked-resource, quiet and offscreen states.
- **Content and meaning:** verify headings, labels, help, validation, status, empty, error and recovery copy across real actions, locales, themes and screen-reader announcements; confirm interface promises match authoritative outcomes (`saved`, `submitted`, `paid`, `published`).
- **Publishing medium:** for `README` and docs, check hierarchy, selectable text, copyable commands, links, alt text, image widths, narrow code/table scrolling and host readback (local approximation ≠ live host). A video of a UI does not establish its operability; verify diagram semantics and generated assets' delivered bytes alongside editable sources, matching every claim to the observed medium. Keep design research commentary out of user-facing product UI, demonstrating promised material and motion through rendered objects rather than labels asserting quality.
- **Motion, growth and operational workflows:** test full motion episodes, reversal/interruption, reduced motion, late fonts/assets, long content growth inside scrolling containers, template vs. override propagation across locales, multi-page batch selection, mixed partial outcomes and role-specific views (customer vs. operator).

## Measure performance across the complete task

Choose measures from the operation people need to finish. Record task, initial data/cache, device/browser, network, workload and revision. Separate immediate feedback, usable content and authoritative completion, then trace the relevant dependency; a responsive acknowledgment can coexist with a slow service result.

| Experience question | Useful observation | Interpretation boundary |
|---|---|---|
| Is input acknowledged promptly? | Input delay, handler work and next relevant presented frame | Responsiveness covers a different boundary from service completion |
| When is the next action possible? | Marks from entry/input to usable content or confirmed outcome | Name local readiness, server acceptance or completed work explicitly |
| Does motion remain smooth? | Natural-time observation plus frame timing, long tasks and dropped/presented frames | A screenshot, sampled clip or average rate can hide a stall |
| Does the task remain stable? | Layout shifts plus focus, object and scroll continuity | Layout metrics cover only their defined shifts |
| What does preparation cost? | Requests, bytes, duplicate work, concurrency, decoding and sustained resource use | Compare saved waiting with unused work |
| Are stressed results correct? | Object state, response ownership, partial outcomes and recovery | Optimizations preserve required business results |

Use field observations where available and controlled runs for diagnosis/regression ([user-centric metrics](https://web.dev/articles/user-centric-performance-metrics), [INP](https://web.dev/articles/optimize-inp), [Performance.measure](https://developer.mozilla.org/en-US/docs/Web/API/Performance/measure)). Keep automation elapsed time, double-animation-frame samples and video encoding rate distinct from field INP and application frame delivery. Compare equivalent cold/warm before/after runs under realistic volume, rapid inputs and slow/failing boundaries, reporting both measured gain and cost.

## Keep evidence maps, records and scoped assertions independent

Reconcile coverage, source roles, decisions, adopted locations and checked conditions in both directions using [the evidence map](evidence-map.md) and [evidence-to-action rules](evidence-actions.md): decisions resolve to supporting evidence and actual call sites, while changed dependencies trace back to affected claims. Keep acquired, observed, compared, trialed, adopted, verified, blocked, waived and owner-approved facts separate; global snapshot changes never mechanically invalidate unrelated visual history—evaluate actual changed objects and dependencies to decide what carries forward vs. requires recheck.

Optional read-only structural inspectors—[manifest inspector](../scripts/check_manifest.py) (`--view checks --json`) and [evidence inspector](../scripts/check_design_evidence.py) ([record profile](evidence-records.md))—report literal declared fields, IDs, paths and theoretical category prompts only. Exit `0`, readable JSON or a passing automated assertion proves its exact scoped check, never adequate research, retained visual craft or task completion. When delegating capture, challenge or bounded checks to auxiliary roles, follow [delegation guidance](delegation.md): the main agent directly views pivotal visual evidence and owns final assembled verification.

## Taste and craft-defect audit

**Functional pass is not aesthetic completion.** Before concluding an increment or audit, step back and inspect the rendered desktop and mobile captures with a critical design-director eye—explicitly looking for flat, generic, cramped or multi-source Frankenstein results that survive automated DOM and layout tests untouched.

Audit every consequential surface against [AI-slop and generic-UI failure signatures](principles.md#diagnostic-generic-ui-and-ai-slop-failure-signatures) and the [six operational craft calibrations](principles.md#six-operational-craft-calibrations):

| Observed craft defect | Concrete visual indicators | Mandatory upgrade route |
|---|---|---|
| **Generic / template-like feel** | Unadapted stock components, cookie-cutter card grids, default system sans, cliché gradients or absent focal craft moment | Re-source higher-completeness work via multi-tier discovery ([component sourcing](component-sourcing.md)) or apply [source-preserving de-genericization](principles.md#source-preserving-de-genericization-and-visual-harmonization) |
| **Flat, lifeless hierarchy** | Collapsed luminance steps, timid display-to-body type contrast, uniform gray borders, missing directional light/shadow depth | Recalibrate luminance ladder, typographic scale tension and ambient+contact edge/shadow tokens without breaking source structure |
| **Frankenstein multi-source seams** | Mismatched corner radii, conflicting icon stroke weights, inconsistent padding scales or clashing dark-mode neutrals across adopted blocks | Unify adopted components onto one canonical token system and isolate CSS cascade layers (`@layer`) |
| **Degraded adopted rendering** | Silent webfont fallback, resting 3D transform text blur, clipped glow/backdrop shadows or distorted spacing vs. candidate demo | Repair rendering fidelity (flatten resting 3D transforms, restore font metrics, fix clipping wrappers) and re-compare against the demo |
| **Visual noise / cramped chrome** | Borders around every sub-group, redundant status pills, stacked banners pushing core content down on `390px` mobile | Subtract non-load-bearing chrome and borders, restore relational whitespace and lift the primary task cleanly into the first screen |

Route every diagnosed craft defect to its responsible upgrade, capture a fresh **immutable post-fix screenshot**, and re-inspect whole → relationships → details → whole before declaring the increment ready for presentation.
