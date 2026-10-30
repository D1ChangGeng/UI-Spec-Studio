# Common execution environment

Read TASK.md and the supplied skill at ui-spec/SKILL.md, including its applicable
reference-reading contract. Implement in app/. Keep source/evidence notes in this
workspace. Work only in this assigned workspace; unrelated work is not
task context. Do not subdelegate this task or publish external changes.

## Runtime and browser

- Python browser tooling: /tmp/ui-spec-study-venv/bin/python
- Python packages: playwright 1.57.0, markdown-it-py 4.0.0
- Chrome for Testing: /tmp/ui-spec-study-browsers/chrome-linux64/chrome
- Actual available Chrome version: 156.0.8078.80
- Local browser launch needs exec_command sandbox_permissions=require_escalated:
  the ordinary sandbox rejects its process socket. This exception is for local
  test browser execution; normal project edits remain in the workspace.
- Launch Playwright with executable_path set to the path above, headless=True
  and args=['--no-sandbox']. It was smoke-tested for DOM interaction and screenshots.
- Start a local server on the port assigned in RUN.md. For vanilla applications,
  python -m http.server PORT --bind 127.0.0.1 --directory app is sufficient.
  For React/Vite, use npm run dev -- --host 127.0.0.1 --port PORT.
- Browser and server process execution may both need require_escalated. Continue
  normal authorized local testing; preserve actual errors and unresolved limits.

## Dependencies and inputs

The app/node_modules link provides the exact frozen optional dependency installation
for this workspace. app/package-lock.json identifies the resolved packages.
Do not mutate this shared installation. If you need additional dependencies,
replace the symlink with a task-local installation before changing packages.
T1's unmodified starter build has passed; T2/T3's existing vanilla pages are served
without a bundler unless your actual implementation requires one.

The supplied resources/ candidates are pinned and licensed; see resources/README.md.
modern-web-guidance.txt is common retrieved guidance, not a product design target.
The task determines relevant techniques and feature detection.

Use tools.view_image to inspect produced local screenshots. If observing continuous
interaction through ordered frames, preserve order and timing and describe that
scope accurately. Source captures, actual visual inspection, interaction assertions
and real-user acceptance establish different facts.

External resource research and legitimate public package acquisition are available
through the host's tools. Do not treat a network failure as evidence about a
resource's design. Keep implementation and evidence within this task's boundary.
