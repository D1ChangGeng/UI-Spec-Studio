"""Replay identity and input comparability, without grading design or messages."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from source_continuity import runtime_v117, runtime_v118

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT/'docs/experiments/observable-execution'
SPEC = importlib.util.spec_from_file_location('observable_replay', ROOT/'tools/replay_granularity_run.py')
REPLAY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPLAY)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def archive_files(path):
    with zipfile.ZipFile(path) as archive:
        return {name:archive.read(name) for name in archive.namelist()}


class ObservableStudyIdentityTests(unittest.TestCase):
    def test_three_complete_runtime_inputs_match_frozen_registration(self):
        registration = json.loads((STUDY/'registration.json').read_text(encoding='utf-8'))
        for code, expected in registration['runtime'].items():
            with self.subTest(condition=code):
                content = archive_files(STUDY/'inputs'/f'runtime-{code}.zip')
                self.assertEqual({name.removeprefix('ui-spec/'):digest(value)
                                  for name,value in content.items()}, expected)
        a = archive_files(STUDY/'inputs/runtime-s8.zip')
        c = archive_files(STUDY/'inputs/runtime-k2.zip')
        self.assertEqual(len(a), 37)
        self.assertEqual(len(c), 37)
        for name, value in a.items():
            relative = name.removeprefix('ui-spec/')
            self.assertEqual(value, runtime_v117(ROOT, 'skills/ui-spec/'+relative))
        for name, value in c.items():
            self.assertEqual(value, runtime_v118(ROOT, 'skills/'+name))

    def test_visibility_comparison_preserves_baseline_except_declared_module(self):
        a = archive_files(STUDY/'inputs/runtime-s8.zip')
        b = archive_files(STUDY/'inputs/runtime-v5.zip')
        changed = {name for name in a.keys() | b.keys() if a.get(name) != b.get(name)}
        self.assertEqual(changed, {'ui-spec/SKILL.md','ui-spec/references/observable-visibility.md'})
        self.assertEqual(b['ui-spec/references/observable-visibility.md'],
                         (STUDY/'visibility-module.md').read_bytes())

    def test_each_completed_application_replays_exactly_with_common_starters(self):
        registration = json.loads((STUDY/'registration.json').read_text(encoding='utf-8'))
        starters = {}
        for cell in registration['cells']:
            with self.subTest(cell=cell['cell']):
                archive = STUDY/'runs'/cell['cell']
                index = json.loads((archive/'archive-index.json').read_text(encoding='utf-8'))
                for stage in ('initial','final'):
                    with tempfile.TemporaryDirectory() as temp:
                        output = Path(temp)/'restored'
                        REPLAY.restore(archive, output, stage)
                        actual = {p.relative_to(output).as_posix():digest(p.read_bytes())
                                  for p in output.rglob('*') if p.is_file()}
                        self.assertEqual(actual,{p:r['sha256'] for p,r in index['snapshots'][stage]['files'].items()})
                        if stage == 'initial':
                            expected = {'app/'+p:h for p,h in cell['starter'].items()}
                            self.assertEqual(actual, expected)
                            self.assertEqual(actual, starters.setdefault(cell['task'], actual))
                for name, row in index['bundles'].items():
                    self.assertEqual(digest((archive/name).read_bytes()), row['sha256'])
                evidence = {}
                for name in index['bundles']:
                    if name.startswith('participant-evidence'):
                        evidence.update({p:digest(v) for p,v in archive_files(archive/name).items()})
                self.assertEqual(evidence, index['evidence_members'])

    def test_outward_text_and_contemporary_source_are_retained_without_reconstruction(self):
        registration = json.loads((STUDY/'registration.json').read_text(encoding='utf-8'))
        received = [json.loads(line) for line in (STUDY/'received-relays.jsonl').read_text(encoding='utf-8').splitlines()]
        received = {(row['cell'],row['id']):row for row in received if 'id' in row}
        for cell in registration['cells']:
            archive = STUDY/'runs'/cell['cell']
            index = json.loads((archive/'archive-index.json').read_text(encoding='utf-8'))
            for item in index['messages']:
                path = archive/item['path']
                row = json.loads(path.read_text(encoding='utf-8'))
                with self.subTest(cell=cell['cell'],message=row['id']):
                    self.assertEqual(digest(path.read_bytes()),item['sha256'])
                    self.assertEqual(digest(row['text'].encode()), row['text_sha256'])
                    source = archive_files(path.parent/row['source_archive'])
                    self.assertEqual({p:digest(v) for p,v in source.items()}, row['source_files'])
                    receipt = received[(cell['cell'],row['id'])]
                    if 'text' in receipt:
                        # Early coordinator receipts retained rendered text; their
                        # terminal LF is presentation-only, not a changed message.
                        self.assertEqual(receipt['text'].rstrip('\n'), row['text'].rstrip('\n'))
                    else:
                        self.assertEqual(receipt['archived_text_sha256'], row['text_sha256'])
            self.assertEqual(row['channel'], 'final')
            self.assertEqual(row['source_files'], {p:v['sha256'] for p,v in index['snapshots']['final']['files'].items()})


if __name__ == '__main__':
    unittest.main()
