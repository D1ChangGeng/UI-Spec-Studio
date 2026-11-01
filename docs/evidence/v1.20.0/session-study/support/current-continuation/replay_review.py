#!/usr/bin/env python3
"""Reconstruct a fresh reviewer with verified frozen-product byte reuse."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'continuation'))
from replay_snapshot import safe, extract
from review_snapshot_io import read_snapshot
from large_archives import restore_large_files


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    path = args.snapshot.resolve()
    snapshot = read_snapshot(path)
    if snapshot.get('previous_snapshot'):
        raise ValueError('Fresh reviewer reconstruction requires an independent initial snapshot')
    borrowed = {}
    for part in snapshot.get('borrowed_inventory_parts', []):
        source = safe(path.parent, part['file'])
        if sha(source) != part['sha256'] or source.stat().st_size != part['bytes']:
            raise ValueError('Borrowed inventory part differs')
        values = json.loads(source.read_text())
        if len(values) != part['entries'] or set(values).intersection(borrowed):
            raise ValueError('Invalid or duplicate borrowed inventory entries')
        borrowed.update(values)
    if len(borrowed) != snapshot.get('borrowed_files_count', 0):
        raise ValueError('Borrowed file count differs')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    temporary = Path(tempfile.mkdtemp(prefix='review-product-byte-reuse-'))
    try:
        for index in sorted({item['source_index'] for item in borrowed.values()}):
            spec = snapshot['borrowed_sources'][index]
            source_snapshot = safe(repo, spec['snapshot']['path'])
            if sha(source_snapshot) != spec['snapshot']['sha256']:
                raise ValueError('Borrowed source snapshot differs')
            replay = temporary / str(index)
            result = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / 'continuation/replay_snapshot.py'),
                                     '--repo', str(repo), '--cell', spec['cell_id'],
                                     '--snapshot-directory', str(source_snapshot.parent), '--output', str(replay)], check=False)
            if result.returncode:
                raise ValueError('Borrowed source reconstruction failed')
            for name, item in borrowed.items():
                if item['source_index'] != index:
                    continue
                original = safe(replay, item['original_path'])
                if sha(original) != item['sha256']:
                    raise ValueError('Borrowed original bytes differ')
                target = safe(output, name)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(original, target)
            shutil.rmtree(replay)
        for item in snapshot['archives']['archives']:
            archive = safe(path.parent, item['file'])
            if sha(archive) != item['sha256']:
                raise ValueError('Review overlay archive differs')
            extract(archive, output)
        restore_large_files(snapshot['archives'].get('split_files', []), path.parent, output, safe)
        actual = {p.relative_to(output).as_posix(): sha(p) for p in output.rglob('*') if p.is_file()}
        if actual != snapshot['file_hashes']:
            raise ValueError('Reconstructed reviewer differs from full original file inventory')
        for name, target in snapshot.get('symbolic_links', {}).items():
            link = safe(output, name)
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(target)
            if os.readlink(link) != target:
                raise ValueError('Original symbolic link target differs')
        print(json.dumps({'status': 'passed', 'restored_symbolic_links': len(snapshot.get('symbolic_links', {})), 'verified_files': len(actual), 'borrowed_files': len(borrowed),
                          'scope': 'Byte-complete reconstruction of the retained reviewer snapshot with verified product-byte reuse; not an additional review or acceptance.'}, indent=2))
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


if __name__ == '__main__':
    main()
