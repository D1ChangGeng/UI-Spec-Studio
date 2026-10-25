# Temporal visual review: a note through time

This authored local fixture carries one research note through a reversible card
preview, a delayed save, failure/retry and a saved-note view. It reuses the Study
sample's product vocabulary and browser-local save boundary. Its CSS artwork and
motion are authored for this study; no third-party resource adoption is claimed.

The visible disclosure identifies the 900 ms preview delay. Saving reaches real
browser Storage. The card expresses preview intent independently of that save.
The saved-note view keeps an existing persisted version visible during a newer
save; the first in-flight save shows an explicitly labelled provisional snapshot.
A newer draft remains editable.

## Run the example

From the repository root:

```bash
python -m http.server 8000
```

Open `http://localhost:8000/examples/temporal-review/`. Use See context to turn the
same note over and back, including a reversal during motion. Pause the decoration,
save while continuing to edit, then open Saved note and return. The language and
theme controls retain current work. Preview controls can clear this demo's data.

## Capture and check the real sequence

Use the existing optional browser dependencies:

```bash
python -m pip install -r tools/requirements-preview.txt
python -m playwright install chromium
python tools/validate_temporal.py --output-dir temporal-evidence
```

`--browser-path` selects an available Chromium executable. `--no-video` produces
ordered screenshots only and leaves playback unobserved. The full release check
records both screenshots and video through a temporary localhost server.

| Episode | Observed boundary and engineering check |
|---|---|
| Flip and return | One DOM object, both completed transitions and a stationary layout container |
| Interrupted flip | A second visible-control input during the active transition; final face and inert state |
| Decorative cycle | Natural progression through an iteration event; actual sampled transforms |
| Over-limit draft | A long insertion remains intact; count/error, invalid state and disabled saving explain the bound |
| First save and navigation | A provisional snapshot is labelled while Storage remains empty; confirmed outcome appears in the current view |
| Save while editing | The previous saved snapshot remains visible during a newer save; one native write and a retained newer draft |
| Failed save and retry | Explicit injected Storage failure; preserved value and text; recovery through native Storage |
| Saved view and return | Persisted content, shared header, retained draft, return focus and paused decorative phase |
| Reduced motion | Browser preference disables optional movement while retaining the equivalent content/action |
| Unreadable saved note | A malformed stored record remains unknown; the view explains recovery and returns to the retry; explicit clear restores editing |
| Clear failure from Saved note | Failed removal retains storage and reveals a focused recovery control; successful native retry confirms removal |

An associated count discloses the 600-character save bound. Longer pasted text
remains editable; clear feedback and disabled saving prevent silent loss. The
browser checks that behavior, and a normal return to editing focuses the textarea.
An unreadable result returns to its existing recovery control instead.

The desktop run uses English/light at 1280 × 900; the narrow run uses Chinese/dark
at 390 × 844. Device pixel ratio is 1. Install fonts covering Chinese before the
narrow run; the release environment uses Noto CJK. The report records resolved
heading and hint fonts, and actual glyphs still require visual inspection.
These are focused condition samples, not an
exhaustive cross-product of locale, theme, viewport or device.

## Read the evidence accurately

`report.json` identifies the source commit, worktree state and source-file hashes;
browser and viewing conditions; scheduled and actual actions; event timestamps;
before/after state snapshots; capture spans and gaps between capture brackets. Screenshot
times bracket the capture call because a screenshot is not an atomic state read.
The actual image instant lies within each bracket; the reported bracket gaps do not establish the maximum inter-image sampling gap. Requested delays remain separate from actual cadence. The browser clock and
animation timing run normally, with screenshot animations explicitly allowed.

Each episode folder contains chronological full-viewport PNGs. The WebM files use
the same dimensions as their viewport and are finalized by closing the browser
context. Each video covers one whole context. Document performance timestamps
locate actions and frames; exact video-time synchronization is not asserted.

Open the images and watch the relevant recording intervals to assess perceived
object identity, motion rhythm, dynamic composition and cross-view continuity.
Use whole frames for context and original-size frames for text and local detail.
The script leaves visual review pending even when behavior assertions pass.

Natural-time capture still has sampling and recording overhead. These outputs
support the states and changes actually observed; they do not measure presented
frame delivery, field responsiveness or smoothness on target hardware. Static
endpoints and a video file's existence alone do not establish transition quality.
Record viewing, interpretation and user acceptance separately from capture.

The fixture's save delay is illustrative and its failure is deliberately injected.
Actual Storage persistence is checked by reload. Service latency, production
permissions and real-user comprehension require evidence from their own product.
