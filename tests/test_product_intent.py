"""Scoped structural/source tests; the separate browser job executes the scenario."""
from __future__ import annotations
import json
from html.parser import HTMLParser
from pathlib import Path
import tempfile
import unittest
import zipfile
from test_tools import ROOT, load, package, validator

scenario = load('scenario_checks', 'tools/validate_scenario.py')

class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.sources=[];self.values=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and a.get('href','').startswith('https:'):self.sources.append(a['href'])
        if tag=='input' and a.get('name')=='model':self.values.append(a.get('value'))

class ProductIntentTests(unittest.TestCase):
    def test_scenario_has_distinct_model_controls_and_unique_ids(self):
        d=Document();d.feed((ROOT/'examples/product-intent/index.html').read_text(encoding='utf-8'))
        self.assertEqual(set(d.values),{'conversation','documents'})
        self.assertEqual(len(d.ids),len(set(d.ids)))
        self.assertTrue({'composer','editor','decision-dialog','source-dialog','history-dialog'}<=set(d.ids))

    def test_live_decision_panel_links_product_and_engineering_sources(self):
        d=Document();d.feed((ROOT/'examples/product-intent/index.html').read_text(encoding='utf-8'))
        self.assertTrue(any('anthropic.com' in u for u in d.sources))
        self.assertTrue(any('notion.com' in u for u in d.sources))
        self.assertTrue(any('/input-group' in u for u in d.sources))
        self.assertTrue(any('radix-ui.com/colors' in u for u in d.sources))

    def test_source_values_and_license_are_preserved(self):
        css=(ROOT/'examples/product-intent/tokens.css').read_text()
        for value in ('#fcfcfd','#60646c','#1c2024','#111113','#b0b4ba','#edeef0'):
            self.assertIn(value,css)
        self.assertIn('dbdb85470547c7d34b9001f48fddb08ded335979',css)
        notice=(ROOT/'examples/product-intent/THIRD-PARTY.md').read_text()
        self.assertIn('Copyright (c) 2021-2022 Modulz',notice)
        self.assertIn('Copyright (c) 2022-Present WorkOS',notice)
        self.assertIn('MIT License',notice)

    def test_no_remote_runtime_is_required(self):
        text=(ROOT/'examples/product-intent/index.html').read_text(encoding='utf-8')
        self.assertNotIn('<script src="https:',text)
        css=(ROOT/'examples/product-intent/styles.css').read_text()
        self.assertNotIn('url("https:',css)

    def test_source_uses_text_for_untrusted_user_content(self):
        script=(ROOT/'examples/product-intent/app.js').read_text()
        self.assertIn('user.textContent = question',script)
        self.assertNotIn('innerHTML',script)

    def test_contrast_calculation_known_limits(self):
        self.assertAlmostEqual(scenario.contrast([0,0,0],[255,255,255]),21)
        self.assertAlmostEqual(scenario.contrast([128,128,128],[128,128,128]),1)
        self.assertAlmostEqual(scenario.contrast([255,255,255],[0,0,0]),21)

    def test_selected_color_pairs_reach_target(self):
        for foreground,background in (([96,100,108],[252,252,253]),([176,180,186],[17,17,19]),([255,255,255],[35,88,185])):
            self.assertGreaterEqual(scenario.contrast(foreground,background),4.5)

    def test_decision_template_is_self_contained(self):
        path=ROOT/'skills/ui-spec/assets/templates/design-decisions.md'
        text=path.read_text()
        for phrase in ('Direction and authority','Reuse assessment','Surface and resource selection','implementation/preview','approval'):
            self.assertIn(phrase,text)
        self.assertEqual(validator.validate(ROOT),[])

    def test_common_contract_retains_six_references(self):
        entry=(ROOT/'skills/ui-spec/SKILL.md').read_text()
        for name in validator.COMMON:self.assertIn(f'references/{name}.md',entry)
        self.assertIn('optional `shape`',entry)
        self.assertIn('one-shot',entry)
        self.assertIn('actual user decision', (ROOT/'skills/ui-spec/references/component-sourcing.md').read_text())

    def test_standalone_distribution_contains_decision_template(self):
        with tempfile.TemporaryDirectory() as td:
            files=package.build(ROOT,Path(td))
            with zipfile.ZipFile(files[1]) as archive:
                self.assertIn('ui-spec/assets/templates/design-decisions.md',archive.namelist())

    def test_source_distribution_contains_runnable_scenario(self):
        with tempfile.TemporaryDirectory() as td:
            files=package.build(ROOT,Path(td))
            with zipfile.ZipFile(files[0]) as archive:
                for name in ('index.html','styles.css','tokens.css','app.js','THIRD-PARTY.md'):
                    self.assertIn('ui-spec-studio/examples/product-intent/'+name,archive.namelist())

    def test_scene_tests_keep_approval_and_storage_scope_explicit(self):
        source=(ROOT/'tools/validate_scenario.py').read_text()
        self.assertIn("'owner_approval':'pending'",source)
        self.assertIn("report['storage_verified']=True",source)
        self.assertIn('preview_pass_storage_pending',source)
        self.assertIn('local-http',source)

    def test_ci_requires_actual_browser_scenario_for_release(self):
        source=(ROOT/'.github/workflows/validate.yml').read_text()
        self.assertIn('needs: [test, install, publication, scenario]',source)
        self.assertIn('python tools/validate_scenario.py --output-dir scenario-evidence',source)
        self.assertNotIn('--in-memory',source)

    def test_catalog_identity_is_retained(self):
        data=json.loads((ROOT/'skills/ui-spec/assets/resource-catalog.json').read_text())
        self.assertEqual(len(data['resources']),37)
        self.assertEqual(len({r['id'] for r in data['resources']}),37)
