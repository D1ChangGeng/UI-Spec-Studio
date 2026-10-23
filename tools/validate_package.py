#!/usr/bin/env python3
"""Validate portable package structure, metadata and local reference integrity."""
from __future__ import annotations
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
COMMON = ("workflow", "analysis", "principles", "component-sourcing", "interaction-and-variants", "verification")
REQUIRED = ["README.md", "README.zh-CN.md", "LICENSE", "VERSION", "AGENTS.md", "SECURITY.md", "CONTRIBUTING.md",
            "skills/ui-spec/SKILL.md", "skills/ui-spec/LICENSE", "skills/ui-spec/scripts/prepare.py",
            "skills/ui-spec/scripts/check_manifest.py", "docs/INSTALL.md", "docs/GUIDE.md", "docs/MODEL.md",
            "docs/WRITING.md", "docs/REVIEW.md", "docs/MANIFEST.md", "docs/RESEARCH.md", "docs/EVALUATION.md",
            "docs/PUBLISHING.md", "skills/ui-spec/references/integration.md",
            *[f"skills/ui-spec/references/{name}.md" for name in COMMON]]
IGNORED = {".git", "dist", "node_modules", "__pycache__", ".pytest_cache"}


def validate(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for name in REQUIRED:
        path = root / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Required regular file missing or empty: {name}")
    skill = root / "skills/ui-spec/SKILL.md"
    if not skill.is_file() or skill.is_symlink():
        return errors
    try:
        text = skill.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return errors + [f"SKILL.md read failed: {exc}"]
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append("SKILL.md requires YAML frontmatter")
    else:
        header = match.group(1)
        def scalar(name: str) -> str:
            value = re.search(rf"^{re.escape(name)}:\s*(.+)$", header, re.M)
            if not value:
                return ""
            raw = value.group(1).strip()
            try:
                parsed = json.loads(raw) if raw.startswith('"') else raw
            except ValueError:
                errors.append(f"Invalid scalar: {name}")
                return ""
            return parsed if isinstance(parsed, str) else ""
        name = scalar("name")
        if name != skill.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append("Skill name must match its directory and Agent Skills naming rules")
        if not 1 <= len(scalar("description")) <= 1024:
            errors.append("Description must have 1–1024 characters")
        if len(scalar("compatibility")) > 500:
            errors.append("Compatibility must have <= 500 characters")
    if len(text.splitlines()) > 500:
        errors.append("Keep the entry below 500 lines")
    for name in COMMON:
        if f"references/{name}.md" not in text:
            errors.append(f"Entry must directly link the common reference: {name}")
    version_path = root / "VERSION"
    if version_path.is_file():
        version = version_path.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
            errors.append("VERSION must use major.minor.patch")
        if f'version: "{version}"' not in text:
            errors.append("Skill metadata and VERSION must match")
        if not (root / "docs/releases" / f"v{version}.md").is_file():
            errors.append("Version-specific release notes are required")
    for md in root.rglob("*.md"):
        if any(p in IGNORED for p in md.relative_to(root).parts):
            continue
        if md.is_symlink():
            errors.append(f"Package Markdown must be a regular file: {md.relative_to(root)}")
            continue
        try:
            body = md.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"Markdown read failed: {md.relative_to(root)}: {exc}")
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", body):
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            try:
                candidate = (md.parent / target).resolve()
                candidate.relative_to(root)
            except (ValueError, OSError, RuntimeError):
                errors.append(f"Reference leaves repository or cannot resolve: {md.relative_to(root)} -> {target}")
                continue
            if not candidate.exists():
                errors.append(f"Broken local link: {md.relative_to(root)} -> {target}")
            if md.is_relative_to(skill.parent) and not candidate.is_relative_to(skill.parent):
                errors.append(f"Installed skill reference leaves its bundle: {target}")
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("Package structure, metadata, common-reference links and local paths: PASS")
