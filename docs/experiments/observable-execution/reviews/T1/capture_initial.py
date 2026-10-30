import asyncio, json, os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).parent
OUT=ROOT/'evidence'
OUT.mkdir(exist_ok=True)
APPS={'R7':8661}
BROWSER='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell'

async def main():
    results={}
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=BROWSER,headless=True,args=['--no-sandbox'])
        for name,port in APPS.items():
            results[name]={}
            for size,width,height in [('desktop',1440,900),('mobile',390,844)]:
                context=await browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1)
                page=await context.new_page()
                errors=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                await page.goto(f'http://127.0.0.1:{port}',wait_until='networkidle')
                await page.screenshot(path=str(OUT/f'{name}-{size}-isolated-initial.png'))
                await page.screenshot(path=str(OUT/f'{name}-{size}-isolated-full.png'),full_page=True)
                results[name][size]=await page.evaluate('''() => ({
                  title:document.title, text:document.body.innerText,
                  scroll:{width:innerWidth,height:innerHeight,documentWidth:document.documentElement.scrollWidth,documentHeight:document.documentElement.scrollHeight},
                  controls:[...document.querySelectorAll('button,a,input,select,textarea')].map(e=>({tag:e.tagName,text:e.innerText,aria:e.getAttribute('aria-label'),placeholder:e.getAttribute('placeholder'),role:e.getAttribute('role'),type:e.type,href:e.getAttribute('href'),box:{x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height}})),
                  headings:[...document.querySelectorAll('h1,h2,h3')].map(e=>({tag:e.tagName,text:e.innerText,font:getComputedStyle(e).font,fontFamily:getComputedStyle(e).fontFamily,color:getComputedStyle(e).color,box:{x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height}}))
                })''')
                results[name][size]['page_errors']=errors
                await context.close()
        await browser.close()
    (ROOT/'r7_isolated_initial_measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    print(json.dumps(results,ensure_ascii=False,indent=2))

asyncio.run(main())
