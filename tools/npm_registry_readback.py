#!/usr/bin/env python3
"""Verify eventual public npm readback after a successful or idempotent publish.

Read-only: never authenticates, publishes or changes distribution tags. A
successful npm publish can precede publicly visible version metadata; a
temporary 404 must never be mistaken for a failed publish.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
NAME = "ui-spec-studio"
REPOSITORY = "https://github.com/D1ChangGeng/UI-Spec-Studio"
REGISTRY = "https://registry.npmjs.org"


class ReadbackPending(RuntimeError):
    """The registry has not yet converged; do not blindly publish again."""


class IntegrityConflict(RuntimeError):
    """The registry returned authoritative, but unexpected, package identity."""


def fetch_json(url: str) -> object:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "Cache-Control": "no-cache",
            "User-Agent": "ui-spec-studio-release-readback",
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code in (404, 408, 429, 500, 502, 503, 504):
            raise ReadbackPending(f"Public registry HTTP {error.code}") from error
        raise
    except (TimeoutError, URLError) as error:
        raise ReadbackPending(f"Public registry request pending: {error}") from error


def verify_once(version: str, expected_integrity: str, fetch=fetch_json) -> None:
    """Require the exact immutable version and the public latest dist-tag."""
    metadata = fetch(f"{REGISTRY}/{NAME}/{quote(version, safe='')}")
    if not isinstance(metadata, dict):
        raise IntegrityConflict("Invalid registry version metadata")
    repo = metadata.get("repository")
    repo_url = repo if isinstance(repo, str) else repo.get("url") if isinstance(repo, dict) else None
    if isinstance(repo_url, str):
        repo_url = repo_url.removeprefix("git+").removesuffix(".git")
    if metadata.get("name") != NAME or metadata.get("version") != version or repo_url != REPOSITORY:
        raise IntegrityConflict("Registry name, version or repository does not match the approved release")
    dist = metadata.get("dist")
    remote_integrity = dist.get("integrity") if isinstance(dist, dict) else None
    if remote_integrity != expected_integrity:
        raise IntegrityConflict("Registry SHA-512 differs from the exact release tarball")

    tags = fetch(f"{REGISTRY}/-/package/{NAME}/dist-tags")
    if not isinstance(tags, dict):
        raise ReadbackPending("Public npm dist-tags not yet available")
    latest = tags.get("latest")
    if latest != version:
        raise ReadbackPending(f"Public latest dist-tag is {latest!r}, expected {version}")


def wait_for_readback(
    version: str,
    integrity: str,
    *,
    attempts: int = 9,
    fetch=fetch_json,
    pause=time.sleep,
) -> None:
    if attempts < 1:
        raise ValueError("attempts must be positive")
    for attempt in range(1, attempts + 1):
        try:
            verify_once(version, integrity, fetch)
            print(f"PUBLIC_REGISTRY_INTEGRITY_VERIFIED {NAME}@{version}")
            print(f"PUBLIC_LATEST_DIST_TAG_VERIFIED {NAME}@{version}")
            return
        except ReadbackPending as error:
            print(f"PUBLIC_READBACK_PENDING ({attempt}/{attempts}): {error}", flush=True)
            if attempt == attempts:
                raise
            pause(min(2 * attempt, 10))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tarball", type=Path, default=ROOT / "dist/ui-spec-installer.tgz")
    parser.add_argument("--attempts", type=int, default=9)
    args = parser.parse_args()
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    integrity = "sha512-" + base64.b64encode(
        hashlib.sha512(args.tarball.read_bytes()).digest()
    ).decode("ascii")
    try:
        wait_for_readback(version, integrity, attempts=args.attempts)
    except ReadbackPending as error:
        print(
            "PUBLIC_READBACK_PENDING: no confirmed public metadata after bounded retries. "
            "If npm publish already succeeded, do NOT republish the same version; "
            "check the public registry and rerun read-only verification. "
            f"Last observation: {error}",
            file=sys.stderr,
        )
        return 2
    except (IntegrityConflict, OSError, ValueError) as error:
        print(f"PUBLIC_REGISTRY_VERIFICATION_FAILED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
