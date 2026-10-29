from playwright.sync_api import sync_playwright
from pathlib import Path
import json,hashlib,traceback
O=Path('evidence/continuation');r={'tests':[],'captures':[],'errors':[],'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('app').glob('*') if p.is_file()}};KEY='fieldnote-collection-v1'
def check(name,val):
 r['tests'].append({'name':name,'pass':bool(val)});(O/'report.json').write_text(json.dumps(r,indent=2))
def snap(g,n):
 a=g.evaluate('performance.now()');g.screenshot(path=str(O/(n+'.png')),animations='allow');r['captures'].append({'file':n,'start':a,'end':g.evaluate('performance.now()'),'viewport':g.viewport_size})
def notes(g):return g.evaluate('(k)=>JSON.parse(localStorage.getItem(k)||"[]")',KEY)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 for width,theme in [(1440,'light'),(390,'dark'),(1440,'dark'),(390,'light')]:
  c=b.new_context(viewport={'width':width,'height':900 if width==1440 else 844},color_scheme=theme);g=c.new_page();g.on('pageerror',lambda e:r['errors'].append(str(e)));g.goto('http://127.0.0.1:8939');prefix=f'{width}-{theme}'
  check(prefix+' honest empty',g.locator('#empty-state').is_visible() and g.locator('.note-tile').count()==0);snap(g,prefix+'-empty')
  for i,text in enumerate(['Compare insulation before changing the heating schedule.','Measure demand in the morning.\n'*18]):
   g.locator('#new-note').click();g.wait_for_timeout(450);g.locator('#note-text').fill(text);g.locator('#note-text').press('Control+Enter');g.wait_for_timeout(1800)
   check(prefix+f' note {i} confirmed',g.locator('#note-card').get_attribute('data-face')=='back' and len(notes(g))==i+1)
   if i==0:snap(g,prefix+'-saved')
   g.locator('#back-collection').click();g.wait_for_timeout(450)
  snap(g,prefix+'-collection');check(prefix+' two cards',g.locator('.note-tile').count()==2);check(prefix+' focus returns to selected card',g.evaluate('document.activeElement.classList.contains("note-tile")'))
  ids=g.locator('.note-tile').evaluate_all('(es)=>es.map(e=>e.dataset.noteId)');g.evaluate('window.firstTile=document.querySelector(".note-tile")');g.locator('.note-tile').first.click();g.wait_for_timeout(450)
  check(prefix+' prepared correct short content',g.locator('#note-text').input_value().startswith('Compare insulation') and g.locator('#note-card').get_attribute('data-record-id')==ids[0])
  g.locator('#note-text').fill('Revised evidence for the first note.');g.locator('#back-collection').click();g.wait_for_timeout(450)
  check(prefix+' draft tile honest and stable',g.locator('.note-tile').first.locator('.tile-state').inner_text()=='Draft · this session' and g.evaluate('window.firstTile===document.querySelector(".note-tile")'))
  g.locator('.note-tile').nth(1).click();g.wait_for_timeout(450);check(prefix+' switching restores long text',g.locator('#note-text').input_value().startswith('Measure demand'))
  g.locator('#back-collection').click();g.wait_for_timeout(450);g.locator('.note-tile').first.click();g.wait_for_timeout(450);check(prefix+' per-note draft retained',g.locator('#note-text').input_value()=='Revised evidence for the first note.')
  g.locator('#save').click();g.locator('#all-notes').click();g.wait_for_timeout(1300);check(prefix+' background save does not leave collection',g.locator('#collection').is_visible() and notes(g)[0]['text']=='Revised evidence for the first note.')
  g.reload();check(prefix+' collection reload persistence',g.locator('.note-tile').count()==2);check(prefix+' no horizontal overflow',g.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  c.close()
 c=b.new_context(viewport={'width':1440,'height':900});g=c.new_page();g.goto('http://127.0.0.1:8939');g.evaluate('(k)=>localStorage.setItem(k,JSON.stringify([{id:"a",serial:1,title:"Q",text:"First short note."},{id:"b",serial:2,title:"Q",text:"Second note, with a separate identity."}]))',KEY);g.reload();g.locator('.note-tile').first.click()
 for i in range(5):snap(g,f'open-{i:02}');g.wait_for_timeout(55)
 g.wait_for_timeout(350);g.locator('#note-text').fill('Unsaved replacement.');old=notes(g);g.evaluate('() => {window.nativeSet=Storage.prototype.setItem;Storage.prototype.setItem=()=>{throw Error("injected write failure")}}');g.locator('#save').click();g.wait_for_timeout(1100);check('failed collection write retains all saved records',notes(g)==old and g.locator('#note-card').get_attribute('data-face')=='front');g.locator('#back-collection').click();g.wait_for_timeout(400);snap(g,'failed-collection');check('collection exposes failed note and draft',g.locator('.note-tile.failed').count()==1 and 'Unsaved replacement' in g.locator('.note-tile').first.inner_text());g.locator('.note-tile').first.click();g.wait_for_timeout(400);check('reopening failed note offers retry',g.locator('#retry').is_visible());g.evaluate('() => {Storage.prototype.setItem=window.nativeSet}');g.locator('#retry').click();g.wait_for_timeout(1800);check('retry updates only selected record',notes(g)[0]['text']=='Unsaved replacement.' and notes(g)[1]['text']==old[1]['text']);g.locator('#back-collection').click()
 for i in range(5):snap(g,f'return-{i:02}');g.wait_for_timeout(55)
 g.wait_for_timeout(400)
 # Rapid actual visible-control navigation, before route animations finish.
 g.locator('.note-tile').first.click();g.wait_for_timeout(50);g.locator('#all-notes').click();g.wait_for_timeout(50);g.locator('.note-tile').nth(1).click();g.wait_for_timeout(450)
 check('rapid opening resolves latest note with prepared faces',g.locator('#note-card').get_attribute('data-record-id')=='b' and g.locator('#note-text').input_value()==old[1]['text'] and g.locator('#saved-text').inner_text()==old[1]['text']);snap(g,'rapid-latest');c.close()
 for reduced in [True,False]:
  c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce' if reduced else 'no-preference');g=c.new_page();g.goto('http://127.0.0.1:8939');g.evaluate('()=>localStorage.setItem("ui-spec-temporal-note-v1",JSON.stringify({id:"heating-study",title:"Old question",text:"A note from the original app."}))');g.reload();check('legacy read '+str(reduced),g.locator('.note-tile').count()==1);g.locator('.note-tile').click();g.wait_for_timeout(450);g.locator('#save').click();g.wait_for_timeout(1800);check('migration keeps identity '+str(reduced),notes(g)[0]['id']=='heating-study');snap(g,'reduced-saved' if reduced else 'migrated-saved');g.locator('#back-collection').click();g.wait_for_timeout(450);check('return focus '+str(reduced),g.evaluate('document.activeElement.dataset.noteId')=='heating-study');snap(g,'reduced-collection' if reduced else 'migrated-collection');c.close()
 c=b.new_context();g=c.new_page();g.goto('http://127.0.0.1:8939');g.evaluate('(k)=>localStorage.setItem(k,"broken")',KEY);g.reload();check('corrupt collection is not an empty state or overwritten',not g.locator('#empty-state').is_visible() and g.locator('#new-note').is_disabled() and g.locator('#collection-retry').is_visible());snap(g,'unreadable-collection');g.evaluate('(k)=>localStorage.setItem(k,"[]")',KEY);g.locator('#collection-retry').click();check('read retry recovers real collection',g.locator('#empty-state').is_visible());c.close();b.close()
(O/'report.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
