"""Preserve oversized original files in independently verified ZIP pieces."""
from pathlib import Path
import hashlib
import zipfile
from archive_evidence_v2 import bounded_archives, write_json

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def archive_with_large_files(source, paths, output, stem):
    normal = [p for p in paths if p.stat().st_size <= 7_500_000]
    result = bounded_archives(source, normal, output, stem)
    result['split_files'] = []
    for path in sorted(set(paths) - set(normal)):
        raw = path.read_bytes()
        record = {'path': path.relative_to(source).as_posix(), 'bytes': len(raw),
                  'sha256': sha(raw), 'parts': []}
        for i, start in enumerate(range(0, len(raw), 7_500_000), 1):
            piece = raw[start:start + 7_500_000]
            name = f'large-object-{record["sha256"][:16]}-part-{i:03d}.zip'
            archive = output / name
            if archive.exists():
                raise FileExistsError(archive)
            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
                z.writestr('payload', piece)
            with zipfile.ZipFile(archive) as z:
                if z.read('payload') != piece:
                    raise ValueError('Large original piece mismatch')
            record['parts'].append({'file': name, 'sha256': sha(archive.read_bytes()),
                                    'member': 'payload', 'payload_sha256': sha(piece),
                                    'payload_bytes': len(piece)})
        result['split_files'].append(record)
    return result

def restore_large_files(records, run, output, safe):
    for record in records:
        chunks = []
        for part in record['parts']:
            path = safe(run, part['file'])
            if sha(path.read_bytes()) != part['sha256']:
                raise ValueError('Large archive identity mismatch')
            with zipfile.ZipFile(path) as z:
                raw = z.read(part['member'])
            if len(raw) != part['payload_bytes'] or sha(raw) != part['payload_sha256']:
                raise ValueError('Large piece identity mismatch')
            chunks.append(raw)
        raw = b''.join(chunks)
        if len(raw) != record['bytes'] or sha(raw) != record['sha256']:
            raise ValueError('Reassembled original identity mismatch')
        path = safe(output, record['path'])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
