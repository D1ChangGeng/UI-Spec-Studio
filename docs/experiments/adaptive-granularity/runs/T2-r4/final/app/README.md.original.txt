# Meridian

A browser-local conversational research demonstration. Questions, filenames and answers remain in the browser. There is no API key, backend, external font, analytics, or runtime network dependency.

## Open the app

From the cell directory (one level above this file):

```bash
python3 -m http.server 8844 --bind 127.0.0.1
```

Open **http://127.0.0.1:8844/app/**. The source is static HTML, CSS and JavaScript; there is no build step. Serve over HTTP to exercise browser persistence consistently. The implementation session left that preview server running locally.

## Try the main journey

1. Select a starter question or type your own. Enter sends; Shift + Enter adds a line.
2. Watch the illustrative answer unfold. Stop keeps the partial answer and any follow-up draft.
3. Read an inline numbered source as its paragraph arrives, even while the answer continues. Desktop opens a companion panel; compact widths open a native dialog. The cited paragraph is highlighted and repeated in the source view. Stop/Try again is also available there. Back to answer, Close or Escape returns to the thread.
4. Ask another question, scroll upward while it writes, and use **Latest response** to return to the end.
5. Open **Demo** in the header to make the next answer longer, slower, or fail once. **Try again** recovers in the same answer without duplicating the question.
6. Add files to see filename chips. File bytes are never read. Start another thread and return from the history list; drafts and reading position are retained.

Use the sidebar's appearance control to switch light and dark themes. On mobile, the menu opens the sidebar controls. Sample threads are explicitly labeled and separate from your own questions.

## Source structure

- `index.html`: semantic shell, native dialogs and inline SVG symbols.
- `foundation.css`: actual selected CSS relationships adapted from the supplied conversation foundation.
- `styles.css`: Meridian's visual system, responsive layout, themes and reading surfaces.
- `app.js`: deterministic content, streaming state, request ownership, source reading, history and local persistence.
- `SOURCES.md` and `THIRD-PARTY.md`: adoption boundaries and retained notices.

Browser records use `meridian-workspace-v1` and `meridian-theme`. Clearing those keys resets the demo. No deletion control or synchronization is implemented.

## Verification and limits

The browser evidence and replay scripts are in `../evidence/`. `../DELIVERY.md` and `../DESIGN.md` explain reviewed behavior, visual repairs and remaining conditions. Chromium 143 was tested at 1440×900 and 390×844, with one 390×500 reachability check. Physical mobile keyboards, Safari, Firefox, screen-reader operation, forced colors, and large history stress are not verified.

The answers and source documents are authored fixtures. Three topic families and a generic framework demonstrate the interaction; they are not an open-ended model. A follow-up continues the current topic with a fixed framework. Attachments are names only. Storage is browser-local and can be cleared by the browser.
