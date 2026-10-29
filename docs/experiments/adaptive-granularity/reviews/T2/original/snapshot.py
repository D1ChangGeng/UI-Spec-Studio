import asyncio, json, pathlib, os
from playwright.async_api import async_playwright
OUT=pathlib.Path(__file__).resolve().parent
CHROME='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell'
async def main():
    results=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox'])
        for i in range(1,4):
            for stage,off in [('initial',3),('final',0)]:
                for name,w,h in [('desktop',1440,900),('mobile',390,844)]:
                    c=await browser.new_context(viewport={'width':w,'height':h},color_scheme='light')
                    page=await c.new_page(); errors=[]
                    page.on('pageerror',lambda e:errors.append(str(e)))
                    await page.goto(f'http://127.0.0.1:{8080+i+off}')
                    await page.screenshot(path=OUT/f'v{i}-{stage}-{name}-welcome.png')
                    results.append({'variant':i,'stage':stage,'viewport':[w,h],'errors':errors,'title':await page.title(),'overflow':await page.evaluate('document.documentElement.scrollWidth > innerWidth')})
                    await c.close()
        await browser.close()
    (OUT/'snapshot-results.json').write_text(json.dumps(results,indent=2))
asyncio.run(main())
