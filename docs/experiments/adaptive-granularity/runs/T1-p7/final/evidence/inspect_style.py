import asyncio,json
from playwright.async_api import async_playwright
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  page=await b.new_page();await page.goto('http://localhost:8777');await page.wait_for_timeout(500)
  print(await page.evaluate("JSON.stringify(['html','.brand','#save','#new-note'].map(s=>{const e=document.querySelector(s),c=getComputedStyle(e);return {s,color:c.color,bg:c.backgroundColor,ink:c.getPropertyValue('--ink'),accent:c.getPropertyValue('--accent'),primary:c.getPropertyValue('--pico-primary-background'),pbg:c.getPropertyValue('--pico-background-color')}}))"))
  print(await page.evaluate("document.styleSheets[1].cssRules.length"))
  print(await page.evaluate("[...document.styleSheets[1].cssRules].slice(-8).map(x=>x.cssText).join('\\n')"))
  await b.close()
asyncio.run(main())
