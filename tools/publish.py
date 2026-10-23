#!/usr/bin/env python3
"""Publish a tested checkout as a verified release in an existing GitHub repository."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from package import build, source_files  # noqa: E402
from validate_package import validate  # noqa: E402


def command(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=cwd, text=True, encoding="utf-8", capture_output=True, check=False)
    if check and result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(args[:4])}\n{result.stderr.strip()}")
    return result


def plan(owner: str, name: str) -> dict[str, object]:
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", owner):
        raise ValueError("Use a valid GitHub owner")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}", name):
        raise ValueError("Use a valid repository name")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("VERSION must use major.minor.patch")
    return {"repository": f"{owner}/{name}", "tag": f"v{version}",
            "source_files": [p.relative_to(ROOT).as_posix() for p in source_files(ROOT)],
            "scope": "Release the tested current commit in the existing repository"}


def publish(owner: str, name: str) -> dict[str, str]:
    details = plan(owner, name)
    errors = validate(ROOT)
    if errors:
        raise ValueError("Package validation failed: " + "; ".join(errors))
    for tool in ("git", "gh"):
        if shutil.which(tool) is None:
            raise RuntimeError(f"Install {tool} and configure authorized access first")
    if command(["git", "status", "--porcelain"], ROOT).stdout.strip():
        raise ValueError("Publish a clean committed checkout")
    repo, tag = str(details["repository"]), str(details["tag"])
    remote_name = command(["gh", "repo", "view", repo, "--json", "nameWithOwner", "--jq", ".nameWithOwner"], ROOT).stdout.strip()
    if remote_name.lower() != repo.lower():
        raise ValueError("Repository identity does not match the requested destination")
    head = command(["git", "rev-parse", "HEAD"], ROOT).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError("Expected an exact Git commit SHA")
    observed = command(["gh", "api", f"repos/{repo}/commits/{head}", "--jq", ".sha"], ROOT).stdout.strip()
    if observed != head:
        raise ValueError("Current commit must exist in the target repository")
    tag_check = command(["gh", "api", f"repos/{repo}/commits/{tag}", "--jq", ".sha"], ROOT, check=False)
    if tag_check.returncode == 0 and tag_check.stdout.strip() != head:
        raise ValueError("Release tag identifies a different commit; choose a new version")
    notes = ROOT / "docs/releases" / f"{tag}.md"
    if not notes.is_file():
        raise ValueError("Provide version-specific release notes")
    command([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], ROOT)
    assets = build(ROOT)
    if tag_check.returncode != 0:
        command(["gh", "api", f"repos/{repo}/git/refs", "--method", "POST",
                 "-f", f"ref=refs/tags/{tag}", "-f", f"sha={head}"], ROOT)
    existing = command(["gh", "release", "view", tag, "--repo", repo, "--json", "isDraft,url"], ROOT, check=False)
    if existing.returncode == 0:
        state = json.loads(existing.stdout)
        if not isinstance(state, dict) or type(state.get("isDraft")) is not bool:
            raise ValueError("Existing release metadata is incomplete")
    else:
        # A create failure (including a permission/network failure) is surfaced directly.
        command(["gh", "release", "create", tag, *[str(p) for p in assets], "--repo", repo,
                 "--verify-tag", "--title", f"UI Spec Studio {tag}", "--notes-file", str(notes), "--draft"], ROOT)
        state = {"isDraft": True}
    tag_head = command(["gh", "api", f"repos/{repo}/commits/{tag}", "--jq", ".sha"], ROOT).stdout.strip()
    if tag_head != head:
        raise ValueError("Release tag identifies a different commit; preserve it and choose a new version")
    with tempfile.TemporaryDirectory(prefix="ui-spec-release-check-") as temporary:
        command(["gh", "release", "download", tag, "--repo", repo, "--dir", temporary], ROOT)
        for asset in assets:
            downloaded = Path(temporary) / asset.name
            if not downloaded.is_file() or hashlib.sha256(downloaded.read_bytes()).digest() != hashlib.sha256(asset.read_bytes()).digest():
                raise ValueError(f"Release asset readback differs: {asset.name}")
    if state.get("isDraft"):
        command(["gh", "release", "edit", tag, "--repo", repo, "--draft=false", "--latest"], ROOT)
    final = json.loads(command(["gh", "release", "view", tag, "--repo", repo, "--json", "isDraft,url,tagName"], ROOT).stdout)
    if not isinstance(final, dict) or not isinstance(final.get("url"), str) or final.get("isDraft") is not False or final.get("tagName") != tag:
        raise ValueError("Release publication readback is incomplete")
    return {"repository": f"https://github.com/{repo}", "commit": head, "tag": tag,
            "release": final["url"], "asset_readback": "sha256-verified"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="D1ChangGeng")
    parser.add_argument("--name", default="UI-Spec-Studio")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    try:
        result = publish(args.owner, args.name) if args.execute else plan(args.owner, args.name)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"publish: {exc}\nInspect the remote release state before retrying.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
