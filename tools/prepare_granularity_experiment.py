#!/usr/bin/env python3
"""Freeze isolated application inputs; do not execute, rate or certify Agent work."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MATERIAL = ROOT / 'docs/experiments/adaptive-granularity'
ARM_CODES = {'A': 'p7', 'B': 'r4', 'C': 'm9'}
POINTER = ('\n## Scope judgment for the current work\n\n'
           'Read [the scope judgment](references/scope-judgment.md) before choosing '
           'the implementation increment, and apply it with the existing professional methods.\n')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def snapshot(root: Path) -> dict[str, bytes]:
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Input must be a real directory')
    result = {}
    for p in sorted(root.rglob('*')):
        if p.is_symlink():
            raise ValueError('Symlink in experiment source')
        if '__pycache__' in p.parts or p.suffix == '.pyc':
            continue
        if p.is_file():
            result[p.relative_to(root).as_posix()] = p.read_bytes()
    return result


def write_files(root: Path, files: dict[str, bytes]) -> None:
    for relative, content in files.items():
        p = root/relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)


def build(baseline: Path, output: Path, treatment: Path | None = None) -> dict:
    source = snapshot(baseline)
    expected = json.loads((MATERIAL/'baseline-identity.json').read_text(encoding='utf-8'))
    if {p: digest(b) for p, b in source.items()} != expected['files']:
        raise ValueError('Baseline differs from the frozen complete v1.16.1 runtime')
    if output.exists() or output.is_symlink():
        raise ValueError('Output already exists; preserve earlier runs')
    parent = output.parent.resolve(strict=True)
    output = parent/output.name
    if output.is_relative_to(baseline.resolve()) or output.is_relative_to((treatment or ROOT/'skills/ui-spec').resolve()):
        raise ValueError('Output must be outside Skill inputs')
    judgment = dict(source)
    judgment['SKILL.md'] += POINTER.encode('utf-8')
    judgment['references/scope-judgment.md'] = (MATERIAL/'judgment-module.md').read_bytes()
    arms = {'A': source, 'B': judgment, 'C': snapshot(treatment or ROOT/'skills/ui-spec')}
    tasks = json.loads((MATERIAL/'tasks.json').read_text(encoding='utf-8'))
    record = {'status': 'prepared_not_run', 'baseline_commit': expected['commit'],
              'scope': 'Nine independent condition/family cells, each with a same-Agent continuation',
              'participant_runs_executed': 0, 'arm_codes': ARM_CODES,
              'arms': {name: {p: digest(b) for p, b in files.items()} for name, files in arms.items()},
              'cells': [], 'initial_ceiling_minutes': 18, 'continuation_ceiling_minutes': 8}
    stage = Path(tempfile.mkdtemp(prefix='.granularity-', dir=parent))
    try:
        for task in tasks:
            tid = task['id']
            if not isinstance(tid, str) or not tid.isalnum():
                raise ValueError('Unsafe task identifier')
            initial = (MATERIAL/task['initial']).read_bytes()
            followup = (MATERIAL/task['continuation']).read_bytes()
            starter = snapshot(ROOT/task['starter']) if task.get('starter') else {}
            reference = snapshot(ROOT/task['reference']) if task.get('reference') else {}
            for arm, files in arms.items():
                cell_id = f'{tid}-{ARM_CODES[arm]}'
                cell = stage/cell_id
                write_files(cell/'ui-spec', files)
                (cell/'app').mkdir(parents=True)
                write_files(cell/'app', starter)
                if reference:
                    write_files(cell/'reference-project', reference)
                (cell/'TASK.md').write_bytes(initial)
                # Follow-ups stay outside participant directories until the first delivery.
                pending = stage/'continuations'/cell_id
                pending.mkdir(parents=True)
                (pending/'TASK.md').write_bytes(followup)
                record['cells'].append({'cell': cell_id, 'task': tid, 'arm': arm,
                    'initial_sha256': digest(initial), 'continuation_sha256': digest(followup),
                    'starter': {p: digest(b) for p, b in starter.items()},
                    'reference': {p: digest(b) for p, b in reference.items()},
                    'status': 'prepared_not_run'})
        (stage/'registration.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
        stage.rename(output)
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build(args.baseline, args.output)
        print(json.dumps({'status': result['status'], 'cells': len(result['cells']),
                          'participant_runs_executed': 0, 'output': str(args.output)}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'prepare_granularity_experiment: {exc}', file=__import__('sys').stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
