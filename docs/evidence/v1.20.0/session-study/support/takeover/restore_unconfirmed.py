#!/usr/bin/env python3
"""Restore verified frozen inputs only after retained prior-attempt replay matches."""
from pathlib import Path
import argparse, datetime, hashlib, json, shutil
ROOT=Path('/workspace/scratch/e1cfe6e447ee')
REPO=ROOT/'UI-Spec-Studio'
STUDY=REPO/'docs/evidence/v1.20.0/session-study'
def inventory(root):
 return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and not set(p.relative_to(root).parts)&{'.git','__pycache__','.pytest_cache'} and not p.relative_to(root).as_posix().startswith('app/node_modules/')}
p=argparse.ArgumentParser();p.add_argument('cells',nargs='+');args=p.parse_args()
plan=json.loads((STUDY/'registration.json').read_text())
for cell_id in args.cells:
 c=next(x for x in plan['cells'] if x['id']==cell_id)
 snapshot=json.loads((STUDY/'incomplete-attempts'/(cell_id+'-before-takeover')/'snapshot.json').read_text())
 old=Path(snapshot['source_workspace']);replay=ROOT/'ui-study/recovered-attempts'/(cell_id+'-before-takeover');stage=ROOT/'ui-study/staged'/cell_id
 assert inventory(old)==snapshot['workspace_files'],'Original changed after capture; stop: '+cell_id
 assert inventory(replay)==snapshot['workspace_files'],'Retained replay differs; stop: '+cell_id
 assert inventory(stage)==c['workspace_files'],'Staged frozen inputs differ; stop: '+cell_id
 retained=old.parent.parent/'unconfirmed-worksets'/(old.name+'-before-e1cfe6e447ee-takeover')
 assert not retained.exists()
 retained.parent.mkdir(exist_ok=True)
 old.rename(retained);stage.rename(old)
 if cell_id.startswith('T2-'):
  cache=retained/'app/node_modules'
  if cache.exists():shutil.copytree(cache,old/'app/node_modules',symlinks=True)
 assert inventory(old)==c['workspace_files'],'Restored source identity differs'
 print(json.dumps({'cell_id':cell_id,'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'terminal_evidence_available':False,'prior_attempt_retained':str(retained),'restored_workspace':str(old),'verified_retained_files':len(snapshot['workspace_files']),'verified_frozen_files':len(c['workspace_files']),'external_dependency_cache_copied':(old/'app/node_modules').exists(),'task_method_role_prompt_changed':False}),flush=True)

