#!/usr/bin/env python3
"""Snapshot, reconstruct and index one actually completed supplementary attempt."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('configuration', type=Path)
    args = parser.parse_args()
    configuration = args.configuration.resolve()
    cfg = json.loads(configuration.read_text())
    repo = Path(cfg['repo']).resolve()
    support = repo / 'docs/evidence/v1.20.0/session-study/support'
    here = support / 'current-continuation'
    output = (repo / cfg['evidence_directory']).resolve()
    output.relative_to(repo / 'docs/evidence/v1.20.0/session-study/continuation-2100')
    if output.exists():
        raise FileExistsError('Use a fresh evidence directory; preserve unsuccessful stages')

    def capture(log, command):
        result = subprocess.run([sys.executable, str(support / 'capture_command.py'),
                                 '--output', str(log), '--cwd', str(repo), '--timeout', '600',
                                 '--', *command], check=False)
        if result.returncode:
            raise SystemExit(result.returncode)

    capture(output.parent / (output.name + '-freeze-command'),
            [sys.executable, str(here / 'freeze_cell.py'), '--repo', str(repo),
             '--cell', cfg['cell_id'], '--source', cfg['source_workspace'], '--output', str(output),
             '--spawn', str(repo / cfg['spawn_repository_path']),
             '--completion', str(repo / cfg['completion_repository_path'])])
    capture(output / 'reconstruction-check',
            [sys.executable, str(support / 'continuation/replay_snapshot.py'),
             '--repo', str(repo), '--cell', cfg['cell_id'], '--snapshot-directory', str(output),
             '--output', cfg['replay_directory']])
    capture(output / 'index-command', [sys.executable, str(here / 'index_cell.py'), str(configuration)])


if __name__ == '__main__':
    main()
