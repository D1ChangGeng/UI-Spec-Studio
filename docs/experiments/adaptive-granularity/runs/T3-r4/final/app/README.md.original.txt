# Fieldnote

A browser-local notebook with several research cards. Each note has an editable front and a confirmed saved back.

## Run

From this cell:

```bash
python -m http.server 8314 --directory app
```

Open http://localhost:8314. No build or external runtime dependency is required.

## Use

Choose **New note**, enter a title (up to 120 characters) and body (up to 600), then **Save note** or Ctrl/⌘ + Enter. The existing 900 ms demonstration delay remains. Only successful Storage writes turn the card to its saved face. You can continue editing during saving; the submitted snapshot is saved and newer edits remain a draft.

**Notebook** returns to the collection, retaining each draft and restoring the corresponding tile, focus and page scroll. Open another card to edit it. Stable numbering and the selected border preserve orientation. Both faces are prepared before the editor appears. Pending saves belong to their original note even when you switch.

Failures preserve the collection and drafts. Failed drafts are labeled in the collection and can be opened for retry. Unreadable storage is distinguished from an empty collection and blocks writes until recovery. Demo settings offer confirmed clear-all with retry if removal fails.

## Storage and boundaries

Confirmed notes use `fieldnote-collection-v2`. The legacy `ui-spec-temporal-note-v1` note is read when no collection exists and carried into the first successful collection save. Unsaved drafts, selection and scroll are session memory only; reload discards those drafts. Theme and language are session-only. There is no cloud sync, conflict-resolution interface, search, manual sorting, or per-note deletion in this increment.

Light/dark and English/Chinese retain note content. Reduced motion uses opacity in place of rotation. Attribution is in THIRD_PARTY.md. Continuation test scripts, capture brackets, source hashes and screenshots are in ../evidence/continuation/. Prior evidence and DELIVERY.md are retained.
