from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib
D=Path(__file__).parent/'refined';D.mkdir(exist_ok=True);R={'checks':[],'frames':[],'errors':[]}
notes=[{'id':f'n{i}','number':i,'title':f'Note {i}','text':('A short thought.' if i==1 else ('Long evidence with useful context. '*15) if i==2 else 'Another question worth keeping.')} for i in range(1,7)]
def check(n,v):R['checks'].append({'name':n,'pass':bool(v)})
def snap(p,n):a=p.evaluate('performance.now()');p.screenshot(path=str(D/(n+'.png')),animations='allow');R['frames'].append({'file':n+'.png','bracket_ms':[a,p.evaluate('performance.now()')]})
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 for w,theme,motion in [(1440,'light','no-preference'),(390,'dark','no-preference'),(390,'light','reduce')]:
  tag=f'{w}-{theme}-{motion}';ctx=b.new_context(viewport={'width':w,'height':900 if w==1440 else 844},color_scheme=theme,reduced_motion=motion);p=ctx.new_page();p.on('pageerror',lambda e:R['errors'].append(str(e)));p.goto('http://127.0.0.1:8737');p.evaluate('(notes)=>localStorage.setItem("fieldnote-collection-v2",JSON.stringify({version:2,notes}))',notes);p.reload();snap(p,tag+'-collection')
  p.locator('.collection-card').nth(4).scroll_into_view_if_needed();scroll=p.evaluate('scrollY');p.locator('.collection-card').nth(4).click();p.wait_for_timeout(450);check(tag+' correct identity',p.locator('#note-card').get_attribute('data-record-id')=='n5');p.locator('#back-collection').click();p.wait_for_timeout(500);check(tag+' scroll restored',abs(p.evaluate('scrollY')-scroll)<2);check(tag+' same card focused',p.evaluate("document.activeElement.dataset.noteId==='n5'"))
  p.locator('.collection-card').nth(1).click();p.wait_for_timeout(450);actual=p.locator('#saved-text').text_content();R[tag+' prepared-diagnosis']={'textContentLength':len(actual),'innerTextLength':len(p.locator('#saved-text').inner_text()),'expectedLength':len(notes[1]['text'])};check(tag+' hidden content prepared',actual==notes[1]['text']);p.locator('#flip').click();p.wait_for_timeout(750);check(tag+' visible saved face populated',p.locator('#saved-text').inner_text()==notes[1]['text']);snap(p,tag+'-saved');p.locator('#back-collection').click();p.wait_for_timeout(450)
  if motion=='no-preference':
   p.locator('.collection-card').nth(0).click()
   for i in range(5):p.wait_for_timeout(45);snap(p,tag+f'-open-{i}')
   p.locator('#back-collection').click()
   for i in range(5):p.wait_for_timeout(45);snap(p,tag+f'-return-{i}')
   p.locator('.collection-card').nth(0).dispatch_event('click');p.locator('.collection-card').nth(2).dispatch_event('click');p.locator('.collection-card').nth(1).dispatch_event('click');p.wait_for_timeout(600);check(tag+' rapid latest intent',p.locator('#note-card').get_attribute('data-record-id')=='n2' and p.locator('#note-text').input_value()==notes[1]['text']);check(tag+' rapid back prepared',p.locator('#saved-text').text_content()==notes[1]['text'])
  else:
   p.locator('.collection-card').nth(0).click();check('reduced immediate editor focus',p.evaluate("document.activeElement.id==='note-text'"));p.locator('#back-collection').click();check('reduced immediate return focus',p.evaluate("document.activeElement.dataset.noteId==='n1'"));p.locator('#locale-toggle').click();snap(p,'chinese-collection')
  ctx.close()
 b.close()
R['hashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (D.parent.parent.parent/'app').glob('*') if p.is_file()};(D/'report.json').write_text(json.dumps(R,indent=2));print(json.dumps(R,indent=2))
