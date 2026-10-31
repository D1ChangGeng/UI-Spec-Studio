#!/usr/bin/env python3
"""Snapshot a completed participant without synthesizing any tool evidence."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'continuation'))
import argparse,datetime,hashlib,json,shutil,sys
from large_archives import archive_with_large_files,write_json

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def visible_source(path,root):
    rel=path.relative_to(root)
    return (path.is_file() and not any(part in {'.git','__pycache__','.pytest_cache'} for part in rel.parts)
            and not rel.as_posix().startswith('app/node_modules/'))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cell',required=True)
    args=parser.parse_args()
    import os
    root=Path(os.environ['UI_STUDY_ROOT']);repo=Path(os.environ['UI_STUDY_REPO']);study=repo/'docs/evidence/v1.20.0/session-study'
    plan=json.loads((study/'registration.json').read_text());cell=next(c for c in plan['cells'] if c['id']==args.cell)
    dispatch=json.loads((root/'ui-study/dispatch-map.json').read_text());package=Path(next(c for c in dispatch if c['id']==args.cell)['work_package'])
    if not (package/'FINAL.md').is_file():raise ValueError('Participant FINAL.md is required; completion export must be recorded separately.')
    run_name=os.environ.get('UI_STUDY_RUN_NAME',args.cell)
    if Path(run_name).name!=run_name:raise ValueError('Expected a single explicit run-directory name')
    target=study/'runs'/run_name
    target.mkdir(parents=True,exist_ok=False)
    paths=sorted([p for p in package.rglob('*') if visible_source(p,package)])
    identities={p.relative_to(package).as_posix():digest(p) for p in paths}
    baseline=cell['workspace_files']
    changed=[p for p in paths if identities[p.relative_to(package).as_posix()]!=baseline.get(p.relative_to(package).as_posix())]
    deleted=sorted(set(baseline)-set(identities))
    protocol_changes={name:{'expected':expected,'observed':identities.get('method/'+name)} for name,expected in cell['method_files'].items() if identities.get('method/'+name)!=expected}
    role_changes={role:{'expected':expected,'observed':identities.get('roles/'+role+'.toml')} for role,expected in cell['role_instruction_files'].items() if identities.get('roles/'+role+'.toml')!=expected}
    archives=archive_with_large_files(package,changed,target,'workspace-overlay')
    record={'schema_version':1,'cell_id':args.cell,'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':'coordinator byte snapshot, not a tool-event transcript','source_workspace':str(package),'reconstruction':'Extract the frozen task inputs and cell instructions at the work-package root, the complete method archive into method/, and applicable distributed-role archive into roles/. Overlay every workspace-overlay ZIP at the work-package root; remove deleted_paths. Archives preserve file bytes and executable mode with normalized archive timestamps. app/node_modules is an excluded dependency cache; T2 includes its built app/dist in the original/overlay inputs.','excluded':'app/node_modules, .git, __pycache__, .pytest_cache; external browser/Python/font runtime is documented separately.','workspace_files':identities,'workspace_modes':{p.relative_to(package).as_posix():oct(p.stat().st_mode&0o777) for p in paths},'changed_or_added':sorted(p.relative_to(package).as_posix() for p in changed),'deleted_paths':deleted,'method_changes':protocol_changes,'role_changes':role_changes,'overlay':archives}
    write_json(target/'snapshot.json',record)
    for name in ['FINAL.md','VISUAL-REVIEW.md','DELEGATION.json']:
        if (package/name).is_file():
            # Preserve raw participant Markdown as data, including temporary sandbox links.
            destination=name+'.txt' if name.endswith('.md') else name
            shutil.copyfile(package/name,target/destination)
    print(json.dumps({'cell':args.cell,'files':len(paths),'changed':len(changed),'deleted':len(deleted),'method_changes':len(protocol_changes),'role_changes':len(role_changes),'archives':archives['archives']},indent=2))
if __name__=='__main__':main()
