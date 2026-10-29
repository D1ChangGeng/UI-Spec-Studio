import asyncio,json,time,traceback
from pathlib import Path
from playwright.async_api import async_playwright
out=Path('evidence');checks=[];frames=[]
def check(name,ok,detail=None):
 checks.append({'name':name,'pass':bool(ok),'detail':detail});print(json.dumps(checks[-1]),flush=True)
async def capture(page,name):
 start=time.time();await page.screenshot(path=str(out/name));frames.append({'file':name,'capture_started_unix':start,'capture_finished_unix':time.time(),'viewport':page.viewport_size})
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  page=await b.new_page(viewport={'width':1440,'height':900})
  await page.goto('http://127.0.0.1:8739/app/');await capture(page,'final-desktop-home.png')
  await page.locator('#history-list .history-item').filter(has_text='Streets that stay cool').click();await page.wait_for_timeout(100)
  await page.locator('#reader').evaluate('(el)=>el.scrollTop=260');old=await page.locator('#reader').evaluate('(el)=>el.scrollTop')
  await page.locator('#question').fill('A draft for this thread');await page.locator('#history-list .history-item').filter(has_text='Making room').click();await page.locator('#history-list .history-item').filter(has_text='Streets that stay cool').click();await page.wait_for_timeout(100)
  check('history returns to stored reading position',await page.locator('#reader').evaluate('(el)=>el.scrollTop')==old,{'expected':old,'actual':await page.locator('#reader').evaluate('(el)=>el.scrollTop')})
  check('history preserves per-thread draft',await page.locator('#question').input_value()=='A draft for this thread')
  await page.locator('#question').fill('How could we compare two street designs?');await page.locator('#question').press('Enter');await page.wait_for_timeout(1000)
  await page.locator('#reader').evaluate('(el)=>el.scrollTop=180');before=await page.locator('#reader').evaluate('(el)=>({top:el.scrollTop,height:el.scrollHeight,client:el.clientHeight})');await capture(page,'continuity-01-reading-older.png');await page.wait_for_timeout(2200);after=await page.locator('#reader').evaluate('(el)=>({top:el.scrollTop,height:el.scrollHeight,client:el.clientHeight})');await capture(page,'continuity-02-new-content-below.png')
  check('reading stays fixed while an overflowing answer grows',abs(before['top']-after['top'])<1 and after['height']>before['height'] and before['height']>before['client'],{'before':before,'after':after})
  check('back-to-latest offered',await page.locator('#latest').is_visible());await page.locator('#latest').click();await page.locator('#stop').click();partial=await page.locator('.answer').last.inner_text();await capture(page,'continuity-03-stopped.png')
  await page.get_by_role('button',name='Continue response').click();await page.wait_for_timeout(50);resumed=await page.locator('.answer').last.inner_text();check('continue preserves already-written opening',partial.split('Response stopped')[0].strip() in resumed)
  await capture(page,'continuity-04-resumed.png');await page.wait_for_function('document.querySelector("#stop").hidden',timeout=15000);await capture(page,'final-desktop-complete.png')
  await page.locator('.source-button').last.click();await capture(page,'final-desktop-source.png');await page.locator('[data-close-source]').click()
  await page.locator('#theme').click();await capture(page,'final-desktop-dark.png');await page.locator('#theme').click()
  await page.set_viewport_size({'width':390,'height':844});await page.locator('#menu').click();await page.locator('#history-dialog [data-new]').click();await page.wait_for_timeout(100);await capture(page,'final-mobile-home.png');check('new thread starts at reader top',await page.locator('#reader').evaluate('(el)=>el.scrollTop')==0)
  await page.locator('#question').fill('line one');await page.locator('#question').press('Shift+Enter');await page.locator('#question').press('x');check('Shift+Enter inserts a newline',await page.locator('#question').input_value()=='line one\nx')
  await page.locator('#question').fill('A focused research question');await page.locator('#question').press('Enter');await page.wait_for_timeout(1000);await page.reload();check('reload interrupts unfinished generation safely',await page.get_by_role('button',name='Continue response').is_visible());await page.get_by_role('button',name='Continue response').click();await page.wait_for_function('document.querySelector("#stop").hidden',timeout=15000);await page.locator('#reader').evaluate('(el)=>el.scrollTop=0');await capture(page,'final-mobile-answer.png');await page.locator('.source-button').first.click();await capture(page,'final-mobile-source.png');await page.keyboard.press('Escape');check('mobile source native focus return',await page.evaluate('document.activeElement.classList.contains("source-button")'))
  await page.locator('#mobile-theme').click();await page.locator('#reader').evaluate('(el)=>el.scrollTop=0');await capture(page,'final-mobile-dark.png')
  await page.set_viewport_size({'width':390,'height':500});await page.locator('#question').fill('\n'.join(['Long context']*10));check('short-height send stays inside viewport',await page.locator('#send').evaluate('(el)=>el.getBoundingClientRect().bottom<=innerHeight'));await capture(page,'short-height.png')
  await b.close()
try:asyncio.run(main())
except Exception:checks.append({'name':'exception','pass':False,'detail':traceback.format_exc()});print(traceback.format_exc())
finally:out.joinpath('continuity-results.json').write_text(json.dumps({'checks':checks,'frames':frames},indent=2));print('RESULT',sum(c['pass'] for c in checks),'/',len(checks))
