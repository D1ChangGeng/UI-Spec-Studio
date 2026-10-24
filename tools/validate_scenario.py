#!/usr/bin/env python3
"""Exercise the authored page-foundation study; report each evidence scope."""
from __future__ import annotations
import argparse
import base64
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import threading
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / 'examples/product-intent'
VIEWS = ((390,844),(768,1024),(1280,720),(1920,1080))

def contrast(a, b):
    def lum(rgb):
        c=[v/255/12.92 if v/255<=.04045 else ((v/255+.055)/1.055)**2.4 for v in rgb]
        return sum(x*w for x,w in zip(c,(.2126,.7152,.0722)))
    x,y=sorted((lum(a),lum(b)));return (y+.05)/(x+.05)

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def validate(output: Path, browser_path=None, in_memory=False, source_preview=False):
    from playwright.sync_api import sync_playwright, expect
    output=output.resolve();output.mkdir(parents=True,exist_ok=True)
    foundation=json.loads((SCENARIO/'foundation.json').read_text(encoding='utf-8'))
    report={'scope':'Authored native design port; original product approval and upstream React runtime integration remain separate',
            'renderer':'in-memory' if in_memory else 'local-http', 'owner_approval':'pending',
            'storage_verified':False,'foundation':foundation,'captures':[],'checks':[],'errors':[],
            'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SCENARIO.iterdir() if p.is_file()}}
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(SCENARIO)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    origin=f'http://127.0.0.1:{server.server_port}'
    document=(SCENARIO/'index.html').read_text(encoding='utf-8')
    style=(SCENARIO/'styles.css').read_text().replace('@import url("tokens.css");',(SCENARIO/'tokens.css').read_text())
    document=document.replace('<link rel="stylesheet" href="styles.css">','<style>'+style+'</style>').replace('<script src="app.js"></script>','<script>'+(SCENARIO/'app.js').read_text(encoding='utf-8')+'</script>')
    try:
        with sync_playwright() as p:
            options={'headless':True}
            if browser_path:options['executable_path']=browser_path
            browser=p.chromium.launch(**options);report['browser']=browser.version
            context=browser.new_context(locale='zh-CN',device_scale_factor=1)
            page=context.new_page();page.set_default_timeout(12000)
            page.on('pageerror',lambda error:report['errors'].append(str(error)))
            external=[]
            page.on('request',lambda request:external.append(request.url) if not request.url.startswith(origin+'/') else None)
            def load(theme='light'):
                if in_memory:page.set_content(document,wait_until='load')
                else:page.goto(origin+'/index.html',wait_until='load')
                if theme=='dark':page.locator('#theme').click()
                page.evaluate('document.fonts.ready')
            def capture(name,**facts):
                page.screenshot(path=str(output/(name+'.png')))
                report['captures'].append({'name':name,'viewport':page.viewport_size,**facts})
            for theme in ('light','dark'):
                for model in ('conversation','documents'):
                    for w,h in VIEWS:
                        page.set_viewport_size({'width':w,'height':h});load(theme)
                        if model=='documents':page.locator('input[value=documents]').check()
                        expect(page.locator('#preference')).to_contain_text('待确认')
                        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
                        assert not page.evaluate('document.documentElement.scrollHeight>innerHeight+1')
                        pair=page.locator('body').evaluate('(e)=>({ink:getComputedStyle(e).color,bg:getComputedStyle(e).backgroundColor})')
                        rgb=lambda s:list(map(int,re.findall(r"\d+",s)[:3]))
                        ratio=contrast(rgb(pair['ink']),rgb(pair['bg']));assert ratio>=4.5
                        if model=='conversation':
                            expect(page.locator('#composer')).to_be_visible()
                            assert page.locator('#composer').evaluate('(e)=>getComputedStyle(e).borderRadius')=='28px'
                            assert page.locator('#conversation').bounding_box()['width']<=769
                            assert page.locator('.welcome h1').evaluate('(e)=>getComputedStyle(e).fontWeight')=='400'
                        capture(f'{model}-{theme}-{w}',theme=theme,model=model,body_contrast=ratio)
                        page.locator('#decision-open').click();expect(page.locator('#decision-dialog')).to_be_visible()
                        expect(page.locator('[data-foundation="assistant-ui-chatgpt"]')).to_have_count(1)
                        assert page.locator('#decision-dialog a[href^="https://"]').count()>=7
                        if model=='conversation' and w in (390,1280):capture(f'decisions-{theme}-{w}',theme=theme)
                        page.keyboard.press('Escape');expect(page.locator('#decision-open')).to_be_focused()
                        if w==390:
                            page.locator('#history').click();expect(page.locator('#history-dialog')).to_be_visible()
                            page.keyboard.press('Escape');expect(page.locator('#history')).to_be_focused()
                        report['checks'].append(f'{model}/{theme}/{w}: viewport, authority, foundation geometry, contrast, record and focus')
            page.set_viewport_size({'width':1280,'height':720})
            for theme in ('light','dark'):
                load(theme)
                page.locator('[data-prompt]').first.click();expect(page.locator('#send')).to_be_enabled()
                page.evaluate("() => {window.inputFrame=null;document.querySelector('#question').addEventListener('input',()=>{const t=performance.now();requestAnimationFrame(()=>window.inputFrame=performance.now()-t);},{once:true});}")
                page.locator('#question').fill('城市供热如何降低高峰负荷？');page.wait_for_function('window.inputFrame!==null')
                report.setdefault('input_to_next_frame_ms',{})[theme]=page.evaluate('window.inputFrame')
                page.locator('#question').press('Control+Enter');expect(page.locator('.answer')).to_have_count(1)
                page.locator('.source-button').click();expect(page.locator('#source-dialog')).to_be_visible()
                page.keyboard.press('Escape');expect(page.locator('.source-button')).to_be_focused()
                capture(f'answer-{theme}',theme=theme)
                if theme=='light':
                    thumb=page.screenshot(type='jpeg',quality=45)
                    print('ADAPTED_PREVIEW_JPEG_BASE64='+base64.b64encode(thumb).decode())
                page.locator('.testbar summary').click();page.locator('#response').select_option('slow')
                page.locator('#question').fill('请求中的问题');page.locator('#send').click();page.locator('#question').fill('回复到达前输入的新草稿')
                expect(page.locator('.answer')).to_have_count(2);expect(page.locator('#question')).to_have_value('回复到达前输入的新草稿')
                page.locator('#send').click();page.locator('#stop').click();page.wait_for_timeout(1900)
                expect(page.locator('.answer')).to_have_count(2);expect(page.locator('#question')).to_have_value('回复到达前输入的新草稿')
                page.locator('#response').select_option('error');page.locator('#send').click();expect(page.locator('.error')).to_be_visible()
                capture(f'error-{theme}',theme=theme)
                page.locator('#response').select_option('ready');page.get_by_role('button',name='重试',exact=True).click()
                expect(page.locator('.error')).to_have_count(0);expect(page.locator('.answer')).to_have_count(3)
                page.locator('#response').select_option('slow');page.locator('#question').fill('切换期间请求');page.locator('#send').click()
                page.locator('input[value=documents]').check();page.wait_for_timeout(1900)
                expect(page.locator('.answer')).to_have_count(3);expect(page.locator('.pending')).to_have_count(0)
                page.locator('[data-doc]').first.click();page.locator('#note-body').fill('已编辑的本地示例内容')
                page.locator('#save-note').click();expect(page.locator('#save-status')).to_contain_text('保存不可用' if in_memory else '已保存')
                capture(f'edited-{theme}',theme=theme)
                if not in_memory:
                    page.reload();page.locator('input[value=documents]').check();page.locator('[data-doc]').first.click()
                    expect(page.locator('#note-body')).to_have_value('已编辑的本地示例内容');report['storage_verified']=True
                    if theme=='dark':page.locator('#theme').click()
                page.locator('#back').click();page.locator('input[value=conversation]').check()
                if page.locator('.testbar details').get_attribute('open') is None:page.locator('.testbar summary').click()
                page.locator('#response').select_option('long');page.locator('#question').fill('长内容测试');page.locator('#send').click()
                expect(page.locator('.answer').last.locator('p')).to_have_count(10)
                assert page.locator('#thread').evaluate('(e)=>e.scrollHeight>e.clientHeight')
                page.locator('#thread').evaluate('(e)=>e.scrollTop=e.scrollHeight')
                assert page.locator('#composer').bounding_box()['y']>=0
                capture(f'long-{theme}',theme=theme)
                page.emulate_media(reduced_motion='reduce')
                assert page.locator('#theme').evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
                page.emulate_media(reduced_motion='no-preference')
                report['checks'].append(f'{theme}: keyboard send, source/focus, new draft, cancel, failure/retry, stale result, local note, long reading, reduced motion')
            report['external_requests']=external;assert not external;assert not report['errors']
            report['result']='preview_pass_storage_pending' if in_memory else 'pass'
            context.close()
            if source_preview:
                observation={'url':'https://www.assistant-ui.com/demos/chatgpt','scope':'Public upstream page observation; independent of pinned code and adapted fixture'}
                try:
                    base='https://raw.githubusercontent.com/assistant-ui/assistant-ui/'+foundation['source_commit']+'/'
                    with urllib.request.urlopen(base+foundation['source_path'],timeout=30) as response: source=response.read()
                    digest=hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest()
                    if digest!=foundation['source_blob']:raise ValueError('Pinned upstream source bytes differ')
                    (output/'upstream-chatgpt.tsx.txt').write_bytes(source)
                    with urllib.request.urlopen(base+'LICENSE',timeout=30) as response:(output/'UPSTREAM-LICENSE.txt').write_bytes(response.read())
                    observation['source_blob_verified']=digest
                    upstream=browser.new_context(viewport={'width':1280,'height':900},color_scheme='light')
                    screen=upstream.new_page();screen.goto(observation['url'],wait_until='domcontentloaded',timeout=45000)
                    screen.wait_for_timeout(3000);screen.screenshot(path=str(output/'upstream-page.png'))
                    small=screen.screenshot(type='jpeg',quality=45)
                    print('SOURCE_PREVIEW_JPEG_BASE64='+base64.b64encode(small).decode())
                    observation['screenshot']='upstream-page.png';observation['status']='observed';upstream.close()
                except Exception as error:
                    observation['status']='unavailable';observation['detail']=str(error)
                report['upstream_observation']=observation
            browser.close()
    except Exception as error:
        report['result']='fail';report['errors'].append(str(error));raise
    finally:
        server.shutdown();server.server_close()
        (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--browser-path');p.add_argument('--in-memory',action='store_true');p.add_argument('--source-preview',action='store_true')
    a=p.parse_args();r=validate(a.output_dir,a.browser_path,a.in_memory,a.source_preview)
    print(json.dumps({'result':r['result'],'captures':len(r['captures']),'checks':len(r['checks']),'storage_verified':r['storage_verified'],'scope':r['scope']},ensure_ascii=False,indent=2))
