from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import json,time,traceback,hashlib
out=Path(__file__).parent;results=[];frames=[];errors=[];start=time.monotonic()
def test(name,ok,detail=None):
 results.append({'name':name,'pass':bool(ok),'detail':detail});print(json.dumps(results[-1]),flush=True)
 if not ok:raise AssertionError(name)
def shot(page,name):
 a=time.monotonic()-start;page.screenshot(path=str(out/(name+'.png')));frames.append({'file':name+'.png','seconds':[round(a,3),round(time.monotonic()-start,3)]})
def long_question(page):
 page.locator('.demo-badge').click();page.locator('#response-mode').select_option('long');page.get_by_role('button',name='Close demo controls').click();page.locator('#question').fill('How do urban trees help cities stay cool?');page.locator('#send').click();expect(page.locator('.citation').first).to_be_visible(timeout=7000)
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  page=b.new_page(viewport={'width':1440,'height':900});page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:8767/app/');long_question(page)
  page.locator('#question').fill('A follow-up I am keeping.');page.locator('.citation').first.click();page.wait_for_timeout(80)
  test('Source opens while the long answer is still streaming',page.locator('#stop').is_visible() and page.locator('#source-panel').is_visible())
  test('Answer paragraph and synthetic source passage are identified',page.locator('.cited-paragraph').count()==1 and page.locator('#source-panel .source-excerpt').is_visible())
  shot(page,'desktop-01-open-stream')
  page.locator('#reader').evaluate('(e)=>e.scrollTop=220');page.wait_for_timeout(80);a=page.locator('#reader').evaluate('(e)=>e.scrollTop');page.wait_for_timeout(900);z=page.locator('#reader').evaluate('(e)=>e.scrollTop')
  test('New output leaves the reader-held position unchanged',abs(a-z)<2,{'before':a,'after':z})
  page.locator('#question').fill('\n'.join(['A growing draft while reading a source']*7));page.wait_for_timeout(100);z2=page.locator('#reader').evaluate('(e)=>e.scrollTop')
  test('Composer growth retains reading position and reachable controls',abs(z-z2)<2 and page.locator('#stop').bounding_box()['y']<900,{'before':z,'after':z2})
  shot(page,'desktop-02-grown-composer')
  page.locator('#source-panel [data-source-action]').click();test('Stop works while keeping the source open',not page.locator('#stop').is_visible() and page.locator('#source-panel').is_visible() and page.locator('#source-panel [data-source-action]').inner_text()=='Continue answer')
  shot(page,'desktop-03-stopped')
  page.locator('#source-panel [data-source-action]').click();test('Continue works inside the open reader',page.locator('#stop').is_visible() and page.locator('#source-panel').is_visible())
  expect(page.locator('.copy')).to_be_visible(timeout=15000)
  page.locator('#source-panel [data-source-action]').click();test('Retry restarts the answer without closing the source',page.locator('#stop').is_visible() and page.locator('#source-panel').is_visible() and page.locator('.message.user').count()==1)
  page.wait_for_timeout(1000);page.locator('#source-panel [data-source-action]').click();shot(page,'desktop-04-retry-stopped')
  draft=page.locator('#question').input_value();before=page.locator('#reader').evaluate('(e)=>e.scrollTop');page.locator('#source-close').click();page.wait_for_timeout(100);after=page.locator('#reader').evaluate('(e)=>e.scrollTop')
  test('Closing returns to same draft and reading offset',draft==page.locator('#question').input_value() and abs(before-after)<2,{'before':before,'after':after})
  test('The last inspected paragraph remains identifiable',page.locator('.cited-paragraph').count()==1)
  page.locator('.resume').click();expect(page.locator('.citation').first).to_be_visible(timeout=7000);page.locator('.citation').first.click();page.locator('#reader').evaluate('(e)=>e.scrollTop=0');page.locator('#jump-latest').click();page.wait_for_timeout(350)
  gap=page.locator('#reader').evaluate('(e)=>e.scrollHeight-e.scrollTop-e.clientHeight');test('Back to latest opts back into following with panel open',gap<3,{'bottom_gap':gap})
  page.locator('[data-theme-toggle]').first.click();shot(page,'desktop-05-dark-panel');page.locator('#source-panel [data-source-action]').click()
  phone=b.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);phone.on('pageerror',lambda e:errors.append(str(e)));phone.goto('http://127.0.0.1:8767/app/');long_question(phone);phone.locator('#question').fill('My phone draft stays here.');phone.locator('.citation').first.click()
  test('Phone source is a focused native modal during streaming',phone.locator('#source-dialog').evaluate('(e)=>e.matches(":modal")') and phone.locator('#source-dialog [data-source-action]').inner_text()=='Stop answer')
  shot(phone,'phone-01-open-stream');phone.locator('#source-dialog [data-source-action]').click()
  test('Phone Stop stays in source view',phone.locator('#source-dialog').evaluate('(e)=>e.open') and phone.locator('#source-dialog [data-source-action]').inner_text()=='Continue answer')
  shot(phone,'phone-02-stopped');phone.locator('#source-dialog [data-source-action]').click();expect(phone.locator('#source-dialog [data-source-action]')).to_have_text('Retry answer',timeout=15000)
  phone.locator('#source-dialog [data-source-action]').click();test('Phone Retry preserves modal and source passage',phone.locator('#source-dialog').evaluate('(e)=>e.open') and phone.locator('#source-dialog .source-excerpt').is_visible())
  phone.wait_for_timeout(1000);phone.locator('#source-dialog [data-source-action]').click();before=phone.locator('#reader').evaluate('(e)=>e.scrollTop');phone.get_by_role('button',name='Back to answer',exact=True).click();phone.wait_for_timeout(120);after=phone.locator('#reader').evaluate('(e)=>e.scrollTop')
  test('Phone explicit return retains draft and reading position',phone.locator('#question').input_value()=='My phone draft stays here.' and abs(before-after)<2,{'before':before,'after':after})
  shot(phone,'phone-03-return');phone.locator('#mobile-history').click();phone.locator('#history-dialog [data-theme-toggle]').click();phone.get_by_role('button',name='Close research history').click();phone.locator('.resume').click();expect(phone.locator('.citation').first).to_be_visible(timeout=7000);phone.locator('.citation').first.click();shot(phone,'phone-04-dark-source');phone.keyboard.press('Escape')
  test('Escape closes phone source and returns focus',not phone.locator('#source-dialog').evaluate('(e)=>e.open') and phone.locator('.citation').first.evaluate('(e)=>e===document.activeElement'))
  test('No horizontal overflow at either target viewport',page.evaluate('document.documentElement.scrollWidth<=innerWidth') and phone.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  test('No uncaught browser errors',not errors,errors)
  b.close()
except Exception as e:
 print(traceback.format_exc(),flush=True);results.append({'name':'Runner completed','pass':False,'detail':str(e)})
finally:
 (out/'checks.json').write_text(json.dumps({'checks':results,'frames':frames,'errors':errors,'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('app').glob('*') if f.is_file()},'conditions':'Chromium 143, 1440x900 desktop and 390x844 phone emulation, scale 1. Ordered captures with monotonic time brackets; not continuous playback.'},indent=2));print('RESULT',sum(x['pass'] for x in results),'/',len(results),flush=True)
