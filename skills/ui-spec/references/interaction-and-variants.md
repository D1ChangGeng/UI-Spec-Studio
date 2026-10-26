# Interaction, accessibility, language and themes

Align interactions with the current task. Study mature behavior through its relevant controls and states, then verify the inherited relationships in composition and runtime.

## Contents

- [Controls, objects and choices](#control-semantics-and-focus)
- [Language and themes](#language-and-content)
- [Motion and temporal qualities](#motion)
- [Scrolling and growth](#scrolling-and-content-growth)
- [Task and resource continuity](#continuity-is-a-user-visible-contract)
- [Responsiveness and preparation](#preserve-the-primary-loop-and-perceived-responsiveness)
- [Asset and content states](#assets-have-runtime-states)

## Control semantics and focus

Use native elements or suitable accessible primitives. Name icon-only controls and provide usable targets; hover hints supplement names and touch. Follow each control pattern's focus entry, movement, dismissal and return. When a control disappears, return focus to a usable, visible task element.

Complete key paths with keyboard and pointer/touch. Check focus visibility, pending/disabled semantics, field-error association and useful announcements. Reinforce color status with language, shape or icons. Meet the project's accessibility target and report the checks actually performed.

Reference patterns: https://www.w3.org/WAI/ARIA/apg/
WCAG 2.2: https://www.w3.org/TR/WCAG22/

## Objects, choices and action relationships

Choose a carrier from the recognizable object and task: a product, record, file, conversation or media item may suit a card, row, table, message or editor. Preserve identity and selection as details and actions change. Make object-level opening or transformation discoverable; keep independent actions separately operable and avoid nested interactive targets.

Offer controls for real choices; show determined values and permitted revision clearly. A single option can need confirmation without a multi-option selector. Establish primary/secondary, peer, sequential or consequential relationships before assigning weight and position.

Judge material and state together: resting, hovered, focused, expanded, selected, pending, disabled and invalid where supported. Inspect text, icon, border, translucency and elevation against the actual background. Clear selection, contrast and focus remain necessary on glass or decorative surfaces.

## Language and content

Localize menus, dialogs, validation, empty states and dynamic product text with natural, consistent terminology. Preserve fixed identifiers, brand names and user-authored content.

Define locale initialization, preference priority and persistence; preserve the task during switching. Format dates, numbers and units according to the contract. Language selection does not itself change stored values or contractual currency. Check long labels, actual responses, mixed scripts, font fallback and supported writing direction. Define missing-translation fallback and make omissions discoverable during development.

## Themes and perception

Map surfaces, type, borders, focus, status, elevation and effects to semantic roles. View each theme under actual backgrounds and font rendering: brightness and contrast affect perceived weight and legibility.

Define initialization, system preference and explicit overrides; establish theme before meaningful paint. Keep all components coherent and retain task state during switching. Controls communicate action or current state consistently. Group locale, theme, identity and navigation utilities by meaning.

## Motion

Name the event and purpose: entry, navigation, manipulation, local change, feedback or expressive emphasis. Choose timing, trajectory and easing for its meaning and frequency. Inspect corresponding reference, demo, trial and integrated episodes; recheck affected motion after theme, container or state-adapter changes. Endpoints leave the transition unresolved.

Preserve object identity through expansion, reversal and return. A flip needs coordinated faces, pivot, visibility and active hit regions; test reversal from intermediate positions. Acknowledgment can begin before data arrives, while pending presentation carries unresolved work. A completed animation does not establish business completion.

Compose the full movement: rotation, scaling, particles, shadows and brightness extend beyond a resting box and shift visual weight. Observe text clearance, hierarchy and material coherence across the range. Adjust amplitude, layers, masks, layout or delivery, then judge the complete scene again. Deliberate overlap retains readable content, recognizable motion and operable targets.

Honor reduced-motion preferences with equivalent meaning and access; retain identity through type, composition, material and static relationships. Provide appropriate control for prolonged nonessential motion. Essential information remains available through keyboard and touch without optional pointer effects. The [temporal method](verification.md#inspect-a-time-bounded-visual-episode) governs behavior-sized windows, sampling and evidence limits.

## Read motion through perceptible qualities

Judge these connected qualities in actual episodes; correlate findings with code, state and traces. Use them for diagnosis rather than a single aesthetic score.

| Quality | What to observe | Design decision it informs |
|---|---|---|
| Temporal continuity | Input, acknowledgment, change and completion have clear order and readable holds | Sequence dependencies without delaying unrelated work |
| Object continuity | Shape, content, pivot, position and selection retain identity through change | Coordinate anchors, replacement, reversal and return |
| Motion quality | Speed, easing, trajectory, rhythm and settling fit the event | Tune paths and timing, including frequent/reversed use |
| Dynamic composition | Moving elements, light and text retain hierarchy and usable space | Coordinate effects, bounds, masks and foreground placement |
| State and feedback alignment | Progress, content, animation and controls describe the same outcome | Bind presentation to valid intent and authoritative readiness/completion |
| Temporal stability | Late resources, content changes and repeated input retain layout and control | Reserve space, reconcile stale responses and preserve focus/scroll |
| Cross-view continuity | Navigation, overlays and task steps retain identity and orientation | Coordinate chrome, transitions and return/resume state |

A stationary trigger can clarify expansion; an unrelated shifting panel can weaken it. Compare episodes when selecting candidates. Diagnose material, wording, layout and state ownership alongside easing.

## Resilience

Exercise short heights, text/browser zoom, mobile keyboards, safe areas, slow assets, offline/errors and repeated actions where relevant. Reflow preserves content and operation. A table or editor may use scoped horizontal scrolling while the surrounding page remains usable.

Use fixtures for reproducible scenarios and real integration for service responses, authorization and persistence.

## Scrolling and content growth

Choose scroll ownership from the task and content growth: continuous reading often suits a document; workspaces may retain navigation around a local region. Give regions clear roles. Observe entry, hold, exit and reverse browsing with scroll position/direction retained. Test wheel, touch, keyboard, focus reveal, sticky controls and overlays at relevant short heights and virtual-keyboard conditions.

Preserve reading position as content arrives or expands. Decide when to reveal a new result, retain an existing reading point or restore an object's position on return. Following a live feed and reading older material are distinct intentions. Pagination or virtualization needs stable anchors and usable search/focus/assistive behavior.

Coordinate scrollbar visibility, color and width with theme and platform behavior. Reserve space when classic scrollbars would shift composition; [scrollbar-gutter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scrollbar-gutter) has different effects for classic and overlay scrollbars. Verify discoverability and actual access to hidden content through the scrolling control.

## Continuity is a user-visible contract

Distinguish first entry, navigation, local edits and asynchronous feedback. Retain meaningful input, focus, selection and scroll; transition the part whose meaning changes. For rapid requests, show the latest valid intent and reconcile optimistic state with its authority.

Overlays need deliberate positioning, dismissal and focus return at supported sizes. Latency, denied actions and recovery receive the same content and material care as the default state. Inspect the departure, intervening presentation and arrival across related views; stable endpoints alone can conceal a shared-shell flash or context loss.

## Choreograph attention across elements

Use **Motion Storytelling** to express a relationship: signals propagate, evidence groups, objects connect or results form. Establish the trigger, first acknowledgment, dependent changes, retained anchor and attention destination. Sequence, stagger and hold elements to make that relationship perceptible; important text needs readable holds.

A professional tool can combine prompt routine feedback with expressive result formation or a branded stage change. Assign these motion roles within one system. Keep selection/actions associated, pending distinct from confirmed, and unrelated input usable. Resume reversible motion from its current presentation where appropriate; duration follows distance, frequency and urgency.

Inspect normal, reversed, interrupted and rapid input, including new results during movement. Resolve competing attention or blocked operation at its cause while retaining the accepted expressive direction.

## Interactive time and authored time

Choose the intended output. A **working product** needs semantic, operable components and truthful feedback under user/service timing. A **product demonstration** selects representative tasks and identifies staged data or timing. An **authored visual work** can use a fixed stage, layers and deterministic timeline; inspect seeking, readable holds, resets, loop joins and final encoded playback. Shared assets do not make their validation interchangeable.

Transfer anticipation and attention order within those boundaries. Sound and haptics supplement semantic/visual feedback under user and platform control. Preserve expressive identity in reduced-motion equivalents.

## Published documents and screen artifacts

Anchors, links, copyable code, disclosures and media alternatives form a document's interaction. Preserve essential text and a clear route to the next action. Inspect promised language/theme variants and graphics at actual display widths. Use the host's supported markup, scroll and focus behavior. A local preview establishes its renderer; final-host readback and visible inspection establish publication conditions.

## Preserve behavior across resource boundaries

Assign focus, selection, scrolling, portals and request state clear owners. Prefer the source's supported configuration/composition; preserve its effective state and motion mechanisms. Trial consequential changes under actual content and adapters. A positioning engine needs the relevant semantic control; animation follows application intent and outcome.

Coordinate listeners, engines and cleanup. Exercise combined controls with keyboard/touch, re-entry, reversal, delayed results, real text, themes, growth and reduced motion. Judge cumulative attention and runtime cost.

## Preserve the primary loop and perceived responsiveness

Identify the continuing operation: conversation preserves its composer; editing preserves the object and selection; task work preserves filters and progress. Supporting evidence or artifacts retain a clear return to that primary work.

Acknowledge input promptly and preserve drafts. Separate feedback, usable result and authoritative completion. Trace input handling, calculation, requests, decoding, state updates and layout/paint to the dependency delaying the next action.

Prepare likely data/assets when use probability, validity and cost justify it. Bound concurrency, prioritize current/next objects and retain capacity for direct input. Deduplicate in-flight work, reuse valid results and defer or discard obsolete work. Compare large eager batches with staged preparation. The [integration reference](integration.md#prepare-data-with-correct-authority-and-lifetime) owns identity, freshness and commitment boundaries.

Keep independently operated objects independent: ready items respond immediately, while unready items provide truthful local feedback. Entry-time preparation does not guarantee readiness. Speculation that consumes quota, reserves inventory or creates a commitment follows the real authority contract.

Where measurement supports it, split expensive work, move suitable computation off the main thread, reduce repeated layout or render fewer active items. Choose media/motion complexity for target devices and sustained use. Compare saved wait with added requests, bytes and processing. [INP guidance](https://web.dev/articles/optimize-inp) explains input, processing and presentation delay; service completion needs its own measure.

Exercise input, submit/cancel/retry, rapid selection, loading and long-content scrolling. Correlate stalls with runtime evidence; synthetic timing retains its fixture scope. Tune resource and motion cost to observed sustained-use needs while preserving accepted expression.

## Inherit behavior at its useful scope

Study a foundation's complete task loop through actual controls, including concealed menus, panels and return paths. For an auxiliary area, observe width allocation, stable task entry, reading measure and focus through opening and closing. Transfer the useful relationship and test it with current content, input, loading and recovery. The current application owns product-specific behavior and outcomes.

## Assets have runtime states

Design loading, ready, unavailable, paused, reduced-motion and renderer-limited conditions. Retain intrinsic space and useful content during arrival. Informative imagery needs an equivalent, functional icons an action name and decoration a suitable accessibility role.

Connect asset state inputs to actual intent/outcomes; manage visibility, interruption, teardown, posters and fallbacks across media/canvas boundaries. Observe late fonts/images and failure paths from initial appearance through the stable result. A failed renderer leaves the primary task accessible.

## Content communicates state and intent

Pair consequential controls with accurate action and outcome language. Distinguish pending, confirmed, denied and failed states; associate errors with fields and expose them through focus and announcements. Preserve drafts through retry, cancellation and locale changes. Localize visible copy, names and state text together, then inspect the changed layout. The [content method](content-design.md) owns writing decisions; this file owns their interaction semantics.
