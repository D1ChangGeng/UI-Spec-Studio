# Optional Codex adapter — v1.20.0

This is an optional host adapter, not a replacement for `ui-spec`. Install the complete Skill first through your established Skills workflow. The main agent and substantive specialist work retain its eight-reference reading contract. Models and permissions come from the actual host; a role file cannot create a sandbox, a browser, a login or a separate desktop.

## Install without overwriting personal work

Use Python 3.11+ when the target already has user configuration, so the standard-library TOML parser can validate a safe merge. Python 3.10 supports a fresh configuration and unchanged installer-owned registrations. From the repository or this standalone adapter directory:

```bash
python integrations/codex/install.py install --project /path/to/product --dry-run
python integrations/codex/install.py install --project /path/to/product
```

From inside `integrations/codex`, use `python install.py ...`. On Windows, `py -3 install.py ...` uses the selected Python interpreter. Install in the environment that actually runs Codex: WSL and Windows have separate home/configuration locations. `--user` explicitly targets `CODEX_HOME` (or `~/.codex`); it is never selected implicitly.

An explicit `install` command installs **all four roles by default**: `ui_researcher`, `ui_integrator`, `ui_challenger` and `ui_experience_observer`. It registers their paths and descriptions through four native `[agents.<name>]` entries in a clearly marked, owned block in `config.toml`. The dry-run report includes that configuration change. Existing settings, model choices and permissions remain intact. The latter two roles remain **on-demand for actual delegation**, not opt-in for installation; installation alone never invokes a role or establishes an experimentally proven benefit. Legacy `--with-optional` is accepted as a no-op for earlier candidate commands. The installer does not change `AGENTS.md` or Skill knowledge. Review `AGENTS-snippet.md` and merge its meaning into existing project instructions without replacing them.

```bash
python integrations/codex/install.py status --project /path/to/product
python integrations/codex/install.py install --project /path/to/product --upgrade
python integrations/codex/install.py uninstall --project /path/to/product
```

Managed upgrades require existing installed bytes to match the prior ownership receipt. Manual edits and unrelated same-named files are conflicts, not permission to overwrite. An identical pre-existing unowned role remains unowned and is not removed on uninstall. Uninstall removes only still-matching owned files. Modified files are retained and reported. Dry runs do not create directories. Installation has an exclusive local lock and rolls back its own partial writes on operational failure; this is file protection, not an Agent workflow.

Configuration ownership covers only the marked registration block. Reinstallation, upgrades and uninstall preserve user edits outside that block byte for byte. Existing same-named registrations are conflicts. If the managed block was edited, uninstall preserves the block and its referenced roles for review. An earlier two-role or four-file-only installation can add the registrations without replacing its other configuration. The installer does not change project trust or enable a disabled multi-agent capability; use the host's normal settings and a trusted consumer project.

Rollback uses a previously archived adapter with `--upgrade --allow-downgrade`, after reviewing the report. It still refuses user-modified files. Roles no longer selected are not silently removed; uninstall explicitly and reinstall the intended set.

## Launch with installed native roles

Some hosts do not load the project's native role registrations even when the files are installed correctly. The optional launcher registers the four installed role paths through Codex's `agents.<name>.config_file` command-line settings for the current invocation. It requires Python 3.11+ and an installed Codex executable. It enables `multi_agent` and `agents.enabled` for that invocation. It does not write the profile, change project trust, select a model, set sandbox permissions or configure network access.

```bash
python integrations/codex/launch.py --project /path/to/product
python integrations/codex/launch.py --project /path/to/product --dry-run -- exec --ephemeral "Use ui-spec. Inspect the current project."
python integrations/codex/launch.py --project /path/to/product --codex-executable /path/to/codex -- exec --ephemeral "Use ui-spec. Inspect the current project."
```

The first command opens Codex in the selected project. `--user` instead reads the four roles from the same user scope as the installer and runs Codex in the current directory. Arguments after `--` pass directly to Codex as an argument array. Standard input, output, errors, environment and authentication stay with the child process. Terminal Ctrl-C reaches Codex, and the launcher returns its exit status. `--dry-run` prints only the exact argument array as JSON; it neither starts Codex nor creates files.

All four installed roles must have their expected identity and nonempty description and instructions. The launcher accepts the distributed role contract: `name`, `description`, `developer_instructions`. Other TOML keys are rejected without modifying the file; use normal Codex settings and options for model and permission choices. Missing roles, malformed files, symlinked role paths or ancestors and unsafe path components are rejected. Forwarded `--cd`/`-C`, overrides of these four role registrations and settings that disable the required multi-agent capability are also rejected. Select the working directory with the launcher's scope options.

Registration does not add a custom-role selector to a host or model interface that lacks one. The current runtime probe verified explicit registration with Codex CLI `0.166.0-alpha.1` and a main model exposing the v1 native agent selector. The tested 6.x/v2 interface exposed generic child creation without that selector. Use a supported host/model combination and confirm the actual role binding; the launcher does not choose an experimental model or promise support for every host.

## Use natural delegation

Ask the main agent to investigate the important unresolved relationship, for example:

> Use ui-spec. Ask an independent researcher to investigate mature composer-and-reading-space implementations. Inspect actual growth, attachment and scrolling behavior and return strong candidates, viewed evidence, adoptable sources and significant unknowns. Keep the final product decision and integrated visual review in the main thread.

For integration, identify the selected source/variant, protected visual relationships, permitted modules, data/state contracts and actual checks. This is not permission to invent unspecified layout or motion.

## Verify the actual runtime

`python integrations/codex/doctor.py --project /path/to/product` performs only local environment/file checks and `codex --version` when available. It does not spawn an agent, test credentials, certify tool inheritance or verify model access. Perform a real scoped natural delegation and inspect the host thread, source reads, accessible browser evidence and returned findings before claiming runtime compatibility.

For the checked configuration contract, consult the official sources in `MODEL-POLICY.md`. Current role TOML uses `name`, `description`, `developer_instructions`; it intentionally does not set a model. Optional model preferences remain experiments, not product defaults.

Native custom-role selection depends on the host's exposed orchestration interface. Some model/tool combinations expose subagent creation without a custom-role selector. Confirm that the desired role is actually selected before counting that run as a specialist; giving a generic child the role name is insufficient. Hosts that require the `multi_agent` feature can enable it through their normal configuration or the documented `--enable multi_agent` launch option. The study runner registers exact role paths per invocation and preserves ephemeral CLI sessions; observed host/version/model combinations belong in the version's runtime evidence.

Consult the version review and adaptive-research study records for the exact environments, executions and observed limits. Native role discovery, comparative model results and UI quality each require their own evidence; installer tests establish only the exercised file lifecycle.
