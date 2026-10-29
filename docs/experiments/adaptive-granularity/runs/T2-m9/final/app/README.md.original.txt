# Meridian

A working browser-local conversational research demonstration. Open through any static HTTP server. No build, package install, API key or external service is required.

From this cell:

```bash
python -m http.server 8739 --bind 127.0.0.1
```

Open http://127.0.0.1:8739/app/ . The current testing server uses this address.

## Try the complete loop

1. Choose a starting question, or type your own. Enter sends; Shift+Enter inserts a newline.
2. Watch the response appear. Stop retains the partial answer; Continue response resumes it.
3. Scroll upward while another answer grows. The reading position stays put. Back to latest returns to the newest content.
4. Open a sample source note. On desktop it sits beside the conversation; on smaller screens it opens in a native modal dialog.
5. Open Local demo and select Simulate a failure on the next response. Send a question, then Retry response.
6. Add filenames with the attachment button. Only names are recorded; the contents are never read.
7. Create another thread and return through history. Drafts, filenames, thread content, theme and reading position are saved locally.

Ctrl/Cmd+K creates a new thread. Native dialogs support Escape and keyboard focus return. Light/dark appearance is available in the left navigation or narrow header.

## Boundary

Answers and notes are deterministic authored samples. No research retrieval, model, file parsing, accounts, cloud synchronization or external requests are implemented. Storage is local to the current browser and origin. This is not a production research system.

## Source and maintenance

- `index.html`: semantic shell, composer, native dialogs.
- `styles.css`: warm editorial theme, responsive layout, shared reading/input measure.
- `app.js`: local state, timers, rendering, persistence, interruption and recovery.
- `tokens.css`: retained Radix Slate scale used for secondary-text roles.
- `THIRD-PARTY.md`: notices and pinned source attribution.

The layout relationships are adapted from the supplied native reference, itself a documented cross-stack transfer of assistant-ui's ChatGPT page. The upstream React implementation is not installed. The design record at `../DESIGN.md` identifies retained relationships, authored behavior and evidence limits.

## Read sources while an answer arrives

Inline citations appear as paragraphs complete, before the full answer is finished. Open a citation to highlight that paragraph and read its source note. The note repeats a short excerpt so its relationship to the answer remains clear.

Opening the source holds the conversation's reading position. Back to latest explicitly resumes following, including with the desktop dock open; scrolling upward stops following again. The desktop composer, stop/continue and retry remain usable beside the note. On a phone, use the sticky Back action or Escape to return to the same draft and citation.

Current continuation decisions and checks are in `../CONTINUATION-DESIGN.md` and `../evidence/continuation/`.
