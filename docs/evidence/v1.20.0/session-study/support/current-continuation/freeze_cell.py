#!/usr/bin/env python3
"""Snapshot a completed participant without synthesizing any tool evidence."""
from pathlib import Path
import argparse,datetime,hashlib,json,shutil,sys
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'continuation'))
from large_archives import archive_with_large_files,write_json

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def visible_source(path,root):
    rel=path.relative_to(root)
    return (path.is_file() and not path.is_symlink() and not any(part in {'.git','__pycache__','.pytest_cache'} for part in rel.parts)
            and not rel.as_posix().startswith('app/node_modules/'))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cell',required=True)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--spawn',type=Path,required=True)
    parser.add_argument('--completion',type=Path,required=True)
    args=parser.parse_args()
    repo=args.repo.resolve();study=repo/'docs/evidence/v1.20.0/session-study'
    plan=json.loads((study/'registration.json').read_text());cell=next(c for c in plan['cells'] if c['id']==args.cell)
    package=args.source.resolve();registered_package=str(package)
    spawn=json.loads(args.spawn.read_text());completion=json.loads(args.completion.read_text())
    agent=spawn['result']['task_name']
    if spawn['request']['fork_turns']!='none' or completion.get('agent_id')!=agent or completion.get('message_type')!='FINAL_ANSWER':raise ValueError('Actual fresh primary spawn and FINAL_ANSWER notification required before snapshot')
    if not package.is_absolute() or not package.is_dir():raise ValueError('An explicit existing absolute workspace is required')
    if not (package/'FINAL.md').is_file():raise ValueError('Participant FINAL.md is required; completion export must be recorded separately.')
    target=args.output.resolve()
    target.relative_to(study/'continuation-2100')
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
    if str(package)!=registered_package:record['registered_source_workspace']=registered_package;record['host_path_scope']='Explicit coordinator host path mapping; actual captured source workspace above, unchanged frozen input content and registered primary prompt.'
    write_json(target/'snapshot.json',record)
    for name in ['FINAL.md','VISUAL-REVIEW.md','DELEGATION.json']:
        if (package/name).is_file():
            # Preserve raw participant Markdown as data, including temporary sandbox links.
            destination=name+'.txt' if name.endswith('.md') else name
            shutil.copyfile(package/name,target/destination)
    print(json.dumps({'cell':args.cell,'files':len(paths),'changed':len(changed),'deleted':len(deleted),'method_changes':len(protocol_changes),'role_changes':len(role_changes),'archives':archives['archives']},indent=2))
if __name__=='__main__':main()
