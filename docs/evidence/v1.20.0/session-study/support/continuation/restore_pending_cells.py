from pathlib import Path
import datetime, hashlib, json, shutil, sys

REPO = Path('/workspace/scratch/1e61855ad686/UI-Spec-Studio')
STUDY = REPO / 'docs/evidence/v1.20.0/session-study'
sys.path.insert(0, str(STUDY / 'support'))
from replay_snapshot import extract

plan = json.loads((STUDY / 'registration.json').read_text())
records = []
for cell_id in ('T2-C-r1', 'T3-A-r1'):
    cell = next(x for x in plan['cells'] if x['id'] == cell_id)
    work = Path(cell['work_package'])
    snapshot = json.loads((STUDY / 'incomplete-attempts' / (cell_id + '-previous-session') / 'snapshot.json').read_text())
    for name, expected in snapshot['workspace_files'].items():
        assert hashlib.sha256((work / name).read_bytes()).hexdigest() == expected, name
    retained = work.parent.parent / 'unconfirmed-worksets' / (work.name + '-previous-session')
    retained.parent.mkdir(exist_ok=True)
    assert not retained.exists()
    work.rename(retained)
    work.mkdir()
    for ref in cell['input_artifacts']:
        path = REPO / ref['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == ref['sha256']
        prefix = 'method/' if path.name.startswith('method-v') else ('roles/' if path.name == 'distributed-role-instructions.zip' else '')
        extract(path, work, prefix)
    actual = {p.relative_to(work).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in work.rglob('*') if p.is_file()}
    assert actual == cell['workspace_files'], cell_id
    dependency = retained / 'app/node_modules'
    if dependency.exists():
        shutil.copytree(dependency, work / 'app/node_modules', symlinks=True)
    records.append({'cell_id': cell_id, 'retained_previous_workspace': str(retained), 'restored_frozen_workspace': str(work), 'verified_input_files': len(actual), 'source_and_prompt_changed': False})
output = {'kind': 'actual coordinator restoration command output', 'completed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'records': records}
print(json.dumps(output, indent=2))
