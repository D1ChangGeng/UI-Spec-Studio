import asyncio, contextlib, functools, hashlib, json, os, threading, time, traceback
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.async_api import async_playwright

BASE=Path('/workspace/scratch/43b440780c87/granularity-review-packets/T3')
OUT=BASE/'review-output'
CHROME='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell'
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
os.environ['PLAYWRIGHT_BROWSERS_PATH']='/workspace/scratch/43b440780c87/playwright-cache'
LONG=('District heating fieldnote — shared demand\n\n'
      'At 07:00, most buildings request heat together. Compare preheating, insulation, and a slower morning ramp. Keep the existing comfort standard while checking which homes benefit.\n\n'
      '城市供热观察：清晨的需求同时上升。应比较保温、提前供热和分时调节，并记录室内舒适度。不要把平均值当作所有家庭的体验。\n\n'
      'Evidence to collect: hourly demand, indoor temperature, and resident feedback. Open question: can the change reduce the peak without moving discomfort to older buildings?\n\n'
      '下一步：记录两周数据，复查极冷天气，并询问住户。')
SHORT='Library visit — ask about the archive opening hours.'
THIRD='雨后的街道\n记录树荫、积水和行人的路线。下次带上相机。'
RESULTS={'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'content':{'long':LONG,'long_length':len(LONG),'short':SHORT,'third':THIRD},'runs':[]}

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def hashes():
    return {str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for n in range(1,4) for stage in ('initial','final') for p in sorted((BASE/f'variant-{n:02d}'/stage).glob('*')) if p.is_file()}

def flush():
    (OUT/'observations.json').write_text(json.dumps(RESULTS,ensure_ascii=False,indent=2))

async def state(page):
    return await page.evaluate('''() => {
      const by=id=>document.getElementById(id), el=by('note-text'), card=by('note-card');
      const rect=e=>{if(!e)return null;const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}};
      const visible=e=>!!e&&!!e.getClientRects().length&&getComputedStyle(e).visibility!=='hidden';
      const storage={};for(let i=0;i<localStorage.length;i++){let k=localStorage.key(i);storage[k]=localStorage.getItem(k)};
      return {url:location.href,viewport:{width:innerWidth,height:innerHeight},scroll:{x:scrollX,y:scrollY},theme:document.documentElement.dataset.theme,lang:document.documentElement.lang,
       face:card?.dataset.face,motion:card?.dataset.motion,cardTransform:card?getComputedStyle(card).transform:null,cardRect:rect(card),cardSpaceRect:rect(by('card-space')),
       active:{id:document.activeElement?.id,tag:document.activeElement?.tagName,text:document.activeElement?.textContent?.slice(0,90)},
       note:el?{value:el.value,selection:[el.selectionStart,el.selectionEnd],scrollTop:el.scrollTop,clientHeight:el.clientHeight,scrollHeight:el.scrollHeight,visible:visible(el)}:null,
       title:by('note-title')?.value,front:{inert:by('card-front')?.inert,ariaHidden:by('card-front')?.getAttribute('aria-hidden')},back:{inert:by('card-back')?.inert,ariaHidden:by('card-back')?.getAttribute('aria-hidden')},
       savedText:by('saved-text')?.textContent,savedRect:rect(by('saved-text')),status:by('status')?.textContent,collectionStatus:(by('collection-status')||by('collection-message'))?.textContent,
       saveDisabled:by('save')?.disabled,retryVisible:visible(by('retry')),collectionVisible:visible(by('collection')),tiles:[...document.querySelectorAll('#note-grid>button')].map(e=>({id:e.dataset.id||e.dataset.noteId,text:e.textContent,rect:rect(e),current:e.dataset.current,selected:e.classList.contains('selected')})),storage,
       documentSize:{width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight},reduced:matchMedia('(prefers-reduced-motion: reduce)').matches,
       animations:document.getAnimations().map(a=>({state:a.playState,currentTime:a.currentTime,duration:a.effect?.getTiming().duration}))};
    }''')

async def capture(page,run,label,full=False):
    p=OUT/run['name']/f'{label}.png';p.parent.mkdir(exist_ok=True)
    s=await state(page);s['label']=label;s['image']=str(p.relative_to(OUT));s['captured_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    await page.screenshot(path=str(p),full_page=full,animations='allow')
    run['states'].append(s);flush();return s

async def frames(page,run,label,times):
    start=time.monotonic()
    for ms in times:
        await asyncio.sleep(max(0,ms/1000-(time.monotonic()-start)))
        s=await capture(page,run,f'{label}-{ms:04d}ms');s['actual_elapsed_ms']=round((time.monotonic()-start)*1000)
    flush()

async def fill(page,text,title='District heating fieldnote'):
    if await page.locator('#note-title').count():await page.locator('#note-title').fill(title)
    await page.locator('#note-text').fill(text)

async def settle(page,ms=1900):await page.wait_for_timeout(ms)

async def new_note(page,text,title='District heating fieldnote'):
    await page.locator('#new-note').click();await settle(page,450);await fill(page,text,title)

async def return_front(page):
    if await page.locator('#note-card').get_attribute('data-face')=='back':
        await page.locator('#return').click();await settle(page,850)

async def back(page):await page.locator('#back-collection').click();await settle(page,500)

async def open_tile(page,index):await page.locator('#note-grid>button').nth(index).click();await settle(page,500)

async def desktop(browser,n):
    run={'name':f'variant-{n:02d}-desktop','variant':n,'viewport':[1440,900],'mode':'normal','states':[],'checks':[],'errors':[]};RESULTS['runs'].append(run)
    context=await browser.new_context(viewport={'width':1440,'height':900},color_scheme='light',reduced_motion='no-preference')
    page=await context.new_page();page.on('pageerror',lambda e:run['errors'].append(str(e)))
    try:
        await page.goto(f'http://127.0.0.1:{8430+n}/final/');await capture(page,run,'00-empty')
        await new_note(page,LONG);await capture(page,run,'01-long-editor')
        await page.locator('#theme-toggle').click();await capture(page,run,'02-dark-editor')
        await page.locator('#locale-toggle').click();await capture(page,run,'03-dark-chinese-editor')
        run['checks'].append({'appearance_keeps_draft':await page.locator('#note-text').input_value()==LONG})
        await page.locator('#theme-toggle').click();await page.locator('#locale-toggle').click()
        await page.locator('#note-text').evaluate('(e)=>{e.focus();e.setSelectionRange(26,45);e.scrollTop=80}')
        await page.keyboard.press('Control+Enter');await page.keyboard.press('Control+Enter');await page.keyboard.press('Control+Enter')
        await frames(page,run,'04-save',[0,450,700,950,1100,1400,1900])
        await page.locator('#saved-text').evaluate('(e)=>e.scrollTop=e.scrollHeight');await capture(page,run,'05-saved-long-bottom')
        await page.locator('#return').click();await frames(page,run,'06-reverse',[0,130,320,850])
        run['checks'].append({'keyboard_return_selection':(await state(page))['note']['selection']})
        await fill(page,'Overflow '+('长 note ' * 110));await capture(page,run,'07-over-limit')
        await fill(page,LONG);await page.locator('#save').click();await back(page);await capture(page,run,'08-return-during-save');await settle(page,1000)
        await new_note(page,SHORT,'Archive visit');await page.locator('#save').click();await settle(page);await back(page)
        await new_note(page,THIRD,'雨后的街道');await page.locator('#save').click();await settle(page);await back(page);await capture(page,run,'09-three-card-collection')
        await page.locator('#note-grid>button').nth(0).focus();await page.keyboard.press('Enter');await settle(page,450)
        revised=LONG+'\nDraft addition.';await fill(page,revised)
        await page.locator('#note-text').evaluate('(e)=>{e.setSelectionRange(12,22);e.scrollTop=65}')
        await back(page);await open_tile(page,2);await back(page);await open_tile(page,0)
        run['checks'].append({'switch_retains_draft':await page.locator('#note-text').input_value()==revised,'switch_return_state':await state(page)})
        for i in range(3):await back(page);await open_tile(page,i%3)
        await back(page);await open_tile(page,0)
        before=await page.evaluate('JSON.stringify({...localStorage})')
        await page.evaluate('''() => {window.__originalSetItem=Storage.prototype.setItem;window.__failWrite=true;Storage.prototype.setItem=function(k,v){if(window.__failWrite)throw new DOMException('Review injected quota failure','QuotaExceededError');return window.__originalSetItem.call(this,k,v)}}''')
        await page.locator('#save').click();await settle(page,1200);s=await capture(page,run,'10-save-failure')
        run['checks'].append({'failure_preserves_storage':await page.evaluate('JSON.stringify({...localStorage})')==before,'failure_keeps_draft':await page.locator('#note-text').input_value()==revised,'failure_face':s['face']})
        await back(page);await capture(page,run,'11-failure-collection');await open_tile(page,0)
        await page.evaluate('window.__failWrite=false');await page.locator('#retry').click();await settle(page);await capture(page,run,'12-retry-success')
        await page.reload();await settle(page,350);await capture(page,run,'13-reload-collection');await open_tile(page,0)
        run['checks'].append({'reload_retains_saved':await page.locator('#note-text').input_value()==revised})
        # Repeated quick forward/reverse requests use actual mouse presses on the stable external flip control.
        await page.locator('#flip').click();await page.wait_for_timeout(90);await page.locator('#flip').click();await page.wait_for_timeout(90);await page.locator('#flip').click();await settle(page,900);await capture(page,run,'14-rapid-flip-final')
        await return_front(page)
        # Clear affordance: record whether a cancellation exists, then dismiss a native confirmation if presented.
        dialogs=[]
        async def reject_dialog(d):dialogs.append({'type':d.type,'message':d.message});await d.dismiss()
        page.on('dialog',reject_dialog)
        await page.locator('details>summary').click();await capture(page,run,'15-clear-affordance');await page.locator('#clear').click();await settle(page,500)
        s=await capture(page,run,'16-clear-result');run['checks'].append({'clear_dialogs':dialogs,'post_clear_storage':s['storage'],'post_clear_tiles':len(s['tiles'])})
    except Exception as e:
        run['errors'].append({'exception':str(e),'traceback':traceback.format_exc()})
        with contextlib.suppress(Exception):await capture(page,run,'ERROR-original')
    finally:
        flush();await context.close()

async def mobile(browser,n,reduced=False):
    run={'name':f'variant-{n:02d}-'+('reduced' if reduced else 'mobile'),'variant':n,'viewport':[390,844],'mode':'reduced' if reduced else 'normal','states':[],'checks':[],'errors':[]};RESULTS['runs'].append(run)
    context=await browser.new_context(viewport={'width':390,'height':844},color_scheme='light',reduced_motion='reduce' if reduced else 'no-preference')
    page=await context.new_page();page.on('pageerror',lambda e:run['errors'].append(str(e)))
    try:
        await page.goto(f'http://127.0.0.1:{8430+n}/final/');await capture(page,run,'00-empty')
        await new_note(page,LONG);await page.evaluate('scrollTo(0,0)');await capture(page,run,'01-long-editor-top')
        await page.locator('#save').scroll_into_view_if_needed();await capture(page,run,'02-long-editor-actions')
        await page.locator('#note-text').evaluate('(e)=>{e.focus();e.setSelectionRange(20,30);e.scrollTop=90}')
        await page.keyboard.press('Control+Enter');await frames(page,run,'03-save',[0,500,950,1200,1800])
        await page.locator('#saved-text').evaluate('(e)=>e.scrollTop=e.scrollHeight');await capture(page,run,'04-long-saved-bottom')
        await page.locator('#return').click();await frames(page,run,'05-reverse',[0,160,850])
        run['checks'].append({'reverse_selection':(await state(page))['note']['selection']})
        await back(page);await new_note(page,SHORT,'Archive visit');await page.locator('#save').click();await settle(page,1700);await back(page)
        await new_note(page,THIRD,'雨后的街道');await page.locator('#save').click();await settle(page,1700);await back(page)
        await page.evaluate('scrollTo(0,0)');await capture(page,run,'06-collection-top')
        await page.locator('#note-grid>button').nth(2).scroll_into_view_if_needed();await capture(page,run,'07-collection-third')
        await page.locator('#note-grid>button').nth(2).click();await settle(page,500);await page.locator('#back-collection').click();await settle(page,500);await capture(page,run,'08-return-third-orientation')
        await open_tile(page,0);await page.locator('#theme-toggle').click();await page.locator('#locale-toggle').click();await page.evaluate('scrollTo(0,0)');await capture(page,run,'09-dark-chinese-editor')
        run['checks'].append({'appearance_keeps_draft':await page.locator('#note-text').input_value()==LONG,'document_width':await page.evaluate('document.documentElement.scrollWidth')})
        await page.locator('#locale-toggle').click();await page.locator('#save').click();await settle(page,1700);await capture(page,run,'10-dark-saved')
        await page.reload();await settle(page,200);await capture(page,run,'11-reload-collection')
    except Exception as e:
        run['errors'].append({'exception':str(e),'traceback':traceback.format_exc()})
        with contextlib.suppress(Exception):await capture(page,run,'ERROR-original')
    finally:
        flush();await context.close()

async def initial(browser,n):
    run={'name':f'variant-{n:02d}-initial','variant':n,'viewport':[1440,900],'mode':'initial-comparison','states':[],'checks':[],'errors':[]};RESULTS['runs'].append(run)
    context=await browser.new_context(viewport={'width':1440,'height':900},color_scheme='light')
    page=await context.new_page()
    try:
        await page.goto(f'http://127.0.0.1:{8430+n}/initial/');await capture(page,run,'00-initial-editor');await fill(page,LONG);await page.locator('#save').click();await settle(page);await capture(page,run,'01-initial-saved')
    except Exception as e:run['errors'].append({'exception':str(e),'traceback':traceback.format_exc()})
    finally:flush();await context.close()

async def main():
    OUT.mkdir(exist_ok=True);before=hashes();(OUT/'source-hashes-before.json').write_text(json.dumps(before,indent=2))
    servers=[]
    for n in range(1,4):
        server=ThreadingHTTPServer(('127.0.0.1',8430+n),functools.partial(QuietHandler,directory=str(BASE/f'variant-{n:02d}')))
        threading.Thread(target=server.serve_forever,daemon=True).start();servers.append(server)
    try:
        async with async_playwright() as p:
            browser=await p.chromium.launch(executable_path=CHROME,headless=True,args=['--no-sandbox'])
            for n in range(1,4):
                print('START',n,flush=True)
                await desktop(browser,n);await mobile(browser,n);await mobile(browser,n,True);await initial(browser,n)
                print('DONE',n,flush=True)
            await browser.close()
    finally:
        for s in servers:s.shutdown()
        after=hashes();(OUT/'source-hashes-after.json').write_text(json.dumps(after,indent=2));RESULTS['source_unchanged']=before==after;RESULTS['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());flush()

if __name__=='__main__':asyncio.run(main())
