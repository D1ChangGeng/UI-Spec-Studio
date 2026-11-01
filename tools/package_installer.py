#!/usr/bin/env python3
"""Build a byte-limited, deterministic, npm-executable installer without cloning the source."""
from __future__ import annotations
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile

ROOT = Path(__file__).resolve().parents[1]
TIMESTAMP = 1767225600  # 2026-01-01 UTC


def build_installer(root: Path = ROOT, output_dir: Path | None = None) -> Path:
    root = Path(root)
    version = (root / 'VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Invalid VERSION')
    package = json.loads((root / 'installer/package.json').read_text(encoding='utf-8'))
    if package.get('version') != version or package.get('bin') != {'ui-spec': 'bin/ui-spec.mjs'}:
        raise ValueError('Installer package metadata and VERSION disagree')
    registry = json.loads((root / 'installer/harnesses.json').read_text(encoding='utf-8'))
    if registry.get('schema_version') != 1 or not {'codex', 'claude-code', 'cursor', 'opencode'}.issubset(registry.get('harnesses', {})):
        raise ValueError('Unexpected Harness registry')
    items: dict[str, bytes] = {}
    included_adapters = set()
    for harness in registry['harnesses'].values():
        adapter = harness.get('adapter')
        if adapter:
            entry = adapter.get('entry', '')
            parts = entry.split('/')
            if len(parts) < 3 or parts[0] != 'adapters' or any(part in ('', '.', '..') for part in parts):
                raise ValueError(f'Unsafe adapter entry: {entry}')
            included_adapters.add(parts[1])
    folders = [(root / 'skills/ui-spec', 'skill')]
    folders += [(root / 'integrations' / name, f'adapters/{name}') for name in sorted(included_adapters)]
    for folder, prefix in folders:
        if not folder.is_dir():
            raise ValueError(f'Missing adapter source: {folder}')
        for file in sorted(folder.rglob('*')):
            if file.is_symlink():
                raise ValueError(f'Refusing symlink in installer: {file}')
            if file.is_file():
                if file.name.endswith('.pyc') or '__pycache__' in file.parts:
                    continue
                rel = file.relative_to(folder).as_posix()
                items[f'{prefix}/{rel}'] = file.read_bytes()
    for name in sorted(included_adapters):
        items[f'adapters/{name}/LICENSE'] = (root / 'LICENSE').read_bytes()
    if not any(path == 'skill/SKILL.md' for path in items):
        raise ValueError('Skill entry missing')
    for role in ('ui_researcher', 'ui_integrator', 'ui_challenger', 'ui_experience_observer'):
        if f'adapters/codex/agents/{role}.toml' not in items:
            raise ValueError(f'Missing Codex role: {role}')
    for harness in registry['harnesses'].values():
        adapter = harness.get('adapter')
        if adapter and adapter['entry'] not in items:
            raise ValueError(f"Adapter entry is not bundled: {adapter['entry']}")
    manifest = {'schema_version': 1, 'version': version,
                'files': {path: hashlib.sha256(content).hexdigest() for path, content in sorted(items.items())}}
    files = {
        'package/package.json': (root / 'installer/package.json').read_bytes(),
        'package/harnesses.json': (root / 'installer/harnesses.json').read_bytes(),
        'package/bin/ui-spec.mjs': (root / 'installer/bin/ui-spec.mjs').read_bytes(),
        'package/payload/manifest.json': (json.dumps(manifest, sort_keys=True, indent=2) + '\n').encode(),
    }
    files.update({f'package/payload/{path}': content for path, content in items.items()})
    output = Path(output_dir or root / 'dist') / 'ui-spec-installer.tgz'
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('wb') as raw:
        with gzip.GzipFile(fileobj=raw, mode='wb', filename='', mtime=0, compresslevel=9) as stream:
            with tarfile.open(fileobj=stream, mode='w') as tar:
                for name, data in sorted(files.items()):
                    info = tarfile.TarInfo(name)
                    info.size = len(data)
                    info.mode = 0o755 if name == 'package/bin/ui-spec.mjs' else 0o644
                    info.uid = info.gid = 0
                    info.uname = info.gname = ''
                    info.mtime = TIMESTAMP
                    tar.addfile(info, io.BytesIO(data))
    return output


if __name__ == '__main__':
    print(build_installer())
