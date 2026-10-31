#!/usr/bin/env python3
"""Install the pinned Linux x64 browser/recorder used by CI acceptance.

System libraries remain the responsibility of ``playwright install-deps chromium``.
This tool uses official archives and reviewed SHA-256 pins, and changes neither
browser launch options nor the acceptance scripts. Use a fresh output directory.
"""
from __future__ import annotations

import argparse
import hashlib
from importlib import metadata
import json
from pathlib import Path, PurePosixPath
import platform
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

PLAYWRIGHT_VERSION = "1.57.0"
BROWSER_VERSION = "143.0.7499.4"
ASSETS = (
    {
        "name": "chrome-headless-shell",
        "version": BROWSER_VERSION,
        "urls": [
            "https://storage.googleapis.com/chrome-for-testing-public/"
            "143.0.7499.4/linux64/chrome-headless-shell-linux64.zip",
        ],
        "bytes": 115006070,
        "sha256": "a9a525cb3832d59a810f78f8ba6c5ed3592a6a488984627f5d827c2a365c8a5a",
        "directory": "chrome-headless-shell-143.0.7499.4",
        "executable": "chrome-headless-shell-linux64/chrome-headless-shell",
    },
    {
        "name": "ffmpeg",
        "version": "1011",
        "urls": [
            "https://playwright.download.prss.microsoft.com/dbazure/download/"
            "playwright/builds/ffmpeg/1011/ffmpeg-linux.zip",
            "https://cdn.playwright.dev/dbazure/download/"
            "playwright/builds/ffmpeg/1011/ffmpeg-linux.zip",
            "https://cdn.playwright.dev/builds/ffmpeg/1011/ffmpeg-linux.zip",
        ],
        "bytes": 2376500,
        "sha256": "ebc74fc5b94830176a3c2914ae96bd8bc7f6a91f4f33890230f84a172ee61ccc",
        "directory": "ffmpeg-1011",
        "executable": "ffmpeg-linux",
    },
)


class ProvisionError(RuntimeError):
    """A browser supply or compatibility check failed."""


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_verified(asset: dict, path: Path, record: dict) -> None:
    """Retry only the pinned official sources; never accept alternate bytes."""
    record["attempts"] = []
    partial = path.with_suffix(".partial")
    for _ in range(2):
        for url in asset["urls"]:
            attempt = {"url": url}
            record["attempts"].append(attempt)
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "UI-Spec-Studio-CI"})
                with urllib.request.urlopen(request, timeout=30) as response:
                    if response.status != 200:
                        raise ProvisionError(f"Unexpected HTTP status: {response.status}")
                    attempt["resolved_url"] = response.geturl()
                    if not attempt["resolved_url"].startswith("https://"):
                        raise ProvisionError("Download redirected outside HTTPS")
                    count = 0
                    with partial.open("wb") as stream:
                        while chunk := response.read(1024 * 1024):
                            count += len(chunk)
                            if count > asset["bytes"]:
                                raise ProvisionError("Archive exceeds its pinned length")
                            stream.write(chunk)
                digest = file_sha256(partial)
                attempt.update({"bytes": count, "sha256": digest})
                if count != asset["bytes"] or digest != asset["sha256"]:
                    raise ProvisionError("Archive length or SHA-256 does not match the reviewed pin")
                partial.replace(path)
                attempt["status"] = "verified"
                record["source_url"] = url
                return
            except Exception as error:
                attempt.update({"status": "failed", "error": str(error)})
                partial.unlink(missing_ok=True)
    raise ProvisionError(f"No verified official archive was obtained for {asset['name']}")


def extract_archive(archive_path: Path, destination: Path) -> None:
    """Extract regular files/directories with executable bits and no link escape."""
    with zipfile.ZipFile(archive_path) as archive:
        members = archive.infolist()
        seen = set()
        for member in members:
            path = PurePosixPath(member.filename)
            mode = member.external_attr >> 16
            if (not member.filename or "\\" in member.filename or path.is_absolute()
                    or ".." in path.parts or not path.parts or ":" in path.parts[0]
                    or stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)
                    or path.as_posix() in seen):
                raise ProvisionError(f"Unsafe or duplicate ZIP member: {member.filename}")
            seen.add(path.as_posix())
        for member in members:
            target = destination.joinpath(*PurePosixPath(member.filename).parts)
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(member) as source, target.open("xb") as stream:
                    shutil.copyfileobj(source, stream)
                target.chmod(0o755 if (member.external_attr >> 16) & 0o111 else 0o644)


def verify_playwright() -> None:
    distribution = metadata.distribution("playwright")
    if distribution.version != PLAYWRIGHT_VERSION:
        raise ProvisionError(f"Expected Playwright {PLAYWRIGHT_VERSION}, got {distribution.version}")
    registry_path = distribution.locate_file("playwright/driver/package/browsers.json")
    registry = json.loads(registry_path.read_text(encoding="utf-8"))["browsers"]
    versions = {item["name"]: item for item in registry}
    if (versions["chromium-headless-shell"]["browserVersion"] != BROWSER_VERSION
            or versions["ffmpeg"]["revision"] != "1011"):
        raise ProvisionError("Playwright's browser/FFmpeg registry differs from the reviewed pins")


def provision(output_dir: Path, report: dict) -> dict[str, str]:
    if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
        raise ProvisionError("This CI provisioner supports Linux x86-64 only")
    verify_playwright()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ProvisionError("Use a fresh --output-dir; existing installations are preserved")
    output_dir.mkdir(parents=True, exist_ok=True)
    executables = {}
    for asset in ASSETS:
        record = {key: asset[key] for key in ("name", "version", "bytes", "sha256")}
        report["artifacts"].append(record)
        archive = output_dir / f"{asset['directory']}.zip"
        download_verified(asset, archive, record)
        destination = output_dir / asset["directory"]
        with tempfile.TemporaryDirectory(prefix="extract-", dir=output_dir) as staging:
            extracted = Path(staging) / "files"
            extracted.mkdir()
            extract_archive(archive, extracted)
            binary = extracted / asset["executable"]
            if not binary.is_file() or not binary.stat().st_mode & 0o111:
                raise ProvisionError(f"Missing executable in verified {asset['name']} archive")
            record["executable_sha256"] = file_sha256(binary)
            extracted.rename(destination)
        executables[asset["name"]] = str(destination / asset["executable"])
        record["executable"] = executables[asset["name"]]
    version = subprocess.run(
        [executables["chrome-headless-shell"], "--version"],
        capture_output=True, text=True, check=True, timeout=20,
    ).stdout.strip()
    if version != f"Google Chrome for Testing {BROWSER_VERSION}":
        raise ProvisionError(f"Unexpected browser version: {version}")
    report["browser_version_output"] = version
    return {
        "browser_path": executables["chrome-headless-shell"],
        "browsers_path": str(output_dir),
        "ffmpeg_path": executables["ffmpeg"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args(argv)
    report = {"schema_version": 1, "status": "provisioning", "platform": platform.platform(),
              "playwright_version": PLAYWRIGHT_VERSION, "artifacts": []}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    try:
        outputs = provision(args.output_dir.resolve(), report)
        if args.github_output:
            if any("\n" in value or "\r" in value for value in outputs.values()):
                raise ProvisionError("Output paths must be single-line values")
            with args.github_output.open("a", encoding="utf-8") as stream:
                stream.write("".join(f"{key}={value}\n" for key, value in outputs.items()))
        report.update({"status": "ready", "outputs": outputs})
        result = 0
    except Exception as error:
        report.update({"status": "failed", "error": str(error)})
        result = 1
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return result


if __name__ == "__main__":
    raise SystemExit(main())
