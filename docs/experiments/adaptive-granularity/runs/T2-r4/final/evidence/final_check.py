import asyncio,json,hashlib,time
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent/'final3';ROOT.mkdir(exist_ok=True)
async def main():
  log=[]
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
    page=await b.new_page(viewport={'width':1440,'height':900},color_scheme='light')
    await page.goto('http://127.0.0.1:8844/app/')
    await page.screenshot(path=str(ROOT/'desktop-welcome.png'))
    await page.locator('[data-example=heat]').click()
    await page.locator('#reader').evaluate('el=>el.scrollTop=0')
    await page.wait_for_timeout(100)
    await page.screenshot(path=str(ROOT/'desktop-reading.png'))
    await page.locator('.source-chip').first.click()
    await page.screenshot(path=str(ROOT/'desktop-source.png'))
    await page.locator('#source-close').click()
    await page.locator('#theme').click()
    await page.screenshot(path=str(ROOT/'desktop-dark.png'))
    await page.locator('#theme').click()
    await page.set_viewport_size({'width':390,'height':844})
    await page.locator('#reader').evaluate('el=>el.scrollTop=0')
    await page.wait_for_timeout(100)
    await page.screenshot(path=str(ROOT/'mobile-reading.png'))
    await page.locator('#new-mobile').click()
    result=not await page.locator('#latest').is_visible() and await page.locator('#feedback').inner_text()==''
    log.append({'check':'New thread clears prior latest action and status','pass':result});assert result
    await page.screenshot(path=str(ROOT/'mobile-welcome.png'))
    await page.locator('#question').fill('Test interruption ownership')
    await page.locator('#demo-open-top').click();await page.locator('#next-response').select_option('slow');await page.locator('#demo-done').click()
    await page.locator('#send').click()
    await page.locator('#new-mobile').click()
    await page.wait_for_timeout(2600)
    result=await page.locator('.answer').count()==0 and not await page.locator('#stop').is_visible()
    log.append({'check':'New thread cancels stale pending completion','pass':result});assert result
    await page.locator('#nav-open').click();await page.locator('.history-item',has_text='Test interruption ownership').click()
    result=await page.locator('.answer').get_attribute('data-status')=='stopped'
    log.append({'check':'Interrupted old thread remains recoverable','pass':result});assert result
    await page.locator('.answer-state button').click()
    await page.wait_for_function("document.querySelector('.answer')?.dataset.status==='complete'",timeout=15000)
    result=await page.locator('.message.user').count()==1
    log.append({'check':'Interrupted thread retry retains single question','pass':result});assert result
    await b.close()
  (ROOT/'checks.json').write_text(json.dumps({'checks':log,'source_sha256':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT.parent.parent/'app').glob('*') if x.is_file()}},indent=2))
  print(json.dumps(log,indent=2))
asyncio.run(main())
