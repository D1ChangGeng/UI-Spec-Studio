# Fieldnotes settings — delivered

The working settings application is implemented in the supplied `app/` directory. It retains Tabler’s mature settings layout, type, surfaces, fields, switches and theme family. The authoritative `settings-store.js` is byte-for-byte unchanged. Product changes are confined to `index.html` and `settings-controller.js`; no distribution CSS, dependency or original visual design was added. See [SOURCE-ADOPTION.md](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/SOURCE-ADOPTION.md) and the [source-integrity record](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/evidence/final-source-integrity.json).

## Run the product

From `/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/app`:

```bash
python3 -m http.server 4402 --bind 127.0.0.1
```

Use `http://127.0.0.1:4402/?theme=light&lang=en` or `http://127.0.0.1:4402/?theme=dark&lang=zh`. Add `&fail=once` for a failed otherwise-valid save followed by a successful retry. This is an executor-local preview, not a published website. The preview server started for verification has been stopped.

## What changed

Profile fields now have a semantic form, explicit required labels, associated help/error text and localized corrective messages. Validation uses the store’s existing rules, marks the actual fields with Tabler’s native invalid state and immediately reveals the first invalid field.

Save feedback is beside the footer actions. Pending, failed, retry and successful states follow actual store events. The native loading button preserves its accessible label. A failed save preserves both the draft and the previous stored value; Retry save uses the real service again. Cancel restores the latest persisted settings and remains unavailable while an uncancellable save is pending.

The controller distinguishes the submitted snapshot from edits made during the 750 ms delay. A completed snapshot does not overwrite newer inputs or claim they were saved. Language and theme switch in place, including during a pending operation, and preserve values, errors and operation state. Privacy text describes the draft preference while retaining the supplied guarantee that email stays private.

The two fixture buttons use Tabler’s native page-header action composition. The display name spans the existing grid, organization/location retain source grid columns, and the identity marker uses a native avatar size. The original settings navigation remains. Its profile, notification and privacy anchors reveal and focus the intended section. A redundant floating customization trigger was removed after it visibly overlapped the narrow name input.

Keyboard recovery received a specific repair: after pending disable displaces focus, failure or success returns focus to Save only if the user has not moved elsewhere. Keyboard users can retry with Enter immediately; editing another field during pending retains that field’s focus.

## Source and design judgment

The adopted foundation is the supplied Tabler 1.7.1 implementation and MIT license, with its exact tagged source and independently identified deployed HTML snapshot retained. The primary designer personally inspected the supplied original snapshot rendered locally, exact-source alert/validation specimens, the baseline and the integrated product.

Field-local feedback plus a persistent footer alert was selected over a toast because it gives field correction and operation outcome separate, visible homes without adding overlay or dismissal behavior. The default source tint/border was retained, with the source body-text color utility for readable status text. The page, grid, avatar and button changes are configuration/composition within the existing family. Detailed choices and the evidence that changed them are in [DESIGN-DECISIONS.md](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/DESIGN-DECISIONS.md).

## Verification completed

| Check | Actual result and evidence |
| --- | --- |
| Viewport/theme/language matrix | All 12 combinations of 1440×900, 1280×600 and 390×844 × light/dark × English/Chinese exercised. [Results](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/evidence/final-run-02/results.json) |
| Real settings journey | Required/length/email errors, no invalid writes, failed save, retry, newer edits during pending, cancel, reload, theme/language retention and section return passed. No page script errors were recorded in that run. |
| Final visible states | All 12 combinations recaptured through invalid, pending, failed and successful save after removal of the overlapping trigger. [Capture index](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/evidence/final-captures/results.json) |
| Focus recovery | Four fresh compact/narrow conditions passed immediate Enter retry, focus return and no focus theft from newer edits. [Results](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/evidence/focus-recheck/results.json) |
| Existing saved value and pending locale changes | Failure preserved an already persisted value; language and theme changed while the operation was actually pending; retry saved the draft; a 101-character name was rejected without mutation. [Results](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/evidence/persisted-failure/results.json) |
| Final state presentation | Four representative conditions passed immediately visible invalid focus, the native spinner’s child-content contract and Enter retry at the final code hashes. [Results](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/evidence/state-presentation-final/results.json) |

The primary designer opened all twelve final initial viewport images and representative long-content, validation, pending, failure, success and focused-recovery frames. Actual image-tool responses, command stdout/stderr, timestamps and the unsuccessful first narrow run remain under `evidence/`. The first narrow failure was diagnosed as a 21.5 px Save movement during pointerdown/up; that defect was repaired and rechecked. The earlier keyboard test’s broad pass was challenged by its focus log and followed by the focused recovery repair.

Representative output: [desktop settings](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/evidence/final-captures/1440x900-light-en/initial.png), [narrow focused retry](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/evidence/focus-recheck/390-light-en/03-focused-retry.png), and [final narrow validation](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/evidence/state-presentation-final/390-light-zh/invalid-visible-focus.png).

## Remaining limitations

The retained narrow settings navigation occupies substantial vertical space, and long single-line values require caret/horizontal scrolling inside their input at 390 px. The page itself had no horizontal overflow in the exercised matrix. Compact views use ordinary document scrolling; they do not fit the entire form in one viewport.

Verification used the supplied local Chromium environment and provisioned CJK font. No physical-device/virtual-keyboard, screen-reader or cross-browser audit was performed. Temporal evidence consists of controlled real-delay episodes, event logs and personally viewed ordered frames; no natural-time video playback or frame-rate claim is made. The source research’s public screenshot-export limitation is documented separately, with retained local exact-source renders clearly identified.

Gallery destinations and sample gallery chrome remain peripheral source context under the input contract. Authentication and external service work were not added. There is no unresolved blocker in the exercised browser-local settings path, and no owner approval or user-comprehension study is implied.

Full observation notes are in [VISUAL-REVIEW.md](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/VISUAL-REVIEW.md). The single read-only research child’s exact prompt, request/result, report and final-notification exports are linked from [DELEGATION.json](sandbox:/workspace/scratch/708e8b7f118e/ui-study/worksets/w02/DELEGATION.json); model/backend identity, native role bindings, total tokens and billed cost remain unknown where the host did not expose them.
