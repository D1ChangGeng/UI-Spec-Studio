import asyncio,json,os,sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
os.environ['FONTCONFIG_FILE']='/workspace/scratch/654b1ee6916f/ui-spec-fonts/fonts.conf'
EXE='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell'

async def main():
    report=json.loads((ROOT/'operated-ui.json').read_text()) if (ROOT/'operated-ui.json').exists() else {}
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=EXE,headless=True,args=['--no-sandbox'])
        for app,port in [('L6',8671),('N3',8672),('P8',8673)]:
            if sys.argv[1:] and app not in sys.argv[1:]:
                continue
            report[app]={}
            for size,w,h in [('desktop',1440,900),('mobile',390,844)]:
                ctx=await browser.new_context(viewport={'width':w,'height':h})
                page=await ctx.new_page()
                await page.goto(f'http://127.0.0.1:{port}/',wait_until='networkidle')
                await page.get_by_role('button',name='Read your note ↗' if app=='N3' else 'Turn to your note').click()
                await page.wait_for_timeout(900)
                await page.screenshot(path=str(ROOT/'captures'/f'{app}-{size}-back.png'),full_page=True)
                report[app][size]={'back_text':await page.locator('body').inner_text(),'flip_active':await page.evaluate('({tag:document.activeElement.tagName,text:document.activeElement.innerText,id:document.activeElement.id})')}
                report[app][size]['ui_elements']=await page.locator('button,article,textarea,dialog,details,summary').evaluate_all('(els)=>els.map(e=>({tag:e.tagName,id:e.id,class:e.className,text:e.innerText,aria:e.getAttribute("aria-label"),rect:{x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height}}))')
                await page.get_by_role('button',name='Saved note',exact=True).click()
                await page.wait_for_timeout(400)
                await page.screenshot(path=str(ROOT/'captures'/f'{app}-{size}-saved-dialog.png'),full_page=True)
                report[app][size]['dialog_text']=await page.locator('body').inner_text()
                await page.get_by_role('button',name='Return to editing',exact=True).click()
                await page.wait_for_timeout(400)
                report[app][size]['return_active']=await page.evaluate('({tag:document.activeElement.tagName,id:document.activeElement.id,selectionStart:document.activeElement.selectionStart,selectionEnd:document.activeElement.selectionEnd})')
                if size=='mobile':
                    await page.get_by_role('button',name='中文 · 切换中文',exact=True).click()
                    await page.locator('button').filter(has_text='◐').click()
                    await page.wait_for_timeout(500)
                    await page.screenshot(path=str(ROOT/'captures'/f'{app}-mobile-zh-dark.png'),full_page=True)
                    report[app][size]['zh_dark_text']=await page.locator('body').inner_text()
                (ROOT/'operated-ui.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
                await ctx.close()
        (ROOT/'operated-ui.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
        print(json.dumps(report,ensure_ascii=False,indent=2))
        await browser.close()

asyncio.run(main())
