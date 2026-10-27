from pathlib import Path
import datetime, hashlib, json
base=Path(__file__).resolve().parents[1]
a=json.loads((base/'private/assignment.frozen.json').read_text())
events=[json.loads(x) for x in (base/'private/run-events.jsonl').read_text().splitlines() if x]
launched={x['run_id'] for x in events if x['event']=='spawned'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'skill_snapshots':[],'unlaunched_initial_inputs':[],'shared_runtime':{},'frozen_outputs':[]}
for row in [r for wave in a['waves'] for r in wave]:
 rid=row['run_id'];root=Path(row['path']);expected=a['skill_files'][row['arm']]
 actual={str(p.relative_to(root/'skill')):sha(p) for p in (root/'skill').rglob('*') if p.is_file()}
 out['skill_snapshots'].append({'run_id':rid,'files':len(actual),'exact_match':actual==expected})
 if rid not in launched:
  findings={name:sha(root/'app'/name)==value for name,value in row['initial_files'].items()}
  out['unlaunched_initial_inputs'].append({'run_id':rid,'all_registered_files_match':all(findings.values()),'mismatches':[k for k,v in findings.items() if not v]})
 frozen=base/'frozen'/rid/'FROZEN.json'
 if frozen.exists():
  f=json.loads(frozen.read_text());mismatch=[name for name,meta in f['files'].items() if sha(frozen.parent/'app'/name)!=meta['sha256']]
  out['frozen_outputs'].append({'run_id':rid,'recorded_files':len(f['files']),'digest_mismatches':mismatch})
for name,value in a['runtime_files'].items():out['shared_runtime'][name]={'sha256':sha(base.parent/'ui-eval-runtime'/name),'matches_registration':sha(base.parent/'ui-eval-runtime'/name)==value}
(base/'private/control-integrity.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'skill_snapshots_match':sum(x['exact_match'] for x in out['skill_snapshots']),'skill_snapshots_total':len(out['skill_snapshots']),'unlaunched_inputs_match':all(x['all_registered_files_match'] for x in out['unlaunched_initial_inputs']),'frozen_file_mismatches':sum(len(x['digest_mismatches']) for x in out['frozen_outputs']),'shared_runtime_match':all(x['matches_registration'] for x in out['shared_runtime'].values())}))
