# Leafnote

Serve this folder over HTTP, then open it in a browser:

```bash
python -m http.server 8844 --directory app
```

Open http://localhost:8844. A fresh browser starts with an empty notebook; **Explore example notes** adds four clearly identified synthetic notes. Create a note, edit its title and context, and choose **Save note**. Search matches both title and body. Select a result to return to editing.

## Keyboard

- Tab / Shift+Tab moves through native controls.
- Ctrl+S / Command+S saves.
- `/` focuses search when outside an input.
- `N` creates a note when outside an input.
- Escape cancels the deletion dialog. Cancellation has initial focus.

## Persistence and recovery

`leafnote-notebook-v2` contains saved notes and separate recoverable drafts. Typing keeps a draft locally; Save promotes it to a saved note. Failures keep text in memory and provide retry/export. Navigation and reload recover persisted drafts. An unavailable draft write enables the browser's leave-page warning.

The earlier `ui-spec-content-note-v1` note is imported when no v2 notebook exists. Its original key is never modified or removed, including when the imported note is later deleted. Invalid stored data is preserved and blocks writes; Export includes raw stored data and the in-memory draft for manual recovery. A concurrent external-tab change blocks writing rather than silently overwriting it.

Export creates a JSON backup. A backup importer is not implemented. Preferences use `leafnote-preferences`. No backend or synchronization exists; clearing browser storage removes local data. Keep an exported copy for durability.

## Foundation and evidence

Bootstrap 5.3.8 CSS is vendored with its MIT notice. Custom CSS configures the list, forms and buttons into an editorial two-pane notebook. The selected-item/list relationship also references the shadcn v3 Mail example; no shadcn source is imported. See ../DESIGN.md for adoption decisions and ../evidence for tests and captures.

## Display density

The shared header offers Comfortable and Compact density. This changes collection spacing, editor typography and section rhythm without changing the selected note or its draft. Density is stored with language/theme in leafnote-preferences and restored on reload. Continuation evidence and its limits are in ../evidence/continuation/REVIEW.md.
