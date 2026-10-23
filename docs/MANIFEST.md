# Optional coverage manifest

Use the project's existing test matrix when it already records equivalent facts. This format is a lightweight alternative supported by the bundled checker.

## Run

```bash
python <skill-dir>/scripts/prepare.py --project-root /path/to/project
python <skill-dir>/scripts/check_manifest.py --project-root /path/to/project --mode draft --json
python <skill-dir>/scripts/check_manifest.py --project-root /path/to/project --mode review
python <skill-dir>/scripts/check_manifest.py --project-root /path/to/project --mode finish
```

The manifest defaults to `.ui-spec/manifest.json`. `--manifest path/from/project.json` selects another local file. `prepare.py` creates missing records and preserves existing ones.

## Fields

| Field | Purpose |
|---|---|
| `schema_version` | `1` |
| `project`, `phase` | Project label and current intent: init, shape, iterate, audit or finish |
| `revision` | Exact current implementation/test reference, such as a Git commit or scoped digest |
| `design_revision` | Accepted design reference used by finish; may differ from connected implementation revision |
| `design_system_path` | Existing nonempty project-local design record, or null |
| `viewports` | Unique IDs with actual CSS `width` and `height` |
| `variants` | Unique IDs with supported `locale` and `theme`; use `default` when appropriate |
| `routes` | Page families with ID, path, purpose, primary state, all declared states and critical states |
| `journeys` | User-task IDs, participating route IDs and an observable outcome |
| `requirements` | Additional exact route/state/viewport/variant combinations |
| `checks` | One current result per check target, including actual evidence where executed |
| `approvals` | Scope-specific design approvals with a source reference |
| `connections` | Trusted behavior owners, real data modes and passing integration checks |
| `exceptions` | Explicit, scoped waivers with reason and approver/reference |

Identifiers use lowercase letters, digits, underscores and hyphens, up to 80 characters, beginning with a letter or digit. Route records represent page families; dynamic item IDs are sampled by content/permission characteristics, documented in the route or brief.

See the complete [planned example](../examples/manifest.json). It deliberately starts with planned work and contains no claim of executed visual or product verification.

`phase` is the active operation. Approval, connection and individual check records
carry scope maturity. Use existing project records when they express these facts
adequately. Keep the complete route inventory in its authoritative location and
state the selected matrix scope explicitly for round reviews. A full acceptance
review reconciles all in-scope routes and their coverage.

## Coverage rules

1. Each route's primary state requires a visual check for **every declared viewport × variant**.
2. Each additional critical state requires a visual check in **every variant**, at one declared viewport minimum. Add exact viewport cases under `requirements` where risk warrants them.
3. Each journey requires a completed journey check in **every declared variant**.
4. `finish` additionally requires a recorded design approval covering every selected route and a passing real integration check for each route, linked from `connections`.

A source route, role or variant omitted from the manifest is outside what this checker can discover. Reconcile the inventory with the real project during audit. An empty route inventory can be a draft but cannot pass review or finish.

## Check records

A visual check:

```json
{
  "id": "collection-ready-desktop",
  "kind": "visual",
  "route": "collection",
  "state": "ready",
  "viewport": "desktop",
  "variant": "en-light",
  "status": "planned"
}
```

After actual execution, set `status` to `pass`, record the current `revision`, the person/agent that inspected it under `reviewer`, `inspected: true`, and `evidence: [".ui-spec/evidence/collection-desktop.png"]`. The path must reference an existing nonempty file inside the project. Record environment and fixture details in the review record or additional fields.

A journey check uses `kind: "journey"`, `journey: "browse"` and `variant`. A passing result also needs current revision, evidence, reviewer and observed `outcome`.

An integration check uses `kind: "integration"`, `route`, current revision, evidence, reviewer, observed `outcome` and a `data_mode` of `service`, `local` or `static`. This declares the architecture actually exercised. Fixture-only behavior is a design test rather than a completed integration.

Each declared target has one current check record. Put retest history in Git or existing evidence logs; update the record to the current result.

## Status and modes

`planned` means awaiting execution. `pass` records an executed check. `fail` and `blocked` require a reason. `waived` requires a matching explicit exception.

- **draft** validates record integrity and reports pending coverage. Existing pass claims still require valid evidence references.
- **review** additionally requires completed declared coverage and resolves open failed/blocked checks.
- **finish** additionally requires scoped approval, actual connection records and passing integration evidence.

Waivers are recorded decisions, not successful tests. An exception has `target`, `reason`, `approved_by` and `reference`. Targets are `visual:route:state:viewport:variant` or `journey:journey:variant`; a waived check matches its target. Critical-state coverage derives from a completed exact visual case. Real integration remains a finish requirement even when a separate observation has an approved exception.

## Approval and connection example

```json
{
  "approvals": [{
    "routes": ["collection"],
    "revision": "accepted-spec-reference",
    "by": "product-owner",
    "reference": "Review record identifying the accepted collection screen"
  }],
  "connections": [{
    "route": "collection",
    "mode": "service",
    "owner": "Existing application API",
    "contract": "api/collection-contract.md",
    "check_ids": ["collection-live"]
  }]
}
```

The approval revision matches `design_revision`, while executed checks match `revision`. This distinguishes the approved design from the connected implementation. Store genuine approvals already supplied by the user; the checker cannot establish identity or consent.

## Evidence handling and limits

Evidence paths are project-relative and resolved within the project. External evidence stores can be represented by a local, sanitized review record containing the authorized reference. Evidence content remains the reviewer's responsibility.

The checker accepts file references, not pixels. It verifies existence and declared status; it does not parse screenshots, run browser operations, inspect service transactions, authenticate approvals or independently verify a Git claim. Its output explicitly carries this boundary.

Exit codes: `0` for the selected record checks passing, `1` for invalid/pending requirements, `2` for an invocation or file-reading problem.
