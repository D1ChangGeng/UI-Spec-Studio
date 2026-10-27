#!/usr/bin/env python3
"""Describe declared UI coverage records; query views are not project completion gates."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
from typing import Any

from structural_records import LIMITS, Observation, local_file, read_record, text, unreadable

ID = re.compile(r'^[a-z0-9][a-z0-9_-]{0,79}$')
LEGACY_VIEWS = {'draft': 'overview', 'review': 'checks', 'finish': 'connections'}
VIEWS = ('overview', 'checks', 'connections')


def _safe_file(root: Path, value: Any) -> bool:
    """Compatibility utility for safe local file existence, with no content approval."""
    try:
        local_file(root, value)
        return True
    except (OSError, ValueError, RuntimeError):
        return False


def inspect_record(data: Any, root: Path, view: str = 'overview') -> dict:
    legacy = view if view in LEGACY_VIEWS else None
    view = LEGACY_VIEWS.get(view, view)
    if view not in VIEWS:
        raise ValueError('Unknown manifest query view')
    obs = Observation(data, root)
    if not isinstance(data, dict):
        obs.note('$', 'record_shape', 'Parsed JSON root is not an object')
        return obs.report('manifest')
    if type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        obs.note('$.schema_version', 'profile_identifier', 'Declared schema_version is not the supported integer 1')
    for key in ('project', 'phase'):
        obs.field(data, key, '$')
    obs.revision(data, '$')
    if data.get('design_system_path') is not None:
        obs.file(data['design_system_path'], '$.design_system_path')
    tables = {key: obs.table(key) for key in ('viewports', 'variants', 'routes', 'journeys', 'checks')}
    views, variants, routes, journeys, checks = (tables[k][1] for k in ('viewports', 'variants', 'routes', 'journeys', 'checks'))
    for name, (rows, _) in tables.items():
        for i, row in enumerate(rows):
            if text(row.get('id')) and not ID.fullmatch(row['id']):
                obs.note(obs.row_path(row, f'$.{name}[{i}]') + '.id', 'identifier_vocabulary', 'ID does not match this manifest profile\'s lowercase identifier form')
    for i, v in enumerate(tables['viewports'][0]):
        p = obs.row_path(v, f'$.viewports[{i}]')
        for key in ('width', 'height'):
            n = obs.field(v, key, p, int)
            if type(n) is int and n < 1:
                obs.note(p + '.' + key, 'dimension_value', 'Declared CSS dimension is not positive')
    for i, v in enumerate(tables['variants'][0]):
        p = obs.row_path(v, f'$.variants[{i}]')
        for key in ('locale', 'theme'): obs.field(v, key, p)
    states: dict[str, dict] = {}
    for i, route in enumerate(tables['routes'][0]):
        p = obs.row_path(route, f'$.routes[{i}]')
        for key in ('path', 'purpose'): obs.field(route, key, p)
        declared = obs.strings(route, 'states', p)
        state_index = {x: {} for x in declared if text(x)}
        if text(route.get('id')): states[route['id']] = state_index
        if 'primary_state' in route and route['primary_state'] is not None:
            obs.ref(route['primary_state'], state_index, p + '.primary_state')
        for j, s in obs.string_items(route, 'critical_states', p):
            obs.ref(s, state_index, p + f'.critical_states[{j}]')
        obs.revision(route, p)
    for i, j in enumerate(tables['journeys'][0]):
        p = obs.row_path(j, f'$.journeys[{i}]')
        obs.refs(j, 'routes', routes, p); obs.field(j, 'outcome', p)

    def target(item: dict, p: str, kind: str | None = None) -> str | None:
        kind = kind or item.get('kind')
        if kind == 'visual':
            for key, known in (('route', routes), ('viewport', views), ('variant', variants)):
                if key in item: obs.ref(item[key], known, p + '.' + key)
                else: obs.field(item, key, p)
            r = item.get('route')
            st = states.get(r, {}) if isinstance(r, str) else {}
            if 'state' in item: obs.ref(item['state'], st, p + '.state')
            else: obs.field(item, 'state', p)
            vals = [item.get(k) for k in ('route', 'state', 'viewport', 'variant')]
            if all(isinstance(x, str) for x in vals) and vals[0] in routes and vals[1] in st and vals[2] in views and vals[3] in variants:
                return 'visual:' + ':'.join(vals)
        elif kind == 'journey':
            for key, known in (('journey', journeys), ('variant', variants)):
                if key in item: obs.ref(item[key], known, p + '.' + key)
                else: obs.field(item, key, p)
            j, v = item.get('journey'), item.get('variant')
            if isinstance(j, str) and j in journeys and isinstance(v, str) and v in variants:
                return f'journey:{j}:{v}'
        elif kind == 'integration':
            r = item.get('route')
            if r is not None: obs.ref(r, routes, p + '.route')
            else: obs.field(item, 'route', p)
            if isinstance(r, str) and r in routes: return 'integration:' + r
        else:
            obs.note(p + '.kind', 'unlisted_kind', 'No target-matching rule is defined for this declared kind')
        return None

    check_rows = []; waiver_rows = []; by_target: dict[str, list[dict]] = {}
    for i, check in enumerate(tables['checks'][0]):
        p = obs.row_path(check, f'$.checks[{i}]')
        for key in ('kind', 'status', 'reviewer', 'reason', 'outcome', 'data_mode'):
            obs.field(check, key, p)
        if 'inspected' in check: obs.field(check, 'inspected', p, bool)
        obs.revision(check, p)
        for j, file in obs.string_items(check, 'evidence', p):
            obs.file(file, p + f'.evidence[{j}]')
        t = target(check, p)
        row = {'field': p, 'id': check.get('id'), 'target': t, 'declared_status': check.get('status'), 'record': check}
        (waiver_rows if check.get('status') == 'waived' else check_rows).append(row)
        if t: by_target.setdefault(t, []).append(row)
    exceptions = obs.rows(data, 'exceptions')
    for i, exc in enumerate(exceptions):
        p = obs.row_path(exc, f'$.exceptions[{i}]')
        for key in ('target', 'reason', 'approved_by', 'reference'):
            obs.field(exc, key, p)
    approvals = obs.rows(data, 'approvals')
    for i, approval in enumerate(approvals):
        p = obs.row_path(approval, f'$.approvals[{i}]')
        obs.refs(approval, 'routes', routes, p); obs.revision(approval, p)
        for key in ('by', 'reference'): obs.field(approval, key, p)
    connections = obs.rows(data, 'connections')
    for i, connection in enumerate(connections):
        p = obs.row_path(connection, f'$.connections[{i}]')
        if 'route' in connection: obs.ref(connection['route'], routes, p + '.route')
        else: obs.field(connection, 'route', p)
        obs.refs(connection, 'check_ids', checks, p)
        for key in ('mode', 'owner', 'contract'): obs.field(connection, key, p)

    critical_targets: dict[str, tuple[str, str, str]] = {}

    def matching(t: str) -> dict:
        # Match addresses only; do not examine pass/fail, evidence, reviewer, or revision.
        candidates = by_target.get(t, [])
        if t in critical_targets:
            r, state, variant = critical_targets[t]
            candidates = [row for rows in by_target.values() for row in rows
                          if row['record'].get('kind') == 'visual'
                          and row['record'].get('route') == r and row['record'].get('state') == state
                          and row['record'].get('variant') == variant]
        ex = [obs.row_path(e, f'$.exceptions[{i}]') for i, e in enumerate(exceptions) if e.get('target') == t]
        return {'target': t, 'check_record_fields': [c['field'] for c in candidates if c['declared_status'] != 'waived'],
                'waived_check_record_fields': [c['field'] for c in candidates if c['declared_status'] == 'waived'],
                'exception_record_fields': ex}

    declared = []
    for i, requirement in enumerate(obs.rows(data, 'requirements')):
        p = obs.row_path(requirement, f'$.requirements[{i}]')
        t = target(requirement, p, requirement.get('kind', 'visual'))
        declared.append({'field': p, 'declared_target': requirement,
                         **(matching(t) if t else {'target': None, 'check_record_fields': [],
                                                   'waived_check_record_fields': [], 'exception_record_fields': []})})
    # A projection of named inventory, never mandatory completion rules.
    combinations = set()
    for r, route in routes.items():
        st = route.get('primary_state')
        if isinstance(st, str) and st in states.get(r, {}):
            combinations.update(f'visual:{r}:{st}:{v}:{a}' for v in views for a in variants)
        for st in route.get('critical_states', []) if isinstance(route.get('critical_states'), list) else []:
            if isinstance(st, str) and st in states.get(r, {}):
                for a in variants:
                    address = f'critical:{r}:{st}:{a}'
                    combinations.add(address)
                    critical_targets[address] = (r, st, a)
        combinations.add(f'integration:{r}')
    combinations.update(f'journey:{j}:{v}' for j in journeys for v in variants)
    inventory = [matching(t) for t in sorted(combinations)]
    def unlisted(row: dict) -> bool:
        return not (row['check_record_fields'] or row['waived_check_record_fields'] or row['exception_record_fields'])
    projection = {
        'overview': {k: tables[k][0] for k in ('viewports', 'variants', 'routes', 'journeys')},
        'checks': {'declared_checks': tables['checks'][0], 'declared_exceptions': exceptions},
        'connections': {'declared_connections': connections, 'declared_approvals': approvals},
    }[view]
    result = obs.report('manifest')
    result.update(query_view=view,
                  query_compatibility={'legacy_mode': legacy, 'meaning': 'Display alias only; no stage or completion decision'},
                  counts={k: len(rows) for k, (rows, _) in tables.items()},
                  declared_check_records=check_rows, declared_waived_check_records=waiver_rows,
                  declared_exceptions=exceptions, declared_approvals=approvals,
                  declared_connections=connections, declared_item_records=declared,
                  unlisted_declared_items=[r for r in declared if r['target'] and unlisted(r)],
                  inventory_combinations={'basis': 'Projection of declared primary/critical states, viewports, variants, journeys and routes; not task requirements.',
                                          'task_applicability': 'not_assessed', 'items': inventory,
                                          'unlisted': [r for r in inventory if unlisted(r)]},
                  view=copy.deepcopy(projection))
    return result


def validate(data: Any, root: Path, mode: str = 'draft') -> dict:
    """Legacy import name; mode is a display alias and no approval/gating result is returned."""
    return inspect_record(data, root, mode)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', required=True, type=Path)
    parser.add_argument('--manifest', default='.ui-spec/manifest.json')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--view', choices=VIEWS)
    group.add_argument('--mode', choices=tuple(LEGACY_VIEWS), help='Legacy alias for a query view, not a completion stage')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        root = args.project_root.resolve(strict=True)
        data = read_record(root, args.manifest)
        result = inspect_record(data, root, args.view or args.mode or 'overview')
        result['record_source']['path'] = args.manifest
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print('Structure inspection completed')
            print('record_readability: readable')
            print(f"query_view: {result.get('query_view', args.view or args.mode or 'overview')}")
            for entry in result['structural_findings']:
                print(f"{entry['path']}: {entry['code']} — {entry['message']}")
            print(json.dumps({k: result.get(k, []) for k in ('declared_item_records', 'unlisted_declared_items')}, ensure_ascii=False))
            print('\n'.join(LIMITS))
        return 0
    except (OSError, ValueError, TypeError, RuntimeError, RecursionError) as exc:
        print(json.dumps(unreadable(args.manifest, exc), ensure_ascii=False, indent=2))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
