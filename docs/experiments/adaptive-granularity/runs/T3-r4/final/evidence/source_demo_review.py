from playwright.sync_api import sync_playwright
from pathlib import Path
import json
O=Path(__file__).parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 q=b.new_page(viewport={'width':1000,'height':700},ignore_https_errors=True)
 q.goto('https://3dtransforms.desandro.com/card-flip',wait_until='domcontentloaded')
 (O/'source-desandro.html').write_text(q.content())
 entries=[]
 for i in [1,2]:
  card=q.locator('.card').nth(i);card.scroll_into_view_if_needed();q.wait_for_timeout(100)
  q.screenshot(path=str(O/f'source-candidate-{i}-before.png'))
  card.click()
  for j in range(5):
   t=q.evaluate('performance.now()');q.screenshot(path=str(O/f'source-candidate-{i}-{j}.png'));entries.append({'candidate':i,'frame':j,'time':t,'transform':card.evaluate('(e)=>getComputedStyle(e).transform')});q.wait_for_timeout(130)
  q.wait_for_timeout(300);card.click();q.wait_for_timeout(1100)
 (O/'source-episodes.json').write_text(json.dumps(entries,indent=2));b.close()
