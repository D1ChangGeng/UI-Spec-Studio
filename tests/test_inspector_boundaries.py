"""Boundary/property regressions; synthetic fixtures, not independent Agent trials."""
from __future__ import annotations
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from test_tools import ROOT, prepare, checker as manifest, load
from test_design_evidence import sample, checker as design

integrity=load('independent_integrity','skills/ui-spec/scripts/check_file_integrity.py')


class InspectorBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name);(self.root/'evidence.txt').write_bytes(b'fake media fixture')

    def test_independent_digest_match_and_mismatch(self):
        b=(self.root/'evidence.txt').read_bytes()
        good=integrity.compare(self.root,'evidence.txt',hashlib.sha256(b).hexdigest())
        bad=integrity.compare(self.root,'evidence.txt','0'*64)
        self.assertEqual(good['digest_result'],'match');self.assertEqual(bad['digest_result'],'mismatch')
        self.assertEqual(good['verification_scope'],'one local regular file byte digest')

    def test_digest_invalid_hex_and_outside_path(self):
        for path,digest in [('evidence.txt','bad'),('../evidence.txt','0'*64)]:
            with self.assertRaises(ValueError):integrity.compare(self.root,path,digest)

    def test_independent_digest_exit_codes(self):
        cmd=[sys.executable,str(ROOT/'skills/ui-spec/scripts/check_file_integrity.py'),'--project-root',str(self.root),'--path','evidence.txt','--sha256']
        expected=hashlib.sha256((self.root/'evidence.txt').read_bytes()).hexdigest()
        for value,code in [(expected,0),('0'*64,1),('invalid',2)]:
            r=subprocess.run(cmd+[value],capture_output=True,text=True,timeout=10)
            self.assertEqual(r.returncode,code,r.stderr)
            self.assertNotIn('Traceback',r.stderr)

    def test_inspector_does_not_read_referenced_file_contents(self):
        d=sample()
        with patch.object(Path,'read_bytes',side_effect=AssertionError('inspector read file bytes')):
            report=design.inspect_record(d,self.root)
        self.assertEqual(report['file_observations'][0]['content_inspection'],'not_performed')

    def test_status_permutations_do_not_generate_policy_findings(self):
        baseline=sample()
        for ev in ('acquired','observed','new-custom-state'):
            for action in ('trial','implement','expand','finish','specialized-project-step'):
                d=copy.deepcopy(baseline);d['evidence'][0]['status']=ev
                d['decisions'][0]['next_action']={'kind':action}
                d['decisions'][0]['gaps']=[{'id':'G','impact':'high','status':'blocked'}]
                self.assertEqual(design.inspect_record(d,self.root)['structural_findings'],[])

    def test_theoretical_hints_do_not_produce_nonzero_exit(self):
        p=self.root/'empty.json';p.write_text(json.dumps({'format':design.FORMAT,'objects':[],'decisions':[]}))
        r=subprocess.run([sys.executable,str(ROOT/'skills/ui-spec/scripts/check_design_evidence.py'),'--project-root',str(self.root),'--record',p.name],capture_output=True,text=True,timeout=10)
        data=json.loads(r.stdout)
        self.assertEqual(r.returncode,0)
        self.assertEqual(len(data['candidate_unrepresented_categories']),16)

    def test_unfilled_prepare_has_no_assumed_environment_or_acceptance(self):
        (self.root/'DESIGN.md').write_text('Unreviewed user file')
        result=prepare.prepare(self.root,'A name')
        data=json.loads((self.root/'.ui-spec/manifest.json').read_text())
        self.assertEqual(data['record_origin'],'initialized_unconfirmed')
        self.assertEqual(data['viewports'],[]);self.assertEqual(data['variants'],[])
        self.assertEqual(data['approvals'],[]);self.assertIsNone(data['revision'])
        self.assertEqual(data['initialization']['design_reference_status'],'file_detected_content_and_approval_not_inspected')
        self.assertIn('no viewport',result['limits'])

    def test_lookup_zero_match_has_no_next_action(self):
        r=subprocess.run([sys.executable,str(ROOT/'skills/ui-spec/scripts/find_resources.py'),'no-match-unique-phrase','--json'],capture_output=True,text=True,timeout=10)
        d=json.loads(r.stdout);self.assertEqual(d['count'],0)
        self.assertNotIn('next_action',d);self.assertIn('query_observation',d)
        self.assertEqual(d['result_kind'],'dated_catalog_matches')

    def test_all_record_views_are_read_only_even_with_invalid_references(self):
        d=sample();d['decisions'][0]['evidence']=['missing'];before=copy.deepcopy(d)
        for view in ('overview','detail','execution'):
            result=design.inspect_record(d,self.root,view=view)
            self.assertIn('view',result);self.assertEqual(d,before)

    def test_invalid_row_does_not_shift_finding_location(self):
        d=sample();d['evidence'].insert(0,17);d['evidence'][1]['objects']=['absent']
        report=design.inspect_record(d,self.root)
        paths=[x['path'] for x in report['structural_findings']]
        self.assertIn('$.evidence[0]',paths);self.assertIn('$.evidence[1].objects[0]',paths)

    def test_duplicate_id_reference_is_ambiguous_not_resolved(self):
        d=sample();d['objects'].append(copy.deepcopy(d['objects'][1]))
        result=design.inspect_record(d,self.root)
        self.assertIn('ambiguous',[x['resolution'] for x in result['reference_observations'] if x['id']=='panel'])

    def test_malformed_nested_values_are_local_findings(self):
        original=sample()
        changes=[('relations',[{'from':{},'to':[],'type':7}]),('required_checks',[{'object':[],'condition':{},'domain':17}]),
                 ('decisions',[{'id':'D','objects':{},'comparison':{'alternatives':42},'next_action':[]}]),
                 ('objects',[{'id':['not-an-id'],'level':{},'parent':[]}])]
        for key,value in changes:
            d=copy.deepcopy(original);d[key]=value
            with self.subTest(key=key):
                r=design.inspect_record(d,self.root)
                self.assertTrue(r['structural_findings'])
                self.assertEqual(r['record_readability'],'readable')

    def test_historical_archive_not_read_as_current(self):
        (self.root/'archive.json').write_text('{not readable JSON')
        d=sample();d['archive']=[{'id':'past','location':{'path':'archive.json'}}]
        r=design.inspect_record(d,self.root)
        self.assertEqual(r['counts']['decisions'],1)
        self.assertFalse(r['structural_findings'])
        self.assertTrue(any(f.get('content_inspection')=='not_performed' for f in r['file_observations']))

    def test_malformed_file_lists_keep_original_indices(self):
        d=sample()
        d['decisions'][0]['implementation']={'state':'adopted','paths':[None,'missing.py']}
        report=design.inspect_record(d,self.root)
        file=next(f for f in report['file_observations'] if f.get('path')=='missing.py')
        self.assertEqual(file['field'],'$.decisions[0].implementation.paths[1]')

    def test_manifest_malformed_ids_remain_readable_observations(self):
        data={'schema_version':1,'viewports':[None,{'id':'desktop','width':0,'height':800}],
              'variants':[None,{'id':'light','theme':{},'locale':'en'}],
              'routes':[{'id':'editor:bad','states':['pending:input'],'primary_state':'pending:input','critical_states':['pending:input']}],
              'checks':[{'id':'C','kind':'visual','route':'editor:bad','state':'pending:input','viewport':'desktop','variant':'light','evidence':[None,'missing.png']}],
              'exceptions':[None,{'target':'visual:editor:bad:pending:input:desktop:light','reason':42}]}
        report=manifest.inspect_record(data,self.root)
        self.assertEqual(report['record_readability'],'readable')
        self.assertTrue(any(x['path']=='$.viewports[1].width' for x in report['structural_findings']))
        self.assertTrue(any(x['path']=='$.variants[1].theme' for x in report['structural_findings']))
        self.assertTrue(any(x['path']=='$.exceptions[1].reason' for x in report['structural_findings']))
        self.assertTrue(any(x.get('field')=='$.checks[0].evidence[1]' for x in report['file_observations']))

    def test_scope_change_does_not_rewrite_original_evidence(self):
        d=sample();before=copy.deepcopy(d)
        design.inspect_record(d,self.root,changed=['font'])
        self.assertEqual(d,before)

    def test_file_safety_internal_directory_symlink(self):
        (self.root/'inside').mkdir();(self.root/'inside/data').write_text('test')
        try:(self.root/'link').symlink_to(self.root/'inside',target_is_directory=True)
        except (OSError,NotImplementedError):self.skipTest('Symlinks unavailable')
        d=sample();d['evidence'][0]['location']={'path':'link/data'}
        self.assertTrue(any(f['code']=='path_not_inspected' for f in design.inspect_record(d,self.root)['structural_findings']))


if __name__=='__main__':unittest.main()
