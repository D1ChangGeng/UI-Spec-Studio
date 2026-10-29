import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
out=Path('evidence/final');out.mkdir(exist_ok=True);log=[]
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  ctx=await b.new_context(viewport={'width':1440,'height':900});page=await ctx.new_page();page.on('dialog',lambda d:d.accept());await page.goto('http://localhost:8777');await page.locator('#locale-toggle').click();await page.wait_for_timeout(350);await page.screenshot(path=str(out/'empty-desktop.png'));await page.locator('#examples').click()
  for loc in ['en','zh']:
   if await page.locator('html').get_attribute('lang')!=('en' if loc=='en' else 'zh-CN'):await page.locator('#locale-toggle').click()
   for theme in ['light','dark']:
    if await page.locator('html').get_attribute('data-theme')!=theme:await page.locator('#theme-toggle').click()
    for width,height in [(1440,900),(390,844)]:
     await page.set_viewport_size({'width':width,'height':height});await page.evaluate('window.scrollTo(0,0)');await page.wait_for_timeout(400)
     await page.screenshot(path=str(out/f'{width}-{loc}-{theme}-editor.png'))
     if width==390:
      await page.locator('#back').click();await page.wait_for_timeout(300);await page.screenshot(path=str(out/f'{width}-{loc}-{theme}-list.png'));await page.locator('.note-card').nth(0).click();await page.locator('#note-body').focus();await page.evaluate('window.scrollTo(0,0)')
  await page.locator('.note-card').count()
  # Narrow long-title / body evidence plus delete and lower reading point.
  await page.locator('#back').click();await page.locator('.note-card').nth(1).click();await page.locator('#note-body').focus();await page.evaluate('window.scrollTo(0,0)');await page.wait_for_timeout(350);await page.screenshot(path=str(out/'mobile-long-chinese.png'))
  await page.locator('#note-body').evaluate('(el)=>el.scrollTop=el.scrollHeight');await page.evaluate('window.scrollTo(0,document.body.scrollHeight)');await page.screenshot(path=str(out/'mobile-long-bottom.png'))
  await page.locator('#delete').click();await page.wait_for_timeout(350);await page.screenshot(path=str(out/'mobile-delete.png'));await page.keyboard.press('Escape')
  log.append({'check':'mobile modal cancellation returns focus','pass':await page.evaluate('document.activeElement.id')=='delete'})
  await page.set_viewport_size({'width':1440,'height':900});await page.locator('#new-note').click();await page.locator('#note-title').fill('Concurrent draft kept')
  pg2=await ctx.new_page();await pg2.goto('http://localhost:8777');await pg2.evaluate("localStorage.setItem('leafnote-notes-v2',JSON.stringify({version:2,notes:JSON.parse(localStorage.getItem('leafnote-notes-v2')).notes.map(n=>({...n,context:'Updated in another tab'}))}))")
  await page.wait_for_timeout(100);log.append({'check':'other-tab change disables stale save','pass':await page.locator('#save').is_disabled()});await page.locator('#retry').click();log.append({'check':'other-tab recovery keeps current draft','pass':await page.locator('#note-title').input_value()=='Concurrent draft kept' and not await page.locator('#save').is_disabled()})
  # Actual getItem fault and recovery, separate context.
  ctx2=await b.new_context();pg=await ctx2.new_page();await pg.add_init_script("window.originalGet=Storage.prototype.getItem;Storage.prototype.getItem=function(){throw new DOMException('Access blocked','SecurityError')};")
  await pg.goto('http://localhost:8777');log.append({'check':'read error blocks saves','pass':await pg.locator('#save').is_disabled()});await pg.locator('#note-title').fill('Read recovery draft');await pg.evaluate('() => {Storage.prototype.getItem=window.originalGet;}');await pg.locator('#retry').click();log.append({'check':'read retry preserves draft','pass':await pg.locator('#note-title').input_value()=='Read recovery draft' and not await pg.locator('#save').is_disabled()})
  await ctx2.close();await ctx.close();await b.close()
try:asyncio.run(main())
except Exception as e:log.append({'exception':str(e)})
(out/'checks.json').write_text(json.dumps(log,indent=2));print(json.dumps(log,indent=2))
