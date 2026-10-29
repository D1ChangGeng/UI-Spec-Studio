import asyncio, contextlib, functools, json, threading, time, traceback
from http.server import ThreadingHTTPServer
from playwright.async_api import async_playwright
from review_runner import BASE, OUT, CHROME, QuietHandler, SHORT, fill, state

DATA={'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'runs':[]}
async def snap(page,run,label):
    s=await state(page);s['label']=label
    p=OUT/run['name']/f'{label}.png';p.parent.mkdir(exist_ok=True)
    await page.screenshot(path=str(p));s['image']=str(p.relative_to(OUT));run['states'].append(s)
    (OUT/'keyboard-observations.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2))
async def probe(browser,n,width):
    run={'name':f'variant-{n:02d}-keyboard-{width}','variant':n,'viewport':[width,844 if width==390 else 900],'states':[],'errors':[]};DATA['runs'].append(run)
    ctx=await browser.new_context(viewport={'width':width,'height':run['viewport'][1]},color_scheme='light')
    page=await ctx.new_page()
    try:
        await page.goto(f'http://127.0.0.1:{8630+n}/final/')
        await page.locator('#new-note').click();await page.wait_for_timeout(500);await fill(page,SHORT,'Archive visit')
        await page.evaluate('''()=>{window.__set=Storage.prototype.setItem;window.__fail=true;Storage.prototype.setItem=function(k,v){if(window.__fail)throw new DOMException('Keyboard probe forced quota failure','QuotaExceededError');return window.__set.call(this,k,v)}}''')
        await page.locator('#save').focus();await snap(page,run,'00-keyboard-save-focused');await page.keyboard.press('Enter');await page.wait_for_timeout(1200);await snap(page,run,'01-keyboard-failure')
        await page.keyboard.press('Tab');await snap(page,run,'02-next-tab')
        await page.keyboard.press('Tab');await snap(page,run,'03-second-tab')
        await page.evaluate('window.__fail=false');await page.locator('#retry').focus();await page.keyboard.press('Enter');await page.wait_for_timeout(1800);await snap(page,run,'04-keyboard-retry')
    except Exception as e:run['errors'].append({'exception':str(e),'traceback':traceback.format_exc()})
    finally:
        (OUT/'keyboard-observations.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2));await ctx.close()
async def main():
    servers=[]
    for n in range(1,4):
        s=ThreadingHTTPServer(('127.0.0.1',8630+n),functools.partial(QuietHandler,directory=str(BASE/f'variant-{n:02d}')));threading.Thread(target=s.serve_forever,daemon=True).start();servers.append(s)
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox'])
            for n in range(1,4):
                for width in (1440,390):await probe(b,n,width)
            await b.close()
    finally:
        for s in servers:s.shutdown()
        DATA['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());(OUT/'keyboard-observations.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2))
if __name__=='__main__':asyncio.run(main())
