#!/usr/bin/env python3
"""Exercise byte reuse on existing historical review bytes, not a new review."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    study = repo / 'docs/evidence/v1.20.0/session-study'
    here = study / 'support/current-continuation'
    temporary = Path(tempfile.mkdtemp(prefix='historical-review-reuse-validation-'))
    series = 'helper-validation-' + temporary.name
    frozen = study / 'continuation-2100/review' / series
    try:
        source = temporary / 'historical-review'
        subprocess.run([sys.executable, str(study / 'support/continuation/replay_review.py'),
                        '--repo', str(repo), '--snapshot',
                        'docs/evidence/v1.20.0/session-study/review/cohort-01/snapshot.json',
                        '--output', str(source)], check=True)
        snapshots = temporary / 'product-snapshots.json'
        snapshots.write_text(json.dumps([path.with_name('snapshot.json').relative_to(repo).as_posix()
                                        for path in sorted((study / 'runs').glob('*/run.json'))]))
        subprocess.run([sys.executable, str(here / 'freeze_review.py'), '--repo', str(repo),
                        '--source', str(source), '--review-series', series, '--cohort', 'cohort-01',
                        '--product-snapshots', str(snapshots)], check=True)
        snapshot = frozen / 'cohort-01/snapshot.json'
        subprocess.run([sys.executable, str(here / 'replay_review.py'), '--repo', str(repo),
                        '--snapshot', str(snapshot), '--output', str(temporary / 'reconstructed')], check=True)
        result = json.loads(snapshot.read_text())
        print(json.dumps({'status': 'passed', 'kind': 'helper validation over existing historical reviewer bytes; not a new reviewer execution',
                          'borrowed_files': result['borrowed_files_count'],
                          'overlay_archives': len(result['archives']['archives']),
                          'scope': 'Fresh input-plus-overlay helper reconstructed the historical review byte inventory without a repeated product pack. Temporary duplicate validation archives are removed after the check; original evidence is unchanged.'}, indent=2))
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
        shutil.rmtree(frozen, ignore_errors=True)


if __name__ == '__main__':
    main()
