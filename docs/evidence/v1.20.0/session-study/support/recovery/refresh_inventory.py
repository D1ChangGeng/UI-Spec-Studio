#!/usr/bin/env python3
"""Update the dated study navigation from retained records, not delivered messages."""
from pathlib import Path
import argparse
import datetime
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    study = repo / 'docs/evidence/v1.20.0/session-study'
    status_path = repo / 'docs/experiments/adaptive-research/execution-status.json'
    status = json.loads(status_path.read_text())
    plan = json.loads((study / 'registration.json').read_text())
    records = {}
    for path in sorted((study / 'runs').glob('*/run.json')):
        value = json.loads(path.read_text())
        if value['status'] != 'completed' or value['cell_id'] in records:
            raise ValueError('Noncompleted or duplicate current record')
        records[value['cell_id']] = (path, value)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    children = sum(len(value['children']) for path, value in records.values())
    active = status.get('active_primary_cells', {})
    if set(active) & set(records):
        raise ValueError('A completed run must be removed from the active observation')
    lines = ['## Execution inventory', '',
             f'Observed {now}. **{len(records)} of {len(plan["cells"])}** registered cells have retained completed evidence records, with **{children}** completed child contexts. Execution coverage is distinct from product success and release approval.', '',
             status['independent_product_acceptance'], '',
             '| Cell | Condition | Retained status | Completed children |',
             '| --- | --- | --- | ---: |']
    for cell in plan['cells']:
        name = cell['id']
        if name in records:
            path, value = records[name]
            directory = path.parent.relative_to(study).as_posix()
            state = f'[Completed record]({directory}/run.json) · [product]({directory}/FINAL.md)'
            count = str(len(value['children']))
        elif name in active:
            state, count = 'Fresh execution active; terminal evidence not yet retained', 'Active'
        else:
            state, count = 'Frozen inputs restored; fresh complete evidence required', '—'
        lines.append(f"| {name} | {cell['condition']} | {state} | {count} |")
    readme = study / 'README.md'
    text = readme.read_text()
    start, end = text.index('## Execution inventory'), text.index('## What is retained')
    text = text[:start] + '\n'.join(lines) + '\n\n' + text[end:]
    text = text.replace('The T1-C and T2-B prompt audits', 'The T1-C, T2-B and T4-G prompt audits')
    readme.write_text(text)
    status.update(observed_at_utc=now, completed_primary_cells=len(records),
                  completed_child_contexts=children, completed_cell_ids=sorted(records))
    status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'completed': len(records), 'children': children, 'active': active}))


if __name__ == '__main__':
    main()
