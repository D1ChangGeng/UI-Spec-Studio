from playwright.sync_api import sync_playwright
import json,time
from pathlib import Path
out=Path(__file__).parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
 page.goto('http://127.0.0.1:8767/reference-project/')
 page.screenshot(path=str(out/'reference-conversation.png'))
 page.locator('[name=model][value=documents]').check()
 page.screenshot(path=str(out/'reference-documents.png'))
 page.locator('[name=model][value=conversation]').check()
 page.locator('#question').fill('How can urban trees cool a neighborhood?')
 page.locator('#send').click()
 page.wait_for_timeout(400)
 page.screenshot(path=str(out/'reference-active.png'))
 try:
  page.goto('https://www.assistant-ui.com/examples/chatgpt',wait_until='domcontentloaded',timeout=25000)
  page.wait_for_timeout(1200)
  page.screenshot(path=str(out/'assistant-ui-original.png'))
  (out/'research-browser.json').write_text(json.dumps({'local_reference':'rendered conversation, documents, active','external_url':page.url,'external_title':page.title(),'date':time.time()},indent=2))
 except Exception as e:
  (out/'research-browser.json').write_text(json.dumps({'external_failure':str(e),'local_reference':'rendered conversation, documents, active'},indent=2))
 b.close()
