<!-- Derived navigation copy; never use as an original participant export. -->

> Repository navigation copy. The participant report is retained byte for byte in [FINAL.md.txt](FINAL.md.txt) and the workspace overlay archives. Only local artifact link destinations below are adapted for this repository.

# Fieldnotes — editorial workspace with an unresolved final store issue

The visual implementation and live workflow checks are complete, but final store hygiene remains unresolved. The runnable TiddlyWiki workspace now uses **Vanilla Paper 0.10.0** with a leading-edge navigation rail, bounded reading sheets, a red page margin, distinct reading/interface/editor typography, and coherent Day and Night palettes. The native note store, search, links, tags, pencil/checkmark editing and server persistence remain intact.

[View the final workspace](artifacts/evidence/captures/settled-start.png) · [Dark reading](artifacts/evidence/captures/settled-night-reading-1440.png) · [Compact editor](artifacts/evidence/captures/settled-day-editing-1280.png) · [Narrow dark editor](artifacts/evidence/captures/settled-night-editing-390.png)

## Run

From `/workspace/scratch/708e8b7f118e/ui-study/worksets/w09/app`:

```bash
PORT=4409 ./start.sh
```

Open [http://127.0.0.1:4409/](http://127.0.0.1:4409/). Node 20+ is required; no package installation is needed. The local preview was stopped after verification to leave a stable handoff. [index.html](artifacts/app/wiki/output/index.html) is the successfully built offline export; the server path remains the authoritative editing/persistence path.

Use **Control Panel → Appearance → Palette** to select Vanilla Paper Day or Night. **Appearance → Paper** exposes the source's layout and editor options. Native Animation duration can be set to `0` for a quiet interaction setting.

## Design decision and source retention

Notebook was the first preference: its centered sheet and action bar made a plausible compact workpad. The populated comparison showed that Paper better carries the requested editorial studio character through actual long reading and editing: serif reading, sans controls, a ruled mono editor and a consistent paper/margin relationship. Starlight supplied a more textured serif alternative, but retained a broad line measure. The source comparison and its limits are documented in [DESIGN-MODEL.md](artifacts/DESIGN-MODEL.md.txt).

Paper is adopted from Simon Huber's MIT-licensed source at revision `031a78d4d4187128c632f8a647fa05408eddc700`. All **55 upstream theme files are unchanged**, with their identities retained. Configuration selects the left rail and always-visible note actions; three control/date palette roles use an existing darker ink color from the same palette. There is no original layout, new visual component, generated image or replacement storage system. Unused trial themes were removed from the runtime. The exact adoption boundary and source notices are in [INTEGRATION-DECISION.md](artifacts/INTEGRATION-DECISION.md.txt).

## Verified result

- Read the full interview, reached its final unresolved question, opened the Evidence ledger table and returned through native navigation.
- Edited an English and a Chinese passage through the actual textarea and checkmark. The filesystem contained both changes, and reload returned the exact saved note.
- Started and cancelled another edit; the saved note remained unchanged and the native draft was removed.
- Used keyboard search and keyboard activation to reach the working-draft editor.
- Captured reading and editing in both palettes at **1440×900, 1280×640 and 390×844**; document and editor bounds passed. Settled captures replaced an early screenshot taken during the native edit transition.
- Checked Chinese UI reading, changed palettes through the native Control Panel, and inspected ordered normal-motion and reduced-motion sidebar frames.
- Completed the upstream offline build and recorded exact source hashes. The final runtime request sample contained no external requests.

The eight supplied notes retain their meaning and structure. Seven bodies are unchanged. The interview contains only the two documented meaning-preserving edits used for the persistence test. Detailed observed results and exact tool-response records are linked from [VISUAL-REVIEW.md](artifacts/VISUAL-REVIEW.md.txt) and [verification.json](artifacts/evidence/verification.json).

## Limits

Verification used Chromium 143 and emulated viewport sizes. It does not establish cross-browser, physical-mobile-keyboard or screen-reader acceptance. Motion was inspected through timestamped frames and controlled operations, without natural-speed playback or a frame-pacing benchmark. Server failure/retry recovery was not fault-injected; the upstream mechanism is unchanged. Paper's own settings text remains English. Public author-page retrieval was unavailable, so Paper's original source was rendered locally with its own documentation; it is not represented as an observed hosted demo. The interrupted image-response export and initial test-selector failures are retained with their corrections.

A final integrity scan also found stale test-draft/seed files after the restart/build sequence. Archiving was attempted with the server stopped and the export rebuilt, but a subsequent fresh native boot still loaded a stale draft; file inspection showed the stale files present again. This final check failed, and the cause remains unresolved. The result should not be treated as fully accepted for continued editing until the duplicate/stale file behavior is diagnosed. This finding and its scope are recorded in VISUAL-REVIEW.md; a browser-only cancellation check was not treated as proof of complete filesystem cleanup.
