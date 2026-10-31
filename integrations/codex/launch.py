#!/usr/bin/env python3
"""Launch Codex with all four installed roles registered for this invocation.

Python 3.11+, standard library only. Inherits model, authentication, permissions,
stdio and environment. Does not install files or write a Codex profile.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

try:
    import tomllib
except ImportError:
    tomllib = None

sys.path.insert(0, str(Path(__file__).absolute().parent))
import install


class LaunchError(ValueError):
    pass


def config_key(assignment: str) -> tuple[list[str], str]:
    """Parse quoted/dotted TOML keys without interpreting the caller's value."""
    key, separator, value = assignment.partition('=')
    if not separator or not key.strip():
        raise LaunchError('Codex --config requires a key=value assignment')
    try:
        current = tomllib.loads(key.strip() + ' = 0')
    except (ValueError, TypeError) as exc:
        raise LaunchError('Codex --config has an invalid TOML key') from exc
    parts = []
    while isinstance(current, dict) and len(current) == 1:
        name, current = next(iter(current.items()))
        parts.append(name)
    if current != 0 or isinstance(current, bool) or not parts:
        raise LaunchError('Codex --config must contain one dotted key')
    return parts, value.strip()


def check_forwarded_args(args: list[str]) -> None:
    """Protect the selected working directory and four native registrations."""
    index = 0
    while index < len(args):
        token = args[index]
        if token == '--':
            break  # Native option terminator: following text is a literal prompt.
        if token in ('-C', '--cd') or token.startswith('--cd=') or token.startswith('-C'):
            raise LaunchError('Choose the working directory with --project, or run --user from it; do not forward --cd/-C')
        assignment = None
        if token in ('-c', '--config'):
            index += 1
            if index == len(args):
                raise LaunchError('Missing value after Codex --config/-c')
            assignment = args[index]
        elif token.startswith('--config='):
            assignment = token[len('--config='):]
        elif token.startswith('-c') and token != '-c':
            assignment = token[2:].removeprefix('=')
        if assignment is not None:
            parts, value = config_key(assignment)
            if parts == ['agents'] or (len(parts) > 1 and parts[0] == 'agents' and parts[1] in install.ROLES):
                raise LaunchError('Forwarded config conflicts with the four installed UI Spec role registrations')
            if parts == ['features']:
                raise LaunchError('Use individual feature settings; replacing the features table can disable the required multi_agent feature')
            if parts in (['agents', 'enabled'], ['features', 'multi_agent']) and value != 'true':
                raise LaunchError('The launcher requires native multi-agent support; conflicting disable setting rejected')
        disabled = None
        if token == '--disable':
            index += 1
            if index == len(args):
                raise LaunchError('Missing feature after Codex --disable')
            disabled = args[index]
        elif token.startswith('--disable='):
            disabled = token[len('--disable='):]
        if disabled == 'multi_agent':
            raise LaunchError('The launcher enables multi_agent for this invocation; conflicting --disable rejected')
        index += 1


def installed_roles(root: Path) -> list[tuple[str, Path, str]]:
    if '..' in root.parts or any(character in str(root) for character in ('\x00', '\n', '\r')):
        raise LaunchError('Role installation path contains unsafe components')
    roles = []
    for name in install.ROLES:
        path = install.safe(root, f'agents/{name}.toml')
        raw = install.regular(path)
        if raw is None:
            raise LaunchError(f'Installed role is missing: {path}; run install.py for this scope first')
        try:
            data = tomllib.loads(raw.decode('utf-8'))
        except (ValueError, UnicodeError) as exc:
            raise LaunchError(f'Installed role is not valid UTF-8 TOML: {path}') from exc
        if data.get('name') != name:
            raise LaunchError(f'Installed role identity does not match {name}: {path}')
        extra = set(data) - {'name', 'description', 'developer_instructions'}
        if extra:
            raise LaunchError(f'Installed role {name} has unsupported configuration keys: {", ".join(sorted(extra))}; use normal Codex options for model and permission settings')
        for field in ('description', 'developer_instructions'):
            if not isinstance(data.get(field), str) or not data[field].strip():
                raise LaunchError(f'Installed role {name} needs a nonempty {field}')
        roles.append((name, path, data['description']))
    return roles


def command(project: str | None, user: bool, executable: str, args: list[str]) -> tuple[list[str], Path]:
    if tomllib is None:
        raise LaunchError('The launcher requires Python 3.11+ to validate installed TOML roles')
    check_forwarded_args(args)
    root = install.codex_root(project, user)
    cwd = root.parent if project else Path.cwd()
    if not cwd.is_dir():
        raise LaunchError(f'Working directory does not exist: {cwd}')
    roles = installed_roles(root)
    if not executable or any(character in executable for character in ('\x00', '\n', '\r')):
        raise LaunchError('Codex executable must be a command name or a local executable path')
    found = shutil.which(executable)
    if found is None:
        raise LaunchError('Codex executable was not found; provide --codex-executable PATH or install Codex')
    # Resolve before changing cwd, so a relative executable keeps its meaning.
    result = [str(Path(found).absolute()), '--enable', 'multi_agent', '-c', 'agents.enabled=true']
    for name, path, description in roles:
        result += ['-c', f'agents.{name}.config_file=' + json.dumps(str(path)),
                   '-c', f'agents.{name}.description=' + json.dumps(description)]
    return result + args, cwd


def run(argv: list[str], cwd: Path) -> int:
    # Keep the foreground process group and stdio. Ctrl-C reaches Codex directly;
    # continue waiting if it cancels a turn rather than exiting the interactive UI.
    with subprocess.Popen(argv, cwd=cwd) as process:
        while True:
            try:
                code = process.wait()
                return 128 - code if code < 0 else code
            except KeyboardInterrupt:
                continue


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument('--project')
    scope.add_argument('--user', action='store_true')
    parser.add_argument('--codex-executable', default='codex')
    parser.add_argument('--dry-run', action='store_true', help='Print the exact argv as JSON; do not start Codex or write files')
    parser.add_argument('codex_args', nargs=argparse.REMAINDER, help='Codex arguments after --')
    values = parser.parse_args(argv)
    forwarded = values.codex_args
    if forwarded and forwarded[0] != '--':
        parser.error('Separate Codex arguments with --')
    forwarded = forwarded[1:] if forwarded else []
    try:
        launch_argv, cwd = command(values.project, values.user, values.codex_executable, forwarded)
        if values.dry_run:
            print(json.dumps(launch_argv, ensure_ascii=False, indent=2))
            return 0
        return run(launch_argv, cwd)
    except (OSError, ValueError) as exc:
        print(f'Cannot launch Codex: {exc}', file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == '__main__':
    raise SystemExit(main())
