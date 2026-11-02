#!/usr/bin/env python3
"""Preflight a new npm release using exact public version metadata (read-only).

An empty/JSON-encoded npm CLI value is NOT proof that the requested version is
unpublished. Only an actual HTTP 404 permits the first publish attempt.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "ui-spec-studio"
REPOSITORY = "https://github.com/D1ChangGeng/UI-Spec-Studio"
REGISTRY = "https://registry.npmjs.org"


class RegistryProbeError(RuntimeError):
    """Unknown or conflicting registry state must fail closed."""


def public_version_metadata(version: str) -> dict | None:
    """Return immutable metadata; None means a confirmed HTTP 404, not an npm CLI guess."""
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise RegistryProbeError("Invalid exact release version")
    request = Request(
        f"{REGISTRY}/{PACKAGE}/{quote(version, safe='')}",
        headers={
            "Accept": "application/json",
            "Cache-Control": "no-cache",
            "User-Agent": "ui-spec-studio-oidc-publish-preflight",
        },
    )
    try:
        with urlopen(request, timeout=25) as response:
            if response.status != 200:
                raise RegistryProbeError(f"Unexpected registry HTTP {response.status}")
            metadata = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            return None
        raise RegistryProbeError(f"Unable to determine public version: HTTP {error.code}") from error
    except (TimeoutError, URLError, ValueError) as error:
        raise RegistryProbeError(f"Unable to determine public version: {error}") from error
    if not isinstance(metadata, dict):
        raise RegistryProbeError("Invalid public registry version metadata")
    return metadata


def inspect(version: str, integrity: str, read=public_version_metadata) -> str:
    metadata = read(version)
    if metadata is None:
        return "NOT_PUBLISHED"

    repository = metadata.get("repository")
    repo_url = repository if isinstance(repository, str) else (
        repository.get("url") if isinstance(repository, dict) else None
    )
    if isinstance(repo_url, str):
        repo_url = repo_url.removeprefix("git+").removesuffix(".git")
    if (metadata.get("name") != PACKAGE or metadata.get("version") != version
            or repo_url != REPOSITORY):
        raise RegistryProbeError("Public package name, version or repository identity conflict")
    dist = metadata.get("dist")
    actual = dist.get("integrity") if isinstance(dist, dict) else None
    if actual != integrity:
        raise RegistryProbeError("Public npm version has conflicting SHA-512; refusing publish")
    return "ALREADY_PUBLISHED_MATCH"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tarball", type=Path, default=ROOT / "dist/ui-spec-installer.tgz")
    args = parser.parse_args()
    try:
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        archive = args.tarball.read_bytes()
        integrity = "sha512-" + base64.b64encode(hashlib.sha512(archive).digest()).decode("ascii")
        outcome = inspect(version, integrity)
        print(outcome)
        return 0
    except (RegistryProbeError, OSError, ValueError) as error:
        print(f"NPM_PUBLISH_PREFLIGHT_BLOCKED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
