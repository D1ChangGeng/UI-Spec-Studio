from pathlib import Path
import http.server,threading,functools,json,time,hashlib
from playwright.sync_api import sync_playwright
R=Path('/tmp/craft-tasks'); O=R/'captures';O.mkdir(exist_ok=True)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(R/'dist')))
threading.Thread(target=server.serve_forever,daemon=True).start();rows=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 for task in ['chat','drawer']:
  for width in [1440,390]:
   row={'task':task,'width':width,'viewport_height':1000 if width>500 else 844,'actions':[],'errors':[],'captures':[],'viewed':False}
   page=b.new_page(viewport={'width':width,'height':row['viewport_height']},reduced_motion='no-preference')
   page.on('pageerror',lambda error:row['errors'].append(str(error)))
   def snap(name):
    f=O/f'{task}-{width}-{name}.png';start=time.time();page.screenshot(path=str(f));row['captures'].append({'file':f.name,'capture_started':start,'capture_finished':time.time(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
   try:
    page.goto(f'http://127.0.0.1:{server.server_port}/?task={task}',wait_until='networkidle');page.wait_for_timeout(600);snap('initial')
    row['initial_text']=page.locator('body').inner_text();row['initial_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
    row['initial_buttons']=page.get_by_role('button').all_text_contents()
    if task=='chat':
     inp=page.locator('textarea').first;inp.fill('Summarize the selected research sources.');inp.press('Enter');page.wait_for_timeout(400);snap('streaming')
     row['actions'].append('Entered prompt and pressed Enter');page.wait_for_timeout(3600);snap('result')
     row['result_text']=page.locator('body').inner_text();row['result_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
     inp.fill('/error');inp.press('Enter');page.wait_for_timeout(400);snap('error');row['error_text']=page.locator('body').inner_text()
    else:
     page.get_by_role('button',name='Review source',exact=True).click();page.wait_for_timeout(450);snap('open');row['dialog_count']=page.get_by_role('dialog').count()
     note=page.locator('#note');note.fill('A retained local note');page.locator('.sheet-scroll').evaluate('(e)=>e.scrollTop=300');snap('scrolled')
     page.get_by_role('button',name='Return to reading',exact=True).click();page.wait_for_timeout(400);snap('closed');row['focus_after_close']=page.evaluate('document.activeElement?.textContent')
     page.get_by_role('button',name='Review source',exact=True).click();page.wait_for_timeout(350);row['note_retained']=page.locator('#note').input_value()=='A retained local note'
     box=page.get_by_role('dialog').bounding_box();x=box['x']+box['width']/2;y=box['y']+16
     page.mouse.move(x,y);page.mouse.down()
     for i,dy in enumerate([20,60,100,60,20]):
      page.mouse.move(x,y+dy,steps=4);page.wait_for_timeout(70);snap('drag-'+str(i))
     page.mouse.up();page.wait_for_timeout(500);snap('settled');row['actions'].append('Open, edit, scroll, close, reopen, pointer drag and reversal')
     page.keyboard.press('Escape');page.wait_for_timeout(300);row['dialogs_after_escape']=page.get_by_role('dialog').count()
   except Exception as e:row['execution_error']=str(e)
   finally:
    rows.append(row);page.close()
 b.close()
server.shutdown();(R/'capture-results.json').write_text(json.dumps({'scope':'Actual browser operation of authored fixture adapters using original registry sources. Not independent model runs or accepted product quality. Screenshots pending actual viewing.','cases':rows},indent=2)+'\n',encoding='utf-8')
print(json.dumps([{k:v for k,v in r.items() if k not in ['captures','initial_text','result_text','error_text','initial_buttons']} for r in rows],indent=2))
