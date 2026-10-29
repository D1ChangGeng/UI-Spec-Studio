from playwright.sync_api import sync_playwright
from pathlib import Path
import json
D=Path(__file__).parent/'references'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1100,'height':900},ignore_https_errors=True)
 page.goto('https://3dtransforms.desandro.com/card-flip',timeout=20000)
 (D/'desandro.html').write_text(page.content())
 print(page.locator('.card').count(),page.locator('.card').evaluate_all('(els)=>els.map(e=>({class:e.className,text:e.textContent}))'))
 page.locator('.card').nth(1).scroll_into_view_if_needed();page.screenshot(path=str(D/'center-rest.png'))
 page.locator('.card').nth(1).click()
 for i in range(5):
  page.wait_for_timeout(130);page.screenshot(path=str(D/f'center-{i}.png'))
 page.locator('.card').nth(2).scroll_into_view_if_needed();page.screenshot(path=str(D/'slide-rest.png'))
 page.locator('.card').nth(2).click()
 for i in range(5):
  page.wait_for_timeout(130);page.screenshot(path=str(D/f'slide-{i}.png'))
 b.close()
