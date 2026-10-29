import asyncio,os,json
from playwright.async_api import async_playwright
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  page=await b.new_page(viewport={'width':1440,'height':900},ignore_https_errors=True)
  for name,url,scroll in [('simplenote-workspace','https://simplenote.com/',740),('mail-v3','https://v3.shadcn.com/examples/mail',450),('pico-modal','https://picocss.com/docs/modal',450)]:
   try:
    await page.goto(url,wait_until='domcontentloaded',timeout=25000)
    await page.wait_for_timeout(600)
    await page.evaluate('(y)=>window.scrollTo(0,y)',scroll)
    await page.screenshot(path=f'evidence/research-{name}.png')
    print(name,await page.title())
   except Exception as e:print(name,str(e))
  await b.close()
asyncio.run(main())
