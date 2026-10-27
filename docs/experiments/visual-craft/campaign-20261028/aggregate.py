"""Derive descriptive results from original observations; never manufacture missing runs."""
from pathlib import Path
from datetime import datetime, timedelta
from statistics import median
import hashlib, json, sys

base=Path(__file__).resolve().parents[1]
partial='--partial' in sys.argv
assignment=json.loads((base/'private/assignment.frozen.json').read_text())
schedule=[r for wave in assignment['waves'] for r in wave]
blind=json.loads((base/'private/blind-map.json').read_text())['map']
label_by_run={r['run_id']:r['anonymous_id'] for r in blind}
run_by_label={r['anonymous_id']:r['run_id'] for r in blind}
events=[json.loads(line) for line in (base/'private/run-events.jsonl').read_text().splitlines() if line]
starts={r['run_id']:r for r in events if r['event']=='spawned'}
dims=[r['id'] for r in json.loads((base/'private/review-rubric.json').read_text())['dimensions']]

def time(s): return datetime.fromisoformat(s.replace('Z','+00:00'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

rows=[]
for spec in schedule:
 rid=spec['run_id'];folder=base/'frozen'/rid;ev=base/'evaluations'/rid
 if not (folder/'FROZEN.json').exists() or not (ev/'results.json').exists():
  if partial: continue
  raise SystemExit('Incomplete assigned output: '+rid)
 frozen=json.loads((folder/'FROZEN.json').read_text());result=json.loads((ev/'results.json').read_text())
 if len(result['groups'])!=10:raise SystemExit('Not ten acceptance groups: '+rid)
 supplement_path=base/'contract-supplement'/rid/'results.json'
 supplement=json.loads(supplement_path.read_text()) if supplement_path.exists() else None
 supplement_complete=bool(supplement and supplement.get('finishedAt') and len(supplement['groups'])=={'T1':2,'T2':8,'T3':4}[spec['task']])
 if not supplement_complete and not partial:raise SystemExit('Missing complete contract supplement: '+rid)
 supplemental_by_id={g['id']:g for g in supplement['groups']} if supplement_complete else {}
 combined=[]
 for original in result['groups']:
  extra=supplemental_by_id.get(original['id'])
  passed=original['status']=='pass' and (not extra or extra['status']=='pass')
  combined.append({'id':original['id'],'name':original['name'],'status':'pass' if passed else 'fail',
                   'error':original.get('error') or (extra or {}).get('error'),
                   'assertions':original['assertions']+(extra or {}).get('assertions',[]),
                   'original_status':original['status'],'supplement_status':extra['status'] if extra else 'not-applicable-or-not-yet-run'})
 commands=[];mismatches=[];malformed=[]
 for p in sorted((folder/'app/evidence/commands').glob('*.json')):
  try:record=json.loads(p.read_text())
  except (json.JSONDecodeError,UnicodeDecodeError) as error:
   malformed.append({'record_file':str(p.relative_to(folder/'app')),'error':str(error)});continue
  record['record_file']=str(p.relative_to(folder/'app'));commands.append(record)
  output=p.parent/record['output_file']
  if not output.exists() or digest(output)!=record['output_sha256']:mismatches.append(record['record_file'])
 commands.sort(key=lambda r:r['started_at'])
 builds=[r for r in commands if r.get('argv',[])[:3]==['npm','run','build']]
 good=[r for r in builds if r.get('exit_code')==0 and r['record_file'] not in mismatches]
 launch=starts.get(rid,{}).get('launch_window_utc')
 elapsed=(time(frozen['frozen_at'])-time(launch)).total_seconds()/60 if launch else None
 first_build=(time(good[0]['started_at'])-time(launch)).total_seconds()/60 if launch and good else None
 timeline=json.loads((ev/'temporal/timeline.json').read_text()) if (ev/'temporal/timeline.json').exists() else None
 diagnostics=json.loads((ev/'diagnostics/diagnostics.json').read_text()) if (ev/'diagnostics/diagnostics.json').exists() else None
 counts={'static_standardized_captures':len(result['captures']),'supplemental_contract_captures':len(supplement['captures']) if supplement_complete else 0,'temporal_frames':len(timeline['frames']) if timeline else 0,'continuous_clips':int(bool(timeline and (ev/'temporal'/timeline['video']).exists()))}
 row={k:spec[k] for k in ['run_id','task','replicate','arm','wave']}
 row.update(anonymous_id=label_by_run[rid],version=assignment['versions'][spec['arm']][0],functional_passes=result['functionalPasses'],functional_total=result['functionalTotal'],failures=[{'group':g['id'],'name':g['name'],'error':g.get('error'),'assertions':g['assertions']} for g in result['groups'] if g['status']!='pass'],page_errors=result['uniquePageErrors'],console_error_count=len(result['consoleErrors']),immutable_inputs=frozen['immutable_inputs'],frozen_at=frozen['frozen_at'],build_present=frozen['build_present'],wall_minutes_launch_window_to_freeze=round(elapsed,2) if elapsed is not None else None,first_successful_logged_build_minutes=round(first_build,2) if first_build is not None else None,retained_command_records=len(commands),command_output_digest_mismatches=mismatches,logged_build_commands=len(builds),logged_successful_builds=len(good),dist_bytes=sum(f['bytes'] for f in result['diagnostics']['buildFiles']),capture_counts=counts,temporal_errors=timeline.get('errors',[]) if timeline else ['missing'],asset_diagnostic=diagnostics,evidence_sha256={'freeze_manifest':digest(folder/'FROZEN.json'),'independent_results':digest(ev/'results.json')})
 row.update(initial_functional_passes=result['functionalPasses'],functional_passes=sum(g['status']=='pass' for g in combined),functional_verification_complete=supplement_complete,
            functional_scope='Original ten groups AND uniform supplemental checks of previously omitted published-contract conditions; original observations preserved.',
            supplemental_group_checks={'passed':supplement['functionalPasses'],'total':supplement['functionalTotal']} if supplement_complete else None,
            failures=[{'group':g['id'],'name':g['name'],'error':g['error'],'assertions':g['assertions'],'original_status':g['original_status'],'supplement_status':g['supplement_status']} for g in combined if g['status']!='pass'])
 row['malformed_command_records']=malformed
 row['retained_command_record_files']=len(commands)+len(malformed)
 row['retained_command_records']=len(commands)
 if supplement_complete:
  row['page_errors']=sorted(set(result['uniquePageErrors']+supplement['uniquePageErrors']))
  row['console_error_count']+=len(supplement['consoleErrors'])
  row['evidence_sha256']['contract_supplement']=digest(supplement_path)
 rows.append(row)

reviews=[]
for index in range(1,4):
 p=base/'reviews'/('R'+str(index))/'ratings.json'
 if not p.exists():
  if partial:continue
  raise SystemExit('Missing independent review '+str(index))
 review=json.loads(p.read_text())
 if {r['anonymous_id'] for r in review['outputs']}!=set(run_by_label):raise SystemExit('Reviewer output set mismatch '+str(index))
 for output in review['outputs']:
  if set(output['scores'])!=set(dims):raise SystemExit('Score dimensions mismatch')
  for d,value in output['scores'].items():
   if type(value) is not int or not 0<=value<=4:raise SystemExit('Score outside ordinal anchors')
   if not output['evidence'].get(d):raise SystemExit('Missing exact visual evidence')
 for family in ['T1','T2','T3']:
  rankings=[r for r in review['family_rankings'] if r['task']==family]
  if len(rankings)!=1:raise SystemExit('Missing family ranking')
  labels=[x for tier in rankings[0]['ordered_tiers'] for x in tier]
  expected={r['anonymous_id'] for r in blind if r['task']==family}
  if len(labels)!=4 or set(labels)!=expected:raise SystemExit('Ranking membership mismatch')
 reviews.append({'reviewer':'R'+str(index),'sha256':digest(p),'data':review})

row_by_id={r['run_id']:r for r in rows}
for row in rows:
 ratings=[next(x for x in r['data']['outputs'] if x['anonymous_id']==row['anonymous_id']) for r in reviews]
 row['visual']={d:{'ratings':[r['scores'][d] for r in ratings],'median':median([r['scores'][d] for r in ratings]),'range':[min(r['scores'][d] for r in ratings),max(r['scores'][d] for r in ratings)]} for d in dims} if ratings else None
pairs=[]
for task in ['T1','T2','T3']:
 for rep in [1,2]:
  pair=[r for r in rows if r['task']==task and r['replicate']==rep]
  if len(pair)!=2:continue
  a=next(r for r in pair if r['arm']=='A');b=next(r for r in pair if r['arm']=='B')
  preferences=[]
  for review in reviews:
   tiers=next(r for r in review['data']['family_rankings'] if r['task']==task)['ordered_tiers']
   rank={label:i for i,tier in enumerate(tiers) for label in tier}
   vote='B' if rank[b['anonymous_id']]<rank[a['anonymous_id']] else 'A' if rank[a['anonymous_id']]<rank[b['anonymous_id']] else 'tie'
   preferences.append({'reviewer':review['reviewer'],'preference':vote})
  majority=next((v for v in ['A','B','tie'] if sum(p['preference']==v for p in preferences)>=2),None)
  pairs.append({'task':task,'replicate':rep,'A':a['run_id'],'B':b['run_id'],'functional_delta_B_minus_A':b['functional_passes']-a['functional_passes'],'visual_median_deltas':{d:b['visual'][d]['median']-a['visual'][d]['median'] for d in dims} if reviews else None,'reviewer_preferences':preferences,'majority_preference':majority if reviews else None})
arms={}
for arm in ['A','B']:
 subset=[r for r in rows if r['arm']==arm]
 arms[arm]={'version':assignment['versions'][arm][0],'runs':len(subset),'functional_passes':sum(r['functional_passes'] for r in subset),'functional_groups':sum(r['functional_total'] for r in subset),'all_ten_passed_runs':sum(r['functional_passes']==10 for r in subset),'runs_with_page_errors':sum(bool(r['page_errors']) for r in subset),'wall_minutes':{'median':median([r['wall_minutes_launch_window_to_freeze'] for r in subset]),'range':[min(r['wall_minutes_launch_window_to_freeze'] for r in subset),max(r['wall_minutes_launch_window_to_freeze'] for r in subset)]} if subset else None,'visual_run_median_summary':{d:{'median':median([r['visual'][d]['median'] for r in subset]),'range':[min(r['visual'][d]['median'] for r in subset),max(r['visual'][d]['median'] for r in subset)]} for d in dims} if reviews and subset else None}
out={'scope':'DESCRIPTIVE_COMPLETE' if len(rows)==12 and len(reviews)==3 and all(r["functional_verification_complete"] for r in rows) else 'INCOMPLETE_CHECKPOINT','campaign':assignment['campaign'],'versions':assignment['versions'],'runs_completed':len(rows),'reviews_completed':len(reviews),'dimensions':dims,'arms':arms,'runs':rows,'matched_pairs':pairs,'review_files':[{'reviewer':r['reviewer'],'sha256':r['sha256']} for r in reviews],'interpretation_limits':['Three selected task briefs; two independent generations per version per brief; one inherited model/harness, exact backend checkpoint and random seed unavailable.','Three independent model reviewers share the same model family; no human-user test or statistical generalization.','Six separate ordinal visual dimensions; no summed aesthetic score or percentage capability uplift.','Wall time uses approximate launch windows and evaluator freeze times, not active thinking time.','First successful logged build can be the unmodified starter; it is not time to completed implementation.','Command records are a retained subset, not all tool calls. The provided logger numbers records from completed-file count; concurrent wrapper processes can overwrite a number. Do not treat retained counts as total work or total cost. Digest mismatches are separately reported.','Complete frontend fixture journeys do not establish production search/backend capability, physical-device performance, screen-reader usability or commercial product equivalence.','Ordered samples and a retained continuous clip do not prove that reviewers watched natural playback or establish FPS.']}
dest=base/'analysis';dest.mkdir(exist_ok=True)
file=dest/('checkpoint.json' if partial else 'results.json');file.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'scope':out['scope'],'runs':len(rows),'reviews':len(reviews),'output':str(file),'commands_with_digest_mismatch':sum(len(r['command_output_digest_mismatches']) for r in rows)},ensure_ascii=False))
