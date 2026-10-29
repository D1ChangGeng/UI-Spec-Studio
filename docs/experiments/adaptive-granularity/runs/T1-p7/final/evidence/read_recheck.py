import asyncio,json
from playwright.async_api import async_playwright
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  pg=await b.new_page();await pg.add_init_script("window.originalGet=Storage.prototype.getItem;Storage.prototype.getItem=function(){throw new DOMException('Access blocked','SecurityError')};")
  await pg.goto('http://localhost:8777');await pg.locator('#note-title').fill('Read recovery draft');await pg.evaluate('() => {Storage.prototype.getItem=window.originalGet;}');await pg.locator('#retry').click();r={'check':'read retry preserves and durably stores draft, reenables save','pass':await pg.locator('#note-title').input_value()=='Read recovery draft' and not await pg.locator('#save').is_disabled() and await pg.evaluate("JSON.parse(localStorage.getItem('leafnote-drafts-v2')).new.title")=='Read recovery draft'}
  await pg.screenshot(path='evidence/final/read-recovery.png');print(json.dumps(r));open('evidence/final/read-recheck.json','w').write(json.dumps(r,indent=2));await b.close()
asyncio.run(main())
