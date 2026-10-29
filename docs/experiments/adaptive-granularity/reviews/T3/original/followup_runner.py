import asyncio, contextlib, functools, json, threading, time, traceback
from pathlib import Path
from http.server import ThreadingHTTPServer
from playwright.async_api import async_playwright
from review_runner import BASE, OUT, CHROME, QuietHandler, LONG, SHORT, THIRD, state, fill

DATA={'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'runs':[]}
def flush():(OUT/'followup-observations.json').write_text(json.dumps(DATA,indent=2,ensure_ascii=False))
async def cap(page,run,label):
    path=OUT/run['name']/f'{label}.png';path.parent.mkdir(exist_ok=True)
    s=await state(page);s['label']=label;s['image']=str(path.relative_to(OUT));await page.screenshot(path=str(path),animations='allow');run['states'].append(s);flush();return s
async def sequence(page,run,label,times):
    start=time.monotonic()
    for ms in times:
        await asyncio.sleep(max(0,ms/1000-(time.monotonic()-start)))
        s=await cap(page,run,f'{label}-{ms:04d}ms');s['actual_elapsed_ms']=round((time.monotonic()-start)*1000)
    flush()

async def review(browser,n):
    run={'name':f'variant-{n:02d}-followup','variant':n,'states':[],'checks':[],'errors':[]};DATA['runs'].append(run)
    ctx=await browser.new_context(viewport={'width':1440,'height':900},color_scheme='light')
    page=await ctx.new_page()
    try:
        await page.goto(f'http://127.0.0.1:{8530+n}/final/')
        await page.locator('#new-note').click();await page.wait_for_timeout(450);await fill(page,LONG)
        await page.evaluate('''()=>{window.__set=Storage.prototype.setItem;window.__blockWrite=true;Storage.prototype.setItem=function(k,v){if(window.__blockWrite)throw new DOMException('Review forced write failure','QuotaExceededError');return window.__set.call(this,k,v)}}''')
        await page.locator('#save').click();await page.wait_for_timeout(1200);s=await cap(page,run,'00-first-save-failure')
        run['checks'].append({'first_failure_face':s['face'],'first_failure_storage_empty':not s['storage'],'first_failure_draft_retained':s['note']['value']==LONG})
        await page.evaluate('window.__blockWrite=false');await page.locator('#retry').click();await page.wait_for_timeout(1800)
        await page.locator('#return').click();await page.wait_for_timeout(850)
        await fill(page,LONG+'\nA');await page.locator('#save').click();await page.locator('#note-text').fill(LONG+'\nA plus newer unsaved text');await page.wait_for_timeout(1800)
        s=await cap(page,run,'01-type-during-save');run['checks'].append({'typing_during_save_front':s['face']=='front','typing_during_save_draft':s['note']['value'],'typing_during_save_saved':s['savedText'],'status':s['status']})
        await page.locator('#back-collection').click();await page.wait_for_timeout(500)
        for text in (SHORT,THIRD):
            await page.locator('#new-note').click();await page.wait_for_timeout(400);await fill(page,text,'Archive visit' if text==SHORT else '雨后的街道');await page.locator('#save').click();await page.wait_for_timeout(1800);await page.locator('#back-collection').click();await page.wait_for_timeout(450)
        await cap(page,run,'02-route-start')
        await page.locator('#note-grid>button').nth(1).click();await sequence(page,run,'03-open-second',[0,80,160,260,500])
        await page.locator('#flip').click();await page.wait_for_timeout(850)
        await page.locator('#back-collection').click();await sequence(page,run,'04-return-second',[0,80,160,260,500])
        # A rapid route request while the card is already rotating; use actual click actions.
        await page.locator('#note-grid>button').nth(0).click();await page.wait_for_timeout(450);await page.locator('#flip').click();await page.wait_for_timeout(80);await page.locator('#back-collection').click();await page.locator('#note-grid>button').nth(2).click();await sequence(page,run,'05-rapid-switch',[0,100,500])
        s=await state(page);run['checks'].append({'rapid_switch_third_value':s['note']['value'],'rapid_switch_third_back':s['savedText'],'rapid_switch_face':s['face']})
        await page.locator('#back-collection').click();await page.wait_for_timeout(500)
        # Startup read failure with persisted records already present; recovery occurs through the supplied UI.
        await ctx.add_init_script('''window.__get=Storage.prototype.getItem;window.__blockRead=true;Storage.prototype.getItem=function(k){if(window.__blockRead)throw new DOMException('Review forced read failure','SecurityError');return window.__get.call(this,k)}''')
        await page.reload();await page.wait_for_timeout(250);await page.evaluate('window.__blockRead=false');await cap(page,run,'06-read-failure')
        await page.locator('#collection-retry').click();await page.wait_for_timeout(300);s=await cap(page,run,'07-read-recovered');run['checks'].append({'read_recovery_tiles':len(s['tiles'])})
    except Exception as e:
        run['errors'].append({'exception':str(e),'traceback':traceback.format_exc()})
        with contextlib.suppress(Exception):await cap(page,run,'ERROR-original')
    finally:flush();await ctx.close()

async def reduced_repro(browser,n,width):
    run={'name':f'variant-{n:02d}-reduced-repro-{width}','variant':n,'states':[],'checks':[],'errors':[]};DATA['runs'].append(run)
    ctx=await browser.new_context(viewport={'width':width,'height':844 if width==390 else 900},color_scheme='light',reduced_motion='reduce')
    page=await ctx.new_page()
    try:
        await page.goto(f'http://127.0.0.1:{8530+n}/final/');await page.wait_for_timeout(250);await cap(page,run,'00-empty')
        await page.locator('#new-note').click();await page.wait_for_timeout(1000);await fill(page,LONG);await page.evaluate('scrollTo(0,0)');await page.wait_for_timeout(1500);await cap(page,run,'01-editor-stable')
        await page.wait_for_timeout(300);await cap(page,run,'02-editor-second-capture')
        await page.locator('#save').click();await page.wait_for_timeout(1900);await cap(page,run,'03-saved-stable')
        await page.locator('#return').click();await page.wait_for_timeout(500);await cap(page,run,'04-return-stable')
        await page.locator('#back-collection').click();await page.wait_for_timeout(500);await cap(page,run,'05-collection-return')
        await page.locator('#note-grid>button').first.focus();await page.keyboard.press('Enter');await page.wait_for_timeout(500)
        focus=[]
        for i in range(7):
            await page.keyboard.press('Tab');focus.append(await page.evaluate('({id:document.activeElement.id,tag:document.activeElement.tagName,hiddenFace:!!document.activeElement.closest("[inert]"),text:document.activeElement.textContent.slice(0,70)})'))
        run['checks'].append({'tab_sequence':focus,'hidden_face_focused':any(s['hiddenFace'] for s in focus)})
        await page.evaluate('scrollTo(0,0)');await cap(page,run,'06-tab-followup')
    except Exception as e:
        run['errors'].append({'exception':str(e),'traceback':traceback.format_exc()})
        with contextlib.suppress(Exception):await cap(page,run,'ERROR-original')
    finally:flush();await ctx.close()

async def main():
    servers=[]
    for n in range(1,4):
        s=ThreadingHTTPServer(('127.0.0.1',8530+n),functools.partial(QuietHandler,directory=str(BASE/f'variant-{n:02d}')));threading.Thread(target=s.serve_forever,daemon=True).start();servers.append(s)
    try:
        async with async_playwright() as p:
            browser=await p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox'])
            for n in range(1,4):
                await review(browser,n)
                await reduced_repro(browser,n,390)
                await reduced_repro(browser,n,1440)
            await browser.close()
    finally:
        for s in servers:s.shutdown()
        DATA['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());flush()

if __name__=='__main__':asyncio.run(main())
