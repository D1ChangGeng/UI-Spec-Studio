# Interaction, accessibility, language and themes

Apply these requirements to the interaction and variants the product actually supports. Include their important consequences while planning a screen, then verify them in the resulting interface.

## Control semantics and focus

Use native elements or appropriate accessible primitives. Every icon-only action has an accessible name and a usable target. Hover hints supplement discoverability; they do not replace names or touch behavior. Menus, dialogs, tabs, comboboxes and tooltips follow the relevant interaction pattern, including focus entry, movement, dismissal and return.

Complete key paths with keyboard and pointer/touch. Check visible focus, loading/disabled semantics, error association and announcements for meaningful asynchronous changes. Color is one cue among multiple cues for status. Meet the project's target accessibility standard; record what automated and manual checks actually covered.

Reference patterns: https://www.w3.org/WAI/ARIA/apg/
WCAG 2.2: https://www.w3.org/TR/WCAG22/

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

## Resilience

Review short heights, text zoom, browser zoom, mobile virtual keyboard, safe areas, slow assets, offline/error states and repeated actions where applicable. Reflow should preserve information and function. A two-dimensional table or editor may need scoped horizontal scrolling, while the surrounding page remains usable.

Initial evidence can use deterministic fixtures. Complete integration evidence should include actual service responses, authorization outcomes and persistence appropriate to the scope.

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
