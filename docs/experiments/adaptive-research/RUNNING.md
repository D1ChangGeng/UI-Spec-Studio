# Running the prepared study tools

The scripts do not perform any work until invoked. They do not provide model credentials or a graphical environment. Preserve the original baseline and candidate in separate worktrees. Follow PROTOCOL.md before using real account credits.

For the owner's authorized session substitute, follow
[SESSION-SIMULATION.md](SESSION-SIMULATION.md) instead of invoking this native
runner. Its schema-v2 records retain genuine collaboration calls and task tool
outputs, with explicit export provenance. Do not convert them into native events
or set the native runner's simulation flag to false. The original schema-v1
publication path and its runtime checks continue to apply to native claims.

Prepare four real starter directories as described in the protocol; T4 needs a settled mature-resource decision. Edit `plan.example.json` into a separate plan using models actually available to the experiment account, matched budgets and a registered order. Do not use model aliases unsupported by the host.

Set each cell's `network_access` to a real boolean. It defaults to `false`; authorized public-source research can set it to `true`, which is passed explicitly as `sandbox_workspace_write.network_access` while retaining the workspace sandbox. Match it across paired conditions and verify actual connectivity before freezing the campaign. Network permission does not supply credentials, authorize account changes or establish that a resource is reachable.

```bash
python tools/run_adaptive_research.py prepare \
  --baseline-skill /path/to/baseline/skills/ui-spec \
  --candidate-skill /path/to/candidate/skills/ui-spec \
  --starters /path/to/reviewed-starters \
  --plan /path/to/reviewed-plan.json \
  --output /path/to/new-study

# Read-only execution preflight; no model call.
python tools/run_adaptive_research.py run --study /path/to/new-study \
  --cell T2-C-r1 --codex-home /path/to/provisioned-experiment-home

# Explicit paid/plan-usage execution. Uses normal permissions, never --yolo.
python tools/run_adaptive_research.py run --study /path/to/new-study \
  --cell T2-C-r1 --codex-home /path/to/provisioned-experiment-home \
  --execute --acknowledge-cost
```

A `process_completed` record establishes only the captured native execution. Check research participation, visual observation and product output independently. A role invocation is not a quality finding, and no record is automatically a release approval.

When the host requires its existing authenticated environment to remain unchanged, explicitly select `--inherit-profile` instead of `--codex-home`:

```bash
python tools/run_adaptive_research.py run --study /path/to/new-study \
  --cell T2-C-r1 --inherit-profile --execute --acknowledge-cost
```

This mode does not set or replace `CODEX_HOME`. The default `exec` transport passes `--ignore-user-config` to Codex, keeps `workspace-write`, and places runtime state/logs under this attempt's directory. Its runs use `--ephemeral`; retained stdout/stderr provide the execution record. Installed role files are registered explicitly for that invocation through native `agents.<name>.config_file` and description settings, and multi-agent conditions enable the native feature. The runner does not infer role selection merely from these declarations.

The inherited mode records the existing profile's non-secret config hash and known instruction identities. It does not claim an empty profile: authentication, host-provided tools, skills and other inherited instructions require actual-run review. Match this mode and its observed inheritance across paired cells. If the outer execution host requires separate sandbox approval to contact the authenticated service, obtain it through that host while keeping the child CLI's declared sandbox; the runner cannot grant it. Do not publish raw runtime state or profile contents. If the host cannot select custom roles, record the run as incompatible with the specialist condition; do not emulate native discovery by manually injecting the role text into a generic child.

When Codex is installed outside `PATH`, pass its verified absolute path with `--codex-executable /path/to/codex`. Missing or non-executable paths remain blocked preflights.

## Native child evidence through app-server

The tested Codex `0.166.0-alpha.1` CLI `exec --json` stream includes parent collaboration events but omits the selected child's native role metadata and detailed child tool history. Those events alone cannot authenticate the B/C/D/E/F delegated interventions. For a host exposing the standard app-server protocol, freeze these additional fields in every paired cell before preparation:

```json
{
  "transport": "app-server",
  "profile_mode": "inherited",
  "session_persistence": "ephemeral",
  "network_access": true
}
```

Use the same `run --inherit-profile --execute --acknowledge-cost` command. The app-server transport uses the existing authenticated profile because that interface does not expose `exec`'s `--ignore-user-config` option. Its known configuration hash, inherited instructions and process-scoped overrides are recorded. It never rewrites that profile, reads credentials, enables internal raw events or grants an approval on the user's behalf. The frozen execution policy is `workspaceWrite` with the stated network boolean, `on-request` approval and the host's native `auto_review` reviewer. An unresolved client approval, missing capability, denied tool or incomplete required lifecycle is retained as an unsuccessful attempt.

The B arm must additionally freeze `generic_role_binding` to the actually observed native representation of the default role: `null` on the tested runtime, or `"default"` on a host that reports that value. An absent metadata field is not equivalent to an observed null. A/C/D/E/F/G cannot acquire a role binding from the participant's prose or the installer receipt.

Listen before creating the new parent thread. Retain standard original JSON-RPC lines, parent/child thread metadata, actual tool lifecycles, terminal turns and native per-thread usage. Bind them to the exact registration, task and workspace identity. Safe original lines are `appserver/wire.jsonl`; every received line has a sequence/hash entry in `wire-index.jsonl`. Reasoning content is omitted. Mixed envelopes that require removal are separately labeled derived projections and cannot stand in for original native evidence. Do not publish runtime state, account notifications or profile directories.

On the tested version, ephemeral child threads cannot be resumed or paged for historical items. Their evidence must therefore be complete in the live standard stream; the runner does not claim later history recovery. An explicitly registered `session_persistence: "persistent"` additionally uses supported public pagination and leaves normal session persistence to the native runtime. Do not switch persistence modes after registration or mix them within a controlled pair. If a different host cannot supply the needed standard stream or metadata, record incompatibility instead of synthesizing child events.

Native `agentRole` and parent lineage prove the selected role, while completed child work-tool items prove actual tool use. The execution audit must still assess whether that work addressed the registered intervention. Requested models, configured thread models and any creation-time resolved model metadata are distinct fields; per-response model identity remains unknown when unavailable. Per-thread token totals are retained without treating the parent total as the multi-agent total. No billing request or token-to-dollar estimate is made by this transport.

Each run has a fresh workspace and a non-overwritten `runs/<cell>/` attempt. A frozen task/role/Skill mutation blocks execution. Archives contain public app/evidence files only; unsupported/private assets are reported as exclusions. Review raw logs for secrets before copying them into the repository. The maintainer must rebase relative artifact paths to repository paths during evidence promotion, preserving bytes and updating the index rather than rewriting raw logs.

To finish acceptance, run all existing tests and browser/publication suites, obtain independent review, and explicitly complete `docs/evidence/v1.20.0/release-decision.json` with actual artifact paths and hashes. Run `python tools/check_adaptive_release.py`. This verifies consistency, not professional merit. The existing publish command is blocked while the decision is pending; do not bypass the guard to publish an untested candidate.
