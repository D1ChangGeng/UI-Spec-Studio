#!/usr/bin/env python3
"""Exercise the bilingual content/UX writing fixture through an actual HTTP browser."""
from __future__ import annotations
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import threading

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT/'examples/content-review'
VIEWS = ((390,844),(768,1024),(1280,800),(1920,1080))

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass


def rgb(css):
    return list(map(int,re.findall(r'\d+',css)[:3]))

def contrast(a,b):
    def lum(vals):
        l=[]
        for n in vals:
            c=n/255
            l.append(c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4)
        return sum(n*w for n,w in zip(l,(.2126,.7152,.0722)))
    x,y=sorted([lum(a),lum(b)])
    return (y+.05)/(x+.05)

def validate(output:Path,browser_path:str|None=None,in_memory:bool=False)->dict:
    from playwright.sync_api import sync_playwright,expect
    output=output.resolve();output.mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(EXAMPLE)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    origin=f'http://127.0.0.1:{server.server_port}'
    document=(EXAMPLE/'index.html').read_text(encoding='utf-8')
    if in_memory:
        css=(EXAMPLE/'styles.css').read_text(encoding='utf-8')
        js=(EXAMPLE/'app.js').read_text(encoding='utf-8')
        shim='''<script>(()=>{const __fakeValues = Object.create(null); Object.defineProperty(window, 'localStorage', {configurable:true,value:{setItem(k,v){__fakeValues[k]=String(v)},getItem(k){return __fakeValues[k] ?? null},removeItem(k){delete __fakeValues[k]}}});})();</script>'''
        document=document.replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>')
        document=document.replace('<script src="app.js"></script>',shim+'<script>'+js+'</script>')
    report={'renderer':'in-memory' if in_memory else 'local-http','scope':'Authored bilingual fixture; in-memory mode uses a simulated storage object; production outcomes and user comprehension are separate','storage_verified':False,'captures':[], 'tests':[], 'page_errors':[], 'external_requests':[], 'result':'pending'}
    try:
        with sync_playwright() as p:
            kw={'headless':True}
            if browser_path:kw['executable_path']=browser_path
            browser=p.chromium.launch(**kw)
            context=browser.new_context(locale='zh-CN',device_scale_factor=1)
            page=context.new_page();page.set_default_timeout(12000)
            page.on('pageerror',lambda err:report['page_errors'].append(str(err)))
            page.on('request',lambda req:report['external_requests'].append(req.url) if not req.url.startswith(origin+'/') else None)
            def load(lang,theme):
                page.set_content(document,wait_until='load') if in_memory else page.goto(origin+'/index.html',wait_until='load')
                if not in_memory:
                    page.evaluate("localStorage.removeItem('ui-spec-content-note-v1')")
                    page.reload()
                if lang=='en':page.locator('#locale-toggle').click()
                if theme=='dark':page.locator('#theme-toggle').click()
                page.evaluate('document.fonts.ready')
            def capture(name,**extra):
                page.screenshot(path=str(output/(name+'.png')),full_page=False)
                report['captures'].append({'name':name,'viewport':page.viewport_size,**extra})
                if page.viewport_size['width'] in (390,1280) and 'error-' not in name and 'failed-' not in name:
                    page.screenshot(path=str(output/(name+'-full.png')),full_page=True)
            for lang in ('zh','en'):
                for theme in ('light','dark'):
                    for w,h in VIEWS:
                        page.set_viewport_size({'width':w,'height':h});load(lang,theme)
                        expect(page.locator('#main-title')).to_have_text('把研究线索整理成笔记' if lang=='zh' else 'Turn a research lead into a note')
                        expect(page.locator('#save')).to_contain_text('保存笔记' if lang=='zh' else 'Save note')
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'),(lang,theme,w)
                        assert page.locator('#note-title').get_attribute('aria-describedby')=='title-hint title-error'
                        assert page.locator('#note-title').get_attribute('aria-required')=='true'
                        pair=page.locator('body').evaluate('(e)=>({text:getComputedStyle(e).color,background:getComputedStyle(e).backgroundColor})')
                        ratio=contrast(rgb(pair['text']),rgb(pair['background']));assert ratio>=7,(lang,theme,ratio)
                        # Text geometry should retain normal flow at real widths.
                        title=page.locator('#main-title').bounding_box()
                        assert title and title['width']>=180 and title['x']>=0
                        assert page.locator('#save').bounding_box()['width']>=100
                        capture(f'{lang}-{theme}-{w}',lang=lang,theme=theme,body_contrast=ratio)
                        report['tests'].append(f'{lang}/{theme}/{w}: wording, label, contrast, geometry, overflow')
                    page.set_viewport_size({'width':390,'height':844});load(lang,theme)
                    page.locator('#save').click()
                    expect(page.locator('#note-title')).to_be_focused()
                    expect(page.locator('#title-error')).to_be_visible()
                    expect(page.locator('#note-title')).to_have_attribute('aria-invalid','true')
                    expect(page.locator('#title-error')).to_have_text('填写笔记标题后再保存。' if lang=='zh' else 'Add a note title before saving.')
                    capture(f'error-{lang}-{theme}',lang=lang,theme=theme)
                    page.locator('#note-title').fill('城市供热需要核查的需求变化' if lang=='zh' else 'Demand changes to verify in district heating')
                    page.locator('#note-body').fill('来源仍需要核查' if lang=='zh' else 'Sources still need checking')
                    page.locator('#save').click()
                    expect(page.locator('#state-message')).to_have_text('笔记已保存在此浏览器。' if lang=='zh' else 'Note saved in this browser.')
                    expect(page.locator('#recent-title')).to_have_text('城市供热需要核查的需求变化' if lang=='zh' else 'Demand changes to verify in district heating')
                    capture(f'saved-{lang}-{theme}',lang=lang,theme=theme)
                    if not in_memory:
                        page.reload(); report['storage_verified']=True
                        expect(page.locator('#note-title')).to_have_value('城市供热需要核查的需求变化' if lang=='zh' else 'Demand changes to verify in district heating')
                    report['tests'].append(f'{lang}/{theme}: error, feedback, saved data and reload')
                    # Locale switch preserves entered content, updates the copy and the semantic direction.
                    page.locator('#locale-toggle').click();expect(page.locator('html')).to_have_attribute('lang','en' if lang=='zh' else 'zh-CN')
                    expect(page.locator('#note-title')).not_to_be_empty()
                    # Return to the intended locale and trigger a visible storage error.
                    page.locator('#locale-toggle').click()
                    page.locator('.fixture-controls summary').click();page.locator('#simulate-failure').check()
                    page.locator('#note-title').fill('等待保存的笔记' if lang=='zh' else 'Note awaiting save')
                    page.locator('#save').click()
                    expect(page.locator('#state-message')).to_have_text('当前无法保存这份笔记。输入内容仍在页面中。' if lang=='zh' else 'This note could not be saved. Your text is still here.')
                    expect(page.locator('#retry')).to_be_visible()
                    capture(f'failed-{lang}-{theme}',lang=lang,theme=theme)
                    page.locator('#simulate-failure').uncheck();page.locator('#retry').click()
                    expect(page.locator('#state-message')).to_have_text('笔记已保存在此浏览器。' if lang=='zh' else 'Note saved in this browser.')
                    expect(page.locator('#recent-title')).to_have_text('等待保存的笔记' if lang=='zh' else 'Note awaiting save')
                    page.locator('#long-example').click()
                    assert len(page.locator('#note-title').input_value())>(35 if lang=='zh' else 70)
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
                    report['tests'].append(f'{lang}/{theme}: locale, failure/retry, long-content reflow')
            assert not report['page_errors'],report['page_errors']
            assert not report['external_requests'],report['external_requests']
            report['result']='preview_pass_storage_pending' if in_memory else 'pass'; report['browser_version']=browser.version
            context.close();browser.close()
    except Exception as error:
        report['result']='fail';report['detail']=str(error)
        raise
    finally:
        server.shutdown();server.server_close()
        (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir',required=True,type=Path)
    ap.add_argument('--browser-path')
    ap.add_argument('--in-memory',action='store_true',help='Inline assets and simulated storage for restricted browser preview; persistence remains unverified')
    args=ap.parse_args()
    result=validate(args.output_dir,args.browser_path,args.in_memory)
    print(json.dumps({'result':result['result'],'captures':len(result['captures']),'tests':len(result['tests']),'storage_verified':result['storage_verified'],'scope':result['scope']},ensure_ascii=False,indent=2))
