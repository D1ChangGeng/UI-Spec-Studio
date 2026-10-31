# Independent code-review fixes during the v1.20.0 continuation

Observed on 2026-11-01 Asia/Tokyo. These are engineering corrections, not completed UI research experiments or a release approval.

## Independent findings and corrections

The Codex GitHub code reviewer examined PR #4 and reported three concrete findings in review `5723700026` against `541766cf6fdc8ec19e5ad5c3c952024d11c444f5`:

1. **P1: run records were not bound to the exact frozen registration.** A matching cell name and task hash could cause an old execution to count after models, starters or runtime inputs changed. The guard now requires the run's `registration_sha256` to match the supplied registration's actual bytes, validates its declared workspace hash map, and compares `input_workspace_identity` using the runner's existing exact serialization. Missing and mismatched identities fail closed.
2. **P1: a final-runtime cell could use older role instructions.** The guard now requires exactly the four distributed role registrations and matches each installed `.codex/agents/<role>.toml` hash to the current adapter's actual bytes. Candidate Skill identity alone no longer proves final adapter identity.
3. **P2: cancellation could leave the model process running and no attempt record.** Keyboard interruption now triggers bounded owned-process-tree/group cleanup, reaps the direct child, preserves logs and output snapshot (or its capture failure), records `interrupted` without a completed Agent-run claim, and then returns CLI exit code 130. A second Ctrl-C is deferred while cleanup and finalization run. POSIX descendants are also sent SIGKILL if the leader has already exited; Windows uses the existing explicit task-tree termination path.

The fixes do not change the professional Skill, source-reuse rules, four-role installation policy, models, required experiment arms or human visual-review requirements. The release decision remains pending.

## Regression evidence

The newly added regression cases reproduced the findings before the implementation was changed: the targeted test file reported 10 failures and one error. After the fixes and additional OS-cancellation coverage, all **69 targeted tests** passed. The full clean-interpreter suite then passed **456 tests** (442 existing tests plus 14 added cases).

The real SIGINT test starts a sleeping Python process and interrupts its supervising runner, checks exit 130, a reaped child, a preserved attempt record and output index. This is an operating-system mechanics test, **not** a Codex/model/GUI experiment. Other new process doubles remain explicitly labeled synthetic unit fixtures. The fixture records are not release evidence.

Local logs are retained in the continuation evidence bundle with these SHA-256 identities:

| Log | SHA-256 |
| --- | --- |
| review-regressions-before.log | cfbea56e456e5dc3f1bec2268cf214cf130193c3e2634369d99b60af2b3a42c0 |
| review-regressions-after.log | 7874ac7050e4da1c91b9f5ab2634cb8fb0b58ff228455e96e5ebec885dc59b7f |
| unit-tests-after-review.log | 2c62b98b3ae37d438a080fcf9a5a0a4e8981605d63ae757abedb7fd74932f0e1 |

Exact changed source blob identities are `eb5ea826bf49e9e2213aa829b51101b129bc9cee` (release guard), `c3090089dd5ed5f61e458d78c148c10ee87890db` (runner) and `b4038c4873acde387c95946c6c997ed69d4eeb65` (tests). Subsequent hosted CI must validate the committed tree; these local observations do not pre-assert its result.

## Delivery and execution preflight

For the earlier `5a21ac201bdce6541b1dbf499fd18e3846049b6b` candidate, recovery run `41219410490` succeeded, including immutable-commit remote installation and live GitHub README rendering. Its runtime-availability artifact `13049611092` (archive SHA-256 `5b67f88ef4fa1a0300ab0cb3155c094a4f9c2f1bd36ea0e99e1ae6c49bef6acc`) reports no Codex executable and no configured `OPENAI_API_KEY` or `CODEX_API_KEY` reference. No credential values were read into the report and no model was invoked.

The separate arbitrary Codex Cloud task still needs a repository environment. A successful GitHub code review does not supply that execution environment and does not establish the real matched UI campaign. Preserve this distinction, the historical metadata-only evidence, and the pending final product-quality review.
