import asyncio,json,pathlib,time,traceback
from playwright.async_api import async_playwright
OUT=pathlib.Path(__file__).resolve().parent
CHROME='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell'
QUERY='How can cities make streets cooler in summer? Give a long comparison of shade, routes, maintenance, and practical tradeoffs.'
DRAFT='Follow-up draft — keep this while I read.\nWhich route should we compare first?\n请保留这段草稿，并比较树荫和候车地点。\nList the assumptions.\nConsider maintenance.\nInclude a short pilot.\nWhat evidence would change the decision?'
async def metrics(page):
    return await page.evaluate('''() => {const r=document.querySelector('#reader'),q=document.querySelector('#question'),a=document.querySelector('.answer'),blocks=[...r.querySelectorAll('[data-chunk],.block,[data-anchor]')];const top=r.getBoundingClientRect().top,anchor=blocks.find(n=>!n.hidden&&n.getBoundingClientRect().bottom>top+12);return {scroll:r.scrollTop,height:r.clientHeight,scrollHeight:r.scrollHeight,answerChars:a?.innerText.length||0,anchor:anchor?.textContent.slice(0,90),anchorOffset:anchor?anchor.getBoundingClientRect().top-top:null,draft:q.value,composerHeight:q.getBoundingClientRect().height,focus:document.activeElement?.outerHTML.slice(0,240),highlightCount:document.querySelectorAll('.cited-paragraph').length,stopVisible:!!document.querySelector('#stop')&&!document.querySelector('#stop').hidden,overflow:document.documentElement.scrollWidth>innerWidth,sourceVisible:[...document.querySelectorAll('#source-panel,#source-dock,#source-dialog')].some(n=>n.tagName==='DIALOG'?n.open:!n.hidden)} }''')
async def case(browser,v,mobile):
    label=f'v{v}-'+('mobile' if mobile else 'desktop');events=[];errors=[];requests=[];start=time.monotonic()
    c=await browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},color_scheme='light')
    page=await c.new_page();page.set_default_timeout(7000)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url) if not r.url.startswith('http://127.0.0.1:') else None)
    async def record(name,shot=False):
        d={'event':name,'seconds':round(time.monotonic()-start,3),**await metrics(page)};events.append(d)
        if shot:await page.screenshot(path=OUT/f'{label}-{name}.png')
    async def close_source():
        if v==1:sel='[data-close="source-dialog"]' if mobile else '[data-close-source]'
        elif v==2:sel='[data-close="source-dialog"]' if mobile else '#source-close'
        else:sel='#source-return'
        await page.locator(sel).click()
    try:
        await page.goto(f'http://127.0.0.1:{8080+v}')
        if v==2:
            await page.locator('[data-demo]:visible').first.click();await page.locator('#response-mode').select_option('long');await page.locator('[data-close="demo-dialog"]').click()
        if v==3:
            await page.locator('#demo-open-top').click();await page.locator('#next-response').select_option('long');await page.locator('#demo-done').click()
        await page.locator('#question').fill(QUERY);await page.locator('#question').press('Enter');await record('pending',True)
        await page.locator('#question').fill(DRAFT)
        file_sel='#file-picker' if v==3 else '#file-input'
        await page.locator(file_sel).set_input_files({'name':'field-notes.txt','mimeType':'text/plain','buffer':b'Local review fixture. Filename only.'})
        citation=page.locator('.inline-citation' if v==3 else '.citation').first
        await citation.wait_for(state='visible',timeout=15000)
        await record('stream-draft',True)
        await citation.scroll_into_view_if_needed();await record('before-source')
        await citation.click();await page.wait_for_timeout(100);await record('source-open-0',True)
        await page.wait_for_timeout(650);await record('source-open-650ms',True)
        source_action=None
        if v==2:source_action=page.locator(('#source-dialog' if mobile else '#source-panel')+' [data-source-action]')
        if v==3:source_action=page.locator('#source-generation-action')
        if v==1 and mobile:
            events.append({'event':'source-stop-controls','count':await page.locator('#source-dialog button').count(),'labels':await page.locator('#source-dialog button').all_text_contents()})
            await close_source();await page.locator('#stop').click();await record('stopped-after-return',True)
            await page.get_by_role('button',name='Continue response',exact=True).click()
        else:
            await (source_action if source_action else page.locator('#stop')).click();await record('stopped-source',True)
            if source_action:await source_action.click()
            else:await page.get_by_role('button',name='Continue response',exact=True).click()
            await record('recovery-source',True)
            await page.wait_for_timeout(600);await close_source()
        await page.wait_for_timeout(100);await record('source-return',True)
        # A deliberate wheel input takes the reader away from the newest output.
        await page.locator('#reader').hover();await page.mouse.wheel(0,-900);await page.wait_for_timeout(150)
        await record('manual-scroll-0',True);await page.wait_for_timeout(900);await record('manual-scroll-900ms',True)
        latest=page.locator('#jump-latest' if v==2 else '#latest')
        if await latest.is_visible():await latest.click();await record('latest-click')
        await page.wait_for_function("document.querySelector('#stop').hidden",timeout=25000)
        await record('complete',True)
        # Desktop theme is directly reachable; narrow theme is exercised separately.
        if not mobile:
            theme=page.locator('[data-theme-toggle]:visible').first if v==2 else page.locator('#theme')
            await theme.click();await record('dark-draft',True)
        await page.reload();await page.wait_for_timeout(300);await record('reload',True)
        # Second question fails on demand, then recovers via the visible retry action.
        if v==1:
            await page.locator('#demo-open').click();await page.locator('#fail-next').check();await page.locator('[data-close="demo-dialog"]').click()
        elif v==2:
            await page.locator('[data-demo]:visible').first.click();await page.locator('#response-mode').select_option('fail');await page.locator('[data-close="demo-dialog"]').click()
        else:
            await page.locator('#demo-open-top').click();await page.locator('#next-response').select_option('failure');await page.locator('#demo-done').click()
        await page.locator('#question').fill('What would a small pilot on this route look like?');await page.locator('#question').press('Enter')
        retry=page.get_by_role('button',name='Retry response' if v in (1,2) else 'Try again',exact=True).last
        await retry.wait_for(state='visible',timeout=8000);await record('simulated-failure',True)
        await retry.click();await page.wait_for_function("document.querySelector('#stop').hidden",timeout=25000);await record('failure-recovered',True)
    except Exception as e:
        events.append({'event':'HARNESS_OR_PRODUCT_FAILURE','type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()})
        try:await page.screenshot(path=OUT/f'{label}-original-failure.png')
        except:pass
    finally:
        (OUT/f'{label}-events.json').write_text(json.dumps({'variant':v,'viewport':[390,844] if mobile else [1440,900],'query':QUERY,'draft':DRAFT,'events':events,'pageerrors':errors,'externalRequests':requests},ensure_ascii=False,indent=2))
        await c.close()
async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox'])
        await asyncio.gather(*(case(browser,v,m) for v in [1,2,3] for m in [False,True]))
        await browser.close()
asyncio.run(main())
