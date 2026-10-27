"""Publish consistent inspection surfaces after every planned review is complete."""
from pathlib import Path
import hashlib
import json
import shutil

base = Path(__file__).resolve().parents[1]
dest = base.parent / 'ui-spec-studio/docs/experiments/visual-craft/campaign-20261028'
result = json.loads((base / 'analysis/results.json').read_text())
if result['scope'] != 'DESCRIPTIVE_COMPLETE' or result['runs_completed'] != 12 or result['reviews_completed'] != 3:
    raise SystemExit('Complete original observations and blind reviews are required')

shutil.copy2(base / 'analysis/results.json', dest / 'RESULTS.json')
for name in ['blind-map.json', 'finalization-plan.json', 'publication.json']:
    shutil.copy2(base / 'private' / name, dest / name)
for index in range(1, 4):
    folder = dest / 'reviews' / f'R{index}'
    folder.mkdir(parents=True, exist_ok=True)
    for p in (base / 'reviews' / f'R{index}').iterdir():
        if p.is_file():
            shutil.copy2(p, folder / p.name)
    shutil.copy2(base / 'blind-review' / f'ORDER-{index}.json', folder / 'ORDER.json')

primary = {'T1': ['01-desktop-initial.png', '04-source-detail.png', '09-mobile-original-theme.png'],
           'T2': ['01-desktop-initial.png', '06-detail.png', '10-overview-390.png'],
           'T3': ['01-source-compact.png', '04-expanded.png', '09-sheet-390.png']}
family_names = {'T1': 'Folio：完整研究对话前端', 'T2': 'ATELIER：高表现力专业工作区', 'T3': 'Margin：局部阅读面板与动作'}
lines = ['# 统一条件下的全部产物', '',
         '本页保留每个产物预先选定的八种静态观察条件；没有按表现筛选实现或替换结果。缩略图用于定位，点击原图可查看完整分辨率。动态片段、逐帧时间线和其他功能状态在对应的完整证据归档中。', '',
         '版本与匿名标识在三份独立盲评完成后公开。图像不是功能通过证明，也不代表人类用户测试或自然视频播放评估。', '']
manifest = []
for task in ['T1', 'T2', 'T3']:
    lines += [f'## {family_names[task]}', '']
    rows = sorted([r for r in result['runs'] if r['task'] == task], key=lambda r: (r['replicate'], r['arm']))
    for row in rows:
        rid, aid = row['run_id'], row['anonymous_id']
        packet = base / 'blind-review' / aid
        evidence = json.loads((packet / 'EVIDENCE.json').read_text())
        folder = dest / 'gallery' / rid
        folder.mkdir(parents=True, exist_ok=True)
        for name in evidence['images']:
            source = packet / name
            target = folder / name
            shutil.copy2(source, target)
            manifest.append({'run_id': rid, 'anonymous_id': aid, 'file': str(target.relative_to(dest)),
                             'bytes': target.stat().st_size, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
        lines += [f'### {row["version"]} · 重复 {row["replicate"]} · {aid}', '',
                  f'产物 `{rid}`。独立功能验收 {row["functional_passes"]}/{row["functional_total"]} 组。', '',
                  '| 桌面主视图 | 主要详情 / 展开视图 | 窄屏使用 |',
                  '| --- | --- | --- |']
        cells = []
        for name in primary[task]:
            if name in evidence['images']:
                rel = f'gallery/{rid}/{name}'
                cells.append(f'[![{aid} {name}]({rel})]({rel})')
            else:
                cells.append('该预定观察条件未生成；见原始中断证据。')
        lines += ['| ' + ' | '.join(cells) + ' |', '',
                  '全部预定静态条件：' + ' · '.join(f'[{name}](gallery/{rid}/{name})' for name in evidence['images']), '']
        if evidence['unavailable_images']:
            lines += ['缺失条件：' + ', '.join(evidence['unavailable_images']), '']

reference = dest / 'gallery/T1-reference'
reference.mkdir(parents=True, exist_ok=True)
for p in (base / 'blind-review/T1-reference').iterdir():
    if p.is_file():
        shutil.copy2(p, reference / p.name)
source_license = base / 'references/perplexica/LICENSE'
if source_license.exists():
    shutil.copy2(source_license, reference / 'LICENSE')
lines += ['## 共同产品参考', '',
          'Vane（原 Perplexica）作者提供的三个画面用于对齐相同前端任务范围的视觉成熟度。它们来自当前与历史界面，不能视为对现行商业服务所有功能的测量。', '',
          '- [当前作者视图](gallery/T1-reference/author-current-view.png)',
          '- [历史起始视图](gallery/T1-reference/author-historical-empty-view.png)',
          '- [历史回答视图](gallery/T1-reference/author-historical-answer-view.png)',
          '- [固定来源与提交身份](gallery/T1-reference/IDENTITY.json)', '']
(dest / 'GALLERY.md').write_text('\n'.join(lines), encoding='utf-8')
(dest / 'gallery/MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

checkpoint = json.loads((dest / 'CHECKPOINT.json').read_text())
checkpoint.update(scope='Completed descriptive comparison; all assigned originals and independent reviews retained',
                  completed_runs=12, visual_reviews_completed=3)
(dest / 'CHECKPOINT.json').write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'published_gallery_images': len(manifest), 'reviews': 3, 'runs': 12, 'destination': str(dest)}))
