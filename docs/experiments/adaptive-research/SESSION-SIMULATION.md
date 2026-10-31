# Owner-authorized session simulation acceptance

## Scope and evidence boundary

The repository owner explicitly authorized replacing the unavailable native
Codex Cloud validation with the closest feasible simulation using actual
independent agents in this ChatGPT session, then merging PR #4 and publishing
v1.20.0. Retain the exact user statement in the authorization artifact; this
document does not supply authorization by itself.

Actual agents perform research, change source, run the applications and inspect
real screenshots. The simulated part is the native role environment: the host
passes the distributed role instructions to ordinary independent agent contexts.
This cannot authenticate native role registration or discovery, resolved backend
model/effort identities, native usage, billing, context pressure, human product
acceptance, or the original native campaign. A host-requested alternate model in
D is a declared request; its resolved identity remains unknown. D can instead be
explicitly unexecuted with a reason.

Schema 1 retains the original native checks without a fallback. Schema 2 accepts
only `owner_authorized_session_simulation` and `approve_limited`. Both use the
existing publication command and require all engineering gates. No installed
Skill or adapter behavior changes for this acceptance route.

## Freeze and execute

Finish acceptance-validator, test and AGENTS changes before freezing the plan:
the candidate fingerprint includes them. Freeze the complete candidate Skill,
baseline Skill, role instructions, task/starter inputs, exact dispatched prompts
and environment conditions. Preserve the baseline commit named in PROTOCOL.md.
Use fresh `fork_turns=none` contexts and disjoint workspaces. Shared host, system
instructions, tools, environment access and browser limitations remain disclosed
in the environment artifact and plan's `host_limitations`.

The 18-cell matrix retains the original task/condition targets, but every new
record is explicitly a session simulation. In B/C/D/E and F-integrator, actual
fresh child contexts must do the registered work. A and F-main use no children;
G remains adaptive. Freeze all four distributed role instruction hashes for
adapter arms, while the narrower condition controls actual use. Record requested
models separately from unavailable resolved identities. Actual participation,
substantive work and reading/viewing require inspection of the original tool
outputs; hashes alone cannot establish them.

Capture tool outputs as work occurs. An exact export of a conversation's tool
request/response or completion notification is a `faithful_conversation_export`;
stdout captured directly by a wrapper may be `original_tool_output`. Identify the
actual tool in `source`, describe the capture boundary in `scope`, and set
`synthetic: false` only for real source output. A manually written summary belongs
in an execution audit, never in either tool-export category. Include actual agent
identifiers in spawn/completion exports. Retain prompts and final agent outputs
separately. Do not publish hidden reasoning, credentials or unrelated session data.

Dedicated subprocess browser tests may exercise owned task applications. Freeze
their browser/runtime provenance and capture conditions. These observations do
not establish access from the user's browser or from native Codex child tools.
Each cell's primary agent must actually view its final screenshots. Preserve
source snapshots, capture bytes, behavior logs and the corresponding view calls.

Keep every unsuccessful attempt and comparison defect. Completed execution is
independent of product success: a runnable comparator with broken behavior or
poor visual choices remains an observed result. Do not repair it in place after
review. Separately identify any continuation and retain both versions. Every
planned cell is either completed or listed under `unexecuted_cells`; omissions
cannot remove the matched A/B/C comparison, T4 F pair, G, or four task families.

## Review

A fresh product reviewer must be independent of all cell agents, their children
and the coordinator. Give the reviewer anonymous frozen products and matched task
requirements where feasible. Record actual blinding and its limitations; the
checker does not infer blinding from filenames. The reviewer views screenshots
for every completed product and records scoped strengths, defects and unknowns.
Negative comparator findings do not fail a mechanical acceptance threshold.

G products have a separate `final_runtime_acceptance` declaration identifying
their accepted scope, limitations and repair disposition. Retain any repair
evidence; an empty repair list needs an honest explanatory disposition. Final
acceptance may remain limited and does not assert universal aesthetic improvement.
The overall review's `accept_limited` is an agent judgment supporting the owner's
authorized release, not a human product-quality vote.

## Record shapes

All paths below are repository-relative. Every `REF` is
`{"path":"...","sha256":"<64 lowercase hexadecimal characters>"}` and must
identify retained, nonempty bytes. `EXPORT` is a REF with these additional fields:

```json
{
  "source": "actual tool or collaboration notification name",
  "scope": "what the exported request/response or stdout actually contains",
  "export_kind": "faithful_conversation_export",
  "synthetic": false
}
```

`original_tool_output` is the other allowed export kind. Images must retain PNG
bytes, not a path-only assertion. `VIEW` has `viewer_agent_id`, `screenshot` (REF),
and `view_export` (EXPORT). The screenshot must belong to the product being viewed.
The placeholders below describe a schema, not an executed experiment.

### Owner authorization (JSON artifact)

```json
{
  "schema_version": 1,
  "authority": "repository_owner",
  "source": "the actual user-message source in this conversation",
  "authorized_at": "<ISO-8601 timestamp with timezone>",
  "statement": "<exact user authorization, preserving its language>",
  "scope": "<authorized substitute and publication scope>",
  "authorized_actions": [
    "substitute_native_validation", "merge_pr_4",
    "tag_v1.20.0", "publish_v1.20.0"
  ]
}
```

### Frozen plan (JSON artifact)

Use `schema_version: 2`, `study_kind: "owner_authorized_session_simulation"`,
`candidate_source_identity`, `frozen_at`, `host_limitations`, `environment` (REF),
`baseline_method_files`, `candidate_method_files`, and `cells`.

The two method maps contain **every file** in their respective complete Skill,
mapping the Skill-relative path to SHA-256. Each cell contains:

| Field | Meaning |
| --- | --- |
| `id`, `task`, `condition` | Unique cell ID; T1–T4; original matrix target A/B/C/D/E-challenger/E-observer/F-main/F-integrator/G-final-runtime |
| `task_sha256` | Exact task instructions digest |
| `prompt` | REF to the exact prompt dispatched to the cell's primary agent |
| `input_artifacts` | Nonempty list of retained input snapshot REFs |
| `workspace_files` | Input workspace path → SHA-256 map |
| `starter_files` | Starter-relative path → SHA-256 map |
| `method_files` | Complete baseline method map for A–E; complete candidate map for F/G |
| `role_instruction_files` | Role name → current distributed TOML SHA-256; empty for A/B, all four roles for C–G |
| `main_model`, `subagent_model` | Host-requested model labels, including a truthful inherited/default label |
| `main_effort`, `subagent_effort` | Declared request/host policy; not authenticated resolved effort |
| `timeout_seconds`, `max_subagents` | Positive integer execution bounds |
| `tool_profile` | Frozen host/tool condition label, matched within paired comparisons |

All A/B/C controls match within each intended trio except the registered
intervention; the same applies to the T4 F pair. A shared environment artifact
records actual tool and browser/runtime details. At least one A/B/C trio, the T4
F pair, G and all four task families must complete under this limited route.

### Completed run (JSON artifact)

```json
{
  "schema_version": 2,
  "execution_kind": "real_session_agent",
  "simulation": true,
  "status": "completed",
  "cell_id": "<registered cell>",
  "candidate_source_identity": "<current candidate identity>",
  "registration_sha256": "<exact plan bytes digest>",
  "task_sha256": "<cell task digest>",
  "prompt_sha256": "<cell prompt REF digest>",
  "input_workspace_identity": "<workspace-map serialization digest>",
  "environment_sha256": "<plan environment REF digest>",
  "agent_id": "<actual primary agent ID>",
  "parent_agent_id": "<actual coordinator ID>",
  "fork_turns": "none",
  "started_at": "<timezone-qualified timestamp>",
  "completed_at": "<timezone-qualified timestamp>",
  "spawn": "EXPORT",
  "completion": "EXPORT",
  "tool_outputs": ["EXPORT"],
  "result": "REF",
  "children": [],
  "execution_audit": "REF",
  "product_evidence_index": "REF",
  "model_observation": {
    "main_requested": "<cell main_model>",
    "subagent_requested": "<cell subagent_model>",
    "main_resolved": null,
    "subagent_resolved": null,
    "scope": "<actual request evidence; resolved identities unavailable>"
  },
  "metrics": {
    "native_usage_tokens": null,
    "native_billing_cost": null,
    "main_context_pressure": null,
    "unavailable_reason": "<why these values are unavailable>"
  },
  "limitations": "<actual run-specific limitations>"
}
```

Compute `input_workspace_identity` exactly as the native runner does:
`sha256(json.dumps(cell["workspace_files"], sort_keys=True).encode()).hexdigest()`.
It is not the digest of an independently formatted JSON file. Timestamps must
place authorization before freeze, each run after freeze, and review after runs.

Each child has `agent_id`, `parent_agent_id` (the cell's primary agent),
`fork_turns: "none"`, `status: "completed"`, `role`, `prompt` (REF),
`spawn`/`completion` (EXPORT), `tool_outputs` (nonempty EXPORT list), `result` (REF),
`role_instruction_sha256` (the frozen role digest, null for generic),
`model_requested` (cell's `subagent_model`), and `model_resolved: null`.
Role labels describe the simulated instructions, never native bindings.

### Product evidence index (JSON artifact)

Use `schema_version: 1`, `cell_id`, `preview_command`, `capture_conditions`,
`source_files` (nonempty REF list), `screenshots` (nonempty PNG REF list),
`behavior_logs` (nonempty EXPORT list), and `viewed_screenshots` (nonempty VIEW list
whose viewer is the cell's primary agent). Failed behavior assertions are retained
and can support a negative finding; their exit status is not a quality threshold
in this consistency check.

### Independent review (JSON artifact)

The review is also an actual participant record: `agent_id`, `parent_agent_id`,
`fork_turns: "none"`, `status: "completed"`, `prompt` (REF), `spawn`/`completion`
(EXPORT), `tool_outputs` (nonempty EXPORT list), and `result` (REF to actual full
review output). Add these review-specific fields:

```json
{
  "schema_version": 1,
  "kind": "independent_product_review",
  "outcome": "accept_limited",
  "reviewed_at": "<timezone-qualified timestamp>",
  "condition_blind": true,
  "blinding_limitations": "<actual masking and any disclosure>",
  "scope": "<reviewed tasks and observation conditions>",
  "limitations": "<remaining unknowns>",
  "reviewed_products": [
    {
      "cell_id": "<completed cell>",
      "product_evidence_sha256": "<that run's product-index REF digest>",
      "findings": "<supported strengths, failures and unknowns>",
      "viewed_screenshots": ["VIEW"]
    }
  ],
  "final_runtime_acceptance": {
    "cell_ids": ["<all completed G cells>"],
    "disposition": "accepted_with_limits",
    "scope": "<accepted final-runtime behavior and UI scope>",
    "limitations": "<remaining quality and evidence limits>",
    "repair_disposition": "<repairs and verification, or why none is needed>",
    "repair_evidence": []
  }
}
```

Every completed product must appear once; each review VIEW identifies the
independent reviewer. `condition_blind` must report the actual state and may be
false with its limitation. `repair_evidence` holds REFs when repairs occurred.

### Release decision

Use these fields in `docs/evidence/v1.20.0/release-decision.json` only after review:

```json
{
  "schema_version": 2,
  "acceptance_route": "owner_authorized_session_simulation",
  "target_version": "1.20.0",
  "decision": "approve_limited",
  "baseline_commit": "05d0286b0b27e8e57d5751d5cf649c8800408001",
  "candidate_identity": "<exact reviewed source fingerprint>",
  "owner_authorization": "REF",
  "registered_plan": "REF",
  "run_records": ["REF"],
  "unexecuted_cells": {},
  "reviewer": "<independent review agent_id>",
  "reviewed_at": "<same timestamp as the independent review>",
  "review_report": "REF",
  "scope": "<limited acceptance scope>",
  "limitations": "<native campaign gaps and bounded product findings>",
  "native_claims": {
    "native_codex_role_binding": false,
    "registered_native_model_trials": false,
    "native_usage_metrics": false,
    "native_cloud_campaign": false
  },
  "engineering_checks": []
}
```

Each engineering-check row has `name`, `status: "passed"`,
`candidate_source_identity` and `log` (REF). Required names remain
`upstream_unit_suite`, `package_validation`, `catalog`, `readme_art`,
`browser_scenarios`, `installer_smoke`, and `package_build`.

Run `python tools/check_adaptive_release.py` on the exact final checkout. The
result states **limited session evidence consistency**, not native validation or
visual-quality certification. Inspect original evidence independently, update
release disclosures, then use the existing publication workflow and asset
readback checks. Preserve historical tags, old media, native failures and the
original native study's incomplete status.
