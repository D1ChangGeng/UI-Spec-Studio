"""Synthetic consistency fixtures only; these are never actual Agent evidence."""
from __future__ import annotations

import base64
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('session_test_guard', ROOT / 'tools/check_adaptive_release.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

# A genuine tiny PNG encoding in an explicitly synthetic checker fixture.
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aWQAAAABJRU5ErkJggg==')
ROUTE = 'owner_authorized_session_simulation'


class SessionSimulationEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        for name in ('AGENTS.md', 'docs/MODEL.md', 'docs/WRITING.md'):
            self.put(name, b'MECHANICAL TEST FIXTURE, NOT REAL EVIDENCE')
        self.put('VERSION', b'1.20.0\n')
        self.put('skills/ui-spec/SKILL.md', b'candidate fixture')
        self.roles = {}
        for role in guard.ADAPTER_ROLES:
            ref = self.put('integrations/codex/agents/' + role + '.toml', ('# fixture ' + role).encode())
            self.roles[role] = ref['sha256']
        self.identity = guard.candidate_identity(self.root)
        self.environment = self.put('e/environment.txt', b'explicit synthetic host fixture')
        self.authorization = {'schema_version': 1, 'authority': 'repository_owner',
            'source': 'mechanical fixture, not user authorization', 'statement': 'not an actual authorization',
            'scope': 'unit test only', 'authorized_at': '2026-10-31T00:00:00Z',
            'authorized_actions': ['substitute_native_validation', 'merge_pr_4', 'tag_v1.20.0', 'publish_v1.20.0']}
        self.plan = {'schema_version': 2, 'study_kind': ROUTE, 'candidate_source_identity': self.identity,
            'frozen_at': '2026-10-31T00:01:00Z', 'host_limitations': 'all evidence is synthetic test data',
            'environment': self.environment, 'baseline_method_files': {'SKILL.md': guard.digest(b'baseline fixture')},
            'candidate_method_files': {'SKILL.md': guard.digest(b'candidate fixture')}, 'cells': []}
        for task, condition in (('T1', 'A'), ('T1', 'B'), ('T1', 'C'), ('T2', 'C'), ('T3', 'C'),
                                ('T4', 'F-main'), ('T4', 'F-integrator'), ('T2', 'G-final-runtime')):
            self.add_cell(task, condition)
        self.plan_ref = self.put_json('e/plan.json', self.plan)
        self.runs = [self.make_run(cell) for cell in self.plan['cells']]
        reviewer = self.participant('reviewer', 'COORDINATOR-TEST-DOUBLE')
        self.review = {**reviewer, 'schema_version': 1, 'kind': 'independent_product_review',
            'prompt': self.put('e/review-prompt.txt', b'synthetic review prompt'),
            'outcome': 'accept_limited', 'reviewed_at': '2026-10-31T00:04:00Z', 'condition_blind': False,
            'blinding_limitations': 'fixture is not blind or actual review', 'scope': 'checker only',
            'limitations': 'not an actual review', 'reviewed_products': [],
            'final_runtime_acceptance': {'cell_ids': ['T2-G-final-runtime'], 'disposition': 'accepted_with_limits',
                'scope': 'synthetic declarations only', 'limitations': 'no actual product acceptance',
                'repair_disposition': 'fixture has no repair', 'repair_evidence': []}}
        for run in self.runs:
            product = self.read_json(run['product_evidence_index'])
            self.review['reviewed_products'].append({'cell_id': run['cell_id'],
                'product_evidence_sha256': run['product_evidence_index']['sha256'],
                'findings': 'Negative comparator result deliberately retained in fixture.',
                'viewed_screenshots': [self.view(product['screenshots'][0], reviewer['agent_id'])]})
        checks = [{'name': name, 'status': 'passed', 'candidate_source_identity': self.identity,
                   'log': self.put('e/' + name + '.log', b'explicit mechanical check fixture')}
                  for name in ('upstream_unit_suite', 'package_validation', 'catalog', 'readme_art',
                               'browser_scenarios', 'installer_smoke', 'package_build')]
        self.decision = {'schema_version': 2, 'acceptance_route': ROUTE, 'target_version': '1.20.0',
            'decision': 'approve_limited', 'baseline_commit': guard.BASE, 'candidate_identity': self.identity,
            'reviewer': reviewer['agent_id'], 'reviewed_at': self.review['reviewed_at'], 'scope': 'checker fixture',
            'limitations': 'not actual authorization, execution or review', 'unexecuted_cells': {},
            'native_claims': {key: False for key in ('native_codex_role_binding', 'registered_native_model_trials',
                                                   'native_usage_metrics', 'native_cloud_campaign')},
            'engineering_checks': checks}

    def put(self, path, raw):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        return {'path': path, 'sha256': guard.digest(raw)}

    def put_json(self, path, value):
        return self.put(path, json.dumps(value, sort_keys=True).encode())

    def read_json(self, ref):
        return json.loads((self.root / ref['path']).read_bytes())

    def export(self, path, value):
        return {**self.put(path, value.encode()), 'source': 'EXPLICIT SYNTHETIC TEST DOUBLE',
                'scope': 'mechanical fixture, never publish as actual evidence',
                'export_kind': 'faithful_conversation_export', 'synthetic': False}

    def participant(self, name, parent):
        agent = 'TEST-DOUBLE-' + name
        return {'agent_id': agent, 'parent_agent_id': parent, 'fork_turns': 'none', 'status': 'completed',
            'spawn': self.export('e/' + name + '/spawn.txt', 'TEST DOUBLE spawn ' + agent),
            'completion': self.export('e/' + name + '/completion.txt', 'TEST DOUBLE completed ' + agent),
            'result': self.put('e/' + name + '/result.txt', b'not an actual agent result'),
            'tool_outputs': [self.export('e/' + name + '/tool.txt', 'synthetic stdout fixture')]}

    def view(self, image, agent):
        return {'viewer_agent_id': agent, 'screenshot': image,
                'view_export': self.export('e/' + agent + '-view.txt', 'TEST DOUBLE view ' + agent)}

    def add_cell(self, task, condition):
        name = task + '-' + condition
        inp = self.put('e/' + task + '/input.txt', ('fixture ' + task).encode())
        cell = {'id': name, 'task': task, 'condition': condition, 'task_sha256': inp['sha256'],
            'prompt': self.put('e/' + name + '/prompt.txt', ('fixture ' + name).encode()),
            'input_artifacts': [inp], 'workspace_files': {'INPUT.md': inp['sha256']},
            'starter_files': {'INPUT.md': inp['sha256']},
            'method_files': self.plan['candidate_method_files'] if condition.startswith(('F-', 'G-')) else self.plan['baseline_method_files'],
            'role_instruction_files': {} if condition in ('A', 'B') else self.roles.copy(),
            'main_model': 'inherited request', 'subagent_model': 'inherited request',
            'main_effort': 'inherited', 'subagent_effort': 'inherited',
            'timeout_seconds': 30, 'max_subagents': 3, 'tool_profile': 'synthetic host'}
        self.plan['cells'].append(cell)
        return cell

    def make_run(self, cell):
        name = cell['id']
        run = self.participant(name, 'COORDINATOR-TEST-DOUBLE')
        image = self.put('e/' + name + '/capture.png', PNG)
        product = {'schema_version': 1, 'cell_id': name, 'preview_command': 'synthetic fixture only',
            'capture_conditions': 'a test PNG, no browser or agent executed',
            'source_files': [self.put('e/' + name + '/app.html', b'<p>explicit test fixture</p>')],
            'screenshots': [image], 'viewed_screenshots': [self.view(image, run['agent_id'])],
            'behavior_logs': [self.export('e/' + name + '/behavior.txt', 'fixture negative behavior outcome')]}
        roles = {'B': ['generic'], 'C': ['ui_researcher'], 'D': ['ui_researcher'],
                 'E-challenger': ['ui_researcher', 'ui_challenger'],
                 'E-observer': ['ui_researcher', 'ui_experience_observer'],
                 'F-integrator': ['ui_integrator']}.get(cell['condition'], [])
        children = []
        for role in roles:
            children.append({**self.participant(name + '-' + role, run['agent_id']), 'role': role,
                'prompt': self.put('e/' + name + '-' + role + '/prompt.txt', b'child prompt fixture'),
                'role_instruction_sha256': self.roles.get(role),
                'model_requested': cell['subagent_model'], 'model_resolved': None})
        run.update({'schema_version': 2, 'execution_kind': 'real_session_agent', 'simulation': True,
            'cell_id': name, 'candidate_source_identity': self.identity, 'registration_sha256': self.plan_ref['sha256'],
            'task_sha256': cell['task_sha256'], 'prompt_sha256': cell['prompt']['sha256'],
            'input_workspace_identity': guard.digest(json.dumps(cell['workspace_files'], sort_keys=True).encode()),
            'environment_sha256': self.environment['sha256'], 'started_at': '2026-10-31T00:02:00Z',
            'completed_at': '2026-10-31T00:03:00Z', 'children': children,
            'execution_audit': self.put('e/' + name + '/audit.txt', b'not a real audit'),
            'product_evidence_index': self.put_json('e/' + name + '/product.json', product),
            'model_observation': {'main_requested': cell['main_model'], 'subagent_requested': cell['subagent_model'],
                'main_resolved': None, 'subagent_resolved': None, 'scope': 'host request fixture only'},
            'metrics': {'native_usage_tokens': None, 'native_billing_cost': None, 'main_context_pressure': None,
                'unavailable_reason': 'not provided by session tools'}, 'limitations': 'all records synthetic'})
        return run

    def refreeze(self):
        self.plan_ref = self.put_json('e/plan.json', self.plan)
        for run in self.runs:
            run['registration_sha256'] = self.plan_ref['sha256']

    def check(self):
        self.decision.update({'owner_authorization': self.put_json('e/authorization.json', self.authorization),
            'registered_plan': self.plan_ref, 'review_report': self.put_json('e/review.json', self.review),
            'run_records': [self.put_json('e/' + r['cell_id'] + '/run.json', r) for r in self.runs]})
        self.put_json(guard.DECISION, self.decision)
        return guard.require_release_evidence(self.root)

    def reject(self, pattern=None):
        with self.assertRaisesRegex(guard.EvidenceError, pattern or 'Session simulation'):
            self.check()

    def test_consistent_limited_declarations_keep_native_boundary(self):
        result = self.check()
        self.assertEqual(result['status'], 'limited_session_evidence_consistent')
        self.assertFalse(result['native_campaign_completed'])
        self.assertIn('does not authenticate', result['boundary'])

    def test_pending_unlimited_or_unknown_route_cannot_approve(self):
        for key, value in (('decision', 'pending'), ('decision', 'approve'), ('acceptance_route', 'skip_native')):
            with self.subTest(key=key, value=value):
                old = self.decision[key]
                self.decision[key] = value
                self.reject()
                self.decision[key] = old

    def test_native_claims_cannot_be_promoted_by_substitute(self):
        for key in self.decision['native_claims']:
            self.decision['native_claims'][key] = True
            self.reject('Native role')
            self.decision['native_claims'][key] = False

    def test_missing_owner_publication_scope_rejected(self):
        self.authorization['authorized_actions'].remove('publish_v1.20.0')
        self.reject('Owner authorization')

    def test_wrong_candidate_or_registration_rejected(self):
        self.runs[0]['registration_sha256'] = '0' * 64
        self.reject('registration or candidate')
        self.runs[0]['registration_sha256'] = self.plan_ref['sha256']
        self.put('VERSION', b'1.20.1')
        self.reject('v1.20.0')

    def test_input_prompt_or_environment_rebinding_rejected(self):
        for key in ('input_workspace_identity', 'task_sha256', 'prompt_sha256', 'environment_sha256'):
            old = self.runs[0][key]
            self.runs[0][key] = '0' * 64
            self.reject()
            self.runs[0][key] = old

    def test_fresh_context_and_actual_coordination_identity_required(self):
        self.runs[0]['fork_turns'] = 'all'
        self.reject('fresh contexts')
        self.runs[0]['fork_turns'] = 'none'
        self.runs[0]['agent_id'] = 'not-in-tool-output'
        self.reject('coordination export')

    def test_derived_synthetic_or_unfinished_execution_rejected(self):
        for key, value in (('export_kind', 'derived_summary'), ('synthetic', True)):
            old = self.runs[0]['tool_outputs'][0][key]
            self.runs[0]['tool_outputs'][0][key] = value
            self.reject()
            self.runs[0]['tool_outputs'][0][key] = old
        self.runs[0]['status'] = 'failed'
        self.reject('completed real session')

    def test_missing_or_wrong_required_child_rejected(self):
        child = self.runs[1]['children'].pop()
        self.reject('Required actual child')
        self.runs[1]['children'].append(child)
        child['parent_agent_id'] = 'wrong parent'
        self.reject('Child parent')

    def test_changed_role_instruction_hash_rejected(self):
        self.runs[2]['children'][0]['role_instruction_sha256'] = '0' * 64
        self.reject('Child role instructions')

    def test_unavailable_usage_and_resolved_models_cannot_be_invented(self):
        self.runs[0]['metrics']['native_usage_tokens'] = 0
        self.reject('must be null')
        self.runs[0]['metrics']['native_usage_tokens'] = None
        self.runs[0]['model_observation']['main_resolved'] = 'asserted without evidence'
        self.reject('resolved model')

    def test_missing_pixels_viewing_or_frozen_product_rejected(self):
        ref = self.runs[0]['product_evidence_index']
        product = self.read_json(ref)
        product['viewed_screenshots'] = []
        self.runs[0]['product_evidence_index'] = self.put_json(ref['path'], product)
        self.reject('viewing exports')

    def test_artifact_tampering_still_fails(self):
        ref = self.runs[0]['tool_outputs'][0]
        (self.root / ref['path']).write_bytes(b'changed')
        self.reject('Evidence identity differs')

    def test_independent_reviewer_cannot_be_coordinator_or_participant(self):
        self.review['agent_id'] = 'COORDINATOR-TEST-DOUBLE'
        self.decision['reviewer'] = self.review['agent_id']
        self.reject('independent')

    def test_review_cannot_omit_negative_comparator_or_final_scope(self):
        row = self.review['reviewed_products'].pop()
        self.reject('every completed comparator')
        self.review['reviewed_products'].append(row)
        self.review['final_runtime_acceptance']['cell_ids'] = ['T1-A']
        self.reject('Final-runtime products')

    def test_negative_comparator_findings_do_not_require_green_products(self):
        self.review['reviewed_products'][0]['findings'] = 'Observed broken retry and poor visual hierarchy; retain negative result.'
        self.assertEqual(self.check()['actual_run_records'], 8)

    def test_d_model_request_can_be_explicitly_unexecuted(self):
        cell = self.add_cell('T2', 'D')
        cell['subagent_model'] = 'gpt-6.1-terra requested, unresolved'
        self.refreeze()
        self.reject('Every unexecuted')
        self.decision['unexecuted_cells'][cell['id']] = 'Native model contrast unavailable; do not infer a winner.'
        self.assertEqual(self.check()['actual_run_records'], 8)

    def test_d_may_record_an_alternate_request_without_claiming_resolution(self):
        cell = self.add_cell('T2', 'D')
        cell['subagent_model'] = 'gpt-6.1-terra'
        self.refreeze()
        run = self.make_run(cell)
        self.runs.append(run)
        product = self.read_json(run['product_evidence_index'])
        self.review['reviewed_products'].append({'cell_id': run['cell_id'],
            'product_evidence_sha256': run['product_evidence_index']['sha256'],
            'findings': 'A different model was requested; resolved backend identity is unknown.',
            'viewed_screenshots': [self.view(product['screenshots'][0], self.review['agent_id'])]})
        result = self.check()
        self.assertEqual(result['actual_run_records'], 9)
        self.assertFalse(result['native_campaign_completed'])

    def test_session_record_cannot_masquerade_as_native_execution(self):
        self.runs[0]['simulation'] = False
        self.reject('completed real session')

    def test_exact_final_method_and_matched_controls_are_required(self):
        self.plan['cells'][0]['main_model'] = 'different request'
        self.refreeze()
        self.runs[0]['model_observation']['main_requested'] = 'different request'
        self.reject('Unmatched comparison control')

    def test_chronology_and_timezone_required(self):
        self.runs[0]['started_at'] = '2026-10-31T00:00:00Z'
        self.reject('chronology')
        self.runs[0]['started_at'] = '2026-10-31T00:02:00'
        self.reject('timezone')

    def test_all_engineering_gates_still_required(self):
        self.decision['engineering_checks'].pop()
        self.reject('publication checks')

    def test_engineering_logs_must_identify_current_candidate(self):
        self.decision['engineering_checks'][0]['candidate_source_identity'] = '0' * 64
        self.reject('exact current candidate')


if __name__ == '__main__':
    unittest.main()
