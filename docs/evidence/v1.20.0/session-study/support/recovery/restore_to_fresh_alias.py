#!/usr/bin/env python3
"""Restore exact inputs at a fresh physical directory and replace only a verified alias."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,sys
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--root',type=Path,required=True)
p.add_argument('--cell',required=True)
p.add_argument('--physical-name',required=True)
p.add_argument('--expected-old-target',type=Path,required=True)
p.add_argument('--output-record',type=Path,required=True)
a=p.parse_args()
if Path(a.physical_name).name!=a.physical_name:raise ValueError('Single physical directory name required')
repo=a.repo.resolve();root=a.root.resolve();study=repo/'docs/evidence/v1.20.0/session-study'
sys.path.insert(0,str(study/'support'))
from replay_snapshot import extract
c=next(x for x in json.loads((study/'registration.json').read_text())['cells'] if x['id']==a.cell)
alias=Path(c['work_package']);old=a.expected_old_target.resolve();fresh=root/'ui-study/active-worksets'/a.physical_name
if not alias.is_symlink() or alias.resolve()!=old:raise ValueError('Existing coordinator alias differs')
if fresh.exists() or a.output_record.exists():raise FileExistsError('Fresh paths required')
fresh.mkdir(parents=True)
for ref in c['input_artifacts']:
    archive=repo/ref['path']
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=ref['sha256']:raise ValueError('Frozen archive changed')
    prefix='method/' if archive.name.startswith('method-v') else 'roles/' if archive.name=='distributed-role-instructions.zip' else ''
    extract(archive,fresh,prefix)
actual={f.relative_to(fresh).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in fresh.rglob('*') if f.is_file()}
if actual!=c['workspace_files']:raise ValueError('Fresh restored inputs differ')
temporary=alias.with_name(alias.name+'-new-verified-alias')
if temporary.exists() or temporary.is_symlink():raise FileExistsError(temporary)
temporary.symlink_to(fresh,target_is_directory=True)
os.replace(temporary,alias)
if alias.resolve()!=fresh.resolve():raise ValueError('Alias replacement differs')
record={'kind':'Coordinator exact-input restoration at unique physical workspace','observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cell_id':a.cell,'registered_alias':str(alias),'old_physical_workspace_left_intact':str(old),'new_physical_workspace':str(fresh),'verified_frozen_files':len(actual),'prior_trial_output_supplied':False,'scope':'The earlier restoration reported exact inputs, but a later ordinary and elevated read again showed prior extra files. Cause is unknown. This fresh physical directory retains no prior outputs; only the verified coordinator alias was atomically replaced. Original workspace and immutable verified archive remain intact.'}
a.output_record.parent.mkdir(parents=True,exist_ok=True);a.output_record.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))

