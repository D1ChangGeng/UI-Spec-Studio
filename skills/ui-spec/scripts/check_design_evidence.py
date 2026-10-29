#!/usr/bin/env python3
"""Inspect represented design structure; leave applicability, evidence and action judgments to the Agent."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys
from typing import Any

from structural_records import LIMITS, Observation, local_file, read_record, text, unreadable

FORMAT = "ui-spec-evidence/1"
LEVELS = tuple(f"L{i}" for i in range(6))
VOCABULARY = Path(__file__).resolve().parents[1] / "assets/design-coverage-categories.json"


def _rows(data: Any, key: str) -> list[dict]:
    value = data.get(key, []) if isinstance(data, dict) else []
    return [x for x in value if isinstance(x, dict)] if isinstance(value, list) else []


def _ids(value: Any) -> set[str]:
    return {x for x in value if text(x)} if isinstance(value, list) else set()


def inspect_spec_records(obs: Observation, data: dict, objects: dict, decisions: dict) -> dict:
    """Describe optional increment declarations without assigning or judging work."""
    if 'product_context' in data:
        context = obs.field(data, 'product_context', '$', dict)
        if isinstance(context, dict):
            for key in ('overall_goal', 'current_ui'):
                if key in context:
                    obs.field(context, key, '$.product_context')
    tables = {key: obs.table(key) for key in ('candidate_specs', 'formal_specs') if key in data}
    # One reference namespace; a repeated ID remains ambiguous across the two lists.
    all_specs: dict[str, dict] = {}
    ambiguous: set[str] = set()
    for key, (rows, index) in tables.items():
        ambiguous.update(obs.ambiguous.get(id(index), set()))
        for sid, row in index.items():
            if sid in all_specs:
                ambiguous.add(sid)
                obs.note(obs.row_path(row, '$.' + key) + '.id', 'duplicate_id',
                         f'ID {sid!r} is declared in both candidate and formal records; lookup is ambiguous')
            else:
                all_specs[sid] = row
    obs.ambiguous[id(all_specs)] = ambiguous
    for key, (rows, _index) in tables.items():
        for i, row in enumerate(rows):
            p = obs.row_path(row, f'$.{key}[{i}]')
            for name in ('purpose', 'boundary_reason', 'relationship'):
                if name in row:
                    obs.field(row, name, p)
            if 'quality_goals' in row:
                obs.strings(row, 'quality_goals', p)
            for name in ('objects', 'research_objects', 'implementation_objects', 'regression_objects'):
                if name in row:
                    obs.refs(row, name, objects, p)
            if 'decisions' in row:
                obs.refs(row, 'decisions', decisions, p)
            if 'related_specs' in row:
                obs.refs(row, 'related_specs', all_specs, p)
            obs.revision(row, p)
    return {'candidate_specs': _rows(data, 'candidate_specs'),
            'formal_specs': _rows(data, 'formal_specs'),
            'product_context': data.get('product_context'),
            'basis': 'Supplied declarations and literal references only; candidates are not formal increments.',
            'scope_judgment': 'not_assessed',
            'limits': 'No splitting, merging, sequencing, quality assessment or completion decision is performed.'}


def relation_candidates(data: Any, changed: list[str]) -> dict:
    """Traverse only the declared links, cycle-safely; make no applicability decision."""
    objects = {o['id']: o for o in _rows(data, 'objects') if text(o.get('id'))}
    known_changed = {x for x in changed if x in objects}
    related = set(known_changed)
    edges = [(oid, o['parent']) for oid, o in objects.items()
             if isinstance(o.get('parent'), str) and o['parent'] in objects]
    for r in _rows(data, 'relations'):
        a, b, kind = r.get('from'), r.get('to'), r.get('type')
        if not isinstance(a, str) or not isinstance(b, str) or a not in objects or b not in objects:
            continue
        if kind in ('affects', 'appears_in'):
            edges.append((a, b))
        elif kind == 'depends_on':
            edges.append((b, a))
        elif kind == 'shares':
            edges.extend(((a, b), (b, a)))
    while True:
        expanded = related | {b for a, b in edges if a in related}
        if expanded == related:
            break
        related = expanded
    return {'changed_ids': list(changed), 'unresolved_changed_ids': sorted(set(changed) - objects.keys()),
            'object_ids': sorted(related),
            'decision_ids': [d.get('id') for d in _rows(data, 'decisions') if _ids(d.get('objects')) & related],
            'basis': 'Declared containment, depends_on, affects, shares and appears_in only; temporal order is not traversed.',
            'task_applicability': 'not_assessed',
            'limits': 'Listed objects are possible relation-review candidates, not defects or required actions; unlisted effects may exist.'}


def project_view(data: Any, view: str, changed: list[str] | None = None) -> dict:
    """Project current records; historical archives do not silently become current decisions."""
    if view not in {'overview', 'detail', 'execution'}:
        raise ValueError('Unknown view')
    decisions = _rows(data, 'decisions')
    keys = {'overview': ('id', 'objects', 'purpose', 'question', 'gaps', 'next_action'),
            'execution': ('id', 'objects', 'implementation', 'checks', 'approval', 'gaps', 'next_action')}
    if view == 'detail':
        result = {key: _rows(data, key) for key in ('objects', 'decisions', 'evidence', 'conditions', 'relations')}
    else:
        result = {'decisions': [{k: d[k] for k in keys[view] if k in d} for d in decisions]}
        if view == 'overview':
            result.update(objects=_rows(data, 'objects'), coverage_challenges=_rows(data, 'coverage_challenges'))
    result['record_layer'] = 'current_model'
    result['meaningful_revisions'] = _rows(data, 'revisions')
    result['evidence_archive_references'] = _rows(data, 'archive')
    # The three views share identities and declarations, not separately maintained plans.
    for key in ('product_context', 'candidate_specs', 'formal_specs'):
        if isinstance(data, dict) and key in data:
            result[key] = data[key]
    result['declared_relation_review_candidates'] = relation_candidates(data, changed or [])
    return copy.deepcopy(result)


def inspect_record(data: Any, project_root: Path, *, view: str = 'overview',
                   changed: list[str] | None = None) -> dict:
    obs = Observation(data, project_root)
    if not isinstance(data, dict):
        obs.note('$', 'record_shape', 'Parsed JSON root is not an object')
        return obs.report('design_evidence')
    obs.field(data, 'format', '$')
    if data.get('format') != FORMAT:
        obs.note('$.format', 'profile_identifier', f'Declared format is not the supported {FORMAT!r} profile')
    obs.revision(data, '$')
    tables = {key: obs.table(key) for key in ('objects', 'conditions', 'evidence', 'decisions')}
    objects, conditions, evidence, decisions = (tables[k][1] for k in ('objects', 'conditions', 'evidence', 'decisions'))
    spec_records = inspect_spec_records(obs, data, objects, decisions)
    for i, obj in enumerate(tables['objects'][0]):
        path = obs.row_path(obj, f'$.objects[{i}]')
        for key in ('level', 'title'):
            obs.field(obj, key, path)
        if 'level' in obj and obj['level'] not in LEVELS:
            obs.note(path + '.level', 'unlisted_level', 'Declared level is outside the L0–L5 vocabulary')
        if 'parent' in obj and obj['parent'] is not None:
            obs.ref(obj['parent'], objects, path + '.parent')
        obs.strings(obj, 'categories', path)
        obs.revision(obj, path)
    # A cycle is a graph fact, not a workflow blockade.
    for oid, obj in objects.items():
        seen = {oid}; parent = obj.get('parent')
        while isinstance(parent, str) and parent in objects:
            if parent in seen:
                obs.note(obs.row_path(obj, f'objects[{oid}]') + '.parent', 'containment_cycle', 'Declared containment returns to a previously visited object')
                break
            seen.add(parent); parent = objects[parent].get('parent')
    for i, item in enumerate(tables['conditions'][0]):
        p = obs.row_path(item, f'$.conditions[{i}]')
        obs.field(item, 'description', p)
        obs.revision(item, p)
    relations = obs.rows(data, 'relations')
    for i, row in enumerate(relations):
        p = obs.row_path(row, f'$.relations[{i}]')
        obs.field(row, 'type', p)
        for key in ('from', 'to'):
            if key in row: obs.ref(row[key], objects, p + '.' + key)
            else: obs.field(row, key, p)
    for i, item in enumerate(tables['evidence'][0]):
        p = obs.row_path(item, f'$.evidence[{i}]')
        for key in ('kind', 'role', 'status', 'observation', 'window', 'method'):
            obs.field(item, key, p)
        obs.refs(item, 'objects', objects, p); obs.refs(item, 'conditions', conditions, p)
        obs.field(item, 'location', p, dict); obs.location(item.get('location'), p + '.location')
        if 'sha256' in item: obs.field(item, 'sha256', p)  # Declaration only; independent tool compares bytes.
        obs.revision(item, p)

    check_records: list[dict] = []; exception_records: list[dict] = []
    for i, decision in enumerate(tables['decisions'][0]):
        p = obs.row_path(decision, f'$.decisions[{i}]')
        d_objects = obs.refs(decision, 'objects', objects, p)
        obs.refs(decision, 'evidence', evidence, p)
        for key in ('purpose', 'question', 'judgment', 'choice'):
            obs.field(decision, key, p)
        obs.revision(decision, p); obs.action(decision, p)
        action = decision.get('next_action')
        if isinstance(action, dict):
            obs.field(action, 'kind', p + '.next_action')
            obs.field(action, 'reason', p + '.next_action')
            obs.refs(action, 'objects', objects, p + '.next_action')
        for key in ('comparison', 'implementation', 'approval'):
            value = obs.field(decision, key, p, dict)
            if not isinstance(value, dict): continue
            at = p + '.' + key
            obs.revision(value, at)
            if key == 'comparison':
                obs.field(value, 'state', at); obs.strings(value, 'alternatives', at)
                obs.refs(value, 'evidence', evidence, at); obs.field(value, 'rationale', at)
            elif key == 'implementation':
                obs.field(value, 'state', at); obs.refs(value, 'evidence', evidence, at)
                for n, path in obs.string_items(value, 'paths', at):
                    obs.file(path, at + f'.paths[{n}]')
            else:
                for field in ('status', 'source', 'scope'): obs.field(value, field, at)
        for j, check in enumerate(obs.rows(decision, 'checks', p)):
            cp = obs.row_path(check, p + f'.checks[{j}]')
            for key in ('domain', 'status', 'finding', 'role'): obs.field(check, key, cp)
            os = obs.refs(check, 'objects', objects, cp) if 'objects' in check else d_objects
            cs = obs.refs(check, 'conditions', conditions, cp)
            obs.refs(check, 'evidence', evidence, cp); obs.revision(check, cp)
            row = {'field': cp, 'decision_id': decision.get('id'), 'objects': os, 'conditions': cs,
                   'domain': check.get('domain'), 'declared_status': check.get('status'),
                   'declared_role': check.get('role'), 'matching_role': check.get('role', 'integrated'),
                   'record': check}
            if check.get('status') == 'waived': exception_records.append(row)
            else: check_records.append(row)
            if 'exception' in check:
                ex = obs.field(check, 'exception', cp, dict)
                if isinstance(ex, dict):
                    for key in ('by', 'source', 'reason', 'scope'): obs.field(ex, key, cp + '.exception')
        seen_gaps = set()
        for j, gap in enumerate(obs.rows(decision, 'gaps', p)):
            gp = obs.row_path(gap, p + f'.gaps[{j}]')
            gid = obs.field(gap, 'id', gp, identity=True)
            if text(gid):
                if gid in seen_gaps: obs.note(gp + '.id', 'duplicate_id', 'Gap identifier is repeated within this decision')
                seen_gaps.add(gid)
            for key in ('status', 'impact', 'question'): obs.field(gap, key, gp)
            obs.refs(gap, 'objects', objects, gp); obs.refs(gap, 'resolution_evidence', evidence, gp)
            obs.action(gap, gp)
            if 'exception' in gap:
                obs.field(gap, 'exception', gp, dict)
    for i, row in enumerate(obs.rows(data, 'coverage_challenges')):
        p = obs.row_path(row, f'$.coverage_challenges[{i}]')
        for key in ('discovery', 'disposition', 'reason'): obs.field(row, key, p)
        obs.refs(row, 'objects', objects, p); obs.refs(row, 'evidence', evidence, p); obs.action(row, p)

    declared_items = []
    for i, req in enumerate(obs.rows(data, 'required_checks')):
        p = obs.row_path(req, f'$.required_checks[{i}]')
        for key, known in (('object', objects), ('condition', conditions)):
            if key in req: obs.ref(req[key], known, p + '.' + key)
            else: obs.field(req, key, p)
        for key in ('domain', 'role'): obs.field(req, key, p)
        def matches(c: dict) -> bool:
            return (isinstance(req.get('object'), str) and req['object'] in c['objects']
                    and isinstance(req.get('condition'), str) and req['condition'] in c['conditions']
                    and c['domain'] == req.get('domain') and c['matching_role'] == req.get('role', 'integrated'))
        declared_items.append({'field': p, 'declared_target': req,
                               'check_record_fields': [c['field'] for c in check_records if matches(c)],
                               'exception_record_fields': [c['field'] for c in exception_records if matches(c)],
                               'basis': 'Literal object/condition/domain/role match only; status and revision do not determine sufficiency.'})
    for i, rev in enumerate(obs.rows(data, 'revisions')):
        p = obs.row_path(rev, f'$.revisions[{i}]')
        for key in ('id', 'summary', 'reason', 'current_judgment'): obs.field(rev, key, p)
        obs.refs(rev, 'objects', objects, p); obs.refs(rev, 'evidence', evidence, p)
        obs.strings(rev, 'historical_objects', p)  # Historical IDs are not current reference claims.
        obs.location(rev.get('previous'), p + '.previous'); obs.revision(rev, p)
    for i, archive in enumerate(obs.rows(data, 'archive')):
        p = obs.row_path(archive, f'$.archive[{i}]')
        for key in ('id', 'description'): obs.field(archive, key, p)
        obs.location(archive.get('location'), p + '.location'); obs.revision(archive, p)

    by_level = {level: [o.get('id') for o in tables['objects'][0] if o.get('level') == level] for level in LEVELS}
    tagged = {tag for obj in tables['objects'][0] for tag in _ids(obj.get('categories'))}
    try:
        vocab = json.loads(VOCABULARY.read_text(encoding='utf-8'))
        categories = vocab['categories']
        vocabulary_source = vocab['version']
    except (OSError, ValueError, KeyError, TypeError) as exc:
        categories = []; vocabulary_source = None
        obs.note('bundled_vocabulary', 'vocabulary_read_problem', str(exc))
    hints = [{'category': row['id'], 'description': row['description'],
              'basis': 'No explicit matching category tag on current objects; prose and archived material were not classified.',
              'task_applicability': 'not_assessed'} for row in categories if row['id'] not in tagged]
    result = obs.report('design_evidence')
    result.update(object_inventory={'by_level': by_level, 'declared_categories': sorted(tagged),
                                    'unrepresented_levels': [x for x, rows in by_level.items() if not rows]},
                  counts={k: len(tables[k][0]) for k in tables},
                  declared_relations=relations, declared_check_records=check_records,
                  declared_exception_records=exception_records, declared_item_records=declared_items,
                  unlisted_declared_items=[r for r in declared_items if not r['check_record_fields'] and not r['exception_record_fields']],
                  candidate_unrepresented_categories=hints, coverage_vocabulary=vocabulary_source,
                  declared_spec_records=spec_records,
                  view=project_view(data, view, changed))
    return result


def validate(data: Any, project_root: Path) -> dict:
    """Import-compatible name; returns the neutral inspection report, never a pass flag."""
    return inspect_record(data, project_root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--record', default='.ui-spec/design-evidence.json')
    parser.add_argument('--view', choices=('overview', 'detail', 'execution'), default='overview')
    parser.add_argument('--changed', action='append', default=[], help='Object ID used only for declared-relation lookup')
    args = parser.parse_args()
    try:
        root = args.project_root.resolve(strict=True)
        data = read_record(root, args.record)
        result = inspect_record(data, root, view=args.view, changed=args.changed)
        result['record_source']['path'] = args.record
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0  # Inspection ran, even with findings; never a design/phase gate.
    except (OSError, ValueError, TypeError, RuntimeError, RecursionError) as exc:
        print(json.dumps(unreadable(args.record, exc), ensure_ascii=False, indent=2))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
