from playwright.sync_api import sync_playwright
import os,json
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox']);page=b.new_page();page.goto('http://127.0.0.1:8844/');page.locator('#samples').click();page.locator('#theme-toggle').click()
 for s in [':root','.primary','.utility','.note-row.active']:
  print(s,page.locator(s).first.evaluate('(e)=>({color:getComputedStyle(e).color,bg:getComputedStyle(e).backgroundColor,accent:getComputedStyle(e).getPropertyValue("--accent"),ink:getComputedStyle(e).getPropertyValue("--ink"),before:getComputedStyle(e,"::before").backgroundColor,font:getComputedStyle(e).fontFamily})'))
 b.close()
