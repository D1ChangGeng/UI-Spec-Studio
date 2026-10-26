# Bounded content application

This is the final three-file output of a fresh-context UI Spec Studio application.
It refines save-state and recovery language in the repository's existing bilingual
research-note fixture. It retains the original visual direction, single-note
storage key and schema. This is evidence of a scoped application, separate from
the maintained fixture under `examples/content-review/`.

From this directory, run `python -m http.server 8765 --bind 127.0.0.1` and open
`http://127.0.0.1:8765/index.html`. The note is stored in that browser origin's
`localStorage`; a different origin does not share it. The interface contains
explicit preview controls for a simulated failure and authored write delay.

The [application record](../content-application-review.json) identifies the original
task, corrected input setup, baseline and final source hashes, adoption, executed
checks, actual viewing and limits. The [runtime report](../content-runtime-checks.json)
records 113 passing assertions and 72 captures in the original temporary
environment. Selected images are retained beside the record; the full screenshot
matrix and temporary browser/font installation are not packaged here.

This output has no server integration, automatic saving, version history or
external publication. It does not establish real-user comprehension or preference.
