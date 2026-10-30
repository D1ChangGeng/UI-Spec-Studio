from pathlib import Path
import json, re
from playwright.sync_api import sync_playwright

BASE = Path('/workspace/scratch/654b1ee6916f/observable-product-review/T3/review')
OUT = BASE / 'evidence'
BROWSER = '/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell'

MEASURE = '''() => {
  const rect = el => { const r = el.getBoundingClientRect(); return Object.fromEntries(['x','y','width','height'].map(k=>[k,r[k]])); };
  const fields = Object.fromEntries(['note-title','note-body'].map(id => {
    const e=document.getElementById(id), s=getComputedStyle(e), p=getComputedStyle(e,'::placeholder');
    return [id,{rect:rect(e),value:e.value,placeholder:e.placeholder,enteredFontSize:s.fontSize,enteredLineHeight:s.lineHeight,fontFamily:s.fontFamily,padding:s.padding,borderWidth:s.borderWidth,borderRadius:s.borderRadius,background:s.backgroundColor,enteredColor:s.color,placeholderFontSize:p.fontSize,placeholderOpacity:p.opacity,placeholderColor:p.color,outline:s.outline,outlineOffset:s.outlineOffset,focused:document.activeElement===e}];
  }));
  return {locale:document.documentElement.lang,theme:document.documentElement.dataset.theme,viewport:{width:innerWidth,height:innerHeight},scroll:{x:scrollX,y:scrollY},horizontalOverflow:document.documentElement.scrollWidth>innerWidth,activeElement:document.activeElement.id,fields,save:{rect:rect(document.getElementById('save')),fontSize:getComputedStyle(document.getElementById('save')).fontSize},editor:rect(document.querySelector('.editor-panel')),context:rect(document.querySelector('.context-panel'))};
}'''

def take(page, name):
    page.screenshot(path=str(OUT/f'{name}.png'))
    page.locator('.editor-panel').screenshot(path=str(OUT/f'{name}-editor.png'))

def state(page):
    return {'title':page.locator('#note-title').input_value(),'body':page.locator('#note-body').input_value(),'message':page.locator('#state-message').inner_text(),'recentTitle':page.locator('#recent-title').inner_text(),'retryVisible':page.locator('#retry').is_visible(),'saveDisabled':page.locator('#save').is_disabled(),'saveBusy':page.locator('#save').get_attribute('aria-busy'),'activeElement':page.evaluate('document.activeElement.id'),'storage':page.evaluate("localStorage.getItem('ui-spec-content-note-v1')")}

records=[]
flows=[]
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=BROWSER,headless=True,args=['--no-sandbox'])
    for variant,port in [('D5',8681),('STARTER',8680)]:
      for width,height in [(390,844),(1440,900)]:
       for locale in ['zh','en']:
        for theme in ['light','dark']:
          page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
          page.on('pageerror',lambda error:errors.append(str(error)))
          page.goto(f'http://127.0.0.1:{port}',wait_until='networkidle')
          if locale=='en':page.locator('#locale-toggle').click()
          if theme=='dark':page.locator('#theme-toggle').click()
          page.evaluate('document.fonts.ready')
          name=f'{variant}-{width}-{locale}-{theme}'
          item={'variant':variant,'configuration':name,'empty':page.evaluate(MEASURE)}
          if variant=='D5':take(page,name+'-empty')
          page.locator('#theme-toggle').focus()
          page.keyboard.press('Tab')
          assert page.evaluate('document.activeElement.id')=='note-title'
          item['emptyKeyboardFocus']=page.evaluate(MEASURE)
          if variant=='D5' and (width,locale,theme) in [(390,'en','light'),(1440,'zh','dark')]:take(page,name+'-focus-empty')
          title='城市供热高峰调节' if locale=='zh' else 'Research demand patterns'
          body='核对原始材料，并保留待验证的问题。\n下一步：比较相关研究。' if locale=='zh' else 'Review the source material and open questions.\nNext: compare the related studies.'
          page.locator('#note-title').fill(title)
          page.keyboard.press('Tab')
          assert page.evaluate('document.activeElement.id')=='note-body'
          page.keyboard.insert_text(body)
          page.evaluate('window.scrollTo(0,0)')
          item['enteredKeyboardFocus']=page.evaluate(MEASURE)
          if variant=='D5':take(page,name+'-entered-focus')
          records.append(item)
          page.close()
      # The same source owns saving and recovery in all four copies.
      page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
      page.goto(f'http://127.0.0.1:{port}',wait_until='networkidle')
      page.locator('#locale-toggle').click()
      page.locator('#note-title').fill('Saved baseline')
      page.locator('#note-body').fill('Original local note')
      page.locator('#save').click()
      page.wait_for_function("document.querySelector('.state-area').dataset.status==='saved'")
      flow={'variant':variant,'saved':state(page)}
      page.reload(wait_until='networkidle')
      flow['afterReload']=state(page)
      assert flow['afterReload']['title']=='Saved baseline' and flow['afterReload']['body']=='Original local note'
      page.locator('#locale-toggle').click()
      page.locator('summary').click()
      page.locator('#simulate-failure').check()
      page.locator('#simulate-slow').check()
      page.locator('#note-title').fill('Recovered draft')
      page.locator('#note-body').fill('Keep this text after a failed write.')
      page.locator('#save').click()
      flow['pending']=state(page)
      page.wait_for_function("document.querySelector('.state-area').dataset.status==='error'")
      flow['failed']=state(page)
      assert flow['failed']['title']=='Recovered draft'
      assert json.loads(flow['failed']['storage'])['title']=='Saved baseline'
      assert flow['failed']['retryVisible']
      if variant=='D5':take(page,'D5-save-failed-1440-en-light')
      page.locator('#simulate-failure').uncheck()
      page.locator('#retry').click()
      page.wait_for_function("document.querySelector('.state-area').dataset.status==='saved'")
      flow['retried']=state(page)
      assert json.loads(flow['retried']['storage'])['title']=='Recovered draft'
      assert not flow['retried']['retryVisible']
      assert flow['retried']['activeElement']=='note-title'
      if variant=='D5':take(page,'D5-save-recovered-1440-en-light')
      page.reload(wait_until='networkidle')
      flow['recoveredAfterReload']=state(page)
      assert flow['recoveredAfterReload']['title']=='Recovered draft'
      flows.append(flow)
      page.close()
    browser.close()

def rgb(s):return [int(x) for x in re.findall(r'\d+',s)[:3]]
def lum(c):
    c=[v/255 for v in c]
    c=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in c]
    return .2126*c[0]+.7152*c[1]+.0722*c[2]
for rec in records:
    for f in rec['empty']['fields'].values():
        bg=rgb(f['background']);fg=rgb(f['placeholderColor']);a=float(f['placeholderOpacity'])
        blend=[v*a+b*(1-a) for v,b in zip(fg,bg)]
        l1,l2=sorted([lum(blend),lum(bg)],reverse=True)
        f['computedPlaceholderContrast']=(l1+.05)/(l2+.05)

(BASE/'measurements.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
(BASE/'save-retry.json').write_text(json.dumps({'flows':flows,'pageErrors':errors},ensure_ascii=False,indent=2))
comparison=[]
for r in records[:8]:
    other=next(x for x in records if x['variant']=='STARTER' and x['empty']['viewport']==r['empty']['viewport'] and x['empty']['locale']==r['empty']['locale'] and x['empty']['theme']==r['empty']['theme'])
    equality={}
    for state_name in ['empty','emptyKeyboardFocus','enteredKeyboardFocus']:
        equality[state_name]=all(r[state_name]['fields'][k]['rect']==other[state_name]['fields'][k]['rect'] and r[state_name]['fields'][k]['enteredFontSize']==other[state_name]['fields'][k]['enteredFontSize'] for k in ['note-title','note-body']) and r[state_name]['save']==other[state_name]['save'] and r[state_name]['editor']==other[state_name]['editor'] and r[state_name]['context']==other[state_name]['context']
    comparison.append({'configuration':r['configuration'],'geometryAndEnteredTextEqualToStarter':equality,'title':r['empty']['fields']['note-title'],'body':r['empty']['fields']['note-body'],'horizontalOverflow':r['empty']['horizontalOverflow']})
(BASE/'comparison.json').write_text(json.dumps(comparison,ensure_ascii=False,indent=2))
print(json.dumps({'comparisons':[{'configuration':x['configuration'],'equal':x['geometryAndEnteredTextEqualToStarter'],'titleRect':x['title']['rect'],'bodyRect':x['body']['rect'],'enteredFontSize':x['title']['enteredFontSize'],'placeholderFontSize':x['title']['placeholderFontSize'],'contrast':round(x['title']['computedPlaceholderContrast'],3),'overflow':x['horizontalOverflow']} for x in comparison],'flows':flows,'pageErrors':errors},ensure_ascii=False,indent=2))
