#!/usr/bin/env python3
"""Render real README content locally; optionally inspect its actual GitHub host."""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
VIEWS = ((390,844),(768,1024),(1440,1000))
STYLE = '''
:root{color-scheme:light dark;--bg:#fff;--fg:#1f2328;--muted:#59636e;--line:#d1d9e0;--soft:#f6f8fa;--link:#0969da}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#f0f6fc;--muted:#9198a1;--line:#3d444d;--soft:#151b23;--link:#4493f8}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Arial,"Noto Sans CJK SC",sans-serif}
.preview-label{font-size:12px;color:var(--muted);padding:10px 24px;border-bottom:1px solid var(--line)}
article{max-width:980px;margin:28px auto;padding:32px;border:1px solid var(--line);border-radius:6px;overflow-wrap:break-word}
h1,h2,h3{line-height:1.25;margin:24px 0 16px;font-weight:600}h1{font-size:2em;padding-bottom:.3em;border-bottom:1px solid var(--line);margin-top:0}h2{font-size:1.5em;padding-bottom:.3em;border-bottom:1px solid var(--line);margin-top:32px}h3{font-size:1.25em}
p{margin:0 0 16px}a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}a:focus-visible,summary:focus-visible{outline:2px solid var(--link);outline-offset:4px}
img{max-width:100%;height:auto;vertical-align:middle}picture{display:block;margin:20px 0}pre{padding:16px;overflow:auto;background:var(--soft);border-radius:6px;font:13px/1.55 ui-monospace,SFMono-Regular,Consolas,monospace;max-width:100%}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:85%;background:var(--soft);border-radius:4px;padding:.15em .3em}pre code{font-size:100%;padding:0;background:transparent}
table{border-spacing:0;border-collapse:collapse;display:block;max-width:100%;overflow:auto;margin-bottom:16px}td,th{border:1px solid var(--line);padding:8px 12px;text-align:left}tr:nth-child(2n){background:var(--soft)}summary{cursor:pointer}details{margin:24px 0}details[open]>summary{margin-bottom:16px}ul,ol{padding-left:2em}blockquote{padding:0 1em;color:var(--muted);border-left:.25em solid var(--line);margin-left:0}
@media(max-width:767px){article{margin:0;padding:20px 16px;border:0;border-radius:0}.preview-label{padding:8px 16px}h1{font-size:1.75em}h2{font-size:1.35em}}
'''


def render_document(markdown: str, language: str) -> str:
    from markdown_it import MarkdownIt
    md=MarkdownIt('commonmark',{'html':True}).enable('table').enable('strikethrough')
    body=md.render(markdown)
    return f'<!doctype html><html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>UI Spec Studio — README preview</title><style>{STYLE}</style></head><body><div class="preview-label">Local Markdown preview · GitHub-like stylesheet · not a GitHub screenshot</div><article class="markdown-body">{body}</article></body></html>'


def _inspect(page, article, path: Path) -> dict:
    page.evaluate('document.fonts.ready')
    page.wait_for_function('''() => [...document.querySelectorAll('article img')].every(i=>i.complete&&i.naturalWidth>0)''',timeout=30000)
    box=article.bounding_box()
    image=article.locator('picture img').first
    img=image.evaluate('(i)=>({currentSrc:i.currentSrc,width:i.clientWidth,height:i.clientHeight,naturalWidth:i.naturalWidth})')
    overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
    if overflow: raise ValueError('Document overflows the actual viewport')
    # Preserve the original viewport for both visible and document-length captures.
    page.screenshot(path=str(path.with_suffix('.png')),full_page=False)
    page.screenshot(path=str(path.with_name(path.name+'-full.png')),full_page=True)
    details=article.locator('details').first
    if details.count():
        details.locator('summary').click()
        if details.get_attribute('open') is None: raise ValueError('Disclosure did not open')
        details.locator('summary').click()
        page.evaluate('scrollTo(0,0)')
    install=article.locator('pre').first.inner_text()
    if 'npx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec' not in install:
        raise ValueError('Primary installation command is not selectable native text')
    if not image.get_attribute('alt'): raise ValueError('Artwork needs alternative text')
    return {'viewport':page.viewport_size,'article':box,'artwork':img,'document_overflow':overflow,
            'native_install_command':True,'disclosure':'exercised','image_alt':True,
            'screenshot':path.name+'.png','full_screenshot':path.name+'-full.png'}


def preview(output: Path, browser_path: str | None = None, live_commit: str | None = None) -> dict:
    from playwright.sync_api import sync_playwright
    if live_commit and not re.fullmatch('[0-9a-f]{40}',live_commit):
        raise ValueError('Use an exact 40-character source commit for live readback')
    output=output.resolve();output.mkdir(parents=True,exist_ok=True)
    results=[]
    asset_urls = {path.name: ('data:image/svg+xml;base64,' if path.suffix == '.svg' else 'data:image/png;base64,') + base64.b64encode(path.read_bytes()).decode('ascii')
                  for path in (ROOT / 'docs/assets').iterdir() if path.suffix in {'.svg', '.png'}}
    with sync_playwright() as pw:
        options={'headless':True}
        if browser_path: options['executable_path']=browser_path
        browser=pw.chromium.launch(**options)
        try:
            for filename,lang in [('README.md','en'),('README.zh-CN.md','zh')]:
                text=(ROOT/filename).read_text(encoding='utf-8')
                document=render_document(text,'zh-CN' if lang=='zh' else 'en')
                # Embed the exact local asset bytes for an entirely offline preview.
                for name, data_url in asset_urls.items():
                    document=document.replace('docs/assets/'+name,data_url)
                for theme in ['light','dark']:
                    context=browser.new_context(color_scheme=theme,device_scale_factor=1,locale='en-US')
                    page=context.new_page()
                    for width,height in VIEWS:
                        page.set_viewport_size({'width':width,'height':height})
                        page.set_content(document,wait_until='load')
                        name=f'local-{lang}-{theme}-{width}'
                        result=_inspect(page,page.locator('article'),output/name)
                        expected=f'studio-{"compact-" if width<=600 else ""}{theme}.svg'
                        if result['artwork']['currentSrc'] != asset_urls[expected]:
                            raise ValueError('Theme/narrow artwork selection differs')
                        result['artwork']['currentSrc']=expected
                        results.append({'renderer':'local-markdown-approximation','language':lang,'theme':theme,**result})
                    if live_commit:
                        page.set_viewport_size({'width':1440,'height':1000})
                        url=f'https://github.com/D1ChangGeng/UI-Spec-Studio/blob/{live_commit}/{filename}'
                        page.goto(url,wait_until='domcontentloaded',timeout=60000)
                        article=page.locator('article.markdown-body').first;article.wait_for(timeout=45000)
                        for width,height in VIEWS:
                            page.set_viewport_size({'width':width,'height':height});page.evaluate('scrollTo(0,0)')
                            result=_inspect(page,article,output/f'github-{lang}-{theme}-{width}')
                            results.append({'renderer':'github','url':url,'language':lang,'requested_color_scheme':theme,
                                            'host_color_mode':page.locator('html').get_attribute('data-color-mode'),**result})
                    context.close()
        finally:browser.close()
    report={'source_files':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['README.md','README.zh-CN.md']},
            'captures':results,'scope':'DOM, asset selection, native copy, disclosure and overflow checks; inspect screenshots separately for visual judgment',
            'local_renderer':'Markdown-It with a GitHub-like stylesheet; not pixel-identical to GitHub',
            'live_commit':live_commit}
    (output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--browser-path');p.add_argument('--live-commit');args=p.parse_args()
    try:
        report=preview(args.output_dir,args.browser_path,args.live_commit)
        print(json.dumps({'captures':len(report['captures']),'report':str(args.output_dir/'report.json'),
                          'live_commit':report['live_commit'],'scope':report['scope']},indent=2))
    except Exception as exc:
        print(f'preview_readme: {exc}',file=sys.stderr);raise SystemExit(1)
