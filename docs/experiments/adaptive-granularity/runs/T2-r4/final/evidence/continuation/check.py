import asyncio,json,time,traceback,hashlib
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parent
log={'checks':[],'captures':[],'errors':[],'external_requests':[]};start=time.monotonic()
def check(name,value,detail=None):
 r={'name':name,'pass':bool(value),'elapsed_s':round(time.monotonic()-start,3),'detail':detail};log['checks'].append(r);print(json.dumps(r),flush=True);assert value,name
async def shot(page,name):
 t=time.monotonic()-start;await page.screenshot(path=str(ROOT/(name+'.png')));log['captures'].append({'file':name+'.png','start_s':round(t,3),'end_s':round(time.monotonic()-start,3)})
async def begin(page):
 await page.locator('#demo-open-top').click();await page.locator('#next-response').select_option('long');await page.locator('#demo-done').click();await page.locator('#question').fill('How can cities cool down without using more energy?');await page.locator('#question').press('Enter')
 await page.locator('.inline-citation').first.wait_for(timeout=15000)
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  for width,height in [(1440,900),(390,844)]:
   c=await b.new_context(viewport={'width':width,'height':height},color_scheme='light');page=await c.new_page();page.on('pageerror',lambda e:log['errors'].append(str(e)));page.on('request',lambda r:log['external_requests'].append(r.url) if not r.url.startswith('http://127.0.0.1:8844/') else None)
   await page.goto('http://127.0.0.1:8844/app/');await begin(page)
   check(f'{width}: Inline citation arrives before answer completion',await page.locator('.answer').get_attribute('data-status')=='streaming')
   await shot(page,f'{width}-01-citation-arrives')
   paragraph=await page.locator('.inline-citation').first.evaluate('el=>el.parentElement.textContent')
   await page.locator('.inline-citation').first.click()
   await page.wait_for_timeout(100)
   check(f'{width}: Cited paragraph is highlighted',await page.locator('.cited-paragraph').count()==1)
   context=await page.locator('#source-context').inner_text()
   check(f'{width}: Reader identifies the actual cited paragraph',context in paragraph and len(context)>50)
   check(f'{width}: Source is readable during streaming',await page.locator('#source-dialog').evaluate('el=>el.open') and await page.locator('#source-generation-action').inner_text()=='Stop response')
   await shot(page,f'{width}-02-source-while-streaming')
   if width==1440:
    check('Desktop companion is non-modal',await page.locator('#source-dialog').evaluate("el=>!el.matches(':modal')"))
    await page.locator('#reader').evaluate('el=>el.scrollTop=80')
    before=await page.locator('#reader').evaluate('el=>el.scrollTop');await page.wait_for_timeout(900);after=await page.locator('#reader').evaluate('el=>el.scrollTop')
    check('Source reading is not pulled by arriving text',abs(before-after)<3,{'before':before,'after':after})
    await page.locator('#question').fill('Compare two possible routes\nKeep the assumptions visible\nInclude maintenance needs\nAnd a practical pilot\nWhat would you measure first?')
    check('Composer grows beside source',await page.locator('#question').evaluate('el=>el.clientHeight')>90)
    check('Composer growth preserves earlier reading point',abs(before-await page.locator('#reader').evaluate('el=>el.scrollTop'))<3)
    await shot(page,'1440-03-expanded-composer')
   else:
    check('Compact source has native modal semantics',await page.locator('#source-dialog').evaluate("el=>el.matches(':modal')"))
   await page.locator('#source-generation-action').click()
   check(f'{width}: Stop works inside source view',await page.locator('.answer').get_attribute('data-status')=='stopped' and await page.locator('#source-generation-action').inner_text()=='Try again')
   frozen=await page.locator('.answer-content').inner_text();await page.wait_for_timeout(500)
   check(f'{width}: Stop prevents further text',await page.locator('.answer-content').inner_text()==frozen)
   await shot(page,f'{width}-04-source-stopped')
   await page.locator('#source-generation-action').click()
   check(f'{width}: Retry retains source view',await page.locator('#source-dialog').evaluate('el=>el.open'))
   check(f'{width}: Retry retains cited text',await page.locator('#source-context').inner_text()==context)
   check(f'{width}: Retry does not duplicate question',await page.locator('.message.user').count()==1)
   await page.locator('.inline-citation').first.wait_for(timeout=15000)
   await shot(page,f'{width}-05-source-retrying')
   await page.locator('#source-return').click();await page.wait_for_timeout(100)
   check(f'{width}: Explicit return closes source',not await page.locator('#source-dialog').evaluate('el=>el.open'))
   check(f'{width}: Return resolves regenerated citation focus',await page.evaluate("document.activeElement.classList.contains('inline-citation')"))
   if width==1440:check('Draft survives source stop/retry/return',await page.locator('#question').input_value()=='Compare two possible routes\nKeep the assumptions visible\nInclude maintenance needs\nAnd a practical pilot\nWhat would you measure first?')
   await page.locator('#reader').evaluate('el=>el.scrollTop=0');await page.wait_for_timeout(900)
   check(f'{width}: Scroll back remains under user control',await page.locator('#reader').evaluate('el=>el.scrollTop')==0)
   check(f'{width}: Latest is reachable',await page.locator('#latest').is_visible())
   await page.locator('#latest').click()
   check(f'{width}: Latest reaches current output',await page.locator('#reader').evaluate('el=>el.scrollHeight-el.scrollTop-el.clientHeight<3'))
   await page.locator('.inline-citation').first.click();await page.keyboard.press('Escape');await page.wait_for_timeout(100)
   check(f'{width}: Escape returns safely',not await page.locator('#source-dialog').evaluate('el=>el.open') and await page.evaluate("document.activeElement.classList.contains('inline-citation')"))
   await page.wait_for_function("document.querySelector('.answer')?.dataset.status==='complete'",timeout=20000)
   check(f'{width}: Retried long answer completes',len((await page.locator('.answer-content').inner_text()).split())>500)
   await page.locator('.inline-citation').first.click()
   if width==1440:await page.locator('#theme').click()
   await shot(page,f'{width}-06-completed-source')
   check(f'{width}: No page horizontal overflow',await page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
   await c.close()
  check('No runtime errors',not log['errors'],log['errors']);check('No external application requests',not log['external_requests'],log['external_requests']);await b.close()
try:asyncio.run(main())
except Exception as e:log['failure']=str(e);log['traceback']=traceback.format_exc();print(log['traceback'])
finally:
 log['source_sha256']={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT.parent.parent/'app').glob('*') if x.is_file()};(ROOT/'run-1.json').write_text(json.dumps(log,indent=2))
