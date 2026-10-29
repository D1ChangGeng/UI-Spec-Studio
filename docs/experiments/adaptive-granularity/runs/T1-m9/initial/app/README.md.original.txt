# Leafnote

A bilingual, browser-local research notebook. Create, search, reopen, edit, save and delete notes. Working drafts are kept separately from explicitly saved notes. No backend, cloud synchronization or account is present.

## Run locally

From this cell:

```bash
python -m http.server 8619 --bind 127.0.0.1 --directory app
```

Open http://127.0.0.1:8619/ in a browser. Keep the same origin and browser profile to return to the same notebook. Fonts and styles are bundled, so no remote dependency is loaded by the application.

## Use

- New note creates a draft. Add a title and optional context, then Save note.
- Search matches the title and body, including local drafts.
- Select a note to reopen it. On a phone, All notes returns to the same collection/search.
- Ctrl/Cmd+S saves; Ctrl/Cmd+K focuses search; Ctrl/Cmd+Shift+N creates a note.
- Chinese/English and light/dark controls preserve the current input and persist preferences.
- Export notebook downloads the saved collection and local drafts as JSON. Import is not implemented.
- Delete identifies the note and requires confirmation. Keep note and Escape cancel.

Fresh storage begins with five clearly labeled fictional examples. Existing v1 content is migrated before examples are considered, and the original record remains untouched.

## Persistence

`leafnote-notebook-v2` owns saved notes and deleted-note IDs. `leafnote-drafts-v2` owns working copies. `leafnote-preferences` owns language and theme. `ui-spec-content-note-v1` is read only as a migration source, then retained. Invalid or unreadable data blocks destructive writes and offers retry plus a raw recovery download. Draft write failures retain input in memory and warn before leaving.

A saved collection changed by another tab requires reading the latest version before saving; current local drafts are kept. Simultaneous editing of drafts in multiple tabs is not a collaboration feature. Use one editing tab for reliable draft persistence.

## Source and review

Bootstrap 5.3.8 supplies the locally bundled list/control foundation. Inter Variable is bundled from its official repository. Their licenses are in `vendor/`. The original app-specific state code and CSS own the notebook behavior, editorial layout and responsive adaptation. See `../DESIGN.md` for the observed reference comparison and design decisions.

Reproduce the browser checks in the supplied environment with:

```bash
FONTCONFIG_FILE=/workspace/scratch/43b440780c87/preview-fontconfig.xml /workspace/scratch/43b440780c87/test-env/bin/python evidence/test_app.py
FONTCONFIG_FILE=/workspace/scratch/43b440780c87/preview-fontconfig.xml /workspace/scratch/43b440780c87/test-env/bin/python evidence/check_recovery.py
```

Run these from the cell with the local HTTP server active. Tests use synthetic content and their own browser contexts. `../evidence/` preserves factual logs, reference failures, capture history and final screenshots. Browser assertions, visual observation and end-user acceptance are separate facts.
