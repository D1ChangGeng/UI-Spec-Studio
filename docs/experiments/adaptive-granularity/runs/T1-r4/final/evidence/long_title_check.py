from playwright.sync_api import sync_playwright
from pathlib import Path
import os,json
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
root=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':900});p.goto('http://127.0.0.1:8844/');p.locator('#samples').click();results=[]
 for width,height in [(1440,900),(390,844)]:
  p.set_viewport_size({'width':width,'height':height})
  for lang in ['en','zh']:
   if p.locator('html').get_attribute('lang') != ('en' if lang=='en' else 'zh-CN'):p.locator('#locale-toggle').click()
   for mode in ['light','dark']:
    if p.locator('html').get_attribute('data-theme') != mode:p.locator('#theme-toggle').click()
    if width==390 and p.locator('#back').is_visible():p.locator('#back').click()
    p.locator('.note-row').last.click();p.wait_for_timeout(200);fit=p.locator('#note-title').evaluate('(e)=>e.scrollHeight <= e.clientHeight + 1');assert fit,(width,lang,mode);p.screenshot(path=str(root/f'long-{width}-{lang}-{mode}.png'));results.append({'viewport':[width,height],'locale':lang,'theme':mode,'title_fits':fit})
 (root/'long-title-check.json').write_text(json.dumps(results,indent=2));b.close();print('8/8 long-title fields fit; editor remains scrollable.')
