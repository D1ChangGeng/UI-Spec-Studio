# Running the prepared study tools

The scripts do not perform any work until invoked. They do not provide model credentials or a graphical environment. Preserve the original baseline and candidate in separate worktrees. Follow PROTOCOL.md before using real account credits.

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

A `process_completed` record is only a real parent-session completion. Check native child session identities, tools, visual evidence and product output independently. Actual subagent use and total child costs are deliberately not inferred. No record is automatically a release approval.

When the host requires its existing authenticated environment to remain unchanged, explicitly select `--inherit-profile` instead of `--codex-home`:

```bash
python tools/run_adaptive_research.py run --study /path/to/new-study \
  --cell T2-C-r1 --inherit-profile --execute --acknowledge-cost
```

This mode does not set or replace `CODEX_HOME`. It passes `--ignore-user-config` to Codex, keeps `workspace-write`, and places runtime state/logs under this attempt's directory. Every run uses `--ephemeral`; raw stdout/stderr and the study artifacts provide the retained record. Installed role files are registered explicitly for that invocation through native `agents.<name>.config_file` and description settings, and multi-agent conditions enable the native feature. The runner does not infer role selection merely from these declarations.

The inherited mode records the existing profile's non-secret config hash and known instruction identities. It does not claim an empty profile: authentication, host-provided tools, skills and other inherited instructions require actual-run review. Match this mode and its observed inheritance across paired cells. If the outer execution host requires separate sandbox approval to contact the authenticated service, obtain it through that host while keeping the child CLI's declared sandbox; the runner cannot grant it. Do not publish raw runtime state or profile contents. If the host cannot select custom roles, record the run as incompatible with the specialist condition; do not emulate native discovery by manually injecting the role text into a generic child.

When Codex is installed outside `PATH`, pass its verified absolute path with `--codex-executable /path/to/codex`. Missing or non-executable paths remain blocked preflights.

Each run has a fresh workspace and a non-overwritten `runs/<cell>/` attempt. A frozen task/role/Skill mutation blocks execution. Archives contain public app/evidence files only; unsupported/private assets are reported as exclusions. Review raw logs for secrets before copying them into the repository. The maintainer must rebase relative artifact paths to repository paths during evidence promotion, preserving bytes and updating the index rather than rewriting raw logs.

To finish acceptance, run all existing tests and browser/publication suites, obtain independent review, and explicitly complete `docs/evidence/v1.20.0/release-decision.json` with actual artifact paths and hashes. Run `python tools/check_adaptive_release.py`. This verifies consistency, not professional merit. The existing publish command is blocked while the decision is pending; do not bypass the guard to publish an untested candidate.
