#!/usr/bin/env python3
"""Copy the self-contained skill to an explicit local skill directory."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def install(target: Path, source: Path = ROOT / "skills/ui-spec") -> str:
    source = source.resolve(strict=True)
    if target.is_symlink():
        raise ValueError("Choose a regular destination directory")
    target = target.absolute()
    if target.exists():
        raise FileExistsError(f"Destination already exists; inspect it before updating: {target}")
    resolved = target.resolve()
    if resolved == source or source in resolved.parents:
        raise ValueError("Destination must be outside the source skill")
    for path in source.rglob("*"):
        if path.is_symlink():
            raise ValueError("Skill source contains a symbolic link")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return str(target)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", type=Path, required=True, help="Exact directory, e.g. /project/.agents/skills/ui-spec")
    args = p.parse_args()
    try:
        print(install(args.target))
    except (OSError, ValueError) as exc:
        print(f"install_local: {exc}", file=sys.stderr)
        raise SystemExit(2)
