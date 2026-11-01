#!/usr/bin/env python3
"""Restore absent registered inputs at persistent-root backed aliases."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, sys
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--root',type=Path,required=True)
p.add_argument('--output-record',default='remaining-input-restoration-1048.json')
p.add_argument('--attempt-context',default='Unstarted registered cells; no prior output supplied.')
p.add_argument('cells',nargs='+')
a=p.parse_args()
repo=a.repo.resolve();root=a.root.resolve();study=repo/'docs/evidence/v1.20.0/session-study'
sys.path.insert(0,str(study/'support'))
from replay_snapshot import extract
plan=json.loads((study/'registration.json').read_text())
rows=[]
for name in a.cells:
    c=next(c for c in plan['cells'] if c['id']==name)
    work=Path(c['work_package'])
    target=root/'ui-study/active-worksets'/work.name
    if work.exists() or work.is_symlink() or target.exists():
        raise ValueError('Do not overwrite an existing workspace: '+name)
    target.mkdir(parents=True)
    for reference in c['input_artifacts']:
        source=repo/reference['path']
        if hashlib.sha256(source.read_bytes()).hexdigest()!=reference['sha256']:
            raise ValueError('Frozen input differs')
        prefix='method/' if source.name.startswith('method-v') else 'roles/' if source.name=='distributed-role-instructions.zip' else ''
        extract(source,target,prefix)
    actual={path.relative_to(target).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in target.rglob('*') if path.is_file()}
    if actual!=c['workspace_files']:
        raise ValueError('Restored file identities differ: '+name)
    work.parent.mkdir(parents=True,exist_ok=True)
    work.symlink_to(target,target_is_directory=True)
    if not (work/'TASK.md').is_file():
        raise ValueError('Registered alias unreadable')
    rows.append({'cell_id':name,'registered_path':str(work),'physical_workspace':str(target),'verified_files':len(actual),'registered_input_bytes_changed':False,'alias_scope':'Filesystem continuity only; exact registered prompt, input content and method/role files remain unchanged.'})
result={'kind':'coordinator restoration of absent registered inputs','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'attempt_context':a.attempt_context,'records':rows,'limitations':'The old locations were absent in ordinary and elevated checks. This observation does not identify their deletion cause or reconstruct any completed experiment.'}
if Path(a.output_record).name!=a.output_record or not a.output_record.endswith('.json'):raise ValueError('Use a single JSON record filename')
output=study/'coordination/recovery-0830'/a.output_record
if output.exists():raise ValueError('Do not overwrite restoration record')
output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
