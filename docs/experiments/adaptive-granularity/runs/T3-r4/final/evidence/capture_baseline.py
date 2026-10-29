from playwright.sync_api import sync_playwright
from pathlib import Path
import json,time
out=Path(__file__).parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':900})
 page.goto('http://127.0.0.1:8314');page.screenshot(path=str(out/'before-desktop.png'))
 try:
  page.goto('https://3dtransforms.desandro.com/card-flip',wait_until='domcontentloaded',timeout=20000)
  page.screenshot(path=str(out/'source-desandro.png'),full_page=True)
  print(page.locator('.card').count())
  cards=page.locator('.card')
  if cards.count():
   cards.first.click()
   for i in range(4):
    page.wait_for_timeout(150);page.screenshot(path=str(out/f'source-turn-{i}.png'))
 except Exception as e: print('source demo unavailable',str(e))
 b.close()
