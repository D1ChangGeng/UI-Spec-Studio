from playwright.sync_api import sync_playwright
from pathlib import Path
import json,hashlib
O=Path(__file__).parent;checks=[];K='fieldnote-collection-v2'
def ck(n,v,d=None):checks.append({'check':n,'pass':bool(v),'details':d})
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 q=b.new_page(viewport={'width':1440,'height':900});q.goto('http://127.0.0.1:8314');ids=[]
 for title in ['First thought','Second thought']:
  q.locator('#new-note').click();q.locator('#note-title').fill(title);q.locator('#note-text').fill(title+' evidence');ids.append(q.locator('#note-card').get_attribute('data-record-id'));q.locator('#back-collection').click()
 before=q.locator('.note-tile').evaluate_all('(es)=>es.map(e=>e.dataset.id)');q.locator('.note-tile').nth(1).click();q.locator('#save').click();q.locator('#back-collection').click();focus=q.evaluate('document.activeElement.dataset.id');q.wait_for_timeout(1200)
 ck('background save preserves focused tile',q.evaluate('document.activeElement.dataset.id')==focus);ck('saving second draft preserves order',q.locator('.note-tile').evaluate_all('(es)=>es.map(e=>e.dataset.id)')==before)
 q.locator('.note-tile').nth(0).click();q.locator('#save').click();q.wait_for_timeout(1700);q.locator('#back-collection').click();q.reload();ck('final saved order survives reload',q.locator('.note-tile').evaluate_all('(es)=>es.map(e=>e.dataset.id)')==before)
 q.locator('.note-tile').nth(0).click();q.locator('#note-text').fill('Snapshot');q.locator('#save').click();q.locator('#note-text').fill('Newer unsaved draft');q.locator('#back-collection').click();q.wait_for_timeout(1100);q.locator('.note-tile').nth(0).click();ck('newer draft survives background save and reopening',q.locator('#note-text').input_value()=='Newer unsaved draft');ck('saved back is submitted snapshot',q.locator('#saved-text').inner_text()=='Snapshot')
 q.locator('#back-collection').click();q.locator('summary').click();q.on('dialog',lambda d:d.accept());q.evaluate("()=>{window.nativeRemove=Storage.prototype.removeItem;Storage.prototype.removeItem=function(){throw Error('Injected remove failure')}}");q.locator('#clear').click();ck('clear failure preserves tiles',q.locator('.note-tile').count()==2);ck('clear failure retry available',q.locator('#collection-retry').is_visible());q.screenshot(path=str(O/'clear-failure.png'));q.evaluate('()=>{Storage.prototype.removeItem=window.nativeRemove}');q.locator('#collection-retry').click();ck('clear recovery reaches honest empty state',q.locator('#empty-collection').is_visible() and q.locator('.note-tile').count()==0)
 q.close();b.close()
(O/'orientation-report.json').write_text(json.dumps({'checks':checks,'hashes':{f:hashlib.sha256((O.parent.parent/'app'/f).read_bytes()).hexdigest() for f in ['index.html','styles.css','app.js']}},indent=2));print(json.dumps(checks,indent=2))
