# Fieldnote

A single browser-local research note. Write on the front, save, and read the persisted version on the reverse. Failed saves leave the draft available and offer a retry. Editing during the demo's save delay preserves the newer draft.

## Run locally

From this `app` directory:

```sh
python -m http.server 8939 --bind 127.0.0.1
```

Open http://127.0.0.1:8939 . No build, package installation or backend is required.

- **Save note** or **Ctrl/Command + Enter** saves a snapshot in this browser.
- **Keep editing** or **Escape** returns to the draft, restoring selection and textarea scroll.
- The control below the card can reverse a turn while it is moving.
- Theme and Chinese/English controls preserve the note.
- **About this demo** explains the local boundary and exposes clearing.

## Boundaries

The save has a 900ms demo delay; the actual write is browser localStorage. The original `ui-spec-temporal-note-v1` key is preserved for existing records. Notes have a 600-character save bound; pasted longer text is retained and explained. Unsaved edits remain in the open page but do not survive reload. There is no account, server sync or production service.

## Verification

The cell's `evidence/check_app.py` runs real HTTP browser tests and captures. Failure injection patches Storage only inside isolated test pages and restores the native methods for retries. `evidence/run-01.log` preserves the initial harness failure; later logs distinguish the repaired run. The design and delivery records explain actually viewed evidence and remaining conditions.
