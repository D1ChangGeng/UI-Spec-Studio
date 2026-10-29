import asyncio,json
from playwright.async_api import async_playwright
from pathlib import Path
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  page=await b.new_page(viewport={'width':1440,'height':900})
  await page.goto('http://127.0.0.1:8739/reference-project/')
  await page.screenshot(path='evidence/reference-conversation.png')
  await page.get_by_label('02 资料空间').check()
  await page.screenshot(path='evidence/reference-documents.png')
  print('Captured supplied reference conversation and document alternatives at 1440x900.')
  await b.close()
asyncio.run(main())
