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
