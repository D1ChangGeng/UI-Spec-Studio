import asyncio,json,hashlib
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent/'final4';ROOT.mkdir(exist_ok=True)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
    page=await b.new_page(viewport={'width':1440,'height':900},color_scheme='light')
    await page.goto('http://127.0.0.1:8844/app/')
    await page.locator('#demo-open-top').click();await page.locator('#next-response').select_option('long');await page.locator('#demo-done').click()
    await page.locator('#question').fill('How can cities keep their cool?');await page.locator('#question').press('Enter')
    await page.wait_for_function("document.querySelector('.answer')?.dataset.status==='complete'",timeout=25000)
    text=await page.locator('.answer-content').inner_text()
    metrics=await page.locator('#reader').evaluate('el=>({height:el.scrollHeight,viewport:el.clientHeight})')
    result={'complete':True,'words':len(text.split()),'reading':metrics,'no_test_instruction_copy':'test sustained reading' not in text,'composer_reachable':await page.locator('#composer').evaluate('el=>el.getBoundingClientRect().bottom<=innerHeight')}
    assert result['no_test_instruction_copy'] and result['composer_reachable'] and metrics['height']>metrics['viewport']*2
    await page.screenshot(path=str(ROOT/'long-answer-complete.png'))
    await page.locator('#reader').evaluate('el=>el.scrollTop=850')
    await page.screenshot(path=str(ROOT/'long-answer-middle.png'))
    result['source_sha256']={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT.parent.parent/'app').glob('*') if x.is_file()}
    (ROOT/'checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));await b.close()
asyncio.run(main())
