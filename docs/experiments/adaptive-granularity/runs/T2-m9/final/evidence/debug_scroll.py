import asyncio,json
from playwright.async_api import async_playwright
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  page=await b.new_page(viewport={'width':1440,'height':900});await page.goto('http://127.0.0.1:8739/app/')
  await page.locator('#question').fill('How can cities make streets cooler in summer?');await page.locator('#question').press('Enter');await page.wait_for_timeout(1650);await page.locator('#question').fill('A follow-up draft stays here');await page.locator('#stop').click();await page.wait_for_timeout(600);await page.get_by_role('button',name='Continue response').click();await page.wait_for_timeout(1300)
  print('before',await page.locator('#reader').evaluate('(e)=>({top:e.scrollTop,height:e.scrollHeight,client:e.clientHeight})'))
  print('set',await page.locator('#reader').evaluate('(e)=>{e.scrollTop=0;return {top:e.scrollTop,height:e.scrollHeight,client:e.clientHeight}}'))
  for i in range(7):
   await page.wait_for_timeout(200);print(i,await page.locator('#reader').evaluate('(e)=>({top:e.scrollTop,height:e.scrollHeight,client:e.clientHeight})'))
  await b.close()
asyncio.run(main())
