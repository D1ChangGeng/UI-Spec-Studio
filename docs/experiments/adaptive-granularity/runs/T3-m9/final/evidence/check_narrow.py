from playwright.sync_api import sync_playwright
import json
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 c=b.new_context(viewport={'width':390,'height':844},color_scheme='dark');g=c.new_page();g.goto('http://127.0.0.1:8939')
 g.locator('#note-text').fill('A first draft that must survive a failed save.')
 g.evaluate('() => {window.setOriginal=Storage.prototype.setItem;Storage.prototype.setItem=()=>{throw Error("injected first-save failure")}}');g.locator('#save').click();g.wait_for_timeout(1100)
 results.append({'check':'first failure never shows saved face','pass':g.locator('#note-card').get_attribute('data-face')=='front' and g.evaluate('localStorage.length')==0 and g.locator('#retry').is_visible()})
 g.screenshot(path='evidence/390-dark-first-failure.png');bounds=g.locator('#retry').bounding_box();results.append({'check':'failure retry in narrow viewport','pass':bounds['y']+bounds['height']<=844})
 g.evaluate('() => {Storage.prototype.setItem=window.setOriginal}');g.locator('#retry').click();g.wait_for_timeout(1800);g.locator('#return').click();g.wait_for_timeout(800)
 text=('A long note keeps its own scroll area.\n'*16)[:600];g.locator('#note-text').fill(text);g.locator('#note-text').evaluate('(e)=>e.scrollTop=e.scrollHeight');g.screenshot(path='evidence/390-dark-long-note.png');results.append({'check':'narrow long note scrolls without hiding save','pass':g.locator('#note-text').evaluate('(e)=>e.scrollHeight>e.clientHeight') and g.locator('#save').bounding_box()['y']+44<844})
 g.locator('#theme-toggle').click();g.locator('#locale-toggle').click();results.append({'check':'theme and language preserve draft','pass':g.locator('#note-text').input_value()==text})
 g.locator('#note-text').press('Control+Enter');g.wait_for_timeout(1800);g.locator('#saved-text').focus();g.locator('#saved-text').press('End');g.screenshot(path='evidence/390-light-zh-long-saved.png')
 results.append({'check':'saved long note exposes internal scroll','pass':g.locator('#saved-text').evaluate('(e)=>e.scrollHeight>e.clientHeight')})
 b.close()
open('evidence/narrow-report.json','w').write(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
