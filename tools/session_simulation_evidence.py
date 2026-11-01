#!/usr/bin/env python3
"""Consistency checks for an explicitly authorized, limited session simulation.

Actual agents execute this route. What is simulated is the unavailable native
Codex role environment. These records cannot establish native role binding,
resolved model identity, native usage, human acceptance, or visual quality.
The original schema-v1 native validator is deliberately independent of this file.
"""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import struct

ROUTE = 'owner_authorized_session_simulation'
HASH = re.compile(r'[0-9a-f]{64}\Z')
ROLES = {'ui_researcher', 'ui_integrator', 'ui_challenger', 'ui_experience_observer'}
CONDITIONS = {'A', 'B', 'C', 'D', 'E-challenger', 'E-observer',
              'F-main', 'F-integrator', 'G-final-runtime'}
REQUIRED_CHECKS = {'upstream_unit_suite', 'package_validation', 'catalog',
                   'readme_art', 'browser_scenarios', 'installer_smoke', 'package_build'}
NATIVE_CLAIMS = {'native_codex_role_binding', 'registered_native_model_trials',
                 'native_usage_metrics', 'native_cloud_campaign'}
UNAVAILABLE_METRICS = {'native_usage_tokens', 'native_billing_cost', 'main_context_pressure'}
MATCHED_KEYS = ('task_sha256', 'starter_files', 'method_files', 'main_model',
                'main_effort', 'subagent_model', 'subagent_effort',
                'timeout_seconds', 'max_subagents', 'tool_profile')


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


class SessionEvidence:
    def __init__(self, root, decision, artifact, candidate_identity, error_type, baseline):
        self.root = root
        self.decision = decision
        self.read_artifact = artifact
        self.identity = candidate_identity(root)
        self.error_type = error_type
        self.baseline = baseline
        self.agents = set()

    def fail(self, message):
        raise self.error_type('Session simulation: ' + message)

    def text(self, obj, key):
        value = obj.get(key) if isinstance(obj, dict) else None
        if not isinstance(value, str) or not value.strip():
            self.fail('Missing declaration: ' + key)
        return value

    def rows(self, obj, key, *, empty=False):
        value = obj.get(key) if isinstance(obj, dict) else None
        if not isinstance(value, list) or (not empty and not value):
            self.fail('Missing list: ' + key)
        return value

    def artifact(self, ref):
        raw = self.read_artifact(self.root, ref)
        if not raw.strip():
            self.fail('Empty evidence artifact')
        return raw

    def object(self, ref):
        try:
            value = json.loads(self.artifact(ref))
        except (ValueError, UnicodeError) as exc:
            self.fail('Unreadable JSON artifact: ' + str(exc))
        if not isinstance(value, dict):
            self.fail('Expected a JSON object artifact')
        return value

    def timestamp(self, obj, key):
        try:
            value = datetime.fromisoformat(self.text(obj, key).replace('Z', '+00:00'))
        except ValueError:
            self.fail('Invalid timestamp: ' + key)
        if value.tzinfo is None:
            self.fail('Timestamp needs a timezone: ' + key)
        return value

    def hashes(self, obj, key):
        value = obj.get(key)
        if not isinstance(value, dict) or not value or any(
            not isinstance(k, str) or not k or not isinstance(v, str) or not HASH.fullmatch(v)
            for k, v in value.items()
        ):
            self.fail('Missing or invalid identity map: ' + key)
        return value

    def export(self, ref, *, identity=None):
        if not isinstance(ref, dict) or ref.get('synthetic') is not False:
            self.fail('Tool exports must declare non-synthetic source output')
        if ref.get('export_kind') not in {'original_tool_output', 'faithful_conversation_export'}:
            self.fail('A derived summary cannot substitute for a tool output export')
        self.text(ref, 'source')
        self.text(ref, 'scope')
        raw = self.artifact(ref)
        if identity is not None:
            try:
                found = identity in raw.decode('utf-8')
            except UnicodeError:
                found = False
            if not found:
                self.fail('Declared agent identity is absent from its coordination export')
        return raw

    def participant(self, row, *, parent=None):
        agent = self.text(row, 'agent_id')
        self.text(row, 'parent_agent_id')
        if row.get('status') != 'completed':
            self.fail('An unfinished or failed agent cannot establish completed participation')
        if agent in self.agents:
            self.fail('Fresh independent agent identities are required')
        if row.get('fork_turns') != 'none':
            self.fail('Independent participants require fresh contexts (fork_turns=none)')
        if parent is not None and row.get('parent_agent_id') != parent:
            self.fail('Child parent identity differs from its actual cell agent')
        if row.get('parent_agent_id') == agent:
            self.fail('An agent cannot be its own parent')
        self.agents.add(agent)
        self.export(row.get('spawn'), identity=agent)
        self.export(row.get('completion'), identity=agent)
        self.artifact(row.get('result'))
        for ref in self.rows(row, 'tool_outputs'):
            self.export(ref)
        return agent

    def image(self, ref):
        raw = self.artifact(ref)
        if len(raw) < 33 or raw[:8] != b'\x89PNG\r\n\x1a\n' or raw[12:16] != b'IHDR':
            self.fail('Screenshot must retain actual PNG image bytes')
        if not all(struct.unpack('>II', raw[16:24])):
            self.fail('Screenshot dimensions must be nonzero')

    def views(self, rows, screenshots, viewer):
        if not isinstance(rows, list) or not rows:
            self.fail('Actual screenshot viewing exports are required')
        for view in rows:
            if not isinstance(view, dict) or view.get('viewer_agent_id') != viewer:
                self.fail('Screenshot viewing identity differs from its reviewer')
            image = view.get('screenshot')
            if not isinstance(image, dict) or (image.get('path'), image.get('sha256')) not in screenshots:
                self.fail('Viewed screenshot does not belong to the frozen product')
            self.image(image)
            self.export(view.get('view_export'))

    def product(self, ref, cell, agent):
        product = self.object(ref)
        if product.get('schema_version') != 1 or product.get('cell_id') != cell:
            self.fail('Product evidence belongs to a different cell')
        self.text(product, 'preview_command')
        self.text(product, 'capture_conditions')
        sources = self.rows(product, 'source_files')
        for source in sources:
            self.artifact(source)
        screenshots = set()
        for image in self.rows(product, 'screenshots'):
            self.image(image)
            screenshots.add((image['path'], image['sha256']))
        for log in self.rows(product, 'behavior_logs'):
            self.export(log)
        self.views(product.get('viewed_screenshots'), screenshots, agent)
        return screenshots

    def check(self):
        d = self.decision
        if d.get('acceptance_route') != ROUTE or d.get('decision') != 'approve_limited':
            self.fail('This route permits only explicitly limited owner-authorized acceptance')
        if d.get('target_version') != '1.20.0' or (self.root / 'VERSION').read_text().strip() != '1.20.0':
            self.fail('This authorization route is scoped to v1.20.0')
        if d.get('candidate_identity') != self.identity or d.get('baseline_commit') != self.baseline:
            self.fail('Current candidate or baseline differs from the reviewed source')
        for key in ('reviewer', 'scope', 'limitations'):
            self.text(d, key)
        reviewed_at = self.timestamp(d, 'reviewed_at')
        claims = d.get('native_claims')
        if not isinstance(claims, dict) or any(claims.get(key) is not False for key in NATIVE_CLAIMS):
            self.fail('Native role/model/usage/campaign claims must remain explicitly unverified')

        authority = self.object(d.get('owner_authorization'))
        if authority.get('schema_version') != 1 or authority.get('authority') != 'repository_owner':
            self.fail('Repository owner authorization is required')
        for key in ('source', 'statement', 'scope'):
            self.text(authority, key)
        actions = self.rows(authority, 'authorized_actions')
        if not {'substitute_native_validation', 'merge_pr_4', 'tag_v1.20.0', 'publish_v1.20.0'} <= set(actions):
            self.fail('Owner authorization does not cover the substitute and publication scope')
        authorized_at = self.timestamp(authority, 'authorized_at')

        registration = self.artifact(d.get('registered_plan'))
        registration_hash = sha256(registration)
        plan = self.object(d.get('registered_plan'))
        if plan.get('schema_version') != 2 or plan.get('study_kind') != ROUTE:
            self.fail('A separate frozen session simulation plan is required')
        if plan.get('candidate_source_identity') != self.identity:
            self.fail('Frozen plan identifies a different complete candidate')
        frozen_at = self.timestamp(plan, 'frozen_at')
        if authorized_at > frozen_at:
            self.fail('The substitute must be authorized before registration')
        self.text(plan, 'host_limitations')
        environment = plan.get('environment')
        self.artifact(environment)
        candidate = {p.relative_to(self.root / 'skills/ui-spec').as_posix(): sha256(p.read_bytes())
                     for p in (self.root / 'skills/ui-spec').rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts}
        if not candidate or plan.get('candidate_method_files') != candidate:
            self.fail('Complete final Skill identities differ from the candidate')
        baseline_method = self.hashes(plan, 'baseline_method_files')
        cells = {}
        for cell in self.rows(plan, 'cells'):
            name = self.text(cell, 'id')
            if name in cells or cell.get('condition') not in CONDITIONS or cell.get('task') not in {'T1', 'T2', 'T3', 'T4'}:
                self.fail('Duplicate or invalid registered cell')
            for key in ('workspace_files', 'starter_files', 'method_files'):
                self.hashes(cell, key)
            if not isinstance(cell.get('task_sha256'), str) or not HASH.fullmatch(cell['task_sha256']):
                self.fail('Missing task identity')
            for key in ('main_model', 'subagent_model', 'main_effort', 'subagent_effort', 'tool_profile'):
                self.text(cell, key)
            for key in ('timeout_seconds', 'max_subagents'):
                if type(cell.get(key)) is not int or cell[key] <= 0:
                    self.fail('Invalid registered execution bound: ' + key)
            self.artifact(cell.get('prompt'))
            for ref in self.rows(cell, 'input_artifacts'):
                self.artifact(ref)
            expected = candidate if cell['condition'].startswith(('F-', 'G-')) else baseline_method
            if cell['method_files'] != expected:
                self.fail('Condition does not use its complete frozen method')
            role_files = cell.get('role_instruction_files')
            if not isinstance(role_files, dict):
                self.fail('Role instruction identity map is required (possibly empty)')
            for role, value in role_files.items():
                if role not in ROLES or value != sha256((self.root / 'integrations/codex/agents' / (role + '.toml')).read_bytes()):
                    self.fail('Role instructions differ from the distributed adapter')
            expected_roles = ROLES if cell['condition'] not in {'A', 'B'} else set()
            if set(role_files) != expected_roles:
                self.fail('All four adapter role instructions must be frozen for adapter arms')
            cells[name] = cell

        records = self.rows(d, 'run_records')
        completed, products, parents = {}, {}, set()
        for reference in records:
            run = self.object(reference)
            name = run.get('cell_id')
            if name not in cells or name in completed:
                self.fail('Duplicate or unregistered run')
            cell = cells[name]
            if run.get('schema_version') != 2 or run.get('execution_kind') != 'real_session_agent' or run.get('simulation') is not True or run.get('status') != 'completed':
                self.fail('Only completed real session agents establish substitute execution')
            if run.get('registration_sha256') != registration_hash or run.get('candidate_source_identity') != self.identity:
                self.fail('Run belongs to a different registration or candidate')
            workspace_hash = sha256(json.dumps(cell['workspace_files'], sort_keys=True).encode())
            if run.get('input_workspace_identity') != workspace_hash or run.get('task_sha256') != cell['task_sha256'] or run.get('prompt_sha256') != cell['prompt']['sha256']:
                self.fail('Run prompt, task or input workspace identity differs from registration')
            if run.get('environment_sha256') != environment['sha256']:
                self.fail('Run environment differs from the frozen host conditions')
            start, end = self.timestamp(run, 'started_at'), self.timestamp(run, 'completed_at')
            if not frozen_at <= start <= end <= reviewed_at:
                self.fail('Execution/review chronology differs from the frozen registration')
            parent = self.text(run, 'parent_agent_id')
            parents.add(parent)
            agent = self.participant(run)
            model = run.get('model_observation')
            if not isinstance(model, dict) or model.get('main_requested') != cell['main_model'] or model.get('subagent_requested') != cell['subagent_model']:
                self.fail('Requested model identities differ from registration')
            if any(key not in model or model[key] is not None for key in ('main_resolved', 'subagent_resolved')):
                self.fail('This route retains unavailable resolved model identities as null')
            self.text(model, 'scope')
            metrics = run.get('metrics')
            if not isinstance(metrics, dict) or any(key not in metrics or metrics[key] is not None for key in UNAVAILABLE_METRICS):
                self.fail('Unavailable native metrics must be null, never inferred or zero')
            self.text(metrics, 'unavailable_reason')
            self.text(run, 'limitations')
            children = self.rows(run, 'children', empty=True)
            used = set()
            for child in children:
                self.participant(child, parent=agent)
                self.artifact(child.get('prompt'))
                role = child.get('role')
                if role not in ROLES | {'generic'}:
                    self.fail('Unknown simulated child role')
                if child.get('role_instruction_sha256') != cell['role_instruction_files'].get(role):
                    self.fail('Child role instructions differ from the frozen simulation')
                if child.get('model_requested') != cell['subagent_model'] or 'model_resolved' not in child or child['model_resolved'] is not None:
                    self.fail('Child requested model must be frozen and resolved identity unavailable')
                used.add(role)
            required = {'B': {'generic'}, 'C': {'ui_researcher'}, 'D': {'ui_researcher'},
                        'E-challenger': {'ui_researcher', 'ui_challenger'},
                        'E-observer': {'ui_researcher', 'ui_experience_observer'},
                        'F-integrator': {'ui_integrator'}}.get(cell['condition'], set())
            allowed = ROLES if cell['condition'] == 'G-final-runtime' else required
            if not required <= used or not used <= allowed:
                self.fail('Required actual child work is absent or violates the simulated condition')
            self.artifact(run.get('execution_audit'))
            products[name] = (run['product_evidence_index'], self.product(run.get('product_evidence_index'), name, agent))
            completed[name] = cell

        outstanding = set(cells) - set(completed)
        omissions = d.get('unexecuted_cells')
        if not isinstance(omissions, dict) or set(omissions) != outstanding or any(not isinstance(v, str) or not v.strip() for v in omissions.values()):
            self.fail('Every unexecuted planned cell needs its explicit limitation')
        conditions = {c['condition'].split('-')[0] for c in completed.values()}
        if not {'A', 'B', 'C', 'F', 'G'} <= conditions or {c['task'] for c in completed.values()} != {'T1', 'T2', 'T3', 'T4'}:
            self.fail('Substitute baseline, research, integration, final-runtime and four task families are incomplete')
        pairs = []
        for task in ('T1', 'T2', 'T3'):
            rows = {c['condition']: c for c in completed.values() if c['task'] == task}
            if {'A', 'B', 'C'} <= set(rows):
                pairs.append([rows[key] for key in ('A', 'B', 'C')])
        integration = {c['condition']: c for c in completed.values() if c['task'] == 'T4'}
        if not pairs or not {'F-main', 'F-integrator'} <= set(integration):
            self.fail('A matched A/B/C comparison and T4 integration pair are required')
        pairs.append([integration[key] for key in ('F-main', 'F-integrator')])
        for pair in pairs:
            for key in MATCHED_KEYS:
                if any(row.get(key) != pair[0].get(key) for row in pair[1:]):
                    self.fail('Unmatched comparison control: ' + key)

        review = self.object(d.get('review_report'))
        if review.get('schema_version') != 1 or review.get('kind') != 'independent_product_review' or review.get('outcome') != 'accept_limited':
            self.fail('Independent limited product acceptance is missing')
        reviewer = self.text(review, 'agent_id')
        if reviewer in parents or reviewer != d['reviewer']:
            self.fail('Product reviewer must be independent of the coordinator and declared consistently')
        self.participant(review)
        self.artifact(review.get('prompt'))
        if self.timestamp(review, 'reviewed_at') != reviewed_at:
            self.fail('Review timestamp differs from the release decision')
        if type(review.get('condition_blind')) is not bool:
            self.fail('Declare actual review blinding')
        for key in ('blinding_limitations', 'scope', 'limitations'):
            self.text(review, key)
        inspected = set()
        for row in self.rows(review, 'reviewed_products'):
            name = row.get('cell_id')
            if name not in products or name in inspected or row.get('product_evidence_sha256') != products[name][0]['sha256']:
                self.fail('Independent review identifies a different or duplicate frozen product')
            self.text(row, 'findings')
            self.views(row.get('viewed_screenshots'), products[name][1], reviewer)
            inspected.add(name)
        if inspected != set(completed):
            self.fail('Independent review must cover every completed comparator, including failures')
        final = review.get('final_runtime_acceptance')
        final_cells = {name for name, cell in completed.items() if cell['condition'] == 'G-final-runtime'}
        if not isinstance(final, dict) or final.get('disposition') != 'accepted_with_limits' or set(self.rows(final, 'cell_ids')) != final_cells:
            self.fail('Final-runtime products need their own scoped acceptance')
        for key in ('scope', 'limitations', 'repair_disposition'):
            self.text(final, key)
        for ref in self.rows(final, 'repair_evidence', empty=True):
            self.artifact(ref)

        checks = {}
        for row in self.rows(d, 'engineering_checks'):
            name = self.text(row, 'name')
            if name in checks or row.get('status') != 'passed' or row.get('candidate_source_identity') != self.identity:
                self.fail('Engineering checks must pass once for the exact current candidate')
            self.artifact(row.get('log'))
            checks[name] = row
        if not REQUIRED_CHECKS <= set(checks):
            self.fail('All existing publication checks remain required')
        return {'status': 'limited_session_evidence_consistent', 'acceptance_route': ROUTE,
                'reviewer': reviewer, 'actual_run_records': len(records),
                'native_campaign_completed': False, 'limitations': d['limitations'],
                'boundary': 'Artifact consistency does not authenticate every claim or certify visual quality. '
                            'Actual session agents simulate role instructions; native roles, resolved models, '
                            'usage and the original native campaign remain unverified.'}


def require_session_evidence(root: Path, decision: dict, *, artifact, candidate_identity,
                             error_type, baseline: str) -> dict:
    return SessionEvidence(root, decision, artifact, candidate_identity, error_type, baseline).check()
