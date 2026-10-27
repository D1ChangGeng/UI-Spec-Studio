"""Authored declaration/path fixtures; these are not Agent behavior or visual-quality tests."""
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/ui-spec/scripts"))
SCRIPT = ROOT / "skills/ui-spec/scripts/check_design_evidence.py"
spec = importlib.util.spec_from_file_location("design_evidence_checker", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def sample() -> dict:
    return {
        "format": checker.FORMAT, "revision": "fixture-r1",
        "objects": [{"id": "goal", "level": "L0", "title": "Synthetic task"},
                    {"id": "panel", "level": "L2", "title": "Synthetic panel", "parent": "goal"},
                    {"id": "font", "level": "L4", "title": "Synthetic typography"},
                    {"id": "independent", "level": "L3", "title": "Unrelated supported change"}],
        "conditions": [{"id": "wide", "description": "Fixture wide/light/English/open state"},
                       {"id": "narrow", "description": "Fixture narrow/dark/Chinese/open state"}],
        "relations": [{"from": "font", "to": "panel", "type": "affects"}],
        "evidence": [{"id": "E1", "kind": "visual", "role": "integrated", "status": "observed",
                      "location": {"path": "evidence.txt"}, "objects": ["panel"], "conditions": ["wide"],
                      "product_revision": "fixture-r1", "observation": "Authored test declaration; no real visual inspection claimed"}],
        "decisions": [{"id": "D1", "objects": ["panel"], "purpose": "Synthetic readable panel",
                       "question": "Can the fixture record support this scoped declaration?",
                       "judgment": "Authored declaration for testing only", "choice": "Synthetic candidate",
                       "evidence": ["E1"], "checks": [{"domain": "visual", "status": "pass", "objects": ["panel"],
                          "conditions": ["wide"], "revision": "fixture-r1", "evidence": ["E1"],
                          "finding": "Synthetic fixture declaration, not a product-quality result"}],
                       "gaps": [], "next_action": {"kind": "verify", "reason": "Inspect remaining real conditions separately"}}],
        "coverage_challenges": [], "required_checks": []}


class DesignEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        (self.root/'evidence.txt').write_text('Synthetic file, not inspected pixels')
        (self.root/'component.py').write_text('# synthetic fixture')
        self.data=sample();self.decision=self.data['decisions'][0]
        self.evidence=self.data['evidence'][0];self.check=self.decision['checks'][0]

    def result(self): return checker.inspect_record(self.data,self.root)

    def assert_finding(self, code):
        self.assertIn(code,[x['code'] for x in self.result()['structural_findings']])

    def assert_neutral(self):
        r=self.result();self.assertEqual(r['record_readability'],'readable')
        for key in ('ok','satisfied','pending_coverage','affected_decisions','next_action'):
            self.assertNotIn(key,r)
        return r

    def test_structure_without_research_no_completion_signal(self):
        self.data['evidence']=[];self.decision.update(evidence=[],checks=[])
        r=self.assert_neutral();self.assertEqual(r['counts']['evidence'],0)

    def test_empty_template_has_no_fabricated_decisions(self):
        d=json.loads((ROOT/'skills/ui-spec/assets/templates/design-evidence.json').read_text())
        r=checker.inspect_record(d,self.root)
        self.assertEqual(r['record_source']['record_origin'],'unfilled_template')
        self.assertEqual(r['counts']['objects'],0)
        self.assertFalse(r['structural_findings'])

    def test_parsed_wrong_root_still_readable_with_shape_finding(self):
        r=checker.inspect_record([],self.root)
        self.assertEqual(r['record_readability'],'readable')
        self.assertEqual(r['structural_findings'][0]['code'],'record_shape')

    def test_duplicate_ids(self):
        self.data['objects'].append(copy.deepcopy(self.data['objects'][0]))
        self.assert_finding('duplicate_id')

    def test_unknown_level(self):
        self.data['objects'][0]['level']='L6';self.assert_finding('unlisted_level')

    def test_unknown_parent(self):
        self.data['objects'][1]['parent']='missing';self.assert_finding('unresolved_reference')

    def test_containment_cycle_is_graph_fact(self):
        self.data['objects'][0]['parent']='panel';self.assert_finding('containment_cycle');self.assert_neutral()

    def test_dependency_cycle_has_finite_candidates(self):
        self.data['relations'].append({'from':'panel','to':'font','type':'affects'})
        r=checker.project_view(self.data,'overview',['font'])['declared_relation_review_candidates']
        self.assertEqual(r['object_ids'],['font','goal','panel'])
        self.assertEqual(r['task_applicability'],'not_assessed')

    def test_unknown_reference(self):
        self.decision['evidence']=['missing'];self.assert_finding('unresolved_reference')

    def test_missing_file(self):
        self.evidence['location']={'path':'missing.png'};self.assert_finding('local_file_reference')

    def test_unsafe_paths(self):
        for path in ('../outside','/etc/passwd','C:/secret','folder\\file.txt'):
            with self.subTest(path=path):
                self.evidence['location']={'path':path};self.assert_finding('path_not_inspected')

    def test_symlink_not_followed(self):
        try:(self.root/'alias').symlink_to(self.root/'evidence.txt')
        except (OSError,NotImplementedError):self.skipTest('Symlinks unavailable')
        self.evidence['location']={'path':'alias'};self.assert_finding('path_not_inspected')

    def test_directory_is_metadata_not_file_evidence(self):
        self.evidence['location']={'path':'.'}
        self.assertEqual(self.result()['file_observations'][0]['filesystem_kind'],'directory')

    def test_digest_not_compared_by_inspector(self):
        self.evidence['sha256']='0'*64
        r=self.assert_neutral();self.assertFalse(r['structural_findings'])
        self.assertNotIn('observed_sha256',json.dumps(r))

    def test_remote_reference_not_fetched(self):
        self.evidence['location']={'url':'https://example.invalid/item'}
        self.assertEqual(self.result()['file_observations'][0]['availability'],'not_fetched')

    def test_credentials_and_non_http_not_fetched(self):
        for url in ('https://user:secret@example.invalid','file:///etc/passwd','javascript:alert(1)'):
            self.evidence['location']={'url':url};self.assert_finding('url_shape')

    def test_one_candidate_not_rejected(self):
        self.decision['comparison']={'state':'compared','alternatives':['one'],'evidence':[]}
        self.assertFalse(self.result()['structural_findings']);self.assert_neutral()

    def test_same_candidate_name_not_professionally_classified(self):
        self.decision['comparison']={'state':'compared','alternatives':['A','A']}
        self.assertFalse(self.result()['structural_findings'])

    def test_missing_observation_is_description_not_design_failure(self):
        del self.evidence['observation']
        r=self.result();self.assertFalse(r['structural_findings'])
        self.assertIn({'path':'$.evidence[0].observation','presence':'not_declared'},r['field_observations'])

    def test_acquired_does_not_generate_pass_or_block(self):
        self.evidence['status']='acquired';self.assertFalse(self.result()['structural_findings']);self.assert_neutral()

    def test_text_visual_mismatch_is_left_to_professional_judgment(self):
        self.evidence['kind']='text';self.assertFalse(self.result()['structural_findings'])
        self.assertEqual(self.result()['declared_check_records'][0]['declared_status'],'pass')

    def test_demo_and_integration_roles_remain_visible(self):
        self.evidence['role']='demo'
        r=self.result();self.assertFalse(r['structural_findings'])
        self.assertEqual(r['declared_check_records'][0]['domain'],'visual')

    def test_known_different_conditions_not_rejected(self):
        self.check['conditions'].append('narrow');self.assertFalse(self.result()['structural_findings'])

    def test_parent_and_child_no_certification(self):
        self.check['objects']=['goal'];self.assertFalse(self.result()['structural_findings']);self.assert_neutral()

    def test_global_snapshot_does_not_invalidate_scoped_history(self):
        self.data['revision']='unrelated-server-r2'
        r=self.result();self.assertFalse(r['structural_findings'])
        self.assertIn('fixture-r1',[x['declared_revision'] for x in r['revision_declarations']])

    def test_temporal_window_missing_is_field_observation(self):
        self.evidence['kind']='temporal';self.check['domain']='temporal'
        self.assertFalse(self.result()['structural_findings'])
        self.assertIn({'path':'$.evidence[0].window','presence':'not_declared'},self.result()['field_observations'])

    def test_existing_file_does_not_establish_adoption(self):
        self.decision['implementation']={'state':'adopted','paths':['component.py']}
        r=self.assert_neutral()
        self.assertTrue(all(x.get('content_inspection')=='not_performed' for x in r['file_observations']))

    def test_adoption_without_path_is_not_implementation_veto(self):
        self.decision['implementation']={'state':'adopted','paths':[]}
        self.assertFalse(self.result()['structural_findings'])

    def test_high_impact_gap_does_not_veto_actions(self):
        self.decision['gaps']=[{'id':'G','question':'Unseen behavior','impact':'high','status':'open'}]
        for action in ('trial','implement','expand','finish'):
            with self.subTest(action=action):
                self.decision['next_action']={'kind':action,'reason':'Agent decision recorded'}
                r=self.assert_neutral();self.assertFalse(r['structural_findings'])
                self.assertEqual(r['declared_actions'][0]['declared_value']['kind'],action)

    def test_no_next_action_is_not_tool_generated(self):
        del self.decision['next_action']
        self.assertEqual(self.result()['declared_actions'],[])

    def test_resolved_gap_does_not_certify_or_require_evidence_type(self):
        self.decision['gaps']=[{'id':'G','status':'resolved','impact':'high','question':'Fixture'}]
        self.assertFalse(self.result()['structural_findings']);self.assert_neutral()

    def test_waiver_not_counted_as_check(self):
        self.check['status']='waived'
        self.data['required_checks']=[{'object':'panel','condition':'wide','domain':'visual'}]
        r=self.result()
        self.assertEqual(len(r['declared_check_records']),0)
        self.assertEqual(len(r['declared_exception_records']),1)
        self.assertFalse(r['declared_item_records'][0]['check_record_fields'])
        self.assertTrue(r['declared_item_records'][0]['exception_record_fields'])

    def test_declared_approval_not_authenticated(self):
        self.decision['approval']={'status':'approved'}
        r=self.result();self.assertFalse(r['structural_findings'])
        self.assertIn({'path':'$.decisions[0].approval.source','presence':'not_declared'},r['field_observations'])

    def test_planned_check_counts_as_record_without_being_pass(self):
        self.check['status']='planned'
        self.data['required_checks']=[{'object':'panel','condition':'wide','domain':'visual'}]
        r=self.result();self.assertFalse(r['unlisted_declared_items'])
        self.assertEqual(r['declared_check_records'][0]['declared_status'],'planned')

    def test_unlisted_declared_item_never_blocks_finish(self):
        self.data['required_checks']=[{'object':'panel','condition':'narrow','domain':'visual'}]
        self.decision['next_action']['kind']='finish'
        r=self.result();self.assertEqual(len(r['unlisted_declared_items']),1)
        self.assertFalse(r['structural_findings'])

    def test_theoretical_absence_not_declared_absence(self):
        r=self.result();self.assertFalse(r['unlisted_declared_items'])
        self.assertTrue(r['candidate_unrepresented_categories'])
        self.assertTrue(all(x['task_applicability']=='not_assessed' for x in r['candidate_unrepresented_categories']))

    def test_explicit_category_tag_not_prose_inference(self):
        self.data['objects'][0]['title']='Excellent responsive typography'
        self.data['objects'][0]['categories']=['typography-content']
        hints={r['category'] for r in self.result()['candidate_unrepresented_categories']}
        self.assertNotIn('typography-content',hints);self.assertIn('responsive-variants',hints)

    def test_unknown_changed_id_is_only_unresolved_lookup(self):
        r=checker.project_view(self.data,'overview',['missing'])
        self.assertEqual(r['declared_relation_review_candidates']['unresolved_changed_ids'],['missing'])

    def test_three_views_read_only(self):
        before=copy.deepcopy(self.data)
        for view in ('overview','detail','execution'):
            r=checker.project_view(self.data,view,['font'])
            self.assertEqual(r['decisions'][0]['id'],'D1')
            self.assertEqual(r['declared_relation_review_candidates']['decision_ids'],['D1'])
            r['decisions'][0]['id']='modified-return-value'
        self.assertEqual(self.data,before)

    def test_revision_and_archive_do_not_override_current_model(self):
        (self.root/'old.json').write_text(json.dumps({'decisions':[{'id':'D1','choice':'old'}]}))
        self.data['archive']=[{'id':'old','location':{'path':'old.json'},'revision':'old-r0'}]
        self.data['revisions']=[{'id':'R1','summary':'Replaced candidate','reason':'Actual trial changed fit','historical_objects':['removed-panel'],'current_judgment':'Use current choice'}]
        r=self.result();self.assertFalse(r['structural_findings'])
        self.assertEqual(r['view']['decisions'][0]['id'],'D1')
        self.assertEqual(r['view']['evidence_archive_references'][0]['revision'],'old-r0')

    def test_reopening_resolved_gap_does_not_alter_prior_record(self):
        self.decision['gaps']=[{'id':'G','status':'resolved','impact':'high','question':'Old single-line layout'}]
        prior=copy.deepcopy(self.data);self.decision['gaps'][0]['status']='open'
        self.result();self.assertEqual(prior['decisions'][0]['gaps'][0]['status'],'resolved')
        self.assertEqual(self.decision['gaps'][0]['status'],'open')

    def test_runtime_pass_cannot_certify_visual_quality(self):
        self.check['domain']='engineering';self.check['finding']='Known poor aesthetics in this synthetic fixture'
        self.assert_neutral();self.assertFalse(self.result()['structural_findings'])

    def test_low_impact_evidence_does_not_require_extra_research(self):
        self.decision.update(comparison={'state':'inherited'},next_action={'kind':'implement','reason':'Bounded supported change'})
        self.assertFalse(self.result()['structural_findings'])
        self.assertEqual(len(self.result()['declared_actions']),1)

    def test_malformed_shapes_do_not_crash(self):
        for collection,key in (('objects','level'),('evidence','kind'),('decisions','checks')):
            for value in ({},[7],7):
                d=copy.deepcopy(self.data);d[collection][0][key]=value
                r=checker.inspect_record(d,self.root);self.assertTrue(r['structural_findings'])

    def test_open_discovery_without_action_does_not_generate_one(self):
        self.data['coverage_challenges']=[{'discovery':'Possible mobile state','disposition':'open'}]
        self.assertFalse(self.result()['structural_findings'])

    def test_cli_findings_readable_exit_zero(self):
        self.decision['evidence']=['unlisted']
        (self.root/'record.json').write_text(json.dumps(self.data))
        before={p.name:p.read_bytes() for p in self.root.iterdir()}
        run=subprocess.run([sys.executable,str(SCRIPT),'--project-root',str(self.root),'--record','record.json'],text=True,capture_output=True,timeout=10)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertEqual(json.loads(run.stdout)['record_readability'],'readable')
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.root.iterdir()})

    def test_cli_malformed_record_exit_two(self):
        for value in ('{invalid','{"x":1,"x":2}','{"x":NaN}'):
            (self.root/'bad.json').write_text(value)
            run=subprocess.run([sys.executable,str(SCRIPT),'--project-root',str(self.root),'--record','bad.json'],text=True,capture_output=True,timeout=10)
            self.assertEqual(run.returncode,2)
            self.assertEqual(json.loads(run.stdout)['record_readability'],'unreadable')
            self.assertNotIn('Traceback',run.stderr)


if __name__=='__main__':unittest.main()
