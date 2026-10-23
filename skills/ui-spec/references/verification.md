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
