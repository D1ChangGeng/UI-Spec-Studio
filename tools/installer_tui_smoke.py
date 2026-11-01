#!/usr/bin/env python3
"""Exercise Clack's real interactive, Unicode terminal flow under a POSIX PTY."""
from __future__ import annotations
import os
import fcntl
import struct
import termios
from pathlib import Path
import pty
import select
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from package_installer import build_installer


def wizard(cmd: list[str], project: Path, keys: bytes, *, timeout: float = 35) -> str:
    master, slave = pty.openpty()
    # pty.openpty() has zero terminal columns on some CI runners; Clack
    # will wrap every character if this width is not initialized.
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 44, 140, 0, 0))
    env = dict(os.environ, CI='false', TERM='xterm-256color', NO_COLOR='1')
    proc = subprocess.Popen(cmd, cwd=project, env=env, stdin=slave, stdout=slave, stderr=slave,
                            start_new_session=True)
    os.close(slave)
    sent = False
    text = bytearray()
    end = time.monotonic() + timeout
    try:
        while time.monotonic() < end:
            ready, _, _ = select.select([master], [], [], 0.2)
            if ready:
                try:
                    chunk = os.read(master, 65536)
                except OSError:
                    chunk = b''
                if chunk:
                    text.extend(chunk)
                    if not sent and b'How should this Skill be handled?' in text:
                        os.write(master, keys)
                        sent = True
            if proc.poll() is not None:
                break
        if proc.poll() is None:
            proc.kill()
            raise AssertionError('Installer terminal flow did not complete; keys sent=' + str(sent) + '\n' + text.decode('utf-8', 'replace')[-4500:])
        output = text.decode('utf-8', 'replace')
        if not sent:
            raise AssertionError('No interactive migration choice was shown: ' + output[-1000:])
        if proc.returncode != 0:
            raise AssertionError('Interactive installer failed: ' + output[-1200:])
        if 'UI SPEC STUDIO' not in output:
            raise AssertionError('Terminal product title missing')
        return output
    finally:
        os.close(master)
        if proc.poll() is None:
            proc.kill()
        proc.wait(timeout=5)


def run() -> None:
    if os.name != 'posix':
        raise SystemExit('Interactive POSIX PTY test runs on Ubuntu; Windows native behavior has separate smoke tests')
    with tempfile.TemporaryDirectory(prefix='ui-spec-terminal-') as td:
        root = Path(td)
        archive = build_installer(ROOT, root)
        with tarfile.open(archive) as tar:
            tar.extractall(root / 'extracted', filter='data')
        package = root / 'extracted/package'
        # npm resolves the pinned, mature Clack UI for real terminal behavior;
        # the ordinary offline smoke tests require no dependency download.
        npm = shutil.which('npm') or 'npm'
        install = subprocess.run(
            [npm, 'install', '--prefix', str(package), '--ignore-scripts',
             '--no-package-lock', '--no-save', '--no-audit', '--no-fund'],
            capture_output=True, text=True, timeout=100
        )
        if install.returncode or not (package / 'node_modules/@clack/prompts/package.json').is_file():
            raise AssertionError('Real @clack/prompts library unavailable:\n' + install.stderr)
        project = root / 'project'
        target = project / '.agents/skills/ui-spec'
        target.parent.mkdir(parents=True)
        shutil.copytree(package / 'payload/skill', target)
        before = (target / 'SKILL.md').read_bytes().replace(b'version: "1.20.2"', b'version: "1.20.1"')
        (target / 'SKILL.md').write_bytes(before)
        cmd = ['node', str(package / 'bin/ui-spec.mjs'), 'install', '--agent', 'codex',
               '--project', str(project), '--lang', 'en']
        # The second menu choice is to leave the installation untouched.
        output = wizard(cmd, project, b'\x1b[B\r')
        if (target / 'SKILL.md').read_bytes() != before or (target / '.ui-spec-install.json').exists():
            raise AssertionError('Cancel/keep choice unexpectedly modified the existing installation')
        if 'No changes' not in output and 'No changes' not in output.replace('\r', ''):
            raise AssertionError('Expected a clear cancellation/keep result')
        # Default choice: make a reversible backup and install the new Skill.
        output = wizard(cmd, project, b'\r')
        if not (target / '.ui-spec-install.json').is_file():
            raise AssertionError('Interactive migration did not install the managed Skill')
        if 'files' not in output.lower() or 'verified' not in output.lower():
            raise AssertionError('Meaningful terminal verification/progress evidence absent')
        removed = subprocess.run(
            ['node', str(package / 'bin/ui-spec.mjs'), 'uninstall', '--agent', 'codex',
             '--project', str(project), '--no-tui'],
            capture_output=True, text=True, timeout=35
        )
        if removed.returncode or (target / 'SKILL.md').read_bytes() != before:
            raise AssertionError('Interactive migration did not preserve and restore original files:\n' + removed.stderr)
        print('Clack terminal prompts, choice preservation, file progress and restore: PASS')


if __name__ == '__main__':
    run()
