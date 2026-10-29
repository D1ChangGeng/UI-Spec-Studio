import asyncio
from playwright.async_api import async_playwright
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  page=await b.new_page();page.on('pageerror',lambda e:print(str(e),flush=True));await page.goto('http://127.0.0.1:8739/app/');await page.wait_for_timeout(100);print(await page.evaluate('localStorage.getItem("meridian-workspace-v1")'));await b.close()
asyncio.run(main())
