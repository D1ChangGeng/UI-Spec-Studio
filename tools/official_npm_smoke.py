#!/usr/bin/env python3
"""Verify the actual PUBLIC npm-named UI Spec Studio CLI, including legacy migration.

Never publishes, logs in, or accesses npm credentials. An unregistered name is
reported as an explicit SKIP unless --require-published is given.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
NAME = "ui-spec-studio"
EXPECTED_REPO = "https://github.com/D1ChangGeng/UI-Spec-Studio"


def invoke(argv: list[str], cwd: Path, *, timeout: int = 110, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(argv, cwd=cwd, encoding="utf-8", errors="replace",
                            capture_output=True, text=True, timeout=timeout)
    if expect_success and result.returncode:
        raise RuntimeError(
            f"Command failed ({result.returncode}): {argv[:4]}\n"
            f"stdout:\n{result.stdout[-1500:]}\nstderr:\n{result.stderr[-2500:]}"
        )
    return result


def registry_field(data: dict, field: str) -> str | None:
    if isinstance(data.get(field), str):
        return data[field]
    current: object = data
    for name in field.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(name)
    return current if isinstance(current, str) else None


def run(*, require_published: bool = False) -> dict:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    npm = shutil.which("npm")
    npx = shutil.which("npx")
    if not npm or not npx:
        raise RuntimeError("npm and npx are required for official public-distribution verification")
    query = invoke([npm, "view", f"{NAME}@latest", "name", "version",
                    "repository.url", "dist.integrity",
                    "--json", "--prefer-online", "--fetch-retries=0"], ROOT,
                   expect_success=False)
    if query.returncode:
        if "E404" not in query.stderr and "E404" not in query.stdout:
            raise RuntimeError("npm registry read failed for another reason:\n" + query.stderr[-1800:])
        if require_published:
            raise RuntimeError("Official npm package is unregistered: first owner-authenticated publish required")
        return {"registry": "unregistered", "result": "SKIP", "expected_version": version}
    data = json.loads(query.stdout)
    actual_repo = registry_field(data, "repository.url")
    if actual_repo:
        actual_repo = actual_repo.removeprefix("git+").removesuffix(".git")
    if data.get("name") != NAME or actual_repo != EXPECTED_REPO:
        raise RuntimeError(f"Untrusted npm package identity; refusing installation: {data}")
    published = data.get("version")
    integrity = registry_field(data, "dist.integrity")
    if not integrity or not integrity.startswith("sha512-"):
        raise RuntimeError("Registry metadata has no SHA-512 tarball integrity")
    if published != version:
        if require_published:
            raise RuntimeError(f"Expected npm latest {version}, registry reports {published}")
        return {"registry": "registered", "result": "SKIP_NEW_CANDIDATE",
                "expected_version": version, "published_version": published}

    with tempfile.TemporaryDirectory(prefix="ui-spec-official-npm-") as td:
        base = Path(td)
        clean = base / "clean"
        legacy = base / "legacy"
        clean.mkdir()
        legacy.mkdir()
        version_out = invoke([npx, "--yes", f"{NAME}@latest", "--version"], base)
        if f"{NAME} {version}" not in version_out.stdout:
            raise RuntimeError(f"Official npx latest resolved wrong CLI version: {version_out.stdout}")
        flags = ["--agent", "codex", "--project", str(clean), "--no-tui"]
        result = invoke([npx, "--yes", f"{NAME}@latest", "install", *flags], base)
        installation = json.loads(result.stdout)
        if installation.get("result") != "installed":
            raise RuntimeError(f"Clean npm installation did not finish: {installation}")
        root = clean / ".agents/skills/ui-spec"
        original = root / "SKILL.md"
        if not original.is_file() or not (clean / ".codex/agents/ui_researcher.toml").is_file():
            raise RuntimeError("Official npm package omitted the Skill or native Codex adapter")
        if installation.get("skill_files") != 37:
            raise RuntimeError("Unexpected portable Skill file inventory")
        old_root = legacy / ".agents/skills/ui-spec"
        old_root.parent.mkdir(parents=True)
        shutil.copytree(root, old_root)
        (old_root / ".ui-spec-install.json").unlink()
        old_entry = old_root / "SKILL.md"
        old_bytes = old_entry.read_bytes() + b"\n# locally retained legacy user edit\n"
        old_entry.write_bytes(old_bytes)
        migration = json.loads(invoke(
            [npx, "--yes", f"{NAME}@latest", "install", "--agent", "codex",
             "--project", str(legacy), "--migrate", "--no-tui"], base
        ).stdout)
        backup = Path(migration.get("backup") or "")
        if migration.get("result") != "upgraded" or not backup.is_dir():
            raise RuntimeError(f"Official npm named migration did not retain a backup: {migration}")
        if (backup / "SKILL.md").read_bytes() != old_bytes:
            raise RuntimeError("Migrated original Skill does not match the prior bytes")
        restore = json.loads(invoke(
            [npx, "--yes", f"{NAME}@latest", "uninstall", "--agent", "codex",
             "--project", str(legacy), "--no-tui"], base
        ).stdout)
        if restore.get("result") != "original-restored" or old_entry.read_bytes() != old_bytes:
            raise RuntimeError("Uninstall did not restore the original user-modified Skill")
        return {
            "registry": "published",
            "result": "PASS",
            "package": NAME,
            "version": version,
            "integrity": integrity,
            "public_cli": "npx --yes ui-spec-studio@latest",
            "skill_files": installation["skill_files"],
            "native_codex": True,
            "old_skill_migration": "verified",
            "uninstall_original_restored": True,
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-published", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(run(require_published=args.require_published), indent=2))
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"official_npm_smoke: {error}", file=sys.stderr)
        raise SystemExit(1)
