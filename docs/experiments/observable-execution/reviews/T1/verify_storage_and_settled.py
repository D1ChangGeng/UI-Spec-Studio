import asyncio,json,re,traceback
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).parent;OUT=ROOT/'evidence'
BROWSER='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell'
APPS={'R7':8661,'T4':8662,'M2':8663}
LONG='Keeping your place when everything around you is changing'
async def state(page):
 return await page.evaluate('''()=>({url:location.href,scrollY,body:document.body.innerText,documentWidth:document.documentElement.scrollWidth,storage:{...localStorage},active:{tag:document.activeElement.tagName,text:document.activeElement.innerText.slice(0,140),aria:document.activeElement.getAttribute('aria-label')},buttons:[...document.querySelectorAll('button')].map(e=>({text:e.innerText,aria:e.getAttribute('aria-label'),pressed:e.getAttribute('aria-pressed')}))})''')
async def main():
 results={}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=BROWSER,args=['--no-sandbox'])
  for n,port in APPS.items():
   c=await b.new_context(viewport={'width':1440,'height':900});page=await c.new_page();r={};results[n]=r
   try:
    await page.goto(f'http://127.0.0.1:{port}',wait_until='networkidle')
    await page.evaluate("() => {window.__reviewOriginalSetItem=Storage.prototype.setItem; Storage.prototype.setItem=function(){throw new DOMException('Review injected storage write failure','QuotaExceededError')};}")
    await page.get_by_role('button',name=re.compile(r'^Save.*The quiet interface$')).click()
    await page.wait_for_timeout(200)
    r['failed']=await state(page)
    await page.screenshot(path=str(OUT/f'{n}-desktop-storage-failed.png'))
    await page.set_viewport_size({'width':390,'height':844})
    await page.screenshot(path=str(OUT/f'{n}-mobile-storage-failed.png'))
    # Search and saved-only still usable during the failure.
    await page.get_by_role('button',name=re.compile(r'^Saved')).click()
    r['failed_saved_view']=await state(page)
    await page.evaluate('() => {Storage.prototype.setItem=window.__reviewOriginalSetItem;}')
    retry=page.get_by_role('button',name=re.compile(r'retry|try again',re.I))
    if await retry.count():
     await retry.first.click();r['recovery_action']='retry'
    else:
     r['recovery_action']='no retry; toggle off/on'
     await page.get_by_role('button',name=re.compile(r'^(Unsave|Remove).*The quiet interface$')).click()
     await page.get_by_role('button',name=re.compile(r'^All collections')).click()
     await page.get_by_role('button',name=re.compile(r'^Save.*The quiet interface$')).click()
    r['recovered']=await state(page)
    await page.reload(wait_until='networkidle');r['reloaded']=await state(page)
   except Exception as e:r['failure']={'error':str(e),'traceback':traceback.format_exc(),'state':await state(page)}
   await c.close()
  # R7 uses an observable page transition: record the stable view separately from the earlier 100ms frame.
  results['R7']['settled']={}
  for size,w,h in [('desktop',1440,900),('mobile',390,844)]:
   c=await b.new_context(viewport={'width':w,'height':h});page=await c.new_page()
   await page.goto('http://127.0.0.1:8661',wait_until='networkidle')
   await page.locator('a').filter(has_text=LONG).click()
   await page.wait_for_timeout(600)
   results['R7']['settled'][size]={'top':await state(page)}
   await page.screenshot(path=str(OUT/f'R7-{size}-detail-settled.png'))
   await page.mouse.move(w/2,h/2)
   await page.mouse.wheel(0,600)
   await page.wait_for_timeout(200)
   results['R7']['settled'][size]['reading']=await state(page)
   await page.screenshot(path=str(OUT/f'R7-{size}-detail-settled-reading.png'))
   await c.close()
  await b.close()
 (ROOT/'storage_and_settled_measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 print(json.dumps({n:{'action':v.get('recovery_action'),'failed':v.get('failed',{}).get('body','')[:460],'after_storage':v.get('reloaded',{}).get('storage'),'failure':v.get('failure')} for n,v in results.items()},ensure_ascii=False,indent=2))
asyncio.run(main())
