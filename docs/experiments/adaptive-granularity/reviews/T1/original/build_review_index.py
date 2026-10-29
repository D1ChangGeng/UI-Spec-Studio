from pathlib import Path
import json,hashlib,datetime,struct

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'review-output'
main=json.loads((OUT/'run-02/check-results.json').read_text())
supp=json.loads((OUT/'supplemental-results.json').read_text())
final=json.loads((OUT/'final-probe-results.json').read_text())
failure=json.loads((OUT/'failure-preference-results.json').read_text())
viewed=[]
for i in range(1,4):
 name=f'variant-{i:02d}'
 specs=[('captures', 'desktop-comfortable-long', 'final comfortable desktop comparison'),
        ('run-02/captures','desktop-initial','final fresh-start state'),
        ('run-02/captures','desktop-compact-draft','final compact desktop comparison')]
 specs += [('run-02/captures',x,'final narrow comparison') for x in ['mobile-comfortable-long','mobile-compact-long','mobile-comfortable-collection','mobile-compact-collection','mobile-dark-chinese-draft','mobile-delete-cancel']]
 specs += [('supplemental-captures',x,'initial comparison' if x.startswith('initial') else 'supplemental operated state') for x in ['initial-desktop-long','initial-mobile-long','desktop-density-keyboard-focus','mobile-manual-scroll-interior','mobile-dark-chinese-storage-failure']]
 specs += [('final-probe-captures',x,'settled theme or outer scroll') for x in ['mobile-settled-dark-chinese','mobile-outer-scroll']]
 specs += [('failure-preference-captures','failure-then-density','combined failure and preference change')]
 for folder,suffix,purpose in specs:
  p=OUT/folder/f'{name}-{suffix}.png';assert p.exists(),p
  viewed.append({'variant':name,'path':str(p.relative_to(ROOT)),'viewport':list(struct.unpack('>II',p.read_bytes()[16:24])),'purpose':purpose,'inspection':'original PNG pixels viewed with view_image; static frame'})
diagnostic=OUT/'captures/variant-01-original-harness-failure.png'
viewed.append({'variant':'variant-01','path':str(diagnostic.relative_to(ROOT)),'viewport':[1440,900],'purpose':'diagnostic original harness failure','inspection':'original PNG pixels viewed with view_image; static frame'})
captured=[str(p.relative_to(ROOT)) for p in sorted(OUT.rglob('*.png'))]
inventory={'viewed_count':len(viewed),'product_frames_viewed_per_variant':17,'additional_diagnostic_frames':1,'viewed_frames':viewed,'captured_count':len(captured),'all_captured_frames':captured,'captured_not_viewed':[p for p in captured if p not in {v['path'] for v in viewed}],'viewed_continuous_intervals':[],'note':'Operating wheel/keyboard/click actions is evidenced by scripts and states. No continuous playback interval was viewed. Some immediate theme captures are transition frames; settled captures are identified separately.'}
(OUT/'viewed-images.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
observations={
'variant-01':{
 'composition_material':'Cream editor, pale green-gray collection, thin rule separation, filled/edge-marked selection, persistent bottom save/status bar and local/export footer.',
 'type_hierarchy':'Large serif title; final metadata/body labels are stronger than initial. Comfortable/compact body 16/15 px with 30.4/25.5 px line-height. Desktop body measure 645/579 px for this content.',
 'feedback':'Specific save-failure feedback initially appears at the bottom. Density/theme/language failures then replace it with preference-only feedback and hide Retry.',
 'spatial_stability':'Growing body scrolls within fixed editor. English-to-Chinese UI switch changes this bilingual title height 167.19→238.5 px and body top 480.19→551.5 px at 390×844 comfortable.',
 'continuity':'All 28 comparable behavior assertions passed. Draft text and selected note retained during appearance changes. Density works by keyboard, but select focus has no visible outline/shadow.',
 'initial_relationship':'Collection/editor relationship, growing note body, bottom save/status bar already present initially; final adds shared density, reading-scale/label changes and a two-row narrow header.',
 'reproduced_gaps':['G01','G02']},
'variant-02':{
 'composition_material':'Separate project/context field and collection context line; white selected card on muted sidebar with fine border/shadow and green edge; persistent top save/feedback when outer page scrolls.',
 'type_hierarchy':'Serif title with explicit title/context/body labels; continuation enlarges small text and stacks narrow project/context label/value. Body 16/15 px, 30.4/25.5 px leading; desktop measure remains 680 px.',
 'feedback':'Initial write-failure notice and Retry are clear. Appearance preference write failure then replaces note-save warning, removes error styling and hides Retry. Settled dark-theme frame is coherent; an earlier immediate frame was transitional.',
 'spatial_stability':'Bounded body textarea is 405 px high on mobile. Body begins about y=701 comfortable/y=649 compact. Wheel over body moves its internal scroll while title/context remain. Wheel outside field scrolls page; global appearance header then leaves view.',
 'continuity':'All 28 comparable assertions passed, including context-bearing notes, new-draft reload, keyboard density/search/reopen and earlier-content recovery. Density select shows 3 px keyboard focus outline.',
 'initial_relationship':'Separate context field, bounded textarea and page scrolling were already present initially. Continuation changes reading measure, sizes, density and narrow field arrangement.',
 'reproduced_gaps':['G02']},
'variant-03':{
 'composition_material':'Pale collection and tinted editor, filled/edge-marked selection, strong body label, note-type badge, fixed toolbar and compact local/status footer. Fresh state labels five automatic notes as fictional.',
 'type_hierarchy':'Keeps body at 16 px across densities; bilingual content leading 32.8/28.8 px. Desktop reading measure 650/680 px. Larger final labels/metadata than initial.',
 'feedback':'Retains save-error notice and Retry across failing density/theme/language preference writes. Global narrow error banner adds about 74 px above editor and reduces reading space; unsaved status stays in footer.',
 'spatial_stability':'Growing body scrolls inside fixed editor. Tested title/body coordinates unchanged by UI-language switch. Banner insertion causes visible layout movement during failure.',
 'continuity':'All 28 comparable assertions passed. Visible 3 px density keyboard focus. No additional consequential defect reproduced in tested scenarios; this is limited coverage, not a universal pass.',
 'initial_relationship':'Initial already used the collection/editor split, growing document and footer; continuation adds density and changes reading roles, line heights and spacing.',
 'reproduced_gaps':[]}}
current_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('variant-*/*/*') if p.is_file()}
(OUT/'source-integrity.json').write_text(json.dumps({'original_hashes':main['source_hashes_before'],'final_hashes':current_hashes,'unchanged':current_hashes==main['source_hashes_before']},indent=2))
variants={}
for name in observations:
 checks=main['variants'][name]['checks']+supp['variants'][name]['checks']+final['variants'][name]['checks']
 variants[name]={**observations[name],'comparable_assertions_executed':len(checks),'comparable_assertions_passed':sum(c['pass'] for c in checks),'executed_check_set':'common_28','failed_comparable_checks':[c['name'] for c in checks if not c['pass']],'viewed_product_frames':17,'page_errors_in_main_corrected_run':main['variants'][name]['page_errors'],'failure_preference_probe':{'draft_retained':failure['variants'][name]['draft_retained'],'save_failure_retry_before':failure['variants'][name]['retry_before'],'retry_after_density':failure['variants'][name]['retry_after'],'status_after_density':failure['variants'][name]['after_density']}}
summary={
 'packet':'T1','task_family':'notebook','review_started_approx_utc':'2026-10-29T21:46:00Z','review_completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Review only. Three anonymous variants operated from assigned packet with fresh contexts/distinct local origins. No implementation or publication changes.',
 'viewports':[[1440,900],[390,844]],'representative_content':{'collection_notes':4,'title_characters':65,'body_characters':3199,'draft_characters':3235,'body_languages':['English','Chinese'],'full_content_evidence':'review-output/run-02/check-results.json'},
 'source_integrity':{'application_files_hashed':len(current_hashes),'unchanged_since_main_run_start':current_hashes==main['source_hashes_before'],'hash_evidence':'review-output/source-integrity.json'},
 'executed_check_sets':{'common_28':{'names':[c['name'] for c in main['variants']['variant-01']['checks']+supp['variants']['variant-01']['checks']+final['variants']['variant-01']['checks']],'results_by_variant':['review-output/run-02/check-results.json','review-output/supplemental-results.json','review-output/final-probe-results.json']}},
 'variants':variants,
 'consequential_gaps':[
  {'id':'G01','variants':['variant-01'],'kind':'keyboard feedback','finding':'Density select has no visible focus cue while actually focused. Keyboard selection still works.','reproduction':'1440×900, light mode; focus skip link then Tab to density select; inspect outline/shadow and press ArrowDown/Enter.','evidence':['review-output/supplemental-results.json','review-output/supplemental-captures/variant-01-desktop-density-keyboard-focus.png']},
  {'id':'G02','variants':['variant-01','variant-02'],'kind':'failure feedback priority','finding':'Changing density while storage writes fail replaces note-save warning with preference-only message, removes error styling and hides Retry. Text remains. Variant-03 preserves save error/Retry.','reproduction':'390×844, long saved note, English/light/comfortable. Inject setItem QuotaExceededError, edit, Ctrl+S, then select Compact. Also observed after theme/language changes. Restore writes and Ctrl+S to recover.','evidence':['review-output/failure-preference-results.json','review-output/failure-preference-captures/variant-01-failure-then-density.png','review-output/failure-preference-captures/variant-02-failure-then-density.png','review-output/failure-preference-captures/variant-03-failure-then-density.png'],'initial_version_combination_tested':False}
 ],
 'consequential_design_differences':['Variant-02 gives title/project context more space and uses a bounded body scroll region; variants-01/03 scroll the growing document inside a fixed editor.','Variant-01 and variant-02 reduce compact body size to 15 px; variant-03 retains 16 px and adjusts spacing/leading.','Variant-01 UI-language change reflows this bilingual title; tested title/body geometry remains stable in variants-02/03.','Variant-03 inserts a global failure banner, improving persistent error visibility while moving editor content; variants-01/02 use existing status bands.','Variant-03 starts with five explicitly fictional examples; variants-01/02 start empty with example opt-ins.'],
 'harness_failures':[{'run':'original review_checks.py','affected_variants':['variant-01','variant-02','variant-03'],'error':'TypeError: Illegal invocation when restoration expression returned a native Storage function','classification':'test harness, not product','original_evidence_preserved':True,'corrected_run':'review-output/run-02/check-results.json'}],
 'visual_evidence':{'captured_frames':len(captured),'actually_viewed_frames':len(viewed),'viewed_product_frames_per_variant':17,'extra_diagnostic_frames':1,'viewed_intervals':[],'inventory':'review-output/viewed-images.json','transition_caveat':'Immediate dark-theme frame for variant-02 looked transitional; later settled frame and computed colors are coherent. No persistent theme defect or smoothness claim.'},
 'unobserved_dimensions':['Real phones, virtual keyboard, touch gestures, Chinese IME composition, screen readers and zoom','Other engines and unsupported field-sizing fallbacks','Very large collections and near-limit or pathological content','Concurrent-tab conflicts, corrupt/unreadable storage, partial writes, actual quota exhaustion','Comprehensive reading-position continuity across density changes','Generic reload selection of an arbitrary older saved note','Import/restore of downloaded backups','Continuous animation playback, target-device smoothness, human acceptance, statistical significance','Research/process depth or condition mapping'],
 'conclusions_not_claimed':['aesthetic score','universal winner','universal reliability or accessibility pass','human-user acceptance','target-device smoothness','research-depth inference'],
 'deliverables':['review-output/REVIEW.md','review-output/review.json','review-output/viewed-images.json','review-output/commands.md']}
(OUT/'review.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps({'viewed':len(viewed),'captured':len(captured),'per_variant_checks':{k:v['comparable_assertions_executed'] for k,v in variants.items()},'source_files':len(current_hashes),'source_unchanged':summary['source_integrity']['unchanged_since_main_run_start'],'completed':summary['review_completed_utc']},indent=2))
