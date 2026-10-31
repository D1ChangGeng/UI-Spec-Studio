"""Mechanical runner/guard tests only; test doubles are NEVER Agent participants."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
runner=load('adaptive_study',ROOT/'tools/run_adaptive_research.py')
guard=load('adaptive_release_guard',ROOT/'tools/check_adaptive_release.py')

class StudyMechanicsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        # Canonical fixture roots avoid macOS's system /var alias without
        # relaxing the runner's rejection of caller-supplied linked ancestors.
        self.r=Path(self.temp.name).resolve()
        self.base=self.r/'baseline';self.candidate=self.r/'candidate'
        for method in (self.base,self.candidate):
            (method/'references').mkdir(parents=True);(method/'SKILL.md').write_text('# Explicit mechanical fixture, not real study input\n')
            for name in ('workflow','analysis','principles','component-sourcing','interaction-and-variants','verification','visual-assets','content-design'):
                (method/'references'/f'{name}.md').write_text('mechanical test fixture\n')
        self.starters=self.r/'starters';self.st=(self.starters/'T1');(self.st/'app').mkdir(parents=True)
        (self.st/'INPUT.md').write_text('Mechanical fixture; not a real UI study.\n');(self.st/'app/index.html').write_text('<p>fixture</p>')
        self.plan=self.r/'plan.json';self.out=self.r/'output';self.home=self.r/'home';self.home.mkdir()
        self.row={'id':'T1-C-r1','task':'T1','condition':'C','main_model':'test-model','subagent_model':'test-model',
                  'main_effort':'high','subagent_effort':'medium','timeout_seconds':10,'max_subagents':2}
        self.plan.write_text(json.dumps({'cells':[self.row]}))
    def prepare(self):return runner.prepare(baseline_skill=self.base,candidate_skill=self.candidate,starters=self.starters,plan=self.plan,output=self.out,roles=ROOT/'integrations/codex/agents')
    def test_freeze_records_exact_inputs(self):
        result=self.prepare();cell=result['cells'][0];w=self.out/'cells/T1-C-r1/workspace'
        self.assertEqual(runner.describe(runner.public_files_including_methods(w)),cell['workspace_files'])
        self.assertEqual(result['status'],'prepared_not_executed')
    def test_missing_codex_is_zero_real_runs(self):
        self.prepare()
        with patch.object(runner.shutil,'which',return_value=None):
            result=runner.run(study=self.out,cell_id='T1-C-r1',home=self.home,execute=True,acknowledge_cost=True)
        self.assertEqual(result['status'],'blocked_not_run');self.assertEqual(result['actual_independent_agent_runs'],0)
        self.assertFalse((self.out/'runs').exists())
    def test_frozen_input_mutation_rejected(self):
        self.prepare();(self.out/'cells/T1-C-r1/workspace/TASK.md').write_text('changed')
        with self.assertRaises(runner.StudyError):runner.run(study=self.out,cell_id='T1-C-r1',home=self.home)
    def test_existing_campaign_not_overwritten(self):
        self.prepare()
        with self.assertRaises(runner.StudyError):self.prepare()
    def test_duplicate_cells_rejected(self):
        self.plan.write_text(json.dumps({'cells':[self.row,self.row]}))
        with self.assertRaises(runner.StudyError):self.prepare()
        self.assertFalse(self.out.exists())
    def test_incomplete_skill_rejected(self):
        (self.base/'references/principles.md').unlink()
        with self.assertRaises(runner.StudyError):self.prepare()
    def test_private_starter_file_rejected(self):
        (self.st/'app/.env.local').write_text('synthetic fixture, not a secret')
        with self.assertRaises(runner.StudyError):self.prepare()
    def test_inherited_instructions_rejected(self):
        (self.st/'app/AGENTS.md').write_text('unregistered')
        with self.assertRaises(runner.StudyError):self.prepare()
    def test_t4_requires_real_settled_decision(self):
        row=dict(self.row,id='T4-F-r1',task='T4',condition='F-integrator');self.plan.write_text(json.dumps({'cells':[row]}))
        d=self.starters/'T4';(d/'app').mkdir(parents=True);(d/'app/x.txt').write_text('fixture');(d/'INPUT.md').write_text('fixture')
        with self.assertRaises(runner.StudyError):self.prepare()
    def test_unsafe_cell_rejected(self):
        for name in ('../x','x/y','x y',''):
            with self.subTest(name=name),self.assertRaises(runner.StudyError):runner.validate_cell(dict(self.row,id=name))
    def test_time_and_concurrency_boundaries(self):
        for key,value in [('timeout_seconds',0),('timeout_seconds',True),('max_subagents',0),('max_subagents',17)]:
            with self.subTest(key=key,value=value),self.assertRaises(runner.StudyError):runner.validate_cell(dict(self.row,**{key:value}))
        with self.assertRaises(runner.StudyError):runner.validate_cell(dict(self.row,network_access='true'))
    def test_unknown_condition_not_guessed(self):
        with self.assertRaises(runner.StudyError):runner.validate_cell(dict(self.row,condition='Z'))
    def test_profile_does_not_read_authentication(self):
        (self.home/'auth.json').write_text('not readable JSON; should never be inspected')
        result=runner.profile_preflight(self.home);self.assertEqual(result['auth'],'not_read')
    def test_profile_role_contamination_rejected(self):
        (self.home/'agents').mkdir();(self.home/'agents/other.toml').write_text('other')
        with self.assertRaises(runner.StudyError):runner.profile_preflight(self.home)
    def test_command_has_no_unsafe_execution_flags(self):
        row=dict(self.row,subagents_enabled=True);cmd=runner.command('codex',row,self.r/'work')
        self.assertIn('--json',cmd);self.assertIn('workspace-write',cmd)
        self.assertIn('--ephemeral',cmd)
        self.assertIn('sandbox_workspace_write.network_access=false',cmd)
        self.assertFalse(any('yolo' in x or 'dangerously' in x or x=='resume' for x in cmd))
    def test_inherited_profile_records_limits_without_reading_auth(self):
        (self.home/'auth.json').write_text('not JSON; never inspect authentication bytes')
        (self.home/'AGENTS.md').write_text('known instruction fixture')
        with patch.dict(runner.os.environ,{'CODEX_HOME':str(self.home)}):
            before=dict(runner.os.environ)
            result=runner.inherited_profile_preflight()
            self.assertEqual(dict(runner.os.environ),before)
        self.assertEqual(result['auth'],'not_read')
        self.assertFalse(result['environment_mutation'])
        self.assertIn('AGENTS.md',result['user_instruction_identities'])
        self.assertIn('not an empty profile',result['other_global_instruction_contamination'])
    def test_inherited_command_ignores_config_and_keeps_workspace_sandbox(self):
        row=dict(self.row,subagents_enabled=True)
        cmd=runner.command('codex',row,self.r/'work',inherit_profile=True,runtime_dir=self.r/'runtime')
        self.assertIn('--ignore-user-config',cmd)
        self.assertIn('workspace-write',cmd)
        self.assertTrue(any(x.startswith('sqlite_home=') for x in cmd))
        self.assertTrue(any(x.startswith('log_dir=') for x in cmd))
        self.assertFalse(any('CODEX_HOME=' in x for x in cmd))
    def test_command_registers_every_installed_role_with_exact_file(self):
        row=self.prepare()['cells'][0]
        workspace=self.out/'cells/T1-C-r1/workspace'
        cmd=runner.command('codex',row,workspace,inherit_profile=True,runtime_dir=self.r/'runtime')
        for role in runner.ADAPTER_ROLES:
            self.assertIn(f'agents.{role}.config_file='+json.dumps(str(workspace/'.codex/agents'/f'{role}.toml')),cmd)
            self.assertTrue(any(value.startswith(f'agents.{role}.description=') for value in cmd))
        self.assertIn('multi_agent',cmd)
    def test_network_access_is_frozen_and_explicit_in_command(self):
        self.row['network_access']=True;self.plan.write_text(json.dumps({'cells':[self.row]}))
        row=self.prepare()['cells'][0]
        self.assertTrue(row['network_access'])
        cmd=runner.command('codex',row,self.out/'cells/T1-C-r1/workspace')
        self.assertIn('sandbox_workspace_write.network_access=true',cmd)
    def test_profile_choice_must_be_explicit_and_exclusive(self):
        with self.assertRaises(runner.StudyError):
            runner.run(study=self.out,cell_id='unused')
        with self.assertRaises(runner.StudyError):
            runner.run(study=self.out,cell_id='unused',home=self.home,inherit_profile=True)
    def test_actual_event_parser_retains_usage_without_inferred_child_cost(self):
        raw=b'{"type":"thread.started","thread_id":"test-double-session"}\n{"type":"turn.completed","usage":{"input_tokens":2}}\n'
        r=runner.summarize_events(raw);self.assertEqual(r['thread_id'],'test-double-session');self.assertEqual(r['completed_turns'],1)
        self.assertIsNone(r['total_subagent_usage']);self.assertIsNone(r['actual_auxiliary_agent_count'])
    def test_malformed_and_error_events_not_hidden(self):
        r=runner.summarize_events(b'not-json\n{"type":"error","message":"test"}\n')
        self.assertEqual(r['malformed_lines'],1);self.assertEqual(r['failure_events'],1)
    def test_multiple_thread_starts_not_one_fresh_run(self):
        r=runner.summarize_events(b'{"type":"thread.started","thread_id":"a"}\n{"type":"thread.started","thread_id":"b"}\n')
        self.assertIsNone(r['thread_id'])
    def test_output_snapshot_immutable_and_excludes_font_secrets(self):
        work=self.r/'work';(work/'app').mkdir(parents=True);(work/'evidence').mkdir()
        (work/'app/index.html').write_text('initial');(work/'app/font.woff2').write_bytes(b'not a font fixture')
        (work/'app/.env').write_text('synthetic');(work/'evidence/observations.md').write_text('fixture')
        (work/'app/LICENSE.woff2').write_bytes(b'not a font fixture')
        (work/'app/COPYING.pem').write_text('synthetic key fixture, not a real credential')
        out=self.r/'result';out.mkdir();r=runner.snapshot_outputs(work,out)
        (work/'app/index.html').write_text('later')
        with zipfile.ZipFile(out/'product-output.zip') as z:
            self.assertEqual(z.read('app/index.html'),b'initial');self.assertNotIn('app/font.woff2',z.namelist());self.assertNotIn('app/.env',z.namelist())
            self.assertNotIn('app/LICENSE.woff2',z.namelist());self.assertNotIn('app/COPYING.pem',z.namelist())
        self.assertEqual(r['visual_review'],'not_performed_by_archiver');self.assertEqual(len(r['excluded']),4)
    def test_output_snapshot_preserves_source_and_upstream_legal_notices(self):
        work=self.r/'work';(work/'app/vendor').mkdir(parents=True)
        originals={'vendor/library.js':'export const source = true;',
                   'vendor/LICENSE':'MIT license fixture\nCopyright upstream\n',
                   'vendor/LICENSE-MIT':'Permission notice fixture\n',
                   'vendor/NOTICE':'Required attribution fixture\n',
                   'vendor/NOTICE-CRLF':'Required attribution fixture\r\nOriginal Windows newlines\r\n',
                   'vendor/COPYING':'Redistribution terms fixture\n',
                   'theme.scss':'$space: 1rem; .page { padding: $space; }',
                   'note.tid':'title: Example\n\nEditable research note\n',
                   'yarn.lock':'# Pinned dependency fixture\n'}
        # Write exact LF and CRLF source bytes on every OS; the archiver must
        # preserve both, rather than normalize platform text-mode output.
        for name,content in originals.items():(work/'app'/name).write_bytes(content.encode('utf-8'))
        (work/'app/vendor/font.woff2').write_bytes(b'not an actual font')
        (work/'app/.next/cache').mkdir(parents=True)
        (work/'app/.next/cache/generated.js').write_text('generated dependency cache, not product source')
        out=self.r/'result';out.mkdir();result=runner.snapshot_outputs(work,out)
        with zipfile.ZipFile(out/'product-output.zip') as archive:
            for name,content in originals.items():
                self.assertEqual(archive.read('app/'+name),content.encode('utf-8'))
            self.assertNotIn('app/vendor/font.woff2',archive.namelist())
            self.assertNotIn('app/.next/cache/generated.js',archive.namelist())
        self.assertEqual(result['excluded'],[{'path':'app/vendor/font.woff2','reason':'unsupported or private-sensitive type'}])
    def test_missing_app_prevents_preparation(self):
        (self.st/'app/index.html').unlink()
        with self.assertRaises(runner.StudyError):self.prepare()
    def test_method_and_role_files_are_separate(self):
        r=self.prepare()['cells'][0]
        self.assertEqual(r['method'],'baseline');self.assertEqual(r['role_names'],['ui_researcher'])
        self.assertEqual(r['allowed_role_names'],['ui_researcher'])
        self.assertEqual(r['installed_role_names'],list(runner.ADAPTER_ROLES))
        for role in runner.ADAPTER_ROLES:
            self.assertIn('.codex/agents/'+role+'.toml',r['workspace_files'])
    def test_baseline_and_generic_conditions_do_not_install_specialists(self):
        for condition in ('A','B'):
            with self.subTest(condition=condition):
                self.row.update(condition=condition,id='T1-'+condition)
                self.plan.write_text(json.dumps({'cells':[self.row]}))
                self.out=self.r/condition
                result=self.prepare()['cells'][0]
                self.assertEqual(result['installed_role_names'],[])
                self.assertFalse(any(p.startswith('.codex/agents/') for p in result['workspace_files']))
    def test_final_runtime_preserves_default_install_and_conditional_use(self):
        self.row.update(condition='G-final-runtime',id='T1-G')
        self.plan.write_text(json.dumps({'cells':[self.row]}))
        result=self.prepare()['cells'][0]
        self.assertEqual(result['installed_role_names'],list(runner.ADAPTER_ROLES))
        self.assertEqual(result['allowed_role_names'],list(runner.ADAPTER_ROLES))
    def test_research_conditions_keep_implementation_in_main(self):
        for condition in ('B','C','D','E-challenger','E-observer'):
            with self.subTest(condition=condition):
                self.assertIn('Do not delegate product implementation in this arm.',runner.CONDITIONS[condition]['instruction'])
    def test_f_main_and_integrator_share_task_but_not_delegation(self):
        self.assertEqual(runner.CONDITIONS['F-main']['skill'],runner.CONDITIONS['F-integrator']['skill'])
        self.assertFalse(runner.CONDITIONS['F-main']['agents']);self.assertTrue(runner.CONDITIONS['F-integrator']['agents'])
    def test_d_holds_method_and_prompt_constant(self):
        self.assertEqual(runner.CONDITIONS['C'],runner.CONDITIONS['D'])
    def test_symlink_source_rejected(self):
        try:(self.st/'app/link.txt').symlink_to(self.plan)
        except OSError:self.skipTest('symlinks unavailable')
        with self.assertRaises(runner.StudyError):self.prepare()
    def test_symlink_output_ancestor_rejected(self):
        target=self.r/'real-output';target.mkdir();alias=self.r/'output-alias'
        try:alias.symlink_to(target,target_is_directory=True)
        except OSError:self.skipTest('symlinks unavailable')
        self.out=alias/'campaign'
        with self.assertRaisesRegex(runner.StudyError,'Linked study root'):self.prepare()
        self.assertEqual(list(target.iterdir()),[])

class ReleaseEvidenceMechanicsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.r=Path(self.temp.name).resolve()
        (self.r/'docs/evidence/v1.20.0').mkdir(parents=True)
    def write_decision(self,data):
        (self.r/guard.DECISION).write_text(json.dumps(data))
    def test_pending_release_fails_closed(self):
        self.write_decision({'schema_version':1,'decision':'pending'})
        with self.assertRaisesRegex(guard.EvidenceError,'development candidate'):guard.require_release_evidence(self.r)
    def test_no_decision_fails_closed(self):
        with self.assertRaises(guard.EvidenceError):guard.require_release_evidence(self.r)
    def test_unknown_decision_never_approves(self):
        self.write_decision({'schema_version':1,'decision':'all tests passed'})
        with self.assertRaises(guard.EvidenceError):guard.require_release_evidence(self.r)
    def test_artifact_hash_tampering_rejected(self):
        p=self.r/'evidence.txt';p.write_text('actual')
        with self.assertRaises(guard.EvidenceError):guard.artifact(self.r,{'path':'evidence.txt','sha256':'0'*64})
    def test_artifact_identity_accepts_actual_bytes(self):
        p=self.r/'evidence.txt';p.write_text('actual')
        self.assertEqual(guard.artifact(self.r,{'path':'evidence.txt','sha256':guard.digest(b'actual')}),b'actual')
    def test_artifact_traversal_rejected(self):
        with self.assertRaises(guard.EvidenceError):guard.artifact(self.r,{'path':'../outside','sha256':'0'*64})
    def test_incomplete_artifact_is_not_evidence(self):
        for value in (None,{}, {'path':'x','sha256':'abc'}):
            with self.subTest(value=value),self.assertRaises(guard.EvidenceError):guard.artifact(self.r,value)
    def test_candidate_identity_changes_with_role(self):
        for name in ('VERSION','AGENTS.md','docs/MODEL.md','docs/WRITING.md'):
            p=self.r/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('fixture')
        d=self.r/'integrations/codex/agents';d.mkdir(parents=True);(d/'ui_researcher.toml').write_text('before')
        before=guard.candidate_identity(self.r);(d/'ui_researcher.toml').write_text('after')
        self.assertNotEqual(before,guard.candidate_identity(self.r))
    def test_symlink_evidence_rejected(self):
        (self.r/'actual').write_text('bytes')
        try:(self.r/'alias').symlink_to(self.r/'actual')
        except OSError:self.skipTest('symlinks unavailable')
        with self.assertRaises(guard.EvidenceError):guard.path_at(self.r,'alias')
        root_alias=self.r/'root-alias';root_alias.symlink_to(self.r,target_is_directory=True)
        with self.assertRaisesRegex(guard.EvidenceError,'Linked evidence root'):guard.path_at(root_alias,'actual')

class ReleaseRecordConsistencyTests(unittest.TestCase):
    """Synthetic file records test the checker only, never an actual approval."""
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.r=Path(self.temp.name).resolve()
        for name in ('VERSION','AGENTS.md','docs/MODEL.md','docs/WRITING.md'):
            self.put(name,b'mechanical-test-fixture')
        self.put('skills/ui-spec/SKILL.md',b'mechanical fixture')
        self.cells=[];self.runs=[]
        for i,(task,condition) in enumerate((('T1','A'),('T1','B'),('T1','C'),('T2','C'),('T3','C'),('T4','F-main'),('T4','F-integrator'),('T2','G-final-runtime'))):
            cell=task+'-'+condition
            self.cells.append({'id':cell,'task':task,'condition':condition,'task_sha256':guard.digest(task.encode()),
                'starter_files':{'app.txt':guard.digest(task.encode())},'method_files':{'SKILL.md':guard.digest(b'mechanical fixture')},
                'main_model':'fixture','subagent_model':'fixture','main_effort':'high','subagent_effort':'medium',
                'timeout_seconds':10,'max_subagents':2})
            events=(json.dumps({'type':'thread.started','thread_id':'TEST-DOUBLE-'+str(i)})+'\n'+json.dumps({'type':'turn.completed'})+'\n').encode()
            run={'cell_id':cell,'simulation':False,'status':'process_completed','thread_id':'TEST-DOUBLE-'+str(i),
                 'task_sha256':guard.digest(task.encode()),'events':self.put('fake/'+cell+'.jsonl',events),
                 'execution_audit':self.put('fake/'+cell+'-audit.md',b'Explicit test double, not a real audit'),
                 'product_evidence_index':self.put('fake/'+cell+'-product.json',b'{"fixture":true}')}
            self.runs.append(self.put('fake/'+cell+'-run.json',json.dumps(run).encode()))
        checks=[]
        for name in ('upstream_unit_suite','package_validation','catalog','readme_art','browser_scenarios','installer_smoke','package_build'):
            checks.append({'name':name,'status':'passed','log':self.put('fake/'+name+'.log',b'explicit mechanical test double')})
        self.decision={'schema_version':1,'baseline_commit':guard.BASE,'decision':'approve',
            'candidate_identity':guard.candidate_identity(self.r),'reviewer':'MECHANICAL TEST FIXTURE, NOT A REVIEWER',
            'reviewed_at':'fixture-not-a-date','scope':'unit test only','limitations':'all records here are synthetic test fixtures',
            'review_report':self.put('fake/review.md',b'Not an actual review'),
            'registered_plan':self.put('fake/plan.json',json.dumps({'cells':self.cells,'candidate_source_identity':guard.candidate_identity(self.r),
                     'candidate_method_files':{'SKILL.md':guard.digest(b'mechanical fixture')}}).encode()),
            'run_records':self.runs,'engineering_checks':checks,'unexecuted_cells':{}}
    def put(self,rel,raw):
        p=self.r/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        return {'path':rel,'sha256':guard.digest(raw)}
    def check(self):
        self.put(guard.DECISION,json.dumps(self.decision).encode());return guard.require_release_evidence(self.r)
    def change_run(self,index,changes):
        ref=self.runs[index];data=json.loads((self.r/ref['path']).read_bytes());data.update(changes)
        self.runs[index]=self.put(ref['path'],json.dumps(data).encode());self.decision['run_records']=self.runs
    def test_consistent_declarations_are_not_quality_authentication(self):
        result=self.check();self.assertEqual(result['status'],'declared_evidence_consistent')
        self.assertIn('does not authenticate',result['boundary'])
    def test_changed_candidate_rejected(self):
        self.put('VERSION',b'changed')
        with self.assertRaises(guard.EvidenceError):self.check()
    def test_simulation_flag_rejected(self):
        self.change_run(1,{'simulation':True})
        with self.assertRaises(guard.EvidenceError):self.check()
    def test_failed_run_rejected(self):
        self.change_run(1,{'status':'process_failed_or_incomplete'})
        with self.assertRaises(guard.EvidenceError):self.check()
    def test_duplicate_sessions_rejected(self):
        self.change_run(1,{'thread_id':'TEST-DOUBLE-0'})
        with self.assertRaises(guard.EvidenceError):self.check()
    def test_task_hash_change_rejected(self):
        self.change_run(1,{'task_sha256':'0'*64})
        with self.assertRaises(guard.EvidenceError):self.check()
    def test_unregistered_run_rejected(self):
        self.change_run(1,{'cell_id':'not-registered'})
        with self.assertRaises(guard.EvidenceError):self.check()
    def test_missing_actual_turn_event_rejected(self):
        ref=self.put('fake/absent-turn.jsonl',b'{"type":"thread.started","thread_id":"TEST-DOUBLE-1"}\n')
        self.change_run(1,{'events':ref})
        with self.assertRaises(guard.EvidenceError):self.check()
    def test_missing_required_engineering_log_rejected(self):
        self.decision['engineering_checks']=self.decision['engineering_checks'][:-1]
        with self.assertRaises(guard.EvidenceError):self.check()
    def test_unexecuted_cells_need_explicit_limitation(self):
        self.cells.append({'id':'T2-D','task':'T2','condition':'D','task_sha256':'0'*64})
        self.decision['registered_plan']=self.put('fake/plan.json',json.dumps({'cells':self.cells,'candidate_source_identity':guard.candidate_identity(self.r),
                     'candidate_method_files':{'SKILL.md':guard.digest(b'mechanical fixture')}}).encode())
        self.decision['unexecuted_cells']={'T2-D':'Unavailable model in this hypothetical fixture'}
        with self.assertRaises(guard.EvidenceError):self.check()
        self.decision['decision']='approve_limited'
        self.assertEqual(self.check()['status'],'declared_evidence_consistent')
    def test_generic_or_specialized_arm_missing_not_enough(self):
        self.decision['run_records']=self.runs[1:];self.decision['decision']='approve_limited'
        self.decision['unexecuted_cells']={self.cells[0]['id']:'omitted fixture'}
        with self.assertRaises(guard.EvidenceError):self.check()
    def test_network_mismatch_rejected(self):
        self.cells[1]['network_access']=True
        self.decision['registered_plan']=self.put('fake/plan.json',json.dumps({'cells':self.cells,'candidate_source_identity':guard.candidate_identity(self.r),
                     'candidate_method_files':{'SKILL.md':guard.digest(b'mechanical fixture')}}).encode())
        with self.assertRaisesRegex(guard.EvidenceError,'network_access'):self.check()

if __name__=='__main__':unittest.main()
