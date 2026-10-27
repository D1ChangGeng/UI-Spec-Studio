from pathlib import Path
import http.server,threading,functools,json,time,hashlib
from playwright.sync_api import sync_playwright
R=Path('/tmp/craft-tasks');O=R/'captures';O.mkdir(exist_ok=True)
css=R/'dist/style.css';css.write_text(css.read_text(encoding='utf-8')+Path('.research/trial-refinement.css').read_text(encoding='utf-8'),encoding='utf-8')
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(R/'dist')));threading.Thread(target=server.serve_forever,daemon=True).start();rows=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 for task in ['chat','drawer']:
  for width in [1440,390]:
   row={'task':task,'width':width,'viewport_height':1000 if width>500 else 844,'actions':[],'errors':[],'captures':[],'viewed':False}
   page=b.new_page(viewport={'width':width,'height':row['viewport_height']},reduced_motion='no-preference');page.on('pageerror',lambda error:row['errors'].append(str(error)))
   def snap(name):
    f=O/f'{task}-{width}-{name}.png';start=time.time();page.screenshot(path=str(f));row['captures'].append({'file':f.name,'capture_started':start,'capture_finished':time.time(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
   try:
    page.goto(f'http://127.0.0.1:{server.server_port}/?task={task}',wait_until='networkidle');page.wait_for_timeout(600);snap('initial');row['initial_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
    if task=='chat':
     if width<680:
      page.get_by_role('button',name='Threads',exact=True).click();row['mobile_history_visible']=page.get_by_role('button',name='New Thread',exact=True).is_visible();snap('navigation');page.get_by_role('button',name='Close threads',exact=True).click()
     inp=page.locator('textarea').first;inp.fill('Summarize the selected research sources.');inp.press('Enter');page.wait_for_timeout(400);snap('streaming');page.wait_for_timeout(3600);snap('result');row['result_text']=page.locator('body').inner_text();row['result_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
     inp.fill('/error');inp.press('Enter');page.wait_for_timeout(400);snap('error');row['fixture_error_present']='Fixture: source is unavailable.' in page.locator('body').inner_text()
     inp.fill('A response to cancel');inp.press('Enter');page.wait_for_timeout(150);stop=page.get_by_role('button',name='Stop generating',exact=True);row['stop_present']=stop.is_visible();stop.click();page.wait_for_timeout(200);row['stop_removed']=page.get_by_role('button',name='Stop generating',exact=True).count()==0;snap('cancelled');row['actions'].append('Prompt, stream, long result, fixture error, new response cancellation; narrow history access')
    else:
     page.get_by_role('button',name='Review source',exact=True).click();page.wait_for_timeout(600);snap('open');row['dialog_count']=page.get_by_role('dialog').count();page.locator('#note').fill('A retained local note');page.locator('.sheet-scroll').evaluate('(e)=>e.scrollTop=300');snap('scrolled')
     page.get_by_role('button',name='Return to reading',exact=True).click();page.wait_for_timeout(750);snap('closed');row['focus_after_close']=page.evaluate('document.activeElement?.textContent');row['open_dialogs_after_close']=page.locator('[role=dialog][data-state=open]').count()
     page.get_by_role('button',name='Review source',exact=True).click();page.wait_for_timeout(600);row['note_retained']=page.locator('#note').input_value()=='A retained local note';box=page.get_by_role('dialog').bounding_box();x=box['x']+box['width']/2;y=box['y']+16;page.mouse.move(x,y);page.mouse.down()
     for i,dy in enumerate([20,60,100,60,20]):page.mouse.move(x,y+dy,steps=4);page.wait_for_timeout(70);snap('drag-'+str(i))
     page.mouse.up();page.wait_for_timeout(650);snap('settled');page.keyboard.press('Escape');page.wait_for_timeout(750);row['open_dialogs_after_escape']=page.locator('[role=dialog][data-state=open]').count();row['focus_after_escape']=page.evaluate('document.activeElement?.textContent');snap('escaped');row['actions'].append('Open, edit, scroll, close, reopen, pointer drag/reversal, escape and settled focus')
   except Exception as e:row['execution_error']=str(e)
   finally:rows.append(row);page.close()
 b.close()
server.shutdown();(R/'capture-results.json').write_text(json.dumps({'scope':'Actual browser operations of authored trial adapters using unchanged registry source. Not independent model runs or accepted product quality. Snapshot timing is not frame-rate evidence.','cases':rows},indent=2)+'\n',encoding='utf-8')
print(json.dumps([{k:v for k,v in r.items() if k not in ['captures','result_text']} for r in rows],indent=2))
