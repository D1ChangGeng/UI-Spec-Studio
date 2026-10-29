import asyncio,json,os,traceback
from pathlib import Path
from playwright.async_api import async_playwright
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
OUT=Path('evidence/continuation');log=[]
def ck(name,value):
 log.append({'check':name,'pass':bool(value)})
 if not value:raise AssertionError(name)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  c=await b.new_context(viewport={'width':1440,'height':900});page=await c.new_page();page.on('dialog',lambda d:d.accept());errs=[];page.on('pageerror',lambda e:errs.append(str(e)))
  await page.goto('http://localhost:8777');await page.locator('#locale-toggle').click();await page.locator('#examples').click();await page.locator('.note-card').nth(1).click()
  selected=await page.locator('.note-card[aria-current=true]').get_attribute('data-id');original=await page.locator('#note-body').input_value();draft=original+'\n\n待核查：观察者记录与仪器数据是否一致？\nDraft addition — retain this exact sentence.';await page.locator('#note-body').fill(draft)
  comfy=await page.locator('.note-card').nth(1).bounding_box();await page.locator('#density').select_option('compact');await page.locator('#theme-toggle').click();await page.locator('#locale-toggle').click()
  ck('selection survives density/theme/language',await page.locator('.note-card[aria-current=true]').get_attribute('data-id')==selected)
  ck('draft survives all appearance changes',await page.locator('#note-body').input_value()==draft)
  compact=await page.locator('.note-card').nth(1).bounding_box();ck('compact actually reduces card height',compact['height']<comfy['height'])
  await page.reload();ck('density survives reload',await page.locator('html').get_attribute('data-density')=='compact');ck('selection survives reload',await page.locator('.note-card[aria-current=true]').get_attribute('data-id')==selected);ck('draft survives reload',await page.locator('#note-body').input_value()==draft)
  # Every density / locale / theme / required viewport, with long content.
  for density in ['comfortable','compact']:
   await page.locator('#density').select_option(density)
   for loc in ['en','zh']:
    if await page.locator('html').get_attribute('lang')!=('en' if loc=='en' else 'zh-CN'):await page.locator('#locale-toggle').click()
    for theme in ['light','dark']:
     if await page.locator('html').get_attribute('data-theme')!=theme:await page.locator('#theme-toggle').click()
     for width,height in [(1440,900),(390,844)]:
      await page.set_viewport_size({'width':width,'height':height});await page.evaluate('window.scrollTo(0,0)');await page.locator('#note-body').evaluate('(e)=>e.scrollTop=0');await page.wait_for_timeout(350)
      ck(f'no overflow {density} {loc} {theme} {width}',await page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
      ck(f'draft intact {density} {loc} {theme} {width}',await page.locator('#note-body').input_value()==draft)
      await page.screenshot(path=str(OUT/f'{width}-{density}-{loc}-{theme}-editor.png'))
      if width==390:
       await page.locator('#back').click();await page.wait_for_timeout(150);await page.screenshot(path=str(OUT/f'{width}-{density}-{loc}-{theme}-list.png'));await page.locator(f'.note-card[data-id="{selected}"]').click()
  await page.set_viewport_size({'width':1440,'height':900});await page.locator('#locale-toggle').click();await page.locator('#theme-toggle').click()
  for density in ['comfortable','compact']:
   await page.locator('#density').select_option(density);await page.locator('#new-note').click();title='Investigating how shade, street materials, and afternoon wind affect perceived comfort along a neighbourhood walking route';body=('Observation log — compare shaded and open routes before drawing a conclusion.\n\n材料记录：分别记录温度、风速与云量，保持测量条件一致。\n\n'*25)
   await page.locator('#note-title').fill(title);await page.locator('#note-context').fill('Urban climate · Long-form comparison');await page.locator('#note-body').fill(body);await page.keyboard.press('Control+s');await page.wait_for_timeout(250)
   ck(f'create/save long content {density}',await page.evaluate("JSON.parse(localStorage.getItem('leafnote-notes-v2')).notes[0].body")==body)
   await page.locator('#search').fill('Long-form comparison');ck(f'context search {density}',await page.locator('.note-card').count()==1);await page.locator('.note-card').click();ck(f'reopen long content {density}',await page.locator('#note-body').input_value()==body)
   await page.locator('#note-body').evaluate('(e)=>e.scrollTop=0');await page.wait_for_timeout(250);await page.screenshot(path=str(OUT/f'1440-{density}-long-english.png'))
   await page.set_viewport_size({'width':390,'height':844});await page.evaluate('window.scrollTo(0,0)');await page.wait_for_timeout(250);await page.screenshot(path=str(OUT/f'390-{density}-long-english.png'))
   await page.locator('#delete').click();ck(f'named long-note delete {density}',await page.locator('#delete-name').inner_text()==title);await page.keyboard.press('Escape');ck(f'cancel keeps long note {density}',await page.locator('#note-title').input_value()==title);await page.locator('#delete').click();await page.locator('#confirm-delete').click();ck(f'delete removes long note {density}',await page.evaluate("JSON.parse(localStorage.getItem('leafnote-notes-v2')).notes.some(n=>n.title===\""+title+"\")")==False)
   await page.set_viewport_size({'width':1440,'height':900});await page.locator('#search').fill('')
  ck('no runtime page errors',not errs);await b.close()
try:asyncio.run(main())
except Exception as e:log.append({'exception':str(e),'traceback':traceback.format_exc()})
finally:(OUT/'checks.json').write_text(json.dumps(log,indent=2));print(json.dumps(log,indent=2))
