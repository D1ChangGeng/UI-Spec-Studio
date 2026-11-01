#!/usr/bin/env python3
"""Freeze actual application/Skill inputs before dispatching any participant."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile

ROOT=Path('/workspace/scratch/708e8b7f118e/UI-Spec-Studio')
WORK=Path('/workspace/scratch/708e8b7f118e/ui-study')
PREP=Path('/workspace/scratch/708e8b7f118e/ui-study-prep')
EVIDENCE=ROOT/'docs/evidence/v1.20.0/session-study'
sys.path.insert(0,str(ROOT/'tools'))
from check_adaptive_release import candidate_identity

def digest(raw):return hashlib.sha256(raw).hexdigest()
def write_json(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def ref(path):return {'path':path.relative_to(ROOT).as_posix(),'sha256':digest(path.read_bytes())}
def hashes(path):return {p.relative_to(path).as_posix():digest(p.read_bytes()) for p in sorted(path.rglob('*')) if p.is_file() and not p.is_symlink() and not any(v in p.relative_to(path).parts for v in ('node_modules','__pycache__','.git'))}
def zip_files(path,root,paths):
 path.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
  for name in sorted(paths):
   info=zipfile.ZipInfo(name,(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
   if (root/name).stat().st_mode & 0o111:info.external_attr=0o100755<<16
   z.writestr(info,(root/name).read_bytes())

def main():
 if (EVIDENCE/'registration.json').exists():raise SystemExit('Registration already exists; never overwrite it')
 manifest=json.loads((PREP/'starter-manifest.json').read_text())
 originals=json.loads((ROOT/'docs/experiments/adaptive-research/plan.example.json').read_text())['cells']
 baseline=WORK/'baseline/skills/ui-spec';candidate=ROOT/'skills/ui-spec'
 bm,cm=hashes(baseline),hashes(candidate)
 inputs=EVIDENCE/'inputs';inputs.mkdir(exist_ok=True)
 zip_files(inputs/'method-v1.19.0.zip',baseline,bm);zip_files(inputs/'method-v1.20.0.zip',candidate,cm)
 role_root=ROOT/'integrations/codex/agents';roles={p.stem:digest(p.read_bytes()) for p in sorted(role_root.glob('*.toml'))}
 zip_files(inputs/'distributed-role-instructions.zip',role_root,[p.name for p in role_root.glob('*.toml')])
 starter_refs={}
 for task,item in manifest['tasks'].items():
  source=PREP/'starters'/task
  for name,metadata in item['input_files'].items():
   if digest((source/name).read_bytes())!=metadata['sha256']:raise RuntimeError('Starter changed: '+task+'/'+name)
  archive=inputs/(task+'-input.zip');zip_files(archive,source,item['input_files']);starter_refs[task]=ref(archive)
  print(task,'input archive bytes',archive.stat().st_size)
 shutil.copy2(PREP/'starter-manifest.json',inputs/'starter-manifest.json')
 shutil.copy2(PREP/'PREPARATION.md',inputs/'PREPARATION.md')
 cells=[]
 for number,original in enumerate(originals,1):
  cell=dict(original);task,condition=cell['task'],cell['condition'];work=WORK/'worksets'/f'w{number:02d}'
  if work.exists():raise RuntimeError('Fresh work package already exists')
  source=PREP/'starters'/task;item=manifest['tasks'][task]
  for name in item['input_files']:
   target=work/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/name,target)
  method=candidate if condition.startswith(('F-','G-')) else baseline
  shutil.copytree(method,work/'method')
  shutil.copytree(WORK/'support',work/'support');shutil.copy2(WORK/'support/RUN-CONTROL.md',work/'RUN-CONTROL.md')
  specialized=condition not in ('A','B')
  if specialized:shutil.copytree(role_root,work/'roles')
  requested='gpt-6.1-terra' if condition=='D' else 'session-default-inherited'
  allocation=['# Work allocation','',f'Work package: `{work}`. Use a unique local port, suggested {4400+number}.',
              'The main agent retains the complete product goal, all final design choices and assembled-product inspection.',
              'Keep primary implementation in the main agent except for the explicitly assigned settled integration scope.']
  if condition in ('A','F-main'):
   allocation+=['Carry out this work in your own fresh context. Do not delegate to other agents.']
  elif condition in ('B','C','D','E-challenger','E-observer'):
   allocation+=['Delegate the substantive research inquiry in `RESEARCH-PROMPT.md` to one fresh independent child using `collaboration.spawn_agent` with `fork_turns: "none"`. Send the file contents exactly. You may send a focused follow-up within that same inquiry if actual evidence requires it. Do not delegate product code changes. Inspect the important returned evidence yourself and make the design choice.']
   if condition=='D':allocation+=['For this research child request `model: "gpt-6.1-terra"`; leave reasoning effort inherited. Record the actual requested configuration. Do not infer the resolved backend model.']
   else:allocation+=['Leave the child model and reasoning effort unspecified so the session defaults are inherited.']
   if condition.startswith('E-'):
    extra='ui_challenger' if condition=='E-challenger' else 'ui_experience_observer'
    allocation+=[f'After the research inquiry, delegate a consequential independent inquiry to a fresh `{extra}` instruction-role child. Read `roles/{extra}.toml` and use its developer_instructions as the role guidance with the current task and evidence needed for that inquiry. Preserve its exact dispatched prompt and actual tool results. This child does not implement the product.']
  elif condition=='F-integrator':
   allocation+=['Independently inspect the selected source and settled `INTEGRATION-DECISION.md`. Delegate only its bounded implementation to a fresh child following `roles/ui_integrator.toml`, with exact allowed files and state contract. Record the prompt and actual child tool outputs. After the child returns, personally inspect the assembled application and neighboring experience; you own design acceptance and any necessary coordination. Leave model and effort inherited.']
  else:
   allocation+=['All four distributed instruction roles are available in `roles/`. Decide adaptively whether an independent inquiry or settled bounded integration would help this specific task. You may complete a well-supported task directly. If delegating, use fresh contexts, read the appropriate role instructions, keep research and implementation responsibilities distinct, and retain actual coordination/tool exports. Model and effort inherit the session defaults.']
  allocation+=['Use at most one live child at a time and at most two children overall. Keep the substantive work bounded to 30 minutes; if a genuine blocker or quality gap remains, preserve it honestly instead of claiming completion.','Save child coordination exports and the child report references in `DELEGATION.json` if any child is used. The exact schemas can be simple: retain original tool requests/results rather than creating native-looking events.','Keep normal source and role instructions unchanged. Save actual product changes, captured observations and FINAL.md.']
  (work/'ALLOCATION.md').write_text('\n\n'.join(allocation)+'\n')
  inquiry=(f'Use the complete ui-spec method at {work}/method/ to investigate the consequential UI source and experience questions in {work}/TASK.md and {work}/INPUT.md. Read {work}/RUN-CONTROL.md for evidence and environment conditions. Inspect the current app and relevant mature public products/implementations; search, genuinely observe, compare and refine the inquiry where evidence warrants. Return concise decision-useful sources, actual observed relationships, materially different candidates where useful, practical adoption paths and unresolved limits, with original tool outputs and real viewed captures retained under {work}/evidence/research/. Do not change product code or make final product design decisions. Work only on this package and relevant public sources. Do not create further agents. Save a final research report and return its contents.')
  if specialized and condition in ('C','D','E-challenger','E-observer'):
   inquiry=f'Read and follow the developer_instructions in {work}/roles/ui_researcher.toml as your specialized research role.\n\n'+inquiry
  (work/'RESEARCH-PROMPT.md').write_text(inquiry+'\n')
  prompt=(f'Use the ui-spec Skill in {work}/method/ to complete the application task in {work}/TASK.md and {work}/INPUT.md. Read and follow {work}/RUN-CONTROL.md and {work}/ALLOCATION.md. Work only in that work package and relevant public sources. Complete the running product, keep actual tool/capture evidence, and deliver FINAL.md. Retain primary design responsibility and verify actual visual output. Do not inspect sibling work packages or coordinating release records.')
  prompt_file=EVIDENCE/'prompts'/(cell['id']+'.txt');prompt_file.parent.mkdir(exist_ok=True);prompt_file.write_text(prompt)
  workspace=hashes(work)
  instruction_files={k:v for k,v in workspace.items() if not k.startswith(('app/','method/','roles/'))}
  instr_archive=inputs/(cell['id']+'-instructions.zip');zip_files(instr_archive,work,instruction_files)
  cell.update({'work_package':str(work),'prompt':ref(prompt_file),'input_artifacts':[starter_refs[task],ref(inputs/('method-v1.20.0.zip' if condition.startswith(('F-','G-')) else 'method-v1.19.0.zip')),ref(instr_archive)],'workspace_files':workspace,'starter_files':{k:v['sha256'] for k,v in item['input_files'].items()},'method_files':cm if condition.startswith(('F-','G-')) else bm,'role_instruction_files':roles if specialized else {},'task_sha256':item['task_sha256'],'main_model':'session-default-inherited','subagent_model':requested,'main_effort':'session-default-inherited','subagent_effort':'session-default-inherited','timeout_seconds':1800,'max_subagents':2,'tool_profile':'session-tools-2026-11-01-with-pinned-chromium'})
  if specialized:cell['input_artifacts'].append(ref(inputs/'distributed-role-instructions.zip'))
  cells.append(cell)
  if task=='T2':shutil.copytree(PREP/'dependencies/T2-node_modules',work/'app/node_modules',symlinks=True)
  print(cell['id'],work)
 frozen=datetime.datetime.now(datetime.timezone.utc).isoformat()
 plan={'schema_version':2,'study_kind':'owner_authorized_session_simulation','candidate_source_identity':candidate_identity(ROOT),'candidate_source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'baseline_commit':'05d0286b0b27e8e57d5751d5cf649c8800408001','frozen_at':frozen,'environment':ref(EVIDENCE/'environment.json'),'host_limitations':'Actual independent fresh-context agents share the session host/system/tool catalog and filesystem. Role instructions simulate the unavailable native role environment. Raw available tool/command evidence is retained, but native role binding, resolved model/effort, tokens/bills and hidden traces are unavailable. One run per cell supports scoped findings only. All apps use synthetic non-private content.','baseline_method_files':bm,'candidate_method_files':cm,'cells':cells,'dispatch_policy':'Use registered task/condition inputs in fresh disjoint workspaces; keep a child slot available. Interleave tasks and conditions where capacity permits, with no participant access to prior outputs. Execution chronology and actual network drift are retained rather than claimed randomized.','comparison_limits':'Not randomized, not repeated, one host, no human panel. A/B/C share complete baseline method; C/D differ in requested child model only at the configured condition level, while natural task execution may vary. E and G are bounded process/product observations, not proven causal generalization.'}
 write_json(EVIDENCE/'registration.json',plan)
 write_json(WORK/'dispatch-map.json',[{'id':c['id'],'work_package':c['work_package'],'prompt':(ROOT/c['prompt']['path']).read_text()} for c in cells])
 print('FROZEN',frozen,'identity',plan['candidate_source_identity'],'registration bytes',(EVIDENCE/'registration.json').stat().st_size)

if __name__=='__main__':main()
