from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import os,json
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
r=Path(__file__).resolve().parent;fixtures=json.loads((r/'long-content.json').read_text());checks=[]
def ck(n,f):
 try:f();checks.append({'check':n,'result':'PASS'});print('PASS',n,flush=True)
 except Exception as e:checks.append({'check':n,'result':'FAIL','error':str(e)});print('FAIL',n,str(e),flush=True)
def capture(p,n):p.wait_for_timeout(100);p.screenshot(path=str(r/(n+'.png')))
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':900});errs=[];p.on('pageerror',lambda e:errs.append(str(e)));p.goto('http://127.0.0.1:8844/');p.locator('#samples').click()
 p.locator('#new-note').click();p.locator('#note-title').fill(fixtures['zh_title']);p.locator('#note-body').fill(fixtures['zh_body']);p.locator('#save').click();ck('Create/save long note',lambda:expect(p.locator('.note-row')).to_have_count(5));p.locator('#note-body').fill(fixtures['zh_body']+'\n\n未保存的补充 / unsaved addition');draft=p.locator('#note-body').input_value();selected=p.locator('.note-row.active').get_attribute('data-note-id')
 for density in ['compact','comfortable']:
  p.locator('#density').select_option(density);p.locator('#locale-toggle').click();p.locator('#theme-toggle').click();ck('Draft retained through '+density+' and theme/locale',lambda:expect(p.locator('#note-body')).to_have_value(draft));ck('Selection retained through '+density,lambda:expect(p.locator('.note-row.active')).to_have_attribute('data-note-id',selected))
 p.locator('#density').select_option('compact');p.reload();ck('Density survives reload',lambda:expect(p.locator('#density')).to_have_value('compact'));ck('Draft survives preference reload',lambda:expect(p.locator('#note-body')).to_have_value(draft));p.locator('#save').click();p.locator('#search').fill('无障碍');ck('Long-context search',lambda:expect(p.locator('.note-row')).to_have_count(1));p.locator('.note-row').click();ck('Reopen long saved note',lambda:expect(p.locator('#note-body')).to_have_value(draft));p.locator('#search').fill('')
 for width,height in [(1440,900),(390,844)]:
  p.set_viewport_size({'width':width,'height':height})
  for lang in ['en','zh']:
   if p.locator('html').get_attribute('lang') != ('en' if lang=='en' else 'zh-CN'):p.locator('#locale-toggle').click()
   if width==390 and p.locator('#back').is_visible():p.locator('#back').click()
   # Chinese note for Chinese reading; long English sample for English reading.
   p.locator('.note-row').filter(has_text=fixtures['zh_title'] if lang=='zh' else 'How does shade change a street?').click()
   for density in ['comfortable','compact']:
    p.locator('#density').select_option(density);p.locator('.writing-area').evaluate('(e)=>e.scrollTop=0');p.locator('.editor-toolbar').click(position={'x':180,'y':10});capture(p,f'{width}-{lang}-{density}-editor')
    ck(f'No overflow {width} {lang} {density}',lambda: (_ for _ in ()).throw(AssertionError()) if p.evaluate('document.documentElement.scrollWidth>innerWidth') else None)
    ck(f'Density correctly applied {width} {lang} {density}',lambda:expect(p.locator('html')).to_have_attribute('data-density',density))
    if width==390:p.locator('#back').click();capture(p,f'{width}-{lang}-{density}-collection');p.locator('.note-row.active').click()
 p.locator('#theme-toggle').click();capture(p,'390-zh-compact-dark-editor');p.locator('#delete').click();ck('Long-note deletion identifies title',lambda:expect(p.locator('#delete-name')).to_have_text(fixtures['zh_title']));p.locator('button[value=cancel]').click();ck('Cancel retains selected note',lambda:expect(p.locator('#note-title')).to_have_value(fixtures['zh_title']));p.locator('#delete').click();p.locator('button[value=delete]').click();ck('Confirmed deletion removes just that note',lambda:expect(p.locator('.note-row')).to_have_count(4));p.reload();ck('Deleted note remains absent on reload',lambda:expect(p.locator('.note-row')).to_have_count(4));ck('No page errors',lambda: (_ for _ in ()).throw(AssertionError(errs)) if errs else None)
 (r/'results.json').write_text(json.dumps({'browser':b.version,'checks':checks,'pageErrors':errs},ensure_ascii=False,indent=2));b.close();print('DONE',sum(c['result']=='PASS' for c in checks),'/',len(checks),flush=True)
