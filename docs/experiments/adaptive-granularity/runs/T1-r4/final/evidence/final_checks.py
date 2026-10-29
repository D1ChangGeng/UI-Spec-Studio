from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import os,json
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
ROOT=Path(__file__).resolve().parent
results=[]
def check(name,fn):
 try:fn();results.append({'check':name,'result':'PASS'});print('PASS',name,flush=True)
 except Exception as e:results.append({'check':name,'result':'FAIL','error':str(e)});print('FAIL',name,str(e),flush=True)
def shot(p,n):
 p.wait_for_timeout(200);p.screenshot(path=str(ROOT/(n+'.png')),timeout=10000);print('CAPTURE',n,flush=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox','--disable-dev-shm-usage'])
 context=b.new_context(viewport={'width':1440,'height':900});p=context.new_page();p.goto('http://127.0.0.1:8844/');p.locator('#samples').click();p.locator('#delete').click();p.keyboard.press('n');check('Global shortcuts do not change a modal deletion target',lambda:expect(p.locator('#note-title')).to_have_value('How does shade change a street?'));p.keyboard.press('Escape')
 p.evaluate("() => { window.originalSet=Storage.prototype.setItem;Storage.prototype.setItem=function(){throw new DOMException('full','QuotaExceededError')}; }")
 p.locator('#delete').click();p.locator('button[value=delete]').click();check('Deletion failure keeps four notes',lambda:expect(p.locator('.note-row')).to_have_count(4));check('Deletion failure copy describes deletion',lambda:expect(p.locator('#state-message')).to_contain_text('Could not delete'));p.evaluate('() => {Storage.prototype.setItem=window.originalSet;}');p.locator('#retry').click();p.locator('button[value=cancel]').click();check('Retry deletion remains cancellable',lambda:expect(p.locator('.note-row')).to_have_count(4))
 tab=p.context.new_page();tab.goto('http://127.0.0.1:8844/');tab.locator('#new-note').click();tab.locator('#note-title').fill('Other tab edit');check('Concurrent tab change blocks stale writes',lambda:expect(p.locator('#save')).to_be_disabled());tab.close();p.close();context.close()
 context=b.new_context(viewport={'width':1440,'height':900});p=context.new_page();p.goto('http://127.0.0.1:8844/');p.locator('#samples').click()
 for width,height in [(1440,900),(390,844)]:
  p.set_viewport_size({'width':width,'height':height})
  for lang in ['en','zh']:
   if p.locator('html').get_attribute('lang') != ('en' if lang=='en' else 'zh-CN'):p.locator('#locale-toggle').click()
   for mode in ['light','dark']:
    if p.locator('html').get_attribute('data-theme') != mode:p.locator('#theme-toggle').click()
    if width==390 and p.locator('#back').is_visible():p.locator('#back').click()
    p.locator('.note-row').first.click();check(f'Note title returns into view: {width} {lang} {mode}',lambda: (_ for _ in ()).throw(AssertionError('title above writing pane')) if p.locator('#note-title').bounding_box()['y'] < p.locator('.writing-area').bounding_box()['y'] else None);p.locator('.editor-toolbar').click(position={'x':190,'y':10});shot(p,f'final-{width}-{lang}-{mode}-editor')
    check(f'No horizontal overflow: {width} {lang} {mode}',lambda: (_ for _ in ()).throw(AssertionError()) if p.evaluate('document.documentElement.scrollWidth>innerWidth') else None)
    if width==390:p.locator('#back').click();shot(p,f'final-{width}-{lang}-{mode}-collection')
    p.locator('.note-row').last.click();shot(p,f'long-{width}-{lang}-{mode}')
    p.locator('.writing-area').evaluate('(e)=>e.scrollTop=e.scrollHeight');check(f'Long text scrolls: {width} {lang} {mode}',lambda: (_ for _ in ()).throw(AssertionError()) if p.locator('.writing-area').evaluate('(e)=>e.scrollHeight>e.clientHeight && e.scrollTop===0') else None)
    if width==390:p.locator('#back').click()
 p.set_viewport_size({'width':320,'height':568});check('320px reflow',lambda: (_ for _ in ()).throw(AssertionError()) if p.evaluate('document.documentElement.scrollWidth>innerWidth') else None)
 (ROOT/'final-checks.json').write_text(json.dumps({'browser':b.version,'checks':results,'note':'Assertions and captures only. Visual review documented separately.'},indent=2));b.close()
print('DONE',sum(r['result']=='PASS' for r in results),'/',len(results),flush=True)
