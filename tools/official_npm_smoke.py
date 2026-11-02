#!/usr/bin/env python3
"""Verify the actual PUBLIC npm-named UI Spec Studio CLI, including legacy migration.

Never publishes, logs in, or accesses npm credentials. An unregistered name is
reported as an explicit SKIP unless --require-published is given.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
NAME = "ui-spec-studio"
EXPECTED_REPO = "https://github.com/D1ChangGeng/UI-Spec-Studio"


def invoke(argv: list[str], cwd: Path, *, timeout: int = 110, expect_success: bool = True,
           env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(argv, cwd=cwd, encoding="utf-8", errors="replace",
                            capture_output=True, text=True, timeout=timeout, env=env)
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




def latest_metadata(
    npm: str, version: str, *, require_published: bool, attempts: int = 9,
    pause=time.sleep,
) -> dict | None:
    """Read npm latest with fresh caches; only the expected version is accepted.

    An immediate npm CLI latest result may lag after the raw public npm
    version and dist-tag endpoints are already correct. Fresh cache per attempt
    prevents local negative/stale package metadata from becoming a release
    failure. This helper never publishes or modifies user installations.
    """
    if attempts < 1:
        raise ValueError("attempts must be positive")
    for attempt in range(1, attempts + 1):
        with tempfile.TemporaryDirectory(prefix="ui-spec-npm-latest-") as cache:
            env = {
                **os.environ,
                "NPM_CONFIG_CACHE": str(Path(cache) / "cache"),
                "NPM_CONFIG_PREFER_ONLINE": "true",
            }
            query = invoke(
                [npm, "view", f"{NAME}@latest", "name", "version",
                 "repository.url", "dist.integrity", "--json",
                 "--prefer-online", "--fetch-retries=0"],
                ROOT, expect_success=False, env=env,
            )
        if query.returncode:
            if "E404" not in query.stderr and "E404" not in query.stdout:
                raise RuntimeError(
                    "npm registry read failed for another reason:\n"
                    + query.stderr[-1800:]
                )
            if not require_published:
                return None
            pending = "npm latest still returns E404"
        else:
            data = json.loads(query.stdout)
            if not isinstance(data, dict):
                if not require_published:
                    raise RuntimeError("Registry latest metadata is not a JSON object")
                pending = "npm latest metadata is not yet a complete object"
                if attempt == attempts:
                    raise RuntimeError(
                        f"OFFICIAL_NPM_LATEST_READBACK_PENDING after {attempts} checks: {pending}. "
                        "Never republish an already accepted npm version."
                    )
                print(f"OFFICIAL_NPM_LATEST_READBACK_PENDING ({attempt}/{attempts}): {pending}",
                      file=sys.stderr, flush=True)
                pause(min(2 * attempt, 10))
                continue
            actual_repo = registry_field(data, "repository.url")
            if actual_repo:
                actual_repo = actual_repo.removeprefix("git+").removesuffix(".git")
            if data.get("name") != NAME or actual_repo != EXPECTED_REPO:
                raise RuntimeError(f"Untrusted npm package identity; refusing installation: {data}")
            integrity = registry_field(data, "dist.integrity")
            if not integrity or not integrity.startswith("sha512-"):
                raise RuntimeError("Registry metadata has no SHA-512 tarball integrity")
            published = data.get("version")
            if published == version or not require_published:
                return data
            pending = f"npm latest still reports {published!r}; expected {version}"
        if attempt == attempts:
            raise RuntimeError(
                f"OFFICIAL_NPM_LATEST_READBACK_PENDING after {attempts} checks: {pending}. "
                "Verify the published registry version directly; never republish an "
                "already accepted npm version because of stale latest metadata."
            )
        print(f"OFFICIAL_NPM_LATEST_READBACK_PENDING ({attempt}/{attempts}): {pending}",
              file=sys.stderr, flush=True)
        pause(min(2 * attempt, 10))
    raise AssertionError("Unreachable npm latest retry exhaustion")


def resolve_npx_latest(
    npx: str, base: Path, version: str, *, attempts: int = 9, pause=time.sleep,
) -> dict[str, str]:
    """Require actual npm-named CLI version with a new isolated cache each retry."""
    if attempts < 1:
        raise ValueError("attempts must be positive")
    for attempt in range(1, attempts + 1):
        env = {
            **os.environ,
            "NPM_CONFIG_CACHE": str(base / f"npm-cache-{attempt}"),
            "NPM_CONFIG_PREFER_ONLINE": "true",
        }
        out = invoke([npx, "--yes", f"{NAME}@latest", "--version"], base, env=env)
        if out.stdout.strip() == f"{NAME} {version}":
            return env
        if attempt == attempts:
            raise RuntimeError(
                f"OFFICIAL_NPX_LATEST_READBACK_PENDING after {attempts} checks: "
                f"npm-named CLI resolved {out.stdout.strip()!r}, expected {NAME} {version}. "
                "Do not republish the already accepted version."
            )
        print(f"OFFICIAL_NPX_LATEST_READBACK_PENDING ({attempt}/{attempts}): "
              f"resolved {out.stdout.strip()!r}, expected {NAME} {version}",
              file=sys.stderr, flush=True)
        pause(min(2 * attempt, 10))
    raise AssertionError("Unreachable npx latest retry exhaustion")


def run(*, require_published: bool = False) -> dict:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    npm = shutil.which("npm")
    npx = shutil.which("npx")
    if not npm or not npx:
        raise RuntimeError("npm and npx are required for official public-distribution verification")
    data = latest_metadata(npm, version, require_published=require_published)
    if data is None:
        return {"registry": "unregistered", "result": "SKIP", "expected_version": version}
    published = data.get("version")
    if published != version:
        return {"registry": "registered", "result": "SKIP_NEW_CANDIDATE",
                "expected_version": version, "published_version": published}
    integrity = registry_field(data, "dist.integrity")

    # Establish byte identity independently of the npm registry and npx cache:
    # the published npm tarball must be the exact pinned GitHub release asset.
    release_url = (
        f"https://github.com/D1ChangGeng/UI-Spec-Studio/releases/download/"
        f"v{version}/ui-spec-installer.tgz"
    )
    with urlopen(release_url, timeout=30) as source:
        release_bytes = source.read()
    expected_integrity = "sha512-" + base64.b64encode(hashlib.sha512(release_bytes).digest()).decode("ascii")
    if integrity != expected_integrity:
        raise RuntimeError("Public npm SHA-512 differs from the exact GitHub Release asset")

    with tempfile.TemporaryDirectory(prefix="ui-spec-official-npm-") as td:
        base = Path(td)
        clean = base / "clean"
        legacy = base / "legacy"
        clean.mkdir()
        legacy.mkdir()
        npx_env = resolve_npx_latest(npx, base, version)
        flags = ["--agent", "codex", "--project", str(clean), "--no-tui"]
        result = invoke([npx, "--yes", f"{NAME}@latest", "install", *flags], base, env=npx_env)
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
             "--project", str(legacy), "--migrate", "--no-tui"], base, env=npx_env
        ).stdout)
        backup = Path(migration.get("backup") or "")
        if migration.get("result") != "upgraded" or not backup.is_dir():
            raise RuntimeError(f"Official npm named migration did not retain a backup: {migration}")
        if (backup / "SKILL.md").read_bytes() != old_bytes:
            raise RuntimeError("Migrated original Skill does not match the prior bytes")
        restore = json.loads(invoke(
            [npx, "--yes", f"{NAME}@latest", "uninstall", "--agent", "codex",
             "--project", str(legacy), "--no-tui"], base, env=npx_env
        ).stdout)
        if restore.get("result") != "original-restored" or old_entry.read_bytes() != old_bytes:
            raise RuntimeError("Uninstall did not restore the original user-modified Skill")
        return {
            "registry": "published",
            "result": "PASS",
            "package": NAME,
            "version": version,
            "integrity": integrity,
            "release_tarball_sha512_match": True,
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
