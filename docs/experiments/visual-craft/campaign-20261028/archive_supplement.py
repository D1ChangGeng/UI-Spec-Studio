"""Archive supplemental observations without changing original run archives."""
from pathlib import Path
import gzip
import hashlib
import json
import tarfile

base = Path(__file__).resolve().parents[1]
assignment = json.loads((base / 'private/assignment.frozen.json').read_text())
run_ids = sorted(r['run_id'] for wave in assignment['waves'] for r in wave)
for rid in run_ids:
    path = base / 'contract-supplement' / rid / 'results.json'
    if not path.exists() or not json.loads(path.read_text()).get('finishedAt'):
        raise SystemExit('Incomplete supplemental observations: ' + rid)
dest = base / 'archives'
target = dest / 'contract-supplement.tar.gz'
manifest = {'scope': 'Additional independent observations for already published task-contract conditions; all frozen application sources remain unchanged', 'runs': run_ids, 'files': [], 'parts': []}
with target.open('wb') as raw:
    with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0, compresslevel=6) as gz:
        with tarfile.open(fileobj=gz, mode='w|') as archive:
            files = list((base / 'contract-supplement').rglob('*')) + list((base / 'contract-supplement-history').rglob('*'))
            for p in sorted(files):
                if not p.is_file():
                    continue
                rel = str(p.relative_to(base))
                data = p.read_bytes()
                manifest['files'].append({'path': rel, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
                info = archive.gettarinfo(str(p), arcname=rel)
                info.uid = info.gid = info.mtime = 0
                info.uname = info.gname = ''
                with p.open('rb') as stream:
                    archive.addfile(info, stream)
manifest['archive'] = {'file': target.name, 'bytes': target.stat().st_size, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
with target.open('rb') as stream:
    index = 0
    while data := stream.read(8388606):
        index += 1
        p = dest / 'parts' / (target.name + '.part' + str(index).zfill(2))
        p.write_bytes(data)
        manifest['parts'].append({'file': p.name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'git_blob_sha': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()})
(dest / 'contract-supplement.manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'archive': manifest['archive'], 'files': len(manifest['files']), 'parts': len(manifest['parts'])}))
