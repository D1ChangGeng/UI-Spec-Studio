from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time
out=Path(__file__).parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':900},ignore_https_errors=True)
 try:
  page.goto('https://www.assistant-ui.com/examples/chatgpt',wait_until='domcontentloaded',timeout=20000)
  page.wait_for_timeout(1400)
  page.screenshot(path=str(out/'assistant-ui-original-retry.png'))
  (out/'original-retry.json').write_text(json.dumps({'url':page.url,'title':page.title(),'time':time.time(),'condition':'Public page; test-browser HTTPS certificate verification disabled after environment certificate failure. No input submitted.'},indent=2))
 except Exception as e:
  (out/'original-retry.json').write_text(json.dumps({'failure':str(e)},indent=2))
 b.close()
