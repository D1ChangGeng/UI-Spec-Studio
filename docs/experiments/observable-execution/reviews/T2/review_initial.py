import asyncio, json, os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
os.environ['FONTCONFIG_FILE']='/workspace/scratch/654b1ee6916f/ui-spec-fonts/fonts.conf'
os.environ['PLAYWRIGHT_BROWSERS_PATH']='/workspace/scratch/654b1ee6916f/ui-spec-browsers'
EXE='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell'

async def main():
    (ROOT/'captures').mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=EXE,headless=True,args=['--no-sandbox'])
        report={}
        for app,port in [('L6',8671),('N3',8672),('P8',8673)]:
            report[app]={}
            for size,w,h in [('desktop',1440,900),('mobile',390,844)]:
                ctx=await browser.new_context(viewport={'width':w,'height':h},device_scale_factor=1)
                page=await ctx.new_page()
                await page.goto(f'http://127.0.0.1:{port}/',wait_until='networkidle')
                await page.screenshot(path=str(ROOT/'captures'/f'{app}-{size}-initial.png'),full_page=True)
                report[app][size]={
                    'visible_text':await page.locator('body').inner_text(),
                    'buttons':await page.locator('button').evaluate_all('(els)=>els.map(e=>({text:e.innerText,aria:e.getAttribute("aria-label"),title:e.title}))'),
                    'inputs':await page.locator('input,textarea,select').evaluate_all('(els)=>els.map(e=>({tag:e.tagName,type:e.type,placeholder:e.placeholder,value:e.value,aria:e.getAttribute("aria-label")}))'),
                    'viewport':await page.evaluate('({width:innerWidth,height:innerHeight,scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight})')
                }
                await ctx.close()
        (ROOT/'initial-ui.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
        print(json.dumps(report,ensure_ascii=False,indent=2))
        await browser.close()

asyncio.run(main())
