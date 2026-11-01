#!/usr/bin/env python3
"""Offline end-to-end checks for the release tarball and its managed host adapters."""
from __future__ import annotations
import hashlib
import json
import shutil
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from package_installer import build_installer


def command(argv: list[str], cwd: Path, success: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(argv, cwd=cwd, text=True, encoding='utf-8', capture_output=True, timeout=90)
    if success and result.returncode != 0:
        raise AssertionError(f"Failed {argv[:4]}:\n{result.stdout}\n{result.stderr}")
    if not success and result.returncode == 0:
        raise AssertionError(f'Unexpectedly succeeded: {argv[:4]}')
    return result


def run() -> dict[str, object]:
    expected = {p.relative_to(ROOT / 'skills/ui-spec').as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (ROOT / 'skills/ui-spec').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    with tempfile.TemporaryDirectory(prefix='ui-spec-distribution-') as td:
        base = Path(td)
        archive = build_installer(ROOT, base)
        alternate = build_installer(ROOT, base / 'repeat')
        if archive.read_bytes() != alternate.read_bytes():
            raise AssertionError('Installer tarball is not reproducible')
        with tarfile.open(archive) as tar:
            members = tar.getmembers()
            if any(not m.isfile() or not m.name.startswith('package/') or '..' in Path(m.name).parts for m in members):
                raise AssertionError('Installer includes unsafe/non-file entries')
            if any(m.name.startswith(('package/docs/', 'package/tests/', 'package/.git/')) for m in members):
                raise AssertionError('Repository maintenance files reached installer payload')
            tar.extractall(base / 'unpacked', filter='data')
        package = base / 'unpacked/package'
        cli = package / 'bin/ui-spec.mjs'
        manifest = json.loads((package / 'payload/manifest.json').read_text())
        if set(manifest['files']) != set('skill/' + name for name in expected) | {
            p.relative_to(package / 'payload').as_posix() for p in (package / 'payload/adapters').rglob('*') if p.is_file()
        }:
            raise AssertionError('Unexpected payload inventory')
        command(['node', str(cli), '--help'], base)
        project_checks = []
        for agent in ('codex', 'claude-code', 'cursor', 'opencode'):
            project = base / agent
            project.mkdir()
            if agent == 'codex':
                config = project / '.codex/config.toml'
                config.parent.mkdir()
                config.write_text('model = "existing-user-setting"\n', encoding='utf-8')
            target_rel = '.claude/skills/ui-spec' if agent == 'claude-code' else '.agents/skills/ui-spec'
            target = project / target_rel
            prefix = ['node', str(cli)]
            flags = ['--agent', agent, '--project', str(project)]
            command(prefix + ['install', *flags, '--dry-run'], project)
            if target.exists():
                raise AssertionError('Dry run wrote Skill files')
            command(prefix + ['install', *flags], project)
            command(prefix + ['install', *flags], project)
            status = json.loads(command(prefix + ['status', *flags], project).stdout)
            if status['status'] != 'current' or status['skill_files'] != len(expected):
                raise AssertionError('Status/Skill inventory mismatch')
            installed = {p.relative_to(target).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in target.rglob('*') if p.is_file() and p.name != '.ui-spec-install.json'}
            if installed != expected:
                raise AssertionError(f'{agent} installed wrong files')
            entry = target / 'SKILL.md'
            original = entry.read_bytes()
            entry.write_bytes(original + b'\nlocally modified')
            command(prefix + ['uninstall', *flags], project, success=False)
            if not entry.is_file():
                raise AssertionError('Tampering removed user-modified Skill')
            entry.write_bytes(original)
            command(prefix + ['uninstall', *flags], project)
            if target.exists():
                raise AssertionError('Uninstall left managed Skill files')
            if agent == 'codex':
                if config.read_text(encoding='utf-8') != 'model = "existing-user-setting"\n':
                    raise AssertionError('Codex user configuration was not preserved')
                # An independent native adapter registration is not owned by an
                # absent unified Skill receipt; do not delete it on uninstall.
                native = package / 'payload/adapters/codex/install.py'
                command([sys.executable, str(native), 'install', '--project', str(project)], project)
                native_role = project / '.codex/agents/ui_researcher.toml'
                if not native_role.is_file():
                    raise AssertionError('Independent native Codex adapter fixture did not install')
                command(prefix + ['uninstall', *flags], project)
                if not native_role.is_file():
                    raise AssertionError('An unowned standalone Codex registration was removed')
                command([sys.executable, str(native), 'uninstall', '--project', str(project)], project)
            project_checks.append(agent)
        result = command([(shutil.which('npx') or 'npx'), '--yes', '--offline', archive.as_uri(), 'status', '--agent', 'codex', '--project', str(base / 'not-installed')], base)
        if json.loads(result.stdout)['status'] != 'absent':
            raise AssertionError('npx tarball command failed')
        return {'archive': archive.name, 'archive_bytes': archive.stat().st_size,
                'source_checkout': False, 'skill_files': len(expected), 'verified_hosts': project_checks,
                'checksum': hashlib.sha256(archive.read_bytes()).hexdigest()}


if __name__ == '__main__':
    try:
        print(json.dumps(run(), indent=2))
    except (OSError, ValueError, RuntimeError, AssertionError, subprocess.SubprocessError) as exc:
        print(f'installer_smoke: {exc}', file=sys.stderr)
        raise SystemExit(1)
