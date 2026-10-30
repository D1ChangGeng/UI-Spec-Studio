import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).parent
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
        page=await b.new_page(viewport={'width':1440,'height':900})
        logs={'console':[],'responses':[],'failed':[],'errors':[]}
        page.on('console',lambda m:logs['console'].append({'type':m.type,'text':m.text}))
        page.on('response',lambda r:logs['responses'].append({'url':r.url,'status':r.status}))
        page.on('requestfailed',lambda r:logs['failed'].append({'url':r.url,'failure':r.failure}))
        page.on('pageerror',lambda e:logs['errors'].append(str(e)))
        await page.goto('http://127.0.0.1:8661',wait_until='networkidle')
        await page.wait_for_timeout(2000)
        logs['body']=await page.locator('body').inner_text()
        logs['scripts']=await page.locator('script').evaluate_all('(xs)=>xs.map(x=>({src:x.src,type:x.type}))')
        await page.screenshot(path=str(ROOT/'evidence/R7-desktop-reload.png'))
        (ROOT/'r7-loading-diagnostic.json').write_text(json.dumps(logs,indent=2,ensure_ascii=False))
        print(json.dumps(logs,indent=2,ensure_ascii=False))
        await b.close()
asyncio.run(main())
