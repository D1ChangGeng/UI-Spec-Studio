from playwright.sync_api import sync_playwright
from pathlib import Path
import json,hashlib
O=Path('evidence/continuation');r={'tests':[],'captures':[],'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('app').glob('*') if p.is_file()}};K='fieldnote-collection-v1'
def ck(n,v):r['tests'].append({'name':n,'pass':bool(v)})
def snap(g,n):
 a=g.evaluate('performance.now()');g.screenshot(path=str(O/(n+'.png')),animations='allow');r['captures'].append({'name':n,'start':a,'end':g.evaluate('performance.now()')})
items=[{'id':f'fixture-{i}','serial':i+1,'title':'Energy / Cities','text':t} for i,t in enumerate(['Check hourly demand alongside outdoor temperature.','Which buildings have the most useful meter data?','Next: compare the weekday and weekend patterns.','Keep sources and open questions together.','A longer working note.\n'*22,'Return to this question after reviewing the evidence.','A final short observation.'])]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 for w,theme in [(1440,'light'),(390,'dark')]:
  c=b.new_context(viewport={'width':w,'height':900 if w==1440 else 844},color_scheme=theme);g=c.new_page();g.goto('http://127.0.0.1:8939');g.evaluate('([k,n])=>localStorage.setItem(k,JSON.stringify(n))',[K,items[:3] if w==1440 else items]);g.reload();snap(g,f'{w}-populated-final')
  tile=g.locator('.note-tile').nth(2 if w==1440 else 5);tile.scroll_into_view_if_needed();g.wait_for_timeout(100);pos=g.evaluate('scrollY');identity=tile.get_attribute('data-note-id');tile.click();g.wait_for_timeout(450);g.locator('#note-text').fill('A draft retained at the same numbered card.');g.locator('#back-collection').click();g.wait_for_timeout(450)
  ck(f'{w} scroll restored',abs(g.evaluate('scrollY')-pos)<2);ck(f'{w} focus returns same id',g.evaluate('document.activeElement.dataset.noteId')==identity);ck(f'{w} counts distinguish draft', '1 drafts' in g.locator('#note-count').inner_text());snap(g,f'{w}-return-orientation')
  g.locator(f'[data-note-id="{identity}"]').click();g.wait_for_timeout(450);g.locator('#save').click();g.wait_for_timeout(890)
  for i in range(5):snap(g,f'{w}-flip-{i}');g.wait_for_timeout(60)
  g.wait_for_timeout(400);g.locator('#back-collection').click();g.wait_for_timeout(450)
  # Platform fallback: disable the API only in this test page.
  g.evaluate('document.startViewTransition=undefined');g.locator('.note-tile').first.click();ck(f'{w} no-API fallback prepares note',g.locator('#note-text').input_value()==items[0]['text']);g.locator('#back-collection').click();ck(f'{w} no-API focus return',g.evaluate('document.activeElement.dataset.noteId')==items[0]['id']);c.close()
 c=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');g=c.new_page();g.goto('http://127.0.0.1:8939');g.locator('#new-note').click();g.locator('#note-text').fill('Static mode keeps the same note.');g.locator('#save').click();g.wait_for_timeout(1100);ck('reduced card has no rotation',g.locator('#note-card').evaluate('(e)=>getComputedStyle(e).transform')=='none');g.locator('#back-collection').click();ck('reduced collection return immediate',g.locator('#collection').is_visible() and g.evaluate('document.activeElement.classList.contains("note-tile")'));g.evaluate('(k)=>localStorage.setItem(k,"broken")',K);g.reload();ck('unreadable count makes no zero claim',g.locator('#note-count').inner_text()=='Collection unavailable');c.close();b.close()
(O/'orientation-report.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
