import asyncio,json,hashlib,traceback
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent/'focused2';ROOT.mkdir(exist_ok=True)
log={'checks':[]}
def check(name,value,detail=None):
 log['checks'].append({'name':name,'pass':bool(value),'detail':detail});print(json.dumps(log['checks'][-1]),flush=True);assert value,name
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  for width,height in [(1440,900),(390,844)]:
   c=await b.new_context(viewport={'width':width,'height':height});page=await c.new_page();await page.goto('http://127.0.0.1:8844/app/')
   await page.locator('#demo-open-top').click();await page.locator('#next-response').select_option('long');await page.locator('#demo-done').click();await page.locator('[data-prompt]').first.click()
   await page.locator('.inline-citation').first.wait_for();await page.wait_for_timeout(1400)
   await page.locator('#question').fill('Keep this draft\nAnd its second line')
   await page.locator('.inline-citation').first.click();await page.wait_for_timeout(100)
   if width==1440:
    await page.locator('#reader').evaluate('el=>el.scrollTop=140');before=await page.locator('#reader').evaluate('el=>el.scrollTop');await page.wait_for_timeout(1100);after=await page.locator('#reader').evaluate('el=>el.scrollTop')
    check('Nonzero earlier position remains stable during source reading',before>100 and abs(before-after)<3,{'before':before,'after':after})
    await page.screenshot(path=str(ROOT/'desktop-source-held-position.png'))
    await page.locator('#source-return').click();await page.wait_for_timeout(100)
    check('Desktop close retains reading position',abs(before-await page.locator('#reader').evaluate('el=>el.scrollTop'))<3)
    await page.locator('.inline-citation').first.click()
   await page.locator('#source-dialog').evaluate('el=>el.scrollTop=500');await page.wait_for_timeout(100)
   visible=await page.locator('#source-return').evaluate("el=>{const r=el.getBoundingClientRect(),d=el.closest('dialog').getBoundingClientRect();return r.top>=d.top&&r.bottom<d.bottom}")
   check(f'{width}: Return remains visible deep in source',visible)
   await page.screenshot(path=str(ROOT/f'{width}-source-scrolled.png'))
   await page.locator('#source-return').click()
   check(f'{width}: Scrolled source returns with draft intact',await page.locator('#question').input_value()=='Keep this draft\nAnd its second line' and not await page.locator('#source-dialog').evaluate('el=>el.open'))
   await c.close()
  await b.close()
try:asyncio.run(main())
except Exception as e:log['failure']=str(e);log['traceback']=traceback.format_exc();print(log['traceback'])
finally:
 log['source_sha256']={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT.parent.parent.parent/'app').glob('*') if x.is_file()};(ROOT/'checks.json').write_text(json.dumps(log,indent=2))
