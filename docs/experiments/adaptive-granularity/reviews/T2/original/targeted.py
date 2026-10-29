import asyncio,json,pathlib,time,traceback
from playwright.async_api import async_playwright
OUT=pathlib.Path(__file__).resolve().parent
CHROME='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell'
Q='How can cities make streets cooler in summer? Give a long comparison of shade, routes, maintenance, and practical tradeoffs.'
D='Follow-up draft — keep this while I read.\nWhich route should we compare first?\n请保留这段草稿，并比较树荫和候车地点。\nList the assumptions.\nConsider maintenance.\nInclude a short pilot.\nWhat evidence would change the decision?'
async def inspect(page):
 return await page.evaluate('''()=>{const r=document.querySelector('#reader'),rb=r.getBoundingClientRect(),target=document.querySelector('.cited-paragraph');return {scroll:r.scrollTop,reader:rb.toJSON(),scrollHeight:r.scrollHeight,focus:document.activeElement?.outerHTML.slice(0,180),draft:document.querySelector('#question').value,target:target?.getBoundingClientRect().toJSON(),targetText:target?.textContent,visibleBlocks:[...r.querySelectorAll('[data-chunk],.block,[data-anchor]')].filter(n=>!n.hidden&&n.textContent.trim()&&n.getBoundingClientRect().bottom>rb.top&&n.getBoundingClientRect().top<rb.bottom).map(n=>n.textContent.slice(0,80)),answerText:document.querySelector('.answer')?.innerText,sourceOpen:[...document.querySelectorAll('#source-panel,#source-dock,#source-dialog')].some(n=>n.tagName==='DIALOG'?n.open:!n.hidden),latestVisible:[...document.querySelectorAll('#latest,#jump-latest')].some(n=>!n.hidden)}}''')
async def case(browser,v,mobile):
 name=f'v{v}-targeted-'+('mobile' if mobile else 'desktop');events=[]
 c=await browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},color_scheme='light');p=await c.new_page();p.set_default_timeout(12000)
 async def rec(n):
  events.append({'event':n,**await inspect(p)});await p.screenshot(path=OUT/f'{name}-{n}.png')
 try:
  await p.goto(f'http://127.0.0.1:{8080+v}')
  if v==2:
   await p.locator('[data-demo]:visible').first.click();await p.locator('#response-mode').select_option('long');await p.locator('[data-close="demo-dialog"]').click()
  elif v==3:
   await p.locator('#demo-open-top').click();await p.locator('#next-response').select_option('long');await p.locator('#demo-done').click()
  await p.locator('#question').fill(Q);await p.locator('#question').press('Enter');await p.locator('#question').fill(D)
  cite=p.locator('.inline-citation' if v==3 else '.citation').first
  await cite.wait_for(state='visible')
  if v==2:
   await p.locator('#stop').wait_for(state='hidden',timeout=15000);await cite.click()
   scope=p.locator('#source-dialog' if mobile else '#source-panel')
   nav=scope.locator('.source-nav button').nth(2);await nav.focus();await nav.press('Enter');await p.wait_for_timeout(120);await rec('source3-keyboard-settled')
   await p.keyboard.press('Tab');await rec('source3-next-tab')
   await scope.locator('[data-show-passage]').click();await rec('show-paragraph-immediate')
   await p.wait_for_timeout(200);await rec('show-paragraph-settled')
  elif v==3:
   await cite.click();await p.wait_for_timeout(1200);await p.locator('#source-generation-action').click();await rec('stopped')
   await p.locator('#source-generation-action').click();await p.wait_for_timeout(250);await p.locator('#source-return').click();await rec('retry-return-0')
   if await p.locator('#latest').is_visible():await p.locator('#latest').click()
   await rec('retry-latest');await p.wait_for_timeout(700);await rec('retry-latest-700ms');await p.wait_for_timeout(1200);await rec('retry-latest-1900ms')
  else:
   await cite.click();await rec('source-open')
   panel=p.locator('#source-dialog' if mobile else '#source-dock');await panel.hover();await p.mouse.wheel(0,2000);await p.wait_for_timeout(200);await rec('source-bottom')
   events.append({'event':'panel-controls','controls':await panel.locator('button').all_text_contents(),'closeRect':await panel.locator('button').first.bounding_box()})
   await p.keyboard.press('Escape');await p.wait_for_timeout(100);await rec('escape-closed')
 except Exception as e:
  events.append({'event':'HARNESS_OR_PRODUCT_FAILURE','error':str(e),'traceback':traceback.format_exc()});await p.screenshot(path=OUT/f'{name}-original-failure.png')
 (OUT/f'{name}.json').write_text(json.dumps(events,ensure_ascii=False,indent=2));await c.close()
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox'])
  await asyncio.gather(*(case(b,v,m) for v in [1,2,3] for m in [False,True]));await b.close()
asyncio.run(main())
