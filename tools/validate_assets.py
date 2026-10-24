#!/usr/bin/env python3
"""Exercise asset delivery in a scoped browser fixture; inspect captures separately."""
from __future__ import annotations
import argparse
import base64
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading

ROOT = Path(__file__).resolve().parents[1]
VIEWS = ((390, 844), (1440, 1000))
SVG_NAMES = tuple(f'studio-{prefix}{theme}.svg' for prefix in ('', 'compact-') for theme in ('light', 'dark'))


def source_inventory(root: Path = ROOT) -> list[dict]:
    names = ['tools/readme_art.py', 'examples/asset-review/search.svg',
             'examples/asset-review/THIRD-PARTY.md',
             *['docs/assets/' + name for name in SVG_NAMES]]
    result = []
    for name in names:
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'Expected a regular source file: {name}')
        data = path.read_bytes()
        if not data:
            raise ValueError(f'Empty source file: {name}')
        result.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    return result


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def validate(output: Path, browser_path: str | None = None, in_memory: bool = False) -> dict:
    from playwright.sync_api import sync_playwright, expect
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = {'scope': 'Actual files and browser states in the asset-review fixture; visual approval and specialist production remain separate',
              'renderer': 'in-memory' if in_memory else 'local-http', 'sources': source_inventory(), 'views': [], 'checks': [], 'errors': []}
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f'http://127.0.0.1:{server.server_port}'
    url = origin + '/examples/asset-review/index.html'
    document = (ROOT / 'examples/asset-review/index.html').read_text(encoding='utf-8')
    style = (ROOT / 'examples/asset-review/styles.css').read_text(encoding='utf-8')
    script = (ROOT / 'examples/asset-review/app.js').read_text(encoding='utf-8')
    icon = (ROOT / 'examples/asset-review/search.svg').read_text(encoding='utf-8')
    urls = {name: 'data:image/svg+xml;base64,' + base64.b64encode((ROOT / 'docs/assets' / name).read_bytes()).decode() for name in SVG_NAMES}
    document = document.replace('<link rel="stylesheet" href="styles.css">', '<style>' + style + '</style>')
    script = script.replace("fetch('search.svg')", 'Promise.resolve({ok:true,text:()=>Promise.resolve(' + json.dumps(icon) + ')})')
    document = document.replace('<script src="app.js"></script>', '<script>' + script + '</script>')
    for name, value in urls.items():
        document = document.replace('../../docs/assets/' + name, value)
    try:
        with sync_playwright() as pw:
            options = {'headless': True}
            if browser_path:
                options['executable_path'] = browser_path
            browser = pw.chromium.launch(**options)
            report['browser'] = browser.version
            try:
                for theme in ('light', 'dark'):
                    for density in (1, 2):
                        context = browser.new_context(color_scheme=theme, device_scale_factor=density)
                        page = context.new_page()
                        page.on('pageerror', lambda error: report['errors'].append(str(error)))
                        def load():
                            if in_memory:
                                page.set_content(document, wait_until='load')
                            else:
                                page.goto(url, wait_until='networkidle')
                        for width, height in VIEWS:
                            page.set_viewport_size({'width': width, 'height': height})
                            load()
                            page.wait_for_function("document.documentElement.dataset.iconsReady === 'true'")
                            page.evaluate('document.fonts.ready')
                            image = page.locator('#hero')
                            facts = image.evaluate('(i)=>({src:i.currentSrc,naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight,width:i.clientWidth,height:i.clientHeight})')
                            expected = f'studio-{"compact-" if width <= 600 else ""}{theme}.svg'
                            assert facts['src'] == urls[expected] if in_memory else facts['src'].endswith('/' + expected), 'Unexpected asset variant'
                            assert facts['naturalWidth'] > 0 and facts['naturalHeight'] > 0
                            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                            icons = page.locator('.icon-specimen svg')
                            assert icons.count() == 4
                            for i, size in enumerate((16, 24, 32, 48)):
                                box = icons.nth(i).bounding_box()
                                assert abs(box['width'] - size) < .1 and abs(box['height'] - size) < .1
                                assert icons.nth(i).get_attribute('aria-hidden') == 'true'
                            button = page.get_by_role('button', name='Search the sample', exact=True)
                            box = button.bounding_box()
                            assert box['width'] >= 44 and box['height'] >= 44
                            button.focus()
                            page.keyboard.press('Enter')
                            expect(page.locator('#search-result')).to_contain_text('Search action reached')
                            assert image.get_attribute('alt')
                            assert page.locator('#motion-stage').get_attribute('aria-hidden') == 'true'
                            expect(page.locator('#type-specimen')).to_contain_text('让研究，抵达判断。')
                            stem = f'assets-{theme}-{width}-dpr{density}'
                            page.evaluate('scrollTo(0,0)')
                            frame = page.locator('.art-frame').bounding_box()
                            page.screenshot(path=str(output / (stem + '.png')))
                            page.screenshot(path=str(output / (stem + '-full.png')), full_page=True)
                            page.locator('#icon-sizes').screenshot(path=str(output / (stem + '-icons.png')))
                            facts['src'] = expected
                            report['views'].append({'theme': theme, 'viewport': {'width': width, 'height': height},
                                                    'device_scale_factor': density, 'image': facts,
                                                    'frame': frame,
                                                    'icon_css_sizes': [16, 24, 32, 48], 'named_control': True,
                                                    'captures': [stem + '.png', stem + '-full.png', stem + '-icons.png']})
                        # Real preference and pause state, with the element inside the viewport.
                        page.locator('#motion-toggle').scroll_into_view_if_needed()
                        expect(page.locator('#motion-stage')).to_have_attribute('data-running', 'true')
                        page.locator('#motion-toggle').click()
                        expect(page.locator('#motion-stage')).to_have_attribute('data-running', 'false')
                        assert page.locator('.orbit').evaluate('(e)=>getComputedStyle(e).animationPlayState') == 'paused'
                        page.locator('#motion-toggle').click()
                        expect(page.locator('#motion-stage')).to_have_attribute('data-running', 'true')
                        page.emulate_media(reduced_motion='reduce')
                        expect(page.locator('#motion-toggle')).to_be_disabled()
                        expect(page.locator('#motion-stage')).to_have_attribute('data-running', 'false')
                        assert page.locator('.orbit').evaluate('(e)=>getComputedStyle(e).animationName') == 'none'
                        page.screenshot(path=str(output / f'reduced-{theme}-dpr{density}.png'))
                        page.emulate_media(reduced_motion='no-preference')
                        expect(page.locator('#motion-toggle')).to_be_enabled()
                        page.set_viewport_size({'width': 390, 'height': 844})
                        page.evaluate('scrollTo(0,0)')
                        expect(page.locator('#motion-stage')).to_have_attribute('data-running', 'false')
                        report['checks'].append(f'{theme}/dpr{density}: user pause, reduced motion, offscreen suspension')
                        # Same dimensions, actual request failure, stable reserved frame.
                        load()
                        before = page.locator('.art-frame').bounding_box()
                        if in_memory:
                            page.evaluate('''() => { for (const s of document.querySelectorAll('#artwork source')) s.srcset='data:image/svg+xml;base64,AA==';document.querySelector('#hero').src='data:image/svg+xml;base64,AA=='; }''')
                        else:
                            page.route('**/docs/assets/studio-*.svg', lambda route: route.abort())
                            page.reload(wait_until='networkidle')
                        expect(page.locator('#fallback')).to_be_visible()
                        expect(page.locator('#artwork')).to_be_hidden()
                        after = page.locator('.art-frame').bounding_box()
                        assert abs(before['height'] - after['height']) < .1 and abs(before['width'] - after['width']) < .1
                        page.screenshot(path=str(output / f'unavailable-{theme}-dpr{density}.png'))
                        report['checks'].append(f'{theme}/dpr{density}: {"invalid data image" if in_memory else "blocked HTTP illustration"}, meaningful fallback, reserved geometry')
                        context.close()
                assert not report['errors'], report['errors']
                report['result'] = 'offline_render_pass_http_pending' if in_memory else 'pass'
            finally:
                browser.close()
    except Exception as exc:
        report['result'] = 'fail'
        report['errors'].append(str(exc))
        raise
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        (output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--browser-path')
    parser.add_argument('--in-memory', action='store_true', help='Offline render; HTTP delivery remains unverified')
    args = parser.parse_args()
    result = validate(args.output_dir, args.browser_path, args.in_memory)
    print(json.dumps({'result': result['result'], 'views': len(result['views']),
                      'state_checks': len(result['checks']), 'scope': result['scope']}, indent=2))
