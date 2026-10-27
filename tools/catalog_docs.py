#!/usr/bin/env python3
"""Render the bundled resource map from its single curated data source."""
from __future__ import annotations
import argparse
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog_lookup', ROOT/'skills/ui-spec/scripts/find_resources.py')
lookup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lookup)
TARGET = ROOT/'skills/ui-spec/references/resource-catalog.md'


def render(data: dict) -> str:
    out = ['# UI resource map', '', 'Find a useful starting point by need, then read the exact item and its current primary source.',
           'Apply [the common sourcing method](component-sourcing.md) throughout selection and integration.', '',
           f"Research snapshot: **{data['snapshot_date']}** · **{len(data['resources'])} resources** · **{len(data['access_mechanisms'])} access mechanisms**.",
           data['scope'], '', '## Use the map', '',
           'Read the relevant section, use the [structured catalog](../assets/resource-catalog.json), or query the optional local helper:', '',
           '```bash', 'python <skill-dir>/scripts/find_resources.py --need motion --stack vue --json',
           'python <skill-dir>/scripts/find_resources.py --id fontsource --json',
           'python <skill-dir>/scripts/find_resources.py --role visual-implementation --reuse-scope functional-block --json',
           'python <skill-dir>/scripts/find_resources.py --role visual-implementation --stack vue --json',
           'python <skill-dir>/scripts/find_resources.py --list-filters', '```', '',
           'Queries match all supplied terms; filters combine. Results are alphabetical discovery leads. A stack filter includes framework-neutral candidates; exact adapter compatibility is checked in primary documentation. No match describes this catalogue query, not external availability; the Agent decides further research. The helper reads local data and performs no installation or network operation.', '',
           'Platform documentation, item inspection and project acceptance have different scopes. Review dates identify the source research, and use-time checks establish current fit. Keep actual adoption records in the project. Maintain shared entries through authorized review and normal version control.', '',
           '## Needs and delivery forms', '', '| Need | Scope |', '|---|---|']
    out += [f'| `{key}` | {value} |' for key,value in data['needs'].items()]
    out += ['', 'Source components, packages, primitives, tokens, assets, fonts, blocks, engines, generators, design files and references each have distinct ownership and update requirements. Resources can serve several needs.', '', '## Documented role and reuse-scope filters', '',
           'Role, useful scope and visual completeness are different. These optional labels describe source offerings, not scores. Untagged entries are unclassified here. The Agent still inspects an exact demo, trials real conditions and judges retained quality.', '',
           'Use page/functional-block leads for coherent composition, visual-component/effect leads for specific visible mechanisms, and behavioral foundations for their semantic responsibility. No row is a mandatory supplier or a claim that its examples suit this product.', '',
           'Finesse UI (finesseui.com) below is a design-kit entry, not the separately studied mouse-lin Finesse Skill. Their names must not merge source or licensing claims.', '', '## Resource cards', '']
    for x in sorted(data['resources'],key=lambda x:x['name'].casefold()):
        out += [f"### {x['name']} (`{x['id']}`)", '', x['use_for'], '',
                f"**Find by:** {', '.join(x['needs'])}. **Form:** {', '.join(x['forms'])}. **Stack scope:** {', '.join(x['stacks'])}.",
                f"**Access:** {x['access']}", f"**Adoption judgment:** {x['adoption_notes']}",
                '**Primary sources:** '+' · '.join(f'[Source {i+1}]({u})' for i,u in enumerate(x['sources'])),
                f"**Evidence:** {x['evidence_scope']}; reviewed {x['reviewed_on']}; project use: {x['project_validation']}.", '']
        if x.get('discovery_profile'):
            profile=x['discovery_profile']
            out += [f"**Documented roles:** {', '.join(profile['roles'])}. **Reuse scope leads:** {', '.join(profile['reuse_scopes'])}. **Visible forms to inspect:** {', '.join(profile['visual_forms'])}.",
                    f"**Classification:** {profile['classified_on']}; {profile['basis']}",
                    '**Facet sources:** '+' · '.join(f'[Source {i+1}]({u})' for i,u in enumerate(profile['sources'])), '']
    out += ['## Access mechanisms', '']
    for x in data['access_mechanisms']:
        out += [f"### {x['name']}", '', x['use'], '', x['boundary'], '',
                ' · '.join(f'[Source {i+1}]({u})' for i,u in enumerate(x['sources'])), '']
    out += ['## Maintenance', '', 'The structured catalog is the maintained source; this map is generated from it. Preserve source identity, actual evidence scope and original observation dates. Recheck relevant version, rights, interface and availability when adopting. The release-specific spot checks are recorded in the data without changing every entry’s historical review date.', '']
    return '\n'.join(out)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    try:
        content=render(lookup.load_catalog())
        if args.check:
            if not TARGET.is_file() or TARGET.read_text(encoding='utf-8') != content:
                raise ValueError('Regenerate the resource map with python tools/catalog_docs.py')
            print('Resource data and generated map: PASS')
        else:
            TARGET.write_text(content,encoding='utf-8',newline='\n');print(TARGET)
        return 0
    except (OSError,ValueError) as exc:
        print(f'catalog_docs: {exc}',file=sys.stderr);return 1


if __name__=='__main__': raise SystemExit(main())
