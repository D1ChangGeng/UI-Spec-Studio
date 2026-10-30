# Frozen study inputs

T1/T2/T3-starter.zip preserve the task, common environment and guidance,
starting application and same licensed resource pool. They exclude node_modules,
build output and all participant work. resources.zip also preserves the original
source files (including TSX and Astro) without relying on repository source-package
extension rules. The runtime archives are frozen separately by the coordinator.

The source pool includes pinned Bootstrap v5.3.8, Magic UI and Kokonut UI material
with MIT notices and SHA-256 identities in resources/sources.json. The entire
repositories and any unrelated branding/images are not bundled. The T2/T3 starter
applications preserve the original UI Spec Studio fixture's license and origin
notes. This is a provenance/availability check, not legal advice or a quality
certification. All app content is fictional, browser-local study data.

modern-web-guidance.txt and its Apache-2.0 notice are the exact common inputs
previously archived for the v1.18 study, reused unchanged. Setup additionally
retrieved current responsive/layout/navigation guidance before preparing tooling;
that retrieval did not change participant product code or condition differences.

A common dependency installation was completed using T1's frozen package-lock
with npm ci --ignore-scripts --no-audit --no-fund. Its empty starter build passed.
Python Playwright 1.57.0 and markdown-it-py 4.0.0 were installed. The pinned
Playwright browser mirror returned invalid archives; official Chrome for Testing
156.0.8078.80 was downloaded instead. A local elevated-process launch, DOM action
and screenshot smoke check passed. This establishes tool availability only, not
any product result. Final browser details are in environment-check.json.

The source archive and task digests in manifest.json were generated before
participant execution. Regenerate no input after registration without recording
the old and new identity and the affected run.
