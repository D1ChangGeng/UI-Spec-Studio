from pathlib import Path
import hashlib, json, time
from PIL import Image, ImageChops

OUT=Path(__file__).resolve().parent
BASE=OUT.parent
main=json.loads((OUT/'observations.json').read_text())
follow=json.loads((OUT/'followup-observations.json').read_text())
keyboard=json.loads((OUT/'keyboard-observations.json').read_text())

individual=[
 'variant-01-desktop/01-long-editor.png','variant-01-mobile/01-long-editor-top.png','variant-01-desktop/10-save-failure.png',
 'variant-01-desktop/04-save-0950ms.png','variant-01-reduced/00-empty.png','variant-01-reduced/01-long-editor-top.png',
 'variant-02-desktop/01-long-editor.png','variant-02-desktop/03-dark-chinese-editor.png',
 'variant-03-desktop/01-long-editor.png','variant-03-desktop/03-dark-chinese-editor.png','variant-03-desktop/09-three-card-collection.png','variant-03-mobile/01-long-editor-top.png',
 'variant-01-reduced-repro-390/01-editor-stable.png','variant-01-reduced-repro-390/02-editor-second-capture.png','variant-01-reduced-repro-390/05-collection-return.png','variant-01-followup/06-read-failure.png'
]
sheets=[]
mobile_labels=['00-empty','01-long-editor-top','03-save-1800ms','04-long-saved-bottom','05-reverse-0850ms','06-collection-top','07-collection-third','08-return-third-orientation','09-dark-chinese-editor','10-dark-saved']
for n in range(1,4):
    r=next(r for r in main['runs'] if r['name']==f'variant-{n:02d}-desktop')
    frames=[s['image'] for s in r['states'] if s['label'].startswith(('04-save-','06-reverse-'))]
    sheets.append({'file':f'variant-{n:02d}-motion-sheet.jpg','view_type':'cropped card/contact-sheet scale','frames':frames,'note':'Sampled forward and reverse intervals; actual_elapsed_ms is in observations.json. Not continuous playback.'})
    for mode in ('mobile','reduced'):
        r=next(r for r in main['runs'] if r['name']==f'variant-{n:02d}-{mode}')
        sheets.append({'file':f'variant-{n:02d}-{mode}-sheet.jpg','view_type':'full viewport at contact-sheet scale','frames':[s['image'] for s in r['states'] if s['label'] in mobile_labels]})
    r=next(r for r in follow['runs'] if r['name']==f'variant-{n:02d}-followup')
    sheets.append({'file':f'variant-{n:02d}-route-sheet.jpg','view_type':'full viewport at contact-sheet scale','frames':[s['image'] for s in r['states'] if s['label'].startswith(('03-open','04-return','05-rapid'))],'note':'Sampled opening, return and rapid-switch intervals; actual_elapsed_ms is in followup-observations.json.'})

for label in ('00-empty','03-dark-chinese-editor','10-save-failure'):
    sheets.append({'file':f'comparison-{label}.jpg','view_type':'full viewport at contact-sheet scale','frames':[f'variant-{n:02d}-desktop/{label}.png' for n in range(1,4)]})
sheets.append({'file':'comparison-09-three-card-collection.jpg','view_type':'full viewport at contact-sheet scale','frames':[f'variant-{n:02d}-desktop/09-three-card-collection.png' for n in (1,2)],'note':'The earlier two-variant version was viewed; variant-03 collection was viewed individually at full size.'})
sheets.append({'file':'initial-final-saved.jpg','view_type':'full viewport at contact-sheet scale','frames':[f'variant-{n:02d}-{stage}/{label}.png' for n in range(1,4) for stage,label in [('initial','01-initial-saved'),('desktop','04-save-1900ms')]]})
for width in (390,1440):
    sheets.append({'file':f'reduced-repro-{width}.jpg','view_type':'full viewport at contact-sheet scale','frames':[f'variant-{n:02d}-reduced-repro-{width}/{label}.png' for n in range(1,4) for label in ('01-editor-stable','03-saved-stable','05-collection-return')]})
for label in ('01-keyboard-failure','02-next-tab'):
    sheets.append({'file':f'keyboard-{label}.jpg','view_type':'full narrow viewport side by side','frames':[f'variant-{n:02d}-keyboard-390/{label}.png' for n in range(1,4)]})
viewed=set(individual)
for s in sheets:viewed.update(s['frames'])
captured=[s['image'] for d in (main,follow,keyboard) for r in d['runs'] for s in r['states']]
manifest={'individual_images':individual,'contact_sheets':sheets,'unique_original_frames_visually_inspected':len(viewed),'captured_original_frames':len(captured),'captured_but_not_visually_inspected':[x for x in captured if x not in viewed],'continuous_video_viewed':False,'note':'Appearance claims come from listed pixels. Behavior checks may rely on JSON states from captures not individually viewed. Contact-sheet views are explicitly distinguished from full-size individual images.'}
(OUT/'viewed-evidence.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

normal=Image.open(OUT/'variant-01-mobile/01-long-editor-top.png').convert('RGB').crop((0,0,390,220))
pixels=[]
for path in ['variant-01-reduced/01-long-editor-top.png','variant-01-reduced-repro-390/01-editor-stable.png','variant-01-reduced-repro-390/02-editor-second-capture.png']:
    im=Image.open(OUT/path).convert('RGB').crop((0,0,390,220))
    pixels.append({'image':path,'region':[0,0,390,220],'reference':'variant-01-mobile/01-long-editor-top.png','pixels_exactly_equal':ImageChops.difference(normal,im).getbbox() is None,'unique_colors':len(im.getcolors(390*220))})
(OUT/'pixel-verification.json').write_text(json.dumps({'suspected_issue':'Missing header/introduction in reduced-motion image comparison','classification':'Rejected as product defect; saved source pixels are identical and fresh stable captures are visible.','checks':pixels},indent=2))

before=json.loads((OUT/'source-hashes-before.json').read_text())
after={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for n in range(1,4) for stage in ('initial','final') for p in sorted((BASE/f'variant-{n:02d}'/stage).glob('*')) if p.is_file()}
(OUT/'source-hashes-final.json').write_text(json.dumps(after,indent=2))

checks=[
 {'id':'empty_and_create','result':'All variants showed honest empty collections and created test notes through UI.'},
 {'id':'long_short_limit','result':'479-character mixed note, 52-character English note and 27-character Chinese note were saved/reopened; 779-character input retained with Save disabled.'},
 {'id':'appearance','result':'Draft text preserved through light/dark and English/Chinese UI changes.'},
 {'id':'save_and_reverse','result':'Fixed card-space bounds; saved content populated; tested text selection and inner scroll restored.'},
 {'id':'rapid_actions','result':'Three Ctrl+Enter requests did not duplicate record; rapid flip and route switching ended at requested card/content.'},
 {'id':'editing_pending','result':'Submitted version stored while newer input remained a front-face draft with explicit feedback.'},
 {'id':'collection_orientation','result':'Three cards retained separate identity, drafts, current-tile focus, and narrow return scroll.'},
 {'id':'write_failure_retry','result':'Injected first-save/update Storage exceptions retained draft and prior storage; recovery through retry succeeded.'},
 {'id':'read_failure_retry','result':'Injected read error blocked creation and exposed retry; retry recovered all three records.'},
 {'id':'reload','result':'Saved revision reopened after reload.'},
 {'id':'keyboard','result':'Save shortcut, selected-range restoration, tile Enter activation, Tab samples and failed-save focused activation executed at both viewports.'},
 {'id':'reduced_motion','result':'No 3D rotation in the tested reduced contexts; correct faces, save/reverse/collection return and sampled Tab path at both sizes.'},
 {'id':'clear_control','result':'01 confirmation dismissed with three records intact; 02 immediate clear-all left zero; 03 immediate current-note clear left two.'},
 {'id':'initial_comparison','result':'Initial editor and saved face captured at desktop; initial saved endpoints visually compared with final.'}
]
variants=[
 {'variant':'variant-01','composition':'Persistent intro plus right-hand two-column collection; independent title and body excerpt. Desktop card 714×474; narrow 354×456.','type_material':'Serif heading/read face, sans-serif body editor; pale badge, rounded paper, broad static footprint/shadow. Desktop textarea client height 130 px.','motion':'Stable-axis front/back turn; prepared editor fades in on collection opening; immediate collection return in samples.','continuity':'Draft/storage/focus-range/scroll retained; failed keyboard Save keeps Save focused; read retry transfers focus to New note.','consequential_differences':['Independent editable title gives explicit note identity.','Two-column collection beside intro uses a second row for three cards.','Collection opening fades rather than travelling from tile position.','Clear-all has a dismissible native confirmation.'],'reproduced_gaps':[],'narrow_return_scroll_px':119,'evidence':['variant-01-motion-sheet.jpg','variant-01-route-sheet.jpg','variant-01-mobile-sheet.jpg','variant-01-desktop/10-save-failure.png']},
 {'variant':'variant-02','composition':'Full-width three-column collection with first-line title, count and status; fixed research context beside editor. Desktop card 662×462; narrow 350×364.','type_material':'Serif editor/read content; larger boxed editor, circular mark, rounded card and diffuse lower shadow. Desktop textarea client height 222 px.','motion':'Selected preview enlarges into editor and saved card shrinks back; old preview content remains visible during intermediate opening samples.','continuity':'Data and tested range/scroll retained; failed keyboard Save and successful collection read retry leave BODY focused.','consequential_differences':['First-line/count tiles expose less body context than excerpts.','Spatial collection path maintains selected slot orientation.','Retained research question places narrow editor lower on page.','Clear-all immediately removes all notes without confirmation.'],'reproduced_gaps':[{'id':'failure_focus_loss','severity_description':'Limited keyboard continuity gap; retry remains reachable.','reproduction':'Fresh note with 52-character archive text; make Storage.setItem throw QuotaExceededError; focus Save; press Enter; wait 1200 ms.','viewports':[[1440,900],[390,844]],'observed':'Focus becomes BODY; next Tab reaches retry. Draft remains; no success turn.','evidence':'keyboard-observations.json: variant-02-keyboard-1440 and variant-02-keyboard-390'}],'narrow_return_scroll_px':178,'evidence':['variant-02-motion-sheet.jpg','variant-02-route-sheet.jpg','variant-02-mobile-sheet.jpg','keyboard-01-keyboard-failure.jpg']},
 {'variant':'variant-03','composition':'Full-width three-column collection with large body excerpts and explicit count/local-draft boundary; fixed research context beside narrower editor. Desktop card 570×466; narrow 350×390.','type_material':'Serif text with fine editor rules, restrained corners, star/check motif, lower cast shadow, saved timestamp and shortcut hint. Desktop textarea client height 205 px.','motion':'Prepared destination editor scales from source tile region; collection tile scales down on return. Text/control shapes visibly scale during the sampled morph.','continuity':'Data and tested range/scroll retained; failed keyboard Save and successful collection read retry leave BODY focused.','consequential_differences':['Larger body excerpts aid content recognition but clamp long notes and collapse line breaks.','Prepared destination content is visible from early spatial-transition samples.','Failure retry sits at lower narrow viewport edge.','Clear control immediately removes only current note, without confirmation.'],'reproduced_gaps':[{'id':'failure_focus_loss','severity_description':'Limited keyboard continuity gap; retry remains reachable.','reproduction':'Fresh note with 52-character archive text; make Storage.setItem throw QuotaExceededError; focus Save; press Enter; wait 1200 ms.','viewports':[[1440,900],[390,844]],'observed':'Focus becomes BODY; Tab reaches All notes and then retry. Draft remains; no success turn.','evidence':'keyboard-observations.json: variant-03-keyboard-1440 and variant-03-keyboard-390'}],'narrow_return_scroll_px':315,'evidence':['variant-03-motion-sheet.jpg','variant-03-route-sheet.jpg','variant-03-mobile-sheet.jpg','keyboard-01-keyboard-failure.jpg']}
]
summary={
 'packet':'T3','family':'card_collection','review_started_utc':'2026-10-29T21:47:00Z','report_generated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
 'scope':'Anonymous independent product-output review only; no implementation or publication.',
 'source_unchanged':before==after,'tested_viewports':[[1440,900],[390,844]],'attention':'Same main scenarios, focused follow-up, reduced-motion checks at both sizes, and keyboard failure probes for all three variants.',
 'capture_count':len(captured),'unique_original_frames_visually_inspected':len(viewed),'viewed_evidence_manifest':'viewed-evidence.json',
 'overall':'All variants completed tested local note tasks with preserved drafts, saved data, retry and collection identity. Differences concern composition, preview content, spatial transition and focus/cancellation behavior; no universal ranking inferred.',
 'executed_checks':checks,'variants':variants,
 'behavior_records':['observations.json','followup-observations.json','keyboard-observations.json'],
 'tooling_failures':[{'file':'make-sheets-original-failure.txt','description':'Test virtualenv lacked Pillow for contact-sheet construction; used available environment Python/Pillow after retaining failure. No app source repair.'}],
 'rejected_suspicions':[{'description':'Reduced-mode header disappearance was not in saved pixels; header crops exactly match normal capture and stable fresh-context screenshots show it.','evidence':'pixel-verification.json'}],
 'unobserved_dimensions':['Physical target-device smoothness and continuous playback','Touch and software-keyboard viewport resizing','Screen-reader announcements and exhaustive focus traversal','Formal contrast and translation audits','Firefox/Safari','Large collections beyond three cards','Simultaneous tabs and external storage mutation','Genuine quota/full-disk exhaustion instead of injected exceptions','Every frame between temporal samples','Live reduced-preference change during an active turn','Full initial-version regression and initial narrow views','Research depth and implementation process'],
 'motion_evidence_limit':'Only sampled frames viewed. Capture timings include overhead; actual elapsed times retained. No target-device smoothness claim.',
 'outputs':['REVIEW.md','review.json','viewed-evidence.json','source-hashes-before.json','source-hashes-after.json','source-hashes-final.json']
}
(OUT/'review.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
missing=[x for x in set(captured+individual+[s['file'] for s in sheets]) if not (OUT/x).exists()]
errors=[{'run':r['name'],'errors':r['errors']} for d in (main,follow,keyboard) for r in d['runs'] if r['errors']]
print(json.dumps({'source_unchanged':before==after,'capture_count':len(captured),'visually_inspected_original_count':len(viewed),'missing_evidence':missing,'scenario_errors':errors},indent=2))
