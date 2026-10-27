from pathlib import Path
import datetime,hashlib,json,shutil,sys
base=Path(__file__).resolve().parents[1]
rid=sys.argv[1]
assignment=json.loads((base/'private/assignment.frozen.json').read_text())
cell=next(c for wave in assignment['waves'] for c in wave if c['run_id']==rid)
src=Path(cell['path'])/'app';dest=base/'frozen'/rid/'app'
if dest.exists():raise SystemExit('Already frozen: '+rid)
shutil.copytree(src,dest,symlinks=True,ignore=shutil.ignore_patterns('.git','node_modules','__pycache__'))
# Retain normal installed-module links only as operational pointers; all published
# source and final build files are fingerprinted independently.
if (src/'node_modules').exists():(dest/'node_modules').symlink_to((src/'node_modules').resolve(),target_is_directory=True)
files={}
for p in sorted(dest.rglob('*')):
 if p.is_file() and not p.is_symlink() and 'node_modules' not in p.parts:
  files[str(p.relative_to(dest))]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
immutable=['src/domain.js']+(['src/Shell.jsx'] if cell['task']=='T3' else [])
checks={p:files.get(p,{}).get('sha256')==assignment['task_files'][cell['task']].get(p) for p in immutable}
record={'run_id':rid,'task':cell['task'],'replicate':cell['replicate'],'arm':cell['arm'],'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_path':str(src),'frozen_path':str(dest),'immutable_inputs':checks,'build_present':(dest/'dist/index.html').exists(),'files':files,'scope':'Participant final state, frozen without evaluator source repairs'}
(dest.parent/'FROZEN.json').write_text(json.dumps(record,indent=2)+'\n')
with (base/'private/run-events.jsonl').open('a') as f:f.write(json.dumps({'event':'frozen','run_id':rid,'at':record['frozen_at'],'files':len(files),'build_present':record['build_present'],'immutable_inputs':checks})+'\n')
print(json.dumps({k:record[k] for k in ('run_id','task','frozen_at','frozen_path','build_present','immutable_inputs')},indent=2))
