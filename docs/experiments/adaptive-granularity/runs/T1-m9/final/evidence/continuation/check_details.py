from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import json,time
OUT=Path(__file__).parent;results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 c=b.new_context(viewport={'width':390,'height':844});q=c.new_page();q.goto('http://127.0.0.1:8619/');q.evaluate('document.fonts.ready')
 for density in ['comfortable','compact']:
  q.locator('#density').select_option(density);q.screenshot(path=str(OUT/f'collection-390-{density}.png'))
 q.locator('.note-row').nth(3).click();q.locator('#note-body').focus();q.keyboard.press('Control+End');q.screenshot(path=str(OUT/'long-bottom-compact.png'));assert q.locator('#note-body').evaluate('e=>e.getBoundingClientRect().bottom')<844;results.append({'check':'Long compact note remains keyboard-scrollable to the end','result':'PASS'})
 value=q.locator('#note-body').input_value();q.locator('#note-body').fill(value+'\nAn unsaved observation.');selected=q.locator('.note-row[aria-current]').get_attribute('data-id');q.evaluate("() => {window.prefSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==='leafnote-preferences')throw new Error('Injected preference failure');return window.prefSet.call(this,k,v)}}");q.locator('#density').select_option('comfortable');expect(q.locator('#notice-text')).to_contain_text('could not be saved');expect(q.locator('html')).to_have_attribute('data-density','comfortable');expect(q.locator('#note-body')).to_have_value(value+'\nAn unsaved observation.');q.screenshot(path=str(OUT/'preference-failure-mobile.png'));q.evaluate('() => {Storage.prototype.setItem=window.prefSet}');q.locator('#density').select_option('compact');expect(q.locator('#notice')).to_be_hidden();assert json.loads(q.evaluate("localStorage.getItem('leafnote-preferences')"))['density']=='compact';assert q.locator('.note-row[aria-current]').get_attribute('data-id')==selected;results.append({'check':'Preference-write failure explains persistence limit and recovery clears the message without losing draft or selection','result':'PASS'})
 c.close();b.close()
(OUT/'detail-results.json').write_text(json.dumps(results,indent=2));print(results)
