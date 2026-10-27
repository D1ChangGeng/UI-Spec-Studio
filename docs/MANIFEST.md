# Optional declared coverage manifest

Use existing project test and design records where they already express these
facts. The optional manifest groups named pages, variants, states, journeys,
check records, approvals, connections and exceptions. The inspector reports
**what is recorded**, not whether the product's scope or design is complete.

## Run and choose a query view

```bash
python <skill-dir>/scripts/prepare.py --project-root /path/to/project
python <skill-dir>/scripts/check_manifest.py --project-root /path/to/project --view overview --json
python <skill-dir>/scripts/check_manifest.py --project-root /path/to/project --view checks --json
python <skill-dir>/scripts/check_manifest.py --project-root /path/to/project --view connections --json
```

`--manifest path/from/project.json` selects another project-local record.
`--view` changes presentation only. The earlier `--mode draft`, `review` and
`finish` arguments remain compatibility aliases for overview, checks and
connections, respectively. They impose no stage-completion requirements,
authenticate no approvals and do not decide whether work can proceed.

The report uses `record_readability` separately from `structural_findings`.
It has no aggregate `ok`, `satisfied` or design pass/fail. Exit 0 means a readable
record was inspected, **including one with structural findings**. Exit 2 means
an invocation/read problem. Console output says `Structure inspection completed`,
which describes the tool operation only. JSON integrations must inspect the
specific observations they need, not use the exit status as a project gate.

## Fields and origins

| Field | Recorded meaning |
|---|---|
| `schema_version` | Integer `1`; the input profile remains readable across the output migration |
| `record_origin`, `initialization` | Template or initialized/unconfirmed origin and detected local references |
| `project`, `phase` | Project label and the Agent's current work intent, not tool-assigned state |
| `revision` | Optional snapshot/source identifier; no global freshness policy |
| `design_revision` | Identity of a design whose actual approval remains separate |
| `design_system_path` | Local record reference; file existence says nothing about acceptance |
| `viewports` | IDs and declared CSS dimensions, not inferred device requirements |
| `variants` | IDs with declared locale/theme conditions |
| `routes` | IDs, path, purpose, primary/state/critical labels chosen by the Agent |
| `journeys` | IDs, route references and intended outcome |
| `requirements` | Explicit target addresses the project author chose to list |
| `checks` | Individual declared statuses, evidence locations, reviewer and observed findings |
| `approvals` | Declared design decisions with their scope/source, not authenticated by this tool |
| `connections` | Declared owners/contracts/data modes and references to check records |
| `exceptions` | Declared scope changes with reason, approver/source; not successful verification |

The [planned example](../examples/manifest.json) illustrates data shape, not an
executed project. Identifiers in this profile use lowercase letters, digits,
underscores and hyphens, up to 80 characters. Record shape observations do not
create UI design obligations.

`prepare.py` creates missing ordinary records and preserves existing files.
It leaves viewports, variants, routes, journeys, checks, approvals and connections
empty; it does not silently assume English, light theme or a desktop viewport.
A discovered DESIGN.md is labelled file-detected/content-and-approval-uninspected.
The project label can come from an argument or directory name; that is not
product research. The origin remains `initialized_unconfirmed` until the Agent
establishes the real scope. Preparation never creates a design-evidence map.

## Declared items versus inventory projections

`declared_item_records` matches **explicit requirements** to addressed check and
exception records. `unlisted_declared_items` lists explicit targets with neither
kind of record. Matching only asks whether the literal target is represented.
A planned/failed/blocked check is a record; it is not a successful result.

`inventory_combinations` separately projects the declared route primary state
across named viewports/variants, critical states across named variants, journeys
across named variants, and integration addresses for named routes. These are
**inventory combinations, not automatic coverage requirements**. Its `unlisted`
list is a structural description; task applicability remains unassessed. The
Agent chooses which additional combinations deserve explicit requirements.

Pages, user roles, devices or tasks omitted from the inventory cannot be discovered
by these combinations. An empty list is readable in every view. Coverage discovery
through actual user tasks and mature products remains Agent work; no completion
percentage can prove that unknown scope is complete.

## Results, exceptions and absence remain separate

`declared_check_records` contains non-waived records with their **declared**
statuses. `declared_waived_check_records` lists waived checks.
`declared_exceptions` retains their separate authorizations. No union of these
collections is named satisfied or treated as verification success.

For example, a visual record may contain:

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

After actually running and viewing a scoped check, its author can record pass/fail,
source identity, reviewer, inspected flag, evidence, content and environment.
The inspector reports those fields and file metadata without inferring that the
browser ran, pixels were viewed or the finding is professionally sound.

A journey record uses `kind: journey`, a journey ID and variant. Integration uses
`kind: integration`, a route and the exercised service/local/static boundary.
Actual successful persistence, truthful responses and appropriate recovery must
be demonstrated by their independent tests. A filename or a connection record
does not prove them. A `fail` result remains recorded even in the connections view.

Several check records can address the same target across meaningful revisions.
Unique check IDs distinguish them; no tool automatically selects the newest or
rewrites old results. Keep the current model and concise revisions clear, and
move full histories into linked evidence when they would obscure ongoing work.

## Approval and connection records

```json
{
  "approvals": [{
    "routes": ["collection"],
    "revision": "accepted-design-reference",
    "by": "product-owner",
    "reference": "Actual review identifying the accepted screen and scope"
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

References are mechanically resolved. Whether the linked check supports the
connection, the approval is genuine, or the actual behavior is sufficient is a
separate review. `phase: finish` describes the author's intent, not permission
to release or a tool-certified finish. Changing the global revision does not
invalidate all visual history. The Agent reviews actual changed objects and
conditions and either carries applicable results forward explicitly or rechecks.

## Local files and independent assertions

Local file paths remain inside the project and never traverse symlinks. A missing
file, directory reference or unreadable path is a direct structural observation.
An empty regular file is reported with zero bytes, without inventing its content.
Remote material can be linked by a sanitized local source record; the inspector
does not fetch external resources or authenticate any record's authority.

Independent byte, package, browser and runtime checks keep scoped match/fail
results for what they actually test. See [the structural boundary guide](STRUCTURAL-INSPECTION.md)
for the four responsibilities and migration. Structural inspection, Agent
behavior, engineering verification and final UI acceptance retain separate evidence.
