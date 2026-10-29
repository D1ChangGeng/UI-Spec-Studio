from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time
BASE=Path(__file__).parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':900})
 page.goto('http://127.0.0.1:8737');page.screenshot(path=str(BASE/'original/desktop.png'))
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(BASE/'original/mobile.png'))
 page.set_viewport_size({'width':1100,'height':900})
 try:
  page.goto('https://3dtransforms.desandro.com/card-flip',timeout=20000)
  page.screenshot(path=str(BASE/'references/desandro.png'))
  (BASE/'references/desandro.html').write_text(page.content())
  print('Reference inspected DOM',page.locator('iframe').count())
 except Exception as e: print('Reference acquisition failed',str(e))
 b.close()
