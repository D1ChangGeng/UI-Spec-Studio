import asyncio,json,re,traceback
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).parent;OUT=ROOT/'evidence'
APPS={'R7':8661,'T4':8662,'M2':8663}
BROWSER='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell'
async def state(page):
 return await page.evaluate('''()=>({url:location.href,scrollY,body:document.body.innerText,storage:{...localStorage},active:{tag:document.activeElement.tagName,text:document.activeElement.innerText.slice(0,140),aria:document.activeElement.getAttribute('aria-label')}})''')
async def main():
 results={}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=BROWSER,args=['--no-sandbox'])
  for n,port in APPS.items():
   c=await b.new_context(viewport={'width':390,'height':844});page=await c.new_page();r={};results[n]=r
   try:
    await page.goto(f'http://127.0.0.1:{port}',wait_until='networkidle')
    r['card_text_metrics']=await page.locator('a').filter(has_text='The quiet interface').evaluate('''e=>{const c=e.closest('article')||e.parentElement.parentElement; return [...c.querySelectorAll('*')].filter(x=>x.children.length===0&&x.textContent.trim()).map(x=>({tag:x.tagName,text:x.textContent.trim(),size:getComputedStyle(x).fontSize,lineHeight:getComputedStyle(x).lineHeight,color:getComputedStyle(x).color}));}''')
    for i in range(13):
     await page.keyboard.press('Tab')
     a=(await state(page))['active']
     if a['tag']=='BUTTON' and (a['aria'] or '').startswith('Save') and 'The quiet interface' in a['aria']:break
    r['keyboard_save_focus']=await state(page)
    await page.keyboard.press('Space');r['keyboard_saved']=await state(page)
    await page.get_by_role('button',name=re.compile(r'^Saved')).click()
    await page.get_by_role('button',name=re.compile(r'^Unsave.*The quiet interface$')).focus()
    await page.keyboard.press('Space')
    await page.wait_for_timeout(150)
    r['unsaved_in_saved_view']=await state(page)
    await page.screenshot(path=str(OUT/f'{n}-mobile-unsaved-empty.png'))
    await page.reload(wait_until='networkidle');r['unsaved_reloaded']=await state(page)
   except Exception as e:r['failure']={'error':str(e),'traceback':traceback.format_exc(),'state':await state(page)}
   await c.close()
  # Retry selector correction: M2's visible button is 'Try saving again'.
  c=await b.new_context(viewport={'width':390,'height':844});page=await c.new_page()
  await page.goto('http://127.0.0.1:8663',wait_until='networkidle')
  await page.evaluate("() => {window.__reviewOriginalSetItem=Storage.prototype.setItem; Storage.prototype.setItem=function(){throw new DOMException('Review injected storage write failure','QuotaExceededError')};}")
  await page.get_by_role('button',name='Save The quiet interface',exact=True).click()
  results['M2']['corrected_retry_before']=await state(page)
  await page.evaluate('() => {Storage.prototype.setItem=window.__reviewOriginalSetItem;}')
  await page.get_by_role('button',name='Try saving again',exact=True).click()
  results['M2']['corrected_retry_after']=await state(page)
  await page.reload(wait_until='networkidle');results['M2']['corrected_retry_reload']=await state(page)
  await c.close()
  # Verify that R7's distinct download recovery is a real, usable export.
  c=await b.new_context(viewport={'width':390,'height':844},accept_downloads=True);page=await c.new_page()
  await page.goto('http://127.0.0.1:8661',wait_until='networkidle')
  await page.evaluate("() => {Storage.prototype.setItem=function(){throw new DOMException('Review injected storage write failure','QuotaExceededError')};}")
  await page.get_by_role('button',name='Save collection: The quiet interface',exact=True).click()
  async with page.expect_download() as d:
   await page.get_by_role('button',name='Download copy',exact=True).click()
  download=await d.value
  path=OUT/'R7-storage-failure-download.json';await download.save_as(str(path))
  results['R7']['download']={'suggested_filename':download.suggested_filename,'text':path.read_text()}
  await c.close();await b.close()
 (ROOT/'final_key_measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 print(json.dumps({n:{'saved':r.get('keyboard_saved',{}).get('storage'),'unsaved_reload':r.get('unsaved_reloaded',{}).get('storage'),'unsave_focus':r.get('unsaved_in_saved_view',{}).get('active'),'retry':r.get('corrected_retry_reload',{}).get('storage'),'download':r.get('download'),'failure':r.get('failure')}for n,r in results.items()},ensure_ascii=False,indent=2))
asyncio.run(main())
