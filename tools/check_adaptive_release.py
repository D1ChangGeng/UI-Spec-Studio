#!/usr/bin/env python3
"""Fail closed on missing v1.20 release evidence; never judge aesthetic quality.

This maintainer-only consistency check is not an installed Skill inspector. It
checks declared identities and artifact references, not whether a human judgment
is correct or whether a UI is beautiful. Actual review remains indispensable.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
BASE='05d0286b0b27e8e57d5751d5cf649c8800408001'
HASH=re.compile(r'[0-9a-f]{64}\Z')
DECISION='docs/evidence/v1.20.0/release-decision.json'
EXCLUDED={'__pycache__','.git','node_modules','dist','.pytest_cache'}

class EvidenceError(ValueError): pass

def digest(raw:bytes)->str: return hashlib.sha256(raw).hexdigest()

def path_at(root:Path,rel:str)->Path:
    if not isinstance(rel,str): raise EvidenceError('Unsafe evidence path')
    p=PurePosixPath(rel)
    if any(':' in part for part in p.parts) or p.is_absolute() or '\\' in rel or '..' in p.parts or not p.parts:
        raise EvidenceError('Unsafe evidence path')
    result=root.absolute()
    for ancestor in (result,*result.parents):
        if ancestor.is_symlink(): raise EvidenceError('Linked evidence root')
    for part in p.parts:
        result/=part
        if result.is_symlink(): raise EvidenceError('Linked evidence is not accepted')
    if not result.is_file(): raise EvidenceError(f'Missing evidence file: {rel}')
    return result

def artifact(root:Path,row:dict)->bytes:
    if not isinstance(row,dict) or not isinstance(row.get('path'),str) or not isinstance(row.get('sha256'),str) or not HASH.fullmatch(row['sha256']):
        raise EvidenceError('Artifact needs a relative path and SHA-256')
    raw=path_at(root,row['path']).read_bytes()
    if digest(raw)!=row['sha256']: raise EvidenceError(f'Evidence identity differs: {row["path"]}')
    return raw

def candidate_files(root:Path)->dict[str,str]:
    files={}
    for prefix in ('skills/ui-spec','integrations/codex','tools','tests','.github/workflows'):
        for p in sorted((root/prefix).rglob('*')):
            if any(x in EXCLUDED for x in p.relative_to(root).parts): continue
            if p.is_symlink(): raise EvidenceError('Candidate contains a symlink')
            if p.is_file() and p.suffix in {'.py','.md','.json','.toml','.yml','.yaml','.txt','.svg','.html','.css','.js'}:
                files[p.relative_to(root).as_posix()]=digest(p.read_bytes())
    for name in ('VERSION','AGENTS.md','docs/MODEL.md','docs/WRITING.md'):
        files[name]=digest(path_at(root,name).read_bytes())
    return dict(sorted(files.items()))

def candidate_identity(root:Path)->str:
    return digest(json.dumps(candidate_files(root),sort_keys=True,separators=(',',':')).encode())

def require_release_evidence(root:Path=ROOT)->dict:
    try:
        decision=json.loads(path_at(root,DECISION).read_bytes())
    except (ValueError,UnicodeError) as exc:
        raise EvidenceError('No readable release decision') from exc
    if not isinstance(decision,dict) or decision.get('schema_version')!=1:
        raise EvidenceError('Unknown release-decision format')
    if decision.get('decision') not in ('approve','approve_limited'):
        raise EvidenceError('v1.20 remains a development candidate: real experiments and acceptance are pending')
    if decision.get('candidate_identity')!=candidate_identity(root):
        raise EvidenceError('The reviewed candidate differs from the current runtime/adapter/tools/tests')
    if decision.get('baseline_commit')!=BASE:
        raise EvidenceError('Unexpected baseline')
    for key in ('reviewer','reviewed_at','scope','limitations'):
        if not isinstance(decision.get(key),str) or not decision[key].strip():
            raise EvidenceError(f'Missing review declaration: {key}')
    report=artifact(root,decision.get('review_report'))
    if not report.strip(): raise EvidenceError('Empty review report')
    plan=json.loads(artifact(root,decision.get('registered_plan')))
    if not isinstance(plan,dict) or plan.get('candidate_source_identity')!=candidate_identity(root):
        raise EvidenceError('Frozen study does not identify the current complete candidate')
    cells=plan.get('cells')
    if not isinstance(cells,list) or not cells:
        raise EvidenceError('No frozen real-execution plan')
    names=[r.get('id') for r in cells if isinstance(r,dict)]
    if len(names)!=len(cells) or any(not isinstance(x,str) or not x for x in names) or len(set(names))!=len(names):
        raise EvidenceError('Invalid or duplicate experiment cells')
    records=decision.get('run_records')
    if not isinstance(records,list) or not records: raise EvidenceError('No actual run records')
    seen=set();sessions=set();conditions=set();tasks=set()
    for reference in records:
        run=json.loads(artifact(root,reference))
        cell=run.get('cell_id')
        if cell not in names or cell in seen: raise EvidenceError('Missing, duplicate or unregistered run')
        seen.add(cell)
        if run.get('simulation') is not False or run.get('status')!='process_completed':
            raise EvidenceError('Blocked, synthetic or failed executions cannot establish completed Agent runs')
        sid=run.get('thread_id')
        if not isinstance(sid,str) or not sid or sid in sessions: raise EvidenceError('Fresh independent session identity required')
        sessions.add(sid)
        events=artifact(root,run.get('events'))
        parsed=[]
        for line in events.splitlines():
            if line.strip():
                try: parsed.append(json.loads(line))
                except ValueError as exc: raise EvidenceError('Malformed execution event log') from exc
        if not any(e.get('type')=='thread.started' and e.get('thread_id')==sid for e in parsed if isinstance(e,dict)):
            raise EvidenceError('Declared thread is absent from its raw event log')
        if not any(e.get('type')=='turn.completed' for e in parsed if isinstance(e,dict)):
            raise EvidenceError('No actual completed turn event')
        item=next(r for r in cells if r['id']==cell)
        if run.get('task_sha256')!=item.get('task_sha256'):
            raise EvidenceError('Task identity changed after registration')
        conditions.add(str(item.get('condition')).split('-')[0]);tasks.add(item.get('task'))
        # The main-agent-only baseline is legitimate; subagent use in relevant
        # arms must be independently inspected, not inferred from a role file.
        artifact(root,run.get('execution_audit'))
        artifact(root,run.get('product_evidence_index'))
    outstanding=set(names)-seen
    exclusions=decision.get('unexecuted_cells',{})
    if not isinstance(exclusions,dict) or set(exclusions)!=outstanding:
        raise EvidenceError('Every planned cell must be executed or explicitly limited')
    if outstanding and decision['decision']!='approve_limited':
        raise EvidenceError('Unexecuted planned cells require an explicitly limited release')
    if any(not isinstance(v,str) or not v.strip() for v in exclusions.values()):
        raise EvidenceError('Missing reason for an unexecuted cell')
    if not {'A','B','C','F','G'} <= conditions or len(tasks)<4:
        raise EvidenceError('Required baseline, generic, specialist, integration and final-runtime comparisons/four task families are absent')
    executed=[r for r in cells if r['id'] in seen]
    pairs=[]
    for task in tasks:
        by_condition={r['condition']:r for r in executed if r['task']==task}
        if {'A','B','C'} <= set(by_condition):
            trio=[by_condition[x] for x in ('A','B','C')]
            for key in ('task_sha256','starter_files','method_files','main_model','main_effort','subagent_model','subagent_effort','timeout_seconds','max_subagents'):
                if not trio[0].get(key) or any(r.get(key)!=trio[0][key] for r in trio[1:]):
                    raise EvidenceError(f'Unmatched A/B/C variable: {key}')
            if any(r.get('network_access',False)!=trio[0].get('network_access',False) for r in trio[1:]):
                raise EvidenceError('Unmatched A/B/C variable: network_access')
            pairs.append(task)
    if not pairs: raise EvidenceError('No actual same-task A/B/C comparison')
    integrations={r['condition']:r for r in executed if r['task']=='T4'}
    if not {'F-main','F-integrator'} <= set(integrations):
        raise EvidenceError('No same-task main-versus-delegated integration pair')
    for key in ('task_sha256','starter_files','method_files','main_model','main_effort','subagent_model','subagent_effort','timeout_seconds','max_subagents'):
        a,b=integrations['F-main'],integrations['F-integrator']
        if not a.get(key) or a[key]!=b.get(key): raise EvidenceError(f'Unmatched integration variable: {key}')
    if integrations['F-main'].get('network_access',False)!=integrations['F-integrator'].get('network_access',False):
        raise EvidenceError('Unmatched integration variable: network_access')
    candidate={p.relative_to(root/'skills/ui-spec').as_posix():digest(p.read_bytes())
               for p in (root/'skills/ui-spec').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    if not candidate or plan.get('candidate_method_files')!=candidate:
        raise EvidenceError('Final candidate Skill was not frozen with exact source identities')
    final_cells=[r for r in executed if r['condition']=='G-final-runtime']
    if not final_cells or any(r.get('method_files')!=candidate for r in final_cells):
        raise EvidenceError('No actual exact final-runtime execution')
    checks=decision.get('engineering_checks',[])
    if not isinstance(checks,list): raise EvidenceError('Invalid engineering checks')
    required={'upstream_unit_suite','package_validation','catalog','readme_art','browser_scenarios','installer_smoke','package_build'}
    checked=set()
    for row in checks:
        if not isinstance(row,dict) or row.get('status')!='passed': raise EvidenceError('Engineering check not passed')
        artifact(root,row.get('log'));checked.add(row.get('name'))
    if not required<=checked: raise EvidenceError('Full existing publication checks are incomplete')
    return {'status':'declared_evidence_consistent','reviewer':decision['reviewer'],
            'actual_run_records':len(records),'limitations':decision['limitations'],
            'boundary':'Artifact consistency does not authenticate every claim or certify visual quality; inspect raw runs and products.'}

if __name__=='__main__':
    try: print(json.dumps(require_release_evidence(),indent=2))
    except (EvidenceError,OSError,ValueError,KeyError,TypeError) as exc:
        print('release evidence: '+str(exc),file=sys.stderr);raise SystemExit(2)
