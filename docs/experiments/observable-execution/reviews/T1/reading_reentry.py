import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).parent
LONG='Keeping your place when everything around you is changing'
async def snap(page):
 return await page.evaluate('''()=>({url:location.href,scrollY,active:{tag:document.activeElement.tagName,text:document.activeElement.innerText.slice(0,130)},visibleText:[...document.querySelectorAll('h1,h2,p,a,button')].filter(e=>{const r=e.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight}).map(e=>({text:e.innerText,y:e.getBoundingClientRect().top}))})''')
async def main():
 results={}
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  for n,port in {'R7':8661,'T4':8662,'M2':8663}.items():
   c=await b.new_context(viewport={'width':390,'height':844});page=await c.new_page();r={};results[n]=r
   await page.goto(f'http://127.0.0.1:{port}',wait_until='networkidle')
   link=page.locator('a').filter(has_text=LONG);await link.scroll_into_view_if_needed();r['list_before']=await snap(page)
   await link.click();await page.wait_for_timeout(600)
   await page.mouse.move(195,500);await page.mouse.wheel(0,600);await page.wait_for_timeout(200);r['reading_before']=await snap(page)
   await page.go_back(wait_until='networkidle');await page.wait_for_timeout(600);r['list_returned']=await snap(page)
   await page.locator('a').filter(has_text=LONG).click();await page.wait_for_timeout(600);r['reading_reentered']=await snap(page)
   await page.screenshot(path=str(ROOT/'evidence'/f'{n}-mobile-reading-reentered-stable.png'))
   await c.close()
  await b.close()
 (ROOT/'reading_reentry_measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 print(json.dumps({n:{k:v['scrollY'] for k,v in r.items()}for n,r in results.items()},indent=2))
asyncio.run(main())
