from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time,traceback,hashlib
OUT=Path(__file__).parent
KEY='ui-spec-temporal-note-v1'
results=[];events=[]
def check(name,cond,details=None):
 results.append({'check':name,'pass':bool(cond),'details':details})
 if not cond: print('FAIL:',name,details)
def shot(page,name):
 t0=page.evaluate('performance.now()');page.screenshot(path=str(OUT/(name+'.png')),animations='allow');t1=page.evaluate('performance.now()');events.append({'file':name+'.png','capture_start_ms':t0,'capture_end_ms':t1})
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 ctx=b.new_context(viewport={'width':1440,'height':900},record_video_dir=str(OUT/'video'),record_video_size={'width':1440,'height':900})
 page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8314');page.wait_for_timeout(200);shot(page,'after-desktop-light-draft')
 page.locator('#note-text').fill('Compare winter demand across districts.\n\nCheck whether insulation, flexible heat networks, and storage reduce the evening peak. Keep the source and its limits beside every claim.')
 page.locator('#note-text').evaluate('(e)=>{e.focus();e.setSelectionRange(18,24)}')
 box=page.locator('#card-space').bounding_box()
 page.locator('#save').click();shot(page,'save-01-pending')
 check('pending stays front',page.locator('#note-card').get_attribute('data-face')=='front')
 check('pending has no saved record',page.evaluate('(k)=>localStorage.getItem(k)',KEY) is None)
 page.wait_for_timeout(750)
 for i in range(7):
  shot(page,f'save-turn-{i:02}');page.wait_for_timeout(65)
 page.wait_for_timeout(400)
 check('save reaches Storage',json.loads(page.evaluate('(k)=>localStorage.getItem(k)',KEY))['text'].startswith('Compare winter'))
 check('success turns card',page.locator('#note-card').get_attribute('data-face')=='back')
 check('front inert on back',page.locator('#card-front').evaluate('(e)=>e.inert'))
 check('saved focus',page.evaluate('document.activeElement.id')=='saved-text',page.evaluate('document.activeElement.id'))
 check('stable anchor after save',page.locator('#card-space').bounding_box()==box)
 shot(page,'after-desktop-light-saved')
 page.locator('#return').click();page.wait_for_timeout(800)
 check('return focus',page.evaluate('document.activeElement.id')=='note-text',page.evaluate('document.activeElement.id'))
 check('selection restored',page.locator('#note-text').evaluate('(e)=>[e.selectionStart,e.selectionEnd]')==[18,24])
 page.locator('#flip').click();page.wait_for_timeout(120);shot(page,'reverse-01');page.locator('#flip').click();page.wait_for_timeout(70);shot(page,'reverse-02');page.locator('#flip').click();page.wait_for_timeout(90);shot(page,'reverse-03');page.locator('#flip').click();page.wait_for_timeout(800)
 check('rapid reversal latest intent',page.locator('#note-card').get_attribute('data-face')=='front' and not page.locator('#card-front').evaluate('(e)=>e.inert'))
 page.locator('#note-text').fill('Submitted snapshot');page.locator('#save').click();page.locator('#note-text').fill('A newer draft that must remain editable');page.wait_for_timeout(1100)
 check('in-flight draft retained',page.locator('#note-text').input_value()=='A newer draft that must remain editable')
 check('in-flight saved snapshot correct',json.loads(page.evaluate('(k)=>localStorage.getItem(k)',KEY))['text']=='Submitted snapshot')
 check('newer draft stays front',page.locator('#note-card').get_attribute('data-face')=='front')
 page.evaluate("()=>{window.nativeSet=Storage.prototype.setItem;Storage.prototype.setItem=function(){throw new DOMException('Injected write failure','QuotaExceededError')}}")
 page.locator('#save').click();page.wait_for_timeout(1000);shot(page,'failure-desktop')
 check('failure no success flip',page.locator('#note-card').get_attribute('data-face')=='front')
 check('failure old record unchanged',json.loads(page.evaluate('(k)=>localStorage.getItem(k)',KEY))['text']=='Submitted snapshot')
 check('retry available',page.locator('#retry').is_visible())
 page.evaluate('()=>{Storage.prototype.setItem=window.nativeSet}');page.locator('#retry').click();page.wait_for_timeout(1800)
 check('retry native save',json.loads(page.evaluate('(k)=>localStorage.getItem(k)',KEY))['text']=='A newer draft that must remain editable')
 page.reload();check('reload persists',page.locator('#note-text').input_value()=='A newer draft that must remain editable')
 page.locator('#note-text').fill('L'*601);check('over limit retained',len(page.locator('#note-text').input_value())==601);check('over limit blocked',page.locator('#save').is_disabled());shot(page,'long-over-limit')
 page.locator('#note-text').fill(('First, inspect the district demand data. Then compare the source assumptions and limits.\n\n'*8)[:600]);page.locator('#save').click();page.wait_for_timeout(1750)
 check('long text scrolls',page.locator('#saved-text').evaluate('(e)=>e.scrollHeight>e.clientHeight'))
 page.locator('#saved-text').press('End');shot(page,'long-saved-bottom')
 page.locator('#theme-toggle').click();shot(page,'after-desktop-dark-saved');page.locator('#return').click();page.wait_for_timeout(800);shot(page,'after-desktop-dark-draft')
 check('console errors absent',not errors,errors)
 ctx.close()
 # Matrix of both viewport/theme pairs, full task and reduced motion
 for width,height in [(390,844),(1440,900)]:
  for theme in ['light','dark']:
   c=b.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
   q=c.new_page();q.goto('http://127.0.0.1:8314');
   if theme=='dark':q.locator('#theme-toggle').click()
   shot(q,f'matrix-{width}-{theme}-draft')
   check(f'{width} {theme} no horizontal overflow',q.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   q.locator('#save').click();q.wait_for_timeout(1150)
   shot(q,f'matrix-{width}-{theme}-saved-reduced')
   check(f'{width} {theme} reduced no transform',q.locator('#note-card').evaluate('(e)=>getComputedStyle(e).transform')=='none')
   check(f'{width} {theme} reduced same save',q.locator('#note-card').get_attribute('data-face')=='back')
   q.locator('#return').click();q.wait_for_timeout(180)
   check(f'{width} {theme} reduced return focus',q.evaluate('document.activeElement.id')=='note-text')
   if width==390:
    q.locator('#locale-toggle').click();shot(q,f'matrix-{width}-{theme}-chinese');check(f'{theme} Chinese no overflow',q.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   c.close()
 # Unknown record and removal failure recovery
 c=b.new_context(viewport={'width':390,'height':844});q=c.new_page();q.goto('http://127.0.0.1:8314');q.evaluate('(k)=>localStorage.setItem(k,"malformed")',KEY);q.reload()
 check('unreadable blocks save',q.locator('#save').is_disabled());check('unreadable retry available',q.locator('#retry').is_visible())
 q.locator('#saved-link').click();q.wait_for_timeout(800);shot(q,'unreadable-mobile')
 q.locator('#return').click();q.wait_for_timeout(800);check('unreadable return focuses retry',q.evaluate('document.activeElement.id')=='retry')
 q.locator('summary').click();q.evaluate("()=>{window.nativeRemove=Storage.prototype.removeItem;Storage.prototype.removeItem=function(){throw Error('Injected remove failure')}}")
 q.locator('#clear').click();check('clear failure retained record',q.evaluate('(k)=>localStorage.getItem(k)',KEY)=='malformed');q.evaluate('()=>{Storage.prototype.removeItem=window.nativeRemove}');q.locator('#retry').click();check('clear retry works',q.evaluate('(k)=>localStorage.getItem(k)',KEY) is None)
 c.close();b.close()
report={'checks':results,'captures':events,'console_errors':errors,'browser':'Chromium 143 headless shell','DPR':1,'reduced_motion_matrix':'390x844 and 1440x900, light/dark','source_hashes':{f:hashlib.sha256((OUT.parent/'app'/f).read_bytes()).hexdigest() for f in ['index.html','styles.css','app.js']},'limits':'Assertions are behavioral. Screenshots need separate viewing. Video recorded but playback not claimed.'}
(OUT/'test-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'passed':sum(x['pass'] for x in results),'total':len(results),'failures':[x for x in results if not x['pass']]},indent=2))
