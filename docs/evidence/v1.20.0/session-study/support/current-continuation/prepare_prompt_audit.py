#!/usr/bin/env python3
"""Retain the exact actual dispatch and describe its frozen-prompt difference."""
import argparse
import datetime
import difflib
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--cell', required=True)
    parser.add_argument('--spawn', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    study = repo / 'docs/evidence/v1.20.0/session-study'
    plan = json.loads((study / 'registration.json').read_text())
    cell = next(row for row in plan['cells'] if row['id'] == args.cell)
    spawn = json.loads(args.spawn.read_text())
    if spawn['request']['fork_turns'] != 'none':
        raise ValueError('Fresh actual dispatch required')
    original_path = repo / cell['prompt']['path']
    original = original_path.read_bytes()
    if hashlib.sha256(original).hexdigest() != cell['prompt']['sha256']:
        raise ValueError('Frozen original prompt differs')
    actual = spawn['request']['message'].encode()
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / 'registered-prompt.txt').write_bytes(original)
    (args.output / 'actual-dispatched-prompt.txt').write_bytes(actual)
    (args.output / 'prompt-diff.txt').write_text(''.join(difflib.unified_diff(
        original.decode().splitlines(True), actual.decode().splitlines(True),
        fromfile='registered-prompt', tofile='actual-dispatched-prompt')))

    def reference(path):
        return {'path': path.resolve().relative_to(repo).as_posix(),
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

    result = {'schema_version': 1, 'kind': 'coordinator-derived dispatch deviation audit; not original tool output',
              'cell_id': args.cell, 'agent_id': spawn['result']['task_name'],
              'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'spawn_export': reference(args.spawn), 'registered_prompt': reference(original_path),
              'actual_dispatched_prompt': reference(args.output / 'actual-dispatched-prompt.txt'),
              'diff': reference(args.output / 'prompt-diff.txt'), 'byte_identical_dispatch': original == actual,
              'deviation_scope': 'The actual spawn message is retained exactly. The registered prompt is unchanged. Current dispatch uses a replacement executor workspace prefix and appends explicit path/evidence/fresh-time-bound instructions; this audit does not treat the resulting bytes as the registered dispatch.',
              'timing_scope': 'spawn exported_at is export time only, not participant run start.',
              'acceptance_scope': 'This record preserves a deviation for coordinator/reviewer adjudication. It does not amend registration or establish original-protocol equivalence or completed participation.'}
    (args.output / 'audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
