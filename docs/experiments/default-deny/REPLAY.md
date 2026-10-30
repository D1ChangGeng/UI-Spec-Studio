# Reconstructing the applications and evidence

These are frozen experimental outputs, including observed defects and incomplete
checks. They are not endorsed production templates. The coordinator did not repair
them after the participant handoffs. The [results](RESULTS.md) and independent
reviews explain their actual strengths and limits.

## Application replay

From a checkout or extracted source release, choose one cell and extract the
**whole** application archive into its own directory. Keep both `app/` and
`resources/`; the latter contains source identities and applicable notices.
For example:

```bash
mkdir -p replay/T1-p6
unzip docs/experiments/default-deny/runs/T1-p6/application.zip -d replay/T1-p6
cd replay/T1-p6/app
npm ci
npm run dev -- --host 127.0.0.1 --port 4311
```

Use the committed package lock and a compatible Node/npm installation. Each replay
should install its own dependencies instead of sharing the experiment host's
`node_modules`, which avoids sharing Vite's optimization cache.

| Cell | Actual runtime | Start from the extracted `app/` directory |
|---|---|---|
| T1-p6 | React / Vite | `npm ci`, then `npm run dev -- --host 127.0.0.1 --port 4311` |
| T1-n2 | React / Vite | `npm ci`, then `npm run dev -- --host 127.0.0.1 --port 4314` |
| T2-k4 | React card island / Vite with vanilla business owner | `npm ci`, then `npm run dev -- --host 127.0.0.1 --port 4312` |
| T2-v9 | Static vanilla application | `python -m http.server 4315 --bind 127.0.0.1` |
| T3-r8 | Static vanilla application | `python -m http.server 4313 --bind 127.0.0.1` |
| T3-c7 | Static vanilla application | `python -m http.server 4316 --bind 127.0.0.1` |

Open the corresponding `http://127.0.0.1:PORT/`. Each port has its own browser
storage. Use an isolated browser profile or clear only that test origin before a
fresh run. The tasks operate on local sample content; they do not connect a server
account or a real reference library.

One participant README location is inaccurate and is preserved as an original
handoff fact: T1-p6 says the Magic UI notice is under `app/public/licenses/`.
That folder contains its two font OFL notices; the Magic UI MIT notice is actually
at **`resources/magicui/LICENSE.md`** in the same application archive. Keep that
notice with any reuse. Do not infer an absent license from the mistaken pointer,
or copy only `app/` and lose the notice.

## Inspect the evidence

Each `runs/CELL/archive-index.json` records the application and participant-evidence
archive hashes and every included file's SHA-256. The archive includes saved
source decisions, observations, screenshots and scripts. It excludes installed
dependencies, build output and caches. The exact working-boundary file is adjacent
as `RUN.md`; actual dispatch prompts and input hashes are in the unchanged
[registration](registration.json).

The independent reports are under `reviews/T1`, `reviews/T2` and `reviews/T3`.
Each has a readable Chinese report, the exact review instructions/requirements,
an evidence archive and an index. Directly linked report images/JSON are also
provided adjacent to the report when needed. The full archive retains additional
frames, scripts, unsuccessful checks and recordings. Anonymous mapping is disclosed
separately in [review-mapping.json](review-mapping.json).

To inspect a saved browser script, extract its evidence ZIP first. **Historical
capture scripts are not portable unchanged:** they contain the original workspace,
Python, Chrome, Fontconfig and port paths. Replace these with the reconstructed
application locations and available browser tooling. A new run is new evidence;
do not overwrite the frozen records. The original environment is described in
`inputs/ENVIRONMENT.md` and [environment-addendum.json](environment-addendum.json).
Chinese rendering requires an appropriate local CJK font; the host font fix did
not alter the products' font stacks.

T1's independent review encountered Vite `504 Outdated Optimize Dep` while using
the common installed dependency cache. The preserved review-only startup script
uses separate cache directories without editing application source. This host
correction is distinct from a product defect. Video capture availability also
differed across attempts. A saved video or ordered contact sheet does not prove
that anyone watched it at natural speed.

## Method identities and the final correction

- `inputs/runtime-A.zip`: exact complete installed v1.18.0 method.
- `inputs/runtime-B.zip`: complete candidate used by the six-run comparison;
  preserve its original bytes and interpretation.
- `inputs/runtime-release.zip`: exact complete final v1.19.0 runtime.

The [final delta](final-runtime-delta.json) records the only B-to-release change:
two W1/authorization premises in `references/examples.md`. A separate
[follow-up registration](followup/registration.json) uses that exact final runtime
with the T3 starter and a relevant-examples reading instruction. It is not a
replacement for any original comparison cell. The completed follow-up's
[own replay and outcome](followup/RESULTS.md) points to its separate output archive.
It is a static vanilla application on port 4317, with the same whole-archive/license
and historical-script caveats above.

The source release's identity tests check these archives, reversible predecessor
recovery and the declared final delta. Those checks prove byte relationships, not
resource maturity, exception necessity or visual quality. Dispatch/archive event
timestamps are retained as host observations; their difference is not a measured
participant working duration or a synchronized GitHub server timestamp.
