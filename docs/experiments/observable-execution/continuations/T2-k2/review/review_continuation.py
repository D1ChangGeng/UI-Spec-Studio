import asyncio,json,os,threading,hashlib,traceback
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from playwright.async_api import async_playwright

WORK=Path('/workspace/scratch/654b1ee6916f')
ROOT=WORK/'observable-continuation-review'
CAP=ROOT/'captures'
OLD=WORK/'observable-product-review/T2/L6/app'
NEW=WORK/'observable-continuation/T2-k2/app'
os.environ['FONTCONFIG_FILE']=str(WORK/'ui-spec-fonts/fonts.conf')
EXE=str(WORK/'ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell')

OBSERVER='''() => {
 if(window.__observerStop)window.__observerStop();
 const trace={start:performance.now(),frames:[],clicks:[]};let running=true,raf;
 const click=()=>trace.clicks.push(performance.now()-trace.start);
 document.querySelector('#flip').addEventListener('click',click);
 const tick=()=>{if(!running)return;const card=document.querySelector('#note-card'),f=document.querySelector('#card-front'),b=document.querySelector('#card-back');const m=new DOMMatrixReadOnly(getComputedStyle(card).transform);trace.frames.push({t:performance.now()-trace.start,m11:m.m11,m33:m.m33,target:card.dataset.face,frontAria:f.getAttribute('aria-hidden'),backAria:b.getAttribute('aria-hidden'),frontInert:f.inert,backInert:b.inert,active:document.activeElement.id,flipText:document.querySelector('#flip').innerText});raf=requestAnimationFrame(tick)};
 window.__observerStop=()=>{running=false;cancelAnimationFrame(raf);document.querySelector('#flip').removeEventListener('click',click);return trace};
 window.__trace=trace;raf=requestAnimationFrame(tick);
}'''

SNAPSHOT='''() => {
 const ids=['note-card','card-front','card-back','preview-note','flip'];const out={time:performance.now(),active:document.activeElement.id,viewport:{w:innerWidth,h:innerHeight},scrollY,animations:document.getAnimations().map(a=>({type:a.constructor.name,playState:a.playState,target:a.effect.target.id||a.effect.target.className}))};
 for(const id of ids){const e=document.getElementById(id),s=getComputedStyle(e),r=e.getBoundingClientRect();out[id]={text:e.innerText,rect:{x:r.x,y:r.y,w:r.width,h:r.height},ariaHidden:e.getAttribute('aria-hidden'),inert:e.inert,tabIndex:e.tabIndex,transform:s.transform,backfaceVisibility:s.backfaceVisibility,visibility:s.visibility,opacity:s.opacity,dataset:{...e.dataset}}}
 const m=new DOMMatrixReadOnly(out['note-card'].transform);out.m11=m.m11;out.m33=m.m33;return out;
}'''

def fingerprints():
 paths=[OLD/n for n in ['index.html','styles.css','app.js']]+[NEW/n for n in ['index.html','styles.css','app.js']]+[WORK/'observable-product-review/T2/review.md']
 return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

async def snapshot(page):return await page.evaluate(SNAPSHOT)
async def stop(page):return await page.evaluate('window.__observerStop()')
async def capture(page,name):
 before=await snapshot(page)
 await page.screenshot(path=str(CAP/name))
 after=await snapshot(page)
 return {'file':name,'before':before,'after':after}

async def run_case(browser,label,url,size):
 w,h=(1440,900) if size=='desktop' else (390,844)
 ctx=await browser.new_context(viewport={'width':w,'height':h},device_scale_factor=1,reduced_motion='no-preference')
 page=await ctx.new_page()
 await page.goto(url,wait_until='networkidle')
 baseline=await snapshot(page)
 await page.evaluate(OBSERVER)
 await page.locator('#flip').click()
 await page.wait_for_timeout(45)
 await page.keyboard.press('Shift+Tab')
 early=await snapshot(page)
 early_shot=await capture(page,f'{label}-{size}-early-shifttab.png')
 await page.wait_for_timeout(850)
 early_final=await snapshot(page)
 early_trace=await stop(page)

 # The back is settled and visible. Activate the flip button with the keyboard,
 # then Shift+Tab while the back still faces the reader; observe focus as it hides.
 await page.locator('#flip').focus()
 await page.evaluate(OBSERVER)
 await page.keyboard.press('Space')
 await page.wait_for_timeout(45)
 await page.keyboard.press('Shift+Tab')
 handoff_early=await snapshot(page)
 handoff_shot=await capture(page,f'{label}-{size}-back-leaving-focus.png')
 await page.wait_for_timeout(900)
 handoff_final=await snapshot(page)
 handoff_trace=await stop(page)
 await capture(page,f'{label}-{size}-handoff-settled.png')

 # Reverse once after the card has visibly crossed the half-turn.
 await page.locator('#flip').focus()
 await page.evaluate(OBSERVER)
 await page.keyboard.press('Space')
 await page.wait_for_function("new DOMMatrixReadOnly(getComputedStyle(document.querySelector('#note-card')).transform).m11 < -0.3",polling='raf',timeout=2000)
 before_reverse=await snapshot(page)
 await page.keyboard.press('Space')
 after_reverse=await snapshot(page)
 reversal_shot=await capture(page,f'{label}-{size}-after-midpoint-reversal.png')
 await page.wait_for_timeout(950)
 reversal_final=await snapshot(page)
 reversal_trace=await stop(page)
 await ctx.close()

 # Fresh reduced-motion context, same dimensions and same early keyboard input.
 quiet_ctx=await browser.new_context(viewport={'width':w,'height':h},device_scale_factor=1,reduced_motion='reduce')
 quiet=await quiet_ctx.new_page()
 await quiet.goto(url,wait_until='networkidle')
 await quiet.evaluate(OBSERVER)
 await quiet.locator('#flip').click()
 await quiet.wait_for_timeout(45)
 await quiet.keyboard.press('Shift+Tab')
 reduced_early=await snapshot(quiet)
 reduced_shot=await capture(quiet,f'{label}-{size}-reduced-motion.png')
 await quiet.wait_for_timeout(150)
 reduced_final=await snapshot(quiet)
 reduced_trace=await stop(quiet)
 await quiet_ctx.close()
 return {'baseline':baseline,'early':{'state':early,'capture':early_shot,'settled':early_final,'trace':early_trace},'handoff':{'early':handoff_early,'capture':handoff_shot,'settled':handoff_final,'trace':handoff_trace},'midpoint_reversal':{'before_reverse':before_reverse,'after_reverse':after_reverse,'capture':reversal_shot,'settled':reversal_final,'trace':reversal_trace},'reduced':{'early':reduced_early,'capture':reduced_shot,'settled':reduced_final,'trace':reduced_trace}}

async def main():
 ROOT.mkdir(exist_ok=True);CAP.mkdir(exist_ok=True)
 report={'scope':'Only continuation of L6 invisible-back keyboard focus issue; original comparison unchanged','preflight':'Original service 8671 refused connection; fixed service 8493 returned HTTP 200. This script hosts original read-only for its own lifetime.','fingerprints_before':fingerprints(),'cases':{}}
 server=ThreadingHTTPServer(('127.0.0.1',8671),partial(SimpleHTTPRequestHandler,directory=str(OLD)))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 try:
  async with async_playwright() as p:
   browser=await p.chromium.launch(executable_path=EXE,headless=True,args=['--no-sandbox'])
   for label,url in [('original','http://127.0.0.1:8671/'),('fixed','http://127.0.0.1:8493/')]:
    for size in ['desktop','mobile']:
     name=f'{label}-{size}'
     print('START',name,flush=True)
     try:report['cases'][name]=await run_case(browser,label,url,size)
     except Exception as e:report['cases'][name]={'check_error':str(e),'traceback':traceback.format_exc()};print(traceback.format_exc(),flush=True)
     (ROOT/'raw-measurements.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
     print('DONE',name,flush=True)
   await browser.close()
 finally:server.shutdown()
 report['fingerprints_after']=fingerprints()
 report['files_unchanged']=report['fingerprints_before']==report['fingerprints_after']
 (ROOT/'raw-measurements.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print('ALL DONE; files_unchanged=',report['files_unchanged'],flush=True)

asyncio.run(main())
