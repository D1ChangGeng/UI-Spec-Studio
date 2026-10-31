#!/usr/bin/env python3
"""Build reproducible source and standalone skill ZIP archives."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOP = {"README.md", "README.zh-CN.md", "LICENSE", "VERSION", "AGENTS.md", ".gitignore", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", ".gitattributes"}
DIRS = {"skills", "docs", "examples", "tools", "tests", ".github", "integrations"}
SUFFIXES = {".toml", ".md", ".py", ".json", ".yml", ".yaml", ".txt", ".svg", ".html", ".css", ".js", ".png", ".mp4"}
# Preserve declared study inputs and local replay assets in the full source package.
# This does not enlarge the portable Skill's asset policy.
EVIDENCE_SUFFIXES = {".csv", ".jsonl", ".mjs", ".log", ".woff2", ".webm", ".zip", ".jpg", ".jpeg"}
EXCLUDED = {"__pycache__", "node_modules", ".git", ".pytest_cache", "dist"}


def source_files(root: Path) -> list[Path]:
    result: list[Path] = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if path.is_symlink():
            continue
        if not path.is_file() or any(part in EXCLUDED for part in rel.parts):
            continue
        evidence_asset = (len(rel.parts) > 2 and rel.parts[0] == 'docs'
                          and rel.parts[1] in {'evidence', 'experiments'}
                          and path.suffix in EVIDENCE_SUFFIXES)
        allowed = (len(rel.parts) == 1 and rel.name in TOP) or evidence_asset or (
            len(rel.parts) > 1 and rel.parts[0] in DIRS and
            (path.suffix in SUFFIXES or path.name == "LICENSE"))
        if allowed:
            result.append(path)
    return sorted(result, key=lambda p: p.relative_to(root).as_posix())


def archive(output: Path, items: list[tuple[str, bytes]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as z:
        for name, content in sorted(items):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, content)


def build(root: Path = ROOT, output_dir: Path | None = None) -> list[Path]:
    output = output_dir or root / "dist"
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("VERSION must use major.minor.patch")
    files = source_files(root)
    repo_zip = output / f"ui-spec-studio-{version}.zip"
    skill_zip = output / f"ui-spec-{version}.zip"
    archive(repo_zip, [("ui-spec-studio/" + p.relative_to(root).as_posix(), p.read_bytes()) for p in files])
    skill_root = root / "skills/ui-spec"
    archive(skill_zip, [("ui-spec/" + p.relative_to(skill_root).as_posix(), p.read_bytes())
                        for p in files if p.is_relative_to(skill_root)])
    inventory = output / "contents.json"
    inventory.write_text(json.dumps({"version": version, "files": [
        {"path": p.relative_to(root).as_posix(), "bytes": p.stat().st_size,
         "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files
    ]}, indent=2) + "\n", encoding="utf-8", newline="\n")
    hashes = output / "SHA256SUMS.txt"
    hashes.write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n"
                              for p in (repo_zip, skill_zip, inventory)), encoding="utf-8", newline="\n")
    return [repo_zip, skill_zip, inventory, hashes]


if __name__ == "__main__":
    for path in build():
        print(path)
