# Meridian

A dependency-free, browser-local conversational research demo. Serve this directory over HTTP, then open it in a modern browser:

```sh
python -m http.server 8080 --bind 127.0.0.1 --directory app
```

Open http://127.0.0.1:8080/ after starting that server.

The workspace includes streamed deterministic examples, stop/continue, retry, source reading, local thread/draft/theme persistence, filename-only attachments, and mobile navigation. The Local demo control selects a long response or a simulated failure for the next question. Enter sends; Shift+Enter inserts a line; Ctrl/Cmd+O starts a new thread.

No backend, API keys, remote fonts, libraries, analytics, or content requests are used. The Content Security Policy blocks network connections. Local file contents are never read; only filenames are kept. All answer and source text is authored synthetic material.

## Files

- `index.html`: native page and dialogs
- `styles.css`: Meridian theme and adapted conversation foundation
- `tokens.css`: attributed Radix Slate source palette
- `app.js`: fixture content, stream state, source navigation, and local persistence
- `THIRD-PARTY.md`: preserved source notices

See the cell's `DESIGN.md`, `evidence/`, and `DELIVERY.md` for adoption boundaries, executed checks, viewed captures, and remaining work.
