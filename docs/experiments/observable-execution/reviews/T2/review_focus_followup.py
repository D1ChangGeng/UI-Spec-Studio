import asyncio,json,os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent
os.environ['FONTCONFIG_FILE']='/workspace/scratch/654b1ee6916f/ui-spec-fonts/fonts.conf'
EXE='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell'

async def main():
 out={}
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path=EXE,args=['--no-sandbox'])
  for app,port in [('L6',8671),('N3',8672),('P8',8673)]:
   ctx=await browser.new_context(viewport={'width':1440,'height':900})
   page=await ctx.new_page()
   await page.goto(f'http://127.0.0.1:{port}/',wait_until='networkidle')
   # One observer/listener per page: fixes the initial harness's duplicate click timestamps.
   await page.evaluate('''() => {
     window.__frames=[];window.__clicks=[];window.__running=true;window.__start=performance.now();
     document.querySelector('#flip').addEventListener('click',()=>window.__clicks.push(performance.now()-window.__start));
     const tick=()=>{if(!window.__running)return;const e=document.querySelector('#note-card'),f=document.querySelector('#card-front'),b=document.querySelector('#card-back');const m=new DOMMatrixReadOnly(getComputedStyle(e).transform);window.__frames.push({t:performance.now()-window.__start,m11:m.m11,m33:m.m33,backAria:b.getAttribute('aria-hidden'),frontAria:f.getAttribute('aria-hidden'),backInert:b.inert,frontInert:f.inert,active:document.activeElement.id,target:e.dataset.face});requestAnimationFrame(tick)};requestAnimationFrame(tick);
   }''')
   # Cross the half-turn once, then reverse while still moving and reverse again.
   box=await page.locator('#flip').bounding_box()
   await page.mouse.click(box['x']+box['width']/2,box['y']+box['height']/2)
   await page.wait_for_timeout(340)
   await page.mouse.click(box['x']+box['width']/2,box['y']+box['height']/2)
   await page.wait_for_timeout(100)
   await page.mouse.click(box['x']+box['width']/2,box['y']+box['height']/2)
   await page.wait_for_timeout(100)
   await page.mouse.click(box['x']+box['width']/2,box['y']+box['height']/2)
   await page.wait_for_timeout(1100)
   trace=await page.evaluate('window.__running=false;({frames:window.__frames,clicks:window.__clicks})')
   final=await page.evaluate('''() => ({target:document.querySelector('#note-card').dataset.face,transform:getComputedStyle(document.querySelector('#note-card')).transform,frontAria:document.querySelector('#card-front').getAttribute('aria-hidden'),backAria:document.querySelector('#card-back').getAttribute('aria-hidden'),active:document.activeElement.id})''')
   await page.screenshot(path=str(ROOT/'captures'/f'{app}-reverse-after-midpoint-settled.png'))
   await page.locator('#motion-toggle').click()
   await page.wait_for_timeout(100)
   a=await page.locator('.orbit-arm').evaluate('(e)=>({transform:getComputedStyle(e).transform,animations:e.getAnimations().map(a=>({state:a.playState,time:a.currentTime}))})')
   await page.wait_for_timeout(350)
   b=await page.locator('.orbit-arm').evaluate('(e)=>({transform:getComputedStyle(e).transform,animations:e.getAnimations().map(a=>({state:a.playState,time:a.currentTime}))})')
   out[app]={'trace':trace,'final':final,'paused_after_100ms':a,'paused_after_450ms':b}
   await ctx.close()
  await browser.close()
 (ROOT/'focus-followup.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 for a,v in out.items():
  f=v['trace']['frames'];clicks=v['trace']['clicks'];m=[x for x in f if x['t']>=clicks[0] and abs(x['m33'])>0.05 and ((x['m33']<0)!=(x['backAria']=='false'))]
  print(a,'clicks',clicks,'final',v['final'],'mismatch samples',len(m),'pauseStable',v['paused_after_100ms']==v['paused_after_450ms'])

asyncio.run(main())
