import os, json, time, traceback, hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'review-output'
CAP = OUT / 'captures'
os.environ['FONTCONFIG_FILE']='/workspace/scratch/43b440780c87/preview-fontconfig.xml'
os.environ['PLAYWRIGHT_BROWSERS_PATH']='/workspace/scratch/43b440780c87/playwright-cache'
BROWSER='/workspace/scratch/43b440780c87/playwright-cache/chrome-headless-shell-linux64/chrome-headless-shell'
TITLE='Field notebook: shade, seating and slow routes — 城市步行中的树荫、座椅与停留时间'
SHORTS=[('A bench to revisit','Return at 17:30. Compare shade and seating.'),('雨天的入口观察','下次记录雨棚、座椅与图书馆入口之间的距离。不要将观察误写成结论。'),('Source checklist','Check date, method, climate, and instrument height before comparing evidence.')]
PARA='The afternoon route follows the library, a narrow street and an open square. Record where people pause, then distinguish observation from interpretation. A shaded seat may invite a longer rest, but proximity to a bus stop could explain the same pattern. Check the timing before describing a cause.'
ZH='观察计划：沿图书馆、街角和广场行走，记录人们何时停留、何时继续前行。树荫与座椅可能共同影响选择，但公交到站时间、天气和无障碍通行也需要核查。把现场观察与研究者的解释分开；不要把暂时的线索写成确定结论。'
BODY='SYNTHETIC FIELDWORK · microclimate-53\n\nQuestion / 研究问题\nHow do shade and places to pause shape a short walk?\n树荫与可停留的地方，如何改变一次短途步行？\n\n'+'\n\n'.join(f'{i+1}. English observation\n{PARA}\n\n中文观察\n{ZH}' for i in range(7))+'\n\nNext visit / 下一步\nCompare midday and late afternoon. 所有内容均为虚构测试资料。'
DRAFT=BODY+'\n\nUNSAVED DRAFT / 未保存的补充：请在下次核查雨天路线。'

results={'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'content':{'title':TITLE,'body_length':len(BODY),'body':BODY,'draft':DRAFT,'short_notes':SHORTS},'variants':{},'source_hashes_before':{}}
for p in ROOT.glob('variant-*/*/*'):
    if p.is_file(): results['source_hashes_before'][str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()

def snap(page,variant,name):
    path=CAP/f'{variant}-{name}.png'
    page.screenshot(path=str(path),full_page=False)
    return str(path.relative_to(ROOT))

def state(page):
    return page.evaluate('''() => ({title:document.querySelector('#note-title').value,body:document.querySelector('#note-body').value,density:document.documentElement.dataset.density,theme:document.documentElement.dataset.theme,lang:document.documentElement.lang,selected:[...document.querySelectorAll('#note-list [aria-current="true"]')].map(e=>({text:e.innerText,id:e.dataset.id||e.dataset.noteId})),status:[...document.querySelectorAll('[role="status"]')].filter(e=>e.getClientRects().length).map(e=>e.innerText),viewport:{width:innerWidth,height:innerHeight,scrollWidth:document.documentElement.scrollWidth},focus:document.activeElement.id})''')

def metrics(page):
    return page.evaluate('''() => Object.fromEntries(['#note-title','#note-body','#density','.collection','.editor','#note-list button','.editor-toolbar'].map(s=>{let e=document.querySelector(s);if(!e)return[s,null];let b=e.getBoundingClientRect(),c=getComputedStyle(e);return [s,{x:b.x,y:b.y,width:b.width,height:b.height,font:c.fontFamily,fontSize:c.fontSize,lineHeight:c.lineHeight,clientHeight:e.clientHeight,scrollHeight:e.scrollHeight,overflowY:c.overflowY}]}))''')

def assertcheck(v,name,condition,details=None):
    v['checks'].append({'name':name,'pass':bool(condition),'details':details})

def scrolltop(page):
    page.evaluate('''() => {window.scrollTo(0,0);for(const s of ['.writing-area','.editor-scroll','#note-body']){const e=document.querySelector(s);if(e)e.scrollTop=0}}''')

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=BROWSER,headless=True,args=['--no-sandbox'])
    for i in range(1,4):
        variant=f'variant-{i:02d}'
        v={'checks':[],'captures':[],'page_errors':[],'states':{},'metrics':{}}
        results['variants'][variant]=v
        context=browser.new_context(viewport={'width':1440,'height':900},locale='en-US')
        page=context.new_page();page.set_default_timeout(5000)
        page.on('pageerror',lambda e: v['page_errors'].append(str(e)))
        try:
            page.goto(f'http://127.0.0.1:{8210+i}/final/');page.wait_for_timeout(200)
            v['captures'].append(snap(page,variant,'desktop-initial'))
            v['default_note_count']=page.locator('#note-list button').count()
            # Remove the automatically supplied examples through normal deletion UI.
            if i==3:
                for _ in range(v['default_note_count']):
                    page.locator('#note-list button').first.click()
                    page.locator('#delete-note').click()
                    page.locator('#confirm-delete').click()
            if page.locator('html').get_attribute('lang')!='en':page.locator('#locale-toggle').click()
            for title,body in SHORTS+[(TITLE,BODY)]:
                page.locator('#new-note').click()
                page.locator('#note-title').fill(title)
                if page.locator('#note-context').count():page.locator('#note-context').fill('Urban fieldwork / 城市观察')
                page.locator('#note-body').fill(body)
                page.keyboard.press('Control+s');page.wait_for_timeout(250)
            assertcheck(v,'create_four_notes',page.locator('#note-list button').count()==4,page.locator('#note-list').inner_text())
            scrolltop(page)
            v['captures'].append(snap(page,variant,'desktop-comfortable-long'))
            v['metrics']['desktop_comfortable']=metrics(page)
            # Draft and selected note must survive each appearance change.
            page.locator('#note-body').fill(DRAFT)
            original=state(page);v['states']['before_preferences']=original
            page.locator('#density').select_option('compact')
            after=state(page);assertcheck(v,'draft_and_selection_survive_density',after['body']==DRAFT and after['title']==TITLE and after['selected']==original['selected'],after)
            scrolltop(page);v['captures'].append(snap(page,variant,'desktop-compact-draft'));v['metrics']['desktop_compact']=metrics(page)
            page.locator('#theme-toggle').click()
            after=state(page);assertcheck(v,'draft_and_selection_survive_theme',after['body']==DRAFT and after['title']==TITLE and after['selected']==original['selected'],after)
            page.locator('#locale-toggle').click()
            after=state(page);assertcheck(v,'draft_and_selection_survive_language',after['body']==DRAFT and after['title']==TITLE and len(after['selected'])==1 and after['selected'][0]['id']==original['selected'][0]['id'],after)
            scrolltop(page);v['captures'].append(snap(page,variant,'desktop-dark-chinese-draft'))
            page.reload();page.wait_for_timeout(200)
            after=state(page);v['states']['draft_reload']=after
            assertcheck(v,'density_theme_language_persist_reload',after['density']=='compact' and after['theme']=='dark' and after['lang'].startswith('zh'),after)
            assertcheck(v,'unsaved_draft_survives_reload',after['body']==DRAFT and after['title']==TITLE,after)
            page.locator('#theme-toggle').click();page.locator('#locale-toggle').click()
            # Save and find by body token, then reopen after selecting a different note.
            page.locator('#save').click();page.wait_for_timeout(250)
            page.locator('#note-list button').filter(has_text='A bench to revisit').click()
            page.locator('#search').fill('microclimate-53')
            assertcheck(v,'find_by_body',page.locator('#note-list button').count()==1,page.locator('#note-list').inner_text())
            page.locator('#note-list button').first.click()
            assertcheck(v,'reopen_long_saved_note',page.locator('#note-body').input_value()==DRAFT)
            page.locator('#search').fill('')
            page.reload();page.wait_for_timeout(200)
            # Some implementations do not persist selection, so reopen through the collection if needed.
            v['states']['saved_reload_initial_selection']=state(page)
            if page.locator('#note-title').input_value()!=TITLE:page.locator('#note-list button').filter(has_text=TITLE).click()
            assertcheck(v,'saved_content_survives_reload',page.locator('#note-body').input_value()==DRAFT)
            delete_selector='#delete-note' if i==3 else '#delete'
            dialog_selector='#confirm' if i==1 else '#delete-dialog'
            page.locator(delete_selector).click()
            v['states']['delete_dialog_text']=page.locator(dialog_selector).inner_text()
            assertcheck(v,'delete_identifies_note',TITLE in v['states']['delete_dialog_text'])
            v['captures'].append(snap(page,variant,'desktop-delete-cancel'))
            page.keyboard.press('Escape')
            assertcheck(v,'delete_cancel_retains_note_and_draft',page.locator('#note-body').input_value()==DRAFT and page.locator('#note-list button').count()==4)
            v['states']['delete_cancel_focus']=page.evaluate('document.activeElement.id')
            # Storage failure is injected into this browser context, not application source.
            page.evaluate('''() => {window.__reviewOriginalSetItem=Storage.prototype.setItem;Storage.prototype.setItem=function(){throw new DOMException('Review injected quota failure','QuotaExceededError')}}''')
            failedbody=DRAFT+'\nStorage failure probe / 存储失败检查'
            page.locator('#note-body').fill(failedbody)
            page.keyboard.press('Control+s');page.wait_for_timeout(300)
            v['states']['storage_failure']=state(page)
            scrolltop(page);v['captures'].append(snap(page,variant,'desktop-storage-failure'))
            assertcheck(v,'storage_failure_keeps_current_text',page.locator('#note-body').input_value()==failedbody)
            page.evaluate('Storage.prototype.setItem=window.__reviewOriginalSetItem')
            if page.locator('#retry').is_visible():page.locator('#retry').click()
            else:page.keyboard.press('Control+s')
            page.wait_for_timeout(300)
            page.reload();page.wait_for_timeout(200)
            if page.locator('#note-title').input_value()!=TITLE:page.locator('#note-list button').filter(has_text=TITLE).click()
            assertcheck(v,'storage_failure_recovery_saved_reload',page.locator('#note-body').input_value()==failedbody,state(page))
            # Return to identical long content for all comparison captures.
            page.locator('#note-body').fill(DRAFT);page.keyboard.press('Control+s');page.wait_for_timeout(250)
            page.locator('#density').select_option('comfortable')
            page.set_viewport_size({'width':390,'height':844})
            # The page may show collection after reload; use the actual row to enter editor.
            if not page.locator('#note-body').is_visible():page.locator('#note-list button').filter(has_text=TITLE).click()
            scrolltop(page);v['captures'].append(snap(page,variant,'mobile-comfortable-long'));v['metrics']['mobile_comfortable']=metrics(page)
            assertcheck(v,'mobile_no_horizontal_document_overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
            page.locator('#back').click();scrolltop(page)
            v['captures'].append(snap(page,variant,'mobile-comfortable-collection'))
            page.locator('#search').fill('雨天')
            assertcheck(v,'chinese_search',page.locator('#note-list button').count()>=1,page.locator('#note-list').inner_text())
            page.locator('#search').fill('microclimate-53');page.locator('#note-list button').first.click()
            assertcheck(v,'mobile_return_search_reopen',page.locator('#note-body').input_value()==DRAFT)
            page.locator('#density').select_option('compact');scrolltop(page)
            v['captures'].append(snap(page,variant,'mobile-compact-long'));v['metrics']['mobile_compact']=metrics(page)
            # Inspect an interior Chinese paragraph through manual wheel input.
            if i==3:
                page.locator('#note-body').hover();page.mouse.wheel(0,650)
            else:
                page.locator('#note-body').click();page.keyboard.press('Control+Home');page.keyboard.press('PageDown')
                page.locator('#note-body').hover();page.mouse.wheel(0,350)
            page.wait_for_timeout(150);v['captures'].append(snap(page,variant,'mobile-long-interior'))
            page.locator('#back').click();scrolltop(page)
            page.locator('#search').fill('');v['captures'].append(snap(page,variant,'mobile-compact-collection'))
            page.locator('#note-list button').filter(has_text=TITLE).click()
            page.locator('#note-body').fill(DRAFT+'\nMobile draft / 窄屏草稿')
            page.locator('#theme-toggle').click();page.locator('#locale-toggle').click();page.locator('#density').select_option('comfortable')
            assertcheck(v,'mobile_draft_survives_all_preferences',page.locator('#note-body').input_value()==DRAFT+'\nMobile draft / 窄屏草稿')
            scrolltop(page);v['captures'].append(snap(page,variant,'mobile-dark-chinese-draft'))
            page.locator(delete_selector).click();v['captures'].append(snap(page,variant,'mobile-delete-cancel'));page.keyboard.press('Escape')
            assertcheck(v,'mobile_delete_cancel_retains_draft',page.locator('#note-body').input_value()==DRAFT+'\nMobile draft / 窄屏草稿')
            context.storage_state(path=str(OUT/f'{variant}-state.json'))
        except Exception as e:
            v['original_failure']={'error':str(e),'traceback':traceback.format_exc()}
            v['captures'].append(snap(page,variant,'original-harness-failure'))
        finally:
            context.close()
        (OUT/'check-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    browser.close()
results['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
results['source_hashes_after']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob('variant-*/*/*') if p.is_file()}
results['sources_unchanged']=results['source_hashes_before']==results['source_hashes_after']
(OUT/'check-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps({k:{'checks':len(v['checks']),'failed':[c['name'] for c in v['checks'] if not c['pass']],'original_failure':v.get('original_failure'),'captures':len(v['captures'])} for k,v in results['variants'].items()},ensure_ascii=False,indent=2))
