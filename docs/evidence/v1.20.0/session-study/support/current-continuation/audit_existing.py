#!/usr/bin/env python3
"""Verify retained study records and reconstruct historical snapshots only."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    study = repo / 'docs/evidence/v1.20.0/session-study'
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    support = study / 'support'
    sys.path.insert(0, str(repo / 'tools'))
    from check_adaptive_release import candidate_identity
    plan = json.loads((study / 'registration.json').read_text())
    initial = candidate_identity(repo)
    rows = []

    def capture(name, command):
        log = output / name
        result = subprocess.run([sys.executable, str(support / 'capture_command.py'),
                                 '--output', str(log), '--cwd', str(repo), '--timeout', '600',
                                 '--', *command], capture_output=True, check=False)
        # capture_command.py already retains the original subprocess streams.
        print(json.dumps({'check': name, 'returncode': result.returncode}), flush=True)
        rows.append({'check': name, 'returncode': result.returncode,
                     'command_record': {'path': (log / 'command.json').relative_to(repo).as_posix(),
                                        'sha256': sha(log / 'command.json')}})
        return result.returncode

    records = sorted((study / 'runs').glob('*/run.json'))
    historical = sorted((study / 'runs').glob('*/snapshot.json'))
    historical += sorted((study / 'incomplete-attempts').glob('*/snapshot.json'))
    # Inventory only retained repository evidence, never live participant worksets.
    fixed_roots = ['coordination/final-session', 'engineering/final-session',
                   'review/coordinator-final', 'supplementary-runs', 'incomplete-attempts']
    preserved = {p.relative_to(repo).as_posix(): sha(p)
                 for name in fixed_roots for p in (study / name).rglob('*') if p.is_file()}
    write(output / 'historical-file-identities.json', preserved)
    capture('completed-records', [sys.executable, str(support / 'check_partial_records.py'), '--repo', str(repo)])
    replay_temp = Path(tempfile.mkdtemp(prefix='ui-study-history-replay-'))
    try:
        for snapshot in historical:
            data = json.loads(snapshot.read_text())
            destination = replay_temp / snapshot.parent.name
            capture('reconstruct-' + snapshot.parent.name,
                    [sys.executable, str(support / 'continuation/replay_snapshot.py'),
                     '--repo', str(repo), '--cell', data['cell_id'],
                     '--snapshot-directory', str(snapshot.parent), '--output', str(destination)])
            shutil.rmtree(destination, ignore_errors=True)
        for snapshot in sorted((study / 'review').glob('cohort-*/snapshot.json')):
            destination = replay_temp / snapshot.parent.name
            capture('reconstruct-review-' + snapshot.parent.name,
                    [sys.executable, str(support / 'continuation/replay_review.py'),
                     '--repo', str(repo), '--snapshot', snapshot.relative_to(repo).as_posix(),
                     '--output', str(destination)])
            shutil.rmtree(destination, ignore_errors=True)
    finally:
        shutil.rmtree(replay_temp, ignore_errors=True)
    preservation = []
    for path in sorted((study / 'incomplete-attempts').glob('*/preservation-index.json')):
        data = json.loads(path.read_text())
        count = 0
        for member in data['archives']['members']:
            archive = path.parent / member['archive']
            with zipfile.ZipFile(archive) as handle:
                raw = handle.read(member['path'])
            if hashlib.sha256(raw).hexdigest() != member['sha256'] or len(raw) != member['bytes']:
                raise ValueError('Preserved original differs: ' + member['path'])
            count += 1
        for archive in data['archives']['archives']:
            if sha(path.parent / archive['file']) != archive['sha256']:
                raise ValueError('Preservation archive differs')
        preservation.append({'index': path.relative_to(repo).as_posix(), 'verified_members': count,
                             'counted_as_completed': False})
    current = candidate_identity(repo)
    changed = [name for name, digest in preserved.items() if sha(repo / name) != digest]
    report = {'schema_version': 1, 'kind': 'coordinator consistency audit; not independent review or release acceptance',
              'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'completed_records': len(records), 'historical_snapshots': len(historical),
              'candidate_identity_before': initial, 'candidate_identity_after': current,
              'registered_candidate_identity': plan['candidate_source_identity'],
              'candidate_unchanged_and_registered': initial == current == plan['candidate_source_identity'],
              'historical_files_inventoried': len(preserved), 'historical_files_changed': changed,
              'checks': rows, 'partial_preservation_checks': preservation,
              'scope': 'Original retained bytes and declared participant/product structure. Includes negative behavior evidence without converting it to a product failure threshold. No active worksets accessed; no completion or review judgments created.'}
    write(output / 'audit.json', report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return int(any(row['returncode'] for row in rows) or bool(changed) or not report['candidate_unchanged_and_registered'])


if __name__ == '__main__':
    raise SystemExit(main())
