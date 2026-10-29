from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import os,json,time,traceback
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
ROOT=Path(__file__).resolve().parent
URL='http://127.0.0.1:8844/'
KEY='leafnote-notebook-v2'
checks=[]
def check(name,fn):
 try:fn();checks.append({'test':name,'result':'PASS'});print('PASS',name,flush=True)
 except Exception as e:checks.append({'test':name,'result':'FAIL','error':str(e)});print('FAIL',name,str(e),flush=True)
def shot(page,name):page.screenshot(path=str(ROOT/(name+'.png')))
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL);shot(page,'trial-empty-desktop')
 check('Fresh notebook is empty',lambda:expect(page.locator('.note-row')).to_have_count(0))
 page.locator('#samples').click();shot(page,'trial-desktop-en-light')
 check('Explicit sample loading stores four records',lambda:expect(page.locator('.note-row')).to_have_count(4))
 page.locator('#new-note').click();page.locator('#note-title').fill('Heat, shade and the afternoon walk');page.locator('#note-body').fill('Compare tree cover at 12:00 and 17:30.\n\nSynthetic observations only.');page.locator('#save').click()
 check('Saving creates a collection record',lambda:expect(page.locator('.note-row')).to_have_count(5))
 page.reload();check('Saved content survives actual HTTP reload',lambda:expect(page.locator('#note-title')).to_have_value('Heat, shade and the afternoon walk'))
 page.locator('#search').fill('17:30');check('Search includes note context',lambda:expect(page.locator('.note-row')).to_have_count(2))
 page.locator('#search').fill('NoSuchSyntheticPhrase');check('No-results state',lambda:expect(page.get_by_text('No matching notes',exact=True)).to_be_visible())
 page.locator('#search').fill('');page.locator('#note-body').fill('A recovered draft with 中文 content.');page.locator('.note-row').nth(2).click();page.locator('#search').fill('Heat, shade');page.locator('.note-row').click();check('Switching notes preserves drafts',lambda:expect(page.locator('#note-body')).to_have_value('A recovered draft with 中文 content.'))
 page.reload();check('Draft survives reload',lambda:expect(page.locator('#note-body')).to_have_value('A recovered draft with 中文 content.'))
 page.locator('#locale-toggle').click();page.locator('#theme-toggle').click();check('Locale and theme preserve draft',lambda:expect(page.locator('#note-body')).to_have_value('A recovered draft with 中文 content.'))
 shot(page,'desktop-zh-dark-draft')
 page.locator('#save').click();page.locator('#delete').click();check('Delete dialog identifies note',lambda:expect(page.locator('#delete-name')).to_have_text('Heat, shade and the afternoon walk'))
 check('Delete dialog initially focuses cancellation',lambda:expect(page.locator('button[value=cancel]')).to_be_focused())
 shot(page,'desktop-zh-dark-delete')
 page.keyboard.press('Escape');check('Escape leaves note intact',lambda:expect(page.locator('#note-title')).to_have_value('Heat, shade and the afternoon walk'))
 page.locator('#delete').click();page.locator('button[value=delete]').click();check('Confirmed deletion removes selected record',lambda:expect(page.locator('.note-row')).to_have_count(4))
 page.locator('#locale-toggle').click();page.locator('#theme-toggle').click();page.locator('#search').fill('');page.locator('.note-row').first.click();shot(page,'desktop-en-light')
 page.set_viewport_size({'width':390,'height':844});page.locator('#back').click();shot(page,'mobile-en-light-collection');page.locator('.note-row').first.click();shot(page,'mobile-en-light-editor')
 check('Mobile fits viewport',lambda: (_ for _ in ()).throw(AssertionError('horizontal overflow')) if page.evaluate('document.documentElement.scrollWidth > innerWidth') else None)
 page.locator('#locale-toggle').click();page.locator('#theme-toggle').click();shot(page,'mobile-zh-dark-editor');page.locator('#back').click();shot(page,'mobile-zh-dark-collection')
 page.locator('#locale-toggle').click();page.locator('#theme-toggle').click();page.keyboard.press('n');page.locator('#save').click();check('Empty title validation focuses field',lambda:expect(page.locator('#note-title')).to_be_focused());page.locator('#note-title').fill('Keyboard saved');page.locator('#note-body').fill('Works using Ctrl+S');page.keyboard.press('Control+s');check('Keyboard save is durable',lambda:expect(page.locator('#state-message')).to_have_text('Saved in this browser.'))
 # Real Storage-boundary write fault, preserving native read behavior.
 page.evaluate("window.originalSet=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k==='leafnote-notebook-v2')throw new DOMException('full','QuotaExceededError');return window.originalSet.call(this,k,v)}")
 page.locator('#note-body').fill('Text retained through storage failure');check('Draft write failure is visible',lambda:expect(page.locator('#state-message')).to_contain_text('Draft could not be backed up'))
 page.locator('#save').click();check('Failed save retains input',lambda:expect(page.locator('#note-body')).to_have_value('Text retained through storage failure'));shot(page,'mobile-en-light-storage-failure')
 page.evaluate('Storage.prototype.setItem=window.originalSet');page.locator('#retry').click();check('Storage recovery retry succeeds',lambda:expect(page.locator('#state-message')).to_have_text('Saved in this browser.'))
 # Download goes through the visible export control.
 page.locator('#back').click()
 with page.expect_download() as d:page.locator('#export').click()
 d.value.save_as(str(ROOT/'downloaded-backup.json'));check('Export contains actual records',lambda: (_ for _ in ()).throw(AssertionError('missing records')) if len(json.loads((ROOT/'downloaded-backup.json').read_text())['notebook']['notes'])!=5 else None)
 check('No JavaScript page errors',lambda: (_ for _ in ()).throw(AssertionError(errors)) if errors else None)
 # A separate browser context exercises legacy migration; original bytes remain unchanged.
 legacy=browser.new_page(viewport={'width':1440,'height':900});legacy.goto(URL);legacy.evaluate("localStorage.setItem('ui-spec-content-note-v1',JSON.stringify({title:'Original research note',body:'Keep this earlier content.'}))");legacy.reload();check('Legacy note recovered',lambda:expect(legacy.locator('#note-title')).to_have_value('Original research note'));legacy.locator('#note-body').fill('Updated safely');legacy.locator('#save').click();check('Original legacy bytes preserved',lambda: (_ for _ in ()).throw(AssertionError('legacy changed')) if 'Keep this earlier content.' not in legacy.evaluate("localStorage.getItem('ui-spec-content-note-v1')") else None)
 # Malformed storage preservation.
 broken=browser.new_page();broken.goto(URL);broken.evaluate("localStorage.setItem('leafnote-notebook-v2','{malformed-original')");broken.reload();check('Malformed storage blocks saving',lambda:expect(broken.locator('#save')).to_be_disabled());check('Malformed bytes remain intact',lambda: (_ for _ in ()).throw(AssertionError()) if broken.evaluate("localStorage.getItem('leafnote-notebook-v2')")!='{malformed-original' else None);shot(broken,'malformed-storage')
 # Read fault and successful retry.
 read=browser.new_page();read.add_init_script("window.originalGet=Storage.prototype.getItem;Storage.prototype.getItem=function(k){if(k==='leafnote-notebook-v2')throw new DOMException('blocked','SecurityError');return window.originalGet.call(this,k)}");read.goto(URL);check('Read fault reports uncertainty',lambda:expect(read.locator('#state-message')).to_contain_text('could not be read'));read.evaluate('Storage.prototype.getItem=window.originalGet');read.locator('#retry').click();check('Read retry re-enables saving',lambda:expect(read.locator('#save')).to_be_enabled())
 report={'browser':browser.version,'url':URL,'viewports':[[1440,900],[390,844]],'deviceScaleFactor':1,'tests':checks,'consoleErrors':errors,'scope':'Native HTTP localStorage plus explicitly injected Storage faults; screenshots require independent visual viewing.'}
 (ROOT/'test-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));browser.close()
print(f'{sum(x["result"]=="PASS" for x in checks)}/{len(checks)} assertions passed')
