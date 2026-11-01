<!-- Derived navigation copy; never use as an original participant export. -->

> Repository navigation copy. The participant report is retained byte for byte in [FINAL.md.txt](FINAL.md.txt) and the workspace overlay archives. Only local artifact link destinations below are adapted for this repository.

# Fieldnotes account settings — completed

The running settings application is implemented in `app/`, using the supplied Tabler 1.7.1 foundation. The original card, navigation, typography, native switches, light/dark surfaces, distributed assets and MIT license are retained. The authoritative settings store is unchanged.

## What changed

The account form now gives display name and organization room for long English/Chinese content through Tabler's bundled Autosize component. Explicit labels, required/optional guidance, localized field errors and first-invalid focus support correction. Language and theme controls retain the draft when switched.

Save feedback sits beside the footer actions and reflects real store events: validation, pending, failure, successful save and successful save with newer unsaved edits. A failed save preserves the draft and stored values; retry uses the real service. Cancel restores the latest persisted snapshot. Save and Cancel are disabled during the store's pending operation, while fields remain editable. Focus returns to Save only when doing so will not interrupt continued editing. Public-profile copy describes the draft choice and explains that email stays private.

Implementation uses existing source components and utilities; no replacement visual system or custom CSS was added. The changes and source relationships are recorded in [SOURCE-ADOPTION.md](artifacts/SOURCE-ADOPTION.md.txt) and [DESIGN.md](artifacts/DESIGN.md.txt).

## Verification

The main behavior suite passed **68 assertions** across English/Chinese and light/dark at 1280 × 600: authoritative validation boundaries, first-invalid focus, no writes on invalid/failure, retry, snapshot semantics during continued editing, draft retention through language/theme changes, Cancel, reload persistence and absence of page errors. An independent observer completed **27 assertions** on its recorded earlier revision. Its historical validation concern was subsequently resolved by the main suite; its report is preserved unchanged.

Final-source render captures cover **12 combinations**: 1440 × 900, 1280 × 600 and 390 × 844 in both languages and both themes. All reported no horizontal overflow, page errors or clipped long textarea values. The final invalid, pending, failure and success states were also captured in every language/theme combination. The only change after the 68-assertion suite was applying the existing text-body utility to status alerts; final state captures use that delivery revision.

I personally inspected the actual source baseline and assembled product images, including final narrow settled views and controlled state captures. The status text contrast measurement improved to **9.59:1 in light** and **10.85:1 in dark** using an existing Tabler utility. That result concerns this status text, not a complete accessibility audit. [VISUAL-REVIEW.md](artifacts/VISUAL-REVIEW.md.txt) identifies the observations, repairs, source boundaries and limitations.

Evidence includes [behavior results](artifacts/evidence/final-behavior-02/results.json), [final render facts](artifacts/evidence/final-render/facts.json), [source hashes](artifacts/evidence/final-source.json), [implementation diff](artifacts/evidence/product-changes.patch.txt) and [delegation record](artifacts/DELEGATION.json). Actual tool responses, failed attempts and corrections remain in `evidence/`.

Representative final captures: [narrow English fields](artifacts/evidence/narrow-settled/light-en-fields.png), [narrow Chinese dark actions](artifacts/evidence/narrow-settled/dark-zh-actions.png), and [Chinese dark success](artifacts/evidence/final-state-view/dark-zh-success.png).

## Run and scope

From the package's `app/` directory:

```sh
python3 -m http.server 4404 --bind 127.0.0.1
```

Open `http://127.0.0.1:4404/?lang=en&theme=light`, or use `?lang=zh&theme=dark`. A fresh page with `&fail=once` exercises one failed valid save followed by a successful retry. The preview server used for verification has been stopped; the source is ready to restart with this command.

Settings persist in the current browser's localStorage; no external account service is implied. The inherited navigation makes the narrow page long and requires scrolling or section anchors. Outer Tabler gallery navigation/footer remain English, and unrelated gallery routes are outside this task. Testing used local Chromium captures and controlled episodes; real mobile devices, other browser engines, screen-reader speech and natural-time motion playback were not assessed. No unresolved core settings defect was found in the scoped checks.
