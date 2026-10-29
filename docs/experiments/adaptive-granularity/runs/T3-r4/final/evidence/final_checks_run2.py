from playwright.sync_api import sync_playwright
from pathlib import Path
import json,hashlib
O=Path(__file__).parent;K='ui-spec-temporal-note-v1';checks=[];frames=[]
def check(n,c,d=None):checks.append({'check':n,'pass':bool(c),'details':d})
def shot(q,n):
 a=q.evaluate('performance.now()');q.screenshot(path=str(O/(n+'.png')),animations='allow');z=q.evaluate('performance.now()');frames.append({'file':n+'.png','start_ms':a,'end_ms':z})
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 for theme in ['light','dark']:
  c=b.new_context(viewport={'width':390,'height':844});q=c.new_page();q.goto('http://127.0.0.1:8314')
  if theme=='dark':q.locator('#theme-toggle').click()
  q.evaluate("()=>{window.writes=0;window.realSet=Storage.prototype.setItem;Storage.prototype.setItem=function(...a){window.writes++;return window.realSet.apply(this,a)}}")
  q.locator('#note-text').fill(('Follow district demand across the winter. Check each source, compare the assumptions, and keep the unresolved questions.\n\n'*6)[:600])
  q.locator('#note-text').evaluate('(e)=>{e.focus();e.setSelectionRange(300,310);e.scrollTop=75}')
  before=q.locator('#note-text').evaluate('(e)=>({start:e.selectionStart,end:e.selectionEnd,scroll:e.scrollTop})')
  box=q.locator('#card-space').bounding_box();savebox=q.locator('#save').bounding_box();q.locator('#save').click();q.mouse.click(savebox['x']+20,savebox['y']+20);q.keyboard.press('Enter')
  check(theme+' pending remains draft',q.locator('#note-card').get_attribute('data-face')=='front')
  shot(q,'final-mobile-'+theme+'-pending');q.wait_for_timeout(680)
  for j in range(7):shot(q,f'final-mobile-{theme}-turn-{j}');q.wait_for_timeout(50)
  q.wait_for_timeout(300)
  check(theme+' duplicate attempts one write',q.evaluate('window.writes')==1)
  check(theme+' saved text correct',json.loads(q.evaluate('(k)=>localStorage.getItem(k)',K))['text']==q.locator('#note-text').input_value())
  check(theme+' anchor stable',q.locator('#card-space').bounding_box()==box)
  check(theme+' saved focus',q.evaluate('document.activeElement.id')=='saved-text')
  check(theme+' saved region overflow',q.locator('#saved-text').evaluate('(e)=>e.scrollHeight>e.clientHeight'))
  q.locator('#saved-text').press('End');shot(q,f'final-mobile-{theme}-long-bottom')
  q.locator('#return').click();q.wait_for_timeout(800)
  after=q.locator('#note-text').evaluate('(e)=>({start:e.selectionStart,end:e.selectionEnd,scroll:e.scrollTop})')
  check(theme+' selection and scroll restored',before==after,{'before':before,'after':after})
  q.locator('#saved-link').focus();q.locator('#saved-link').press('Enter');q.wait_for_timeout(800)
  check(theme+' header keyboard focuses reading',q.evaluate('document.activeElement.id')=='saved-text')
  q.keyboard.press('Tab');check(theme+' keyboard skips inert editor',q.evaluate('document.activeElement.id')=='return')
  q.keyboard.press('Enter');q.wait_for_timeout(800);check(theme+' keyboard return editor',q.evaluate('document.activeElement.id')=='note-text')
  # Keep current draft and theme through language switching, including balanced CJK heading.
  q.locator('#locale-toggle').click();shot(q,f'final-mobile-{theme}-chinese')
  check(theme+' Chinese preserves note',len(q.locator('#note-text').input_value())==600)
  c.close()
 # Explicit latest navigation intent and existing snapshot during delayed save
 c=b.new_context(viewport={'width':1440,'height':900});q=c.new_page();q.goto('http://127.0.0.1:8314')
 q.locator('#note-text').fill('Previously saved');q.locator('#save').click();q.wait_for_timeout(1750);q.locator('#return').click();q.wait_for_timeout(800)
 q.locator('#note-text').fill('New submitted version');q.locator('#save').click();q.locator('#saved-link').click()
 check('pending saved face uses prior record',q.locator('#saved-text').inner_text()=='Previously saved')
 q.locator('#flip').click();q.wait_for_timeout(1700);check('explicit return wins late success',q.locator('#note-card').get_attribute('data-face')=='front')
 # First-save failure: no positive badge and no flip
 q.evaluate('(k)=>localStorage.removeItem(k)',K);q.reload();q.evaluate("()=>{Storage.prototype.setItem=function(){throw Error('Injected failure')}}")
 q.locator('#save').click();q.wait_for_timeout(1000);check('first failure no flip',q.locator('#note-card').get_attribute('data-face')=='front');check('first failure no saved badge','✓' not in q.locator('#saved-kicker').inner_text());shot(q,'final-first-save-failure')
 # Unknown data never says not saved; cannot know.
 pass
 c.close()
 c=b.new_context(viewport={'width':390,'height':844});q=c.new_page();q.goto('http://127.0.0.1:8314');q.evaluate('(k)=>localStorage.setItem(k,"bad")',K);q.reload();q.locator('#saved-link').click();q.wait_for_timeout(800);check('unknown footer honest','unavailable' in q.locator('#saved-foot').inner_text());shot(q,'final-unknown-mobile')
 c.close();b.close()
report={'checks':checks,'captures':frames,'hashes':{f:hashlib.sha256((O.parent/'app'/f).read_bytes()).hexdigest() for f in ['index.html','styles.css','app.js']},'viewport':'390x844 normal motion light and dark; desktop pending-navigation and first failure','dpr':1}
(O/'final-test-report.json').write_text(json.dumps(report,indent=2));print(json.dumps({'passed':sum(x['pass'] for x in checks),'total':len(checks),'failures':[x for x in checks if not x['pass']]},indent=2))
