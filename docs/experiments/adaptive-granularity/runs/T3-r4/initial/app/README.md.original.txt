# Fieldnote

A browser-local research note with an editable face and a saved face on one anchored card.

## Run

From this cell:

```bash
python -m http.server 8314 --directory app
```

Open http://localhost:8314. No build or external runtime dependencies are required.

## Use

Write up to 600 characters, then choose **Save note** (or Ctrl/⌘ + Enter). The pending state includes the existing 900 ms demo delay. The card turns only after localStorage accepts the write. **Return to editing** restores your selection and editor scroll position. The outside turn control supports reversal during motion.

You can keep editing during saving. The submitted snapshot is saved; any newer text stays a draft on the front. Unsaved drafts are retained while navigating but are not persisted across reloads. Read saved note always shows the confirmed record, an empty state, or an unreadable-state explanation.

Theme and English/Chinese controls preserve current text. Reduced-motion preference replaces 3D movement with a brief opacity change. Demo settings can clear the local record. A write, read, or clear failure keeps the relevant content and exposes retry.

## Boundaries and source

The Storage key remains `ui-spec-temporal-note-v1`, and the previous data shape is supported. Saving is local to the current browser origin; there is no cloud sync or autosave. Theme and language choices are session-only. Clearing demo data intentionally clears the current draft as well as the saved record.

The scene/object/faces pattern is adapted from David DeSandro’s [Card Flip](https://3dtransforms.desandro.com/card-flip), whose example code is MIT-licensed. The original application already used this technique; the current implementation refines it and binds it to confirmed persistence. Composition, materials, task state and focus adapters are project-owned. See `THIRD_PARTY.md` for source/terms.

## Verification

`../evidence/review_app_run2.py` exercises the HTTP app using Playwright. It records assertions, timestamped screenshot capture brackets, hashes, and a video. Separate follow-up tests verify final repairs and remaining high-risk states. The delivery and design records distinguish automated checks, viewed images, and unverified playback/device conditions. The original failed run is preserved.
