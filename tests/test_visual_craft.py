"""Catalogue and source-continuity checks; not aesthetic or Agent-behavior tests."""
from __future__ import annotations
import base64
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zlib
from test_tools import ROOT, load, package

lookup=load('craft_lookup', ROOT/'skills/ui-spec/scripts/find_resources.py')

class VisualCraftTests(unittest.TestCase):
    def setUp(self):
        self.data=lookup.load_catalog()

    def test_visual_role_and_scope_match_literal_labels(self):
        rows=lookup.select(self.data,role='visual-implementation',reuse_scope='functional-block',limit=100)
        self.assertTrue(rows)
        self.assertTrue(all('functional-block' in r['discovery_profile']['reuse_scopes'] for r in rows))
        self.assertTrue(all('visual-implementation' in r['discovery_profile']['roles'] for r in rows))

    def test_visual_role_vue_retains_named_source_identity(self):
        ids={r['id'] for r in lookup.select(self.data,role='visual-implementation',stack='vue',limit=100)}
        self.assertTrue({'vue-bits','inspira'} <= ids)
        self.assertNotIn('react-bits',ids)

    def test_functional_role_is_not_visual_certificate(self):
        rows=lookup.select(self.data,role='functional-foundation',stack='react',limit=100)
        self.assertTrue(any(r['id']=='radix-primitives' for r in rows))
        self.assertFalse(any(r['id']=='react-bits' for r in rows))

    def test_facet_search_is_literal_and_alphabetical(self):
        rows=lookup.select(self.data,'surface-light',limit=100)
        self.assertTrue(any(r['id']=='react-bits' for r in rows))
        all_rows=lookup.select(self.data,role='visual-implementation',limit=100)
        self.assertEqual([r['name'].casefold() for r in all_rows], sorted(r['name'].casefold() for r in all_rows))

    def test_old_catalog_without_facets_still_loads(self):
        self.data.pop('discovery_facets')
        for row in self.data['resources']:row.pop('discovery_profile',None)
        self.assertEqual(lookup.validate_catalog(self.data),[])
        self.assertTrue(lookup.select(self.data,need='motion'))

    def test_unclassified_is_not_unavailable(self):
        row=self.data['resources'][0]
        row.pop('discovery_profile',None)
        self.assertTrue(lookup.select(self.data,identifier=row['id']))
        self.assertEqual(lookup.select(self.data,identifier=row['id'],role='visual-implementation'),[])

    def test_invalid_facet_names_are_input_errors(self):
        for args in ({'role':'best'},{'reuse_scope':'perfect-ui'}):
            with self.subTest(args=args),self.assertRaises(ValueError):lookup.select(self.data,**args)

    def test_bad_facet_shapes_are_local_errors(self):
        for value in (None,[],False,'premium'):
            data=copy.deepcopy(self.data);data['discovery_facets']=value
            self.assertTrue(lookup.validate_catalog(data))
        for field,value in [('roles',[{}]),('reuse_scopes','page'),('visual_forms',{}),('basis',None),('sources',['https://u:p@example.test']),('classified_on',[])]:
            data=copy.deepcopy(self.data);data['resources'][0]['discovery_profile'][field]=value
            self.assertTrue(lookup.validate_catalog(data),(field,value))

    def test_explicit_null_or_non_object_profile_is_not_absent(self):
        for value in (None, [], False, 'visual'):
            data=copy.deepcopy(self.data)
            data['resources'][0]['discovery_profile']=value
            self.assertTrue(lookup.validate_catalog(data))

    def test_optional_empty_profile_labels_remain_representable(self):
        self.data['resources'][0]['discovery_profile']['roles']=[]
        self.data['resources'][0]['discovery_profile']['reuse_scopes']=[]
        self.assertEqual(lookup.validate_catalog(self.data),[])

    def test_unknown_profile_label_does_not_rank(self):
        self.data['resources'][0]['discovery_profile']['roles']=['best']
        self.assertTrue(any('unknown roles' in x for x in lookup.validate_catalog(self.data)))

    def test_selection_does_not_mutate_data(self):
        before=copy.deepcopy(self.data)
        lookup.select(self.data,role='visual-implementation',limit=100)
        self.assertEqual(self.data,before)

    def test_cli_reports_nonjudgmental_facet_scope(self):
        run=subprocess.run([sys.executable,str(ROOT/'skills/ui-spec/scripts/find_resources.py'),'--role','visual-implementation','--json'],capture_output=True,text=True,encoding='utf-8',check=True)
        result=json.loads(run.stdout)
        self.assertIn('unclassified',result['facet_scope'])
        self.assertIn('no design-quality ranking',result['ordering'])
        self.assertNotIn('next_action',result)
        self.assertNotIn('ok',result)

    def test_zero_matches_not_strategy(self):
        run=subprocess.run([sys.executable,str(ROOT/'skills/ui-spec/scripts/find_resources.py'),'nonexistent-xxx','--role','visual-implementation','--json'],capture_output=True,text=True,encoding='utf-8',check=True)
        result=json.loads(run.stdout)
        self.assertEqual(result['count'],0)
        self.assertIn('not assessed',result['query_observation'])
        self.assertNotIn('next_action',result)

    def test_distinct_finesse_identities(self):
        r=lookup.select(self.data,identifier='finesse')[0]
        self.assertEqual(r['sources'],['https://finesseui.com/'])
        self.assertIn('not mouse-lin',r['discovery_profile']['basis'])

    def test_actual_installed_lookup_carries_facets(self):
        with tempfile.TemporaryDirectory() as td:
            import zipfile
            paths=package.build(ROOT,Path(td)/'out')
            with zipfile.ZipFile(paths[1]) as z:z.extractall(Path(td)/'installed')
            path=Path(td)/'installed/ui-spec/scripts/find_resources.py'
            result=subprocess.run([sys.executable,str(path),'--role','visual-implementation','--reuse-scope','effect','--json'],cwd=td,capture_output=True,text=True,encoding='utf-8',check=True)
            self.assertTrue(json.loads(result.stdout)['results'])

    def test_current_runtime_dispositions_and_old_dates(self):
        rec=json.loads((ROOT/'docs/evidence/v1.16.0/continuity.json').read_text(encoding='utf-8'))
        fr=json.loads((ROOT/'docs/evidence/v1.16.0/baseline-runtime.json').read_text(encoding='utf-8'))
        payload=zlib.decompress(base64.b64decode(fr['payload']))
        self.assertEqual(hashlib.sha256(payload).hexdigest(),fr['payload_sha256'])
        baseline=json.loads(payload)
        self.assertEqual(set(baseline),{r['path'] for r in rec['files']})
        for row in rec['files']:
            old=baseline[row['path']].encode('utf-8');new=(ROOT/row['path']).read_bytes()
            self.assertEqual(hashlib.sha256(old).hexdigest(),row['before_sha256'])
            self.assertEqual(hashlib.sha256(new).hexdigest(),row['current_sha256'])
            if row['disposition']=='unchanged':self.assertEqual(old,new)
            elif row['disposition']=='append-only':self.assertTrue(new.startswith(old))
            else:self.assertTrue(row['reason'])
        old_catalog=json.loads(baseline['skills/ui-spec/assets/resource-catalog.json'])
        self.assertEqual(old_catalog['snapshot_date'],self.data['snapshot_date'])
        self.assertEqual(len(old_catalog['resources']),len(self.data['resources']))
        current={x['id']:x for x in self.data['resources']}
        for old in old_catalog['resources']:
            self.assertEqual(old['reviewed_on'],current[old['id']]['reviewed_on'])
            self.assertEqual(old['sources'],current[old['id']]['sources'])

    def test_neutral_inspectors_and_history_unchanged(self):
        rec=json.loads((ROOT/'docs/evidence/v1.16.0/continuity.json').read_text(encoding='utf-8'))
        for item in rec['neutral_inspectors_unchanged']+rec['historical_evidence_unchanged']:
            self.assertEqual(hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest(),item['sha256'])

    def test_detailed_craft_is_installed_not_only_in_docs(self):
        cases={
          'component-sourcing.md':['Reuse Scope','Visual Completeness','Functional Foundation','Integrated Perceptual Quality','neither a closed','original demonstration','not a mandatory sequence'],
          'principles.md':['actual glyphs','Material coherence','not a universal style','Product'],
          'interaction-and-variants.md':['Interaction ownership','recent velocity','pointercancel','not copied constants'],
          'patterns.md':['A composer that inherits','A sheet that retains'],
          'verification.md':['skeleton','actual source adoption','not aesthetic scores'],
          'evidence-map.md':['cannot judge visual completeness','no mandatory']}
        for name,terms in cases.items():
            text=(ROOT/'skills/ui-spec/references'/name).read_text(encoding='utf-8')
            for term in terms:
                # These are removal alarms; human source review checks the semantics.
                if name=='evidence-map.md' and term=='no mandatory':term='a new mandatory'
                with self.subTest(file=name,term=term):self.assertIn(term,text)

if __name__=='__main__':unittest.main()
