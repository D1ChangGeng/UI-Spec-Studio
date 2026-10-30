"""Release identity and historical recovery; no assessment of design or disclosure quality."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from source_continuity import runtime_v117
from test_tools import ROOT, package


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


class ObservableReleaseContinuityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads(
            (ROOT/'docs/evidence/v1.18.0/continuity.json').read_text(encoding='utf-8'))

    def test_current_runtime_and_exact_v117_identity(self):
        self.assertEqual(self.ledger['baseline_commit'],
                         '91e993b44deed4be07fc3d69e22e8142a17eccc0')
        for row in self.ledger['files']:
            with self.subTest(path=row['path']):
                current = (ROOT/row['path']).read_bytes()
                prior = runtime_v117(ROOT, row['path'])
                self.assertEqual(digest(current), row['current_sha256'])
                self.assertEqual(digest(prior), row['prior_sha256'])

    def test_runtime_inventory_retains_the_existing_portable_files(self):
        current = {p.relative_to(ROOT).as_posix() for p in package.source_files(ROOT)
                   if p.is_relative_to(ROOT/'skills/ui-spec')}
        declared = [row['path'] for row in self.ledger['files']]
        self.assertEqual(len(declared), len(set(declared)))
        self.assertEqual(current, set(declared))
        predecessor = json.loads(
            (ROOT/'docs/evidence/v1.17.0/continuity.json').read_text(encoding='utf-8'))
        self.assertEqual(set(declared), {row['path'] for row in predecessor['files']})

    def test_installed_helpers_and_json_assets_are_unchanged(self):
        for row in self.ledger['files']:
            path = row['path']
            if '/scripts/' in path or path.endswith('.json'):
                with self.subTest(path=path):
                    self.assertEqual((ROOT/path).read_bytes(), runtime_v117(ROOT, path))

    def test_historical_evidence_remains_byte_identical(self):
        for row in self.ledger['historical_evidence_unchanged']:
            with self.subTest(path=row['path']):
                self.assertEqual(digest((ROOT/row['path']).read_bytes()), row['sha256'])


class ObservableRecoveryMechanicsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = 'skills/ui-spec/SKILL.md'
        self.current = b'intro\nalpha\nbeta revised\ngamma\noutro\n'
        self.prior = b'alpha\nbeta\ngamma\n'
        target = self.root/self.path
        target.parent.mkdir(parents=True)
        target.write_bytes(self.current)
        self.ledger_path = self.root/'docs/evidence/v1.18.0/continuity.json'
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

    def test_multiple_reverse_edits_restore_exact_bytes_without_writes(self):
        self.write_ledger()
        before = {p.relative_to(self.root): p.read_bytes()
                  for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(runtime_v117(self.root, self.path), self.prior)
        after = {p.relative_to(self.root): p.read_bytes()
                 for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_changed_current_source_is_rejected(self):
        self.write_ledger()
        (self.root/self.path).write_bytes(self.current+b'Unreviewed change\n')
        with self.assertRaises(ValueError):
            runtime_v117(self.root, self.path)

    def test_corrupted_inverse_or_reconstructed_source_is_rejected(self):
        for key, value in [('current_fragment_sha256', '0'*64),
                           ('prior_text', 'Different predecessor\n')]:
            with self.subTest(field=key):
                data = copy.deepcopy(self.ledger)
                data['files'][0]['inverse_edits'][1][key] = value
                self.write_ledger(data)
                with self.assertRaises(ValueError):
                    runtime_v117(self.root, self.path)

    def test_unknown_or_duplicate_identity_is_rejected(self):
        for rows in ([], self.ledger['files']*2):
            with self.subTest(records=len(rows)):
                self.write_ledger({'files': rows})
                with self.assertRaises(ValueError):
                    runtime_v117(self.root, self.path)


if __name__ == '__main__':
    unittest.main()
