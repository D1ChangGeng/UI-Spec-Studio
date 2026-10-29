#!/usr/bin/env python3
"""Restore one exact application-study snapshot without modifying the archive."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile


def relative_name(value: str) -> Path:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or '..' in path.parts or path.as_posix() != value:
        raise ValueError(f'Unsafe or noncanonical archive path: {value!r}')
    if '\\' in value or ':' in value or value == '.':
        raise ValueError(f'Nonportable archive path: {value!r}')
    return Path(*path.parts)


def restore(archive: Path, output: Path, stage: str = 'final') -> dict:
    archive = archive.resolve()
    if output.exists():
        raise ValueError('Output already exists; choose a new directory to preserve existing work')
    index = json.loads((archive/'archive-index.json').read_text(encoding='utf-8'))
    rows = index['snapshots'][stage]['files']
    recovered = []
    for original, item in rows.items():
        destination = relative_name(original)
        stored = (archive/relative_name(item['path'])).resolve()
        if not stored.is_relative_to(archive):
            raise ValueError(f'Archive source escapes its directory: {item["path"]}')
        if 'member' in item:
            member = relative_name(item['member']).as_posix()
            with zipfile.ZipFile(stored) as bundle:
                content = bundle.read(member)
        else:
            content = stored.read_bytes()
        if hashlib.sha256(content).hexdigest() != item['sha256']:
            raise ValueError(f'Original-byte identity mismatch: {original}')
        recovered.append((destination, content))
    # Validate the complete snapshot before creating any output files.
    output.mkdir(parents=True)
    for destination, content in recovered:
        target = output/destination
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    return {'cell': index['cell'], 'stage': stage, 'files': len(recovered),
            'bytes': sum(len(content) for _, content in recovered),
            'sha256_verification': 'all_original_files_match', 'output': str(output.resolve())}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path, help='Published runs/<cell> directory')
    parser.add_argument('output', type=Path, help='New destination directory')
    parser.add_argument('--stage', choices=('initial', 'final'), default='final')
    args = parser.parse_args()
    try:
        result = restore(args.archive, args.output, args.stage)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        parser.exit(1, f'Cannot restore snapshot: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
