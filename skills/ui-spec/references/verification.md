# Verification: coverage, inspection and honest evidence

## Contents

- [Coverage and assurance](#build-the-coverage-inventory-from-reality)
- [Viewing conditions and actual interaction](#capture-the-actual-viewing-condition)
- [Findings, comparison and status](#findings-and-repair)
- [Judgment at three scales](#read-the-result-at-three-scales)
- [Publishing and resource adoption](#verify-the-publishing-medium)
- [Decision, asset and content evidence](#verify-the-design-decision-chain)
- [Performance across the complete task](#measure-performance-across-the-complete-task)
- [Motion, growth and operational change](#exercise-motion-growth-and-operational-change)

## Build the coverage inventory from reality

Reconcile the route configuration, navigation, authorized roles, overlays, runtime states and existing UX records. Include every implemented in-scope page family. Dynamic records use representative data shapes, lengths and permissions; list the sampling rule. An implemented route without a legitimate product entry is a finding.

Keep a complete inventory of implemented surfaces, and declare the current verification scope separately. A round checks its changed scope and affected dependants; final scope acceptance reconciles the full approved inventory. State the scope whenever reporting coverage.

Declare the supported viewport set and theme/locale combinations for this scope. Every route's primary state must be inspected at every declared viewport and variant. Exercise every additional critical state in each declared variant, with more viewport combinations wherever layout or risk differs. Record additional requirements explicitly. Use approved, explained exclusions for out-of-scope conditions rather than silently dropping them.

A reasonable starting set for a desktop-focused web product might include a compact laptop, a conventional desktop, a large desktop and a supported narrow layout. Choose actual dimensions from target use and include a short-height case. A mobile-first product starts with its phone widths and input constraints. Fixed numbers are not a universal product requirement.

## Match assurance to impact

A local component adjustment needs the affected component states and representative surrounding layout. A shared shell or token change needs its dependent page families. A new journey needs actual task transitions and recovery. Integration needs both visual and real-behavior checks. Supported variant combinations follow an explicit matrix chosen from actual product requirements; user-requested exhaustive coverage remains exhaustive.

Use representative samples to expose different data shapes, lengths, roles and layout conditions. Explain sampling where it changes what can be claimed. Full inventory and selective round checks can coexist because their scopes remain visible.

This reference governs product work, not a requirement to run large comparative model evaluations. Package/tool tests, logical scenario review, real browser inspection and real integration each establish different facts.

## Capture the actual viewing condition

Set the browser's CSS viewport directly. Record dimensions, device pixel ratio, browser, locale/theme, fixture identity and target revision. Distinguish browser zoom and text enlargement from a scaled design-preview canvas. Open the actual route or independently sized frame rather than assessing a screenshot of a fitted thumbnail.

Wait for the relevant page state, fonts and images. Control fixture data, time and animation state for comparisons. Screenshots should include the whole browser content viewport: shell, background, content and surrounding space. Browser chrome itself is not required for a web-content capture.

Capture two kinds of evidence when needed:

- **Viewport evidence:** the actual visible frame at the intended dimensions, including top/bottom relationships and scroll boundaries.
- **Content evidence:** document-length captures or multiple real-scroll checkpoints. Internal scroll containers need their own checkpoints; a full-document capture does not automatically reveal their hidden contents.

Keep layout conditions stable while recording content. Resizing the viewport until a long page fits changes the experience being verified. Include important sticky, overlay, short-height and lower-scroll positions. Record horizontal scrolling only where intended by the content/task.

## View the images and use the interface

Open each required capture with available image-viewing tools. Inspect composition, scale, occupancy, typography, contrast, whitespace, alignment, clipping, assets and persistent controls. Run the task through real UI affordances. Observe navigation, keyboard focus, input retention, loading, error/retry and rapid state changes.

Evaluate cross-page anchors by switching within the same shell under equivalent viewport/scroll conditions. Evaluate motion live or with a short recording; a frozen frame cannot establish continuity. Review reduced-motion and theme/language switching as relevant.

Use automation to check geometry, overflow, accessible names, links, console errors, network failures and screenshot diffs. Use the rendered images and task execution to assess aesthetics and usability. A mechanical check is evidence only for what it measures.

## Findings and repair

Record each actionable finding with page/state/view, severity, observation, evidence, design intent, root layer, repair and retest. Prioritize task blockers, unreadable/hidden controls, shared defects and prominent compositional errors before minor details.

Repair at the responsible layer: design token, shell, component behavior, page composition, data contract, asset or animation. Review neighboring screens that share it. Preserve approved context and unrelated user changes.

## Comparing SPEC and connected product

Use equal fixture/service-shaped content, viewports, fonts, themes, locales and states. Retain approved evidence tied to its revision. Explain intentional differences, such as real data length. Keep a stable fixture mode to reproduce design regression while real-service tests validate behavior. The reference is reviewed design intent plus reproducible evidence, not an unchangeable absolute truth.

## Status meanings

- `planned`: declared coverage, not yet executed.
- `pass`: the specified check was executed, inspected where visual, and has evidence.
- `fail`: an observed issue remains.
- `blocked`: a required capability, resource or permission is unavailable.
- `waived`: an explicitly accepted exception with reason, scope and approver.

An unavailable browser permits code review and other tests, while visual verification remains blocked. State the exact missing capability and continue independent work. Review a current revision before asserting a previous approval still describes it.

## Decide when to present the round

A round is ready for review when the promised task is inspectable, required checks are complete, observed blocking defects are resolved and remaining uncertainty is described at its actual scope. A user can review design while an external integration remains pending; label those separate states.

When browser or image inspection is unavailable, record visual verification as blocked, complete permitted source/contract checks and identify the exact missing observation. A precise partial result is useful; its evidence keeps its original meaning.

## Lightweight checker

`python <skill-dir>/scripts/check_manifest.py --project-root . --mode review`

The optional manifest checker validates declared coverage and evidence references. `--mode finish` also checks recorded approvals and real integration cases. It does not launch browsers, inspect pixels, verify a human's identity, or certify the product. Its output states those limits.

For an existing project with an adequate native test matrix, use that matrix and report equivalent facts rather than duplicating it.

## Primary references

- Playwright screenshots: https://playwright.dev/docs/screenshots
- Playwright emulation: https://playwright.dev/docs/emulation
- Playwright visual comparisons: https://playwright.dev/docs/test-snapshots
- W3C reflow guidance: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- WAI interaction patterns: https://www.w3.org/WAI/ARIA/apg/

## Read the result at three scales

**Whole surface:** identify the task, dominant subject, information order, total visual mass and intended character. Check whether someone can discover what to do or understand without the designer's explanation.

**Relationships:** inspect grouping, alignment, comparison structure, proportions, image/text relationships and the shared shell. Check which relationship a transition makes visible and whether unrelated areas remain stable.

**Details:** inspect typographic roles, real copy, image edges, icon weight, surface boundaries, native controls, focus and timed feedback. Compare against the project's craft target and intended identity rather than unrelated stylistic preferences.

Record observation separately from interpretation. “The summary is separated from the items by most of the viewport” is an observation; “the groups feel unrelated because their distance outweighs the section grouping” is a hypothesis to test. Cite the actual frame/state for either. A screenshot alone cannot establish unseen interaction or audience response.

## Diagnose and improve the strongest relationship

Find the most consequential weak relationship before choosing a parameter to change. Structural or semantic errors deserve structural repairs; detail polish follows a coherent composition. Compare under controlled conditions and change one causal group of variables at a time where useful. Batching related fixes is efficient when their effects remain attributable.

A positive reference helps define the intended quality: why its comparison reads clearly, why its image carries the subject, or how its transition preserves orientation. Identify the condition that makes the technique work before applying it here. Identity-bearing features merit explicit checks even when other details are polished. Mechanical metrics diagnose their measured properties; aesthetic quality has no universal numeric pass score.

Assess task correctness and accessible operation, then communication clarity, identity/coherence and execution craft. This is a review order, not a weighted total that permits a critical failure to disappear in an average. Record an actual improvement as a scoped observation, keeping assumptions about broader user response explicit.

## Verify the publishing medium

For a README or documentation artifact, inspect hierarchy, selectable text, copyable commands, local links, alt text, image width, narrow-screen code/table handling and light/dark variants. Check the actual host-supported markup. A locally rendered approximation is labeled with its renderer and cannot alone prove remote platform appearance.

For diagrams, confirm data/relationship semantics before styling. For timed output, inspect meaningful intermediate states, readability and final playback. For externally generated assets, inspect the delivered file as well as its editable source. Match claims to the output and environment actually observed.

## Retain lessons with boundaries

When a technique materially improves a result, preserve the problem, mechanism, relevant conditions, editable realization, evidence and observed limits in an appropriate existing record. Keep a project-specific preference with that project. A portable example can be proposed for the skill's maintained repertoire with clear provenance and maintenance authorization.

These records make future decisions better grounded; they do not establish automatic model improvement. Favor a few explanatory examples over a catalog of unexplained attractive screenshots.

## Validate resource adoption in context

Separate discovery, item assessment and project acceptance. Catalog/source documentation establishes leads or capabilities; an inspected demo and exact source support the item; the assembled product needs its own checks. Record revision, variant, demo settings and rights. A link failure leaves that observation pending.

Apply the coverage and inspection methods above to adopted items and their dependants, including combined attention/runtime cost, cleanup and service boundaries. Keep mocked retrieval/record tests distinct from actual demo, render and integration evidence.

## Verify the design decision chain

Check the model, primary action, continuation, alternatives and selection authority. Existing UI reuse needs approval or target-based fit; one-shot direction remains provisional until accepted.

Open the decision record beside the preview. Trace choices from convention/source to code and visible state; reconcile retained, replaced and authored work. Exercise first-use, active work and resume.

An anonymized fixture establishes its exercised paths. Original-product verification, independent model evaluation, user research and owner approval remain separate evidence.

## Inspect inherited design value

Compare inherited hierarchy, proportions, reading rhythm and state continuity with the rendered product. Explain reuse scope, adaptations and original contributions. Attribution proves origin; real tasks establish retained value. Distinguish a static port, runtime integration and accepted product.

## Verify assets from master to placement

Follow the asset record from source and permission through transformation, derivative and actual placement. Inspect the delivered bytes rather than only the authoring preview. Apply the common [asset-family checks](visual-assets.md#accept-the-asset-in-use): small-size silhouette and optical weight; type/glyph readability and language coverage; image crop/alpha/color; spatial material and export fidelity; animation states and timing.

Record actual CSS size, density, theme, viewport, content and load conditions. Exercise meaningful blocked-resource, reduced-motion, offscreen and runtime-unavailable states. Separate isolated craft, combined visual quality and measured engineering cost. Whole-page captures, close details and live playback answer different questions. A PNG, file signature or passing metadata check does not establish editable 3D, font shaping or animation behavior.

Use a bounded real browser fixture to validate integration paths when full specialist tooling is outside the current environment. State which production routes were researched, executed or remain pending. Do not generalize that fixture into every asset family or host.

## Verify meaning and actual words in context

Inspect the full visible content scope: page and component strings, headings and navigation, labels, hints, instructions, status, validation, error, empty and confirmation states. Use task execution to inspect the information available at each decision and the outcome each phrase promises. Verify business facts against their owner; the UI reflects actual state, including delayed, denied, partial, unknown or failed results. Localize and inspect supported languages with realistic strings, typography, viewports and themes.

Check accessible names, explicit labels, error associations, announcements, truncation, overlap, line breaks and focus. Mechanical checks establish the properties measured; rendered review establishes rhythm and balance; actual user comprehension requires its own evidence. Compare related pages for terminology, placement and cross-step information responsibility. Explain findings at the content, structure, component, localization or authority layer, then recheck the affected journey.

## Measure performance across the complete task

Choose measurements from the operation people need to finish. Record the task, starting data/cache state, device/browser, network conditions, workload and source revision. Separate first response, usable content and authoritative completion, then capture enough of the execution path to identify the delay. A fast input acknowledgment can coexist with a slow business result.

| Experience question | Useful observation | Interpretation boundary |
|---|---|---|
| Does input receive timely feedback? | Event delay, handler work and presentation of the next relevant frame | Browser responsiveness does not measure all downstream service work |
| When can the user take the next meaningful action? | Task-specific marks from entry/action to usable content or confirmed result | Define whether the endpoint is local readiness, server acceptance or completed work |
| Does interaction stay smooth? | Frame timing, long tasks and dropped or interrupted transitions during the target operation | A screenshot or average rate can hide a consequential stall |
| Does the page remain stable? | Layout shifts plus observed focus, object and scroll-position continuity | A layout metric covers only its defined shifts; inspect task stability separately |
| What does preparation cost? | Requests, transferred bytes, duplicate work, concurrency, decoding and sustained memory/resource use | Compare saved waiting against work the user never uses |
| Does the result remain correct under stress? | Final object state, response ownership, partial results and recovery after repeated or delayed actions | Speed gains retain the same required business outcome |

Use field observations when available and controlled browser runs for diagnosis and regression. [User-centric metrics](https://web.dev/articles/user-centric-performance-metrics) connect measures to user experience; [INP](https://web.dev/articles/optimize-inp) concerns interaction responsiveness. Task-specific [performance measures](https://developer.mozilla.org/en-US/docs/Web/API/Performance/measure) require explicitly placed start/end marks. An automation elapsed time or a double-animation-frame sample retains that label and scope; it is not a field INP measurement.

Compare equivalent before/after tasks under the same conditions, with repeated samples where variability can change the decision. Include cold and warm paths, realistic content volume, rapid independent operations and relevant slow/failing boundaries. Check expiration and input changes when preparation or caching is involved. Choose budgets from product needs and target environments. Report the measured result and tradeoff; simulated service delays and desktop browser observations keep their stated limits.

## Exercise motion, growth and operational change

Inspect motion through its full relevant cycle and both directions, including interruption, reversal and reduced motion. Check object identity, face visibility, focus and interactive regions. Observe maximum visual reach and overlap with important content at supported viewports. A completed transition must show the current valid state; test responses arriving before, during and after it.

Exercise content expansion, late media/fonts, new records, long text and permission-dependent controls in the actual scrolling regions. Check lower content through real scrolling, sticky controls, overlay dismissal, keyboard reveal and position on return. Compare ready, loading and failure states for both component material and readability. Verify that collapsing a resolved choice preserves its meaning and any permitted way to revise it.

For maintained content and management workflows, change a shared template and an overridden item, then inspect the affected consumers and supported language versions. Exercise selection across pagination/filter changes, batch results with mixed outcomes, interruption and scoped retry. Confirm that completed work remains and reported counts match the actual item outcomes. Compare customer and operator views of the same service condition for consistent facts and appropriate actions. Derive repeated-task efficiency from observed steps, elapsed work and recovery effort at representative scale; a single default-state screenshot cannot establish it.
