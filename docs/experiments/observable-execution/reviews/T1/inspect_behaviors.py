import asyncio,json,re,traceback
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).parent;OUT=ROOT/'evidence'
APPS={'R7':8661,'T4':8662,'M2':8663}
BROWSER='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell'
SHORT='The quiet interface';LONG='Keeping your place when everything around you is changing'

async def state(page):
    return await page.evaluate('''()=>({url:location.href,scrollY,width:innerWidth,documentWidth:document.documentElement.scrollWidth,body:document.body.innerText,active:{tag:document.activeElement.tagName,text:document.activeElement.innerText.slice(0,140),aria:document.activeElement.getAttribute('aria-label'),visible:document.activeElement.matches(':focus-visible'),outline:getComputedStyle(document.activeElement).outline},buttons:[...document.querySelectorAll('button')].map(e=>({text:e.innerText,aria:e.getAttribute('aria-label'),pressed:e.getAttribute('aria-pressed')})),storage:{...localStorage}})''')

async def card_state(card):
    return await card.evaluate('''e=>({tag:e.tagName,class:e.className,box:{x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height},layers:[e,...e.querySelectorAll('*')].slice(0,30).map(x=>({tag:x.tagName,class:x.getAttribute('class'),style:x.getAttribute('style'),background:getComputedStyle(x).backgroundImage,color:getComputedStyle(x).backgroundColor,opacity:getComputedStyle(x).opacity,transform:getComputedStyle(x).transform,transition:getComputedStyle(x).transition,outline:getComputedStyle(x).outline,before:getComputedStyle(x,'::before').backgroundImage,after:getComputedStyle(x,'::after').backgroundImage}))})''')

async def main():
  results={}
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path=BROWSER,args=['--no-sandbox'])
    for name,port in APPS.items():
      r={};results[name]=r
      for mode in ['normal','reduce']:
        c=await b.new_context(viewport={'width':1440,'height':900},reduced_motion='reduce' if mode=='reduce' else 'no-preference')
        page=await c.new_page()
        try:
          await page.goto(f'http://127.0.0.1:{port}',wait_until='networkidle')
          link=page.locator('a').filter(has_text=SHORT)
          card=await link.evaluate_handle("e=>e.closest('article') || e.parentElement.parentElement")
          r[mode]={}
          r[mode]['rest']=await card_state(card)
          box=r[mode]['rest']['box']
          for pos,fx,fy in [('pointer-left',.12,.16),('pointer-right',.88,.78)]:
            await page.mouse.move(box['x']+box['w']*fx,box['y']+box['h']*fy,steps=12)
            await page.wait_for_timeout(300)
            r[mode][pos]=await card_state(card)
            await page.screenshot(path=str(OUT/f'{name}-{mode}-{pos}.png'))
          await page.mouse.move(10,10)
          await page.wait_for_timeout(250)
          tabs=[]
          for i in range(14):
            await page.keyboard.press('Tab')
            a=(await state(page))['active'];tabs.append(a)
            if a['tag']=='A' and SHORT in a['text']:
              break
          r[mode]['tabs']=tabs
          r[mode]['focus_card']=await card_state(card)
          await page.screenshot(path=str(OUT/f'{name}-{mode}-keyboard-card.png'))
          if mode=='normal':
            await page.keyboard.press('Enter')
            await page.wait_for_timeout(150)
            r['keyboard_detail']=await state(page)
            await page.screenshot(path=str(OUT/f'{name}-desktop-short-detail.png'))
            # The detail heading receives focus. Traverse backwards to visible back action.
            route=[]
            for i in range(8):
              await page.keyboard.press('Shift+Tab')
              a=(await state(page))['active'];route.append(a)
              if a['tag']=='A' and 'Back to' in a['text']:
                await page.keyboard.press('Enter');break
            await page.wait_for_timeout(150)
            r['keyboard_return_path']=route;r['keyboard_return']=await state(page)
            # A natural lower-list opening and browser Back checks scroll retention independently of search.
            await page.set_viewport_size({'width':390,'height':844})
            longlink=page.locator('a').filter(has_text=LONG)
            await longlink.scroll_into_view_if_needed()
            await page.evaluate('window.scrollBy(0,-120)')
            r['lower_list_before']=await state(page)
            await page.screenshot(path=str(OUT/f'{name}-mobile-lower-list.png'))
            await longlink.click()
            await page.wait_for_timeout(150)
            await page.evaluate('window.scrollTo(0,600)')
            r['lower_detail_reading']=await state(page)
            await page.go_back(wait_until='networkidle')
            await page.wait_for_timeout(150)
            r['lower_list_after_back']=await state(page)
            await page.screenshot(path=str(OUT/f'{name}-mobile-returned-lower-list.png'))
        except Exception as e:
          r[mode+'_failure']={'error':str(e),'traceback':traceback.format_exc(),'state':await state(page)}
          await page.screenshot(path=str(OUT/f'{name}-{mode}-inspection-failure.png'))
        await c.close()
      # Fail only writes after normal load; restore the same browser storage method before retry.
      c=await b.new_context(viewport={'width':1440,'height':900});page=await c.new_page()
      try:
        await page.goto(f'http://127.0.0.1:{port}',wait_until='networkidle')
        await page.evaluate("window.__reviewOriginalSetItem=Storage.prototype.setItem; Storage.prototype.setItem=function(){throw new DOMException('Review injected storage write failure','QuotaExceededError')}")
        save=page.get_by_role('button',name=re.compile(r'^Save.*The quiet interface$'))
        await save.click();await page.wait_for_timeout(100)
        r['storage_write_failed']=await state(page)
        await page.screenshot(path=str(OUT/f'{name}-desktop-storage-failed.png'))
        await page.set_viewport_size({'width':390,'height':844})
        await page.screenshot(path=str(OUT/f'{name}-mobile-storage-failed.png'))
        await page.evaluate('Storage.prototype.setItem=window.__reviewOriginalSetItem')
        retry=page.get_by_role('button',name=re.compile(r'retry|try again',re.I))
        if await retry.count():
          await retry.first.click();r['storage_recovery_action']='retry'
        else:
          r['storage_recovery_action']='no retry control; toggle off and on'
          unsave=page.get_by_role('button',name=re.compile(r'^(Unsave|Remove).*The quiet interface$'))
          if await unsave.count(): await unsave.click()
          save=page.get_by_role('button',name=re.compile(r'^Save.*The quiet interface$'))
          if await save.count(): await save.click()
        await page.wait_for_timeout(100)
        r['storage_recovered']=await state(page)
        await page.reload(wait_until='networkidle')
        r['storage_recovered_reload']=await state(page)
      except Exception as e:
        r['storage_failure']={'error':str(e),'traceback':traceback.format_exc(),'state':await state(page)}
        await page.screenshot(path=str(OUT/f'{name}-storage-inspection-failure.png'))
      await c.close()
      (ROOT/'behavior_measurements.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    await b.close()
  print(json.dumps({n:{k:v for k,v in r.items() if 'failure' in k or 'storage_recovery_action'==k} for n,r in results.items()},ensure_ascii=False,indent=2))

asyncio.run(main())
