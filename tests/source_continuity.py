"""Reconstruct an identified predecessor for historical tests, without changing old evidence."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path


def predecessor_runtime(root: Path, path: str) -> bytes:
    ledger = json.loads((root / 'docs/evidence/v1.16.0/continuity.json').read_text(encoding='utf-8'))
    matches = [row for row in ledger['files'] if row['path'] == path]
    if len(matches) != 1:
        raise ValueError(f'Unknown or duplicate predecessor path: {path}')
    row = matches[0]
    current = (root / path).read_bytes()
    if hashlib.sha256(current).hexdigest() != row['current_sha256']:
        raise ValueError(f'Current source differs from reviewed identity: {path}')
    lines = current.decode('utf-8').splitlines(keepends=True)
    for edit in reversed(row['inverse_edits']):
        a, b = edit['current_start_line'], edit['current_end_line']
        fragment = ''.join(lines[a:b]).encode('utf-8')
        if hashlib.sha256(fragment).hexdigest() != edit['current_fragment_sha256']:
            raise ValueError(f'Inverse fragment differs: {path}')
        lines[a:b] = edit['prior_text'].splitlines(keepends=True)
    original = ''.join(lines).encode('utf-8')
    if hashlib.sha256(original).hexdigest() != row['prior_sha256']:
        raise ValueError(f'Reconstructed predecessor differs: {path}')
    return original
