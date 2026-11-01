# Current continuation evidence helpers

These helpers preserve actual participant/reviewer bytes under `continuation-2100/`.
They leave the frozen registration, runtime, source fingerprint and release decision
unchanged. A new cell is a **supplementary replacement attempt**: its registered
prompt digest identifies the original registration reference; its actual dispatch
has a separate digest and explicit deviation audit. That record does not claim an
exact original dispatch or automatically count toward the registered matrix.

`prepare_prompt_audit.py` retains the actual message from a supplied spawn export,
the original registered prompt, their exact diff and the stated comparison limit.
Its output is a derived audit, not a fabricated tool event. Spawn export timestamps
are export times. `index_cell.py` requires separately supplied actual execution
start/end observations and their scope; it never derives start from export time.

## Preserve a completed cell

Provide a JSON configuration containing these keys, in addition to the existing
index helper's capture/log/child fields:

- `repo`, `cell_id`, `agent_id`, `source_workspace` and `replay_directory` (absolute).
- `evidence_directory` (repository relative, inside `continuation-2100/`).
- `spawn_repository_path`, `completion_repository_path`, `prompt_deviation_audit`.
- `started_at`, `completed_at`, `timing_scope`, `audit_observations`, `limitations`.
- `preview_command`, `capture_conditions`, `final_capture_prefixes`,
  `primary_view_globs`, `behavior_log_globs`, `children`.

Capture/log/report selection follows `support/recovery/index_product.py`:
`final_capture_files`, `primary_return_views`, `additional_tool_exports`,
`direct_source_files`, `report_files`, `additional_source_repository_paths` and
`source_workspace_aliases` are optional. Children require their real prompt,
spawn/completion, result and nonempty actual tool exports. Required condition
roles remain a property of the frozen protocol, not a consequence of indexing.

Run from the repository root, after recording the actual terminal notification:

```bash
python docs/evidence/v1.20.0/session-study/support/current-continuation/preserve_cell.py PATH_TO_ACTUAL_CONFIGURATION.json
```

The command refuses existing evidence directories, requires an actual fresh spawn
and matching `FINAL_ANSWER`, snapshots source, reconstructs every retained file,
then indexes observed products. Every subprocess's command, stdout, stderr and exit
status is retained. A failed stage remains available; the separate
`freeze_cell.py`/`index_cell.py` entry points allow diagnosis without overwriting a
completed index. PNG views retain original tool returns; failed behavior assertions
remain evidence rather than an automatic product acceptance threshold.

Use `prepare_blind_product.py --help` for explicit source/snapshot/replay/review-pack
paths, anonymous labels and mapping output. It copies frozen app/task/capture
bytes and keeps the condition map outside the anonymous pack.

## Preserve a fresh independent reviewer

Create a JSON list of repository-relative completed product `snapshot.json` paths.
After the reviewer completes, run `freeze_review.py` with `--repo`, `--source`,
`--review-series`, `--cohort cohort-01` and `--product-snapshots LIST.json`.
Choose a fresh series. The helper records every source file hash, reuses matching
immutable product bytes by content identity and archives all other actual reviewer
output. This avoids another complete copy of the supplied product pack. Borrowed
files retain exact source identities in bounded inventories. Their attribution is
byte reuse, never an invented reviewer action.

Verify the complete review using this continuation's `replay_review.py --repo REPO
--snapshot SNAPSHOT --output FRESH_DIRECTORY`. The older review replay helper does
not implement this explicit input-plus-overlay scheme.

`index_review.py CONFIG.json` copies reviewer-authored judgments and checks actual
view requests/returns against immutable anonymous maps. Its configuration requires
`repo`, `output_directory`, `snapshot_repository_path`, `reviewer_agent_id`,
`spawn_repository_path`, `completion_repository_path`, `prompt_repository_path`,
`run_records` (repository-relative run paths), `mapping_repository_paths`, and
`declaration_file` (reviewer workspace-relative actual JSON). Optional `products_file`
and `result_file` default to `products.json` and `FINAL.md`.

The reviewer supplies `products.json` records with `anonymous_product`, `findings`,
`judgment`, `viewed_original_files` and matching `view_exports` arrays. The actual
reviewer declaration supplies `outcome`, `reviewed_at`, `condition_blind`,
`blinding_limitations`, `scope`, `limitations`, `final_runtime_acceptance`. The latter
retains the reviewer's own G scope, limitations and repair disposition. Helpers
never invent `accept_limited` or a positive final-runtime judgment. All supplied
completed products require findings and original PNG viewing evidence; participant
and coordinator identities cannot serve as the reviewer.

## Historical checks and publication boundaries

`audit_existing.py --repo REPO --output FRESH_DIRECTORY` checks the current retained
complete records and reconstructs historical product/review snapshots, including
incomplete attempts. It verifies preservation archives and confirms frozen source
identity plus unchanged historical files. Logs establish archive/record consistency,
not independent product review or release acceptance.

`privacy_audit.py --repo REPO --commit COMMIT --output FRESH_DIRECTORY` scans exact
changed commit bytes and named pre-existing final-session trees, including archive
members. Reports include only paths, categories, counts and digests. Pattern
matches need contextual judgment; the absence of known patterns is a bounded
check, not a declaration that arbitrary data is public. No helper pushes to GitHub
or edits old/frozen evidence.
