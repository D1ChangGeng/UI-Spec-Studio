"""Source and discovery regression checks, not design-quality or model experiments."""
from __future__ import annotations

import ast
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

from test_tools import ROOT, load, package
from source_continuity import predecessor_runtime, runtime_v116

lookup = load('visual_craft_lookup', 'skills/ui-spec/scripts/find_resources.py')


class VisualCraftReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads((ROOT / 'docs/evidence/v1.16.0/continuity.json').read_text(encoding='utf-8'))
        cls.catalog = lookup.load_catalog()
        cls.prior_catalog = json.loads(predecessor_runtime(ROOT, 'skills/ui-spec/assets/resource-catalog.json'))

    def test_prior_runtime_identity_and_all_files_preserved(self):
        self.assertEqual(self.ledger['baseline_commit'], 'a89091dfa5754f98b79655c684f978f24fd92716')
        self.assertEqual(self.ledger['baseline_tree'], '03e3c14508244551a18711aff28363452871e2ed')
        rows = self.ledger['files']
        paths = {row['path'] for row in rows}
        actual = {p.relative_to(ROOT).as_posix() for p in package.source_files(ROOT)
                  if p.is_relative_to(ROOT / 'skills/ui-spec')}
        # This is this release's historical identity, not a limit on future scope.
        self.assertEqual(len(rows), 37)
        self.assertEqual(paths, actual)
        self.assertEqual(len(paths), len(rows))
        for row in rows:
            current = runtime_v116(ROOT, row['path'])
            prior = predecessor_runtime(ROOT, row['path'])
            self.assertEqual(hashlib.sha256(current).hexdigest(), row['current_sha256'])
            self.assertEqual(hashlib.sha256(prior).hexdigest(), row['prior_sha256'])
            self.assertEqual(len(prior), row['prior_bytes'])
            self.assertEqual(len(current), row['current_bytes'])
            if row['disposition'] == 'append-only':
                self.assertTrue(current.startswith(prior), row['path'])
            elif row['disposition'] == 'unchanged':
                self.assertEqual(current, prior, row['path'])
            else:
                self.assertTrue(row['reason'])

    def test_structural_helpers_and_optional_schema_unchanged(self):
        paths = [row['path'] for row in self.ledger['files']
                 if '/scripts/' in row['path']]
        paths += ['skills/ui-spec/assets/design-coverage-categories.json',
                  'skills/ui-spec/assets/templates/design-evidence.json',
                  'skills/ui-spec/assets/templates/manifest.json']
        for path in paths:
            self.assertEqual(runtime_v116(ROOT, path), predecessor_runtime(ROOT, path), path)

    def test_old_evidence_keeps_its_own_identity(self):
        for row in self.ledger['historical_evidence_unchanged']:
            self.assertEqual(hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest(), row['sha256'])
        self.assertEqual(len(self.ledger['historical_evidence_unchanged']), 100)

    def test_changed_current_bytes_are_not_certified_as_historical(self):
        path = 'skills/ui-spec/SKILL.md'
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / path
            target.parent.mkdir(parents=True)
            target.write_bytes(runtime_v116(ROOT, path) + b'\nChanged after review\n')
            ledger = root / 'docs/evidence/v1.16.0/continuity.json'
            ledger.parent.mkdir(parents=True)
            ledger.write_text(json.dumps(self.ledger), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Current source differs'):
                predecessor_runtime(root, path)

    def test_inverse_edit_requires_its_own_fragment_identity(self):
        data = copy.deepcopy(self.ledger)
        path = 'skills/ui-spec/SKILL.md'
        row = next(item for item in data['files'] if item['path'] == path)
        row['inverse_edits'][0]['current_fragment_sha256'] = '0' * 64
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / path
            target.parent.mkdir(parents=True)
            target.write_bytes(runtime_v116(ROOT, path))
            ledger = root / 'docs/evidence/v1.16.0/continuity.json'
            ledger.parent.mkdir(parents=True)
            ledger.write_text(json.dumps(data), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Inverse fragment differs'):
                predecessor_runtime(root, path)

    def test_unknown_predecessor_is_not_silently_substituted(self):
        with self.assertRaisesRegex(ValueError, 'Unknown or duplicate'):
            predecessor_runtime(ROOT, 'skills/ui-spec/not-a-historical-file.md')

    def test_old_catalog_entries_dates_and_source_claims_survive(self):
        current = {r['id']: r for r in self.catalog['resources']}
        prior = {r['id']: r for r in self.prior_catalog['resources']}
        self.assertEqual(set(current), set(prior))
        self.assertEqual(len(current), 37)
        for ident, row in prior.items():
            for key, value in row.items():
                if key in {'aliases', 'forms'}:
                    self.assertTrue(set(value) <= set(current[ident][key]), (ident, key))
                else:
                    self.assertEqual(value, current[ident][key], (ident, key))
        self.assertEqual(self.catalog['snapshot_date'], self.prior_catalog['snapshot_date'])
        for row in self.prior_catalog['release_spot_checks']:
            self.assertIn(row, self.catalog['release_spot_checks'])

    def test_profiles_are_documentary_not_quality_scores(self):
        profiles = [r['craft_profile'] for r in self.catalog['resources'] if 'craft_profile' in r]
        self.assertEqual(len(profiles), 15)
        for profile in profiles:
            for key in ('roles', 'reuse_scopes', 'visual_forms', 'sources'):
                self.assertIsInstance(profile[key], list)
                self.assertTrue(profile[key])
            self.assertIn('Not rated', profile['quality_status'])
            self.assertIn('not a visual audit', profile['basis'])
            self.assertFalse({'score', 'rank', 'priority', 'approved', 'next_action'} & set(profile))
        self.assertEqual(self.catalog['craft_discovery']['version'], 'visual-craft-discovery/1')

    def test_visual_form_query_keeps_stack_and_alphabetic_order(self):
        rows = lookup.select(self.catalog, form='visual-component', stack='vue', limit=100)
        self.assertEqual({r['id'] for r in rows}, {'vue-bits', 'inspira'})
        self.assertEqual([r['name'].casefold() for r in rows], sorted(r['name'].casefold() for r in rows))
        self.assertTrue(all('craft_profile' in r for r in rows))
        self.assertEqual(lookup.select(self.catalog, 'absent-visual-source-xyz'), [])

    def test_finesse_skill_is_not_the_finesse_ui_catalog_item(self):
        item = next(r for r in self.catalog['resources'] if r['id'] == 'finesse')
        self.assertIn('finesseui.com', ' '.join(item['sources']))
        self.assertIn('not mouse-lin/finesse-skill', item['craft_profile']['identity_boundary'])
        doc = (ROOT / 'docs/FINESSE-ADAPTATION.md').read_text(encoding='utf-8')
        self.assertIn('c7a91448baf6e98fecf542915cdb7e3155bddc45', doc)
        self.assertIn('Lines 1–125', doc)
        self.assertIn('MIT + Commons Clause', doc)

    def test_source_selection_explains_distinct_professional_objects(self):
        text = (ROOT / 'skills/ui-spec/references/component-sourcing.md').read_text(encoding='utf-8')
        for fragment in ('Reuse Scope', 'Visual Completeness', 'Functional Foundation',
                         'Visual Implementation', 'Integrated Perceptual Quality',
                         'Reuse the visual craft, not merely the underlying functionality'):
            self.assertIn(fragment, text)

    def test_complete_methods_stay_in_installed_references(self):
        expected = {
            'principles.md': ['glyph', 'material', 'composition'],
            'interaction-and-variants.md': ['ownership', 'velocity', 'mature'],
            'visual-assets.md': ['photograph', 'source', 'composition'],
            'patterns.md': ['reading', 'mature', 'motion'],
            'verification.md': ['trial', 'integrated', 'retained'],
            'evidence-map.md': ['source', 'structural', 'quality'],
            'content-design.md': ['user', 'visible', 'technical'],
        }
        for name, terms in expected.items():
            current = (ROOT / 'skills/ui-spec/references' / name).read_text(encoding='utf-8').lower()
            for term in terms:
                self.assertIn(term, current, name)

    def test_no_new_upstream_showcase_or_font_in_installed_bundle(self):
        previous = {row['path'].removeprefix('skills/ui-spec/') for row in self.ledger['files']}
        with tempfile.TemporaryDirectory() as td:
            artifacts = package.build(ROOT, Path(td))
            with zipfile.ZipFile(artifacts[1]) as z:
                names = set(z.namelist())
                self.assertEqual(names, {'ui-spec/' + p for p in previous})
                self.assertFalse(any(p.lower().endswith(('.woff', '.woff2', '.ttf', '.otf')) for p in names))
                for p in ('references/component-sourcing.md', 'references/principles.md',
                          'references/interaction-and-variants.md', 'references/verification.md'):
                    self.assertEqual(z.read('ui-spec/' + p), (ROOT / 'skills/ui-spec' / p).read_bytes())

    def test_current_methods_do_not_claim_experiments_were_run(self):
        record = json.loads((ROOT / 'docs/evidence/v1.16.0/experiment-status.json').read_text(encoding='utf-8'))
        self.assertEqual(record['independent_agent_runs'], 0)
        self.assertEqual(record['status'], 'not_executed')
        self.assertEqual(len(record['task_families']), 3)
        self.assertIn('separate', record['maintainer_application_scope'])

    def test_new_historical_reader_uses_explicit_utf8(self):
        tree = ast.parse((ROOT / 'tests/source_continuity.py').read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'read_text':
                self.assertTrue(any(k.arg == 'encoding' and isinstance(k.value, ast.Constant)
                                    and k.value.value == 'utf-8' for k in node.keywords))


if __name__ == '__main__':
    unittest.main()
