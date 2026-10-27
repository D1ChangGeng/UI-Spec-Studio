"""Literal query and exact historical preservation tests, not perceptual certification."""
from __future__ import annotations
import copy, hashlib, json, subprocess, sys, unittest
from test_tools import ROOT, load
from source_continuity import runtime_v116
lookup=load('reconciled_craft_lookup','skills/ui-spec/scripts/find_resources.py')
class CraftReconciliationTests(unittest.TestCase):
    def setUp(self):self.data=lookup.load_catalog()
    def test_role_scope_and_stack_intersect(self):
        rows=lookup.select(self.data,role='visual-implementation',reuse_scope='visual-component',stack='vue',limit=100)
        self.assertEqual({x['id'] for x in rows},{'vue-bits','inspira'})
    def test_functional_foundation_does_not_include_react_bits(self):
        ids={x['id'] for x in lookup.select(self.data,role='functional-foundation',limit=100)}
        self.assertIn('radix-primitives',ids);self.assertNotIn('react-bits',ids)
    def test_scope_block_returns_actual_declared_labels(self):
        rows=lookup.select(self.data,role='visual-implementation',reuse_scope='block',limit=100)
        self.assertTrue(rows);self.assertTrue(all('block' in x['craft_profile']['reuse_scopes'] for x in rows))
    def test_unclassified_lead_still_exists(self):
        row=next(x for x in self.data['resources'] if 'craft_profile' not in x)
        self.assertTrue(lookup.select(self.data,identifier=row['id']))
        self.assertEqual(lookup.select(self.data,identifier=row['id'],role='visual-implementation'),[])
    def test_legacy_catalog_without_profiles(self):
        for row in self.data['resources']:row.pop('craft_profile',None)
        self.assertEqual(lookup.validate_catalog(self.data),[])
        self.assertTrue(lookup.select(self.data,need='motion'))
    def test_unknown_labels_are_input_errors(self):
        for args in ({'role':'best'},{'reuse_scope':'perfect'}):
            with self.assertRaises(ValueError):lookup.select(self.data,**args)
    def test_malformed_optional_profiles(self):
        for value in (None,False,[],{'roles':[{}],'reuse_scopes':[],'visual_forms':[]}):
            d=copy.deepcopy(self.data);d['resources'][0]['craft_profile']=value
            self.assertTrue(lookup.validate_catalog(d))
    def test_invalid_resource_collection_still_reports_errors(self):
        for value in (None, False, {}, 'invalid'):
            d=copy.deepcopy(self.data);d['resources']=value
            self.assertTrue(lookup.validate_catalog(d))
    def test_empty_labels_are_not_quality_failures(self):
        self.data['resources'][0]['craft_profile']={'roles':[],'reuse_scopes':[],'visual_forms':[]}
        self.assertEqual(lookup.validate_catalog(self.data),[])
    def test_literal_form_search_and_order(self):
        rows=lookup.select(self.data,'pointer-response',limit=100)
        self.assertIn('react-bits',{x['id'] for x in rows})
        rows=lookup.select(self.data,role='visual-implementation',limit=100)
        self.assertEqual([x['name'].casefold() for x in rows],sorted(x['name'].casefold() for x in rows))
    def test_read_only_and_no_strategy(self):
        before=copy.deepcopy(self.data);lookup.select(self.data,role='visual-implementation')
        self.assertEqual(before,self.data)
        result=subprocess.run([sys.executable,str(ROOT/'skills/ui-spec/scripts/find_resources.py'),'absent-source-xyz','--role','visual-implementation','--json'],capture_output=True,text=True,encoding='utf-8',check=True)
        data=json.loads(result.stdout);self.assertEqual(data['count'],0)
        self.assertIn('unclassified',data['facet_scope']);self.assertNotIn('next_action',data);self.assertNotIn('ok',data)
    def test_current_runtime_and_exact_published_predecessor(self):
        ledger=json.loads((ROOT/'docs/evidence/v1.16.1/continuity.json').read_text(encoding='utf-8'))
        self.assertEqual(ledger['baseline_commit'],'1ba50b1e1c6dfbd5540d9b54514ef81ac6160eec')
        for row in ledger['files']:
            current=(ROOT/row['path']).read_bytes();prior=runtime_v116(ROOT,row['path'])
            self.assertEqual(hashlib.sha256(current).hexdigest(),row['current_sha256'])
            self.assertEqual(hashlib.sha256(prior).hexdigest(),row['prior_sha256'])
            if row['disposition']=='unchanged':self.assertEqual(current,prior)
            if row['disposition']=='append-only':self.assertTrue(current.startswith(prior))
        for row in ledger['historical_evidence_unchanged']:
            self.assertEqual(hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest(),row['sha256'])
    def test_neutral_inspectors_remain_identical(self):
        for name in ('check_design_evidence','check_manifest','structural_records','check_file_integrity','prepare'):
            path='skills/ui-spec/scripts/'+name+'.py'
            self.assertEqual((ROOT/path).read_bytes(),runtime_v116(ROOT,path))
    def test_current_lessons_remain_in_installed_skill(self):
        p=(ROOT/'skills/ui-spec/references/patterns.md').read_text(encoding='utf-8')
        self.assertIn('Preserve task entry',p);self.assertIn('Observe settled overlay',p)
        self.assertIn('not proof of smooth natural delivery',p)
if __name__=='__main__':unittest.main()
