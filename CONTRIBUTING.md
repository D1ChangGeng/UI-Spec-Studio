# Contributing

Read [the model](docs/MODEL.md) and [writing standard](docs/WRITING.md). Prefer a
focused change that improves a real design decision, user journey or tooling
boundary. Describe its intended scope and preserve unrelated behavior.

Runtime references use clear English and remain self-contained inside the skill.
Keep user-facing English and Chinese introductions aligned. Component catalogs
are open research starting points; verify the particular source when recommending
an implementation. Preserve applicable notices for any reused material.

Run the package validator, unit tests and reproducible build listed in README.
Add regression tests for changed helper behavior. Document logical scenarios for
changed workflow rules; distinguish expected reasoning from executed agent runs.
Actual UI acceptance belongs to the consuming project's browser/task evidence.

Pull requests should state the change, relevant evidence, compatibility impact and
remaining checks. The release workflow tests Python/platform combinations and
Skills CLI installation. Maintainers review the exact source and version before
publication. See [publishing](docs/PUBLISHING.md).

For publication changes, maintain native readable text and the bilingual reading
path. Regenerate SVG from `tools/readme_art.py`, run its check and inspect browser
captures using the optional preview requirements. Keep the current GitHub rendering
and local approximation distinct in evidence. Add reusable professional methods
with conditions, editable realization and observational limits.
