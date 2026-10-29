import os,json,time,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'review-output';CAP=OUT/'final-probe-captures';CAP.mkdir(exist_ok=True)
DATA=json.loads((OUT/'run-02/check-results.json').read_text());TITLE=DATA['content']['title'];DRAFT=DATA['content']['draft']
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
os.environ['PLAYWRIGHT_BROWSERS_PATH']='/workspace/scratch/43b440780c87/playwright-cache'
EXE='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell'
R={'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'variants':{}}
def cap(pg,name,label):
 path=CAP/f'{name}-{label}.png';pg.screenshot(path=str(path));return str(path.relative_to(ROOT))
def top(pg):pg.evaluate('''() => {scrollTo(0,0);for(const s of ['.writing-area','.editor-scroll','#note-body']){let e=document.querySelector(s);if(e)e.scrollTop=0}}''')
def positions(pg):return pg.evaluate('''() => Object.fromEntries(['#note-title','#note-body'].map(s=>{let e=document.querySelector(s),r=e.getBoundingClientRect(),c=getComputedStyle(e);return[s,{y:r.y,height:r.height,width:r.width,fontSize:c.fontSize,lineHeight:c.lineHeight}]}))''')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=EXE,headless=True,args=['--no-sandbox'])
 for i in range(1,4):
  name=f'variant-{i:02d}';v={'checks':[],'captures':[]};R['variants'][name]=v
  c=b.new_context(viewport={'width':1440,'height':900},locale='en-US',storage_state=str(OUT/'run-02'/f'{name}-state.json'));pg=c.new_page();pg.set_default_timeout(5000)
  try:
   pg.goto(f'http://127.0.0.1:{8210+i}/final/')
   if pg.locator('html').get_attribute('lang')!='en':pg.locator('#locale-toggle').click()
   if pg.locator('html').get_attribute('data-theme')!='light':pg.locator('#theme-toggle').click()
   pg.locator('#density').select_option('comfortable')
   pg.locator('#note-list button').filter(has_text='A bench to revisit').click()
   pg.locator('#delete-note' if i==3 else '#delete').click()
   if i==1:pg.locator('#confirm button[value=delete]').click()
   else:pg.locator('#confirm-delete').click()
   pg.wait_for_timeout(200);pg.reload();pg.wait_for_timeout(200)
   v['checks'].append({'name':'confirmed_delete_persists_reload','pass':pg.locator('#note-list button').filter(has_text='A bench to revisit').count()==0 and pg.locator('#note-list button').count()==3})
   # Keyboard activation of the actual density select remains functional even if its focus cue is absent.
   pg.locator('.skip').focus()
   for _ in range(4):
    pg.keyboard.press('Tab')
    if pg.evaluate('document.activeElement.id')=='density':break
   pg.keyboard.press('ArrowDown');pg.keyboard.press('Enter');pg.wait_for_timeout(180)
   v['checks'].append({'name':'keyboard_density_change','pass':pg.locator('html').get_attribute('data-density')=='compact'})
   pg.locator('header').click(position={'x':5,'y':5})
   pg.keyboard.press('/' if i==1 else 'Control+k')
   v['checks'].append({'name':'keyboard_search_focus','pass':pg.evaluate('document.activeElement.id')=='search'})
   pg.keyboard.type('microclimate-53');pg.keyboard.press('Tab');pg.keyboard.press('Enter')
   v['checks'].append({'name':'keyboard_search_reopen','pass':pg.locator('#note-title').input_value()==TITLE and pg.locator('#note-body').is_visible()})
   # Exact search currently shows only one row; it remains a valid way to enter the note on mobile.
   pg.locator('#note-body').fill(DRAFT);pg.keyboard.press('Control+s');pg.wait_for_timeout(250)
   pg.set_viewport_size({'width':390,'height':844});pg.locator('#density').select_option('comfortable');top(pg)
   v['locale_geometry_en']=positions(pg)
   pg.locator('#locale-toggle').click();pg.wait_for_timeout(250);top(pg)
   v['locale_geometry_zh']=positions(pg)
   pg.locator('#theme-toggle').click();pg.wait_for_timeout(300);top(pg)
   v['settled_dark_styles']=pg.evaluate('''() => Object.fromEntries(['.brand','#density','#save','#note-body'].map(s=>{let e=document.querySelector(s),c=getComputedStyle(e);return[s,{color:c.color,background:c.backgroundColor}]}))''')
   v['captures'].append(cap(pg,name,'mobile-settled-dark-chinese'))
   pg.locator('#theme-toggle').click();pg.locator('#locale-toggle').click();pg.locator('#density').select_option('compact');pg.wait_for_timeout(250);top(pg)
   pg.mouse.move(10,700);pg.mouse.wheel(0,500);pg.wait_for_timeout(200)
   v['outer_scroll_window_y']=pg.evaluate('scrollY');v['captures'].append(cap(pg,name,'mobile-outer-scroll'))
   # Unsaved new-note creation through keyboard activation of the ordinary button.
   pg.locator('#back').click();pg.locator('#new-note').focus();pg.keyboard.press('Enter');pg.locator('#note-title').fill('Keyboard-created draft / 键盘草稿');pg.locator('#note-body').fill('Retain this new draft across all appearance controls.\n新的草稿也应保留。')
   pg.locator('#density').select_option('comfortable');pg.locator('#theme-toggle').click();pg.locator('#locale-toggle').click();pg.reload();pg.wait_for_timeout(250)
   if not pg.locator('#note-body').is_visible():pg.locator('#note-list button').filter(has_text='Keyboard-created draft').click()
   v['checks'].append({'name':'new_unsaved_draft_preferences_and_reload','pass':pg.locator('#note-title').input_value()=='Keyboard-created draft / 键盘草稿' and '新的草稿也应保留。' in pg.locator('#note-body').input_value()})
  except Exception as e:v['original_failure']={'error':str(e),'traceback':traceback.format_exc()};v['captures'].append(cap(pg,name,'original-failure'))
  c.close();(OUT/'final-probe-results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
 b.close()
R['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());(OUT/'final-probe-results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2));print(json.dumps(R,ensure_ascii=False,indent=2))
