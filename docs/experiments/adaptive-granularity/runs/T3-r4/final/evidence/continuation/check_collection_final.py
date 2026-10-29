from playwright.sync_api import sync_playwright
from pathlib import Path
import json,hashlib,traceback
O=Path(__file__).parent;K='fieldnote-collection-v2';checks=[];frames=[];errors=[]
def check(n,v,d=None):checks.append({'check':n,'pass':bool(v),'details':d})
def shot(q,n):
 a=q.evaluate('performance.now()');q.screenshot(path=str(O/(n+'.png')),animations='allow');frames.append({'file':n+'.png','start':a,'end':q.evaluate('performance.now()')})
def stored(q):return q.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',K)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 try:
  c=b.new_context(viewport={'width':1440,'height':900});q=c.new_page();q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:8314');shot(q,'empty-desktop')
  check('honest initial empty state',q.locator('#empty-collection').is_visible() and q.locator('.note-tile').count()==0)
  examples=[('How can cities reduce peak heating demand?',('Compare district demand and insulation. Keep each source and its limits beside the claim.\n\n'*8)[:600]),('A walk along the river','Look for places where water, shade and public space meet.'),('What makes a useful research question?','Start with what remains uncertain.\n\nSeparate a question from the answer you hope to find.')]
  ids=[]
  for i,(title,body) in enumerate(examples):
   q.locator('#new-note').click();q.locator('#note-title').fill(title);q.locator('#note-text').fill(body);ids.append(q.locator('#note-card').get_attribute('data-record-id'));q.locator('#save').click();q.wait_for_timeout(1700)
   check('save '+str(i)+' persisted',len(stored(q)['notes'])==i+1);check('save '+str(i)+' nonempty correct back',q.locator('#saved-text').inner_text()==body and q.locator('#question-back').inner_text()==title)
   q.locator('#back-collection').click();check('return '+str(i)+' focuses identity',q.evaluate('document.activeElement.dataset.id')==ids[-1])
  shot(q,'collection-desktop-light');check('three distinct identities',len(set(ids))==3)
  q.reload();check('collection persists after reload',q.locator('.note-tile').count()==3)
  q.locator('.note-tile').nth(0).click();q.locator('#note-text').fill('Updated heating evidence');q.locator('#save').click();q.locator('#back-collection').click();q.locator('.note-tile').nth(1).click();q.wait_for_timeout(1100)
  check('late save does not switch active identity',q.locator('#note-card').get_attribute('data-record-id')==ids[1]);check('late save does not flip another note',q.locator('#note-card').get_attribute('data-face')=='front');check('correct second note draft',q.locator('#note-text').input_value()==examples[1][1])
  q.locator('#flip').click()
  for j in range(6):shot(q,'open-prepared-'+str(j));check('prepared back frame '+str(j),q.locator('#saved-text').inner_text()==examples[1][1]);q.wait_for_timeout(70)
  q.locator('#back-collection').click();q.locator('.note-tile').nth(0).click();q.locator('#note-text').fill('Failed draft remains with the heating card');q.evaluate("()=>{window.nativeSet=Storage.prototype.setItem;Storage.prototype.setItem=function(){throw Error('Injected quota failure')}}");q.locator('#save').click();q.wait_for_timeout(1000)
  check('failure stays editor',q.locator('#note-card').get_attribute('data-face')=='front');check('failure preserves persisted collection',stored(q)['notes'][0]['text']=='Updated heating evidence');q.locator('#back-collection').click();shot(q,'collection-save-failure');check('failed draft identified in collection',q.locator('.note-tile').nth(0).get_attribute('data-failed')=='true')
  q.locator('.note-tile').nth(0).click();check('failed draft recovered by identity',q.locator('#note-text').input_value()=='Failed draft remains with the heating card');q.evaluate('()=>{Storage.prototype.setItem=window.nativeSet}');q.locator('#retry').click();q.wait_for_timeout(1700);check('retry saves correct record',stored(q)['notes'][0]['text']=='Failed draft remains with the heating card');check('retry restores saved reading focus',q.evaluate('document.activeElement.id')=='saved-text')
  q.locator('#back-collection').click();q.locator('#new-note').click();q.locator('#note-title').fill('An unsaved thought');q.locator('#note-text').fill('x'*601);check('long draft retained and blocked',len(q.locator('#note-text').input_value())==601 and q.locator('#save').is_disabled());q.locator('#back-collection').click();check('unsaved note remains visible',q.locator('.note-tile').count()==4);q.locator('.note-tile').nth(3).click();check('unsaved draft restored',q.locator('#note-text').input_value()=='x'*601)
  q.locator('#back-collection').click();q.locator('#theme-toggle').click();shot(q,'collection-desktop-dark');q.reload();check('only confirmed notes survive reload',q.locator('.note-tile').count()==3)
  fixture=stored(q);c.close()
  for theme in ['light','dark']:
   c=b.new_context(viewport={'width':390,'height':844});q=c.new_page();q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:8314');q.evaluate('([k,v])=>localStorage.setItem(k,JSON.stringify(v))',[K,fixture]);q.reload()
   if theme=='dark':q.locator('#theme-toggle').click()
   shot(q,'collection-mobile-'+theme);q.locator('.note-tile').nth(2).scroll_into_view_if_needed();y=q.evaluate('scrollY');q.locator('.note-tile').nth(2).click();check(theme+' prepared title before animation',q.locator('#question-back').inner_text()==examples[2][0]);q.locator('#flip').click();q.wait_for_timeout(120);shot(q,'mobile-'+theme+'-turn');q.locator('#back-collection').click();q.wait_for_timeout(800)
   check(theme+' restored collection scroll',abs(q.evaluate('scrollY')-y)<2,{'before':y,'after':q.evaluate('scrollY')});check(theme+' returned focus not stolen by stale animation',q.evaluate('document.activeElement.dataset.id')==ids[2]);check(theme+' no horizontal overflow',q.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   for i in [0,2,1,0]:q.locator('.note-tile').nth(i).click();check(theme+' rapid open correct '+str(i),q.locator('#question-back').inner_text()==fixture['notes'][i]['title']);q.locator('#back-collection').click()
   q.emulate_media(reduced_motion='reduce');q.locator('.note-tile').nth(1).click();q.locator('#flip').click();q.wait_for_timeout(160);check(theme+' reduced no rotation',q.locator('#note-card').evaluate('(e)=>getComputedStyle(e).transform')=='none');shot(q,'mobile-'+theme+'-reduced-saved');q.locator('#return').click();q.wait_for_timeout(180);check(theme+' reduced keyboard focus',q.evaluate('document.activeElement.id')=='note-text');q.locator('#back-collection').click();q.locator('#locale-toggle').click();shot(q,'collection-mobile-'+theme+'-chinese');c.close()
  c=b.new_context(viewport={'width':1440,'height':900});q=c.new_page();q.goto('http://127.0.0.1:8314');q.evaluate("()=>localStorage.setItem('ui-spec-temporal-note-v1',JSON.stringify({id:'heating-study',title:'Legacy heating note',text:'A previous saved note'}))");q.reload();check('legacy record visible',q.locator('.note-tile').count()==1);q.locator('.note-tile').click();q.locator('#save').click();q.wait_for_timeout(1000);check('legacy migrates on successful save',stored(q)['notes'][0]['id']=='heating-study');c.close()
  c=b.new_context(viewport={'width':390,'height':844});q=c.new_page();q.goto('http://127.0.0.1:8314');q.evaluate('(k)=>localStorage.setItem(k,"malformed")',K);q.reload();check('unknown collection not called empty',q.locator('#empty-collection').is_hidden());check('unknown collection blocks new writes',q.locator('#new-note').is_disabled());shot(q,'unknown-mobile');q.evaluate('(k)=>localStorage.removeItem(k)',K);q.locator('#collection-retry').click();check('read retry restores empty state',q.locator('#empty-collection').is_visible());check('read retry restores useful focus',q.evaluate('document.activeElement.id')=='new-note');c.close()
 except Exception as e:checks.append({'check':'suite completed','pass':False,'details':traceback.format_exc()});print(traceback.format_exc())
 finally:b.close()
check('no runtime errors',not errors,errors)
(O/'report.json').write_text(json.dumps({'checks':checks,'frames':frames,'errors':errors,'source_hashes':{f:hashlib.sha256((O.parent.parent/'app'/f).read_bytes()).hexdigest() for f in ['index.html','styles.css','app.js']},'conditions':'Chromium 143, DPR1, actual local HTTP. Desktop and mobile light/dark. Collection entries created through visible UI, then reused as layout fixtures.'},indent=2))
print(json.dumps({'passed':sum(x['pass'] for x in checks),'total':len(checks),'failures':[x for x in checks if not x['pass']]},indent=2))
