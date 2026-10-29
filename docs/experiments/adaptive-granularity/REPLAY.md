# Inspect or restore an application-study result

The [registered protocol](PROTOCOL.md) identifies the conditions and fixed tasks.
[Results](RESULTS.md) distinguish participant reports, independent product review,
mechanical checks and unobserved dimensions. Applications use synthetic content
and browser-local data. They are study outputs, with their reported gaps retained.

## Restore original source and evidence

From a checkout or the full source release, choose a new destination:

```bash
python tools/replay_granularity_run.py docs/experiments/adaptive-granularity/runs/T1-m9 work/T1-m9-final
python -m http.server 8000 --directory work/T1-m9-final/app
```

Open `http://localhost:8000/`. Use a fresh browser profile or a distinct local port
for each cell: different implementations can use the same storage-key names.
The original first delivery can be restored separately:

```bash
python tools/replay_granularity_run.py docs/experiments/adaptive-granularity/runs/T1-m9 work/T1-m9-initial --stage initial
```

Replace the cell name with another family/condition from the results. The tool
refuses to overwrite an existing destination and checks every original file's
SHA-256 before creating the output. It restores source, licenses, participant
records, test scripts, logs and captured media. It does not restore a live server,
browser profile or Agent session, and it does not assign a quality verdict.

## Archive layout

Each `runs/<cell>/archive-index.json` maps both initial and final snapshots from
their original relative paths to exact stored bytes. Unchanged initial files
can reference the final copy. Changed earlier files remain separately available.
Raw captures are grouped into bounded ZIP bundles; each index identifies the
member and its SHA-256. Application assets stay beside their actual source.
No frame was altered to improve an observed result.

Participant Markdown records are preserved as `.md.original.txt` in the archive.
Their original local links and wording remain intact, including limitations and
failed attempts. Restoration returns their original filenames. Published result
links and the review gallery provide repository-relative navigation; original
host paths are provenance, not promises of publicly hosted previews.

## Repeat observations carefully

The original scripts record actual commands, locators, content and failure
injection used by their authors. Some contain the original host's absolute Python,
browser, server and evidence paths. Adapt those environment paths deliberately
before replaying a script, retain the original, and report the browser/version and
conditions of the new run. An earlier passing script is not a substitute for
viewing the current result, and a newly failed locator is not automatically a
product failure.

The [environment record](../../evidence/v1.17.0/environment.json) identifies the
Chromium build and the Noto Sans/Serif CJK system fonts, including acquisition URLs
and hashes. Those system dependencies are not bundled with every application.
Matching source bytes alone does not promise matching pixels on another machine.
That record describes the pre-study infrastructure smoke; its observation limits
apply to that smoke, while subsequent application and review outcomes are separate.

Shared tool/guidance inputs are retained byte-for-byte in
[shared-inputs](shared-inputs/identity.json). The frozen
[registration](registration.json) is the pre-execution snapshot and intentionally
retains its preparation status. Actual dispatches, snapshots and host interruptions
belong to [run-events](run-events.json) and the completed result. These records do
not claim a complete host transcript or exact token accounting.

The portable `ui-spec` installation contains the professional method, templates
and inspectors. This study's applications, licensed replay fonts, captured
references and experimental records are distributed in the full source release.

## Restore an independent review

The [independent review index](RESULTS.md#independent-product-review) links exact anonymous reports,
commands, original failures, captures and post-freeze maps. The same restoration
tool accepts a review archive:

```bash
python tools/replay_granularity_run.py docs/experiments/adaptive-granularity/reviews/T1 work/review-T1
```

This restores review files, not the applications. Restore the corresponding cell
sources separately and adapt the original host paths before rerunning a script.
[The gallery](GALLERY.md) exposes selected byte-identical captures directly; its
provenance file maps every image to the original review file and hash.
