# UI Spec Studio maintainer contract

This repository distributes the `ui-spec` skill from `skills/ui-spec/`. Runtime
instructions are English; user-facing introductions include English and Chinese.

Read `docs/MODEL.md` and `docs/WRITING.md` for the accepted design and writing
standards. Six common references form the complete professional foundation;
integration is required for real behavior work. Shape stays optional. Preserve
agent initiative, scoped approval and the Skill/host responsibility boundary.

Keep detailed rules at their responsible source. Prefer task-oriented reasoning,
clear causal explanations and final-state language. Project-specific design
choices remain in the consuming project. Keep supplied references and external
material distinct from active instructions.

Validate the exact source before release:

```bash
python tools/validate_package.py
python -m unittest discover -s tests -v
python tools/package.py
```

Optional tools use Python 3.10+ and the standard library. Structural tests and
installation checks establish their exercised mechanics. Report real-browser,
agent-behavior and service-integration evidence separately. Use logical scenario
review to inspect workflow coherence; comparative model campaigns are optional.

Update VERSION, skill metadata, release notes and installation examples together.
Publish the reviewed commit and read back tag, release and artifact checksums.
Preserve unrelated user changes and public release tags. Private project data
belongs outside source examples and distribution assets.

Version 1.2 develops meaning-to-form reasoning, conditional techniques and editable
screen-based artifacts. README is a designed product surface; preserve its native
text and installation path, theme/narrow assets and documented render conditions.
Run `python tools/readme_art.py --check` to verify its generated artwork. Browser
preview dependencies and checks are documented in docs/design/README-SPEC.md.

Version 1.3 connects proactive ecosystem discovery with assessment, reuse depth,
adaptation and project verification. `assets/resource-catalog.json` inside the
skill is the maintained discovery data; `tools/catalog_docs.py` generates its
readable map. Preserve original observation dates and evidence scope. Run
`python tools/catalog_docs.py --check` with the existing release checks.

Version 1.4 grounds the design in user-recognizable product models. Preserve
functional contracts and evaluate visual candidates against the target. Keep
product conventions and engineering sources distinct in the visible decision
record. Material unresolved directions receive focused user choice; explicit
one-shot/delegated work retains its actual approval scope. Run the authored
browser study with `python tools/validate_scenario.py --output-dir scenario-evidence`.
The study validates its own fixture, not the user's private application or all models.
