from pathlib import Path
from urllib.request import urlopen
from playwright.sync_api import sync_playwright
import os,json
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
root=Path(__file__).resolve().parent.parent
urls={
 'bootstrap.min.css':'https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css',
 'BOOTSTRAP-LICENSE.txt':'https://raw.githubusercontent.com/twbs/bootstrap/v5.3.8/LICENSE'
}
for name,url in urls.items():
 try:
  data=urlopen(url,timeout=20).read();(root/'app/vendor'/name).write_bytes(data);print(name,len(data))
 except Exception as e:print(name,str(e))
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1440,'height':900},device_scale_factor=1,ignore_https_errors=True)
 for name,url in [('baseline','http://127.0.0.1:8844/'),('bootstrap-reference','https://getbootstrap.com/docs/5.3/examples/sidebars/'),('shadcn-reference','https://v3.shadcn.com/examples/mail')]:
  try:
   page.goto(url,wait_until='networkidle',timeout=30000)
   if name=='shadcn-reference':page.get_by_role('heading',name='Inbox',exact=True).scroll_into_view_if_needed()
   page.screenshot(path=str(root/'evidence'/f'{name}.png'));print(name,'captured',page.title())
  except Exception as e:print(name,'ERROR',str(e))
 b.close()
