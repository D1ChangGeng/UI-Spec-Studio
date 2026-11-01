#!/usr/bin/env python3
"""Verify or restore owner-only original records over a public study workspace."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--public-workspace', type=Path, required=True)
    parser.add_argument('--private-archive', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    source = args.public_workspace.resolve()
    if args.output is not None and args.output.exists():
        raise FileExistsError('Choose a fresh private output directory')
    with zipfile.ZipFile(args.private_archive) as archive:
        hashes = json.loads(archive.read('ORIGINAL-WORKSPACE-HASHES.json'))
        names = set(archive.namelist())
        original_members = names - {'ORIGINAL-WORKSPACE-HASHES.json', 'README.txt'}
        if not original_members <= set(hashes):
            raise ValueError('Unexpected private archive member')
        for name, expected in hashes.items():
            path = (source / name).resolve()
            path.relative_to(source)
            raw = archive.read(name) if name in original_members else path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != expected:
                raise ValueError('Original reconstruction hash differs: ' + name)
        if args.output is not None:
            shutil.copytree(source, args.output, copy_function=shutil.copy2)
            output = args.output.resolve()
            for name in original_members:
                path = (output / name).resolve()
                path.relative_to(output)
                path.write_bytes(archive.read(name))
    print(json.dumps({'status': 'passed', 'verified_original_files': len(hashes),
                      'private_original_files': len(original_members),
                      'mode': 'restored' if args.output is not None else 'verified_without_writing',
                      'scope': 'Complete original participant bytes; session-bearing values are not printed. Keep the restored workspace private.'}, indent=2))


if __name__ == '__main__':
    main()
