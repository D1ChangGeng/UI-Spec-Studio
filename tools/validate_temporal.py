#!/usr/bin/env python3
"""Capture chronological browser episodes; inspect the resulting pixels separately."""
from __future__ import annotations

import argparse
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import subprocess
import threading

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/temporal-review'
KEY = 'ui-spec-temporal-note-v1'

# Instrumentation belongs to the test, and does not draw over the product.
# The normal path still calls native Storage. Failure injection is explicitly scoped.
RECORDER = r"""(() => {
  window.__temporal = {events: [], writes: [], removals: [], failWrite: false, failClear: false};
  const record = (type, target, detail) => window.__temporal.events.push({
    at_ms: performance.now(), type, target, detail
  });
  for (const type of ['click','input','keydown','transitionrun','transitionend',
                       'transitioncancel','animationiteration']) {
    document.addEventListener(type, e => record(type, e.target.id || e.target.className,
      e.propertyName || e.animationName || e.key || ''), true);
  }
  const write = Storage.prototype.setItem;
  Storage.prototype.setItem = function(key, value) {
    if (key !== 'ui-spec-temporal-note-v1') return write.call(this, key, value);
    const entry = {at_ms: performance.now(), succeeded: false};
    window.__temporal.writes.push(entry);
    if (window.__temporal.failWrite) throw new DOMException('Test write failure', 'QuotaExceededError');
    const result = write.call(this, key, value);
    entry.succeeded = true;
    return result;
  };
  const remove = Storage.prototype.removeItem;
  Storage.prototype.removeItem = function(key) {
    if (key !== 'ui-spec-temporal-note-v1') return remove.call(this, key);
    const entry = {at_ms: performance.now(), succeeded: false};
    window.__temporal.removals.push(entry);
    if (window.__temporal.failClear) throw new DOMException('Test removal failure', 'SecurityError');
    const result = remove.call(this, key);
    entry.succeeded = true;
    return result;
  };
})();"""

SNAPSHOT = r"""() => {
  const byId = id => document.getElementById(id);
  const box = e => {const r=e.getBoundingClientRect(); return {x:r.x,y:r.y,width:r.width,height:r.height};};
  const card = byId('note-card');
  let storage;
  try {
    const raw = localStorage.getItem('ui-spec-temporal-note-v1');
    storage = raw === null ? {state:'empty'} : {state:'readable',text:JSON.parse(raw).text};
  } catch (_) { storage = {state:'unreadable'}; }
  return {
    at_ms: performance.now(), time_origin_ms: performance.timeOrigin,
    face: card.dataset.face, transform: getComputedStyle(card).transform,
    object_preserved: card === window.__temporal.object,
    record_id: card.dataset.recordId, card_space: box(byId('card-space')),
    header: box(document.querySelector('.site-header')),
    orbit_transform: getComputedStyle(document.querySelector('.orbit-arm')).transform,
    status: byId('status-area').dataset.status || '',
    feedback: byId('status').textContent,
    saved_title: byId('saved-title').textContent, saved_text: byId('saved-text').textContent,
    saved_kicker: byId('saved-kicker').textContent, collection_status: byId('collection-status').textContent,
    storage, draft_length: byId('note-text').value.length,
    limit_text: byId('note-limit').textContent, input_invalid: byId('note-text').getAttribute('aria-invalid'),
    view: byId('collection').hidden ? 'editor' : 'collection',
    focus: document.activeElement.id, scroll: {x:scrollX,y:scrollY},
    retry_visible: byId('retry').getClientRects().length > 0,
    status_visible: byId('status').getClientRects().length > 0,
    save_disabled: byId('save').disabled,
    front_inert: byId('card-front').inert, back_inert: byId('card-back').inert
  };
}"""


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def capture_summary(frames: list[dict]) -> dict:
    """Describe capture intervals, without converting sampling into a frame rate claim."""
    if len(frames) < 2:
        raise ValueError('An episode requires at least two ordered captures')
    previous_end = None
    gaps, starts = [], []
    for frame in frames:
        start, end = frame['capture_start_ms'], frame['capture_end_ms']
        if start > end or (previous_end is not None and start < previous_end):
            raise ValueError('Capture intervals must be ordered and non-overlapping')
        if previous_end is not None:
            gaps.append(start - previous_end)
        previous_end = end
        starts.append(start)
    return {
        'frame_count': len(frames),
        'capture_span_ms': frames[-1]['capture_end_ms'] - frames[0]['capture_start_ms'],
        'maximum_gap_between_capture_brackets_ms': max(gaps),
        'start_to_start_intervals_ms': [b - a for a, b in zip(starts, starts[1:])],
        'interpretation': 'Gaps are between capture brackets; the actual image instants lie within those brackets. This is not the maximum inter-image sampling gap, presented-frame timing or a smoothness score.',
    }


def source_identity() -> dict:
    sources = {}
    for path in sorted(EXAMPLE.glob('*')):
        if path.is_file():
            sources[path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    sources['tools/validate_temporal.py'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    try:
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        dirty = bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True))
    except (OSError, subprocess.CalledProcessError):
        revision, dirty = None, None
    return {'git_revision': revision, 'worktree_dirty': dirty, 'sha256': sources}


def validate(output: Path, browser_path: str | None = None, video: bool = True) -> dict:
    from playwright.sync_api import sync_playwright, expect

    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = {
        'scope': 'Authored local browser fixture with real Storage, normal-time interactions and scoped fault injection.',
        'source': source_identity(), 'renderer': 'local-http', 'time_control': 'none',
        'screenshot_animations': 'allow', 'device_scale_factor': 1,
        'visual_review': 'pending: captured media requires actual viewing',
        'performance_scope': 'No frame-delivery trace, field responsiveness or target-device smoothness claim.',
        'episodes': [], 'checks': [], 'videos': [], 'page_errors': [], 'external_requests': [],
        'storage_verified': False, 'result': 'pending',
    }
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(EXAMPLE)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            launch = {'headless': True}
            if browser_path:
                launch['executable_path'] = browser_path
            browser = pw.chromium.launch(**launch)
            report['browser'] = browser.version
            try:
                for variant in ('desktop', 'narrow'):
                    viewport = {'width': 1280, 'height': 900} if variant == 'desktop' else {'width': 390, 'height': 844}
                    options = {'viewport': viewport, 'device_scale_factor': 1, 'locale': 'en-US', 'reduced_motion': 'no-preference'}
                    if video:
                        options.update(record_video_dir=str(output / 'videos'), record_video_size=viewport)
                    context = browser.new_context(**options)
                    context.add_init_script(RECORDER)
                    page = context.new_page()
                    page.set_default_timeout(10000)
                    page.on('pageerror', lambda error: report['page_errors'].append(str(error)))
                    page.on('request', lambda req: report['external_requests'].append(req.url)
                            if not req.url.startswith(origin + '/') else None)
                    media = page.video
                    try:
                        page.goto(origin + '/index.html', wait_until='load')
                        page.evaluate('document.fonts.ready')
                        page.evaluate('window.__temporal.object = document.getElementById("note-card")')
                        if variant == 'narrow':
                            page.locator('#locale-toggle').click()
                            page.locator('#theme-toggle').click()
                        cdp = context.new_cdp_session(page)
                        cdp.send('DOM.enable')
                        cdp.send('CSS.enable')
                        document_node = cdp.send('DOM.getDocument')['root']['nodeId']
                        fonts = {}
                        for selector in ('#page-title', '#note-hint'):
                            node = cdp.send('DOM.querySelector', {'nodeId': document_node, 'selector': selector})['nodeId']
                            fonts[selector] = cdp.send('CSS.getPlatformFontsForNode', {'nodeId': node})['fonts']
                        cdp.detach()
                        report.setdefault('conditions', []).append({
                            'variant': variant, 'viewport': viewport,
                            'locale': page.locator('html').get_attribute('lang'),
                            'theme': page.locator('html').get_attribute('data-theme'),
                            'zoom': 1, 'video_size': viewport if video else None, 'resolved_fonts': fonts,
                        })

                        def stored():
                            return page.evaluate('(key) => JSON.parse(localStorage.getItem(key) || "null")', KEY)

                        def episode(name, duration_ms, actions=(), *, interval_ms=90, note=''):
                            item = {'name': variant + '-' + name, 'variant': variant, 'note': note,
                                    'requested_gap_ms': interval_ms, 'actions': [], 'frames': []}
                            report['episodes'].append(item)
                            directory = output / item['name']
                            directory.mkdir(exist_ok=True)
                            start_events = page.evaluate('window.__temporal.events.length')
                            def frame():
                                before = page.evaluate(SNAPSHOT)
                                relative = f"{item['name']}/{len(item['frames']):03d}.png"
                                page.screenshot(path=str(output / relative), animations='allow')
                                after = page.evaluate(SNAPSHOT)
                                item['frames'].append({'file': relative,
                                    'capture_start_ms': before['at_ms'], 'capture_end_ms': after['at_ms'],
                                    'before': before, 'after': after})
                            frame()  # Starting context precedes every scheduled action.
                            start = page.evaluate('performance.now()')
                            item['schedule_origin_ms'] = start
                            remaining = list(actions)
                            while True:
                                elapsed = page.evaluate('performance.now()') - start
                                while remaining and elapsed >= remaining[0][0]:
                                    due, kind, target, value = remaining.pop(0)
                                    begin = page.evaluate('performance.now()')
                                    if kind == 'click':
                                        page.locator(target).click()
                                    elif kind == 'fill':
                                        page.locator(target).fill(value)
                                    elif kind == 'key':
                                        page.keyboard.press(value)
                                    elif kind == 'restore-write':
                                        page.evaluate('window.__temporal.failWrite = false')
                                    elif kind == 'restore-clear':
                                        assert stored()['text'] == value, 'Failed clear must preserve the actual stored value'
                                        expect(page.locator('#retry')).to_be_focused()
                                        expect(page.locator('#retry')).to_be_in_viewport()
                                        page.evaluate('window.__temporal.failClear = false')
                                    elif kind == 'reduce-motion':
                                        page.emulate_media(reduced_motion='reduce')
                                    else:
                                        raise ValueError('Unknown episode action: ' + kind)
                                    end = page.evaluate('performance.now()')
                                    item['actions'].append({'requested_offset_ms': due, 'kind': kind,
                                                           'target': target, 'start_ms': begin, 'end_ms': end})
                                    elapsed = end - start
                                frame()
                                if elapsed >= duration_ms and not remaining:
                                    break
                                page.wait_for_timeout(interval_ms)
                            item['events'] = page.evaluate('(n) => window.__temporal.events.slice(n)', start_events)
                            item['capture_summary'] = capture_summary(item['frames'])
                            assert all(f['before']['object_preserved'] and f['after']['object_preserved'] for f in item['frames'])
                            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
                            return item

                        # Keep decoration quiet during object-motion comparisons.
                        page.locator('#motion-toggle').click()
                        forward = episode('flip-return', 1650,
                            [(0,'click','#flip',None),(850,'click','#flip',None)],
                            note='One CSS card object, forward motion, readable back and reverse motion.')
                        expect(page.locator('#note-card')).to_have_attribute('data-face', 'front')
                        ends = [e for e in forward['events'] if e['type'] == 'transitionend']
                        assert len(ends) >= 2, 'Both flip directions must finish during the observed episode'
                        anchors = [f['before']['card_space'] for f in forward['frames']]
                        assert all(all(abs(box[k] - anchors[0][k]) < .5 for k in box) for box in anchors)
                        report['checks'].append(variant + ': forward/reverse completion, retained DOM identity and stationary card container')

                        interrupted = episode('interrupted-flip', 1050,
                            [(0,'click','#flip',None),(180,'click','#flip',None)], interval_ms=55,
                            note='A second visible-control input reverses the transition while it is active.')
                        assert any(e['type'] == 'transitioncancel' for e in interrupted['events'])
                        expect(page.locator('#note-card')).to_have_attribute('data-face', 'front')
                        assert page.locator('#card-back').evaluate('(e)=>e.inert')
                        report['checks'].append(variant + ': mid-motion reversal settles with the inactive face inert')

                        if variant == 'desktop':
                            loop = episode('decoration-cycle', 2150,
                                [(0,'click','#motion-toggle',None)], interval_ms=150,
                                note='Natural-time orbit includes an animationiteration boundary and remains in its reserved art area.')
                            assert any(e['type'] == 'animationiteration' for e in loop['events'])
                            assert len({f['before']['orbit_transform'] for f in loop['frames']}) > 4
                            page.locator('#motion-toggle').click()
                            report['checks'].append('desktop: complete decorative cycle including its browser iteration event')

                        draft = 'Compare the evidence before deciding.' if variant == 'desktop' else '核查证据后再形成判断。'
                        edit = draft + (' Keep the new question.' if variant == 'desktop' else '保留刚补充的问题。')
                        expect(page.locator('#note-limit')).to_contain_text('600')
                        page.locator('#note-text').fill('')
                        page.keyboard.insert_text('x' * 620)
                        assert len(page.locator('#note-text').input_value()) == 620
                        expect(page.locator('#note-text')).to_have_attribute('aria-invalid', 'true')
                        expect(page.locator('#note-limit')).to_contain_text('620')
                        expect(page.locator('#save')).to_be_disabled()
                        assert stored() is None
                        episode('over-limit-draft', 220,
                            note='An actual 620-character insertion stays intact; associated count/error explains the 600-character save bound.')
                        report['checks'].append(variant + ': over-limit insertion retained, visible count/error, disabled save and unchanged Storage')
                        initial = 'A previously saved observation.' if variant == 'desktop' else '之前保存的一条观察。'
                        page.locator('#note-text').fill(initial)
                        first_save = episode('first-save-view', 1350,
                            [(0,'click','#save',None),(80,'click','#saved-link',None)],
                            note='The first save remains pending after navigation: its provisional snapshot is labelled and actual Storage stays empty until completion.')
                        first_pending = [f['after'] for f in first_save['frames'] if f['after']['view'] == 'collection' and f['after']['status'] == 'saving']
                        assert first_pending
                        assert all(s['storage']['state'] == 'empty' and s['collection_status'] and s['saved_text'] == initial for s in first_pending)
                        assert all(s['saved_kicker'] == ('Save in progress' if variant == 'desktop' else '正在保存') for s in first_pending)
                        assert stored()['text'] == initial
                        expect(page.locator('#collection-status')).to_have_text('Note saved in this browser.' if variant == 'desktop' else '笔记已保存在此浏览器。')
                        page.locator('#return').click()
                        report['checks'].append(variant + ': first-save pending and confirmed outcome remain visible across navigation')
                        page.locator('#note-text').fill(draft)
                        page.locator('#save').scroll_into_view_if_needed()
                        writes_before = len(page.evaluate('window.__temporal.writes'))
                        wait = episode('save-while-editing', 1350,
                            [(0,'click','#save',None),(80,'key',None,'Enter'),(280,'fill','#note-text',edit),(430,'click','#saved-link',None)],
                            note='Existing saved snapshot stays visible during a newer save; continued editing retains another draft and the final message identifies the submitted version.')
                        states = {f['after']['status'] for f in wait['frames']}
                        assert {'saving','earlier'} <= states
                        existing_pending = [f['after'] for f in wait['frames'] if f['after']['view'] == 'collection' and f['after']['status'] == 'saving']
                        assert existing_pending
                        assert all(s['storage']['text'] == initial and s['saved_text'] == initial and s['collection_status'] for s in existing_pending)
                        assert stored()['text'] == draft
                        expect(page.locator('#note-text')).to_have_value(edit)
                        assert len(page.evaluate('window.__temporal.writes')) - writes_before == 1
                        expect(page.locator('#collection-status')).to_contain_text('submitted version' if variant == 'desktop' else '提交的版本')
                        page.locator('#return').click()
                        report['checks'].append(variant + ': visible pending old snapshot, one write after repeated Enter, submitted version and newer draft distinguished')

                        page.evaluate('window.__temporal.failWrite = true')
                        failed = episode('failed-save', 1250, [(0,'click','#save',None)],
                            note='Harness injects a named Storage write failure; the prior persisted value remains.')
                        assert failed['frames'][-1]['after']['status'] == 'failed'
                        assert stored()['text'] == draft
                        expect(page.locator('#note-text')).to_have_value(edit)
                        recovered = episode('retry-save', 1250,
                            [(0,'restore-write',None,None),(0,'click','#retry',None)],
                            note='The visible retry returns to native Storage; disappearing retry restores visible editor focus.')
                        assert recovered['frames'][-1]['after']['status'] == 'saved'
                        assert stored()['text'] == edit
                        expect(page.locator('#note-text')).to_be_focused()
                        focus_box = page.locator('#note-text').bounding_box()
                        assert focus_box['y'] >= 0 and focus_box['y'] + focus_box['height'] <= viewport['height'] + 1
                        report['checks'].append(variant + ': real boundary failure, retained draft, native retry, truthful success and visible focus')

                        page.evaluate('scrollTo(0,0)')
                        journey = episode('saved-view-return', 1000,
                            [(0,'click','#saved-link',None),(500,'click','#return',None)], interval_ms=120,
                            note='The saved record is shown, then editing resumes with its draft and shared header.')
                        assert {'editor','collection'} <= {f['after']['view'] for f in journey['frames']}
                        expect(page.locator('#note-text')).to_have_value(edit)
                        expect(page.locator('#note-text')).to_be_focused()
                        headers = [f['before']['header'] for f in journey['frames']]
                        assert all(box == headers[0] for box in headers)
                        assert journey['frames'][0]['before']['orbit_transform'] == journey['frames'][-1]['after']['orbit_transform'], 'Returning preserves the deliberately paused decorative phase'
                        report['checks'].append(variant + ': saved-value view, shared header, draft, return focus and paused decorative phase')

                        quiet = episode('reduced-motion', 450,
                            [(0,'reduce-motion',None,None),(0,'click','#flip',None)],
                            note='Actual browser reduced-motion preference: equivalent back face without optional rotation or orbit.')
                        assert page.locator('#note-card').evaluate('(e)=>getComputedStyle(e).transitionDuration') == '0s'
                        assert page.locator('.orbit-arm').evaluate('(e)=>getComputedStyle(e).animationName') == 'none'
                        expect(page.locator('#motion-toggle')).to_be_disabled()
                        expect(page.locator('#note-card')).to_have_attribute('data-face', 'back')
                        assert quiet['frames'][-1]['after']['back_inert'] is False
                        report['checks'].append(variant + ': reduced motion preserves equivalent content and operative flip control')

                        # Reload proves actual persistence, separate from the recorded episodes.
                        page.reload(wait_until='load')
                        expect(page.locator('#note-text')).to_have_value(edit)
                        assert stored()['text'] == edit
                        report['storage_verified'] = True
                        report['checks'].append(variant + ': stored note survives document reload')
                        page.evaluate('window.__temporal.object = document.getElementById("note-card")')
                        if variant == 'narrow':
                            page.locator('#locale-toggle').click()
                            page.locator('#theme-toggle').click()
                        page.locator('#saved-link').click()
                        page.locator('footer summary').click()
                        page.evaluate('window.__temporal.failClear = true')
                        clearing = episode('clear-failure-from-saved-view', 1150,
                            [(0,'click','#clear',None),(650,'restore-clear',None,edit),(650,'click','#retry',None)],
                            note='Global footer clear fails at native removal boundary; the editor reveals and focuses its retry. Successful retry confirms actual removal.')
                        failures = [f['after'] for f in clearing['frames'] if f['after']['status'] == 'clearFailed']
                        assert failures and all(s['view'] == 'editor' and s['retry_visible'] and s['status_visible'] for s in failures)
                        assert stored() is None
                        assert [v['succeeded'] for v in page.evaluate('window.__temporal.removals')] == [False, True]
                        expect(page.locator('#note-text')).to_have_value('')
                        expect(page.locator('#note-text')).to_be_focused()
                        report['checks'].append(variant + ': global clear failure preserves storage and reveals focused recovery; native retry removes data')
                        # Corrupt the actual serialized record, then use the visible recovery path.
                        page.evaluate('(key) => localStorage.setItem(key, "{unreadable")', KEY)
                        page.reload(wait_until='load')
                        page.evaluate('window.__temporal.object = document.getElementById("note-card")')
                        if variant == 'narrow':
                            page.locator('#locale-toggle').click()
                            page.locator('#theme-toggle').click()
                        expect(page.locator('#save')).to_be_disabled()
                        unknown = episode('unreadable-saved-note', 1250,
                            [(0,'click','#saved-link',None),(650,'click','#return',None)], interval_ms=120,
                            note='Actual malformed Storage data remains unknown; saved view explains recovery and returns focus to the existing retry.')
                        collections = [f['after'] for f in unknown['frames'] if f['after']['view'] == 'collection']
                        assert collections
                        for state in collections:
                            assert state['saved_title'] == ('Saved note unavailable' if variant == 'desktop' else '暂时无法读取已存笔记')
                            assert ('retry' in state['saved_text'] if variant == 'desktop' else '重试' in state['saved_text'])
                        expect(page.locator('#retry')).to_be_focused()
                        page.locator('#retry').click()
                        expect(page.locator('#save')).to_be_disabled()
                        page.locator('footer summary').click()
                        page.locator('#clear').click()
                        expect(page.locator('#save')).to_be_enabled()
                        expect(page.locator('#note-text')).to_have_value('')
                        assert stored() is None
                        report['checks'].append(variant + ': unreadable data stays unknown, reachable retry retains failure, explicit clear restores local editing')
                    finally:
                        context.close()  # Finalizes Playwright video before inspecting file availability.
                        if media:
                            path = Path(media.path())
                            assert path.is_file() and path.stat().st_size > 0
                            report['videos'].append({'file': path.relative_to(output).as_posix(), 'variant': variant,
                                'size': viewport, 'bytes': path.stat().st_size,
                                'timeline': 'Whole context recording. Episode/action times are document performance timestamps; no exact video-time alignment is asserted.'})
                assert not report['page_errors'], report['page_errors']
                assert not report['external_requests'], report['external_requests']
                report['result'] = 'pass'
            finally:
                browser.close()
    except Exception as exc:
        report['result'] = 'fail'
        report['failure'] = str(exc)
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
    parser.add_argument('--no-video', action='store_true', help='Capture ordered images only; playback remains unobserved')
    args = parser.parse_args()
    result = validate(args.output_dir, args.browser_path, not args.no_video)
    print(json.dumps({'result': result['result'], 'episodes': len(result['episodes']),
                      'captures': sum(len(e['frames']) for e in result['episodes']),
                      'videos': len(result['videos']), 'storage_verified': result['storage_verified'],
                      'visual_review': result['visual_review']}, indent=2))
