# Fieldnote

A browser-local collection of research note cards. Open a numbered card, edit its draft, save, and return to the same place in the collection.

## Run locally

From `app/`:

```sh
python -m http.server 8939 --bind 127.0.0.1
```

Open http://127.0.0.1:8939 . No build, package installation or backend is needed.

## Use

- **New note** starts an empty draft. Collection cards show saved, saving, session-draft or failed status.
- Open any card to edit. Its content is prepared before navigation begins.
- **Save note** or **Ctrl/Command + Enter** saves that note. Only a confirmed browser write permits the front/back turn.
- **Keep editing** returns from the saved face and restores textarea selection/scroll.
- **All notes** returns to the collection with the selected card, keyboard focus and previous collection scroll position preserved.
- **Escape** returns from saved to editing, then from editing to the collection.
- Theme and Chinese/English controls retain the work. Reduced motion removes spatial transitions.
- **About this demo** explains the local boundary; its clear control removes only the currently open note.

## Data and limits

Saved records use `fieldnote-collection-v1`. When that key is absent, a valid record under the original `ui-spec-temporal-note-v1` key appears in the collection with its original ID. The next successful save writes the collection; the legacy key remains untouched.

The original 900ms demo save delay and 600-character save bound remain. Longer input is retained and saving is blocked with an explanation. Per-note drafts survive in-page navigation but not reload. The collection labels that lifetime. A failed whole-collection write leaves persisted records unchanged, retains the edited draft, and marks the responsible card for retry. Malformed saved data blocks new writes until a successful read retry.

No cloud sync, account or cross-tab conflict resolution is provided. Saves are serialized during the short local-demo delay; other notes can still be opened and edited. Browser persistence is scoped to the origin used to run the app.

## Evidence

The cell's original evidence is preserved. New tests and captures are under `evidence/continuation/`, with delivery in `CONTINUATION-DELIVERY.md` and decisions/visual observations in `CONTINUATION-DESIGN.md`.
