"""Protocol/state/safety mechanics only. No model calls or study participants."""
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
backend=load('appserver_test_subject',ROOT/'tools/adaptive_appserver.py')
runner=load('appserver_runner_subject',ROOT/'tools/run_adaptive_research.py')
fixtures=load('appserver_test_fixtures',ROOT/'tests/adaptive_rpc_fixture.py')

class NativeEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.row={'condition':'C','main_model':'fixture-main','subagent_model':'fixture-child',
                  'transport':'app-server','profile_mode':'inherited','session_persistence':'ephemeral','network_access':False}
        self.requests,self.wire=fixtures.transcript(self.row)
    def inspect(self):return backend.inspect_evidence(self.requests,self.wire,self.row)
    def test_observed_role_lineage_tool_and_usage_are_required_together(self):
        result=self.inspect();self.assertEqual(result['evidence_errors'],[])
        self.assertEqual(set(result['native_roles'].values()),{'ui_researcher'})
        self.assertIsNone(result['native_model_metadata']['TEST-DOUBLE-parent-child-0']['per_response_model'])
    def test_role_self_report_does_not_replace_native_binding(self):
        for event in self.wire:
            thread=event.get('result',{}).get('thread',{})
            if thread.get('parentThreadId'):
                thread['agentRole']='default';thread['source']['subAgent']['thread_spawn']['agent_role']='default'
        self.assertTrue(any('intervention' in e for e in self.inspect()['evidence_errors']))
    def test_returned_prose_without_child_tool_is_not_participation(self):
        self.wire=[e for e in self.wire if e.get('params',{}).get('item',{}).get('type')!='commandExecution']
        self.assertTrue(any('work-tool' in e for e in self.inspect()['evidence_errors']))
    def test_failed_or_nonterminal_child_tools_do_not_complete_intervention(self):
        for status,code in [('failed',127),('inProgress',None)]:
            with self.subTest(status=status):
                requests,wire=fixtures.transcript(self.row)
                for event in wire:
                    item=event.get('params',{}).get('item',{})
                    if item.get('type')=='commandExecution':item.update(status=status,exitCode=code)
                self.assertTrue(backend.inspect_evidence(requests,wire,self.row)['evidence_errors'])
    def test_completed_dynamic_call_with_false_success_is_not_work_evidence(self):
        for event in self.wire:
            item=event.get('params',{}).get('item',{})
            if item.get('type')=='commandExecution':item.update(type='dynamicToolCall',success=False)
        self.assertTrue(any('work-tool' in e for e in self.inspect()['evidence_errors']))
    def test_a_later_child_turn_needs_completion_in_both_persistence_modes(self):
        for persistence in ('ephemeral','persistent'):
            row=dict(self.row,session_persistence=persistence);requests,wire=fixtures.transcript(row)
            wire.append({'method':'turn/started','params':{'threadId':'TEST-DOUBLE-parent-child-0','turn':{'id':'second','status':'inProgress'}}})
            self.assertTrue(any('unfinished' in e for e in backend.inspect_evidence(requests,wire,row)['evidence_errors']))
    def test_generic_condition_requires_observed_default_role(self):
        self.row['condition']='B'
        self.assertTrue(any('default-role' in e for e in self.inspect()['evidence_errors']))
        self.requests,self.wire=fixtures.transcript(self.row)
        self.assertEqual(self.inspect()['evidence_errors'],[])
    def test_explicit_null_default_binding_is_not_missing_role_metadata(self):
        self.row.update(condition='B',generic_role_binding=None)
        self.requests,self.wire=fixtures.transcript(self.row)
        self.assertEqual(self.inspect()['evidence_errors'],[])
        for event in self.wire:
            thread=event.get('result',{}).get('thread',{})
            if thread.get('parentThreadId'):thread.pop('agentRole')
        self.assertTrue(any('absent' in e for e in self.inspect()['evidence_errors']))
    def test_auxiliary_agent_is_forbidden_in_main_only_arm(self):
        self.row['condition']='A';self.assertTrue(any('main-agent-only' in e for e in self.inspect()['evidence_errors']))
    def test_missing_tool_end_and_missing_child_terminal_do_not_pass(self):
        for method in ('item/completed','turn/completed'):
            with self.subTest(method=method):
                requests,wire=fixtures.transcript(self.row)
                wire=[e for e in wire if not (e.get('method')==method and e.get('params',{}).get('threadId')=='TEST-DOUBLE-parent-child-0')]
                self.assertTrue(backend.inspect_evidence(requests,wire,self.row)['evidence_errors'])
    def test_failed_parent_cannot_be_counted_as_completed(self):
        for e in self.wire:
            if e.get('method')=='turn/completed' and e['params']['threadId']=='TEST-DOUBLE-parent':e['params']['turn']['status']='failed'
        self.assertTrue(any('turn failed' in e for e in self.inspect()['evidence_errors']))
    def test_wrong_model_and_missing_token_events_fail_closed(self):
        for e in self.wire:
            if e.get('result',{}).get('thread',{}).get('parentThreadId'):e['result']['thread']['model']=None
        self.wire=[e for e in self.wire if e.get('method')!='thread/tokenUsage/updated']
        errors=self.inspect()['evidence_errors'];self.assertTrue(any('model' in e for e in errors));self.assertTrue(any('usage' in e for e in errors))
    def test_wrong_native_network_and_blind_approval_are_rejected(self):
        for e in self.wire:
            if 'sandbox' in e.get('result',{}):e['result']['sandbox']['networkAccess']=True
        self.requests.append({'id':'server-fixture','result':{'decision':'accept'}})
        errors=self.inspect()['evidence_errors'];self.assertTrue(any('network' in e for e in errors));self.assertTrue(any('approval' in e for e in errors))
    def test_denied_native_tool_and_reading_another_session_are_rejected(self):
        self.requests.append({'id':999,'method':'thread/read','params':{'threadId':'UNRELATED-TEST-SESSION'}})
        for e in self.wire:
            item=e.get('params',{}).get('item',{})
            if item.get('type')=='commandExecution':item['status']='declined'
        errors=self.inspect()['evidence_errors'];self.assertTrue(any('outside' in e for e in errors));self.assertTrue(any('denied' in e for e in errors))
    def test_wire_hash_index_and_original_format_are_checked(self):
        run={'cell_id':'FIXTURE','registration_sha256':'a'*64,'input_workspace_identity':'b'*64,'task_sha256':'c'*64,
             'thread_id':'TEST-DOUBLE-parent','events':{'format':'codex-app-server-jsonrpc','derived':False}}
        files=fixtures.manifest_files(self.row,run)
        manifest={'schema_version':1,'transport':'app-server','derived':False,'internal_raw_events':False,
                  'root_thread_id':run['thread_id'],'profile_mode':'inherited','session_persistence':'ephemeral','network_access':False,
                  'study_identity':{k:run[k] for k in ('cell_id','registration_sha256','input_workspace_identity','task_sha256')},
                  'files':{k:{'path':k} for k in files}}
        load_file=lambda reference:files[reference['path']]
        backend.verify_manifest(manifest,load_file,self.row,run,files['wire.jsonl'])
        files['wire.jsonl']=files['wire.jsonl'].replace(b'fixture-main',b'tampered-main')
        with self.assertRaisesRegex(backend.AppServerError,'original-line index'):
            backend.verify_manifest(manifest,load_file,self.row,run,files['wire.jsonl'])

class NativeTransportSafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name).resolve()
    def client(self,message):
        process=SimpleNamespace(stdout=io.BytesIO((json.dumps(message)+'\n').encode()),stdin=io.BytesIO())
        client=backend.Client(process,self.root,time.monotonic()+3,'ephemeral');self.addCleanup(client.close);return client,process
    def test_unresolved_approval_is_cancelled_without_grant(self):
        client,process=self.client({'id':'approval-fixture','method':'item/commandExecution/requestApproval','params':{'threadId':'fixture'}})
        with self.assertRaises(backend.ApprovalBlocked):client.pump()
        response=json.loads(process.stdin.getvalue());self.assertEqual(response['result']['decision'],'cancel')
        self.assertTrue(client.approval_blocked)
    def test_reasoning_is_not_written_to_wire_or_projection(self):
        marker='SYNTHETIC PRIVATE REASONING FIXTURE'
        client,_=self.client({'method':'item/completed','params':{'item':{'id':'fixture','type':'reasoning','content':[marker]}}})
        client.pump()
        for name in ('wire.jsonl','wire-index.jsonl','projections.jsonl'):
            self.assertNotIn(marker,(self.root/name).read_text())
        self.assertEqual((self.root/'wire.jsonl').read_bytes(),b'')
    def test_malformed_wire_is_quarantined_counted_and_hashed(self):
        raw=b'explicit malformed protocol fixture\n'
        process=SimpleNamespace(stdout=io.BytesIO(raw),stdin=io.BytesIO())
        client=backend.Client(process,self.root,time.monotonic()+3,'ephemeral');self.addCleanup(client.close)
        with self.assertRaisesRegex(backend.AppServerError,'malformed'):client.pump()
        self.assertEqual(client.malformed_lines,1)
        self.assertEqual((self.root/'private-unparsed-wire.bin').read_bytes(),raw)
        index=json.loads((self.root/'wire-index.jsonl').read_text())
        self.assertEqual(index['sha256'],backend.digest(raw));self.assertEqual((self.root/'wire.jsonl').read_bytes(),b'')
    def test_appserver_command_preserves_authorization_profile_and_unicode(self):
        row={'transport':'app-server','condition':'A','subagents_enabled':False,'max_subagents':2,
             'main_model':'fixture-main','subagent_model':'fixture-child','main_effort':'low','subagent_effort':'low',
             'network_access':True,'installed_role_names':[]}
        command=runner.command('codex',row,self.root/'work-🧪',inherit_profile=True,runtime_dir=self.root/'runtime-🧪')
        self.assertEqual(command[:3],['codex','app-server','--stdio'])
        self.assertIn('approval_policy="on-request"',command);self.assertIn('approvals_reviewer="auto_review"',command)
        self.assertIn('sandbox_workspace_write.network_access=true',command)
        self.assertNotIn('--ignore-user-config',command);self.assertNotIn('--ephemeral',command)
        self.assertFalse(any('CODEX_HOME=' in part or 'never' in part or 'dangerously' in part for part in command))
    @unittest.skipIf(os.name=='nt','POSIX process group mechanical cleanup')
    def test_timeout_reaps_real_silent_test_process_and_preserves_failure(self):
        # A Python sleep is a process fixture, never an Agent or model request.
        row={'condition':'A','main_model':'fixture','subagent_model':'fixture','main_effort':'low',
             'timeout_seconds':1,'profile_mode':'inherited','network_access':False,'session_persistence':'ephemeral'}
        before=dict(os.environ)
        result=backend.execute(command=[sys.executable,'-c','import time;time.sleep(30)'],row=row,
            workspace=self.root,out=self.root/'attempt',env=os.environ.copy(),stop_process=runner.stop_owned_process,prompt='mechanical fixture')
        self.assertEqual(result['status'],'timed_out');self.assertTrue(result['process_cleanup']['direct_child_reaped'])
        self.assertTrue((self.root/'attempt/evidence-manifest.json').is_file());self.assertEqual(dict(os.environ),before)
    @unittest.skipIf(os.name=='nt','POSIX process group mechanical cleanup')
    def test_keyboard_interrupt_records_cancelled_attempt_before_propagation(self):
        row={'condition':'A','main_model':'fixture','subagent_model':'fixture','main_effort':'low',
             'timeout_seconds':3,'profile_mode':'inherited','network_access':False,'session_persistence':'ephemeral'}
        cancelled=[]
        with patch.object(backend.Client,'request',side_effect=KeyboardInterrupt):
            result=backend.execute(command=[sys.executable,'-c','import time;time.sleep(30)'],row=row,
                workspace=self.root,out=self.root/'attempt',env=os.environ.copy(),stop_process=runner.stop_owned_process,
                prompt='mechanical fixture',on_cancel=lambda:cancelled.append(True))
        self.assertEqual(result['status'],'interrupted');self.assertTrue(result['interrupted']);self.assertTrue(cancelled)
        self.assertTrue(result['process_cleanup']['direct_child_reaped'])

if __name__=='__main__':unittest.main()
