#!/usr/bin/env python3
"""Freeze one completed participant run; do not infer design quality or review."""
from __future__ import annotations
import argparse, datetime, hashlib, json, shutil, subprocess, zipfile
from pathlib import Path

EXCLUDED = {'node_modules', '.git', 'dist', '__pycache__', '.pytest_cache'}


def digest(value):
    return hashlib.sha256(value).hexdigest()


def files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob('*'))
            if p.is_file() and not p.is_symlink()
            and not EXCLUDED.intersection(p.relative_to(root).parts)}


def bundle(path, contents):
    with zipfile.ZipFile(path, 'x', compression=zipfile.ZIP_DEFLATED) as output:
        for name, content in sorted(contents.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 10, 30, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            output.writestr(info, content)


def evidence_bundles(target, contents):
    """Keep each independent ZIP comfortably below the publication transport cap."""
    groups = []
    group = {}
    size = 0
    for name, content in sorted(contents.items()):
        if group and size + len(content) > 8_000_000:
            groups.append(group)
            group, size = {}, 0
        group[name] = content
        size += len(content)
    groups.append(group)
    names = []
    for i, group in enumerate(groups, 1):
        name = 'participant-evidence.zip' if len(groups) == 1 else f'participant-evidence-{i:02d}.zip'
        bundle(target/name, group)
        names.append(name)
    return names


def freeze(workspace, study):
    registration = json.loads((study/'registration.json').read_text())
    cell = next(row for row in registration['cells'] if row['cell'] == workspace.name)
    target = study/'runs'/workspace.name
    if target.exists():
        raise ValueError('Preserve an already frozen run')
    outward = sorted((workspace/'outward').glob('message-*.json'))
    if not outward or json.loads(outward[-1].read_text())['channel'] != 'final':
        raise ValueError('A completed actual final message is required')
    final = files(workspace/'app')
    last = json.loads(outward[-1].read_text())
    if last['source_files'] != {'app/'+name:digest(content) for name, content in final.items()}:
        raise ValueError('Application differs from final-message source; investigate before freezing')
    if cell['task'] == 'T1':
        with zipfile.ZipFile(study/'t1-input.zip') as archive:
            initial = {name.removeprefix('app/'):archive.read(name)
                       for name in archive.namelist() if name.startswith('app/') and not name.endswith('/')}
    else:
        repo = study.parents[2]
        prefix = {'T2':'examples/temporal-review/','T3':'examples/content-review/'}[cell['task']]
        initial = {name: subprocess.check_output(['git','show',registration['baseline']+':'+prefix+name],cwd=repo)
                   for name in cell['starter']}
    if {name:digest(content) for name,content in initial.items()} != cell['starter']:
        raise ValueError('Initial input differs from corrected registration')
    first = json.loads(outward[0].read_text())
    first_initial_match = first['source_files'] == {'app/'+name:digest(content) for name,content in initial.items()}
    target.mkdir(parents=True)
    index = {'cell':workspace.name,'task':cell['task'],'condition':cell['condition'],
             'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'first_recorded_message_at':first['recorded_at'],
             'final_recorded_message_at':last['recorded_at'],
             'first_message_source_matches_starter':first_initial_match,
             'final_message_source_matches_final':True,
             'snapshots':{},'scope':'Actual participant outputs, not independent review or human acceptance.'}
    for stage, contents in [('initial',initial),('final',final)]:
        name=f'app-{stage}.zip'
        bundle(target/name, {'app/'+p:content for p,content in contents.items()})
        index['snapshots'][stage]={'files':{'app/'+p:{'path':name,'member':'app/'+p,'sha256':digest(content)}
                                            for p,content in contents.items()}}
    for name in ('TASK.md','ENVIRONMENT.md'):
        shutil.copyfile(workspace/name,target/name)
    if cell['task'] == 'T1':
        # Keep the upstream notice next to each independently replayable source.
        # This does not modify the participant's final application bytes.
        with zipfile.ZipFile(study/'t1-input.zip') as archive:
            (target/'LICENSE-MagicUI.md').write_bytes(archive.read('resources/LICENSE.md'))
    shutil.copytree(workspace/'outward',target/'outward')
    evidence = files(workspace/'evidence') if (workspace/'evidence').exists() else {}
    evidence_archives = evidence_bundles(target,evidence)
    notes = {name:content for name,content in files(workspace).items()
             if name.split('/')[0] not in {'app','ui-spec','evidence','outward','resources'}
             and name not in {'modern-web-guidance.txt','TASK.md','ENVIRONMENT.md','record_design_message.py'}}
    bundle(target/'participant-notes.zip',notes)
    index['bundles']={name:{'sha256':digest((target/name).read_bytes()),'bytes':(target/name).stat().st_size}
                      for name in ('app-initial.zip','app-final.zip','participant-notes.zip',*evidence_archives)}
    index['evidence_archives'] = evidence_archives
    index['evidence_members']={name:digest(content) for name,content in evidence.items()}
    index['notes_members']={name:digest(content) for name,content in notes.items()}
    index['messages']=[{'path':'outward/'+p.name,'sha256':digest(p.read_bytes())} for p in outward]
    (target/'archive-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
    return {'cell':workspace.name,'files':len(final),'evidence':len(evidence),'messages':len(outward),
            'first_message_source_matches_starter':first_initial_match}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workspace',type=Path)
    args=parser.parse_args()
    print(json.dumps(freeze(args.workspace.resolve(),Path(__file__).resolve().parent),indent=2))
