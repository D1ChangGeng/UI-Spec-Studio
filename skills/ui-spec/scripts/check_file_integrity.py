#!/usr/bin/env python3
"""Independently compare one local file's SHA-256; no research or design assertions."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
from structural_records import local_file


def compare(root: Path, path: str, expected: str) -> dict:
    if not isinstance(expected, str) or not re.fullmatch(r'[a-fA-F0-9]{64}', expected):
        raise ValueError('Expected SHA-256 must be 64 hexadecimal characters')
    file = local_file(root.resolve(strict=True), path)
    digest = hashlib.sha256()
    with file.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return {'verification_scope': 'one local regular file byte digest', 'path': path,
            'expected_sha256': expected.lower(), 'observed_sha256': digest.hexdigest(),
            'digest_result': 'match' if digest.hexdigest() == expected.lower() else 'mismatch',
            'limits': 'Digest equality does not prove source truth, observation, runtime use, authorization or UI quality.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', required=True, type=Path)
    parser.add_argument('--path', required=True)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    try:
        result = compare(args.project_root, args.path, args.sha256)
        print(json.dumps(result, indent=2))
        return 0 if result['digest_result'] == 'match' else 1
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({'verification_scope': 'one local regular file byte digest',
                          'digest_result': 'not_checked', 'read_problem': str(exc)}, indent=2))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
