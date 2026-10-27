#!/usr/bin/env python3
"""Find documented resource leads in the bundled catalog; local and read-only."""
from __future__ import annotations
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urlsplit

CATALOG = Path(__file__).resolve().parents[1] / 'assets/resource-catalog.json'
LIMITS = ('Results are documented discovery leads, not installation instructions or '
          'project acceptance. Current source, exact-item fit and real integration are not assessed.')
ID = re.compile(r'^[a-z0-9][a-z0-9-]*$')


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(_text(x) for x in value)


def validate_catalog(data: Any) -> list[str]:
    """Validate data integrity only; network and visual assertions stay external."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ['Catalog must be a JSON object']
    if type(data.get('schema_version')) is not int or data.get('schema_version') != 1:
        errors.append('schema_version must be 1')
    for key in ('purpose', 'scope'):
        if not _text(data.get(key)):
            errors.append(f'{key} must describe the catalog')
    try:
        date.fromisoformat(data.get('snapshot_date', ''))
    except (TypeError, ValueError):
        errors.append('snapshot_date must be an ISO date')
    needs = data.get('needs')
    if not isinstance(needs, dict) or not needs or any(not _text(k) or not _text(v) for k, v in needs.items()):
        errors.append('needs must be a nonempty label map')
        needs = {}
    provenance = data.get('provenance')
    if not isinstance(provenance, dict) or not _text(provenance.get('source_name')) or not isinstance(provenance.get('sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', provenance.get('sha256', '')):
        errors.append('provenance needs a source name and SHA-256')
    for collection in ('resources', 'access_mechanisms'):
        entries = data.get(collection)
        if not isinstance(entries, list) or not entries:
            errors.append(f'{collection} must be a nonempty list')
            continue
        seen: set[str] = set()
        for i, item in enumerate(entries):
            label = f'{collection}[{i}]'
            if not isinstance(item, dict):
                errors.append(f'{label} must be an object'); continue
            identifier = item.get('id')
            if not isinstance(identifier, str) or not ID.fullmatch(identifier):
                errors.append(f'{label}: invalid id')
            elif identifier in seen:
                errors.append(f'{label}: duplicate id {identifier}')
            else:
                seen.add(identifier)
            for key in ('name',):
                if not _text(item.get(key)): errors.append(f'{label}: missing {key}')
            try: date.fromisoformat(item.get('reviewed_on', ''))
            except (TypeError, ValueError): errors.append(f'{label}: invalid reviewed_on')
            if not _strings(item.get('sources')):
                errors.append(f'{label}: sources must identify official evidence')
            else:
                for url in item['sources']:
                    try:
                        parsed = urlsplit(url)
                        valid = parsed.scheme == 'https' and bool(parsed.hostname) and not parsed.username and not parsed.password
                    except ValueError: valid = False
                    if not valid: errors.append(f'{label}: source must be an HTTPS URL without credentials')
            if collection == 'resources':
                for key in ('needs', 'forms', 'stacks', 'aliases'):
                    if not _strings(item.get(key)): errors.append(f'{label}: {key} must be nonempty strings')
                if _strings(item.get('needs')) and any(x not in needs for x in item['needs']):
                    errors.append(f'{label}: unknown need')
                for key in ('use_for', 'access', 'adoption_notes', 'evidence_scope', 'project_validation'):
                    if not _text(item.get(key)): errors.append(f'{label}: missing {key}')
            else:
                for key in ('use', 'boundary'):
                    if not _text(item.get(key)): errors.append(f'{label}: missing {key}')
    profile_rows = data.get('resources')
    for i, item in enumerate(profile_rows if isinstance(profile_rows, list) else []):
        if not isinstance(item, dict) or 'craft_profile' not in item:
            continue
        profile = item['craft_profile']
        if not isinstance(profile, dict):
            errors.append(f'resources[{i}]: craft_profile must be an object'); continue
        for key in ('roles', 'reuse_scopes', 'visual_forms'):
            values = profile.get(key)
            if not isinstance(values, list) or any(not _text(x) for x in values):
                errors.append(f'resources[{i}].craft_profile: {key} must be a string list')
    return errors


def load_catalog(path: Path = CATALOG) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding='utf-8'))
    errors = validate_catalog(data)
    if errors: raise ValueError('; '.join(errors))
    return data


def select(data: dict[str, Any], query: str = '', *, need: str | None = None,
           stack: str | None = None, form: str | None = None, identifier: str | None = None,
           limit: int = 10, role: str | None = None, reuse_scope: str | None = None) -> list[dict[str, Any]]:
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError('limit must be between 1 and 100')
    if need and need not in data['needs']:
        raise ValueError(f'Unknown need: {need}; use --list-filters')
    known_stacks = {s for r in data['resources'] for s in r['stacks']}
    known_forms = {s for r in data['resources'] for s in r['forms']}
    if stack and stack not in known_stacks:
        raise ValueError(f'Unknown stack: {stack}; use --list-filters')
    if form and form not in known_forms:
        raise ValueError(f'Unknown form: {form}; use --list-filters')
    for key, value in (('roles', role), ('reuse_scopes', reuse_scope)):
        available = {label for row in data['resources']
                     for label in row.get('craft_profile', {}).get(key, [])}
        if value and value not in available:
            raise ValueError(f'Unknown {key} label: {value}; use --list-filters')
    terms = query.casefold().split()
    matches = []
    for item in data['resources']:
        if identifier and item['id'] != identifier: continue
        if need and need not in item['needs']: continue
        # Neutral resources are candidates for each code stack. Adapter support is
        # intentionally left to the exact resource's documentation.
        if stack and stack not in item['stacks']:
            if stack in {'reference', 'design-tool', 'multi-runtime', 'multi-framework'} or 'framework-neutral' not in item['stacks']:
                continue
        if form and form not in item['forms']: continue
        profile = item.get('craft_profile', {})
        if role and role not in profile.get('roles', []): continue
        if reuse_scope and reuse_scope not in profile.get('reuse_scopes', []): continue
        searchable = ' '.join([item['id'],item['name'],item['use_for'],item['access'],
                               *item['needs'],*item['forms'],*item['stacks'],*item['aliases'],
                               *profile.get('roles', []), *profile.get('reuse_scopes', []),
                               *profile.get('visual_forms', [])]).casefold()
        if not all(term in searchable for term in terms): continue
        matches.append(item)
    return sorted(matches, key=lambda x: (x['name'].casefold(), x['id']))[:limit]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('query', nargs='?', default='', help='Whitespace-separated terms, all matched literally')
    p.add_argument('--need'); p.add_argument('--stack'); p.add_argument('--form'); p.add_argument('--id', dest='identifier')
    p.add_argument('--role'); p.add_argument('--reuse-scope')
    p.add_argument('--limit', type=int, default=10); p.add_argument('--json', action='store_true'); p.add_argument('--list-filters', action='store_true')
    args = p.parse_args()
    try:
        data = load_catalog()
        if args.list_filters:
            result = {'needs':data['needs'], 'stacks':sorted({s for r in data['resources'] for s in r['stacks']}),
                      'forms':sorted({s for r in data['resources'] for s in r['forms']}),
                      'roles':sorted({s for r in data['resources'] for s in r.get('craft_profile', {}).get('roles', [])}),
                      'reuse_scopes':sorted({s for r in data['resources'] for s in r.get('craft_profile', {}).get('reuse_scopes', [])}), 'limits':LIMITS}
        else:
            items = select(data, args.query, need=args.need, stack=args.stack, form=args.form, identifier=args.identifier, limit=args.limit, role=args.role, reuse_scope=args.reuse_scope)
            result = {'snapshot_date':data['snapshot_date'], 'results':items, 'count':len(items),
                      'ordering':'alphabetical; no design-quality ranking',
                      'result_kind':'dated_catalog_matches',
                      'facet_scope':'Literal declared labels only; an unclassified entry is not unavailable or lower quality.',
                      'source_note_scope':'Catalog-authored guidance is source material, not a tool-selected next action.', 'limits':LIMITS}
            if not items:
                result['query_observation'] = 'No bundled catalog entry matches the supplied filters; external availability and task fit are not assessed.'
        if args.json or args.list_filters:
            print(json.dumps(result, ensure_ascii=True, indent=2))
        else:
            print(f"Resource leads | research snapshot {data['snapshot_date']}")
            for item in result['results']:
                print(f"\n{item['name']} ({item['id']}) — {item['use_for']}")
                print(f"  Needs: {', '.join(item['needs'])}; forms: {', '.join(item['forms'])}")
                print(f"  Access: {item['access']}\n  Catalog adoption note (source guidance, not a tool-selected action): {item['adoption_notes']}")
                for source in item['sources']: print(f'  {source}')
            if 'query_observation' in result: print(result['query_observation'])
            print('\n'+LIMITS)
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f'find_resources: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
