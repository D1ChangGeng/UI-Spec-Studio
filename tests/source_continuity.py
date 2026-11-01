"""Reconstruct an identified predecessor for historical tests, without changing old evidence."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path



def runtime_v119(root: Path, path: str) -> bytes:
    """Recover exact v1.19 bytes through v1.20, without modifying old evidence."""
    current = (root / path).read_bytes()
    extension = root / 'docs/evidence/v1.20.0/continuity.json'
    if not extension.is_file():
        return current
    ledger = json.loads(extension.read_text(encoding='utf-8'))
    rows = [row for row in ledger['files'] if row['path'] == path]
    if len(rows) != 1:
        raise ValueError(f'Unknown or duplicate v1.20 continuity path: {path}')
    row = rows[0]
    if hashlib.sha256(current).hexdigest() != row['current_sha256']:
        raise ValueError(f'Current source differs from v1.20 identity: {path}')
    lines = current.decode('utf-8').splitlines(keepends=True)
    for edit in reversed(row['inverse_edits']):
        a, b = edit['current_start_line'], edit['current_end_line']
        fragment = ''.join(lines[a:b]).encode('utf-8')
        if hashlib.sha256(fragment).hexdigest() != edit['current_fragment_sha256']:
            raise ValueError(f'Inverse v1.20 fragment differs: {path}')
        lines[a:b] = edit['prior_text'].splitlines(keepends=True)
    prior = ''.join(lines).encode('utf-8')
    if hashlib.sha256(prior).hexdigest() != row['prior_sha256']:
        raise ValueError(f'Restored v1.19 source differs: {path}')
    return prior

def runtime_v118(root: Path, path: str) -> bytes:
    """Restore exact v1.18 bytes through the reviewed v1.19 delta, without writes."""
    current = runtime_v119(root, path)
    extension = root / 'docs/evidence/v1.19.0/continuity.json'
    if not extension.is_file():
        return current
    ledger = json.loads(extension.read_text(encoding='utf-8'))
    rows = [row for row in ledger['files'] if row['path'] == path]
    if len(rows) != 1:
        raise ValueError(f'Unknown or duplicate v1.19 continuity path: {path}')
    row = rows[0]
    if hashlib.sha256(current).hexdigest() != row['current_sha256']:
        raise ValueError(f'Current source differs from v1.19 reviewed identity: {path}')
    lines = current.decode('utf-8').splitlines(keepends=True)
    for edit in reversed(row['inverse_edits']):
        a, b = edit['current_start_line'], edit['current_end_line']
        fragment = ''.join(lines[a:b]).encode('utf-8')
        if hashlib.sha256(fragment).hexdigest() != edit['current_fragment_sha256']:
            raise ValueError(f'Inverse v1.19 fragment differs: {path}')
        lines[a:b] = edit['prior_text'].splitlines(keepends=True)
    prior = ''.join(lines).encode('utf-8')
    if hashlib.sha256(prior).hexdigest() != row['prior_sha256']:
        raise ValueError(f'Restored v1.18 source differs: {path}')
    return prior


def runtime_v117(root: Path, path: str) -> bytes:
    """Restore the exact v1.17 runtime through the reviewed v1.18 delta."""
    current = runtime_v118(root, path)
    extension = root / 'docs/evidence/v1.18.0/continuity.json'
    if not extension.is_file():
        return current
    ledger = json.loads(extension.read_text(encoding='utf-8'))
    rows = [row for row in ledger['files'] if row['path'] == path]
    if len(rows) != 1:
        raise ValueError(f'Unknown or duplicate v1.18 continuity path: {path}')
    row = rows[0]
    if hashlib.sha256(current).hexdigest() != row['current_sha256']:
        raise ValueError(f'Current source differs from v1.18 reviewed identity: {path}')
    lines = current.decode('utf-8').splitlines(keepends=True)
    for edit in reversed(row['inverse_edits']):
        a, b = edit['current_start_line'], edit['current_end_line']
        fragment = ''.join(lines[a:b]).encode('utf-8')
        if hashlib.sha256(fragment).hexdigest() != edit['current_fragment_sha256']:
            raise ValueError(f'Inverse v1.18 fragment differs: {path}')
        lines[a:b] = edit['prior_text'].splitlines(keepends=True)
    prior = ''.join(lines).encode('utf-8')
    if hashlib.sha256(prior).hexdigest() != row['prior_sha256']:
        raise ValueError(f'Restored v1.17 source differs: {path}')
    return prior


def runtime_v1161(root: Path, path: str) -> bytes:
    """Restore the exact v1.16.1 runtime through the reviewed v1.17 delta."""
    current = runtime_v117(root, path)
    extension = root / 'docs/evidence/v1.17.0/continuity.json'
    if not extension.is_file():
        return current
    ledger = json.loads(extension.read_text(encoding='utf-8'))
    rows = [row for row in ledger['files'] if row['path'] == path]
    if len(rows) != 1:
        raise ValueError(f'Unknown or duplicate v1.17 continuity path: {path}')
    row = rows[0]
    if hashlib.sha256(current).hexdigest() != row['current_sha256']:
        raise ValueError(f'Current source differs from v1.17 reviewed identity: {path}')
    lines = current.decode('utf-8').splitlines(keepends=True)
    for edit in reversed(row['inverse_edits']):
        a, b = edit['current_start_line'], edit['current_end_line']
        fragment = ''.join(lines[a:b]).encode('utf-8')
        if hashlib.sha256(fragment).hexdigest() != edit['current_fragment_sha256']:
            raise ValueError(f'Inverse v1.17 fragment differs: {path}')
        lines[a:b] = edit['prior_text'].splitlines(keepends=True)
    prior = ''.join(lines).encode('utf-8')
    if hashlib.sha256(prior).hexdigest() != row['prior_sha256']:
        raise ValueError(f'Restored v1.16.1 source differs: {path}')
    return prior


def runtime_v116(root: Path, path: str) -> bytes:
    """Recover the exact released v1.16 source, validating current and inverse bytes."""
    extension = root / 'docs/evidence/v1.16.1/continuity.json'
    current = runtime_v1161(root, path)
    if not extension.is_file():
        return current
    ledger = json.loads(extension.read_text(encoding='utf-8'))
    rows = [row for row in ledger['files'] if row['path'] == path]
    if len(rows) != 1:
        raise ValueError(f'Unknown or duplicate reconciliation path: {path}')
    row = rows[0]
    if hashlib.sha256(current).hexdigest() != row['current_sha256']:
        raise ValueError(f'Current source differs from reconciled identity: {path}')
    lines = current.decode('utf-8').splitlines(keepends=True)
    for edit in reversed(row['inverse_edits']):
        a, b = edit['current_start_line'], edit['current_end_line']
        fragment = ''.join(lines[a:b]).encode('utf-8')
        if hashlib.sha256(fragment).hexdigest() != edit['current_fragment_sha256']:
            raise ValueError(f'Inverse reconciliation fragment differs: {path}')
        lines[a:b] = edit['prior_text'].splitlines(keepends=True)
    original = ''.join(lines).encode('utf-8')
    if hashlib.sha256(original).hexdigest() != row['prior_sha256']:
        raise ValueError(f'Reconstructed reconciliation predecessor differs: {path}')
    return original


def predecessor_runtime(root: Path, path: str) -> bytes:
    ledger = json.loads((root / 'docs/evidence/v1.16.0/continuity.json').read_text(encoding='utf-8'))
    matches = [row for row in ledger['files'] if row['path'] == path]
    if len(matches) != 1:
        raise ValueError(f'Unknown or duplicate predecessor path: {path}')
    row = matches[0]
    current = runtime_v116(root, path)
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
