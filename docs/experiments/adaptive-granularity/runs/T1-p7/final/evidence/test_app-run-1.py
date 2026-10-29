import asyncio, json, os, traceback, sys, time
from pathlib import Path
from playwright.async_api import async_playwright
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
RUN=sys.argv[1] if len(sys.argv)>1 else 'run-1'
OUT=Path('evidence')/RUN;OUT.mkdir(exist_ok=True)
results=[]
def check(name,value):
 results.append({'check':name,'pass':bool(value)})
 if not value:raise AssertionError(name)
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  context=await browser.new_context(viewport={'width':1440,'height':900},device_scale_factor=1)
  page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('dialog',lambda d:d.accept())
  await page.goto('http://localhost:8777/?test');await page.wait_for_timeout(100)
  check('empty collection',await page.locator('.note-card').count()==0)
  await page.locator('#locale-toggle').click();await page.locator('#examples').click()
  check('three labeled synthetic notes',await page.locator('.note-card').count()==3)
  await page.screenshot(path=str(OUT/'desktop-en-light.png'))
  # Draft retains with note switching and reload
  await page.locator('#note-body').fill('New observation retained as a draft.\nSecond line.')
  await page.locator('.note-card').nth(1).click();await page.locator('.note-card').nth(0).click()
  check('draft retained across selection','New observation' in await page.locator('#note-body').input_value())
  await page.reload();check('draft retained across reload','New observation' in await page.locator('#note-body').input_value())
  await page.locator('#save').click();await page.wait_for_timeout(250)
  check('draft becomes saved',await page.locator('#state-message').inner_text()=='Saved in this browser.')
  # Create, save, search context and body, reopen
  await page.locator('#new-note').click();await page.locator('#note-title').fill('A new research lead');await page.locator('#note-context').fill('Water systems');await page.locator('#note-body').fill('Compare drainage observations near the old station.')
  await page.keyboard.press('Control+s');await page.wait_for_timeout(250)
  check('four saved records',await page.evaluate("JSON.parse(localStorage.getItem('leafnote-notes-v2')).notes.length")==4)
  await page.locator('#search').fill('drainage');check('body search',await page.locator('.note-card').count()==1)
  await page.locator('.note-card').click();check('reopen selected title',await page.locator('#note-title').input_value()=='A new research lead')
  await page.locator('#search').fill('not-found');check('no results state',await page.locator('#empty-title').inner_text()=='No matching notes')
  await page.locator('#clear-search').click()
  # Named deletion: keyboard cancel, then failed write, then confirm
  await page.locator('#delete').click();check('delete names note',await page.locator('#delete-name').inner_text()=='A new research lead');check('safe initial focus',await page.evaluate("document.activeElement.id")=='cancel-delete')
  await page.screenshot(path=str(OUT/'delete-confirmation.png'));await page.keyboard.press('Escape')
  check('escape preserves note',await page.locator('.note-card').count()==4)
  await page.locator('#simulate-failure').check();await page.locator('#delete').click();await page.locator('#confirm-delete').click();check('failed delete retains data',await page.locator('.note-card').count()==4 and await page.locator('#delete-error').is_visible())
  await page.locator('#cancel-delete').click();await page.locator('#simulate-failure').uncheck();await page.locator('#delete').click();await page.locator('#confirm-delete').click();check('confirmed delete',await page.locator('.note-card').count()==3)
  # Failure and later retry, preserve input and saved copy
  before=await page.evaluate("localStorage.getItem('leafnote-notes-v2')")
  await page.locator('#note-body').fill('Unsaved due to failure');await page.locator('#simulate-failure').check();await page.locator('#save').click();await page.wait_for_timeout(250)
  check('failed save retains original',await page.evaluate("localStorage.getItem('leafnote-notes-v2')")==before)
  check('failed save meaningful feedback','Could not save' in await page.locator('#state-message').inner_text())
  await page.screenshot(path=str(OUT/'save-failure.png'));await page.locator('#simulate-failure').uncheck();await page.locator('#retry').click();await page.wait_for_timeout(250)
  check('save retry succeeds',await page.locator('#state-message').inner_text()=='Saved in this browser.')
  # Delayed save captures submitted snapshot and retains later typing
  await page.locator('#simulate-slow').check();await page.locator('#note-body').fill('Submitted snapshot');await page.locator('#save').click();await page.locator('#note-body').fill('Newer draft while saving');await page.wait_for_timeout(1150)
  check('save snapshot stable',await page.evaluate("JSON.parse(localStorage.getItem('leafnote-notes-v2')).notes[0].body")=='Submitted snapshot')
  check('newer draft preserved',await page.locator('#note-body').input_value()=='Newer draft while saving' and 'previous version' in await page.locator('#state-message').inner_text())
  await page.locator('#simulate-slow').uncheck();await page.locator('#save').click();await page.wait_for_timeout(250)
  # Export and download JSON
  async with page.expect_download() as dl:await page.locator('#export').click()
  download=await dl.value;await download.save_as(str(OUT/'export-backup.json'));check('backup includes raw legacy key','ui-spec-content-note-v1' in (OUT/'export-backup.json').read_text())
  # Variant screenshots with long Chinese note, plus mobile list/editor
  await page.locator('.note-card').filter(has_text='从单栋建筑').click()
  for locale in ['en','zh']:
   if await page.locator('html').get_attribute('lang')!=('en' if locale=='en' else 'zh-CN'):await page.locator('#locale-toggle').click()
   for theme in ['light','dark']:
    if await page.locator('html').get_attribute('data-theme')!=theme:await page.locator('#theme-toggle').click()
    for width,height in [(1440,900),(390,844)]:
     await page.set_viewport_size({'width':width,'height':height});await page.evaluate('window.scrollTo(0,0)')
     check(f'no overflow {width} {locale} {theme}',await page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
     await page.screenshot(path=str(OUT/f'{width}-{locale}-{theme}-editor.png'))
     if width==390:
      await page.locator('#back').click();await page.screenshot(path=str(OUT/f'{width}-{locale}-{theme}-list.png'));await page.locator('.note-card').filter(has_text='从单栋建筑').click()
  check('no browser errors',not errors)
  await context.close()
  # Legacy migration and malformed collection use fresh real browser storage
  ctx=await browser.new_context(viewport={'width':1440,'height':900});pg=await ctx.new_page();pg.on('dialog',lambda d:d.accept())
  await pg.goto('http://localhost:8777/');await pg.evaluate("localStorage.clear();localStorage.setItem('ui-spec-content-note-v1',JSON.stringify({title:'Recovered legacy note',body:'Original preserved text'}))");await pg.reload()
  check('legacy content recovered',await pg.locator('#note-title').input_value()=='Recovered legacy note')
  await pg.locator('#save').click();await pg.wait_for_timeout(250);check('legacy original retained',await pg.evaluate("JSON.parse(localStorage.getItem('ui-spec-content-note-v1')).body")=='Original preserved text')
  await pg.evaluate("localStorage.setItem('leafnote-notes-v2','{broken')");await pg.reload();check('malformed data blocks overwrite',await pg.locator('#save').is_disabled());await pg.locator('#note-body').fill('Recovery draft');check('malformed original retained',await pg.evaluate("localStorage.getItem('leafnote-notes-v2')")=='{broken');await pg.screenshot(path=str(OUT/'malformed-data.png'))
  # Native storage error, and retry
  await pg.evaluate("localStorage.clear()");await pg.reload();await pg.evaluate("window.originalSet=Storage.prototype.setItem;Storage.prototype.setItem=function(){throw new DOMException('Quota exceeded','QuotaExceededError')}");await pg.locator('#note-title').fill('Quota recovery');check('native draft failure feedback','无法写入' in await pg.locator('#state-message').inner_text());await pg.locator('#save').click();await pg.wait_for_timeout(250);check('native write failure','保存失败' in await pg.locator('#state-message').inner_text());await pg.evaluate('Storage.prototype.setItem=window.originalSet');await pg.locator('#retry').click();await pg.wait_for_timeout(250);check('native write recovery',await pg.evaluate("JSON.parse(localStorage.getItem('leafnote-notes-v2')).notes[0].title")=='Quota recovery')
  await ctx.close();await browser.close()
try:asyncio.run(main())
except Exception as e:results.append({'exception':str(e),'traceback':traceback.format_exc()})
finally:
 (OUT/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
 if any(r.get('pass')==False or 'exception' in r for r in results):sys.exit(1)
