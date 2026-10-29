from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import json,time,hashlib,traceback
out=Path(__file__).parent
results=[];errors=[]
def test(name,ok,detail=None):
 results.append({'name':name,'pass':bool(ok),'detail':detail});print(json.dumps(results[-1]),flush=True)
 if not ok:raise AssertionError(name)
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  page=b.new_page(viewport={'width':390,'height':844});page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:8767/app/')
  page.locator('.demo-badge').click();page.locator('#response-mode').select_option('fail');page.get_by_role('button',name='Close demo controls').click();page.locator('#question').fill('How do trees cool cities?');page.locator('#send').click()
  expect(page.get_by_role('button',name='Retry response',exact=True)).to_be_visible(timeout=5000)
  page.screenshot(path=str(out/'review-mobile-failure.png'))
  page.get_by_role('button',name='Retry response',exact=True).focus();page.keyboard.press('Enter')
  test('Keyboard retry moves focus to Stop',page.locator('#stop').evaluate('(e)=>e===document.activeElement'))
  expect(page.locator('.copy')).to_be_visible(timeout=12000)
  test('Completion returns focused Stop to composer',page.locator('#question').evaluate('(e)=>e===document.activeElement'))
  test('Completion does not promise storage per message',page.locator('.complete-label').inner_text()=='3 demo sources')
  page.locator('#question').fill('A second research question');page.locator('#send').click();page.wait_for_timeout(1100);page.reload()
  test('Reload during streaming recovers as stopped',page.locator('.resume').count()==1 and not page.locator('#stop').is_visible())
  page.locator('.resume').focus();page.keyboard.press('Enter');test('Keyboard Continue moves focus to Stop',page.locator('#stop').evaluate('(e)=>e===document.activeElement'))
  expect(page.locator('.message.answer').last.locator('.copy')).to_be_visible(timeout=12000)
  page.locator('#mobile-history').click();name=page.locator('#history-dialog [data-theme-toggle]').get_attribute('aria-label');test('Theme accessible name includes visible label','Appearance' in name)
  page.locator('#history-dialog [data-theme-toggle]').click();page.get_by_role('button',name='Close research history').click()
  page.locator('.demo-badge').click();page.locator('#response-mode').select_option('fail');page.get_by_role('button',name='Close demo controls').click();page.locator('#question').fill('Test another research route');page.locator('#send').click();expect(page.get_by_role('button',name='Retry response',exact=True)).to_be_visible(timeout=5000)
  page.screenshot(path=str(out/'review-mobile-dark-failure.png'))
  test('Dark mobile failure retains a visible Retry',page.get_by_role('button',name='Retry response',exact=True).is_visible() and page.locator('html').get_attribute('data-theme')=='dark')
  desktop=b.new_page(viewport={'width':1440,'height':900});desktop.on('pageerror',lambda e:errors.append(str(e)));desktop.goto('http://127.0.0.1:8767/app/');desktop.locator('#question').fill('How do urban trees help cities stay cool?');desktop.locator('#send').click();expect(desktop.locator('.copy')).to_be_visible(timeout=12000);desktop.locator('#reader').evaluate('(e)=>e.scrollTop=0');desktop.locator('.source-chip').first.click();desktop.screenshot(path=str(out/'review-desktop-source.png'))
  desktop.locator('#source-panel').evaluate('(e)=>e.scrollTop=500');close=desktop.locator('#source-close').bounding_box();test('Source close stays visible after source scrolling',close['y']>=72 and close['y']+close['height']<900,close)
  desktop.locator('#source-close').click();desktop.locator('#file-input').set_input_files({'name':'remove-me.txt','mimeType':'text/plain','buffer':b'text'});desktop.get_by_role('button',name='Remove remove-me.txt').click();test('Attachment chip removal works',desktop.locator('.attachment').count()==0)
  blocked=b.new_page(viewport={'width':390,'height':844});blocked.on('pageerror',lambda e:errors.append(str(e)));blocked.add_init_script("Storage.prototype.setItem=function(){throw new DOMException('blocked','QuotaExceededError')}")
  blocked.goto('http://127.0.0.1:8767/app/');test('Storage failure gives truthful in-tab fallback','unavailable' in blocked.locator('#composer-note').inner_text() and blocked.locator('.local-note small').inner_text()=='Kept in this tab')
  blocked.locator('#question').fill('A question retained in this tab');blocked.locator('#send').click();expect(blocked.locator('.copy')).to_be_visible(timeout=12000);test('Storage failure does not block conversation',blocked.locator('.message.user').count()==1)
  test('No uncaught browser errors after focused refinements',not errors,errors)
  b.close()
except Exception as e:
 print(traceback.format_exc());results.append({'name':'Runner completed','pass':False,'detail':str(e)})
finally:
 (out/'focus-review.json').write_text(json.dumps({'checks':results,'errors':errors,'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('app').glob('*') if f.is_file()}},indent=2));print('RESULT',sum(c['pass'] for c in results),'/',len(results),flush=True)
