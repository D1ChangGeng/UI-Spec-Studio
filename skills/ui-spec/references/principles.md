# Visual principles

## Understand the strength of each statement

**Invariants — requirements:** readable content, comprehensible hierarchy, valid task paths, accessible controls, visible focus, accurate state, stable shared structure, coherent feedback, truthful claims, inspectable evidence and trusted business boundaries.

**Principles — professional judgment:** typography scale, density, content widths, spacing rhythm, optical corrections, scroll ownership, animation timing and page composition. Apply them according to the task, input method and page family.

**Preferences — project direction:** palette, serif/sans typography, expressive vs restrained style, material effects, imagery, identity, preferred composition and motion intensity. Respect approved direction. A universal workflow serves multiple aesthetics.

**Defaults** offer a starting treatment when the brief leaves a choice open. **Examples** demonstrate reasoning in a particular context. Apply the requirement firmly, the principle with judgment, and the default according to the task. This distinction preserves a reliable quality floor and room for distinct visual work.

A designed interface makes consequential choices coherent: typography, content, imagery, composition and interaction support the same purpose. Precision can distinguish a dense tool; expressive art direction can distinguish a gallery. Give each surface the kind of ambition its user task benefits from.

## 1. Hierarchy follows meaning

Give the current task and its most useful information appropriate prominence. Arrange labels, values, actions and feedback by relationship. Use type, contrast, position and spacing together. Supporting information stays legible; visual simplification preserves required meaning.

Choose typefaces for language coverage, readability and character. Test actual scripts, punctuation, digits, weights, line-height and fallback rendering. Use typography and content width to establish readable rhythm. Long localized labels and realistic values belong in the review set.

## 2. Design tokens express a system

Use shared roles for foreground/background, emphasis, status, borders, elevations, typography, radii, spacing and motion. Tokens encode relationships rather than a screenshot's incidental coordinates. Shared components express interaction rules consistently.

Work at three levels: product-wide identity, page-family shell and page-specific composition. Changes at a shared level require related-page checks. Cross-page consistency does not require every kind of page to have the same width or top offset.

## 3. Core scale and composition occupancy

Judge core controls and the whole content composition separately. Stable control sizes can coexist with a responsive composition. A larger screen may allow wider containers, additional columns, broader contextual areas or more outer space; a narrower screen may reflow and reduce columns.

Evaluate readable dimensions, content density, dominant visual mass and distance between related elements. Use bounded fluid values where useful. Treat viewport percentages and ratios as diagnostic aids, not an aesthetic pass threshold. Browser zoom is a user accessibility control and must remain effective.

Distinguish CSS layout dimensions from CSS transforms, animated projection, preview fitting and screenshot display scaling. A card turned edge-on looks narrow without its layout box becoming smaller. Pause or standardize motion for static comparisons, then review the real transition separately.

## 4. Whitespace is relational

Separate internal padding, group spacing, section spacing and outer margins. Tighten related information; provide stronger separation between distinct tasks. Evaluate negative space around the composition as well as gaps within it.

Collections use meaningful component widths and consistent gaps. Container growth need not distribute a handful of items across the entire screen. For a justified gallery or a task requiring equal column allocation, record that intentional layout behavior. Width follows content and purpose rather than an unconditional rule.

## 5. Optical balance

Judge visual weight from text, component mass, imagery, contrast, depth, background and space. Geometric alignment is a tool. The resulting page should feel composed when viewed at the actual size.

For a compact, fixed-content task surface, visual centering and a slightly upper-centered composition are equally useful starting preferences; a slightly lower center warrants a reason grounded in the composition. Keep controls comfortably reachable and allow short viewports to scroll. Reading surfaces begin at a readable top origin; workspaces follow stable navigation; expressive layouts can intentionally be asymmetric. A project's stated preference can refine this heuristic.

Inspect the entire frame rather than declaring balance from `top: 50%`. Keep the dominant mass comfortably within the usable frame; reserve deliberate extreme placement for a brief that benefits from it. Evaluate dynamic backgrounds across time so transient highlights do not undermine readability or perceived balance.

## 6. Page-family anchors remain stable

Headers, tabs, navigation and content start positions within the same family remain stable at matching viewport and scroll conditions. A short settings panel and a long activity list inherit the same shell. Their content areas handle their own growth.

Switching tabs or records preserves shared component identity and relevant focus/input/selection. Allow intrinsic size changes where necessary, while controlling how neighboring content moves. Validate slow loading and errors as well as steady states.

## 7. Choose layout by task shape

| Shape | Primary considerations |
|---|---|
| Public introduction / marketing | Clear subject, meaningful sequence, distinctive direction, primary action and useful further exploration. |
| Reading / documentation | Comprehension, text measure, headings, navigation, links, reading progress and natural document scrolling. |
| Compact focused task | Appropriate form/subject occupancy, near-balanced vertical space, accessible entry and completion. |
| Multi-column task | Related zones, purposeful width allocation, alignment, priority, stacking and independent growth. |
| Workspace / editor | Stable chrome, task density, selection/focus continuity, deliberate scroll ownership and tool reachability. |
| Collection / detail | Predictable item scale, scanability, filters, pagination/virtualization when justified, content-length resilience. |

These categories can coexist within one product. Use the shape of the surface rather than the brand's business category to choose its behavior.

## 8. Motion supports continuity

Every transition has a purpose: feedback, revealing a relationship, preserving orientation or explaining a change. Match timing and emphasis to interaction frequency and context. Repeated actions deserve immediate feedback and low friction.

Prefer predictable, interruptible transitions for reversible interactions. Anchor menus to their triggers, preserve shared identity during option changes, and keep layout boxes stable when effects only change the visual layer. Check actual rapid interactions, reduced motion and low-capability devices.

## 9. Scrolling is a design decision

Choose document scrolling for natural reading and content growth. Use internal scroll regions for bounded workspaces when they improve orientation. Each region has a clear owner, reachable content, keyboard behavior and sensible restoration. Horizontal scrolling is appropriate for genuinely two-dimensional content with a clear affordance.

Style scrollbars consistently within the supported platform's capabilities. Honor operating-system visibility and high-contrast preferences. Any fade treatment preserves discoverability and operability. Keep content width stable when scrollbars appear. Test shorter viewports, zoom, virtual keyboards, expanded content and overlays.

## 10. Variants are complete designs

Themes have coherent semantic color and elevation roles. Languages have natural copy, appropriate typography and formatting. Content extremes, permissions and failure states retain the same design quality as the default screen. Shared labels and state feedback belong to centralized mechanisms where the project supports them.

Icons share stroke/shape/weight conventions, semantic labels and usable targets. Group utility, identity and global-navigation controls by meaning and usage. The order follows the project's mental model and input constraints.

## 11. Visual judgment and measurements work together

Use DOM geometry, contrast tools, screenshot differences and performance traces to locate issues. Then view the rendered result, complete tasks and make the aesthetic judgment. Automated success is evidence for a particular check, not a substitute for looking.

Compare equivalent content, theme, locale, browser, viewport, font readiness and animation state. Document intentional differences. A coherent screenshot does not establish that the real API, permissions or persistence are connected; those need separate behavioral evidence.

## Diagnose a relationship before changing a coordinate

When a screen looks oversized, separate the control scale, dominant content mass, reading distance and surrounding space. A wider container or smaller gap can correct occupancy while preserving legible controls. When a screen feels too low, inspect the complete frame, image weight and shared shell before changing its vertical origin.

When related pages shift during navigation, preserve the family anchors and solve local balance inside the content region. When a real response introduces a long label or error, allow the content its necessary space and re-evaluate neighboring alignment. These are examples of reasoning, not prescribed layouts.

Fix a shared cause at the token, shell or component level when the evidence supports it. Revisit the affected family under comparable conditions. Read the result visually; use numeric measurements to explain and reproduce the diagnosis.
