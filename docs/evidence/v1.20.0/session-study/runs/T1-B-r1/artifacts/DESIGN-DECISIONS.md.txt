# Fieldnotes settings — current design model

## Formal increment S1: coherent settings and truthful saving

The complete goal is a bilingual, theme-consistent profile, notification, and visibility journey on the supplied Tabler settings page. One increment owns editing, field validation, pending submission, one failed save, retry, cancel, reload, and return. The mature page already supplies the necessary shell and component family; splitting these tightly related states would dilute the continuity check.

Research observes the inherited page and Tabler form/alert examples. Implementation is restricted to the existing settings region and its controller, preserving the authoritative store. Regression covers the surrounding source shell, all requested size/theme/language combinations, focus and scrolling. Gallery routes remain outside the product contract.

## Working evidence and decisions

| Decision | Purpose and evidence | Current choice / next check |
| --- | --- | --- |
| D1 — retain Tabler | INPUT identifies the original settings snapshot and exact 1.7.1 tag. SettingsLayout.astro and settings.astro supply column proportions, card body/footer, headings, form controls and switches. | Preserve this source family, its tokens and distribution files. Judge baseline and final pixels before claiming retained quality. |
| D2 — field and save feedback | Source controller only writes a global line. The store emits authoritative fieldErrors and separate pending/success/error facts. | Use the existing form-control is-invalid / invalid-feedback family and an operation alert near the footer. Focus the first failed field; keep recovery beside Save. Source/demo review pending. |
| D3 — draft continuity | Source controller reloads the page on language change; a pending save captures a snapshot while fields remain editable. | Translate in place, preserve current field values, and distinguish a completed submitted snapshot from later unsaved edits. Never alter the store contract. |
| D4 — content and compact views | Profile identity and fixture controls share the original avatar row; existing three-column fields hide much of long synthetic names. | Use Tabler grid sizing and native wrapping within the existing region. Verify source-supported adaptation with long English/Chinese values and compact scrolling. |

The supplied ui-spec common references, integration reference, evidence map and action rules have been read. Current forms guidance was retrieved through the prescribed modern-web-guidance search/retrieve commands; original exports are under evidence/commands/001-web-search and 002-web-forms. Native field labels, descriptions, submit semantics and live feedback apply. Browser-local persistence remains the authoritative boundary; no server fallback is implied.

No original visual construction is authorized or used. No owner acceptance of the new result is claimed.

## Current decisions after inspected trials

**D1 retained.** The primary designer opened the supplied original settings snapshot rendered locally, the exact-source alert/validation specimen in light and dark, the three baseline product views, and the integrated product. The quarter-width settings navigation, three-quarter content, card boundary, section type, native fields, switches and terminal actions remain recognizable. Source identity and actual adoption are in SOURCE-ADOPTION.md. There is no new stylesheet or distribution-file edit.

**D2 adopted.** Field-local invalid-feedback plus a default inline alert in the footer is the selected composition. The source specimen showed that minor alerts are quieter; the default tint and border give a failed save a distinct place adjacent to Retry without an overlay or dismissal requirement. An important filled alert would give a routine local save too much weight. A toast adds placement and dismissal responsibility and cannot identify the invalid field. The text-body utility keeps message text in the mature body-color role while source status colors remain in the tint and border. This is documented configuration, not new color construction. A sampled informational message measured 9.59:1 in light and 10.85:1 in dark; this does not establish whole-page accessibility compliance.

**D3 adopted and connected.** The unchanged store still validates and saves its 750 ms captured snapshot. The adapter compares the current draft with that snapshot and with returned saved settings. Newer edits stay editable and receive a distinct unsaved message. Language and theme now change in place and update URL parameters; neither replaces the draft. Cancel restores the latest persisted settings and is unavailable during an uncancellable save. Error text remains private-email consistent in both languages.

**D4 adopted with limits.** The native page-header action slot now contains fixture buttons; native avatar-lg supplies the smaller identity marker. The name field spans the existing grid, with organization/location in a 7/5 split and the same narrow stacking. The native single-line input keeps long text editable; at 390 px its complete value still requires caret/horizontal scrolling. The inherited settings navigation remains stacked on narrow screens, so the initial form begins below much of the first viewport. Its working section anchors and ordinary document scroll preserve access; a new mobile navigation design is outside the authorized increment.

## Observations that changed the implementation

1. **Baseline compact feedback was remote from Save.** The research child measured top status positions of −224 px for invalid and −155 px for a failed save after the user reached the footer. Primary inspection corroborated the disconnected location. The adopted footer alert resolves that spatial association.
2. **A real narrow click failed in the first integrated run.** `evidence/narrow-diagnosis/results.json` records Save moving from y=599 to y=620.5 between pointerdown and pointerup when blur inserted the location error. The click landed outside the button. The adapter now defers that blur check when focus goes to a button; submit immediately performs authoritative validation. `006-product-recheck` passes all twelve conditions after the correction. The failed run is retained.
3. **The inherited floating customization trigger overlapped the narrow name field.** Its redundant trigger was removed; the source theme panel and header theme control remain. `007-final-captures` recaptures all twelve conditions and shows no floating control covering the form.
4. **Native pending disable displaced keyboard focus.** The first keyboard run could eventually reach Retry but required a long tab cycle. The primary designer identified this quality defect from its real focus log, despite the earlier test's broad pass label. The adapter now restores Save focus after resolution only if focus is still on the body; a user who moved to a newer edit retains that field focus. `008-focus-recheck` verifies immediate Enter retry, successful focus return and no focus theft in four compact/narrow theme-language conditions. Actual reviewed focus-ring captures are retained.

## Verification and remaining evidence boundary

`evidence/final-run-02/results.json` covers twelve combinations: all requested viewports × both themes × both languages. It executes required and length errors, no invalid persistence, failure, retry, submitted-snapshot/newer-draft distinction, language/theme retention, cancel, reload and section return. `evidence/final-captures/results.json` repeats visible invalid/pending/error/success at the final markup revision. The final focus-only adapter repair changes no resting composition; those captures carry forward for appearance, and `evidence/focus-recheck/results.json` owns the changed focus behavior at the final code hashes.

The primary designer personally opened all twelve final initial viewport captures and representative long, validation, failure, pending, success and keyboard-recovery frames. VISUAL-REVIEW.md gives the observation boundary. Original command output, failed attempts, captured images, actual image-tool responses and code hashes remain available. No natural-time video playback, physical-device/virtual-keyboard test, screen-reader session or cross-browser audit is claimed. The delivered product is a working browser-local application; the fail-once event is an explicit local fixture.

### Final presentation repairs and boundary checks

Fresh source inspection showed `.btn-loading > * { opacity: 0 }`; the adapter now places the accessible button label in a child span so it does not fade underneath the source spinner. Invalid submission focuses and immediately scrolls the first invalid field into view. `010-state-presentation` passes four representative desktop/narrow conditions, with the final source hashes and personally viewed changed-state captures. Resting composition captures carry forward because these repairs do not change that composition.

`009-persisted-failure` verifies that failure preserves an already persisted value, the draft survives, language and theme are both switched while the operation is actually pending, retry persists the draft, and a 101-character display name is rejected without changing saved data.
