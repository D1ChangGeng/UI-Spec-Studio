"""Resource discovery mechanics and distribution; design acceptance is project evidence."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from test_tools import ROOT, load, package, installer

lookup = load('resource_lookup_tests', 'skills/ui-spec/scripts/find_resources.py')
mapgen = load('resource_map_tests', 'tools/catalog_docs.py')


class ResourceTests(unittest.TestCase):
    def setUp(self):
        self.data = lookup.load_catalog()

    def test_catalog_schema(self):
        self.assertEqual(lookup.validate_catalog(self.data), [])
        self.assertEqual(len(self.data['resources']), 37)
        self.assertEqual(len(self.data['access_mechanisms']), 7)

    def test_snapshot_and_entry_dates_are_preserved(self):
        self.assertEqual(self.data['snapshot_date'], '2026-10-24')
        self.assertTrue(all(x['reviewed_on'] == '2026-10-24' for x in self.data['resources']))
        self.assertTrue(all(x['project_validation'] == 'evaluate_in_project' for x in self.data['resources']))

    def test_vue_motion_preserves_stack_identity(self):
        ids = {x['id'] for x in lookup.select(self.data, need='motion', stack='vue', limit=100)}
        self.assertTrue({'vue-bits', 'inspira', 'motion', 'gsap'} <= ids)
        self.assertNotIn('react-bits', ids)

    def test_vue_controls(self):
        ids = {x['id'] for x in lookup.select(self.data, need='controls', stack='vue', limit=100)}
        self.assertTrue({'reka', 'shadcn-vue', 'nuxt-ui'} <= ids)
        self.assertNotIn('base-ui', ids)

    def test_exact_identity_retains_sources_and_boundaries(self):
        result = lookup.select(self.data, identifier='fontsource')
        self.assertEqual(len(result), 1)
        self.assertIn('exclude', result[0]['adoption_notes'])
        self.assertIn('https://fontsource.org/docs/getting-started/ai-and-llms', result[0]['sources'])

    def test_free_terms_require_all_matches(self):
        self.assertEqual([r['id'] for r in lookup.select(self.data, 'fontsource fonts')], ['fontsource'])
        self.assertEqual(lookup.select(self.data, 'fontsource carousel'), [])

    def test_chinese_aliases(self):
        ids = {x['id'] for x in lookup.select(self.data, '字体')}
        self.assertIn('fontsource', ids)

    def test_form_filter(self):
        rows = lookup.select(self.data, form='tokens', limit=100)
        self.assertTrue(rows)
        self.assertTrue(all('tokens' in row['forms'] for row in rows))

    def test_empty_match_is_honest(self):
        self.assertEqual(lookup.select(self.data, 'no-such-resource-xyz'), [])
        self.assertEqual(lookup.select(self.data, identifier='absent'), [])

    def test_limit_and_order_are_deterministic(self):
        a=lookup.select(self.data, limit=4);b=lookup.select(self.data, limit=4)
        self.assertEqual(a,b)
        self.assertEqual(len(a),4)
        self.assertEqual([x['name'].casefold() for x in a], sorted(x['name'].casefold() for x in a))

    def test_invalid_filter_is_explicit(self):
        for args in ({'need':'missing'}, {'stack':'missing'}, {'form':'missing'}, {'limit':0}, {'limit':True}):
            with self.subTest(args=args), self.assertRaises(ValueError): lookup.select(self.data, **args)

    def test_schema_rejects_invalid_roots(self):
        for value in (None, [], 'data', 1):
            self.assertTrue(lookup.validate_catalog(value))

    def test_duplicate_resource_ids_rejected(self):
        self.data['resources'].append(copy.deepcopy(self.data['resources'][0]))
        self.assertTrue(any('duplicate' in e for e in lookup.validate_catalog(self.data)))

    def test_bad_shapes_return_errors(self):
        for key, value in [('sources',[{}]),('needs',[{}]),('name',None),('reviewed_on',[]),('stacks',[]),('aliases',{})]:
            data=copy.deepcopy(self.data);data['resources'][0][key]=value
            with self.subTest(key=key): self.assertTrue(lookup.validate_catalog(data))

    def test_unknown_needs_rejected(self):
        self.data['resources'][0]['needs']=['invented']
        self.assertTrue(any('unknown need' in e for e in lookup.validate_catalog(self.data)))

    def test_source_urls_require_safe_identity(self):
        for url in ('file:///secret','https://user:pass@example.test/file','javascript:alert(1)','http://example.test'):
            data=copy.deepcopy(self.data);data['resources'][0]['sources']=[url]
            with self.subTest(url=url): self.assertTrue(lookup.validate_catalog(data))

    def test_generated_map_matches_data(self):
        self.assertEqual((ROOT/'skills/ui-spec/references/resource-catalog.md').read_text(encoding='utf-8'), mapgen.render(self.data))

    def test_all_resource_ids_and_sources_are_in_map(self):
        text=mapgen.render(self.data)
        for item in self.data['resources']:
            self.assertIn(f"(`{item['id']}`)", text)
            for url in item['sources']: self.assertIn(url,text)

    def test_catalog_is_self_contained_in_skill_archive(self):
        with tempfile.TemporaryDirectory() as td:
            archives=package.build(ROOT,Path(td))
            with zipfile.ZipFile(archives[1]) as archive:
                for path in ('assets/resource-catalog.json','references/resource-catalog.md','scripts/find_resources.py','assets/templates/resource-adoption.md'):
                    self.assertEqual(archive.read('ui-spec/'+path),(ROOT/'skills/ui-spec'/path).read_bytes())

    def test_installed_lookup_runs_read_only_from_other_directory(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);target=root/'installed/ui-spec';installer.install(target)
            before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
            result=subprocess.run([sys.executable,str(target/'scripts/find_resources.py'),'--id','fontsource','--json'],cwd=root,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout)['results'][0]['id'],'fontsource')
            after={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(before,after)

    def test_cli_empty_and_invalid_results(self):
        script=ROOT/'skills/ui-spec/scripts/find_resources.py'
        result=subprocess.run([sys.executable,str(script),'no-such-resource-xyz','--json'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0)
        data=json.loads(result.stdout);self.assertEqual(data['count'],0);self.assertIn('query_observation',data)
        result=subprocess.run([sys.executable,str(script),'--need','missing'],capture_output=True,text=True)
        self.assertEqual(result.returncode,2);self.assertNotIn('Traceback',result.stderr)

    def test_cli_lists_actual_filters(self):
        script=ROOT/'skills/ui-spec/scripts/find_resources.py'
        result=subprocess.run([sys.executable,str(script),'--list-filters'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        data=json.loads(result.stdout);self.assertIn('motion',data['needs']);self.assertIn('vue',data['stacks'])

    def test_common_method_and_stage_links(self):
        skill=(ROOT/'skills/ui-spec/SKILL.md').read_text(encoding='utf-8')
        method=(ROOT/'skills/ui-spec/references/component-sourcing.md').read_text(encoding='utf-8')
        self.assertIn('read all eight common references in full',skill)
        self.assertIn('references/resource-catalog.md',skill)
        for term in ('Requirement-led','Opportunity-led','total cost','project acceptance','authorized review'):
            self.assertIn(term,method)
        for path in ('analysis','workflow','principles','interaction-and-variants','verification','integration'):
            self.assertIn('resource',(ROOT/f'skills/ui-spec/references/{path}.md').read_text(encoding='utf-8').lower())

    def test_readmes_explain_resources_and_current_version(self):
        for path in ('README.md','README.zh-CN.md'):
            text=(ROOT/path).read_text(encoding='utf-8')
            self.assertIn('skills/ui-spec/references/resource-catalog.md',text)
            self.assertIn('docs/RESOURCE-REUSE.md',text)
            self.assertIn('tree/v'+(ROOT/'VERSION').read_text().strip(),text)


if __name__=='__main__':unittest.main()
