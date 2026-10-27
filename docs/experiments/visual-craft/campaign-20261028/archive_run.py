"""Retain a complete frozen run and its independent observations, without editing it."""
from pathlib import Path
import hashlib, json, sys, tarfile, gzip

base = Path(__file__).resolve().parents[1]
rid = sys.argv[1]
frozen = base / 'frozen' / rid
evaluation = base / 'evaluations' / rid
if not (frozen / 'FROZEN.json').exists() or not (evaluation / 'results.json').exists():
    raise SystemExit('Both freeze and independent evaluation are required')
dest = base / 'archives'
dest.mkdir(exist_ok=True)
target = dest / (rid + '.tar.gz')
manifest = {'run_id': rid, 'scope': 'Complete frozen app, original freeze manifest, and independent evaluation; external shared node_modules must be recreated from the registered runtime lock.', 'files': []}

def add_tree(tar, folder, prefix):
    for p in sorted(folder.rglob('*')):
        rel = p.relative_to(folder)
        if p.is_symlink():
            # Original absolute host links are documented but not recreated on extraction.
            manifest['files'].append({'path': str(Path(prefix) / rel), 'symlink_target': str(p.readlink()), 'archived': False})
        elif p.is_file():
            data = p.read_bytes()
            name = str(Path(prefix) / rel)
            manifest['files'].append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'archived': True})
            info = tar.gettarinfo(str(p), arcname=name)
            info.uid = info.gid = 0
            info.uname = info.gname = ''
            info.mtime = 0
            with p.open('rb') as stream:
                tar.addfile(info, stream)

with target.open('wb') as raw:
    with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0, compresslevel=6) as gz:
        with tarfile.open(fileobj=gz, mode='w|') as tar:
            add_tree(tar, frozen, 'frozen')
            add_tree(tar, evaluation, 'independent-evaluation')
manifest['archive'] = {'file': target.name, 'bytes': target.stat().st_size, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
manifest['parts'] = []
part_dir = dest / 'parts'
part_dir.mkdir(exist_ok=True)
with target.open('rb') as source:
    index = 0
    while data := source.read(8388606):
        index += 1
        part = part_dir / (target.name + '.part' + str(index).zfill(2))
        part.write_bytes(data)
        git_blob_sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        manifest['parts'].append({'file': part.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'git_blob_sha': git_blob_sha})
(dest / (rid + '.manifest.json')).write_text(json.dumps(manifest, indent=2) + '\n')
with tarfile.open(target) as tar:
    actual = {member.name for member in tar.getmembers() if member.isfile()}
expected = {row['path'] for row in manifest['files'] if row['archived']}
if actual != expected:
    raise SystemExit('Archive member verification failed')
print(json.dumps({'run_id': rid, 'files': len(actual), **manifest['archive']}))
