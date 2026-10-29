import asyncio, json, time
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
CHROME='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell'

async def main():
    out=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
        for name,url in [('supplied','http://127.0.0.1:8844/reference-project/'),('assistant-ui','https://www.assistant-ui.com/demos/chatgpt'),('sidebar-01','https://ui.shadcn.com/view/new-york-v4/sidebar-01')]:
            page=await b.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
            r={'name':name,'url':url,'viewport':[1440,900]}
            try:
                await page.goto(url,wait_until='domcontentloaded',timeout=20000)
                await page.wait_for_timeout(1600)
                await page.screenshot(path=str(ROOT/'references'/f'{name}.png'))
                r['title']=await page.title();r['capture']=f'references/{name}.png'
                if name=='supplied':
                    await page.locator('#question').fill('城市供热如何降低高峰负荷？')
                    await page.locator('#send').click()
                    await page.wait_for_timeout(500)
                    await page.screenshot(path=str(ROOT/'references'/'supplied-active.png'))
                    await page.get_by_text('查看演示来源 01',exact=True).click()
                    await page.screenshot(path=str(ROOT/'references'/'supplied-source.png'))
                    r['operated']='Question, response, source modal; no upstream AI request submitted.'
            except Exception as e:r['error']=str(e)
            out.append(r);await page.close()
        await b.close()
    (ROOT/'references'/'acquisition.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))

asyncio.run(main())
