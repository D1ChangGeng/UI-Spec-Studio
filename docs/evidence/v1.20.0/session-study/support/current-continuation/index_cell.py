#!/usr/bin/env python3
"""Create coordinator indexes over immutable, actually captured participant evidence."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'continuation'))
from datetime import datetime,timezone
import argparse,base64,hashlib,json,shutil,re,os

def sha(raw):return hashlib.sha256(raw).hexdigest()
def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def iso(value):
    if value.endswith(' UTC'):return datetime.strptime(value,'%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=timezone.utc).isoformat()
    return datetime.fromisoformat(value.replace('Z','+00:00')).isoformat()

def main():
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('configuration',type=Path);args=a.parse_args();cfg=json.loads(args.configuration.read_text())
    repo=Path(cfg['repo']).resolve();study=repo/'docs/evidence/v1.20.0/session-study'
    plan=json.loads((study/'registration.json').read_text());cell=next(c for c in plan['cells'] if c['id']==cfg['cell_id']);name=cell['id']
    out=(repo/cfg['evidence_directory']).resolve();out.relative_to(study/'continuation-2100')
    if (out/'run.json').exists():raise FileExistsError('An indexed completion must not be overwritten')
    snapshot=json.loads((out/'snapshot.json').read_text());package=Path(snapshot['source_workspace']);replay_name=name
    package_paths=[package]
    for alias in cfg.get('source_workspace_aliases',[]):
        alias_path=Path(alias)
        if not alias_path.is_absolute() or not alias_path.is_dir() or alias_path.resolve()!=package.resolve():
            raise ValueError('A workspace alias must resolve to this exact captured source workspace')
        if alias_path not in package_paths:package_paths.append(alias_path)
    def source_relative(path):
        for source_path in package_paths:
            try:return path.relative_to(source_path).as_posix()
            except ValueError:pass
        raise ValueError('Original path is outside the captured workspace and verified aliases: '+str(path))
    if Path(replay_name).name!=replay_name:raise ValueError('Expected a single explicit replay-directory name')
    replay=Path(cfg['replay_directory']).resolve()
    if not replay.is_dir():raise ValueError('Verified reconstruction is required')
    if snapshot['method_changes'] or snapshot['role_changes']:raise ValueError('Frozen method/role changes need explicit adjudication')
    def ref(path):return {'path':path.relative_to(repo).as_posix(),'sha256':sha(path.read_bytes())}
    def retain(relative):
        path=replay/relative
        if not path.is_file():raise FileNotFoundError(relative)
        if sha(path.read_bytes())!=snapshot['workspace_files'].get(relative):raise ValueError('Retained snapshot differs: '+relative)
        # Original text remains byte-identical. Use a data suffix for Markdown
        # and text types omitted by the source bundle's fixed extension policy.
        # The full workspace overlay always keeps the original filename.
        published_suffixes={'.toml','.py','.json','.yml','.yaml','.txt','.svg','.html','.css','.js','.png','.mp4','.csv','.jsonl','.mjs','.log','.woff2','.webm','.zip','.jpg','.jpeg','.sha256'}
        data_name=relative
        if path.suffix=='.md' or (path.suffix not in published_suffixes and path.name!='LICENSE'):
            path.read_bytes().decode('utf-8')
            data_name=relative+'.txt'
        target=out/'artifacts'/data_name;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() and target.read_bytes()!=path.read_bytes():raise ValueError('Already retained bytes differ')
        shutil.copyfile(path,target)
        return ref(target)
    def export(reference,source,scope,kind='faithful_conversation_export'):
        return {**reference,'source':source,'scope':scope,'export_kind':kind,'synthetic':False}
    def retained_export(relative,source,scope,kind='faithful_conversation_export'):
        return export(retain(relative),source,scope,kind)
    # The participant's exact Markdown is retained as .md.txt and inside the
    # immutable overlay. A separately labeled navigation copy has repository
    # links so generic package-link validation never rewrites original evidence.
    for original in ['FINAL.md','VISUAL-REVIEW.md']:
        source=replay/original
        if source.is_file():
            if sha(source.read_bytes())!=snapshot['workspace_files'][original]:raise ValueError('Report changed after snapshot')
            destination=out/(original+'.txt')
            if destination.exists() and destination.read_bytes()!=source.read_bytes():raise ValueError('Raw report differs')
            shutil.copyfile(source,destination)
    directory_links=[]
    def portable_link(match):
        original_path=Path(match.group(1))
        try:relative=source_relative(original_path)
        except ValueError:raise ValueError('Final report links outside captured workspace: '+str(original_path))
        if (replay/relative).is_dir():
            if not any(name.startswith(relative.rstrip('/')+'/') for name in snapshot['workspace_files']):raise ValueError('Directory lacks captured source bytes')
            directory_links.append(relative)
            return '](RECONSTRUCTION.md)'
        reference=retain(relative)
        return ']('+os.path.relpath(repo/reference['path'],out).replace(os.sep,'/')+')'
    navigation=re.sub(r'\]\(sandbox:([^\)]+)\)',portable_link,(replay/'FINAL.md').read_text())
    if directory_links:
        directories='\n'.join('- `'+relative+'`' for relative in sorted(set(directory_links)))
        command='python3 docs/evidence/v1.20.0/session-study/support/continuation/replay_snapshot.py --repo . --cell '+name+' --snapshot-directory '+out.relative_to(repo).as_posix()+' --output /tmp/ui-spec-'+name+'-replay'
        (out/'RECONSTRUCTION.md').write_text('# Reconstruct the delivered source workspace\n\nThis is a coordinator navigation page for directory links in the original participant report. The original report is retained unchanged in [FINAL.md.txt](FINAL.md.txt). Its linked source directories are:\n\n'+directories+'\n\nThe complete source is retained through frozen inputs and immutable overlay archives. From the repository root, choose a fresh output directory and run:\n\n```sh\n'+command+'\n```\n\nThe helper verifies every reconstructed byte and restores recorded file modes. [snapshot.json](snapshot.json) lists all original workspace paths and hashes; [product-evidence.json](product-evidence.json) identifies the required inputs and overlays. Follow the participant preview command in the final report. These directory links are not claims that the small direct-export folder contains the entire application.\n')
    (out/'FINAL.md').write_text('<!-- Derived navigation copy; never use as an original participant export. -->\n\n> Repository navigation copy. The participant report is retained byte for byte in [FINAL.md.txt](FINAL.md.txt) and the workspace overlay archives. Only local artifact link destinations below are adapted for this repository; directory links lead to the complete-workspace reconstruction instructions.\n\n'+navigation)
    def command_exports(patterns):
        rows=[]
        for path in sorted({p for pattern in patterns for p in replay.glob(pattern) if p.is_file() and p.stat().st_size}):
            rel=path.relative_to(replay).as_posix()
            rows.append(retained_export(rel,'capture_command.py / actual subprocess capture','Original nonempty command output or contemporaneous capture metadata. The participant authored the exercised commands; this is not independent product acceptance.','original_tool_output'))
        return rows
    screenshots=[];image_names=set()
    for prefix in cfg['final_capture_prefixes']:
        for path in sorted((replay/prefix).rglob('*.png')):
            rel=path.relative_to(replay).as_posix()
            if rel not in image_names:screenshots.append(retain(rel));image_names.add(rel)
    for rel in cfg.get('final_capture_files',[]):
        if not rel.endswith('.png'):raise ValueError('Expected actual PNG capture')
        if rel not in image_names:screenshots.append(retain(rel));image_names.add(rel)
    views=[]
    for path in sorted({p for pattern in cfg['primary_view_globs'] for p in replay.glob(pattern) if p.is_file()}):
        try:d=json.loads(path.read_text())
        except (ValueError,UnicodeError):continue
        calls=d if isinstance(d,list) else [d]
        for call in calls:
            if not isinstance(call,dict) or call.get('tool')!='view_image':continue
            image_path=call.get('arguments',{}).get('path')
            if not isinstance(image_path,str):continue
            try:relative=source_relative(Path(image_path))
            except ValueError:continue
            if relative in image_names:
                views.append({'viewer_agent_id':cfg['agent_id'],'screenshot':retain(relative),'view_export':retained_export(path.relative_to(replay).as_posix(),'view_image','Full actual view_image request/returned object (or original batch containing it) saved by the primary participant at call time; the original PNG is retained separately.')})
    for item in cfg.get('primary_return_views',[]):
        relative=item['screenshot'];export_path=item['export']
        if relative not in image_names:raise ValueError('Explicit returned-image view is outside the final capture set')
        original=json.loads((replay/export_path).read_bytes())
        payload=original.get('image_url') if isinstance(original,dict) else None
        if not isinstance(payload,str) or payload.split(',',1)[0] not in {'data:image/png;base64','data:application/octet-stream;base64'}:
            raise ValueError('Expected an original PNG image-tool return')
        returned_bytes=base64.b64decode(payload.split(',',1)[1],validate=True)
        if not returned_bytes.startswith(b'\x89PNG\r\n\x1a\n') or returned_bytes!=(replay/relative).read_bytes():
            raise ValueError('Original image-tool return differs from its declared capture')
        views.append({'viewer_agent_id':cfg['agent_id'],'screenshot':retain(relative),'view_export':retained_export(export_path,'view_image','Original full image-tool returned object saved at call time. Its PNG payload is byte-identical to the retained screenshot. The request arguments are not present in this original export; the primary visual report identifies the actual inspection. No request is reconstructed here.','original_tool_output')})
    if not screenshots or not views:raise ValueError('Real final captures and primary view exports are required')
    behavior=command_exports(cfg['behavior_log_globs'])
    if not behavior:raise ValueError('No retained original behavior logs')
    source_files=list(cell['input_artifacts'])+[ref(out/x['file']) for x in snapshot['overlay']['archives']]+[ref(out/'snapshot.json')]
    source_files.extend(ref(out/part['file']) for item in snapshot['overlay'].get('split_files',[]) for part in item['parts'])
    source_files.extend(retain(name) for name in cfg.get('direct_source_files',[]))
    for relative in cfg.get('additional_source_repository_paths',[]):
        path=(repo/relative).resolve();path.relative_to(repo.resolve());source_files.append(ref(path))
    product={'schema_version':1,'cell_id':name,'preview_command':cfg['preview_command'],'capture_conditions':cfg['capture_conditions'],'source_files':source_files,'screenshots':screenshots,'behavior_logs':behavior,'viewed_screenshots':views,'capture_lineage':cfg.get('capture_lineage','See retained capture metadata and primary visual review for exact source/state scope.'),'all_original_evidence':'The byte-complete input/overlay reconstruction also retains baseline, research, failed attempts and captures outside this final-product index.'}
    write(out/'product-evidence.json',product)
    if 'all_original_evidence' in cfg:
        product['all_original_evidence']=cfg['all_original_evidence']
        write(out/'product-evidence.json',product)
    main_tools=behavior.copy()
    for rel in cfg.get('additional_tool_exports',[]):main_tools.append(retained_export(rel,'actual tool call as named in retained record','Full actual tool return captured by the primary participant; scope is identified in the original record.'))
    for item in views:main_tools.append(item['view_export'])
    children=[]
    for c in cfg.get('children',[]):
        completion=ref(repo/c['completion_repository_path']) if 'completion_repository_path' in c else retain(c['completion'])
        tools=command_exports(c.get('command_globs',[]))
        for rel in c.get('tool_exports',[]):tools.append(retained_export(rel,'actual child tool call as named in retained record','Original child research/inspection tool output; retained independently from the parent report.'))
        role=c['role']
        children.append({'agent_id':c['agent_id'],'parent_agent_id':cfg['agent_id'],'fork_turns':'none','status':'completed','role':role,'prompt':ref(repo/c['prompt_repository_path']) if 'prompt_repository_path' in c else retain(c['prompt']),'spawn':retained_export(c['spawn'],'collaboration.spawn_agent','Faithful original child-spawn response containing the actual canonical agent ID; the separate request is retained in the full workspace.'),'completion':export(completion,c.get('completion_source','collaboration notification'),'Faithful actual child completion notification/status observation; full delivered research text is separately retained.'),'tool_outputs':tools,'result':retain(c['result']),'role_instruction_sha256':cell['role_instruction_files'].get(role),'model_requested':cell['subagent_model'],'model_resolved':None})
    spawn_path=(repo/cfg['spawn_repository_path']).resolve();completion_path=(repo/cfg['completion_repository_path']).resolve()
    spawn_path.relative_to(repo);completion_path.relative_to(repo)
    spawn=json.loads(spawn_path.read_text());completion=json.loads(completion_path.read_text())
    if spawn['result']['task_name']!=cfg['agent_id'] or completion['agent_id']!=cfg['agent_id'] or completion['message_type']!='FINAL_ANSWER':raise ValueError('Actual primary completion/spawn identity differs')
    if spawn['request']['fork_turns']!='none':raise ValueError('Fresh fork_turns none required')
    start=iso(cfg['started_at']);end=iso(cfg['completed_at'])
    if datetime.fromisoformat(start)>datetime.fromisoformat(end):raise ValueError('Invalid run chronology')
    if not cfg.get('timing_scope'):raise ValueError('Actual timestamp evidence scope is required; export time is not execution start')
    audit={'schema_version':1,'kind':'coordinator-derived execution audit, not a raw tool event','cell_id':name,'agent_id':cfg['agent_id'],'frozen_method_changes':snapshot['method_changes'],'frozen_role_changes':snapshot['role_changes'],'reconstruction':ref(out/'reconstruction-check/command.json'),'source_change_paths':[p for p in snapshot['changed_or_added'] if p.startswith('app/')],'declared_execution_interval_seconds':(datetime.fromisoformat(end)-datetime.fromisoformat(start)).total_seconds(),'timing_scope':cfg['timing_scope'],'observations':cfg['audit_observations'],'limitations':cfg['limitations'],'report_references':[retain(p) for p in cfg.get('report_files',[])]}
    audit['prompt_deviation']=ref(repo/cfg['prompt_deviation_audit'])
    audit['prompt_identity_scope']='run.prompt_sha256 identifies the frozen registered prompt only; actual dispatch differs and is retained in prompt_deviation. No byte-identical actual dispatch claim is made.'
    write(out/'execution-audit.json',audit)
    record={'schema_version':2,'execution_kind':'real_session_agent','simulation':True,'status':'completed','cell_id':name,'candidate_source_identity':plan['candidate_source_identity'],'registration_sha256':sha((study/'registration.json').read_bytes()),'task_sha256':cell['task_sha256'],'prompt_sha256':cell['prompt']['sha256'],'input_workspace_identity':sha(json.dumps(cell['workspace_files'],sort_keys=True).encode()),'environment_sha256':plan['environment']['sha256'],'agent_id':cfg['agent_id'],'parent_agent_id':'/root','fork_turns':'none','started_at':start,'completed_at':end,'spawn':export(ref(spawn_path),'collaboration.spawn_agent','Exact actual primary spawn arguments and returned canonical ID.'),'completion':export(ref(completion_path),'collaboration FINAL_ANSWER notification','Faithful export of the actual visible primary completion notification.'),'tool_outputs':main_tools,'result':ref(out/'FINAL.md.txt'),'children':children,'execution_audit':ref(out/'execution-audit.json'),'product_evidence_index':ref(out/'product-evidence.json'),'model_observation':{'main_requested':cell['main_model'],'subagent_requested':cell['subagent_model'],'main_resolved':None,'subagent_resolved':None,'scope':'Actual omitted model overrides mean inherited session defaults; explicit experimental requests, where present, remain requests. The host does not expose authenticated resolved backend identities.'},'metrics':{'native_usage_tokens':None,'native_billing_cost':None,'main_context_pressure':None,'unavailable_reason':'The session collaboration interface does not expose native per-thread token/billing/context telemetry. Values are not inferred from duration or tool counts.'},'limitations':cfg['limitations']}
    record['attempt_kind']='supplementary_replacement_attempt'
    record['registration_scope']='Reference to the original registered cell; actual dispatch differs. This supplementary record is not an assertion of exact original-protocol execution.'
    record['prompt_deviation']=audit['prompt_deviation']
    record['prompt_identity_scope']=audit['prompt_identity_scope']
    actual_message=spawn['request']['message'].encode()
    record['actual_dispatched_prompt_sha256']=sha(actual_message)
    write(out/'run.json',record)
    write(out/'index-configuration.json',cfg)
    print(json.dumps({'cell':name,'screenshots':len(screenshots),'primary_views':len(views),'raw_behavior_logs':len(behavior),'children':len(children),'declared_execution_interval_seconds':audit['declared_execution_interval_seconds']},indent=2))
if __name__=='__main__':main()
