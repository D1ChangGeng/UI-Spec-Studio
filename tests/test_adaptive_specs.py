"""Literal increment records and historical identity; never visual-quality ratings."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from test_design_evidence import checker, sample, ROOT
from source_continuity import runtime_v1161
from test_tools import load, package

preparer = load('adaptive_experiment_preparer', 'tools/prepare_granularity_experiment.py')
replay = load('adaptive_experiment_replay', 'tools/replay_granularity_run.py')


class AdaptiveSpecRecordsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'evidence.txt').write_text('Synthetic declaration fixture', encoding='utf-8')
        self.data = sample()
        self.data['product_context'] = {'overall_goal': 'A readable research workspace',
                                        'current_ui': 'The same existing application'}
        self.data['candidate_specs'] = [{'id': 'C2', 'purpose': 'Explore sources', 'objects': ['panel']}]
        self.data['formal_specs'] = [
            {'id': 'S1', 'purpose': 'Improve input and reading continuity',
             'objects': ['goal', 'panel', 'font'], 'research_objects': ['goal', 'panel'],
             'implementation_objects': ['panel'], 'regression_objects': ['font', 'panel'],
             'decisions': ['D1'], 'related_specs': ['C2']},
            {'id': 'S2', 'purpose': 'Shared typography', 'objects': ['panel', 'font'],
             'implementation_objects': ['font'], 'related_specs': ['S1']}]

    def inspect(self):
        return checker.inspect_record(self.data, self.root)

    def test_shared_objects_and_different_scope_extents_are_declarations(self):
        result = self.inspect()
        self.assertEqual(result['structural_findings'], [])
        self.assertEqual(result['declared_spec_records']['scope_judgment'], 'not_assessed')
        self.assertEqual(len(result['declared_spec_records']['formal_specs']), 2)
        self.assertEqual(len(result['declared_spec_records']['candidate_specs']), 1)

    def test_same_records_in_three_views_without_mutation(self):
        before = copy.deepcopy(self.data)
        for view in ('overview', 'detail', 'execution'):
            result = checker.project_view(self.data, view)
            for key in ('product_context', 'candidate_specs', 'formal_specs'):
                self.assertEqual(result[key], self.data[key])
            result['formal_specs'][0]['purpose'] = 'Changed only in the projection'
        self.assertEqual(before, self.data)

    def test_legacy_records_need_no_spec_fields(self):
        for key in ('product_context', 'candidate_specs', 'formal_specs'):
            del self.data[key]
        result = self.inspect()
        self.assertEqual(result['structural_findings'], [])
        self.assertFalse(any('specs' in x['path'] for x in result['field_observations']))

    def test_partial_spec_does_not_generate_quality_or_scope_decision(self):
        self.data['formal_specs'] = [{'id': 'S1'}]
        result = self.inspect()
        self.assertEqual(result['structural_findings'], [])
        for key in ('ok', 'satisfied', 'complete', 'score', 'split', 'merge', 'next_action'):
            self.assertNotIn(key, result)
            self.assertNotIn(key, result['declared_spec_records'])

    def test_unknown_references_are_literal_findings(self):
        self.data['formal_specs'][0].update(decisions=['missing-decision'],
            regression_objects=['missing-object'], related_specs=['missing-spec'])
        unresolved = [x for x in self.inspect()['reference_observations'] if x['resolution'] == 'unresolved']
        self.assertEqual({x['id'] for x in unresolved}, {'missing-decision', 'missing-object', 'missing-spec'})

    def test_duplicate_between_candidate_and_formal_remains_ambiguous(self):
        self.data['candidate_specs'].append({'id': 'S1'})
        result = self.inspect()
        self.assertIn('duplicate_id', {x['code'] for x in result['structural_findings']})
        self.assertIn('ambiguous_reference', {x['code'] for x in result['structural_findings']})

    def test_duplicate_within_one_list_remains_ambiguous(self):
        self.data['formal_specs'].append({'id': 'S1'})
        self.assertIn('ambiguous_reference', {x['code'] for x in self.inspect()['structural_findings']})

    def test_arbitrary_relationship_is_not_a_lifecycle(self):
        self.data['formal_specs'][0].update(relationship='Revisit the previous decision', related_specs=['S2'])
        self.assertEqual(self.inspect()['structural_findings'], [])

    def test_malformed_declarations_do_not_crash(self):
        for value in (None, 42, 'S1', {}, [None, {'id': []}]):
            with self.subTest(value=value):
                self.data['formal_specs'] = value
                self.assertEqual(self.inspect()['record_readability'], 'readable')

    def test_cli_findings_exit_zero_and_preserve_files(self):
        self.data['formal_specs'][0]['objects'].append('absent')
        path = self.root / 'record.json'
        path.write_text(json.dumps(self.data), encoding='utf-8')
        before = path.read_bytes()
        run = subprocess.run([sys.executable, str(ROOT/'skills/ui-spec/scripts/check_design_evidence.py'),
                              '--project-root', str(self.root), '--record', path.name],
                             capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue(json.loads(run.stdout)['structural_findings'])
        self.assertEqual(before, path.read_bytes())


class AdaptiveSpecContinuityTests(unittest.TestCase):
    def test_exact_current_and_predecessor_identities(self):
        ledger = json.loads((ROOT/'docs/evidence/v1.17.0/continuity.json').read_text(encoding='utf-8'))
        self.assertEqual(ledger['baseline_commit'], '9cc2470e21b626c56dd293274277d9809c13defb')
        for row in ledger['files']:
            self.assertEqual(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest(), row['current_sha256'])
            self.assertEqual(hashlib.sha256(runtime_v1161(ROOT, row['path'])).hexdigest(), row['prior_sha256'])
        for row in ledger['historical_evidence_unchanged']:
            self.assertEqual(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest(), row['sha256'])

    def test_changed_identity_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = 'skills/ui-spec/SKILL.md'
            target = root/path
            target.parent.mkdir(parents=True)
            target.write_bytes((ROOT/path).read_bytes() + b'\nUnreviewed change\n')
            ledger = root/'docs/evidence/v1.17.0/continuity.json'
            ledger.parent.mkdir(parents=True)
            ledger.write_bytes((ROOT/'docs/evidence/v1.17.0/continuity.json').read_bytes())
            with self.assertRaises(ValueError):
                runtime_v1161(root, path)


class ExperimentInputTests(unittest.TestCase):
    def baseline(self, parent):
        root = parent/'baseline'
        ledger = json.loads((ROOT/'docs/experiments/adaptive-granularity/baseline-identity.json').read_text(encoding='utf-8'))
        for name in ledger['files']:
            target = root/name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(runtime_v1161(ROOT, 'skills/ui-spec/'+name))
        return root

    def test_matched_inputs_and_hidden_continuations(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            baseline = self.baseline(parent)
            output = parent/'cells'
            result = preparer.build(baseline, output)
            self.assertEqual(result['participant_runs_executed'], 0)
            self.assertEqual(len(result['cells']), 9)
            for task in ('T1', 'T2', 'T3'):
                prompts = [(output/f'{task}-{code}'/'TASK.md').read_bytes()
                           for code in preparer.ARM_CODES.values()]
                self.assertTrue(all(p == prompts[0] for p in prompts))
                for code in preparer.ARM_CODES.values():
                    self.assertFalse((output/f'{task}-{code}'/'continuation.md').exists())
                    self.assertTrue((output/'continuations'/f'{task}-{code}'/'TASK.md').is_file())
            a, b = result['arms']['A'], result['arms']['B']
            self.assertEqual({p for p in a if a[p] != b[p]}, {'SKILL.md'})
            self.assertEqual(set(b)-set(a), {'references/scope-judgment.md'})
            marker = output/'preserve.txt'
            marker.write_text('Keep this completed work', encoding='utf-8')
            with self.assertRaises(ValueError):
                preparer.build(baseline, output)
            self.assertEqual(marker.read_text(encoding='utf-8'), 'Keep this completed work')

    def test_baseline_mutation_rejected_before_creating_cells(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            baseline = self.baseline(parent)
            entry = baseline/'SKILL.md'
            entry.write_bytes(entry.read_bytes()+b'\nChanged condition\n')
            with self.assertRaises(ValueError):
                preparer.build(baseline, parent/'cells')
            self.assertFalse((parent/'cells').exists())

    def test_study_replay_assets_are_included_only_at_evidence_locations(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            included, excluded = set(), set()
            for suffix in ('.woff2', '.webm', '.csv', '.jsonl', '.mjs', '.log', '.zip', '.jpg', '.jpeg'):
                for folder, names in [('docs/experiments/run', included),
                                      ('docs/evidence/run', included),
                                      ('skills/ui-spec/assets', excluded)]:
                    path = root/folder/f'fixture{suffix}'
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(b'synthetic byte-identity fixture')
                    names.add(path)
            actual = set(package.source_files(root))
            self.assertTrue(included <= actual)
            self.assertFalse(excluded & actual)

    def test_published_study_snapshots_retain_exact_inputs_and_outputs(self):
        study = ROOT/'docs/experiments/adaptive-granularity'
        registration = json.loads((study/'registration.json').read_text(encoding='utf-8'))
        included = set(package.source_files(ROOT))
        for cell in registration['cells']:
            directory = study/'runs'/cell['cell']
            index = json.loads((directory/'archive-index.json').read_text(encoding='utf-8'))
            self.assertEqual(set(index['snapshots']), {'initial', 'final'})
            cache = {}
            for stage, snapshot in index['snapshots'].items():
                self.assertEqual(snapshot['files']['TASK.md']['sha256'], cell['initial_sha256'])
                if stage == 'final':
                    self.assertEqual(snapshot['files']['CONTINUE.md']['sha256'], cell['continuation_sha256'])
                else:
                    self.assertNotIn('CONTINUE.md', snapshot['files'])
                for original, item in snapshot['files'].items():
                    replay.relative_name(original)
                    stored = directory/replay.relative_name(item['path'])
                    self.assertIn(stored, included, f'Release would omit {stored}')
                    key = (stored, item.get('member'))
                    if key not in cache:
                        if 'member' in item:
                            with zipfile.ZipFile(stored) as bundle:
                                content = bundle.read(replay.relative_name(item['member']).as_posix())
                        else:
                            content = stored.read_bytes()
                        cache[key] = hashlib.sha256(content).hexdigest()
                    self.assertEqual(cache[key], item['sha256'], original)
            for bundle in index['capture_bundles']:
                self.assertEqual(hashlib.sha256((directory/bundle['path']).read_bytes()).hexdigest(),
                                 bundle['sha256'])


class ExperimentReplayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.archive = self.root/'archive'
        self.archive.mkdir()
        self.app = b'<!doctype html><title>Exact archived fixture</title>'
        self.frame = b'synthetic capture-byte fixture'
        (self.archive/'index.html').write_bytes(self.app)
        with zipfile.ZipFile(self.archive/'captures.zip', 'w') as bundle:
            bundle.writestr('final/evidence/frame.png', self.frame)
        self.index = {'cell': 'synthetic', 'snapshots': {'final': {'files': {
            'app/index.html': {'path': 'index.html', 'sha256': hashlib.sha256(self.app).hexdigest()},
            'evidence/frame.png': {'path': 'captures.zip', 'member': 'final/evidence/frame.png',
                                   'sha256': hashlib.sha256(self.frame).hexdigest()}}}}}

    def write_index(self):
        (self.archive/'archive-index.json').write_text(json.dumps(self.index), encoding='utf-8')

    def test_exact_loose_and_bundled_bytes_are_restored(self):
        self.write_index()
        out = self.root/'restored'
        result = replay.restore(self.archive, out)
        self.assertEqual(result['files'], 2)
        self.assertEqual((out/'app/index.html').read_bytes(), self.app)
        self.assertEqual((out/'evidence/frame.png').read_bytes(), self.frame)

    def test_changed_bytes_fail_before_output_creation(self):
        self.write_index()
        (self.archive/'index.html').write_bytes(b'Changed')
        out = self.root/'restored'
        with self.assertRaises(ValueError):
            replay.restore(self.archive, out)
        self.assertFalse(out.exists())

    def test_unsafe_paths_are_rejected(self):
        for name in ('../outside', '/outside', 'a/../outside', 'a\\outside', 'C:/outside', '.', 'a//b'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                replay.relative_name(name)

    def test_existing_work_is_not_overwritten(self):
        self.write_index()
        out = self.root/'restored'
        out.mkdir()
        (out/'keep.txt').write_text('Keep', encoding='utf-8')
        with self.assertRaises(ValueError):
            replay.restore(self.archive, out)
        self.assertEqual((out/'keep.txt').read_text(encoding='utf-8'), 'Keep')


if __name__ == '__main__':
    unittest.main()
