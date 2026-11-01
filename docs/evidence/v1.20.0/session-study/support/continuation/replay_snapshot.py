#!/usr/bin/env python3
"""Reconstruct a frozen participant from retained input/overlay ZIPs and verify every file."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,shutil,zipfile
from large_archives import restore_large_files

def digest(raw):return hashlib.sha256(raw).hexdigest()
def safe(root,rel):
    p=PurePosixPath(rel)
    if p.is_absolute() or '..' in p.parts or '\\' in rel or any(':' in x for x in p.parts):raise ValueError('Unsafe archive path')
    target=root.joinpath(*p.parts)
    if not target.resolve().is_relative_to(root.resolve()):raise ValueError('Outside reconstruction root')
    return target

def extract(path,output,prefix=''):
    with zipfile.ZipFile(path) as z:
        for item in z.infolist():
            if item.is_dir():continue
            target=safe(output,prefix+item.filename)
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(z.read(item))
            mode=(item.external_attr>>16)&0o777
            if mode:target.chmod(mode)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,required=True);p.add_argument('--cell',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--snapshot-directory',type=Path)
    a=p.parse_args();study=a.repo/'docs/evidence/v1.20.0/session-study';run=a.snapshot_directory if a.snapshot_directory else study/'runs'/a.cell
    plan=json.loads((study/'registration.json').read_text());cell=next(c for c in plan['cells'] if c['id']==a.cell)
    snapshot=json.loads((run/'snapshot.json').read_text());a.output.mkdir(parents=True,exist_ok=False)
    for ref in cell['input_artifacts']:
        path=safe(a.repo,ref['path']);raw=path.read_bytes()
        if digest(raw)!=ref['sha256']:raise ValueError('Input identity differs')
        if path.suffix=='.zip':
            prefix='method/' if path.name.startswith('method-v') else ('roles/' if path.name=='distributed-role-instructions.zip' else '')
            extract(path,a.output,prefix)
    for record in snapshot['overlay']['archives']:
        path=safe(run,record['file'])
        if digest(path.read_bytes())!=record['sha256']:raise ValueError('Overlay identity differs')
        extract(path,a.output)
    restore_large_files(snapshot['overlay'].get('split_files',[]),run,a.output,safe)
    for name in snapshot['deleted_paths']:
        path=safe(a.output,name)
        if path.exists():path.unlink()
    for name,mode in snapshot['workspace_modes'].items():safe(a.output,name).chmod(int(mode,8))
    actual={p.relative_to(a.output).as_posix():digest(p.read_bytes()) for p in a.output.rglob('*') if p.is_file()}
    expected=snapshot['workspace_files']
    if actual!=expected:
        raise ValueError(json.dumps({'missing':sorted(set(expected)-set(actual)),'extra':sorted(set(actual)-set(expected)),'different':sorted(k for k in expected.keys()&actual.keys() if expected[k]!=actual[k])}))
    print(json.dumps({'cell_id':a.cell,'status':'passed','verified_files':len(actual),'input_archives':len(cell['input_artifacts']),'overlay_archives':len(snapshot['overlay']['archives']),'scope':'Byte-complete reconstructed captured workspace excluding the declared dependency/runtime caches. This is an archive integrity check, not new agent work or product-quality acceptance.'},indent=2))
if __name__=='__main__':main()
