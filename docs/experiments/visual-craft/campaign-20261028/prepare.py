from pathlib import Path
import hashlib,io,json,random,shutil,subprocess,tarfile,datetime

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent/'ui-spec-studio'
RUNTIME=ROOT.parent/'ui-eval-runtime'
RUNS=ROOT.parent/'participant-workspaces'
VERSIONS={'A':('v1.15.0','a89091dfa5754f98b79655c684f978f24fd92716'),'B':('v1.16.0','1ba50b1e1c6dfbd5540d9b54514ef81ac6160eec')}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files(p):return {str(f.relative_to(p)):sha(f) for f in sorted(p.rglob('*')) if f.is_file() and 'node_modules' not in f.parts and 'dist' not in f.parts}
def clean_copy(src,dst):
 shutil.copytree(src,dst,ignore=shutil.ignore_patterns('node_modules','dist','evidence','__pycache__'),symlinks=False)

if (ROOT/'private/assignment.json').exists():raise SystemExit('Already prepared; inputs are not overwritten')
rng=random.Random(20261028)
waves=[]
for rep in (1,2):
 choices=['A','B','A'] if rep==1 else ['B','A','B']
 rng.shuffle(choices)
 first=[{'task':f'T{i+1}','replicate':rep,'arm':arm} for i,arm in enumerate(choices)]
 second=[{**x,'arm':'B' if x['arm']=='A' else 'A'} for x in first]
 rng.shuffle(first);rng.shuffle(second);waves.extend([first,second])
assignment={'campaign':'visual-craft-20261028','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'randomization_seed':20261028,'versions':VERSIONS,'budget_minutes':35,'waves':[],'skill_files':{},'task_files':{},'runtime_files':{}}
for arm,(tag,commit) in VERSIONS.items():
 dest=ROOT/'private/snapshots'/arm
 dest.mkdir(parents=True)
 data=subprocess.check_output(['git','archive',commit,'skills/ui-spec'],cwd=REPO)
 with tarfile.open(fileobj=io.BytesIO(data)) as archive:
  for m in archive.getmembers():
   if not m.isfile():continue
   rel=Path(m.name).relative_to('skills/ui-spec');p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(archive.extractfile(m).read())
 assignment['skill_files'][arm]=files(dest)
for task in ('T1','T2','T3'):
 required=['TASK.md','CONTRACT.md','acceptance.json','src/domain.js','package.json']
 for f in required:assert (ROOT/'fixtures'/task/f).is_file(),(task,f)
 assignment['task_files'][task]=files(ROOT/'fixtures'/task)
for name in ('package.json','package-lock.json'):assignment['runtime_files'][name]=sha(RUNTIME/name)
for w,wave in enumerate(waves,1):
 group=[]
 for cell in wave:
  run='p'+''.join(rng.choices('0123456789abcdef',k=7));folder=RUNS/run
  clean_copy(ROOT/'fixtures'/cell['task'],folder/'app')
  clean_copy(ROOT/'private/snapshots'/cell['arm'],folder/'skill')
  (folder/'app/node_modules').symlink_to(RUNTIME/'node_modules',target_is_directory=True)
  (folder/'app/tools').mkdir()
  for name in ('run.py','capture.mjs'):shutil.copy2(ROOT/'support'/name,folder/'app/tools'/name)
  shutil.copy2(ROOT/'support/ENVIRONMENT.md',folder/'app/ENVIRONMENT.md')
  if cell['task']=='T1':(folder/'references').symlink_to(ROOT/'references',target_is_directory=True)
  group.append({**cell,'run_id':run,'wave':w,'path':str(folder),'status':'prepared_not_run','prompt_sha256':sha(folder/'app/TASK.md'),'initial_files':files(folder/'app'),'skill_file_count':len(assignment['skill_files'][cell['arm']])})
 assignment['waves'].append(group)
protocol=ROOT/'private/PROTOCOL.md';assignment['protocol_sha256']=sha(protocol)
(ROOT/'private/assignment.json').write_text(json.dumps(assignment,indent=2)+'\n')
print(json.dumps({'waves':[[{k:c[k] for k in ('run_id','task','replicate','arm','path')} for c in w] for w in assignment['waves']],'protocol_sha256':assignment['protocol_sha256']},indent=2))
