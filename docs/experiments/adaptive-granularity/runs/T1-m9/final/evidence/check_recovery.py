from pathlib import Path
from playwright.sync_api import sync_playwright,expect
import json,traceback
OUT=Path(__file__).parent;checks=[]
def run(name,fn):
 try:fn();checks.append({'name':name,'result':'PASS'})
 except Exception as e:checks.append({'name':name,'result':'FAIL','error':str(e),'trace':traceback.format_exc()})
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 c=b.new_context(viewport={'width':390,'height':844});page=c.new_page();page.goto('http://127.0.0.1:8619/');page.locator('.note-row').first.click()
 def draft_failure():
  page.evaluate("() => {window.originalSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==='leafnote-drafts-v2')throw new Error('injected draft failure');return window.originalSet.call(this,k,v)}}")
  page.locator('#note-body').fill('Unsaved draft remains in memory.');expect(page.locator('#notice-text')).to_contain_text('Your draft could not be stored');expect(page.locator('#mobile-save-status')).to_have_text('Unsaved changes');page.screenshot(path=str(OUT/'draft-failure-mobile.png'));page.locator('#back').click();page.locator('.note-row').nth(1).click();page.locator('#back').click();page.locator('.note-row').first.click();expect(page.locator('#note-body')).to_have_value('Unsaved draft remains in memory.');page.evaluate('() => {Storage.prototype.setItem=window.originalSet}');page.locator('#save').click();expect(page.locator('#mobile-save-status')).to_have_text('Saved locally')
 run('Draft-write failure stays visible and retains text through navigation',draft_failure)
 def conflict():
  page.locator('#note-body').fill('My local draft must not be lost.');other=c.new_page();other.goto('http://127.0.0.1:8619/');other.locator('.note-row').first.click();other.locator('#note-body').fill('Other tab saved version.');other.locator('#save').click();expect(page.locator('#notice-text')).to_contain_text('another tab');expect(page.locator('#save')).to_be_disabled();page.locator('#retry').click();expect(page.locator('#note-body')).to_have_value('My local draft must not be lost.');page.screenshot(path=str(OUT/'conflict-recovery-mobile.png'));other.close();page.locator('#save').click();expect(page.locator('#mobile-save-status')).to_have_text('Saved locally')
 run('Cross-tab saved changes block overwrite and reading latest retains local draft',conflict)
 def deletion_failure():
  page.evaluate("() => {window.originalSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==='leafnote-notebook-v2')throw new Error('injected delete failure');return window.originalSet.call(this,k,v)}}")
  page.locator('#delete-note').click();expect(page.get_by_role('button',name='Keep note',exact=True)).to_be_focused();page.locator('#confirm-delete').click();expect(page.locator('#notice-text')).to_contain_text('Could not delete');expect(page.locator('#note-body')).to_have_value('My local draft must not be lost.');page.evaluate('() => {Storage.prototype.setItem=window.originalSet}');page.locator('#retry').click();page.locator('#confirm-delete').click();expect(page.locator('#notice-text')).to_have_text('Note deleted from this browser.');page.reload();assert not any(n['id']=='example-1' for n in json.loads(page.evaluate("localStorage.getItem('leafnote-notebook-v2')"))['notes'])
 run('Deletion failure keeps note, safe initial focus, retry commits deletion',deletion_failure)
 def scroll_long():
  page.locator('#search').fill('different tree cover');page.locator('.note-row').click();page.locator('#note-body').focus();page.keyboard.press('Control+End');page.screenshot(path=str(OUT/'long-content-bottom-mobile.png'));assert page.locator('#note-body').evaluate('e=>e.getBoundingClientRect().bottom')<900
 run('Long note bottom is reachable with keyboard in narrow editor',scroll_long)
 c.close();b.close()
(OUT/'recovery-results.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
