import asyncio,json,os,time,traceback,sys
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path(__file__).resolve().parent
CAP=ROOT/'captures'
os.environ['FONTCONFIG_FILE']='/workspace/scratch/654b1ee6916f/ui-spec-fonts/fonts.conf'
EXE='/workspace/scratch/654b1ee6916f/ui-spec-browsers/chrome-headless-shell-linux64/chrome-headless-shell'
APPS=[('L6',8671),('N3',8672),('P8',8673)]
LONG_EN=('Opening question: how could a city reduce peak heating demand?\n\n' + 'Compare hourly demand, building insulation and the weather. Keep the source and uncertainty beside each observation.\n\n'*10)[:588]+'\nEND-OF-NOTE'
LONG_ZH=('开头：城市如何降低高峰供热需求？\n\n'+'观察时应把小时需求、建筑保温与天气变化放在一起，并标记证据来源。下一步要比较不同街区，检查哪些解释能得到数据支持，哪些问题仍需继续调查。\n\n'*12)[:593]+'\n笔记结束。'
LONG_EN=LONG_EN[:600]
LONG_ZH=LONG_ZH[:600]

STATE_JS='''() => {
 const ids=['note-card','card-front','card-back','preview-note','note-text','flip','save','retry','status','saved-text'];
 const out={time:performance.now(),scrollY,active:document.activeElement.id,viewport:{w:innerWidth,h:innerHeight,docW:document.documentElement.scrollWidth,docH:document.documentElement.scrollHeight}};
 for(const id of ids){const e=document.getElementById(id);const s=getComputedStyle(e);const r=e.getBoundingClientRect();out[id]={text:e.innerText,value:e.value,rect:{x:r.x,y:r.y,w:r.width,h:r.height},clientHeight:e.clientHeight,scrollHeight:e.scrollHeight,scrollTop:e.scrollTop,overflowY:s.overflowY,font:s.font,fontSize:s.fontSize,lineHeight:s.lineHeight,transform:s.transform,opacity:s.opacity,visibility:s.visibility,backface:s.backfaceVisibility,ariaHidden:e.getAttribute('aria-hidden'),inert:e.inert,tabindex:e.tabIndex,disabled:e.disabled,hidden:e.hidden,selectionStart:e.selectionStart,selectionEnd:e.selectionEnd};}
 out.storage=Object.fromEntries(Object.keys(localStorage).filter(k=>!k.startsWith('__review')).map(k=>[k,localStorage.getItem(k)]));
 return out;
}'''

TRACE_JS='''() => {
 window.__trace=[];window.__traceClicks=[];window.__traceRunning=true;
 const start=performance.now();
 document.getElementById('flip').addEventListener('click',()=>window.__traceClicks.push(performance.now()-start));
 function sample(){if(!window.__traceRunning)return;let card=document.getElementById('note-card'),f=document.getElementById('card-front'),b=document.getElementById('card-back'),n=document.getElementById('preview-note');let st=getComputedStyle(card);let m=new DOMMatrixReadOnly(st.transform);window.__trace.push({t:performance.now()-start,transform:st.transform,m11:m.m11,m13:m.m13,m31:m.m31,m33:m.m33,frontAria:f.getAttribute('aria-hidden'),backAria:b.getAttribute('aria-hidden'),frontInert:f.inert,backInert:b.inert,frontOpacity:getComputedStyle(f).opacity,backOpacity:getComputedStyle(b).opacity,frontVisibility:getComputedStyle(f).visibility,backVisibility:getComputedStyle(b).visibility,active:document.activeElement.id,previewTab:n.tabIndex,flip:document.getElementById('flip').innerText});requestAnimationFrame(sample)};requestAnimationFrame(sample);
}'''

STORAGE_INIT='''(() => {
 window.__storageEvents=[];window.__timerEvents=[];window.__reviewDelay=false;
 const set=Storage.prototype.setItem;
 Storage.prototype.setItem=function(k,v){try{const ret=set.call(this,k,v);window.__storageEvents.push({time:performance.now(),key:k,length:String(v).length,value:String(v).length<10000?String(v):null,result:'ok'});return ret;}catch(e){window.__storageEvents.push({time:performance.now(),key:k,length:String(v).length,result:'error',name:e.name,message:e.message.slice(0,240)});throw e}};
 const timeout=window.setTimeout;
 window.setTimeout=function(cb,delay,...args){let actual=(window.__reviewDelay&&Number(delay)>=100&&Number(delay)<=2000)?2500:delay;if(window.__reviewDelay)window.__timerEvents.push({time:performance.now(),requested:delay,actual});return timeout.call(this,cb,actual,...args)};
})();'''

async def shot(page,name,full=True):
    await page.screenshot(path=str(CAP/name),full_page=full)

async def state(page):return await page.evaluate(STATE_JS)

async def long_case(browser,app,port,size):
    mobile=size=='mobile'
    ctx=await browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 900})
    page=await ctx.new_page()
    await page.goto(f'http://127.0.0.1:{port}/',wait_until='networkidle')
    before=await state(page)
    if mobile:
        await page.locator('#locale-toggle').click()
        await page.locator('#theme-toggle').click()
    note=LONG_ZH if mobile else LONG_EN
    await page.locator('#note-text').fill(note)
    await page.locator('#flip').click()
    await page.wait_for_timeout(1000)
    await page.evaluate('scrollTo(0,0)')
    first=await state(page)
    await shot(page,f'{app}-{size}-long-top.png')
    await page.locator('#preview-note').hover()
    await page.mouse.wheel(0,1600)
    await page.wait_for_timeout(300)
    bottom=await state(page)
    await shot(page,f'{app}-{size}-long-bottom.png')
    await page.locator('#flip').focus()
    await page.keyboard.press('Shift+Tab')
    keyfocus=await page.evaluate('document.activeElement.id')
    await page.keyboard.press('Home')
    await page.wait_for_timeout(100)
    keyhome=await state(page)
    await page.keyboard.press('End')
    await page.wait_for_timeout(150)
    keyend=await state(page)
    await page.locator('#save').click()
    await page.wait_for_timeout(1700)
    savedstatus=await page.locator('#status').inner_text()
    await page.locator('#saved-link').click()
    await page.wait_for_timeout(300)
    saved=await state(page)
    await shot(page,f'{app}-{size}-long-saved.png')
    out={'note':note,'note_length':len(note),'initial':before,'top':first,'bottom':bottom,'keyboard_focus':keyfocus,'keyboard_home':keyhome,'keyboard_end':keyend,'save_status':savedstatus,'saved_view':saved,'saved_full_match':await page.locator('#saved-text').inner_text()==note}
    await ctx.close()
    return out

async def save_case(browser,app,port):
    ctx=await browser.new_context(viewport={'width':1440,'height':900})
    await ctx.add_init_script(STORAGE_INIT)
    page=await ctx.new_page()
    await page.goto(f'http://127.0.0.1:{port}/',wait_until='networkidle')
    a='Snapshot A: the note present when Save was pressed.'
    b='Snapshot B: a newer thought typed while the earlier note is still saving.'
    c='FAILURE DRAFT: '+LONG_EN[:550]+' END-FAILURE'
    await page.locator('#note-text').fill(a)
    await page.evaluate('window.__reviewDelay=true')
    await page.locator('#save').click()
    saving=await state(page)
    await page.wait_for_timeout(100)
    await page.locator('#note-text').fill(b)
    await page.locator('#note-text').evaluate('(e)=>e.setSelectionRange(12,19)')
    during=await state(page)
    await shot(page,f'{app}-desktop-delayed-edit.png')
    await page.wait_for_timeout(2700)
    after=await state(page)
    events=await page.evaluate('({storage:window.__storageEvents,timers:window.__timerEvents})')
    await shot(page,f'{app}-desktop-delayed-result.png')
    await page.locator('#saved-link').click()
    await page.wait_for_timeout(200)
    saved_a=await page.locator('#saved-text').inner_text()
    await shot(page,f'{app}-desktop-delayed-saved-view.png')
    await page.locator('#return').click()
    await page.wait_for_timeout(200)
    returned=await state(page)
    await page.reload(wait_until='networkidle')
    reloaded=await state(page)
    # Establish a known committed baseline before quota failure, without assuming reload keeps drafts.
    await page.locator('#note-text').fill(b)
    await page.locator('#save').click()
    await page.wait_for_timeout(1700)
    baseline=await state(page)
    await page.locator('#note-text').fill(c)
    quota=await page.evaluate('''() => {const key='__review_quota__';let lo=0,hi=6*1024*1024;while(lo<hi){let n=Math.ceil((lo+hi)/2);try{localStorage.setItem(key,'Q'.repeat(n));lo=n}catch(e){if(e.name!=='QuotaExceededError')throw e;hi=n-1}}localStorage.setItem(key,'Q'.repeat(lo));let probe;try{localStorage.setItem('__review_probe__','x');probe='unexpected success';localStorage.removeItem('__review_probe__')}catch(e){probe={name:e.name,message:e.message}}return {storedLength:lo,probe}}''')
    await page.locator('#save').click()
    await page.wait_for_timeout(1700)
    failure=await state(page)
    failure_events=await page.evaluate('window.__storageEvents.filter(e=>!e.key.startsWith("__review"))')
    await shot(page,f'{app}-desktop-real-quota-failure.png')
    await page.locator('#saved-link').click()
    await page.wait_for_timeout(200)
    failure_saved=await state(page)
    await shot(page,f'{app}-desktop-failure-saved-view.png')
    await page.locator('#return').click()
    await page.wait_for_timeout(200)
    failure_return=await state(page)
    await page.evaluate('localStorage.removeItem("__review_quota__")')
    retry_visible=await page.locator('#retry').is_visible()
    if retry_visible:await page.locator('#retry').click()
    else:await page.locator('#save').click()
    await page.wait_for_timeout(1700)
    recovery=await state(page)
    await shot(page,f'{app}-desktop-quota-recovered.png')
    await page.reload(wait_until='networkidle')
    recovery_reload=await state(page)
    await page.locator('#saved-link').click()
    recovered_saved=await page.locator('#saved-text').inner_text()
    out={'snapshot_a':a,'draft_b':b,'failure_draft':c,'saving':saving,'during_edit':during,'after_delay':after,'delay_events':events,'saved_view_during_newer_draft':saved_a,'return_after_delay':returned,'reload_after_unsaved_draft':reloaded,'baseline':baseline,'quota':quota,'failure':failure,'product_storage_events':failure_events,'saved_view_after_failure':failure_saved,'return_after_failure':failure_return,'retry_visible':retry_visible,'recovery':recovery,'recovery_reload':recovery_reload,'recovered_saved_exact_match':recovered_saved==c}
    await ctx.close()
    return out

async def motion_case(browser,app,port,reduced=False):
    ctx=await browser.new_context(viewport={'width':390 if reduced else 1440,'height':844 if reduced else 900},reduced_motion='reduce' if reduced else 'no-preference')
    page=await ctx.new_page()
    await page.goto(f'http://127.0.0.1:{port}/',wait_until='networkidle')
    if reduced:
        await page.locator('#locale-toggle').click()
        await page.locator('#theme-toggle').click()
    initial=await state(page)
    motion_ui=await page.locator('#motion-toggle').evaluate('(e)=>({text:e.innerText,disabled:e.disabled,pressed:e.getAttribute("aria-pressed")})')
    await page.evaluate(TRACE_JS)
    await page.locator('#flip').click()
    await page.wait_for_timeout(45)
    await page.keyboard.press('Shift+Tab')
    early=await state(page)
    await shot(page,f'{app}-{"reduced" if reduced else "normal"}-early-focus.png',False)
    await page.wait_for_timeout(900)
    settled=await state(page)
    trace=await page.evaluate('window.__traceRunning=false;({frames:window.__trace,clicks:window.__traceClicks})')
    await shot(page,f'{app}-{"reduced" if reduced else "normal"}-settled.png',False)
    if reduced:
        await page.locator('#note-text').fill('减少动态效果下，仍能写字、翻面并返回继续编辑。')
        await page.locator('#note-text').evaluate('(e)=>e.setSelectionRange(4,8)')
        await page.locator('#saved-link').click()
        await page.locator('#return').click()
        await page.wait_for_timeout(200)
        returned=await state(page)
        animations=await page.evaluate('document.getAnimations().map(a=>({playState:a.playState,type:a.constructor.name,duration:a.effect.getTiming().duration,target:a.effect.target.id||a.effect.target.className}))')
        out={'initial':initial,'motion_ui':motion_ui,'early':early,'settled':settled,'trace':trace,'return':returned,'animations':animations}
    else:
        await page.locator('#flip').click()
        await page.wait_for_timeout(900)
        await page.evaluate(TRACE_JS)
        box=await page.locator('#flip').bounding_box()
        for i in range(5):
            await page.mouse.click(box['x']+box['width']/2,box['y']+box['height']/2)
            await page.wait_for_timeout(100)
        await page.wait_for_timeout(1200)
        quick=await state(page)
        quicktrace=await page.evaluate('window.__traceRunning=false;({frames:window.__trace,clicks:window.__traceClicks})')
        await shot(page,f'{app}-normal-rapid-settled.png',False)
        await page.locator('#motion-toggle').click()
        pause_a=await page.locator('#orbit-dot').evaluate('(e)=>({rect:e.getBoundingClientRect().toJSON(),animations:document.getAnimations().map(a=>({playState:a.playState,type:a.constructor.name}))})')
        await page.wait_for_timeout(300)
        pause_b=await page.locator('#orbit-dot').evaluate('(e)=>({rect:e.getBoundingClientRect().toJSON(),animations:document.getAnimations().map(a=>({playState:a.playState,type:a.constructor.name}))})')
        out={'initial':initial,'motion_ui':motion_ui,'early':early,'settled':settled,'trace':trace,'rapid':quick,'rapid_trace':quicktrace,'pause_a':pause_a,'pause_b':pause_b}
    await ctx.close()
    return out

async def main():
    report=json.loads((ROOT/'checks.json').read_text()) if (ROOT/'checks.json').exists() else {}
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=EXE,headless=True,args=['--no-sandbox'])
        for app,port in APPS:
            if sys.argv[1:] and app not in sys.argv[1:]:continue
            report.setdefault(app,{})
            for name,fn in [('long_desktop',lambda:long_case(browser,app,port,'desktop')),('long_mobile_zh_dark',lambda:long_case(browser,app,port,'mobile')),('save',lambda:save_case(browser,app,port)),('motion',lambda:motion_case(browser,app,port)),('reduced',lambda:motion_case(browser,app,port,True))]:
                print(f'START {app} {name}',flush=True)
                try:report[app][name]=await fn()
                except Exception as e:
                    report[app][name]={'harness_or_check_error':str(e),'traceback':traceback.format_exc()}
                    print(traceback.format_exc(),flush=True)
                (ROOT/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
                print(f'DONE {app} {name}',flush=True)
        await browser.close()
    print('ALL DONE',flush=True)

asyncio.run(main())
