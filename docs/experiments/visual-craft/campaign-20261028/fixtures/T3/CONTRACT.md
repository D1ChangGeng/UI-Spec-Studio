# Fixture contract

This document describes the public interaction hooks and fixed data behavior for the Margin input fixture. Preserve the hooks when restructuring the source sheet. Additional hooks and components are fine. A hook identifies a logical element; it does not mandate its current tag, layout, or visual treatment.

## Fixed inputs

`src/domain.js` and `src/Shell.jsx` are immutable. Preserve the accepted shell styling in `src/shell.css`, except for a narrowly necessary fit correction described in `TASK.md`.

`src/navigation.js` is intentionally separate so the existing item’s label can change from **Saved** to **Library** without editing the shell. Keep its `id: 'saved'`, count, position, and selection behavior. The existing sidebar buttons only update their selected state; they do not navigate to another page or replace the notebook.

The three source IDs are:

| ID | Source title | Notebook chip |
| --- | --- | --- |
| `heat-mapping` | Reading heat at street level | Osei · 2024 |
| `shade-access` | The distance to shade | Park · 2023 |
| `night-cooling` | When the city does not cool | Rivera · 2025 |

Each record contains `id`, `title`, `subtitle`, `authors`, `publication`, `date`, `year`, `kind`, `readingMinutes`, `pages`, `citation`, `url`, `tags`, `summary`, `keyQuote`, `relevance`, and `sections`. Each section has a `heading` and an array of `paragraphs`. All content is fictional and supplied locally.

## Request behavior

```js
import { fetchSource } from './domain.js';

const controller = new AbortController();
const record = await fetchSource('heat-mapping', {
  signal: controller.signal,
});
// To cancel: controller.abort();
```

- Default completion delay: 450 ms. A successful call resolves a fresh copy of the selected record.
- `?delay=1800` sets the delay for every call on that page. Values are clamped to 0–10000 ms; invalid values use the default.
- `?fault=once` rejects the first request that completes on that page. A later retry succeeds. An aborted request does not consume the failure.
- Cancellation rejects with an error whose `name` is `AbortError`.
- Unknown source IDs reject with a readable error.
- An aborted or superseded request must never replace the selected source in the interface.

Use this API for loading source details. Do not change the fixture implementation, bypass its delay, or call a network service instead.

## Note persistence

The domain exposes `readSavedNote(id)`, `saveSourceNote(id, text)`, and `noteStorageKey(id)`.

Saved notes use these localStorage keys:

| Source | localStorage key |
| --- | --- |
| `heat-mapping` | `margin:source-note:heat-mapping` |
| `shade-access` | `margin:source-note:shade-access` |
| `night-cooling` | `margin:source-note:night-cooling` |

Keep this storage contract. Saves are explicit. An unsaved source-note draft should remain available within the current page session, including after dismissing and reopening. The notebook draft in the accepted shell is independent, held in React state, and must not reset when the sheet changes. A full page reload may reset unsaved drafts.

## Stable `data-testid` hooks

### Accepted shell

| Hook | Meaning |
| --- | --- |
| `app-shell` | Accepted shell root; may be made inert while the modal is open |
| `app-header` | Accepted header |
| `sidebar` | Accepted desktop sidebar; hidden by the accepted shell at narrow widths |
| `nav-notebooks` | Existing Notebooks navigation button |
| `nav-saved` | Existing Saved button to be relabeled Library; keep this hook |
| `reading-pane` | Independent notebook scroll container |
| `notebook-draft` | Controlled, editable notebook draft textarea |
| `citation-heat-mapping` | Notebook trigger for the first source |
| `citation-shade-access` | Notebook trigger for the second source |
| `citation-night-cooling` | Notebook trigger for the third source |

The three notebook triggers are real buttons. They support pointer activation and the normal Enter/Space keyboard behavior. Each is focusable when the sheet is closed. The notebook remains mounted across the complete sheet lifecycle.

### Sheet

| Hook | Meaning |
| --- | --- |
| `source-backdrop` | Overlay surrounding the sheet |
| `source-sheet` | Dialog root; retain `role="dialog"`, `aria-modal="true"`, an accessible name, `data-mode="compact"` or `"expanded"`, and `data-source-id` equal to the currently requested source ID |
| `source-title` | Title of the currently requested source; available during loading and errors |
| `source-close` | Visible, keyboard-operable close control |
| `source-expand` | Mode control; `aria-expanded` reflects expanded state |
| `source-drag-handle` | Region for direct vertical drag interaction; decorative in the starter, functional in the completed design |
| `sheet-source-heat-mapping` | Select the first source while the sheet is open |
| `sheet-source-shade-access` | Select the second source while the sheet is open |
| `sheet-source-night-cooling` | Select the third source while the sheet is open |
| `source-content` | Primary source reading/scroll region |
| `source-metadata` | Source author and publication metadata region after success |
| `source-loading` | Loading indicator; present during requests and announced appropriately |
| `source-error` | Error state; present after a failed request and announced appropriately |
| `source-retry` | Retry control inside the error state |
| `source-note` | Current source’s editable note field |
| `source-note-save` | Explicit save-note action |
| `source-note-status` | Text status for unsaved, saved, or failed note saving; announced appropriately |

For the three `sheet-source-*` buttons, retain a selected state accessible through `aria-pressed`. Keep exactly one logical instance of each hook in the active interface. Inactive transition remnants must not remain focusable, exposed as another dialog, or mistaken for active content.

The completed design may animate removal. Once closing has settled, the dialog must be absent or hidden and inert. Focus must return to the original notebook chip, including when the reader switched sources inside the sheet before closing.

## Useful inspection sequences

1. Scroll the notebook down, edit its draft, return to a source chip without reloading, then open/close and expand/compact the source. Confirm that sheet actions do not reset notebook state.
2. With `?delay=1800`, open Osei, select Park immediately inside the sheet, then select Rivera. Wait for loading to finish. Every displayed source detail and the note field must belong to Rivera.
3. With `?fault=once`, open a source, edit a note, wait for the error, and retry. Confirm recovery and the preserved draft.
4. Save different notes for two sources, close/reopen, and reload. Each saved note should remain attached to its own source.
5. Use Tab and Enter/Space to open and operate the sheet; dismiss with Escape. Confirm return focus and preserved notebook scroll.
6. Reverse the mode toggle before the transition finishes, drag and release a short distance, cancel a pointer gesture, and drag far enough to dismiss. Repeat after changing the selected source.
7. Inspect at 390, 900, and 1440 CSS pixels wide, including reduced-motion mode and a touch-sized viewport.

These sequences describe behavior, not a prescribed visual treatment or implementation strategy.
