"""Render complete numerical tables directly from the retained aggregate."""
from collections import Counter
from pathlib import Path
import json

base = Path(__file__).resolve().parents[1]
d = json.loads((base / 'analysis/results.json').read_text())
if d['scope'] != 'DESCRIPTIVE_COMPLETE':
    raise SystemExit('Incomplete comparison')
names = {'coherence':'任务与整体一致性', 'composition':'构图与空间稳定',
         'typography':'排版与阅读层级', 'material':'表面与素材整合',
         'states':'状态与动作表达', 'identity':'目标与独立辨识度'}

def n(value):
    return str(int(value)) if float(value).is_integer() else str(value)

def interval(value):
    return f'{n(value["median"])} [{n(value["range"][0])}–{n(value["range"][1])}]'

lines = ['# 完整数值表', '',
         '由 `RESULTS.json` 直接生成。视觉分数为六个独立的 0–4 级有序判断；不相加、不加权，不解释为能力比例。每个产物由三位独立版本盲评 Agent 评分。', '',
         '## 功能验收', '',
         '| 任务 | 重复 | v1.15.0 | v1.16.0 | B − A（通过组数） |',
         '| --- | ---: | ---: | ---: | ---: |']
runs = {r['run_id']: r for r in d['runs']}
for pair in d['matched_pairs']:
    a, b = runs[pair['A']], runs[pair['B']]
    lines.append(f'| {pair["task"]} | {pair["replicate"]} | {a["functional_passes"]}/10 | {b["functional_passes"]}/10 | {pair["functional_delta_B_minus_A"]:+d} |')
lines += ['', '这些是重复执行的验收组次，不是相互独立的用户任务样本。', '',
          '## 各版本的视觉分布', '',
          '每格为六个产物中位评分的中位数 [最小值–最大值]。偶数个产物的中位数可能为半级；这不改变原始评分是有序等级的性质。', '',
          '| 维度 | v1.15.0 | v1.16.0 |', '| --- | ---: | ---: |']
for dim in d['dimensions']:
    lines.append(f'| {names[dim]} | {interval(d["arms"]["A"]["visual_run_median_summary"][dim])} | {interval(d["arms"]["B"]["visual_run_median_summary"][dim])} |')
lines += ['', '## 六组配对差值与独立偏好', '',
          '差值为同任务、同重复序号的三评审中位等级 B − A。偏好来自每位评审对该任务四个产物的独立排序，允许并列；没有用六个维度相加推导偏好。', '',
          '| 配对 | 一致性 | 构图 | 排版 | 表面 | 状态 | 辨识度 | R1 / R2 / R3 | 多数偏好 |',
          '| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |']
vote_name = {'A':'A', 'B':'B', 'tie':'并列', None:'无多数'}
for pair in d['matched_pairs']:
    delta = ' | '.join(f'{int(pair["visual_median_deltas"][dim]):+d}' for dim in d['dimensions'])
    votes = ' / '.join(vote_name[p['preference']] for p in pair['reviewer_preferences'])
    lines.append(f'| {pair["task"]} · {pair["replicate"]} | {delta} | {votes} | {vote_name[pair["majority_preference"]]} |')
counts = Counter(p['majority_preference'] for p in d['matched_pairs'])
lines += ['', f'六组配对的多数偏好：A {counts["A"]} 组，B {counts["B"]} 组，并列 {counts["tie"]} 组，无多数 {counts[None]} 组。该计数只描述这六组产物。', '',
          '## 全部产物与评审分歧', '',
          '每格为三位评审的中位数 [最小值–最大值]。原始逐人分数与理由见 `reviews/`。', '',
          '| 产物 / 匿名 ID | 任务 · 重复 · 版本 | 功能 | 一致性 | 构图 | 排版 | 表面 | 状态 | 辨识度 |',
          '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
ordered = sorted(d['runs'], key=lambda r:(r['task'], r['replicate'], r['arm']))
for r in ordered:
    scores = ' | '.join(interval(r['visual'][dim]) for dim in d['dimensions'])
    lines.append(f'| `{r["run_id"]}` / {r["anonymous_id"]} | {r["task"]} · {r["replicate"]} · {r["version"]} | {r["functional_passes"]}/10 | {scores} |')
lines += ['', '## 时间、文件体积与日志诊断', '',
          '耗时为约定启动窗口至主评估者冻结的墙钟时间，含共享主机与调度中断。首个成功构建可能仍是初始工程。命令数只是留存条数；并发编号覆盖使其不能代表总工具调用或成本。构建目录包含未使用的历史 bundle 时，目录体积也不等于实际请求体积。', '',
          '| 产物 | 墙钟分钟 | 首个留存成功构建分钟 | 留存命令 | 日志摘要不符 | dist 字节 |',
          '| --- | ---: | ---: | ---: | ---: | ---: |']
for r in ordered:
    lines.append(f'| `{r["run_id"]}` | {r["wall_minutes_launch_window_to_freeze"]} | {r["first_successful_logged_build_minutes"]} | {r["retained_command_records"]} | {len(r["command_output_digest_mismatches"])} | {r["dist_bytes"]:,} |')
lines += ['', '以上诊断不支持开发效率、网络速度、FPS 或设备性能的因果比较。实际请求体积与阻断外部网络的逐产物观察见 `RESULTS.json` 的 `asset_diagnostic`。', '']
dest = base / 'analysis/TABLES.zh-CN.md'
dest.write_text('\n'.join(lines), encoding='utf-8')
print(json.dumps({'output':str(dest), 'pairs':6, 'outputs':12, 'dimensions':6, 'majority_counts':dict(counts)}, ensure_ascii=False))
