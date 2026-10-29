# Fieldnote

A browser-local collection of research notes. Create a note, edit its front face, save, and read the stored version on its back. Return to All notes to continue with another card.

## Run locally

From this cell:

```sh
python -m http.server 8737 --bind 127.0.0.1 --directory app
```

Open http://127.0.0.1:8737 . No remote service, account or cloud sync is used.

## Collection behavior

Each note has a stable ID and number, its own in-tab draft, selection, scroll and pending save. Collection cards show stored content until a successful write; unsaved and failed drafts have explicit badges and remain reopenable. Drafts do not survive reload. Saved notes do.

The selected editor and saved face are populated before opening. Native same-document View Transitions connect the collection card and detail surface where supported. Reduced motion and unsupported browsers update immediately. Returning restores collection scroll and focus to the same card. Rapid navigation skips the obsolete transition and applies the latest request.

The existing centered front/back flip still follows confirmed localStorage writes. A 650 ms demonstration delay makes pending states observable; editing during a save retains newer draft content. Pending writes belong to their note even after switching to another card. Failed writes keep the prior saved collection and all in-tab drafts.

The 600-character save bound is unchanged. Longer input remains editable and scrollable. `Ctrl+Enter` / `Cmd+Enter` saves. Theme and locale controls retain work.

## Persistence

The versioned collection lives at `fieldnote-collection-v2` as `{version:2,notes:[...]}`. If absent, the original `ui-spec-temporal-note-v1` record is read into the collection without an automatic write. The first successful collection save commits the migrated record alongside new notes.

Read errors block writes and expose retry. Clear commits an empty versioned collection, so a legacy note cannot reappear on reload. Failed clear leaves notes and drafts intact. Multi-tab write conflict handling is not implemented.

## Review

Current continuation delivery: `../CONTINUATION-DELIVERY.md`. New decisions, scripts, failed assertion, diagnoses, captures and reports are under `../evidence/continuation/`. Previous evidence and `../DELIVERY.md` remain historical records of the single-note increment.

Tests used the pinned Chromium environment in `../TOOLING.md`. Captures were viewed separately; no physical-phone or assistive-technology certification is claimed. Original scene/card/face attribution remains in `THIRD_PARTY_NOTICES.md`.
