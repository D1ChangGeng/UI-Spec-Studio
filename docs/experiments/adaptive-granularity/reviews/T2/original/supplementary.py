import asyncio,json,pathlib,time,traceback
from playwright.async_api import async_playwright
OUT=pathlib.Path(__file__).resolve().parent
CHROME='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell'
QUERY='How can cities make streets cooler in summer? Give a long comparison of shade, routes, maintenance, and practical tradeoffs.'
DRAFT='Follow-up draft — keep this while I read.\nWhich route should we compare first?\n请保留这段草稿，并比较树荫和候车地点。\nList the assumptions.\nConsider maintenance.\nInclude a short pilot.\nWhat evidence would change the decision?'
async def metrics(page):
    return await page.evaluate('''() => {const r=document.querySelector('#reader'),q=document.querySelector('#question'),a=document.querySelector('.answer'),blocks=[...r.querySelectorAll('[data-chunk],.block,[data-anchor]')];const top=r.getBoundingClientRect().top,anchor=blocks.find(n=>!n.hidden&&n.getBoundingClientRect().bottom>top+12);return {scroll:r.scrollTop,height:r.clientHeight,scrollHeight:r.scrollHeight,answerChars:a?.innerText.length||0,anchor:anchor?.textContent.slice(0,90),anchorOffset:anchor?anchor.getBoundingClientRect().top-top:null,draft:q.value,composerHeight:q.getBoundingClientRect().height,focus:document.activeElement?.outerHTML.slice(0,240),highlightCount:document.querySelectorAll('.cited-paragraph').length,stopVisible:!!document.querySelector('#stop')&&!document.querySelector('#stop').hidden,overflow:document.documentElement.scrollWidth>innerWidth,sourceVisible:[...document.querySelectorAll('#source-panel,#source-dock,#source-dialog')].some(n=>n.tagName==='DIALOG'?n.open:!n.hidden)} }''')
async def initial(browser,v,mobile):
    name=f'v{v}-initial-source-'+('mobile' if mobile else 'desktop');r={};start=time.monotonic()
    c=await browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},color_scheme='light');page=await c.new_page();page.set_default_timeout(15000)
    try:
        await page.goto(f'http://127.0.0.1:{8083+v}');await page.locator('#question').fill(QUERY);await page.locator('#question').press('Enter')
        sel='.source-button' if v==1 else '.citation' if v==2 else '.source-chip'
        b=page.locator(sel).first;await b.wait_for(state='visible');r['sourceAvailableSeconds']=round(time.monotonic()-start,3);r['responseRunningWhenSourceAvailable']=await page.locator('#stop').is_visible()
        await b.click();await page.screenshot(path=OUT/f'{name}.png');r['buttons']=await page.locator('#source-dock:not([hidden]) button,#source-panel:not([hidden]) button,#source-dialog[open] button').all_text_contents()
    except Exception as e:r['error']=str(e);r['traceback']=traceback.format_exc()
    (OUT/f'{name}.json').write_text(json.dumps(r,indent=2));await c.close()
async def final(browser,v,mobile):
    label=f'v{v}-supplement-'+('mobile' if mobile else 'desktop');events=[];errors=[]
    c=await browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900},color_scheme='light');page=await c.new_page();page.set_default_timeout(10000);page.on('pageerror',lambda e:errors.append(str(e)))
    async def rec(name,shot=True):
        events.append({'event':name,**await metrics(page)})
        if shot:await page.screenshot(path=OUT/f'{label}-{name}.png')
    async def close_source():
        await page.locator(('[data-close="source-dialog"]' if mobile else '[data-close-source]') if v==1 else ('[data-close="source-dialog"]' if mobile else '#source-close') if v==2 else '#source-return').click()
    try:
        await page.goto(f'http://127.0.0.1:{8080+v}')
        if v==2:
            await page.locator('[data-demo]:visible').first.click();await page.locator('#response-mode').select_option('long');await page.locator('[data-close="demo-dialog"]').click()
        elif v==3:
            await page.locator('#demo-open-top').click();await page.locator('#next-response').select_option('long');await page.locator('#demo-done').click()
        await page.locator('#question').fill(QUERY);await page.locator('#question').press('Enter');await page.locator('#question').fill('Short draft held for the source visit.')
        cite=page.locator('.inline-citation' if v==3 else '.citation').first;await cite.wait_for(state='visible')
        await page.evaluate('''() => {window.__reviewClick=[];document.addEventListener('pointerdown',e=>{if(e.target.closest('.citation,.inline-citation')){const r=document.querySelector('#reader');window.__reviewClick.push({scroll:r.scrollTop,rect:e.target.getBoundingClientRect().toJSON(),text:e.target.parentElement.textContent})}},true)}''')
        await cite.click();await page.wait_for_timeout(100);await rec('opened')
        events.append({'event':'citation-pointerdown','samples':await page.evaluate('window.__reviewClick')})
        if not mobile:
            await page.locator('#question').fill(DRAFT);await rec('grow-composer-with-source')
        panel=page.locator('#source-dialog') if mobile or v==3 else page.locator('#source-dock' if v==1 else '#source-content')
        await panel.hover();await page.mouse.wheel(0,1400);await page.wait_for_timeout(180);await rec('source-scrolled')
        ret=page.locator(('[data-close="source-dialog"]' if mobile else '[data-close-source]') if v==1 else ('[data-close="source-dialog"]' if mobile else '#source-close') if v==2 else '#source-return')
        events.append({'event':'return-control-rect','rect':await ret.bounding_box(),'visible':await ret.is_visible()})
        await page.keyboard.press('Escape');await page.wait_for_timeout(100);await rec('escape-return')
        if mobile:await page.locator('#question').fill(DRAFT)
        # Keyboard reopening tests a citation's activation and return focus.
        await cite.focus();await cite.press('Enter');await rec('keyboard-open')
        if v==2:
            scope=page.locator('#source-dialog' if mobile else '#source-panel');await scope.locator('.source-nav button').nth(1).click();await rec('second-source')
            await scope.locator('[data-show-passage]').click();await rec('show-linked-paragraph')
            if not mobile:await close_source()
        elif v==3:
            await page.locator('#source-tabs button').nth(1).click();await rec('second-source');await close_source()
        else:await close_source()
        await page.locator('#stop').wait_for(state='hidden',timeout=20000);await rec('done-before-history',False)
        if v==1:
            if mobile:await page.locator('#menu').click();await page.locator('#history-dialog [data-new]').click()
            else:await page.locator('.sidebar [data-new]').click()
        elif v==2:await page.locator('[data-new]:visible').first.click()
        else:await page.locator('#new-mobile' if mobile else '#new-thread').click()
        await page.locator('#question').fill('Separate thread — should not replace the original draft.')
        if mobile:await page.locator('#menu' if v==1 else '#mobile-history' if v==2 else '#nav-open').click()
        else:
            if v==2:await page.locator('#history-search').fill('streets')
            if v==3:await page.locator('#thread-search').fill('streets')
        sel=('#mobile-history .history-item' if mobile else '#history-list .history-item') if v==1 else ('#mobile-threads .thread-button' if mobile else '#history .thread-button') if v==2 else '#history-list .history-item'
        await page.locator(sel).filter(has_text='How can cities').first.click();await page.wait_for_timeout(80);await rec('history-restored')
        await page.locator('#question').focus();await page.locator('#question').press('Control+End');await page.locator('#question').press('Shift+Enter');await page.locator('#question').press_sequentially('Keyboard continuation.');await rec('keyboard-draft')
        if not mobile:
            await page.locator('.inline-citation' if v==3 else '.citation').first.click();await page.set_viewport_size({'width':390,'height':844});await page.wait_for_timeout(120);await rec('resize-to-narrow')
    except Exception as e:
        events.append({'event':'HARNESS_OR_PRODUCT_FAILURE','error':str(e),'traceback':traceback.format_exc()})
        await page.screenshot(path=OUT/f'{label}-original-failure.png')
    (OUT/f'{label}.json').write_text(json.dumps({'events':events,'pageerrors':errors},ensure_ascii=False,indent=2));await c.close()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox'])
        await asyncio.gather(*(initial(b,v,m) for v in [1,2,3] for m in [False,True]))
        await asyncio.gather(*(final(b,v,m) for v in [1,2,3] for m in [False,True]))
        await b.close()
asyncio.run(main())
