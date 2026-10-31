"""Release byte identity and reversible history, without judging UI policy or quality."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from source_continuity import runtime_v118, runtime_v119
from test_tools import ROOT, package


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


class DefaultDenyReleaseIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(
            (ROOT/'docs/evidence/v1.19.0/continuity.json').read_text(encoding='utf-8'))

    def test_reviewed_current_and_exact_v118_bytes(self):
        self.assertEqual(self.ledger['baseline_commit'],
                         'dde8834c25046b0b73238f5f829500bfe8b40581')
        self.assertEqual(self.ledger['candidate_version'], '1.19.0')
        predecessor = json.loads(
            (ROOT/'docs/evidence/v1.18.0/continuity.json').read_text(encoding='utf-8'))
        previous_hashes = {row['path']: row['current_sha256']
                           for row in predecessor['files']}
        for row in self.ledger['files']:
            with self.subTest(path=row['path']):
                current = runtime_v119(ROOT, row['path'])
                prior = runtime_v118(ROOT, row['path'])
                self.assertEqual(digest(current), row['current_sha256'])
                self.assertEqual(digest(prior), row['prior_sha256'])
                self.assertEqual(row['prior_sha256'], previous_hashes[row['path']])
                self.assertEqual(len(current), row['current_bytes'])
                self.assertEqual(len(prior), row['prior_bytes'])

    def test_portable_inventory_is_continuous(self):
        current = {p.relative_to(ROOT).as_posix() for p in package.source_files(ROOT)
                   if p.is_relative_to(ROOT/'skills/ui-spec')}
        declared = [row['path'] for row in self.ledger['files']]
        predecessor = json.loads(
            (ROOT/'docs/evidence/v1.18.0/continuity.json').read_text(encoding='utf-8'))
        self.assertEqual(len(declared), len(set(declared)))
        self.assertEqual(current, set(declared))
        self.assertEqual(set(declared), {row['path'] for row in predecessor['files']})

    def test_installed_helpers_and_json_assets_are_identical_to_v118(self):
        for row in self.ledger['files']:
            path = row['path']
            if '/scripts/' in path or path.endswith('.json'):
                with self.subTest(path=path):
                    self.assertEqual((ROOT/path).read_bytes(), runtime_v118(ROOT, path))
                    self.assertEqual(row['disposition'], 'unchanged')
                    self.assertEqual(row['inverse_edits'], [])

    def test_preexisting_evidence_remains_byte_identical(self):
        rows = self.ledger['historical_evidence_unchanged']
        self.assertEqual(len(rows), len({row['path'] for row in rows}))
        self.assertIn('docs/evidence/v1.18.0/continuity.json',
                      {row['path'] for row in rows})
        self.assertIn('docs/experiments/observable-execution/registration.json',
                      {row['path'] for row in rows})
        for row in rows:
            with self.subTest(path=row['path']):
                self.assertEqual(digest((ROOT/row['path']).read_bytes()), row['sha256'])


class DefaultDenyRecoveryMechanicsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = 'skills/ui-spec/SKILL.md'
        self.current = b'intro\nalpha\nbeta revised\ngamma\noutro\n'
        self.prior = b'alpha\nbeta\ngamma\n'
        self.target = self.root/self.path
        self.target.parent.mkdir(parents=True)
        self.target.write_bytes(self.current)
        self.ledger_path = self.root/'docs/evidence/v1.19.0/continuity.json'
        self.ledger_path.parent.mkdir(parents=True)
        self.ledger = {'files': [{
            'path': self.path,
            'current_sha256': digest(self.current),
            'prior_sha256': digest(self.prior),
            'inverse_edits': [
                {'current_start_line': 0, 'current_end_line': 1,
                 'current_fragment_sha256': digest(b'intro\n'), 'prior_text': ''},
                {'current_start_line': 2, 'current_end_line': 3,
                 'current_fragment_sha256': digest(b'beta revised\n'), 'prior_text': 'beta\n'},
                {'current_start_line': 4, 'current_end_line': 5,
                 'current_fragment_sha256': digest(b'outro\n'), 'prior_text': ''}]}]}

    def write_ledger(self, data=None):
        self.ledger_path.write_text(json.dumps(data or self.ledger), encoding='utf-8')

    def test_multiple_inverse_edits_restore_exact_bytes_without_writes(self):
        self.write_ledger()
        before = {p.relative_to(self.root): p.read_bytes()
                  for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(runtime_v118(self.root, self.path), self.prior)
        after = {p.relative_to(self.root): p.read_bytes()
                 for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_current_mutation_is_rejected(self):
        self.write_ledger()
        self.target.write_bytes(self.current+b'Unreviewed change\n')
        with self.assertRaises(ValueError):
            runtime_v118(self.root, self.path)

    def test_corrupted_inverse_or_predecessor_is_rejected(self):
        for key, value in [('current_fragment_sha256', '0'*64),
                           ('prior_text', 'Different predecessor\n')]:
            with self.subTest(field=key):
                data = copy.deepcopy(self.ledger)
                data['files'][0]['inverse_edits'][1][key] = value
                self.write_ledger(data)
                with self.assertRaises(ValueError):
                    runtime_v118(self.root, self.path)

    def test_missing_and_duplicate_identities_are_rejected(self):
        for rows in ([], self.ledger['files']*2):
            with self.subTest(records=len(rows)):
                self.write_ledger({'files': rows})
                with self.assertRaises(ValueError):
                    runtime_v118(self.root, self.path)


class DefaultDenyStudyIdentityTests(unittest.TestCase):
    """Keep published execution inputs and outputs reproducible, not quality-scored."""

    @classmethod
    def setUpClass(cls):
        cls.study = ROOT/'docs/experiments/default-deny'
        cls.registration = json.loads((cls.study/'registration.json').read_text())

    def test_registered_inputs_and_paired_task_bytes_are_preserved(self):
        self.assertEqual(digest((self.study/'registration.json').read_bytes()),
                         'f021e5540000cb2f29324143475d5d0989751b3aeb6cd83b9405dab16cb8a013')
        manifest_path = self.study/'inputs/manifest.json'
        self.assertEqual(digest(manifest_path.read_bytes()),
                         self.registration['input_manifest_sha256'])
        manifest = json.loads(manifest_path.read_text())
        for row in manifest['inputs']:
            content = (manifest_path.parent/row['path']).read_bytes()
            self.assertEqual(digest(content), row['sha256'])
            self.assertEqual(len(content), row['bytes'])
        for task in ('T1', 'T2', 'T3'):
            rows = [r for r in self.registration['cells'] if r['task'] == task]
            self.assertEqual({r['condition'] for r in rows}, {'A', 'B'})
            self.assertEqual(len(rows), 2)
            for key in ('task_sha256', 'initial_app', 'starter_archive'):
                self.assertEqual(rows[0][key], rows[1][key])
            boundaries = []
            for row in rows:
                content = (self.study/'runs'/row['cell']/'RUN.md').read_bytes()
                self.assertEqual(digest(content), row['run_md_sha256'])
                boundaries.append(content.decode().replace(
                    'Use localhost port '+str(row['port'])+'.',
                    'Use localhost port PORT.'))
            self.assertEqual(boundaries[0], boundaries[1])
            self.assertEqual(digest((self.study/(task+'.md')).read_bytes()),
                             rows[0]['task_sha256'])
            with zipfile.ZipFile(self.study/rows[0]['starter_archive']) as archive:
                self.assertEqual(digest(archive.read('TASK.md')), rows[0]['task_sha256'])
                for path, sha in rows[0]['initial_app'].items():
                    self.assertEqual(digest(archive.read('app/'+path)), sha)

    def test_tested_methods_and_declared_release_delta_are_exact(self):
        delta = json.loads((self.study/'final-runtime-delta.json').read_text())
        changes = {r['path']: r for r in delta['changes']}
        self.assertEqual(set(changes), {'references/examples.md'})
        for condition, row in self.registration['conditions'].items():
            path = self.study/row['archive']
            self.assertEqual(digest(path.read_bytes()), row['sha256'])
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(set(archive.namelist()),
                                 {'ui-spec/'+p for p in row['files']})
                for relative, sha in row['files'].items():
                    content = archive.read('ui-spec/'+relative)
                    self.assertEqual(digest(content), sha)
                    repo_path = 'skills/ui-spec/'+relative
                    if condition == 'A':
                        expected = runtime_v118(ROOT, repo_path)
                    elif relative in changes:
                        change = changes[relative]
                        expected = change['tested_text'].encode()
                        current = runtime_v119(ROOT, repo_path)
                        self.assertEqual(current, change['release_text'].encode())
                        self.assertEqual(digest(expected), change['tested_sha256'])
                        self.assertEqual(digest(current), change['release_sha256'])
                        self.assertNotEqual(expected, current)
                    else:
                        expected = runtime_v119(ROOT, repo_path)
                    self.assertEqual(content, expected)
        release_path = self.study/delta['released_archive']
        self.assertEqual(digest(release_path.read_bytes()), delta['released_archive_sha256'])
        self.assertEqual(set(delta['released_files']),
                         set(self.registration['conditions']['B']['files']))
        with zipfile.ZipFile(release_path) as archive:
            self.assertEqual(set(archive.namelist()),
                             {'ui-spec/'+p for p in delta['released_files']})
            for relative, sha in delta['released_files'].items():
                content = archive.read('ui-spec/'+relative)
                self.assertEqual(digest(content), sha)
                self.assertEqual(content, runtime_v119(ROOT, 'skills/ui-spec/'+relative))

    def test_all_frozen_outputs_are_intact_and_in_source_distribution(self):
        distributed = set(package.source_files(ROOT))
        for cell in self.registration['cells']:
            directory = self.study/'runs'/cell['cell']
            index_path = directory/'archive-index.json'
            self.assertIn(index_path, distributed)
            index = json.loads(index_path.read_text())
            self.assertEqual(index['condition'], cell['condition'])
            self.assertEqual(index['task_sha256'], cell['task_sha256'])
            for key, filename in [('application', 'application.zip'),
                                  ('participant_evidence', 'participant-evidence.zip')]:
                path = directory/filename
                self.assertIn(path, distributed)
                row = index[key]
                content = path.read_bytes()
                self.assertEqual(digest(content), row['sha256'])
                self.assertEqual(len(content), row['bytes'])
                with zipfile.ZipFile(path) as archive:
                    self.assertEqual(set(archive.namelist()), set(row['files']))
                    for relative, record in row['files'].items():
                        data = archive.read(relative)
                        self.assertEqual(digest(data), record['sha256'])
                        self.assertEqual(len(data), record['bytes'])
        mapping = json.loads((self.study/'review-mapping.json').read_text())
        self.assertEqual(set(mapping), {'T1', 'T2', 'T3'})
        for task, pairs in mapping.items():
            self.assertEqual({r['cell'] for r in pairs},
                             {r['cell'] for r in self.registration['cells']
                              if r['task'] == task})
            directory = self.study/'reviews'/task
            index = json.loads((directory/'archive-index.json').read_text())
            path = directory/'review-evidence.zip'
            self.assertIn(path, distributed)
            self.assertEqual(digest(path.read_bytes()), index['evidence_sha256'])
            report = (directory/'review.zh-CN.md').read_bytes()
            self.assertEqual(digest(report), index['report_sha256'])
            self.assertEqual((directory/'REQUIREMENTS.md').read_bytes(),
                             (self.study/(task+'.md')).read_bytes())
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(set(archive.namelist()), set(index['files']))
                self.assertEqual(archive.read(index['report_file_in_archive']), report)
                for relative, record in index['files'].items():
                    data = archive.read(relative)
                    self.assertEqual(digest(data), record['sha256'])
                    self.assertEqual(len(data), record['bytes'])
                for relative in (index.get('published_link_targets', [])+
                                 index.get('published_gallery_files', [])):
                    self.assertEqual((directory/relative).read_bytes(), archive.read(relative))
        followup = self.study/'followup'
        registration = json.loads((followup/'registration.json').read_text())
        delta = json.loads((self.study/'final-runtime-delta.json').read_text())
        self.assertEqual(registration['runtime_sha256'], delta['released_archive_sha256'])
        self.assertEqual(digest((followup/'TASK.md').read_bytes()), registration['task_sha256'])
        self.assertEqual(digest((followup/'RUN.md').read_bytes()),
                         registration['working_boundary_sha256'])
        directory = followup/'outputs'
        index = json.loads((directory/'archive-index.json').read_text())
        self.assertEqual(index['runtime_archive_sha256'], registration['runtime_sha256'])
        self.assertEqual(index['task_sha256'], registration['task_sha256'])
        for key, filename in [('application', 'application.zip'),
                              ('participant_evidence', 'participant-evidence.zip')]:
            path = directory/filename
            self.assertIn(path, distributed)
            self.assertEqual(digest(path.read_bytes()), index[key]['sha256'])
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(set(archive.namelist()), set(index[key]['files']))
                for relative, record in index[key]['files'].items():
                    data = archive.read(relative)
                    self.assertEqual(digest(data), record['sha256'])
                    self.assertEqual(len(data), record['bytes'])


if __name__ == '__main__':
    unittest.main()
