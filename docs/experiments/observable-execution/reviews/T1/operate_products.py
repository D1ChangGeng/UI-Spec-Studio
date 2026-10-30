import asyncio,json,re,traceback
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).parent
OUT=ROOT/'evidence'
APPS={'T4':8662,'M2':8663}
BROWSER='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell'
LONG='Keeping your place when everything around you is changing'

async def state(page):
    return await page.evaluate('''() => ({url:location.href,scrollY,body:document.body.innerText,active:{tag:document.activeElement.tagName,text:document.activeElement.innerText,aria:document.activeElement.getAttribute('aria-label')},controls:[...document.querySelectorAll('a,button,input,select')].map(e=>({tag:e.tagName,text:e.innerText,aria:e.getAttribute('aria-label'),href:e.getAttribute('href'),value:e.value,pressed:e.getAttribute('aria-pressed')}))})''')

async def main():
    results={}
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=BROWSER,args=['--no-sandbox'])
        for name,port in APPS.items():
            results[name]={}
            for size,w,h in [('desktop',1440,900),('mobile',390,844)]:
                r={};results[name][size]=r
                c=await b.new_context(viewport={'width':w,'height':h})
                page=await c.new_page()
                try:
                    await page.goto(f'http://127.0.0.1:{port}',wait_until='networkidle')
                    search=page.get_by_role('searchbox')
                    await search.fill('light')
                    r['search_light']=await state(page)
                    await page.screenshot(path=str(OUT/f'{name}-{size}-search-light.png'))
                    await search.fill('zzzz-no-result-2849')
                    r['no_results']=await state(page)
                    await page.screenshot(path=str(OUT/f'{name}-{size}-empty.png'))
                    await search.fill('')
                    await page.get_by_role('button',name='Save '+LONG,exact=True).click()
                    r['saved_before_reload']=await state(page)
                    await page.reload(wait_until='networkidle')
                    r['saved_after_reload']=await state(page)
                    await page.get_by_role('button',name=re.compile(r'^Saved')).click()
                    await page.get_by_role('searchbox').fill('place')
                    r['saved_filtered_list']=await state(page)
                    link=page.locator('a').filter(has_text=LONG)
                    await link.click()
                    await page.wait_for_timeout(100)
                    r['detail_open']=await state(page)
                    await page.screenshot(path=str(OUT/f'{name}-{size}-detail-top.png'))
                    await page.screenshot(path=str(OUT/f'{name}-{size}-detail-full.png'),full_page=True)
                    await page.evaluate('window.scrollTo(0,550)')
                    await page.wait_for_timeout(100)
                    r['reading']=await state(page)
                    await page.screenshot(path=str(OUT/f'{name}-{size}-detail-reading.png'))
                    candidates=page.get_by_role('button',name=re.compile(r'Back|collection',re.I))
                    if await candidates.count():
                        await candidates.first.click()
                        r['return_action']='button'
                    else:
                        candidates=page.get_by_role('link',name=re.compile(r'Back to|All collections',re.I))
                        await candidates.first.click()
                        r['return_action']='link'
                    await page.wait_for_timeout(100)
                    r['returned_list']=await state(page)
                    await page.locator('a').filter(has_text=LONG).click()
                    await page.wait_for_timeout(100)
                    r['reopened_detail']=await state(page)
                    await page.screenshot(path=str(OUT/f'{name}-{size}-detail-reopened.png'))
                    await page.go_back(wait_until='networkidle')
                    await page.wait_for_timeout(100)
                    r['browser_back']=await state(page)
                except Exception as e:
                    r['failure']={'exception':str(e),'traceback':traceback.format_exc(),'state':await state(page)}
                    await page.screenshot(path=str(OUT/f'{name}-{size}-operation-failure.png'))
                finally:
                    await c.close()
                    (ROOT/'operation_measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
        await b.close()
    print(json.dumps({n:{s:{k:({'url':v.get('url'),'scrollY':v.get('scrollY'),'active':v.get('active')} if isinstance(v,dict) and 'url' in v else v) for k,v in d.items()} for s,d in x.items()} for n,x in results.items()},ensure_ascii=False,indent=2))

asyncio.run(main())
