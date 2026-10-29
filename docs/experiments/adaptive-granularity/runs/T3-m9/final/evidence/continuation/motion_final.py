from playwright.sync_api import sync_playwright
from pathlib import Path
import json,hashlib
O=Path('evidence/continuation');r={'captures':[],'checks':[],'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('app').glob('*') if p.is_file()}}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 for w in [1440,390]:
  c=b.new_context(viewport={'width':w,'height':900 if w==1440 else 844});g=c.new_page();g.goto('http://127.0.0.1:8939');g.evaluate('()=>localStorage.setItem("fieldnote-collection-v1",JSON.stringify([{id:"a",serial:1,title:"Question",text:"Keep the evidence and open questions together."},{id:"b",serial:2,title:"Question",text:"A separate second note."}]))');g.reload()
  for direction in ['open','return']:
   if direction=='open':g.locator('.note-tile').first.click()
   else:g.locator('#back-collection').click()
   for i in range(5):
    a=g.evaluate('performance.now()');g.screenshot(path=str(O/f'final-{w}-{direction}-{i}.png'),animations='allow');r['captures'].append({'viewport':w,'direction':direction,'frame':i,'start':a,'end':g.evaluate('performance.now()')});g.wait_for_timeout(40)
   g.wait_for_timeout(400)
  r['checks'].append({'name':f'{w} return identity','pass':g.evaluate('document.activeElement.dataset.noteId')=='a'})
  g.locator('.note-tile').nth(1).click();g.wait_for_timeout(50);g.locator('#all-notes').click();g.wait_for_timeout(50);g.locator('.note-tile').first.click();g.wait_for_timeout(450);r['checks'].append({'name':f'{w} rapid final selection','pass':g.locator('#note-text').input_value()=='Keep the evidence and open questions together.'});c.close()
 b.close()
(O/'motion-final-report.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
