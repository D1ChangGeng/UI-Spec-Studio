#!/usr/bin/env python3
"""Offline end-to-end checks for the release tarball and its managed host adapters."""
from __future__ import annotations
import hashlib
import os
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
        version = json.loads((package / 'package.json').read_text())['version']
        pkg = json.loads((package / 'package.json').read_text())
        if pkg.get('name') != 'ui-spec-studio':
            raise AssertionError('Official npm package name differs from the build contract')
        if command(['node', str(cli), '--version'], base).stdout.strip() != f'ui-spec-studio {version}':
            raise AssertionError('CLI --version does not report the actual installed package')
        if 'ui-spec-studio@latest' not in command(['node', str(cli), '--help'], base).stdout:
            raise AssertionError('Installer help does not advertise the official npm command')
        english_help = command(['node', str(cli), '--help', '--lang', 'en'], base).stdout
        chinese_help = command(['node', str(cli), '--help', '--lang', 'zh'], base).stdout
        for term in ('Which tool', 'Harness', 'Native adapter', 'runtime files'):
            if term in english_help:
                raise AssertionError('User-facing English help contains internal installation terminology: ' + term)
        if 'Install:' not in english_help or '--migrate' not in english_help:
            raise AssertionError('English help omits basic user actions')
        if '安装：' not in chinese_help or '备份并替换旧安装' not in chinese_help:
            raise AssertionError('Chinese help omits install and migration instructions')
        if command(['node', str(cli), 'install', '--help', '--lang', 'zh'], base).stdout != chinese_help:
            raise AssertionError('Chinese help should work with subcommand ordering')
        if 'npm has already downloaded the compact release package' in cli.read_text(encoding='utf-8'):
            raise AssertionError('Unnecessary npm implementation explanation remains visible to Skill users')
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
        # The legacy Skills CLI has no ownership receipt. It may have copied
        # ordinary files or linked a shared Skill through a Windows Junction.
        source_skill = package / 'payload/skill'
        old = base / 'legacy-copied'
        old_target = old / '.agents/skills/ui-spec'
        old_target.parent.mkdir(parents=True)
        shutil.copytree(source_skill, old_target)
        old_entry = old_target / 'SKILL.md'
        current_version = (ROOT / 'VERSION').read_text(encoding='utf-8').strip().encode('ascii')
        fresh = old_entry.read_bytes()
        original = fresh.replace(b'version: "' + current_version + b'"', b'version: "1.20.1"') + b'\n# user annotation\n'
        if original == fresh + b'\n# user annotation\n':
            raise AssertionError('Failed to construct a byte-different legacy Skill fixture')
        old_entry.write_bytes(original)
        flags = ['--agent', 'codex', '--project', str(old)]
        cli_command = ['node', str(cli)]
        observed = json.loads(command(cli_command + ['status', *flags], base).stdout)
        if observed['status'] != 'legacy':
            raise AssertionError('Existing old-version Skills CLI copy was not detected')
        refused = command(cli_command + ['install', *flags, '--no-tui'], base, success=False)
        if '--migrate' not in refused.stderr or old_entry.read_bytes() != original:
            raise AssertionError('Refused legacy installation was modified or gave no migration guidance')
        command(cli_command + ['install', *flags, '--migrate', '--dry-run'], base)
        if (old_target / '.ui-spec-install.json').exists() or (old / '.agents/ui-spec-studio').exists():
            raise AssertionError('Legacy dry-run made persistent changes')
        migrated = json.loads(command(cli_command + ['install', *flags, '--migrate', '--lang', 'zh'], base).stdout)
        if migrated['result'] != 'upgraded' or migrated['backup'] == str(old_target):
            raise AssertionError('Legacy migration did not report an independent backup')
        backup = Path(migrated['backup'])
        if not backup.is_dir() or (backup / 'SKILL.md').read_bytes() != original:
            raise AssertionError('Legacy source was not preserved byte for byte')
        if not (old_target / '.ui-spec-install.json').exists():
            raise AssertionError('New managed receipt missing')
        restored = json.loads(command(cli_command + ['uninstall', *flags], base).stdout)
        if restored['result'] != 'original-restored' or old_entry.read_bytes() != original:
            raise AssertionError('Uninstall did not automatically restore the legacy original')
        if backup.exists() or (old_target / '.ui-spec-install.json').exists():
            raise AssertionError('Legacy restored copy still carries installer ownership')

        # Identical unowned Skill: the user can explicitly adopt it, but an
        # uninstall must leave those originally pre-existing files in place.
        adopt = base / 'legacy-adopt'
        adopt_target = adopt / '.agents/skills/ui-spec'
        adopt_target.parent.mkdir(parents=True)
        shutil.copytree(source_skill, adopt_target)
        adopt_flags = ['--agent', 'claude-code', '--project', str(adopt)]
        # Claude Code's Skill directory differs from Codex; use the actual host.
        shutil.rmtree(adopt_target)
        adopt_target = adopt / '.claude/skills/ui-spec'
        adopt_target.parent.mkdir(parents=True)
        shutil.copytree(source_skill, adopt_target)
        command(cli_command + ['install', *adopt_flags, '--adopt'], base)
        receipt = json.loads((adopt_target / '.ui-spec-install.json').read_text())
        if not receipt.get('adopted'):
            raise AssertionError('Identical copy was not adopted in place')
        command(cli_command + ['uninstall', *adopt_flags], base)
        if (adopt_target / '.ui-spec-install.json').exists() or not (adopt_target / 'SKILL.md').exists():
            raise AssertionError('Adopted original files were deleted on uninstall')

        # Refuse to replace another unrelated product's directory.
        unrelated = base / 'other-product'
        unrelated_target = unrelated / '.claude/skills/ui-spec'
        unrelated_target.mkdir(parents=True)
        (unrelated_target / 'SKILL.md').write_text('---\nname: unrelated\n---\n', encoding='utf-8')
        command(cli_command + ['install', '--agent', 'claude-code', '--project', str(unrelated), '--migrate'], base, success=False)
        if not (unrelated_target / 'SKILL.md').is_file():
            raise AssertionError('Unrelated Skill file was overwritten')

        # Preserve the symlink itself (including relative-target semantics)
        # while leaving the real backing source completely untouched.
        linked = base / 'legacy-linked'
        linked_store = base / 'legacy-source'
        linked_target = linked / '.agents/skills/ui-spec'
        linked_target.parent.mkdir(parents=True)
        shutil.copytree(source_skill, linked_store)
        linked_bytes = (linked_store / 'SKILL.md').read_bytes()
        linked_created = False
        try:
            if sys.platform == 'win32':
                # Directory junctions do not require Windows Developer Mode.
                cmd = subprocess.run(['cmd', '/c', 'mklink', '/J', str(linked_target), str(linked_store)],
                                     capture_output=True, text=True, timeout=15)
                linked_created = cmd.returncode == 0
                if not linked_created:
                    raise AssertionError('Windows Junction creation failed: ' + cmd.stderr)
            else:
                linked_target.symlink_to(Path(os.path.relpath(linked_store, linked_target.parent)),
                                         target_is_directory=True)
                linked_created = True
        except (OSError, NotImplementedError):
            if sys.platform == 'win32':
                raise  # Junction compatibility must be tested, not skipped.
        if linked_created:
            flags = ['--agent', 'codex', '--project', str(linked)]
            status = json.loads(command(cli_command + ['status', *flags], base).stdout)
            if status['status'] != 'legacy-link':
                raise AssertionError('Linked/Junction legacy installation was not detected')
            result = json.loads(command(cli_command + ['install', *flags, '--migrate'], base).stdout)
            archived_link = Path(result['backup'])
            is_link = lambda path: path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction())
            if not is_link(archived_link) or not linked_target.is_dir() or is_link(linked_target):
                raise AssertionError('Linked source was not safely replaced by ordinary Skill files')
            command(cli_command + ['uninstall', *flags], base)
            if not is_link(linked_target) or (linked_store / 'SKILL.md').read_bytes() != linked_bytes:
                raise AssertionError('Legacy link or its backing source was modified on recovery')

        # An existing lock is a conflict rather than permission to race another installer.
        locked = base / 'locked'
        lock_dir = locked / '.claude/skills'
        lock_dir.mkdir(parents=True)
        (lock_dir / '.ui-spec-install.lock').write_text('another process')
        command(cli_command + ['install', '--agent', 'claude-code', '--project', str(locked)], base, success=False)
        if not (lock_dir / '.ui-spec-install.lock').is_file():
            raise AssertionError('Concurrent install lock was removed without ownership')

        result = command([(shutil.which('npx') or 'npx'), '--yes', '--offline', archive.as_uri(), 'status', '--agent', 'codex', '--project', str(base / 'not-installed')], base)
        if json.loads(result.stdout)['status'] != 'absent':
            raise AssertionError('npx tarball command failed')
        return {'archive': archive.name, 'archive_bytes': archive.stat().st_size,
                'source_checkout': False, 'skill_files': len(expected), 'verified_hosts': project_checks, 'legacy_scenarios': ['copied', 'adopt', 'unrelated', 'symlink-if-supported', 'concurrent-lock'],
                'checksum': hashlib.sha256(archive.read_bytes()).hexdigest()}


if __name__ == '__main__':
    try:
        print(json.dumps(run(), indent=2))
    except (OSError, ValueError, RuntimeError, AssertionError, subprocess.SubprocessError) as exc:
        print(f'installer_smoke: {exc}', file=sys.stderr)
        raise SystemExit(1)
