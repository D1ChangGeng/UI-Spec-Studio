import os,json,time,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'review-output';CAP=OUT/'supplemental-captures';CAP.mkdir(exist_ok=True)
DATA=json.loads((OUT/'run-02/check-results.json').read_text());TITLE=DATA['content']['title'];BODY=DATA['content']['body'];DRAFT=DATA['content']['draft'];SHORTS=DATA['content']['short_notes']
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
os.environ['PLAYWRIGHT_BROWSERS_PATH']='/workspace/scratch/43b440780c87/playwright-cache'
EXE='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell'
RESULT={'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'variants':{}}
def capture(page,variant,name):
 path=CAP/f'{variant}-{name}.png';page.screenshot(path=str(path));return str(path.relative_to(ROOT))
def top(page):page.evaluate('''() => {window.scrollTo(0,0);for(const s of ['.writing-area','.editor-scroll','#note-body']){let e=document.querySelector(s);if(e)e.scrollTop=0}}''')
def scrollstate(page):return page.evaluate('''() => ({window:scrollY,areas:Object.fromEntries(['.writing-area','.editor-scroll','#note-body'].map(s=>{let e=document.querySelector(s);return[s,e?{scrollTop:e.scrollTop,scrollHeight:e.scrollHeight,clientHeight:e.clientHeight}:null]}))})''')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=EXE,headless=True,args=['--no-sandbox'])
 for i in range(1,4):
  vname=f'variant-{i:02d}';base=f'http://127.0.0.1:{8210+i}';v={'captures':[],'checks':[]};RESULT['variants'][vname]=v
  try:
   c=browser.new_context(viewport={'width':1440,'height':900},locale='en-US');pg=c.new_page();pg.set_default_timeout(5000);pg.goto(base+'/initial/')
   if i==3:
    for _ in range(pg.locator('#note-list button').count()):
     pg.locator('#note-list button').first.click();pg.locator('#delete-note').click();pg.locator('#confirm-delete').click()
   if pg.locator('html').get_attribute('lang')!='en':pg.locator('#locale-toggle').click()
   for title,body in SHORTS+[[TITLE,BODY]]:
    pg.locator('#new-note').click();pg.locator('#note-title').fill(title)
    if pg.locator('#note-context').count():pg.locator('#note-context').fill('Urban fieldwork / 城市观察')
    pg.locator('#note-body').fill(body);pg.keyboard.press('Control+s');pg.wait_for_timeout(220)
   top(pg);v['captures'].append(capture(pg,vname,'initial-desktop-long'))
   pg.set_viewport_size({'width':390,'height':844})
   if not pg.locator('#note-body').is_visible():pg.locator('#note-list button').filter(has_text=TITLE).click()
   top(pg);v['captures'].append(capture(pg,vname,'initial-mobile-long'))
   pg.set_viewport_size({'width':1440,'height':900});pg.goto(base+'/final/');pg.wait_for_timeout(200)
   pg.locator('#note-list button').filter(has_text=TITLE).click()
   v['checks'].append({'name':'initial_to_final_saved_content_compatibility','pass':pg.locator('#note-body').input_value()==BODY and pg.locator('#note-list button').count()==4})
   c.close()
  except Exception as e:v['initial_original_failure']={'error':str(e),'traceback':traceback.format_exc()}
  try:
   c=browser.new_context(viewport={'width':1440,'height':900},locale='en-US',storage_state=str(OUT/'run-02'/f'{vname}-state.json'));pg=c.new_page();pg.set_default_timeout(5000);pg.goto(base+'/final/')
   if pg.locator('html').get_attribute('lang')!='en':pg.locator('#locale-toggle').click()
   if pg.locator('html').get_attribute('data-theme')!='light':pg.locator('#theme-toggle').click()
   pg.locator('#note-list button').filter(has_text=TITLE).click();pg.locator('#note-body').fill(DRAFT);pg.keyboard.press('Control+s');pg.wait_for_timeout(250)
   pg.locator('.skip').focus()
   for _ in range(4):
    pg.keyboard.press('Tab')
    if pg.evaluate('document.activeElement.id')=='density':break
   v['density_keyboard_focus']=pg.locator('#density').evaluate('''e=>{let s=getComputedStyle(e);return {active:e===document.activeElement,outline:s.outline,boxShadow:s.boxShadow,borderColor:s.borderColor}}''')
   v['captures'].append(capture(pg,vname,'desktop-density-keyboard-focus'))
   # Exercise keyboard selection and ensure input caret ranges survive appearance changes.
   pg.locator('#note-body').focus();pg.locator('#note-body').evaluate('e=>e.setSelectionRange(275,305)')
   before=pg.locator('#note-body').evaluate('e=>({start:e.selectionStart,end:e.selectionEnd})')
   pg.locator('#density').select_option('compact');pg.locator('#theme-toggle').click();pg.locator('#locale-toggle').click()
   after=pg.locator('#note-body').evaluate('e=>({start:e.selectionStart,end:e.selectionEnd})')
   v['checks'].append({'name':'body_selection_range_survives_preferences','pass':before==after,'before':before,'after':after})
   pg.locator('#theme-toggle').click();pg.locator('#locale-toggle').click()
   # Draft follows this note through a selection round trip.
   pg.locator('#note-body').fill(DRAFT+'\nDraft switch probe / 切换草稿检查')
   pg.locator('#note-list button').filter(has_text='A bench to revisit').click();pg.locator('#note-list button').filter(has_text=TITLE).click()
   v['checks'].append({'name':'draft_survives_note_switch','pass':pg.locator('#note-body').input_value()==DRAFT+'\nDraft switch probe / 切换草稿检查'})
   pg.set_viewport_size({'width':390,'height':844});top(pg)
   v['scroll_before']=scrollstate(pg)
   pg.mouse.move(190,700);pg.mouse.wheel(0,650);pg.wait_for_timeout(150);pg.mouse.wheel(0,650);pg.wait_for_timeout(150)
   v['scroll_after']=scrollstate(pg);v['captures'].append(capture(pg,vname,'mobile-manual-scroll-interior'))
   # Inspect write-failure feedback with Chinese labels at narrow width.
   top(pg);pg.locator('#theme-toggle').click();pg.locator('#locale-toggle').click();pg.locator('#density').select_option('comfortable')
   pg.evaluate('''() => {window.__reviewOriginalSetItem=Storage.prototype.setItem;Storage.prototype.setItem=function(){throw new DOMException('Review injected quota failure','QuotaExceededError')}}''')
   pg.locator('#note-body').fill(DRAFT+'\nMobile write failure / 窄屏存储失败')
   pg.keyboard.press('Control+s');pg.wait_for_timeout(250);top(pg)
   v['mobile_failure_feedback']=pg.evaluate('''() => [...document.querySelectorAll('[role="status"]')].filter(e=>e.getClientRects().length).map(e=>{let r=e.getBoundingClientRect();return{text:e.innerText,top:r.top,bottom:r.bottom,inViewport:r.top>=0&&r.bottom<=innerHeight}})''')
   v['captures'].append(capture(pg,vname,'mobile-dark-chinese-storage-failure'))
   pg.evaluate('() => {Storage.prototype.setItem=window.__reviewOriginalSetItem}')
   c.close()
  except Exception as e:v['supplemental_original_failure']={'error':str(e),'traceback':traceback.format_exc()}
  try:
   c=browser.new_context(viewport={'width':1440,'height':900},locale='en-US',accept_downloads=True);pg=c.new_page();pg.set_default_timeout(5000);pg.goto(base+'/final/')
   legacy={'title':'Recovered earlier note / 原有笔记','body':'A local record from the earlier one-note editor.\n这份旧笔记应继续可读。'}
   pg.evaluate('''v=>{localStorage.clear();localStorage.setItem('ui-spec-content-note-v1',JSON.stringify(v))}''',legacy);pg.reload();pg.wait_for_timeout(200)
   v['checks'].append({'name':'legacy_note_recovered_and_original_preserved','pass':pg.locator('#note-title').input_value()==legacy['title'] and pg.locator('#note-body').input_value()==legacy['body'] and pg.evaluate("JSON.parse(localStorage.getItem('ui-spec-content-note-v1'))")==legacy})
   exportid='#export-all' if i==3 else '#export'
   with pg.expect_download() as downloadinfo:pg.locator(exportid).click()
   download=downloadinfo.value;download.save_as(str(OUT/f'{vname}-legacy-export.json'))
   raw=(OUT/f'{vname}-legacy-export.json').read_text();v['checks'].append({'name':'export_download_contains_legacy_note','pass':legacy['title'] in raw and legacy['body'].split('\n')[0] in raw})
   c.close()
  except Exception as e:v['legacy_original_failure']={'error':str(e),'traceback':traceback.format_exc()}
  (OUT/'supplemental-results.json').write_text(json.dumps(RESULT,ensure_ascii=False,indent=2))
 browser.close()
RESULT['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());(OUT/'supplemental-results.json').write_text(json.dumps(RESULT,ensure_ascii=False,indent=2))
print(json.dumps(RESULT,ensure_ascii=False,indent=2))
