import asyncio, json, urllib.request, os
from playwright.async_api import async_playwright
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell',args=['--no-sandbox'])
  page=await browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1,ignore_https_errors=True)
  out=[]
  for name,url in [('before','http://localhost:8777'),('simplenote','https://simplenote.com/'),('pico','https://picocss.com/docs/forms'),('shadcn-mail','https://ui.shadcn.com/examples/mail')]:
   try:
    await page.goto(url,wait_until='domcontentloaded',timeout=25000)
    await page.wait_for_timeout(1200)
    await page.screenshot(path=f'evidence/research-{name}.png')
    out.append({'name':name,'url':url,'title':await page.title(),'captured':True})
   except Exception as e: out.append({'name':name,'url':url,'error':str(e)})
  open('evidence/research-log.json','w').write(json.dumps(out,indent=2))
  await browser.close()
asyncio.run(main())
for name,url in [('pico.min.css','https://cdn.jsdelivr.net/npm/@picocss/pico@2.1.1/css/pico.min.css'),('PICO-LICENSE.txt','https://raw.githubusercontent.com/picocss/pico/v2.1.1/LICENSE.md')]:
 try: urllib.request.urlretrieve(url,'app/vendor/'+name)
 except Exception as e: print(name,str(e))
