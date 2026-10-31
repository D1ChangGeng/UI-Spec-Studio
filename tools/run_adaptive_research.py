#!/usr/bin/env python3
"""Freeze isolated study inputs and run actual Codex CLI sessions, never simulations.

Preparation is offline. Execution requires an explicitly selected provisioned or
inherited runtime profile, working Codex login/model/tools, and cost acknowledgement.
A completed CLI turn is not a successful UI task or proof of subagent use.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import subprocess
import sys
import time
import zipfile

ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/'docs/experiments/adaptive-research'
SKIP={'.git','node_modules','__pycache__','dist','.pytest_cache','.venv','.codex','.agents',
      '.next','.nuxt','.svelte-kit','.turbo','.cache','.vite','coverage'}
TASKS=('T1','T2','T3','T4')
ADAPTER_ROLES=('ui_researcher','ui_integrator','ui_challenger','ui_experience_observer')
CONDITIONS={
 'A': {'skill':'baseline','roles':[],'agents':False,'instruction':'Complete this task in the main agent without spawning auxiliary agents.'},
 'B': {'skill':'baseline','roles':[],'agents':True,'instruction':'Use generic auxiliary agents only when useful to deepen research and curate evidence. Keep final design decisions and pivotal visual inspection in the main agent. Do not delegate product implementation in this arm.'},
 'C': {'skill':'baseline','roles':['ui_researcher'],'agents':True,'instruction':'Use ui_researcher when useful to deepen research and curate evidence. You retain key visual judgment and final design responsibility. Do not delegate product implementation in this arm.'},
 'D': {'skill':'baseline','roles':['ui_researcher'],'agents':True,'instruction':'Use ui_researcher when useful to deepen research and curate evidence. You retain key visual judgment and final design responsibility. Do not delegate product implementation in this arm.'},
 'E-challenger': {'skill':'baseline','roles':['ui_researcher','ui_challenger'],'agents':True,'instruction':'Use ui_researcher when useful, and ui_challenger only for a consequential independent comparison. Keep final decisions and pivotal visual inspection yourself. Do not delegate product implementation in this arm.'},
 'E-observer': {'skill':'baseline','roles':['ui_researcher','ui_experience_observer'],'agents':True,'instruction':'Use ui_researcher when useful and ui_experience_observer for a genuinely complex GUI episode. Ordinary observation remains your own capability. Retain final judgment. Do not delegate product implementation in this arm.'},
 'F-main': {'skill':'candidate','roles':[],'agents':False,'instruction':'Integrate the established resource yourself, preserving settled design and source craft. Do not spawn auxiliary agents.'},
 'F-integrator': {'skill':'candidate','roles':['ui_integrator'],'agents':True,'instruction':'Delegate only the established, bounded integration to ui_integrator. Inspect its actual result yourself and own overall acceptance. Return unresolved design choices to yourself.'},
 'G-final-runtime': {'skill':'candidate','roles':list(ADAPTER_ROLES),'agents':True,'instruction':'Use the complete candidate UI Spec Studio. Delegate research or already-settled bounded integration only where valuable. Call ui_challenger or ui_experience_observer only when the decision or GUI investigation warrants it. Retain all pivotal visual judgments and final responsibility.'}
}
COMMON='''\nUse the installed ui-spec Skill and read its complete required professional references. The same user brief, starting application, source rights, theme/locale/viewport targets and verification expectations apply across paired conditions. Research access is not permission to recreate unavailable UI. Keep mature visual provenance and scoped W1-W3 authorization intact.\n\nUse available tools for actual source viewing, meaningful interaction episodes and final product inspection. Preserve exact source identity, observed conditions, relevant screenshots/recordings and a concise account of what changed your design decisions in evidence/. Do not claim observation from descriptions, or smoothness from sparse frames. Keep unsuccessful attempts and unresolved quality visible. No real purchases, external account changes, private uploads or destructive external operations are authorized.\n\nDeliver the working application and your factual evidence. Do not claim that a successful build proves visual quality. Do not modify the study method, task, installed Skill or role files.\n'''

class StudyError(ValueError): pass

def sha(raw:bytes)->str:return hashlib.sha256(raw).hexdigest()
def now()->str:return datetime.now(timezone.utc).isoformat()
def write_json(p:Path,data):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def safe(root:Path,rel:str)->Path:
    p=PurePosixPath(rel)
    if any(':' in part for part in p.parts) or p.is_absolute() or '..' in p.parts or '\\' in rel or not p.parts: raise StudyError('Unsafe relative study path')
    target=root.absolute()
    for parent in (target,*target.parents):
        if parent.is_symlink():raise StudyError('Linked study root')
    for part in p.parts:
        target/=part
        if target.is_symlink():raise StudyError('Linked study member')
    return target

def public_files(root:Path)->dict[str,bytes]:
    if not root.is_dir():raise StudyError('Expected a source directory')
    result={}
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if any(part in SKIP for part in rel.parts):continue
        if p.is_symlink():raise StudyError('Input contains linked content')
        if not p.is_file():continue
        if p.name.startswith('.env') or p.name in {'auth.json','credentials.json','id_rsa','id_ed25519'} or p.suffix in {'.pem','.key'}:
            raise StudyError('Possible private credential material in study input; remove it explicitly')
        result[rel.as_posix()]=p.read_bytes()
    return result

def copy_frozen(files:dict[str,bytes],root:Path):
    for rel,raw in files.items():
        target=safe(root,rel);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)

def describe(files:dict[str,bytes])->dict[str,str]:return {p:sha(b) for p,b in sorted(files.items())}

def validate_cell(row:dict):
    if not isinstance(row,dict) or row.get('condition') not in CONDITIONS or row.get('task') not in TASKS:
        raise StudyError('Unknown task or condition')
    if row['condition'].startswith('F-') and row['task']!='T4':raise StudyError('Bounded integration comparison uses T4')
    for field in ('id','main_model','subagent_model','main_effort','subagent_effort'):
        if not isinstance(row.get(field),str) or not row[field].strip() or '\n' in row[field]:raise StudyError(f'Missing cell field: {field}')
    if not all(c.isalnum() or c in '-_' for c in row['id']):raise StudyError('Unsafe cell identifier')
    if row['main_effort'] not in {'minimal','low','medium','high','xhigh'} or row['subagent_effort'] not in {'minimal','low','medium','high','xhigh'}:
        raise StudyError('Unknown effort; confirm host support')
    if type(row.get('timeout_seconds')) is not int or row['timeout_seconds']<=0:raise StudyError('Positive explicit runtime budget required')
    if type(row.get('max_subagents')) is not int or not 1<=row['max_subagents']<=16:raise StudyError('Explicit bounded concurrency required')
    if 'network_access' in row and type(row['network_access']) is not bool:raise StudyError('network_access must be an explicit boolean')

def prepare(*,baseline_skill:Path,candidate_skill:Path,starters:Path,plan:Path,output:Path,roles:Path)->dict:
    if output.exists():raise StudyError('Use a fresh output directory; prior attempts are immutable')
    cfg=json.loads(plan.read_bytes());cells=cfg.get('cells')
    if not isinstance(cells,list) or not cells:raise StudyError('Plan has no cells')
    for row in cells:validate_cell(row)
    if len({r['id'] for r in cells})!=len(cells):raise StudyError('Duplicate cell identities')
    methods={'baseline':public_files(baseline_skill),'candidate':public_files(candidate_skill)}
    for name,files in methods.items():
        if 'SKILL.md' not in files:raise StudyError('Each method must be a complete installed Skill directory')
        for ref in ('workflow','analysis','principles','component-sourcing','interaction-and-variants','verification','visual-assets','content-design'):
            if f'references/{ref}.md' not in files:raise StudyError('Incomplete professional foundation')
    all_inputs={}
    for task in sorted({r['task'] for r in cells}):
        inputs=public_files(starters/task)
        if 'INPUT.md' not in inputs:raise StudyError('Each real starter needs INPUT.md with product, rights, preview and verification conditions')
        if not any(p.startswith('app/') for p in inputs):raise StudyError('Each task needs a real starting app/ directory')
        if task=='T4' and 'INTEGRATION-DECISION.md' not in inputs:raise StudyError('T4 needs a settled, explicit source and bounded integration decision')
        all_inputs[task]=inputs
    # Reject unexpected inherited role/design instructions in the starter.
    if any(any(Path(p).name in {'AGENTS.md','AGENTS.override.md'} for p in items) for items in all_inputs.values()):
        raise StudyError('Remove unregistered starter Agent instructions before freezing')
    registry={'schema_version':1,'status':'prepared_not_executed','created_at':now(),
              'plan_sha256':sha(plan.read_bytes()),'cells':[],
              'comparison_limits':'A/B/C isolate role effects on baseline Skill; G separately tests final candidate. Live-web and provider nondeterminism remain.',
              'candidate_source_identity':None,'candidate_method_files':describe(methods['candidate'])}
    candidate_root=candidate_skill.absolute().parent.parent
    if (candidate_root/'VERSION').is_file() and (candidate_root/'tools/check_adaptive_release.py').is_file():
        import importlib.util
        spec=importlib.util.spec_from_file_location('candidate_release_identity',candidate_root/'tools/check_adaptive_release.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        registry['candidate_source_identity']=module.candidate_identity(candidate_root)
    for row in cells:
        info=dict(row);info['network_access']=row.get('network_access',False)
        cond=CONDITIONS[row['condition']];task=STUDY/'tasks'/f'{row["task"]}.md'
        if not task.is_file():raise StudyError('Missing canonical task brief')
        taskraw=task.read_bytes()
        files=dict(all_inputs[row['task']]);files['TASK.md']=taskraw
        installed_roles=list(ADAPTER_ROLES) if cond['roles'] or cond['skill']=='candidate' else []
        role_boundary=''
        if installed_roles:
            role_boundary=('\nAll four adapter roles are installed. In this condition, call only these custom roles: '+
                           (', '.join(cond['roles']) if cond['roles'] else 'none')+
                           '. Installation does not require invocation. Preserve actual child role identities for the execution audit.\n')
        files['AGENTS.md']=('Read TASK.md and INPUT.md. The installed ui-spec Skill is in .agents/skills/ui-spec/.\n'+
                            cond['instruction']+role_boundary+COMMON).encode()
        for rel,raw in methods[cond['skill']].items():files['.agents/skills/ui-spec/'+rel]=raw
        for role in installed_roles:
            p=roles/(role+'.toml')
            if not p.is_file() or p.is_symlink():raise StudyError('Missing role source')
            files['.codex/agents/'+role+'.toml']=p.read_bytes()
        destination=output/'cells'/row['id']/'workspace'
        info.update(task_sha256=sha(taskraw),method=cond['skill'],workspace_files=describe(files),
                    role_names=cond['roles'],allowed_role_names=cond['roles'],
                    installed_role_names=installed_roles,subagents_enabled=cond['agents'],
                    starter_files=describe(all_inputs[row['task']]),method_files=describe(methods[cond['skill']]))
        copy_frozen(files,destination);registry['cells'].append(info)
    write_json(output/'registration.json',registry)
    return registry

def profile_preflight(home:Path)->dict:
    if not home.is_dir() or home.is_symlink():raise StudyError('Provide an existing, explicitly provisioned experiment CODEX_HOME')
    for name in ('AGENTS.md','AGENTS.override.md','agents','skills'):
        p=home/name
        if p.is_symlink() or (p.is_file() and p.stat().st_size) or (p.is_dir() and any(p.iterdir())):
            raise StudyError('Experiment CODEX_HOME contains unregistered role/Skill/instruction overrides')
    # Hash configuration for reproducibility, never read/print authentication files.
    config=home/'config.toml'
    if config.is_symlink():raise StudyError('Linked experiment configuration')
    return {'config_sha256':sha(config.read_bytes()) if config.is_file() else None,
            'auth':'not_read','other_global_instruction_contamination':'must_be_checked_by_reviewer'}

def inherited_profile_preflight()->dict:
    """Describe an existing runtime without changing it or inspecting auth bytes."""
    home=Path(os.environ.get('CODEX_HOME') or Path.home()/'.codex').expanduser().absolute()
    config=home/'config.toml'
    if config.is_symlink():raise StudyError('Linked inherited configuration requires separate review')
    instructions={}
    for name in ('AGENTS.md','AGENTS.override.md'):
        p=home/name
        if p.is_symlink():raise StudyError('Linked inherited instruction requires separate review')
        if p.is_file():instructions[name]=sha(p.read_bytes())
    return {'mode':'inherited_profile_ignore_user_config','home':str(home),
            'config_sha256':sha(config.read_bytes()) if config.is_file() else None,
            'auth':'not_read','environment_mutation':False,
            'user_instruction_identities':instructions,
            'user_roles_present':(home/'agents').exists(),
            'user_skills_present':(home/'skills').exists(),
            'isolation':'Fresh workspace and local runtime state; the existing authenticated host environment is inherited.',
            'other_global_instruction_contamination':'ignore-user-config is not an empty profile; reviewer must inspect actual instruction/tool inheritance'}

def summarize_events(raw:bytes)->dict:
    events=[];malformed=0
    for line in raw.splitlines():
        if not line.strip():continue
        try: value=json.loads(line)
        except (ValueError,UnicodeError):malformed+=1;continue
        if isinstance(value,dict):events.append(value)
        else:malformed+=1
    threads=[x.get('thread_id') for x in events if x.get('type')=='thread.started']
    turns=[x for x in events if x.get('type')=='turn.completed']
    failures=[x for x in events if x.get('type') in {'turn.failed','error'}]
    return {'thread_id':threads[0] if len(threads)==1 else None,'completed_turns':len(turns),
            'malformed_lines':malformed,'failure_events':len(failures),
            'reported_usage':[x.get('usage') for x in turns],
            'total_subagent_usage':None,'actual_auxiliary_agent_count':None}

def command(executable:str,row:dict,workspace:Path,*,inherit_profile:bool=False,runtime_dir:Path|None=None)->list[str]:
    values={'agents.enabled':row['subagents_enabled'],
            'agents.max_concurrent_threads_per_session':row['max_subagents'],
            'agents.default_subagent_model':row['subagent_model'],
            'agents.default_subagent_reasoning_effort':row['subagent_effort'],
            'model_reasoning_effort':row['main_effort'],
            'sandbox_workspace_write.network_access':row.get('network_access',False)}
    cmd=[executable,'exec','--json','--ephemeral','--cd',str(workspace),'--sandbox','workspace-write','--model',row['main_model']]
    if row['subagents_enabled']:cmd+=['--enable','multi_agent']
    for role in row.get('installed_role_names',[]):
        if role not in ADAPTER_ROLES:raise StudyError('Unknown installed role registration')
        path=workspace/'.codex/agents'/f'{role}.toml'
        match=re.search(r'^description\s*=\s*("[^\n]*")\s*$',path.read_text(encoding='utf-8'),re.M)
        if not match:raise StudyError('Role description is not a supported single-line string')
        values[f'agents.{role}.config_file']=str(path.absolute())
        values[f'agents.{role}.description']=json.loads(match[1])
    if inherit_profile:
        if runtime_dir is None:raise StudyError('Inherited runtime needs a local state/log directory')
        cmd.append('--ignore-user-config')
        values.update(sqlite_home=str(runtime_dir/'state'),log_dir=str(runtime_dir/'logs'))
    for k,v in values.items():cmd+=['-c',k+'='+json.dumps(v)]
    return cmd+['Read AGENTS.md, TASK.md and INPUT.md. Carry out the task and preserve actual evidence.']

def snapshot_outputs(workspace:Path,out:Path)->dict:
    """Freeze selected public output bytes; never collect a profile or font files."""
    allowed={'.html','.css','.scss','.sass','.less','.js','.jsx','.mjs','.cjs','.ts','.tsx','.mts','.cts','.vue','.svelte','.json',
             '.md','.txt','.svg','.png','.jpg','.jpeg','.webp','.webm','.mp4','.csv',
             '.yml','.yaml','.toml','.py','.mdx','.tid','.lock'}
    excluded_types={'.woff','.woff2','.ttf','.otf','.ttc','.eot','.pem','.key','.p12','.pfx'}
    records={};excluded=[];total=0
    archive=out/'product-output.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for folder in ('app','evidence'):
            for p in sorted((workspace/folder).rglob('*')):
                rel=p.relative_to(workspace)
                if any(x in SKIP for x in rel.parts):continue
                if p.is_symlink():
                    excluded.append({'path':rel.as_posix(),'reason':'symlink'});continue
                if not p.is_file():continue
                legal_name=p.name.upper()
                is_legal=any(legal_name==name or legal_name.startswith(name+'-') or legal_name.startswith(name+'.')
                             for name in ('LICENSE','LICENCE','COPYING','NOTICE','AUTHORS','COPYRIGHT','PATENTS'))
                if p.name.startswith('.env') or p.name in {'auth.json','credentials.json','id_rsa','id_ed25519'} or p.suffix.lower() in excluded_types or not (p.suffix in allowed or is_legal):
                    excluded.append({'path':rel.as_posix(),'reason':'unsupported or private-sensitive type'});continue
                if p.stat().st_size>32*1024*1024 or total+p.stat().st_size>256*1024*1024:
                    excluded.append({'path':rel.as_posix(),'reason':'archive size boundary'});continue
                raw=p.read_bytes();total+=len(raw)
                info=zipfile.ZipInfo(rel.as_posix(),date_time=(2026,1,1,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                z.writestr(info,raw);records[rel.as_posix()]={'sha256':sha(raw),'bytes':len(raw)}
    index={'archive':'product-output.zip','sha256':sha(archive.read_bytes()),
           'files':records,'excluded':excluded,'visual_review':'not_performed_by_archiver',
           'privacy':'Manual review required before public redistribution; no font binaries included.'}
    write_json(out/'output-index.json',index);return index


def run(*,study:Path,cell_id:str,home:Path|None=None,inherit_profile:bool=False,codex_executable:Path|None=None,execute:bool=False,acknowledge_cost:bool=False)->dict:
    if inherit_profile == (home is not None):
        raise StudyError('Select exactly one provisioned CODEX_HOME or inherited profile')
    registration=json.loads((study/'registration.json').read_bytes())
    rows=[r for r in registration['cells'] if r['id']==cell_id]
    if len(rows)!=1:raise StudyError('Unknown or duplicate registered cell')
    row=rows[0];workspace=study/'cells'/cell_id/'workspace'
    if describe(public_files_including_methods(workspace))!=row['workspace_files']:
        raise StudyError('Frozen workspace changed; create a new registered attempt rather than overwriting evidence')
    executable=shutil.which(str(codex_executable) if codex_executable is not None else 'codex')
    report={'schema_version':1,'cell_id':cell_id,'simulation':False,'status':'preflight_only',
            'task_sha256':row['task_sha256'],'actual_independent_agent_runs':0,
            'thread_id':None,'registration_sha256':sha((study/'registration.json').read_bytes()),
            'ui_quality':'not_evaluated','subagent_use':'not_verified','created_at':now(),
            'network_access':row.get('network_access',False),
            'input_workspace_identity':sha(json.dumps(row['workspace_files'],sort_keys=True).encode())}
    if not executable:
        report['status']='blocked_not_run';report['reason']='codex executable not available';return report
    report['profile']=inherited_profile_preflight() if inherit_profile else profile_preflight(home)
    version=subprocess.run([executable,'--version'],capture_output=True,text=True,timeout=15,check=False)
    if version.returncode:raise StudyError('Codex version probe failed')
    report['codex_version']=version.stdout.strip()
    report['model_availability']='not_verified';report['tool_visual_capability']='not_verified'
    if not execute:return report
    if not acknowledge_cost:raise StudyError('Actual execution requires --acknowledge-cost')
    out=study/'runs'/cell_id
    if out.exists():raise StudyError('A prior attempt exists; preserve it and register a fresh attempt')
    # Fresh sessions need a Git workspace; no history or credentials are copied.
    subprocess.run(['git','init','--quiet',str(workspace)],check=True,capture_output=True,timeout=15)
    out.mkdir(parents=True)
    env=os.environ.copy()
    if not inherit_profile:env['CODEX_HOME']=str(home.absolute())
    runtime_dir=out/'runtime'
    if inherit_profile:runtime_dir.mkdir()
    cmd=command(executable,row,workspace,inherit_profile=inherit_profile,runtime_dir=runtime_dir)
    report['command']=cmd;report['started_at']=now()
    begin=time.monotonic();timed_out=False
    with (out/'events.jsonl').open('wb') as stdout,(out/'stderr.log').open('wb') as stderr:
        process=subprocess.Popen(cmd,stdout=stdout,stderr=stderr,env=env,
                                 start_new_session=(os.name!='nt'))
        try:code=process.wait(timeout=row['timeout_seconds'])
        except subprocess.TimeoutExpired:
            timed_out=True
            if os.name=='nt':
                subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True,timeout=15,check=False)
            else:os.killpg(process.pid,signal.SIGTERM)
            try:code=process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                if os.name!='nt':os.killpg(process.pid,signal.SIGKILL)
                else:process.kill()
                code=process.wait(timeout=5)
    report['elapsed_seconds']=round(time.monotonic()-begin,3);report['ended_at']=now();report['returncode']=code
    report.update(summarize_events((out/'events.jsonl').read_bytes()))
    if timed_out:report['status']='timed_out'
    elif code==0 and report['thread_id'] and report['completed_turns'] and not report['malformed_lines'] and not report['failure_events']:
        report['status']='process_completed';report['actual_independent_agent_runs']=1
    else:report['status']='process_failed_or_incomplete'
    report['events']={'path':(out/'events.jsonl').relative_to(study).as_posix(),'sha256':sha((out/'events.jsonl').read_bytes())}
    report['stderr']={'path':(out/'stderr.log').relative_to(study).as_posix(),'sha256':sha((out/'stderr.log').read_bytes())}
    report['execution_audit']=None;report['product_evidence_index']=None
    report['boundary']='Actual CLI execution only. Independent audit must confirm native subagents, observation, artifact provenance, UI results and total usage.'
    try:
        report['output_snapshot']=snapshot_outputs(workspace,out)
    except (OSError,ValueError) as exc:
        report['output_snapshot']={'status':'capture_failed','error':str(exc)}
    write_json(out/'run.json',report)
    # Never automatically copy profiles, credentials, generated binaries or private logs into a public release.
    return report

def public_files_including_methods(root:Path)->dict[str,bytes]:
    result={}
    for p in sorted(root.rglob('*')):
        if any(x in SKIP-{'.codex','.agents'} for x in p.relative_to(root).parts):continue
        if p.is_symlink():raise StudyError('Linked workspace member')
        if p.is_file():result[p.relative_to(root).as_posix()]=p.read_bytes()
    return result

def main()->int:
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
    p=sub.add_parser('prepare')
    for flag in ('baseline-skill','candidate-skill','starters','plan','output'):p.add_argument('--'+flag,required=True,type=Path)
    p.add_argument('--roles',type=Path,default=ROOT/'integrations/codex/agents')
    p=sub.add_parser('run');p.add_argument('--study',type=Path,required=True);p.add_argument('--cell',required=True)
    profile=p.add_mutually_exclusive_group(required=True)
    profile.add_argument('--codex-home',type=Path)
    profile.add_argument('--inherit-profile',action='store_true',help='Keep the existing environment unchanged, ignore user config, record inherited-profile limitations')
    p.add_argument('--codex-executable',type=Path,help='Use an explicitly located Codex binary; defaults to the PATH lookup')
    p.add_argument('--execute',action='store_true');p.add_argument('--acknowledge-cost',action='store_true')
    args=parser.parse_args()
    try:
        if args.action=='prepare':result=prepare(baseline_skill=args.baseline_skill,candidate_skill=args.candidate_skill,starters=args.starters,plan=args.plan,output=args.output,roles=args.roles)
        else:result=run(study=args.study,cell_id=args.cell,home=args.codex_home,inherit_profile=args.inherit_profile,codex_executable=args.codex_executable,execute=args.execute,acknowledge_cost=args.acknowledge_cost)
        print(json.dumps(result,indent=2,ensure_ascii=False));return 2 if result.get('status')=='blocked_not_run' else 0
    except (StudyError,OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as exc:
        print('adaptive study: '+str(exc),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
