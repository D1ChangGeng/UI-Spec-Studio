# Verification: coverage, inspection and honest evidence

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

Keep three evidence scopes distinct: source documentation establishes a platform capability; a demo and exact implementation support an item assessment; the assembled product establishes project acceptance. Record the source revision/variant and demonstration settings needed to reproduce important effects. A link failure describes access on that attempt; seek another legitimate route and retain the unobserved scope accurately.

Exercise the adapted item with representative content, supported inputs, real container constraints, theme/locale variants and product states. Check semantic behavior, visual fidelity, combined attention/runtime cost, cleanup and the relevant service boundary. Preserve rights and notices with the adopted material. Regression scope follows the component or shared system affected.

A catalog lookup is discovery evidence. A mocked retrieval or record test verifies its declared mechanics. Report actual demo, image-inspection and integration observations separately. Use the project's existing evidence location; an optional adoption note can connect the significant decision to these observations.
