import os,json,time,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'review-output';CAP=OUT/'failure-preference-captures';CAP.mkdir(exist_ok=True)
D=json.loads((OUT/'run-02/check-results.json').read_text());TITLE=D['content']['title'];BODY=D['content']['draft']+'\nUNSTORED FAILURE PROBE / 未能存储的测试修改'
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
os.environ['PLAYWRIGHT_BROWSERS_PATH']='/workspace/scratch/43b440780c87/playwright-cache'
R={'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'variants':{}}
def status(pg):return pg.evaluate('''() => [...document.querySelectorAll('[role="status"]')].filter(e=>e.getClientRects().length).map(e=>({text:e.innerText,error:e.dataset.error||e.parentElement.dataset.error||null}))''')
def top(pg):pg.evaluate('''() => {scrollTo(0,0);for(const s of ['.writing-area','.editor-scroll','#note-body']){let e=document.querySelector(s);if(e)e.scrollTop=0}}''')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',headless=True,args=['--no-sandbox'])
 for i in range(1,4):
  n=f'variant-{i:02d}';v={};R['variants'][n]=v
  c=b.new_context(viewport={'width':390,'height':844},storage_state=str(OUT/'run-02'/f'{n}-state.json'),locale='en-US');pg=c.new_page();pg.set_default_timeout(5000)
  try:
   pg.goto(f'http://127.0.0.1:{8210+i}/final/');pg.locator('#note-list button').filter(has_text=TITLE).click()
   if pg.locator('html').get_attribute('lang')!='en':pg.locator('#locale-toggle').click()
   if pg.locator('html').get_attribute('data-theme')!='light':pg.locator('#theme-toggle').click()
   pg.locator('#density').select_option('comfortable');pg.wait_for_timeout(200)
   pg.evaluate('''() => {window.__reviewRestore=Storage.prototype.setItem;Storage.prototype.setItem=function(){throw new DOMException('Review injected storage failure','QuotaExceededError')}}''')
   pg.locator('#note-body').fill(BODY);pg.keyboard.press('Control+s');pg.wait_for_timeout(250)
   v['before_preference']=status(pg);v['retry_before']=pg.locator('#retry').is_visible()
   pg.locator('#density').select_option('compact');pg.wait_for_timeout(250);top(pg)
   v['after_density']=status(pg);v['retry_after']=pg.locator('#retry').is_visible();v['draft_retained']=pg.locator('#note-body').input_value()==BODY
   path=CAP/f'{n}-failure-then-density.png';pg.screenshot(path=str(path));v['capture']=str(path.relative_to(ROOT))
   pg.locator('#theme-toggle').click();pg.locator('#locale-toggle').click();pg.wait_for_timeout(250);v['after_theme_and_locale']=status(pg)
   pg.evaluate('() => {Storage.prototype.setItem=window.__reviewRestore}')
   pg.keyboard.press('Control+s');pg.wait_for_timeout(250);v['after_recovery_save']=status(pg)
  except Exception as e:v['original_failure']={'error':str(e),'traceback':traceback.format_exc()}
  c.close();(OUT/'failure-preference-results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
 b.close()
R['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());(OUT/'failure-preference-results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2));print(json.dumps(R,ensure_ascii=False,indent=2))
