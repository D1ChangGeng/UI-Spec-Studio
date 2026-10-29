from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time
out=Path('evidence');out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 page=b.new_page(ignore_https_errors=True,viewport={'width':1440,'height':900})
 page.goto('http://127.0.0.1:8939');page.screenshot(path=str(out/'baseline-desktop.png'))
 try:
  page.goto('https://3dtransforms.desandro.com/card-flip',wait_until='domcontentloaded',timeout=25000)
  page.screenshot(path=str(out/'source-desandro-page.png'),full_page=True)
  cards=page.locator('.card');print('source cards',cards.count())
  for i in range(cards.count()):
   cards.nth(i).scroll_into_view_if_needed();page.screenshot(path=str(out/f'source-{i}-before.png'))
   cards.nth(i).click();page.wait_for_timeout(350);page.screenshot(path=str(out/f'source-{i}-during.png'));page.wait_for_timeout(900);page.screenshot(path=str(out/f'source-{i}-after.png'))
 except Exception as e: print('Source observation error:',str(e))
 b.close()
