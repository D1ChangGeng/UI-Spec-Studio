#!/usr/bin/env python3
"""Restore exact registered inputs into absent worksets after a host reset."""
from pathlib import Path
import argparse, datetime, hashlib, json
from replay_snapshot import extract

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,required=True)
p.add_argument('cells',nargs='+')
a=p.parse_args()
study=a.repo/'docs/evidence/v1.20.0/session-study'
plan=json.loads((study/'registration.json').read_text())
records=[]
for name in a.cells:
    cell=next(c for c in plan['cells'] if c['id']==name)
    work=Path(cell['work_package'])
    if work.exists():raise ValueError('Refusing to overwrite existing workset: '+str(work))
    work.mkdir(parents=True)
    for ref in cell['input_artifacts']:
        archive=a.repo/ref['path']
        if hashlib.sha256(archive.read_bytes()).hexdigest()!=ref['sha256']:raise ValueError('Frozen input differs')
        prefix='method/' if archive.name.startswith('method-v') else ('roles/' if archive.name=='distributed-role-instructions.zip' else '')
        extract(archive,work,prefix)
    actual={p.relative_to(work).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in work.rglob('*') if p.is_file()}
    if actual!=cell['workspace_files']:raise ValueError('Restored registered input differs: '+name)
    records.append({'cell_id':name,'workspace':str(work),'verified_files':len(actual),'source_prompt_method_role_changes':False})
print(json.dumps({'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operation':'restore absent worksets only; earlier retained attempts remain unchanged','records':records},indent=2))
