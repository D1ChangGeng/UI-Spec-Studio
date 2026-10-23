#!/usr/bin/env python3
"""Create optional repository-local UI records, preserving existing files."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys


def prepare(project_root: Path, name: str | None = None) -> dict[str, list[str]]:
    root = project_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Project root must be an existing directory")
    target = root / ".ui-spec"
    if target.is_symlink():
        raise ValueError("Choose a project-local .ui-spec directory rather than a symlink")
    templates = Path(__file__).resolve().parents[1] / "assets" / "templates"
    manifest = json.loads((templates / "manifest.json").read_text(encoding="utf-8"))
    manifest["project"] = name or root.name
    design = root / "DESIGN.md"
    if design.is_file():
        try:
            design.resolve(strict=True).relative_to(root)
        except ValueError:
            raise ValueError("Design reference must resolve inside the project") from None
        manifest["design_system_path"] = "DESIGN.md"
    content = {
        "brief.md": (templates / "brief.md").read_text(encoding="utf-8"),
        "manifest.json": json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        ".gitignore": "evidence/\n",
    }
    if target.exists() and not target.is_dir():
        raise ValueError("Expected a project-local .ui-spec directory")
    for filename in content:
        path = target / filename
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError(f"Expected a regular project-local file: {path}")
    target.mkdir(exist_ok=True)
    result: dict[str, list[str]] = {"created": [], "preserved": []}
    for filename, text in content.items():
        path = target / filename
        if path.is_symlink():
            raise ValueError(f"Expected a regular project-local file: {path}")
        try:
            with path.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(text)
            result["created"].append(str(path.relative_to(root)))
        except FileExistsError:
            if not path.is_file():
                raise ValueError(f"Expected a file: {path}")
            result["preserved"].append(str(path.relative_to(root)))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--name")
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.project_root, args.name), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"prepare: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
