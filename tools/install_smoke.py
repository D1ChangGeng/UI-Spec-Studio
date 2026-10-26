#!/usr/bin/env python3
"""Exercise the standard Skills CLI in isolated projects and verify installed bytes."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CLI = "skills@1.7.4"


def run(source: str) -> dict[str, object]:
    expected = {p.relative_to(ROOT / "skills/ui-spec").as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (ROOT / "skills/ui-spec").rglob("*")
                if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}
    with tempfile.TemporaryDirectory(prefix="ui-spec-install-") as td:
        project = Path(td)
        command = ["npx", "--yes", CLI, "add", source, "--skill", "ui-spec", "-a", "codex",
                   "-a", "claude-code", "-a", "opencode", "--copy", "-y"]
        env = dict(os.environ, DISABLE_TELEMETRY="1", CI="true")
        result = subprocess.run(command, cwd=project, env=env, text=True, encoding="utf-8", capture_output=True, timeout=240)
        print(result.stdout)
        if result.returncode:
            raise RuntimeError(f"Installer failed ({result.returncode}): {result.stderr}")
        installed = sorted({p.parent for p in project.rglob("SKILL.md") if p.parent.name == "ui-spec"})
        if not (project / ".agents/skills/ui-spec/SKILL.md").is_file() or not (project / ".claude/skills/ui-spec/SKILL.md").is_file():
            raise ValueError("Expected canonical and Claude Code installations")
        for target in installed:
            for relative, digest in expected.items():
                file = target / relative
                if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != digest:
                    raise ValueError(f"Installed content differs: {target.name}/{relative}")
        target = project / ".agents/skills/ui-spec"
        for arguments in (["scripts/prepare.py", "--project-root", str(project)],
                          ["scripts/check_manifest.py", "--project-root", str(project), "--mode", "draft"],
                          ["scripts/find_resources.py", "--id", "fontsource", "--json"],
                          ["scripts/check_design_evidence.py", "--project-root", str(project),
                           "--record", ".agents/skills/ui-spec/assets/templates/design-evidence.json",
                           "--view", "execution"]):
            executed = subprocess.run([sys.executable, str(target / arguments[0]), *arguments[1:]],
                                      cwd=project, text=True, encoding="utf-8", capture_output=True, timeout=30)
            if executed.returncode:
                raise RuntimeError(executed.stderr or executed.stdout)
        return {"source": source, "installer": CLI, "requested_agents": ["codex", "claude-code", "opencode"],
                "installed_copies": len(installed), "verified_files_per_copy": len(expected),
                "helpers": "prepare, coverage checker, resource lookup and design evidence views executed", "scope": "CLI installation and file integrity; host model execution is separate"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(run(args.source), indent=2))
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"install_smoke: {exc}", file=sys.stderr)
        raise SystemExit(1)
