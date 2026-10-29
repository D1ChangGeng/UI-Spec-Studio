# Leafnote

A bilingual, browser-local research notebook. No build step, server API, account, telemetry, or cloud sync. All runtime assets are local.

## Run

From this cell:

```bash
python -m http.server 8777 --directory app
```

Open `http://localhost:8777`. Use **New note** to begin, or **Try example notes** to load three clearly labeled fictional examples into an empty notebook. The examples include short English text, a longer English observation, and a longer Chinese research note.

## Working behavior

- Create, explicitly save, search title/context/body, select, and reopen notes.
- Each existing note and the new-note slot keeps a separate local draft. Changing selection, language, or theme preserves it. A leave-page warning protects unsaved work.
- Ctrl/Cmd+S saves. Ctrl/Cmd+K moves to search. Native buttons and fields support ordinary Tab/Enter operation; the delete dialog focuses Cancel and supports Escape.
- Deletion identifies the saved note and requires confirmation. Failed writes leave the saved collection intact.
- Storage read errors and malformed data block replacement. Recovery remains available from the collection on mobile and beside the editor on desktop.
- Export backup downloads JSON containing notes, drafts, the current editor, and the original raw storage keys. There is no import interface in this increment.
- Chinese/English, light/dark, and Comfortable/Compact reading density are saved when browser storage permits it. The selected note is restored on reload. Appearance changes preserve note identity and draft text; authored note content is never translated.
- Comfortable and Compact adjust list/editor spacing and typography together. Narrow context labels sit above their field, and long titles expand fully in browsers supporting field sizing.

## Storage contract

| Key | Purpose |
| --- | --- |
| `leafnote-notes-v2` | Versioned collection, note IDs, title, context, body, updated time, example flag |
| `leafnote-drafts-v2` | Unsaved drafts keyed by note ID, plus `new` |
| `leafnote-preferences-v1` | Language, theme, density, and selected note ID |
| `ui-spec-content-note-v1` | Original single-note record; read when no v2 collection exists and never deleted by migration |

Writes occur only after a checked read. A changed collection in another tab disables stale saves until read recovery. This is conflict detection, not atomic multi-tab merging. Draft maps are not a collaboration mechanism. Browser cleanup can erase local data; use export for a portable recovery copy.

## Source and maintenance

`vendor/pico.min.css` is Pico CSS 2.1.1, MIT-licensed; the license is in `vendor/PICO-LICENSE.txt`. It carries the semantic form/button/dialog visual base. `styles.css` configures product tokens and defines notebook composition. Native `dialog.showModal()` supplies focus containment and modal semantics; `app.js` owns notes, drafts, outcomes, and localization. Pico's official site now says it is unmaintained: this pinned CSS copy is a local maintenance responsibility.

Public design references and actual captures are recorded in `../DESIGN.md` and `../evidence/`. Reference product screenshots are evidence only and are not shipped as application assets.

## Verification

The available Playwright environment and exact commands are in `../TOOLING.md`. The core test runner is `../evidence/test_app.py`; it exercises the real local HTTP application and actual browser storage, with explicitly injected failure cases. `?test` exposes write-failure and one-second-delay controls for local testing; normal product UI contains no research controls.

See `../evidence/REVIEW.md` for executed assertions, viewed captures, original failures and repairs, and untested conditions. Passing assertions and screenshots are reported separately.

## Typography and density continuation

The current density tokens and narrower reading measure are documented in `../evidence/continuation/DESIGN.md`. New checks and captures are isolated under `../evidence/continuation/`; `../CONTINUATION-DELIVERY.md` summarizes this increment. The prior delivery and original evidence are preserved.
