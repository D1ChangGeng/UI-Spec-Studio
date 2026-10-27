from pathlib import Path
import json,shutil,random,hashlib
base=Path(__file__).resolve().parents[1]
mapping=json.loads((base/'private/blind-map.json').read_text())['map']
dest=base/'blind-review'
dest.mkdir(exist_ok=True)
rubric=json.loads((base/'private/review-rubric.json').read_text())
(dest/'RUBRIC.json').write_text(json.dumps(rubric,indent=2)+'\n')
selected={
'T1':['01-desktop-initial.png','04-source-detail.png','08-long-900.png','08-long-390.png','09-desktop-alternate-theme.png','09-mobile-original-theme.png','09-mobile-alternate-theme.png','07-error.png'],
'T2':['01-desktop-initial.png','02-projects.png','05-schedule.png','06-detail.png','10-desktop-dark.png','10-overview-390.png','10-detail-390.png','10-overview-900.png'],
'T3':['01-source-compact.png','04-expanded.png','08-error.png','09-sheet-390.png','09-sheet-900.png','09-reduced-expanded.png','06-drag-short.png','01-desktop-initial.png']}
manifest=[]
for row in mapping:
 rid,aid,task=row['run_id'],row['anonymous_id'],row['task'];ev=base/'evaluations'/rid
 if not (ev/'results.json').exists():raise SystemExit('Missing completed evaluation: '+rid)
 folder=dest/aid;folder.mkdir(exist_ok=True)
 shutil.copy2(base/'fixtures'/task/'TASK.md',folder/'TASK.md')
 available=[];missing=[]
 for name in selected[task]:
  if (ev/name).exists():shutil.copy2(ev/name,folder/name);available.append(name)
  else:missing.append(name)
 # Missing expected captures may be a real interruption. Preserve the ordinary
 # visible failure frame, without revealing acceptance counts or version labels.
 if missing:
  for p in sorted(ev.glob('failure-*.png')):
   name='interruption-'+p.name.removeprefix('failure-');shutil.copy2(p,folder/name);available.append(name)
 timeline=ev/'temporal/timeline.json';episode=[]
 if timeline.exists():
  tl=json.loads(timeline.read_text());(folder/'episodes').mkdir(exist_ok=True)
  for frame in tl['frames']:
   p=ev/'temporal'/frame['file']
   if p.exists():shutil.copy2(p,folder/'episodes'/p.name);episode.append({k:frame[k] for k in ['file','label','sampleStartedMs','sampleEndedMs']})
  # Raw clip is supplied for a reviewer or person capable of actual playback.
  clip=ev/'temporal'/tl['video']
  if clip.exists():shutil.copy2(clip,folder/'episode.webm')
  (folder/'episodes/timeline.json').write_text(json.dumps({'scope':tl['scope'],'events':tl['events'],'frames':episode},indent=2)+'\n')
 meta={'anonymous_id':aid,'task':task,'images':available,'unavailable_images':missing,'episodes':'episodes/timeline.json','video':'episode.webm','scope':'Standardized rendered evidence; images are not a functional-test result or natural-playback claim.'}
 (folder/'EVIDENCE.json').write_text(json.dumps(meta,indent=2)+'\n');manifest.append(meta)
for reviewer in range(1,4):
 order=manifest[:];random.Random(82026+reviewer).shuffle(order)
 (dest/f'ORDER-{reviewer}.json').write_text(json.dumps([{'anonymous_id':x['anonymous_id'],'task':x['task']} for x in order],indent=2)+'\n')
(dest/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
ref=dest/'T1-reference';ref.mkdir(exist_ok=True)
for src,name in [('perplexica/.assets/vane-screenshot.png','author-current-view.png'),('perplexica/public/screenshots/p1.png','author-historical-empty-view.png'),('perplexica/public/screenshots/p2.png','author-historical-answer-view.png')]:shutil.copy2(base/'references'/src,ref/name)
shutil.copy2(base/'references/IDENTITY.json',ref/'IDENTITY.json')
(dest/'REVIEW-INSTRUCTIONS.md').write_text('''# Independent visual review

Review only this packet. Do not inspect implementation directories, other agents, the maintainer repository, process reports, private campaign files, skill instructions, or version assignments. All outputs are anonymous. Read RUBRIC.json and the common task brief for each family. Follow your assigned ORDER file. Do not browse external material; the common T1 reference is supplied here.

Inspect every output's main desktop, secondary view/detail and narrow view at their recorded scale, both theme conditions where supplied, and representative ordered episodes. The original images are available; overview composites are not a replacement for readable full-size inspection. Each dimension needs an integer0–4 anchored score, exact evidence filenames, visible strengths/defects and a limitation. Do not calculate an overall aesthetic total. Record which files and intervals you actually viewed. Distinguish static and sampled temporal support from actual natural video playback; do not claim playback unless you could actually watch it. No FPS or human-usability conclusion is supported.

Within each task, provide an ordered set of tiers of the four outputs, allowing ties, with comparative reasons. Judge the full intended task and craft relationships; library names, resource quantity and version hypotheses are irrelevant and unavailable. A quiet interface may be excellent; the expressive workspace must visibly meet its editorial/spatial brief throughout populated work. Missing required screenshots should be treated as an evidence limit; an interruption frame is an observed state, not an invitation to guess a failure count.

Finish your independent scores before any discussion. Save JSON using the supplied output schema and a concise review note in your own reviewer directory. Do not repair, run, or alter the applications. Ratings are independent model judgments, not human test results.
''')
print(json.dumps({'outputs':len(manifest),'root':str(dest),'images':sum(len(x['images']) for x in manifest)},indent=2))
