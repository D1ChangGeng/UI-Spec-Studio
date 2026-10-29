from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import json, traceback, time
OUT=Path(__file__).parent
URL='http://127.0.0.1:8619/'
checks=[]
def check(name,fn):
 try:fn();checks.append({'name':name,'result':'PASS'})
 except Exception as e:checks.append({'name':name,'result':'FAIL','error':str(e),'trace':traceback.format_exc()})
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 ctx=b.new_context(viewport={'width':1440,'height':900});page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL);page.evaluate('document.fonts.ready');page.wait_for_timeout(300)
 check('Fresh collection has five fictional examples',lambda:expect(page.locator('.note-row')).to_have_count(5))
 for size in [(1440,900),(390,844)]:
  page.set_viewport_size({'width':size[0],'height':size[1]})
  for lang in ['en','zh']:
   if page.locator('html').get_attribute('lang')!=('en' if lang=='en' else 'zh-CN'):page.locator('#locale-toggle').click()
   for theme in ['light','dark']:
    if page.locator('html').get_attribute('data-theme')!=theme:page.locator('#theme-toggle').click()
    page.wait_for_timeout(200)
    if size[0]<700:
     page.locator('#workspace').evaluate("e=>e.dataset.view='list'");page.screenshot(path=str(OUT/f'collection-{size[0]}-{lang}-{theme}.png'))
     page.locator('.note-row').first.click()
    page.screenshot(path=str(OUT/f'editor-{size[0]}-{lang}-{theme}.png'))
    check(f'No horizontal overflow {size} {lang} {theme}',lambda:assert_no_overflow(page)) if False else None
    overflow=page.evaluate('document.documentElement.scrollWidth > innerWidth')
    checks.append({'name':f'Horizontal reflow {size} {lang} {theme}','result':'FAIL' if overflow else 'PASS'})
 page.set_viewport_size({'width':1440,'height':900})
 if page.locator('html').get_attribute('lang')!='en':page.locator('#locale-toggle').click()
 if page.locator('html').get_attribute('data-theme')!='light':page.locator('#theme-toggle').click()
 def create():
  page.locator('#new-note').click();page.locator('#save').click();expect(page.locator('#title-error')).to_be_visible();page.locator('#note-title').fill('Transit interviews — next steps');page.locator('#note-body').fill('Ask about the last journey, then follow the person’s own words.\n\nDo not assume what mattered.');page.locator('#save').click();expect(page.locator('#save-status')).to_have_text('Saved locally');assert len(json.loads(page.evaluate("localStorage.getItem('leafnote-notebook-v2')"))['notes'])==6
 check('Create, validate, and persist a sixth note',create)
 def draft():
  page.locator('#note-body').fill('A draft survives reload and switching notes.');page.reload();expect(page.locator('#note-body')).to_have_value('A draft survives reload and switching notes.');page.locator('.note-row').nth(1).click();page.locator('#search').fill('draft survives');expect(page.locator('.note-row')).to_have_count(1);page.locator('.note-row').click();expect(page.locator('#note-body')).to_have_value('A draft survives reload and switching notes.');page.locator('#search').fill('')
 check('Draft restoration, note switching, and full-text search',draft)
 def delete_cancel():
  page.locator('#delete-note').click();expect(page.locator('#delete-description')).to_contain_text('Transit interviews');page.screenshot(path=str(OUT/'delete-confirmation.png'));page.get_by_role('button',name='Keep note',exact=True).click();expect(page.locator('#delete-dialog')).not_to_be_visible();expect(page.locator('#note-title')).to_have_value('Transit interviews — next steps');page.locator('#delete-note').click();page.keyboard.press('Escape');expect(page.locator('#delete-dialog')).not_to_be_visible()
 check('Identified delete confirmation, cancel, and Escape',delete_cancel)
 def failure():
  page.evaluate("() => {window.originalSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==='leafnote-notebook-v2')throw new DOMException('Quota full','QuotaExceededError');return window.originalSet.call(this,k,v)}}")
  page.locator('#save').click();expect(page.locator('#notice-text')).to_have_text('Could not save the note. Your current text is still here. Export a copy or try again.');expect(page.locator('#note-body')).to_have_value('A draft survives reload and switching notes.');page.screenshot(path=str(OUT/'storage-failure.png'));page.evaluate('() => {Storage.prototype.setItem=window.originalSet}');page.locator('#retry').click();expect(page.locator('#save-status')).to_have_text('Saved locally')
 check('Injected real Storage write failure and successful retry',failure)
 def pending():
  page.evaluate('window.__leafnoteTestDelay=700');page.locator('#note-body').fill('Submitted snapshot');page.locator('#save').click();page.locator('#note-body').fill('Newer draft during save');expect(page.locator('#notice-text')).to_have_text('The submitted version was saved. Your newer edits remain a draft.');data=json.loads(page.evaluate("localStorage.getItem('leafnote-notebook-v2')"));assert data['notes'][0]['body']=='Submitted snapshot';page.reload();expect(page.locator('#note-body')).to_have_value('Newer draft during save')
 check('Edits during pending save retain newer draft',pending)
 def keyboard():
  page.keyboard.press('Control+k');expect(page.locator('#search')).to_be_focused();page.locator('#search').fill('nothing will match this');expect(page.locator('#empty-search')).to_be_visible();page.screenshot(path=str(OUT/'search-empty.png'));page.locator('#clear-search').click();page.keyboard.press('Control+Shift+n');expect(page.locator('#note-title')).to_be_focused();page.locator('#note-title').fill('Keyboard note');page.keyboard.press('Control+s');expect(page.locator('#save-status')).to_have_text('Saved locally')
 check('Keyboard search, empty recovery, new note, save',keyboard)
 def delete_confirm():
  page.locator('#delete-note').click();page.locator('#confirm-delete').click();expect(page.locator('#notice-text')).to_have_text('Note deleted from this browser.');assert not any(n['title']=='Keyboard note' for n in json.loads(page.evaluate("localStorage.getItem('leafnote-notebook-v2')"))['notes'])
 check('Confirmed deletion persists only after successful write',delete_confirm)
 def export():
  with page.expect_download() as d:page.locator('#export-all').click()
  d.value.save_as(str(OUT/'exported-test-notebook.json'));assert len(json.loads((OUT/'exported-test-notebook.json').read_text())['notes'])==6
 check('Notebook backup download contains persisted collection',export)
 page.locator('#search').fill('different tree cover');page.locator('.note-row').click();page.locator('#search').fill('');page.screenshot(path=str(OUT/'long-content-desktop.png'));page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(OUT/'long-content-mobile.png'))
 for name,seed in [('legacy',"localStorage.setItem('ui-spec-content-note-v1',JSON.stringify({title:'Earlier research',body:'Original preserved'}))"),('malformed',"localStorage.setItem('leafnote-notebook-v2','{broken')")]:
  c=b.new_context(viewport={'width':390,'height':844});q=c.new_page();q.goto(URL);q.evaluate('localStorage.clear()');q.evaluate(seed);q.reload()
  if name=='legacy':
   check('Legacy single note migrates and original stays recoverable',lambda:(expect(q.locator('.note-row')).to_have_count(1),expect(q.locator('#note-title')).to_have_value('Earlier research')))
   assert q.evaluate("localStorage.getItem('ui-spec-content-note-v1')") is not None
  else:
   check('Malformed data blocks destructive writes and remains untouched',lambda:(expect(q.locator('#save')).to_be_disabled(),expect(q.locator('#backup-raw')).to_be_visible()))
   assert q.evaluate("localStorage.getItem('leafnote-notebook-v2')")=='{broken'
   q.locator('#workspace').evaluate("e=>e.dataset.view='editor'");q.screenshot(path=str(OUT/'malformed-recovery-mobile.png'))
  c.close()
 checks.append({'name':'No JavaScript page errors','result':'PASS' if not errors else 'FAIL','errors':errors})
 (OUT/'test-results.json').write_text(json.dumps({'browser':b.version,'checks':checks},indent=2,ensure_ascii=False));print(json.dumps(checks,indent=2,ensure_ascii=False));ctx.close();b.close()
