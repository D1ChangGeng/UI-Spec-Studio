#!/usr/bin/env python3
"""Exercise the authored bilingual content fixture through an actual HTTP browser."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import threading

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/content-review'
VIEWS = ((390, 844), (768, 1024), (1280, 800), (1920, 1080))
KEY = 'ui-spec-content-note-v1'
COPY = {
    'zh': {
        'title': '把研究线索整理成笔记', 'save': '保存笔记',
        'missing': '填写笔记标题后再保存。', 'saving': '正在保存到此浏览器…',
        'saved': '笔记已保存在此浏览器。',
        'savedEarlier': '上一版已保存。当前修改仍需再次保存。',
        'failed': '当前无法保存这份笔记。输入内容仍在页面中。',
        'clearFailed': '未能清除本地演示数据。当前输入仍在页面中，请重试。',
        'resetDone': '本地演示数据已清除。',
        'readFailed': '暂时无法读取已保存的笔记。当前输入仍在页面中，请重试读取后再保存。',
        'invalidStored': '已保存的笔记数据无法识别。请在预览设置中清除本地演示数据后再保存。',
        'readRecoveredDraft': '已重新读取本地笔记。当前输入仍在页面中，保存后会替换已存内容。',
        'recentUnreadable': '暂时无法读取笔记',
    },
    'en': {
        'title': 'Turn a research lead into a note', 'save': 'Save note',
        'missing': 'Add a note title before saving.', 'saving': 'Saving in this browser…',
        'saved': 'Note saved in this browser.',
        'savedEarlier': 'An earlier version was saved. Save again to keep your new edits.',
        'failed': 'This note could not be saved. Your text is still here.',
        'clearFailed': 'Local demo data could not be cleared. Your text is still here. Try again.',
        'resetDone': 'Local demo data cleared.',
        'readFailed': 'Saved notes could not be read. Your text is still here. Try reading again before saving.',
        'invalidStored': 'The saved note data is not readable. Clear local demo data in the preview controls before saving.',
        'readRecoveredDraft': 'The local note has been read again. Your current text is still here. Saving will replace the stored note.',
        'recentUnreadable': 'Saved note unavailable',
    },
}


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def rgb(css):
    return list(map(int, re.findall(r'\d+', css)[:3]))


def contrast(a, b):
    def lum(values):
        values = [n / 255 for n in values]
        values = [n / 12.92 if n <= .04045 else ((n + .055) / 1.055) ** 2.4 for n in values]
        return sum(n * weight for n, weight in zip(values, (.2126, .7152, .0722)))
    low, high = sorted((lum(a), lum(b)))
    return (high + .05) / (low + .05)


def validate(output: Path, browser_path: str | None = None, in_memory: bool = False) -> dict:
    from playwright.sync_api import sync_playwright, expect

    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(EXAMPLE)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    document = (EXAMPLE / 'index.html').read_text(encoding='utf-8')
    if in_memory:
        css = (EXAMPLE / 'styles.css').read_text(encoding='utf-8')
        js = (EXAMPLE / 'app.js').read_text(encoding='utf-8')
        shim = '''<script>(()=>{const values=Object.create(null);Object.defineProperty(window,'localStorage',{configurable:true,value:{setItem(k,v){values[k]=String(v)},getItem(k){return values[k]??null},removeItem(k){delete values[k]}}});})();</script>'''
        document = document.replace('<link rel="stylesheet" href="styles.css">', '<style>' + css + '</style>')
        document = document.replace('<script src="app.js"></script>', shim + '<script>' + js + '</script>')
    report = {
        'renderer': 'in-memory' if in_memory else 'local-http',
        'scope': 'Authored bilingual fixture: browser mechanics, content/state assertions and captures. In-memory storage is simulated. Visual judgment, user comprehension and production-service performance need their own evidence.',
        'storage_verified': False, 'visual_review': 'captures_ready_for_inspection',
        'captures': [], 'tests': [], 'skipped': [], 'page_errors': [], 'external_requests': [], 'result': 'pending',
    }
    try:
        with sync_playwright() as playwright:
            launch = {'headless': True}
            if browser_path:
                launch['executable_path'] = browser_path
            browser = playwright.chromium.launch(**launch)
            context = browser.new_context(locale='zh-CN', device_scale_factor=1)
            page = context.new_page()

            def observe(target):
                target.set_default_timeout(12000)
                target.on('pageerror', lambda error: report['page_errors'].append(str(error)))
                target.on('request', lambda request: report['external_requests'].append(request.url)
                          if not request.url.startswith(origin + '/') else None)

            observe(page)

            def variant(lang, theme):
                if page.locator('html').get_attribute('lang') != ('zh-CN' if lang == 'zh' else 'en'):
                    page.locator('#locale-toggle').click()
                if page.locator('html').get_attribute('data-theme') != theme:
                    page.locator('#theme-toggle').click()
                page.evaluate('document.fonts.ready')

            def load(lang, theme):
                if in_memory:
                    page.set_content(document, wait_until='load')
                else:
                    page.goto(origin + '/index.html', wait_until='load')
                    page.evaluate('(key)=>localStorage.removeItem(key)', KEY)
                    page.reload()
                variant(lang, theme)

            def capture(name, full=False, **extra):
                filename = name + ('-full' if full else '') + '.png'
                page.screenshot(path=str(output / filename), full_page=full)
                report['captures'].append({'name': name, 'file': filename,
                                           'kind': 'document' if full else 'viewport',
                                           'viewport': page.viewport_size, **extra})

            def no_overflow():
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')

            def stored():
                return page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)||"null")', KEY)

            def settings():
                if page.locator('.fixture-controls details').get_attribute('open') is None:
                    page.locator('.fixture-controls summary').click()

            def fail_method(method):
                # Fault the actual boundary, retaining the native method for explicit recovery.
                page.evaluate('''({method,key})=>{
                  const storage=localStorage;
                  const target=typeof Storage!=='undefined'&&Object.getPrototypeOf(storage)===Storage.prototype?Storage.prototype:storage;
                  const descriptor=Object.getOwnPropertyDescriptor(target,method);
                  const original=storage[method];
                  Object.defineProperty(target,method,{configurable:true,value:function(k,...args){
                    if(k===key)throw new DOMException('Injected storage failure','SecurityError');
                    return original.call(this,k,...args);
                  }});
                  window.restoreStorageMethod=()=>Object.defineProperty(target,method,descriptor);
                }''', {'method': method, 'key': KEY})

            for lang in ('zh', 'en'):
                for theme in ('light', 'dark'):
                    for width, height in VIEWS:
                        page.set_viewport_size({'width': width, 'height': height})
                        load(lang, theme)
                        expect(page.locator('#main-title')).to_have_text(COPY[lang]['title'])
                        expect(page.get_by_role('button', name=COPY[lang]['save'], exact=True)).to_have_count(1)
                        expect(page.locator('#note-title')).to_have_accessible_name('笔记标题' if lang == 'zh' else 'Note title')
                        locale_label = page.locator('#locale-toggle').inner_text()
                        assert locale_label in page.locator('#locale-toggle').get_attribute('aria-label')
                        no_overflow()
                        expect(page.locator('#note-title')).to_have_attribute('aria-describedby', 'title-hint title-error')
                        expect(page.locator('#note-title')).to_have_attribute('aria-required', 'true')
                        ratios = {}
                        for selector in ('body', '.field-hint', '.storage-note', '.aside-footer', '#save'):
                            pair = page.locator(selector).first.evaluate('''e=>{
                              let parent=e,background='';
                              while(parent){background=getComputedStyle(parent).backgroundColor;
                                if(background!=='rgba(0, 0, 0, 0)'&&background!=='transparent')break;
                                parent=parent.parentElement;
                              }
                              return {text:getComputedStyle(e).color,background};
                            }''')
                            ratio = contrast(rgb(pair['text']), rgb(pair['background']))
                            assert ratio >= 4.5, (lang, theme, selector, ratio)
                            ratios[selector] = round(ratio, 2)
                        title = page.locator('#main-title').bounding_box()
                        assert title and title['width'] >= 180 and title['x'] >= 0
                        assert page.locator('#save').bounding_box()['width'] >= 100
                        capture(f'{lang}-{theme}-{width}', lang=lang, theme=theme, text_contrast=ratios)
                        if width in (390, 1280):
                            capture(f'{lang}-{theme}-{width}', full=True, lang=lang, theme=theme)
                        report['tests'].append(f'{lang}/{theme}/{width}: wording, accessible names, text contrast, geometry, overflow')

                    page.set_viewport_size({'width': 390, 'height': 844})
                    load(lang, theme)
                    page.locator('#save').click()
                    expect(page.locator('#note-title')).to_be_focused()
                    expect(page.locator('#title-error')).to_be_visible()
                    expect(page.locator('#note-title')).to_have_attribute('aria-invalid', 'true')
                    expect(page.locator('#title-error')).to_have_text(COPY[lang]['missing'])
                    capture(f'error-{lang}-{theme}', lang=lang, theme=theme)
                    other = 'en' if lang == 'zh' else 'zh'
                    page.locator('#locale-toggle').click()
                    expect(page.locator('#title-error')).to_have_text(COPY[other]['missing'])
                    variant(lang, theme)
                    title = '城市供热需要核查的需求变化' if lang == 'zh' else 'Demand changes to verify in district heating'
                    body = '来源仍需要核查' if lang == 'zh' else 'Sources still need checking'
                    page.locator('#note-title').fill(title)
                    page.locator('#note-body').fill(body)
                    page.locator('#save').click()
                    expect(page.locator('#state-message')).to_have_text(COPY[lang]['saved'])
                    expect(page.locator('#recent-title')).to_have_text(title)
                    assert stored() == {'title': title, 'body': body}
                    capture(f'saved-{lang}-{theme}', lang=lang, theme=theme)
                    if not in_memory:
                        page.reload()
                        expect(page.locator('#note-title')).to_have_value(title)
                        expect(page.locator('#note-body')).to_have_value(body)
                        report['storage_verified'] = True
                        # This fixture intentionally initializes to Chinese/light on navigation.
                        variant(lang, theme)
                    report['tests'].append(f'{lang}/{theme}: field error, localized error, actual write and reload')

                    draft = '等待保存的笔记' if lang == 'zh' else 'Note awaiting save'
                    page.locator('#note-title').fill(draft)
                    page.locator('#locale-toggle').click()
                    expect(page.locator('#note-title')).to_have_value(draft)
                    expect(page.locator('#note-body')).to_have_value(body)
                    variant(lang, theme)
                    settings()
                    page.locator('#simulate-failure').check()
                    page.locator('#save').click()
                    expect(page.locator('#state-message')).to_have_text(COPY[lang]['failed'])
                    expect(page.locator('#retry')).to_be_visible()
                    assert stored() == {'title': title, 'body': body}
                    expect(page.locator('#note-title')).to_have_value(draft)
                    capture(f'failed-{lang}-{theme}', lang=lang, theme=theme)
                    page.locator('#simulate-failure').uncheck()
                    page.locator('#retry').click()
                    expect(page.locator('#note-title')).to_be_focused()
                    expect(page.locator('#note-title')).to_be_in_viewport(ratio=1)
                    expect(page.locator('#state-message')).to_have_text(COPY[lang]['saved'])
                    expect(page.locator('#recent-title')).to_have_text(draft)
                    page.locator('#long-example').click()
                    long_title = page.locator('#note-title').input_value()
                    assert len(long_title) > (35 if lang == 'zh' else 70)
                    page.locator('#save').click()
                    expect(page.locator('#recent-title')).to_have_text(long_title)
                    no_overflow()
                    capture(f'long-{lang}-{theme}', full=True, lang=lang, theme=theme)
                    report['tests'].append(f'{lang}/{theme}: preserved draft, failed write, recovery focus, saved long-content reflow')

                    fail_method('removeItem')
                    page.locator('#reset').click()
                    expect(page.locator('#state-message')).to_have_text(COPY[lang]['clearFailed'])
                    assert stored()['title'] == long_title
                    expect(page.locator('#note-title')).to_have_value(long_title)
                    capture(f'clear-failed-{lang}-{theme}', lang=lang, theme=theme)
                    page.evaluate('window.restoreStorageMethod()')
                    page.locator('#retry').click()
                    expect(page.locator('#note-title')).to_be_focused()
                    expect(page.locator('#note-title')).to_be_in_viewport(ratio=1)
                    expect(page.locator('#state-message')).to_have_text(COPY[lang]['resetDone'])
                    assert stored() is None
                    page.locator('#locale-toggle').click()
                    expect(page.locator('#state-message')).to_have_text(COPY[other]['resetDone'])
                    report['tests'].append(f'{lang}/{theme}: native clear failure, retained data/draft, recovery and localized outcome')

            # Controlled time makes the edit-during-write race repeatable. It is not a speed benchmark.
            page.clock.install()
            for lang in ('zh', 'en'):
                for theme in ('light', 'dark'):
                    load(lang, theme)
                    settings()
                    page.locator('#simulate-slow').check()
                    page.clock.pause_at((page.evaluate('Date.now()') + 100) / 1000)
                    page.locator('#note-title').fill('Submitted revision')
                    page.locator('#note-body').fill('Original context')
                    page.locator('#save').click()
                    expect(page.locator('#state-message')).to_have_text(COPY[lang]['saving'])
                    expect(page.locator('#save')).to_be_disabled()
                    page.locator('#note-title').fill('New draft during the write')
                    page.locator('#note-body').fill('New context remains editable')
                    page.locator('#note-title').press('Enter')
                    other = 'en' if lang == 'zh' else 'zh'
                    page.locator('#locale-toggle').click()
                    page.locator('#theme-toggle').click()
                    expect(page.locator('#state-message')).to_have_text(COPY[other]['saving'])
                    page.clock.run_for(1001)
                    expect(page.locator('#state-message')).to_have_text(COPY[other]['savedEarlier'])
                    assert stored() == {'title': 'Submitted revision', 'body': 'Original context'}
                    expect(page.locator('#note-title')).to_have_value('New draft during the write')
                    expect(page.locator('#note-body')).to_have_value('New context remains editable')
                    page.clock.resume()
                    variant(lang, theme)
                    capture(f'edited-during-save-{lang}-{theme}', lang=lang, theme=theme)
                    page.clock.pause_at((page.evaluate('Date.now()') + 100) / 1000)
                    page.locator('#save').click()
                    page.locator('#reset').click()
                    page.clock.run_for(1001)
                    assert stored() is None
                    expect(page.locator('#note-title')).to_have_value('')
                    expect(page.locator('#state-message')).to_have_text(COPY[lang]['resetDone'])
                    page.clock.resume()
                    report['tests'].append(f'{lang}/{theme}: pending input, duplicate submit, locale/theme change, snapshot truth, reset cancellation (controlled clock)')

            context.close()
            context = browser.new_context(locale='zh-CN', device_scale_factor=1)
            page = context.new_page()
            observe(page)
            load('zh', 'light')
            page.keyboard.press('Tab')
            expect(page.locator('#skip')).to_be_focused()
            page.keyboard.press('Enter')
            expect(page.locator('#main')).to_be_focused()
            page.keyboard.press('Tab')
            expect(page.locator('#note-title')).to_be_focused()
            page.locator('#note-title').fill('Keyboard note')
            page.locator('#note-title').press('Enter')
            expect(page.locator('#state-message')).to_have_text(COPY['zh']['saved'])
            variant('en', 'light')
            page.emulate_media(reduced_motion='reduce')
            assert page.locator('#note-title').evaluate('e=>getComputedStyle(e).transitionDuration') == '0s'
            page.set_viewport_size({'width': 320, 'height': 800})
            page.add_style_tag(content='*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}')
            no_overflow()
            expect(page.locator('#save')).to_be_visible()
            capture('en-spacing-reflow-320', full=True, lang='en', theme='light')
            report['tests'].append('Keyboard skip/input/submit; reduced motion; 320px reflow with user text-spacing overrides')

            if in_memory:
                report['skipped'].append('Native startup read failures and malformed persisted records require local HTTP and real Storage')
            else:
                context.close()
                for lang in ('zh', 'en'):
                    for theme in ('light', 'dark'):
                        context = browser.new_context(locale='zh-CN', device_scale_factor=1)
                        context.add_init_script('''(()=>{
                          if(location.protocol!=='http:')return;
                          const key='ui-spec-content-note-v1';
                          localStorage.setItem(key,JSON.stringify({title:'Previously stored note',body:'Stored context'}));
                          const original=Storage.prototype.getItem;
                          window.failRead=true;
                          Storage.prototype.getItem=function(k){
                            if(k===key&&window.failRead)throw new DOMException('Injected read failure','SecurityError');
                            return original.call(this,k);
                          };
                        })();''')
                        page = context.new_page()
                        observe(page)
                        page.set_viewport_size({'width': 390, 'height': 844})
                        page.goto(origin + '/index.html', wait_until='load')
                        variant(lang, theme)
                        expect(page.locator('#state-message')).to_have_text(COPY[lang]['readFailed'])
                        expect(page.locator('#recent-title')).to_have_text(COPY[lang]['recentUnreadable'])
                        expect(page.locator('#save')).to_be_disabled()
                        page.locator('#note-title').fill('Draft written during a read failure')
                        capture(f'read-failed-{lang}-{theme}', lang=lang, theme=theme)
                        page.evaluate('window.failRead=false')
                        page.locator('#retry').click()
                        expect(page.locator('#state-message')).to_have_text(COPY[lang]['readRecoveredDraft'])
                        expect(page.locator('#note-title')).to_have_value('Draft written during a read failure')
                        expect(page.locator('#recent-title')).to_have_text('Previously stored note')
                        expect(page.locator('#save')).to_be_enabled()
                        assert stored()['title'] == 'Previously stored note'
                        report['tests'].append(f'{lang}/{theme}: native read failure, protected stored data, recovery without replacing draft')
                        context.close()

                context = browser.new_context(locale='zh-CN', device_scale_factor=1)
                context.add_init_script("if(location.protocol==='http:')localStorage.setItem('ui-spec-content-note-v1','{malformed')")
                page = context.new_page()
                observe(page)
                page.goto(origin + '/index.html', wait_until='load')
                variant('en', 'light')
                expect(page.locator('#state-message')).to_have_text(COPY['en']['invalidStored'])
                expect(page.locator('#save')).to_be_disabled()
                assert page.evaluate('(key)=>localStorage.getItem(key)', KEY) == '{malformed'
                settings()
                page.locator('#reset').click()
                expect(page.locator('#state-message')).to_have_text(COPY['en']['resetDone'])
                expect(page.locator('#save')).to_be_enabled()
                assert stored() is None
                report['tests'].append('Malformed stored record remains identifiable and is cleared only through the explicit control')
                page.locator('#note-title').fill('Previously written')
                page.locator('#save').click()
                expect(page.locator('#state-message')).to_have_text(COPY['en']['saved'])
                fail_method('setItem')
                page.locator('#note-title').fill('Write retry draft')
                page.locator('#save').click()
                expect(page.locator('#state-message')).to_have_text(COPY['en']['failed'])
                assert stored()['title'] == 'Previously written'
                expect(page.locator('#note-title')).to_have_value('Write retry draft')
                page.evaluate('window.restoreStorageMethod()')
                page.locator('#retry').click()
                expect(page.locator('#state-message')).to_have_text(COPY['en']['saved'])
                assert stored()['title'] == 'Write retry draft'
                report['tests'].append('Native setItem exception preserves the previous stored result and permits an explicit successful retry')

            assert not report['page_errors'], report['page_errors']
            assert not report['external_requests'], report['external_requests']
            report['result'] = 'preview_pass_storage_pending' if in_memory else 'pass'
            report['browser_version'] = browser.version
            context.close()
            browser.close()
    except Exception as error:
        report['result'] = 'fail'
        report['detail'] = str(error)
        raise
    finally:
        server.shutdown()
        server.server_close()
        (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--browser-path')
    parser.add_argument('--in-memory', action='store_true', help='Inline assets and simulated storage; persistence remains unverified')
    args = parser.parse_args()
    result = validate(args.output_dir, args.browser_path, args.in_memory)
    print(json.dumps({name: len(result[name]) if name in ('captures', 'tests') else result[name]
                      for name in ('result', 'captures', 'tests', 'storage_verified', 'scope')}, ensure_ascii=False, indent=2))
