# Fieldnote

A small, browser-local research note. Write on the front of the card, save, then read the stored version on the back. Returning to editing restores the draft, cursor selection and textarea scroll position.

## Open locally

From this cell:

```sh
python -m http.server 8737 --bind 127.0.0.1 --directory app
```

Open http://127.0.0.1:8737 . This is a local demo; there is no deployment, server account, cloud sync or remote save.

## Behavior

- Save writes the submitted snapshot to `localStorage` under the existing `ui-spec-temporal-note-v1` key. Existing valid notes remain readable.
- A 650 ms demonstration delay makes pending feedback observable. The card turns only after Storage accepts the write.
- Writing while saving retains the newer draft on the editing face; the submitted snapshot is saved separately.
- Failure keeps the draft and previous saved version and provides retry. Malformed/unreadable data blocks writes until a successful read or explicit clear.
- The save limit is 600 characters. Longer pasted text is retained, remains scrollable and receives explicit feedback; saving is disabled until shortened.
- Saved notes survive reload. Unsaved drafts live in the current page only; they are not promised to survive closing or reloading it.
- English/Chinese and light/dark controls retain current work. Theme begins from the system preference; theme/locale overrides last for the page session.
- Reduced motion changes faces without spatial movement. Both faces retain the same card dimensions and data semantics.
- `Ctrl+Enter` / `Cmd+Enter` saves from the textarea. Keyboard focus moves through a stationary control while a card turns and returns to the destination after settling. An interrupted turn follows the latest request.

## Review and evidence

See `../DESIGN.md` for the current decisions, references and claim boundaries, and `../DELIVERY.md` for the reviewed result. Evidence scripts, original failures, captures and JSON results are in `../evidence/`.

The automated tests use the pinned local Chromium environment identified in `../TOOLING.md`. They establish the exercised browser behaviors, not a cross-browser accessibility certification. Visual observation is recorded separately. No external runtime dependencies are loaded.

The centered scene/card/face transform construction is adapted from David DeSandro's MIT example. See `THIRD_PARTY_NOTICES.md`.
