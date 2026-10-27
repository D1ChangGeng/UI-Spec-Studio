# Margin: a source reading sheet

Margin is a personal research notebook. A reader is working through **Cooling the city**, following sources and keeping their own notes. The header, sidebar, notebook, and reading pane have already been accepted. The source detail sheet is a functional starter that needs a professional, high-quality local redesign.

Build a richer source reading experience in the sheet. Give a reader a clear sense of the source they are reading, a comfortable way to move between a compact reference view and a more expansive reading view, and continuity as the sheet opens, moves, changes size, or closes. Content hierarchy, typography, spacing, controls, and motion should work together. Make the interaction feel complete during normal use, slow loading, failure, retry, and repeated actions.

The sheet is the consequential design surface. There is also one small navigation change: rename the existing **Saved** sidebar item to **Library**, preserving everything about its current behavior. Keep the accepted shell intact.

## Requirements

1. **Correct source details.** Each of the three notebook source chips opens the corresponding source. Show its identity, authors, publication, supporting metadata, summary, and complete readable source text with a strong, useful hierarchy. Source selection inside the sheet must identify the currently selected source clearly.
2. **Keyboard entry.** All source chips work with keyboard activation as well as a pointer. Opening the sheet places focus appropriately in an accessible dialog. Keyboard users can reach and operate the sheet’s source selection, reading controls, note field, save action, and dismissal controls without focus escaping behind it.
3. **Notes that belong to the source.** A reader can edit and explicitly save a note for each source. Saved notes persist across closing, reopening, and a page reload. An unsaved source-note draft survives closing/reopening, source switching, and compact/expanded changes during the current page session. Notes must never be transferred to a different source.
4. **Compact and expanded reading.** Provide useful compact and expanded modes with a clear control to switch between them. Maintain a coherent spatial relationship between the modes and preserve the reader’s place in the source. Repeated toggles and a reversal before a transition finishes must settle into the user’s latest requested state without a jump, stuck overlay, duplicated content, or lost draft.
5. **Dismissal and return.** A visible close control and Escape dismiss the sheet. Restore focus to the notebook chip that opened it, without scrolling the notebook back to that chip. Opening, expanding, switching sources, and closing must preserve the surrounding notebook’s scroll position and draft text.
6. **Direct vertical movement.** Make the sheet’s drag handle functional with pointer and touch input. Vertical movement should visibly follow the gesture, allow a committed downward gesture to dismiss, and settle sensibly after a short or cancelled gesture. Provide an equivalent keyboard-accessible way to change mode and dismiss. Dragging must coexist with scrolling the source text, and an interrupted or reversed gesture must not leave an unusable sheet.
7. **Latest source wins.** During a rapid A → B selection sequence, including while A is loading, the eventual title, metadata, source text, note, and selected control must all belong to B. Closing or switching must not let an older response overwrite the current selection. Repeated open, switch, close, and reopen actions remain reliable.
8. **Loading, failure, and retry.** Make ordinary and slow loading understandable while retaining the identity of the requested source. The provided one-time failure must produce a useful error and retry action. Retry must recover the same selected source and preserve notes. Avoid stale source text, misleading empty states, or a blocked interface during these paths.
9. **Responsive and accessible use.** Make the full sheet experience usable at viewport widths **390, 900, and 1440 CSS pixels**, including access to long content, note entry, and all controls. Avoid horizontal page overflow and inaccessible clipped actions. Respect reduced-motion preferences while preserving understandable state changes. Use appropriate semantics, readable contrast, and practical touch targets.
10. **Small change, stable shell.** Change the sidebar label **Saved** to **Library** while retaining its `saved` identifier, count, active-state behavior, and position. Preserve the accepted header, sidebar, notebook content, source chips, surrounding draft, and overall shell layout; only narrowly necessary layout fit corrections are allowed. Do not broaden the redesign.

## Scope and files

- Main work belongs in `src/SourceSheet.jsx` and `src/sheet.css`. You may restructure these freely, add local sheet components/styles, and adjust `src/App.jsx` to support the experience.
- Change the sidebar text in `src/navigation.js`. Preserve its identifiers and behavior.
- **Do not edit `src/domain.js` or `src/Shell.jsx`.** Their data, request behavior, notebook content, and shell behavior are fixed inputs.
- `src/shell.css` is the accepted surrounding shell. Preserve its design. A narrowly necessary layout fit correction is allowed only if sheet integration cannot be handled in the sheet’s own styles.
- Preserve the public hooks and behavior described in `CONTRACT.md`. Do not replace the provided data or request API with hard-coded ready states, change the delay/failure controls, or remove stateful content to simplify the interaction.
- This is a local Vite + React app. There is no backend. All source records are fictional fixture content. External source URLs are metadata, not required network resources.

## Run and inspect

```sh
npm run dev -- --port 5173
npm run build
```

The build uses `vite build --base=./`.

Use these fixture routes to inspect behavior:

- `/` — normal source response, approximately 450 ms.
- `/?delay=1800` — a slower response that makes source switching during loading easy to observe.
- `/?fault=once` — the first request that completes fails; retry succeeds.
- `/?fault=once&delay=1800` — slow loading followed by a one-time error.

The one-time error resets on a full page reload. Aborted requests do not consume it. The delay accepts milliseconds between 0 and 10000. Reloading preserves saved source notes; it is expected to reset unsaved drafts and the initial notebook scroll.

The ten requirements are also listed in `acceptance.json`. This task does not require a backend, publication, or changes outside this project.
