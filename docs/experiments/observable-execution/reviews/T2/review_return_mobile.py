import asyncio,json,os,threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent
os.environ['FONTCONFIG_FILE']='/workspace/scratch/654b1ee6916f/ui-spec-fonts/fonts.conf'
EXE='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell'
NOTE=json.loads((ROOT/'checks.json').read_text())['L6']['long_mobile_zh_dark']['note']
MEASURE='''() => {const e=document.querySelector('#note-text'),r=document.querySelector('#return').getBoundingClientRect();return {active:document.activeElement.id,start:e.selectionStart,end:e.selectionEnd,inputScroll:e.scrollTop,pageScroll:scrollY,returnRect:{x:r.x,y:r.y,w:r.width,h:r.height},viewport:{w:innerWidth,h:innerHeight},note:e.value}}'''
async def main():
 out={}
 servers=[]
 for app,port in [('L6',8671),('N3',8672),('P8',8673)]:
  server=ThreadingHTTPServer(('127.0.0.1',port),partial(SimpleHTTPRequestHandler,directory=str(ROOT/app/'app')))
  threading.Thread(target=server.serve_forever,daemon=True).start();servers.append(server)
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=EXE,args=['--no-sandbox'])
  for app,port in [('L6',8671),('N3',8672),('P8',8673)]:
   ctx=await b.new_context(viewport={'width':390,'height':844})
   page=await ctx.new_page()
   await page.goto(f'http://127.0.0.1:{port}/',wait_until='networkidle')
   await page.locator('#locale-toggle').click();await page.locator('#theme-toggle').click()
   await page.locator('#note-text').fill(NOTE)
   await page.locator('#save').click();await page.wait_for_timeout(1200)
   await page.locator('#note-text').focus();await page.keyboard.press('Control+Home')
   for i in range(8):await page.keyboard.press('ArrowDown')
   for i in range(5):await page.keyboard.press('Shift+ArrowRight')
   before=await page.evaluate(MEASURE)
   await page.locator('#saved-link').click();await page.wait_for_timeout(150)
   saved_top=await page.evaluate(MEASURE)
   await page.screenshot(path=str(ROOT/'captures'/f'{app}-mobile-long-saved-viewport.png'))
   await page.keyboard.press('Tab')
   tab=await page.evaluate(MEASURE)
   await page.keyboard.press('Enter');await page.wait_for_timeout(150)
   returned=await page.evaluate(MEASURE)
   await page.screenshot(path=str(ROOT/'captures'/f'{app}-mobile-long-return-focus.png'))
   out[app]={'before':before,'saved_top':saved_top,'tab':tab,'returned':returned}
   await ctx.close()
  await b.close()
 (ROOT/'return-mobile.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 for a,z in out.items():print(a,'return rect',z['saved_top']['returnRect'],'tab',z['tab']['active'],'selection before/after',(z['before']['start'],z['before']['end']),(z['returned']['start'],z['returned']['end']),'input scroll',z['before']['inputScroll'],z['returned']['inputScroll'],'active',z['returned']['active'])
 for server in servers:server.shutdown()
asyncio.run(main())
