# Interaction, accessibility, language and themes

Apply these requirements to the interaction and variants the product actually supports. Include their important consequences while planning a screen, then verify them in the resulting interface.

## Contents

- [Controls, objects and choices](#control-semantics-and-focus)
- [Language and themes](#language-and-content)
- [Motion and dynamic space](#motion)
- [Scrolling and content growth](#scrolling-and-content-growth)
- [State and task continuity](#continuity-is-a-user-visible-contract)
- [Resource boundaries](#preserve-behavior-across-resource-boundaries)
- [Responsiveness and preparation](#preserve-the-primary-loop-and-perceived-responsiveness)
- [Asset and content states](#assets-have-runtime-states)

## Control semantics and focus

Use native elements or appropriate accessible primitives. Every icon-only action has an accessible name and a usable target. Hover hints supplement discoverability; they do not replace names or touch behavior. Menus, dialogs, tabs, comboboxes and tooltips follow the relevant interaction pattern, including focus entry, movement, dismissal and return.

Complete key paths with keyboard and pointer/touch. Check visible focus, loading/disabled semantics, error association and announcements for meaningful asynchronous changes. Color is one cue among multiple cues for status. Meet the project's target accessibility standard; record what automated and manual checks actually covered.

Reference patterns: https://www.w3.org/WAI/ARIA/apg/
WCAG 2.2: https://www.w3.org/TR/WCAG22/

## Objects, choices and action relationships

Choose the interaction carrier from the object people recognize and the work they do with it: a record, product, file, conversation or media item may suit a card, row, table, message or editor. Keep its identity and selection clear while details, status and available actions change. When the object itself opens or transforms, make its affordance and result legible; keep independent actions separately operable and avoid nested interactive targets.

Derive controls from actual decisions. Offer a selector for meaningful alternatives, show an already determined value clearly, and preserve a way to revise it when the journey allows that choice. A single valid option may need confirmation or explanation, without needing a multi-option control. Identify whether actions are primary/secondary, peers, successive steps or consequential commitments before assigning visual weight and position. Two equally prominent buttons are appropriate only when the task supports their equal standing.

Judge component material and state together. Inspect resting, hovered, focused, expanded, selected, pending, disabled and invalid states where supported. Text, icons, borders, translucency and elevation must keep their meaning against the actual background. A glass surface or decorative layer still needs readable contrast, clear selection and visible keyboard focus. Keep the state language coherent across the component family.

## Language and content

Localize the declared supported languages, including menus, dialogs, form errors, empty states and dynamic content that the product owns. Preserve fixed identifiers, brand names and user-authored content as appropriate. Keep natural phrasing and consistent terminology rather than translating layout labels independently.

Decide locale initialization, explicit preference priority and persistence. Preserve current task state during switching. Format dates, times, numbers and units according to the product contract; changing language does not automatically change stored values or contractual currency.

Test long labels, fallback fonts, glyph coverage, mixed scripts, right-to-left behavior when supported, and content from real service responses. Define an intentional fallback and make missing translations discoverable in development.

## Themes and perception

Map surfaces, text, borders, focus, states, elevation and visual effects to semantic theme roles. Review each supported theme independently. Brightness and background contrast change perceived weight, so recheck composition as well as color values.

Define preference initialization, system preference where supported and explicit user overrides. Initialize the intended theme before the first meaningful paint using the project's supported rendering mechanism. Keep forms, menus, scrollbars, charts, effects and icons consistent across theme changes. Preserve task state.

Theme controls communicate the action or current state consistently through visual and accessible labeling. Locale, theme, identity and navigation utilities have a stable grouped order in each responsive layout.

## Motion

Define which events animate: first entrance, navigation, local state update, direct manipulation or status feedback. Choose timing and easing by purpose and frequency, and preserve rapid reversal/interruption where interaction requires it.

Check reduced-motion preferences and provide a quiet equivalent that preserves meaning and access. Pause or simplify long-running decorative motion when appropriate. Match touch and keyboard expectations; optional pointer effects should not carry essential information.

Preserve the same object's identity through expansion, reversal, replacement and return. For a flip, align both faces and the pivot, coordinate which face is visible and interactive, and test both directions from interrupted states. Coordinate animation with data readiness: movement can acknowledge intent while a truthful pending state carries an unresolved result. A completed animation alone does not establish a completed business action.

Compose the full motion envelope: rotation, scaling, particles, shadows and drifting elements occupy space beyond a resting box. Check their closest approach to text and controls across the cycle and at supported viewports. Adjust amplitude, layer order, masks, layout or delivery mode according to the intended effect. Clipping is deliberate composition only when it preserves important content, recognizable motion and operable controls.

## Resilience

Review short heights, text zoom, browser zoom, mobile virtual keyboard, safe areas, slow assets, offline/error states and repeated actions where applicable. Reflow should preserve information and function. A two-dimensional table or editor may need scoped horizontal scrolling, while the surrounding page remains usable.

Initial evidence can use deterministic fixtures. Complete integration evidence should include actual service responses, authorization outcomes and persistence appropriate to the scope.

## Scrolling and content growth

Choose document, local-region or multiple-region scrolling from page responsibility and expected growth. Reading benefits from a continuous document; a workspace may retain navigation and scroll its active content. Give each independent region a clear task and boundary. Check wheel, touch and keyboard traversal, focus reveal, sticky controls and overlay behavior, including short heights and an open virtual keyboard.

Preserve the reader's location when content arrives, expands or changes. Define when a new result should be brought into view, when an existing reading position should remain, and what returning to an object restores. In a live feed, following new content and reading older material are different user intentions. Retain stable object anchors when pagination or virtualization replaces DOM nodes; verify search, focus and assistive use under the chosen approach.

Coordinate scrollbar color, visibility and width with themes and platform behavior. Reserve space where a classic scrollbar would otherwise shift the composition; [scrollbar-gutter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scrollbar-gutter) is one available mechanism, with different effects for classic and overlay scrollbars. Maintain discoverability and comfortable operation. Test the actual scrolling region rather than inferring its hidden content from a full-page screenshot.

## Continuity is a user-visible contract

Separate first entry, navigation, local content changes and asynchronous feedback. Keep shared controls mounted and retain meaningful input, focus, selection and scroll context. Transition the part whose meaning changed. For rapid successive requests, ensure the displayed result belongs to the latest valid intent and reconcile optimistic state with the authoritative outcome.

Dropdowns and overlays need deliberate positioning, dismissal and focus return at each supported viewport. Icon order follows functional grouping and frequent use; visible icon size and the interaction target can differ. Keep theme, locale, identity and navigation controls visually coherent where those controls exist.

Treat latency, denied actions and error recovery as ordinary product states. Their message, focus behavior and layout carry the same quality requirements as the default state. Real integration confirms that the states correspond to actual outcomes.

## Choreograph attention across elements

Treat motion as a relationship in time, not a collection of entrances. Identify what initiates the change, which element provides immediate feedback, which information changes, which anchor stays still and where attention should settle. Choose emphasis and overlap according to that sequence. Allow meaningful content enough stable time to be understood.

For an option change, acknowledge selection promptly and update the affected values while preserving the selector and primary action's relationship. For a delayed service result, distinguish pending intent from confirmed outcome. Reversible operations can transition from their current visual state; unrelated input and focus stay available. Duration follows distance, interaction frequency and task urgency rather than a single global number.

Use continuity of objects and shared spatial references to explain navigation or expansion. Reserve prominent motion for a meaningful event and keep repeated tasks efficient. Coordinate concurrent animations so they do not compete for attention or imply a false order of events. Test rapid reversal, new input during transition, delayed response, interruption and recovery.

## Interactive time and authored time

In a UI, the user, device and service control when events happen. In a video or timed presentation, the author controls the sequence. Transfer ideas such as anticipation, attention order and breathing space with that difference intact. A film's mandatory camera moves, beat grid, soundtrack or fixed holds are not general interaction rules.

For an authored sequence, use explicit timing, readable holds, seekable states and final-output playback. For an interactive sequence, ensure feedback remains correct with uncertain latency and changing intent. Preserve a reduced-motion version with equivalent meaning. Sound or haptics, where the medium supports them, supplement visual/semantic feedback and follow the user's control and platform conventions.

## Published documents and screen artifacts

A reading surface can have interaction through anchors, links, code copying, expandable detail and media alternatives. Use these affordances intentionally. Give the reader a clear route from orientation to a next action; preserve essential content as text instead of hiding it in artwork. Test language and theme variants where promised. Static SVG or images should carry meaning at their actual display width and have a suitable text equivalent.

Avoid imposing an app's scrolling or focus model on a document. Verify the host's supported markup and its rendered output. A local preview validates its stated renderer; the final publishing environment needs its own readback and, when available, direct visual inspection.

## Preserve behavior across resource boundaries

When composing sourced parts, give focus, selection, scrolling, portals and request state clear owners. Preserve the primitive's semantic contract while adapting appearance. Verify touch, keyboard, dismissal, re-entry, rapid reversal and delayed results with the combined implementation. A positioning engine may need a separate semantic control; an animation layer follows confirmed or pending state supplied by the application.

Coordinate listener scope, shared motion engines and teardown. Keep one meaningful feedback sequence for the user's action, with a readable quiet equivalent. Check actual localization, reduced motion, content growth and theme combinations after integration, because their behavior depends on the assembled product.

## Preserve the primary loop and perceived responsiveness

Define the continuing operation for the selected model: a composer follows the conversation, object editing retains the active object and selection, and task work retains filters and status context. For hybrid surfaces, opening supporting evidence or an artifact preserves the primary task and provides a clear return.

Acknowledge input promptly, preserve drafts across interruption, and separate immediate feedback from a usable result and authoritative completion. Trace the task through input handling, calculation, network, asset decoding, state updates, layout/paint and final feedback. Identify which dependency delays the user's next meaningful action before choosing an optimization.

Prepare predictable data or assets at a useful entry point when their probability of use, validity and cost justify it. Parallelize independent preparation within a concurrency and resource budget; prioritize visible or likely next objects and retain capacity for direct input. Reuse in-flight work and valid results, defer low-value material, and stop or ignore obsolete work. A large eager batch can delay the first interaction and consume unused resources, so compare it with staged preparation. The [integration reference](integration.md#prepare-data-with-correct-authority-and-lifetime) owns freshness, identity and commitment boundaries.

For a collection people open rapidly, prepare likely results as the page becomes useful, keep each object's state independent and let ready objects respond immediately. Give unready objects an understandable local state while other work continues. Page entry alone cannot guarantee every result is ready; choose preparation and fallback behavior from observed latency and the business contract. Speculation that consumes a quota, reserves inventory or creates a commitment needs that operation's actual authority.

Keep event work small enough for feedback to render; where measurements justify it, split costly work, move suitable computation off the main thread, reduce repeated layout or render fewer active items. Select animation and media complexity for target devices and sustained use. Measure both the saved wait and any extra requests, bytes or processing introduced. [INP guidance](https://web.dev/articles/optimize-inp) explains input, processing and presentation delays; an end-to-end service result needs its own measurement.

Verify input echo, submit/cancel/retry, rapid selection, loading and long-content scrolling under representative conditions. Synthetic timing supplies a regression signal for the fixture; real-device and service performance have their own evidence. Keep the measured boundary and environment explicit.

Animate a state change according to meaning and frequency. Coordinate cleanup, reduced motion and focus when combining resources. Decorative motion can remain quiet when sustained reading or repeated operation benefits more from stability.

## Inherit behavior at its useful scope

Study the foundation's complete task loop, not only its resting appearance. Preserve useful focus, input, scroll, loading, interruption and recovery decisions as a coordinated system. Directly adopt proven behavior when compatible; test the equivalent contract when porting. Product-specific authority and real service results remain owned by the current application.

## Assets have runtime states

Treat loading, ready, unavailable, paused, reduced-motion and renderer-limited conditions as designed states. Preserve intrinsic space and useful content while material becomes available. Give informative imagery an appropriate equivalent, functional icons an action name, and supporting decoration a quiet accessibility role.

Asset state-machine inputs and events follow real application intent and outcomes. Manage visibility, interruption, cleanup, posters and fallbacks across media and canvas boundaries. Verify actual decoder/renderer and theme behavior. A font or image arriving late should retain usable reading and controls; a failed 3D or animation load should leave the primary task accessible.

## Content communicates state and intent

Pair every consequential action with words that describe what the control really does and what the user should expect. Keep pending, confirmed, denied and failed outcomes distinguishable. Input errors identify the affected field and available correction; focus and announcements expose the message to people using assistive technologies. Keep drafts and user state during retry, cancellation and locale switching. Localize meaning, accessible labels and state text together with the visible interface; recheck layout after real translations change length and line breaking. The [content reference](content-design.md) owns detailed writing decisions, while this file owns their interaction semantics.
