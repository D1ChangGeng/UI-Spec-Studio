from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time,hashlib,traceback
ROOT=Path(__file__).parent;D=ROOT/'run3';D.mkdir(exist_ok=True); report={'browser':'Chromium headless 143','checks':[],'frames':[],'errors':[]}
def check(name,condition,details=None):
 report['checks'].append({'name':name,'pass':bool(condition),'details':details});(D/'report.json').write_text(json.dumps(report,indent=2))
def snap(page,name):
 t0=page.evaluate('performance.now()');page.screenshot(path=str(D/(name+'.png')),animations='allow');t1=page.evaluate('performance.now()');report['frames'].append({'file':name+'.png','capture_ms':[t0,t1]})
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 report['version']=b.version
 for w,h in [(1440,900),(390,844)]:
  for theme in ['light','dark']:
   tag=f'{w}-{theme}';ctx=b.new_context(viewport={'width':w,'height':h},color_scheme=theme,device_scale_factor=1);page=ctx.new_page();page.on('pageerror',lambda e:report['errors'].append(str(e)))
   page.goto('http://127.0.0.1:8737');page.wait_for_timeout(60);snap(page,tag+'-draft')
   box=page.locator('#card-space').bounding_box();check(tag+' no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   page.locator('#note-text').fill('A useful finding.\n\nCompare district-level demand before drawing a conclusion.');page.locator('#save').click();check(tag+' pending stays front',page.locator('#note-card').get_attribute('data-face')=='front');check(tag+' pending no storage',page.evaluate("localStorage.getItem('ui-spec-temporal-note-v1')===null"))
   if w==1440 and theme=='light':
    snap(page,'save-00-pending');page.wait_for_timeout(490)
    for i in range(6):page.wait_for_timeout(95);snap(page,f'save-{i+1:02}')
   page.wait_for_timeout(1450);snap(page,tag+'-saved');check(tag+' saved back',page.locator('#note-card').get_attribute('data-face')=='back');check(tag+' saved focus',page.evaluate("document.activeElement.id==='saved-title'"));check(tag+' position stable',page.locator('#card-space').bounding_box()==box)
   page.locator('#return').click();page.wait_for_timeout(800);check(tag+' return focus',page.evaluate("document.activeElement.id==='note-text'"));check(tag+' return draft',page.locator('#note-text').input_value().startswith('A useful finding'))
   page.reload();check(tag+' reload persistence',page.locator('#note-text').input_value().startswith('A useful finding'))
   ctx.close()
 ctx=b.new_context(viewport={'width':1440,'height':900});page=ctx.new_page();page.goto('http://127.0.0.1:8737')
 page.locator('#note-text').fill('Snapshot one');page.locator('#save').click();page.locator('#note-text').fill('Newer draft');page.wait_for_timeout(800)
 check('edit while saving keeps front',page.locator('#note-card').get_attribute('data-face')=='front');check('submitted snapshot persisted',page.evaluate("JSON.parse(localStorage.getItem('ui-spec-temporal-note-v1')).text==='Snapshot one'"));check('newer draft retained',page.locator('#note-text').input_value()=='Newer draft')
 page.evaluate("() => {window.originalSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==='ui-spec-temporal-note-v1')throw new DOMException('Injected quota failure','QuotaExceededError');return window.originalSet.call(this,k,v)}}")
 page.locator('#save').click();page.wait_for_timeout(750);snap(page,'failed-save');check('write failure stays front',page.locator('#note-card').get_attribute('data-face')=='front');check('write failure draft retained',page.locator('#note-text').input_value()=='Newer draft');check('write failure storage unchanged',page.evaluate("JSON.parse(localStorage.getItem('ui-spec-temporal-note-v1')).text==='Snapshot one'"));check('write failure retry visible',page.locator('#retry').is_visible())
 page.evaluate('() => {Storage.prototype.setItem=window.originalSet}');page.locator('#retry').click();page.wait_for_timeout(1450);check('retry persists',page.evaluate("JSON.parse(localStorage.getItem('ui-spec-temporal-note-v1')).text==='Newer draft'"))
 page.locator('#flip').click();page.wait_for_timeout(150);snap(page,'reverse-00');page.locator('#flip').click();page.wait_for_timeout(110);snap(page,'reverse-01');page.locator('#flip').click();page.wait_for_timeout(800);snap(page,'reverse-02-settled');check('rapid reversal latest intent',page.locator('#note-card').get_attribute('data-face')=='front');check('rapid reversal inert and focus',page.evaluate("!document.querySelector('#card-front').inert && document.querySelector('#card-back').inert && document.activeElement.id==='note-text'"))
 page.locator('#note-text').fill('Long evidence and open questions. '*22);snap(page,'over-limit');check('long draft retained',len(page.locator('#note-text').input_value())>600);check('over limit disabled',page.locator('#save').is_disabled());check('over limit invalid',page.locator('#note-text').get_attribute('aria-invalid')=='true');page.locator('#note-text').fill(('Evidence, questions, and further observations. '*13)[:590]);page.locator('#note-text').evaluate('(el)=>el.scrollTop=el.scrollHeight');check('long editor scrolls',page.locator('#note-text').evaluate('(el)=>el.scrollTop>0'));page.locator('#save').click();page.wait_for_timeout(1450);page.locator('#saved-text').focus();page.keyboard.press('End');snap(page,'long-saved');check('long saved all content',len(page.locator('#saved-text').inner_text())==len(('Evidence, questions, and further observations. '*13)[:590]))
 page.evaluate("() => {window.originalRemove=Storage.prototype.removeItem;Storage.prototype.removeItem=function(){throw Error('Injected remove failure')}}")
 page.locator('summary').click();page.locator('#clear').click();check('remove failure reported',page.locator('#status-area').get_attribute('data-status')=='clearFailed');page.evaluate('() => {Storage.prototype.removeItem=window.originalRemove}');page.locator('#retry').click();page.wait_for_timeout(850);check('remove retry clears',page.evaluate("localStorage.getItem('ui-spec-temporal-note-v1')===null"));check('clear draft empty',page.locator('#note-text').input_value()=='')
 page.evaluate("localStorage.setItem('ui-spec-temporal-note-v1','malformed')");page.reload();check('malformed data blocks save',page.locator('#save').is_disabled());check('malformed retry visible',page.locator('#retry').is_visible());page.evaluate("localStorage.removeItem('ui-spec-temporal-note-v1')");page.locator('#retry').click();check('read retry restores save',not page.locator('#save').is_disabled());ctx.close()
 for theme in ['light','dark']:
  ctx=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',color_scheme=theme);page=ctx.new_page();page.goto('http://127.0.0.1:8737');page.locator('#save').click();page.wait_for_timeout(750);snap(page,'reduced-'+theme);check('reduced '+theme+' no rotation',page.locator('#note-card').evaluate('(e)=>getComputedStyle(e).transform')=='none');page.locator('#return').click();check('reduced '+theme+' immediate focus',page.evaluate("document.activeElement.id==='note-text'"));page.locator('#locale-toggle').click();snap(page,'chinese-'+theme);check('Chinese '+theme+' no horizontal overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'));ctx.close()
 b.close()
report['source_hashes']={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT.parent/'app').glob('*') if x.is_file()}
(D/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'checks':len(report['checks']),'failed':[c for c in report['checks'] if not c['pass']],'page_errors':report['errors']},indent=2))
