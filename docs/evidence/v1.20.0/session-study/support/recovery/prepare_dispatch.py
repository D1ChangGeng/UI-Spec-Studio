#!/usr/bin/env python3
"""Verify untouched registered inputs and record intent before an actual dispatch."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--cell', required=True)
    parser.add_argument('--task-name', required=True)
    parser.add_argument('--record-suffix', default='')
    args = parser.parse_args()
    repo, root = args.repo.resolve(), args.root.resolve()
    study = repo / 'docs/evidence/v1.20.0/session-study'
    plan = json.loads((study / 'registration.json').read_text())
    cell = next(row for row in plan['cells'] if row['id'] == args.cell)
    dispatch = next(row for row in json.loads((root / 'ui-study/dispatch-map.json').read_text()) if row['id'] == args.cell)
    workspace = Path(dispatch['work_package'])
    actual = {}
    for path in workspace.rglob('*'):
        if not path.is_file():
            continue
        relative = path.relative_to(workspace).as_posix()
        if relative.startswith('app/node_modules/'):
            continue
        actual[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != cell['workspace_files']:
        missing = sorted(set(cell['workspace_files']) - set(actual))
        extra = sorted(set(actual) - set(cell['workspace_files']))
        changed = sorted(name for name in actual.keys() & cell['workspace_files'].keys() if actual[name] != cell['workspace_files'][name])
        raise ValueError(json.dumps({'input_mismatch': args.cell, 'missing': missing, 'extra': extra, 'changed': changed}))
    raw_prompt = (repo / cell['prompt']['path']).read_bytes()
    if hashlib.sha256(raw_prompt).hexdigest() != cell['prompt']['sha256']:
        raise ValueError('Frozen prompt differs from registration')
    prompt = raw_prompt.decode('utf-8')
    if prompt != dispatch['prompt']:
        raise ValueError('Dispatch map differs from the exact frozen prompt')
    if '/' in args.task_name or not args.task_name:
        raise ValueError('Use a fresh simple task name')
    if args.record_suffix and (not args.record_suffix.startswith('-') or not all(c.isalnum() or c == '-' for c in args.record_suffix)):
        raise ValueError('Use an explicit alphanumeric attempt suffix beginning with a hyphen')
    record_name = args.cell + args.record_suffix
    recovery = study / 'coordination/recovery-0830'
    intent = recovery / (record_name + '-dispatch-intent.json')
    if intent.exists():
        raise ValueError('Do not overwrite a previous dispatch intent')
    old = study / 'coordination' / (args.cell + '-spawn.json')
    if old.exists():
        preserved = recovery / ('prior-' + record_name + '-spawn.json')
        if preserved.exists() and preserved.read_bytes() != old.read_bytes():
            raise ValueError('Previous dispatch preservation collision')
        shutil.copyfile(old, preserved)
    record = {'kind': 'dispatch preparation, not a spawn result',
              'observed_request_prepared_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'request': {'task_name': args.task_name, 'fork_turns': 'none', 'message': prompt},
              'prompt_sha256': cell['prompt']['sha256'], 'input_file_count': len(actual),
              'scope': 'Fresh exact registered inputs. Earlier unavailable attempt outputs are neither supplied nor counted. Dependency cache is excluded; its separate preparation record remains retained.'}
    intent.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'intent': str(intent), **record}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
