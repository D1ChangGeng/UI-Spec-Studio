# Fieldnote — a continuous note card

Use the supplied ui-spec Skill to refine the existing application in app/.
Keep its browser-local save, retry, draft, language and theme behavior. The front
and back should feel like the same physical object changing its orientation:
stable place and weight, convincing surfaces, readable content and a coherent
return to editing. Improve its type, spacing, material and continuous motion in
the actual composition, while retaining the note-writing task.

The result should remain usable with a long note, repeated quick flip/reverse
actions, delayed saving, a real local-storage write failure and retry. A failed
save must retain the draft and communicate the actual outcome. Preserve focus
and meaning in reduced motion and in both themes. Work at 1440×900 and 390×844.
Use appropriate mature work where it improves this product; the existing source
is a starting point and can be adapted. Keep the interface's language centered on
writing and using notes. Do the implementation and inspect the real result.

Use Chinese for your outward explanation. Keep evidence and source notes in this
workspace as useful for continuation. State the actual result and limitations.

## Confirmed review finding to resolve in the same SPEC

Independent operation found that immediately after flipping (about 45ms), the actual card still faced front (matrix m33 approximately 0.999882) but the back was already aria-hidden=false and inert=false. Shift+Tab from the flip control could move focus into the not-yet-visible preview-note. Correct the relationship between actual visible orientation, keyboard focus and semantic exposure, including rapid reversal and reduced motion. Keep the established material, content, save/retry and draft contracts. Inspect actual intermediate states, not only data-face target or settled endpoints. This is a targeted continuation after the original comparative endpoint was frozen; it is not a replacement comparative run.
