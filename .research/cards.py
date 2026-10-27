from pathlib import Path
import urllib.request,json,hashlib,subprocess,shutil,http.server,functools,threading,time
from playwright.sync_api import sync_playwright
P=Path('/tmp/card-build');P.mkdir(exist_ok=True);O=Path('/tmp/card-evidence');O.mkdir(exist_ok=True);records=[]
def get(url):
 data=urllib.request.urlopen(url,timeout=60).read();records.append({'url':url,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)});return data
base='https://raw.githubusercontent.com/DavidHDev/react-bits/e12c22192ac7b4b452c5e2feb9b586d74765d696/'
(P/'src').mkdir(exist_ok=True);(P/'dist').mkdir(exist_ok=True)
(P/'src/App.jsx').write_bytes(get('https://raw.githubusercontent.com/D1ChangGeng/UI-Spec-Studio/7d276ee220aa57442e43096a178964359ae65e13/.development/craft-study.jsx'))
for name in ['SpotlightCard','TiltedCard']:
 for ext in ['jsx','css']:
  target=P/'src'/name/f'{name}.{ext}';target.parent.mkdir(exist_ok=True);target.write_bytes(get(base+f'src/content/Components/{name}/{name}.{ext}'))
(O/'source-license.md').write_bytes(get(base+'LICENSE.md'))
subprocess.run(['npm','init','-y'],cwd=P,check=True)
subprocess.run(['npm','install','--ignore-scripts','--save-exact','react@19.2.0','react-dom@19.2.0','esbuild@0.25.10'],cwd=P,check=True)
subprocess.run(['node','-e',"require('esbuild').buildSync({entryPoints:['src/App.jsx'],bundle:true,outfile:'dist/app.js',jsx:'automatic',minify:false,define:{'process.env.NODE_ENV':'\"production\"'}})"],cwd=P,check=True)
shutil.copyfile('.research/card-style.css',P/'dist/study.css');shutil.copyfile(P/'package-lock.json',O/'build-lock.json')
(P/'dist/index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="app.css"><link rel="stylesheet" href="study.css"><body><div id="root"></div><script src="app.js"></script></body></html>',encoding='utf-8')
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(P/'dist')));threading.Thread(target=server.serve_forever,daemon=True).start();cases=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for surface in ['plain','spotlight','tilt']:
  for width,lang,theme in [(1440,'en','dark'),(390,'zh','light')]:
   row={'surface':surface,'width':width,'lang':lang,'theme':theme,'errors':[],'captures':[],'viewed':False};page=b.new_page(viewport={'width':width,'height':1000 if width>500 else 844})
   page.on('pageerror',lambda e:row['errors'].append(str(e)))
   def snap(name,loc=None):
    f=O/f'{surface}-{width}-{name}.png';start=time.time();(loc.screenshot if loc else page.screenshot)(path=str(f));row['captures'].append({'file':f.name,'started':start,'finished':time.time(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
   try:
    page.goto(f'http://127.0.0.1:{server.server_port}/?surface={surface}&theme={theme}&lang={lang}',wait_until='networkidle');page.wait_for_timeout(500);snap('frame')
    row['overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1');row['card_count']=page.locator('.note-content').count()
    card=page.locator('.notes').first;card.scroll_into_view_if_needed();snap('cards')
    item=page.locator('.notes > *').first;box=item.bounding_box()
    for i,frac in enumerate([.1,.25,.4,.55,.7,.85,.65,.4,.1]):
     page.mouse.move(box['x']+box['width']*frac,box['y']+box['height']*.4);page.wait_for_timeout(90);snap('pointer-'+str(i),item)
    row['buttons']=page.locator('.open-note').all_text_contents();page.locator('.open-note').first.click();page.wait_for_timeout(400);page.locator('.reader').scroll_into_view_if_needed();snap('reader');row['reader_visible']=page.locator('.reader').is_visible()
    page.locator('.reader button').click();row['reader_closed']=page.locator('.reader').count()==0
    field=page.locator('input').first;field.fill('zzzz-no-match');row['filtered_cards']=page.locator('.note-content').count();field.fill('')
   except Exception as e:row['execution_error']=str(e)
   finally:cases.append(row);page.close()
 b.close()
server.shutdown();(O/'report.json').write_text(json.dumps({'scope':'Current maintainer comparative component trial with same task/content and source identity; not a fresh-context model comparison. Pointer samples include capture overhead, not frame-rate evidence.','sources':records,'cases':cases},indent=2)+'\n',encoding='utf-8')
print(json.dumps([{k:v for k,v in x.items() if k!='captures'} for x in cases],indent=2))
