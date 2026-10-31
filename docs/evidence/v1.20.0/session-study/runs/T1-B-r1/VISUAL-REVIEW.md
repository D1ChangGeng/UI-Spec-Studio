# Primary designer visual review

## Actual viewing conditions

The primary product agent personally opened real PNGs through view_image, retaining each complete tool response at call time in evidence/inspect-*.json, view-*.json and parent-view-*.json. Browser: supplied Chrome headless shell 143.0.7499.4; Playwright 1.57.0; device pixel ratio 1; FONTCONFIG_FILE=/tmp/ui-spec-fonts/fonts.conf with the provisioned Noto CJK font. No generated mockup is used as evidence.

All **twelve final primary states** were personally viewed: 1440×900, 1280×600 and 390×844 × light/dark × English/Simplified Chinese. Files are `evidence/final-captures/<size>-<theme>-<locale>/initial.png`. Subsequent adapter changes only repair focus restoration, immediate invalid-field reveal and loading-button child composition. Resting layout and content did not change; the initial observations carry forward on that limited basis. Changed states have fresh final-code captures in evidence/state-presentation-final/.

Other personally viewed evidence:

- Baseline product at 1440 light English, 1280 dark Chinese and 390 light English.
- Supplied original settings snapshot rendered locally and exact tagged alert/validation specimens in 1440 light and 1280 dark. The specimen is a labeled research composition; it is not a public demo screenshot. The child's failed cloud screenshot-export route is recorded in its report.
- First integrated desktop, dark Chinese validation, compact failure and saved-snapshot/newer-draft views.
- Final compact failure in all four theme-language combinations; light English/dark Chinese pending; light Chinese success; dark English invalid.
- Final narrow long content, compact and narrow focused retry, and narrow focused success.
- Fresh final spinner captures at 1440 light English and 1280 dark Chinese, plus immediately revealed invalid-field views at 390 light Chinese and dark English.

Files without a matching primary view export are capture evidence only. The child's viewed files retain its separate observer identity.

## Composition and retained craft

The unified settings card, quarter-width navigation, content column, typography, native input/switch family and terminal actions remain recognizable from the original. The fixture controls now occupy the source page-header action slot. Native avatar-lg and the adjacent Profile Details heading make one identity region. No replacement theme, custom stylesheet or decorative asset was introduced.

The full-row display name accommodates the specified long bilingual string better on desktop than the original third-width input. Organization/location remain aligned below. Labels, headings and supporting information remain distinct in both languages; actual Chinese glyphs and mixed Latin values render without missing-glyph squares.

Light and dark preserve the source's page/card/input separation. Footer alerts retain source state tint and border while using body-color text. A sampled informational message measured 9.59:1 foreground/background contrast in light and 10.85:1 in dark (evidence/focus-recheck/contrast-calculation.json). This is a scoped measurement, not a full accessibility audit.

## Compact height and narrow use

The 1280×600 page requires ordinary document scrolling. Lower fields and actions remain reachable; status is now beside Save instead of above the viewport. No nested scrolling region was added.

At 390 px, the original stacked settings navigation consumes much of the first viewport. The English title wraps to two lines alongside the fixture buttons; Chinese remains one line. Neither overlaps its actions. Working settings anchors reveal profile, notifications and privacy. The navigation's vertical cost is retained under the scope constraint; a new mobile navigation is not claimed.

The first narrow review showed the inherited floating customization button covering the name input. Its redundant trigger was removed. Final narrow captures show that input unobstructed. Long actual values remain editable; a native single-line input cannot show the entire long string simultaneously at 390 px and still needs caret/horizontal input scrolling. The page itself does not horizontally overflow in the exercised conditions.

## Validation and operation states

Field-local errors combine Tabler's border/symbol and corrective text with programmatic association. The final invalid field is immediately centered in view with its corrective message, avoiding a mid-scroll interval in which focus had moved but the field was not yet visible.

The first integrated narrow test found a real click cancellation. In evidence/narrow-diagnosis/results.json, blur inserted an error and moved Save from y=599 to y=620.5 between pointerdown/up. Deferring that blur check when focus goes to a button keeps the target stationary; submit immediately performs the same authoritative validation. The twelve-condition recheck passed.

An early pending integration let direct button text fade under the spinner. The final child-span composition follows the exact `.btn-loading > *` source contract. Fresh captures show only the source spinner, while the accessible label stays available. The adjacent status names the submitted changes.

Failure text explains retained draft and Retry save. Success distinguishes the saved snapshot from newer unsaved edits. Tests check current inputs and actual browser storage separately. The fail-once event is an explicit local fixture, not a remote outage claim.

## Keyboard continuity and corrected quality

The keyboard route starts at the native skip link and reaches fixture controls, existing settings navigation, fields, switches and actions. Viewed retry frames show the native focus ring.

The earlier keyboard test's broad pass was insufficient: pending disable displaced focus and the test eventually tabbed around the page to reach Save. The primary designer identified this from the real focus log and repaired it. The final adapter restores Save focus after completion only if focus remains on the body; a user editing another field keeps that field's focus. Four fresh conditions verify immediate Enter retry and no focus theft. Final state-presentation checks also verify immediately visible invalid focus and the source loading composition.

## Temporal and evidence limits

Controlled browser episodes use the real store delay. Screenshot-time brackets and event logs establish sampled pre/pending/result states, persistence and focus. Editing, validation, failure, retry, newer edits, cancel, reload, locale/theme switching and section return were exercised.

No natural-time video playback was personally viewed. Spinner smoothness, intermediate scroll cadence and device-wide frame rate remain unverified. Later keyboard captures waited for inherited scrolling to settle; validation now reveals its target immediately. No physical-device/virtual-keyboard, screen-reader or non-Chromium test was performed. No user comprehension or owner acceptance is claimed.

The requested browser-local increment is implemented and visually coherent within the supplied mature source. Observed click, overlay, focus and loading-composition defects were repaired and rechecked. Remaining limits are the retained narrow navigation's vertical cost, native long-input scrolling and the test/viewing boundaries above. Gallery routes, sample gallery chrome, authentication and external services remain outside the product contract.
