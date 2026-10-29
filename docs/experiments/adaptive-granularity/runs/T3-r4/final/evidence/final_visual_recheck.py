from playwright.sync_api import sync_playwright
from pathlib import Path
import json,hashlib
O=Path(__file__).parent;checks=[];frames=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 for theme in ['light','dark']:
  c=b.new_context(viewport={'width':390,'height':844});q=c.new_page();q.goto('http://127.0.0.1:8314')
  if theme=='dark':q.locator('#theme-toggle').click()
  q.locator('#save').click();q.wait_for_timeout(900)
  for j in range(5):
   a=q.evaluate('performance.now()');q.screenshot(path=str(O/f'repaired-{theme}-turn-{j}.png'),animations='allow');frames.append({'theme':theme,'frame':j,'start':a,'end':q.evaluate('performance.now()')});q.wait_for_timeout(70)
  q.wait_for_timeout(300);checks.append({'check':theme+' save focus after final turn','pass':q.evaluate('document.activeElement.id')=='saved-text'})
  q.locator('#return').click();q.wait_for_timeout(100);checks.append({'check':theme+' both faces inert during turn','pass':q.locator('#card-front').evaluate('(e)=>e.inert') and q.locator('#card-back').evaluate('(e)=>e.inert')})
  q.emulate_media(reduced_motion='reduce');q.wait_for_timeout(200);checks.append({'check':theme+' changing preference mid turn restores editor','pass':not q.locator('#card-front').evaluate('(e)=>e.inert') and q.evaluate('document.activeElement.id')=='note-text'})
  q.locator('#locale-toggle').click();q.screenshot(path=str(O/f'repaired-{theme}-chinese.png'))
  checks.append({'check':theme+' natural Chinese phrase break','pass':q.locator('#question-front').inner_text()=='城市如何降低\n高峰供热需求？'})
  c.close()
 b.close()
(O/'final-visual-recheck.json').write_text(json.dumps({'checks':checks,'frames':frames,'hashes':{f:hashlib.sha256((O.parent/'app'/f).read_bytes()).hexdigest() for f in ['index.html','styles.css','app.js']}},indent=2))
print(json.dumps(checks,indent=2))
