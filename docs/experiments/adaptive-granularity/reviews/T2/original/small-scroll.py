import asyncio,json,pathlib,time,traceback
from playwright.async_api import async_playwright
OUT=pathlib.Path(__file__).resolve().parent
CHROME='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell'
Q='How can cities make streets cooler in summer? Give a long comparison of shade, routes, maintenance, and practical tradeoffs.'
async def case(b,v,m):
 label=f'v{v}-small-scroll-'+('mobile' if m else 'desktop');result={}
 c=await b.new_context(viewport={'width':390 if m else 1440,'height':844 if m else 900},color_scheme='light');p=await c.new_page();p.set_default_timeout(10000)
 try:
  await p.goto(f'http://127.0.0.1:{8080+v}')
  if v==2:
   await p.locator('[data-demo]:visible').first.click();await p.locator('#response-mode').select_option('long');await p.locator('[data-close="demo-dialog"]').click()
  elif v==3:
   await p.locator('#demo-open-top').click();await p.locator('#next-response').select_option('long');await p.locator('#demo-done').click()
  await p.locator('#question').fill(Q);await p.locator('#question').press('Enter')
  for _ in range(100):
   if await p.locator('#reader').evaluate('(r)=>r.scrollHeight-r.clientHeight>350'):break
   await p.wait_for_timeout(60)
  await p.locator('#reader').hover()
  latest=p.locator('#jump-latest' if v==2 else '#latest')
  if await latest.is_visible():await latest.click()
  await p.evaluate('''()=>{const r=document.querySelector('#reader');window.__smallScroll=[];const t=performance.now();const add=kind=>window.__smallScroll.push({kind,ms:performance.now()-t,top:r.scrollTop,distance:r.scrollHeight-r.scrollTop-r.clientHeight,height:r.scrollHeight,chars:document.querySelector('.answer').textContent.length,running:!document.querySelector('#stop').hidden});r.addEventListener('scroll',()=>add('scroll'),{passive:true});r.addEventListener('wheel',()=>add('wheel'),{passive:true});add('before');const timer=setInterval(()=>add('sample'),20);setTimeout(()=>clearInterval(timer),700)}''')
  await p.mouse.wheel(0,-40);await p.wait_for_timeout(60);await p.screenshot(path=OUT/f'{label}-early.png');await p.wait_for_timeout(440);await p.screenshot(path=OUT/f'{label}-later.png');await p.wait_for_timeout(100)
  result={'wheelDeltaY':-40,'samples':await p.evaluate('window.__smallScroll')}
 except Exception as e:result={'error':str(e),'traceback':traceback.format_exc()}
 (OUT/f'{label}.json').write_text(json.dumps(result,indent=2));await c.close()
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox'])
  await asyncio.gather(*(case(b,v,m) for v in [1,2,3] for m in [False,True]));await b.close()
asyncio.run(main())
