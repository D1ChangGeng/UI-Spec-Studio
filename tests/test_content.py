"""Deterministic content-source and delivery tests, distinct from user comprehension."""
from __future__ import annotations
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from test_tools import ROOT, load, package, validator

class ContentTests(unittest.TestCase):
    def test_content_reference_is_common_and_direct(self):
        self.assertEqual(len(validator.COMMON),8)
        self.assertIn('content-design',validator.COMMON)
        entry=(ROOT/'skills/ui-spec/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('read all eight common references in full',entry)
        self.assertIn('references/content-design.md',entry)

    def test_method_guides_entire_content_journey(self):
        body=(ROOT/'skills/ui-spec/references/content-design.md').read_text(encoding='utf-8')
        for expected in ('Voice','Tone','Typography','what people need to understand','source facts','Pending','Localize','error','actual outcome','placement'):
            self.assertIn(expected.lower(),body.lower())

    def test_research_links_are_primary_and_scoped(self):
        body=(ROOT/'skills/ui-spec/references/content-sources.md').read_text(encoding='utf-8')
        for expected in ('2026-10-25','GOV.UK','Microsoft','Carbon','WCAG','source'):
            self.assertIn(expected,body)

    def test_content_record_connects_authority_and_delivery(self):
        body=(ROOT/'skills/ui-spec/assets/templates/content-decisions.md').read_text(encoding='utf-8')
        for expected in ('user','locale','copy','Source fact','Evidence','Voice','state'):
            self.assertIn(expected.lower(),body.lower())

    def test_bilingual_content_variants_and_true_status(self):
        js=(ROOT/'examples/content-review/app.js').read_text(encoding='utf-8')
        for text in ('正在保存到此浏览器','Note saved in this browser.','Add a note title before saving.','This note could not be saved','localStorage.setItem','aria-invalid'):
            self.assertIn(text,js)
        self.assertNotIn('innerHTML',js)

    def test_accessible_labels_and_error_association(self):
        html=(ROOT/'examples/content-review/index.html').read_text(encoding='utf-8')
        for val in ('for="note-title"','aria-describedby="title-hint title-error"','role="status"','role="alert"','id="locale-toggle"'):
            self.assertIn(val,html)

    def test_standalone_contains_content_method_and_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            paths=package.build(ROOT,Path(temp))
            with zipfile.ZipFile(paths[1]) as z:
                for rel in ('references/content-design.md','references/content-sources.md','assets/templates/content-decisions.md'):
                    self.assertIn('ui-spec/'+rel,z.namelist())
            with zipfile.ZipFile(paths[0]) as z:
                for rel in ('index.html','styles.css','app.js','README.md'):
                    self.assertIn('ui-spec-studio/examples/content-review/'+rel,z.namelist())

    def test_release_gate_includes_actual_browser(self):
        ci=(ROOT/'.github/workflows/validate.yml').read_text(encoding='utf-8')
        self.assertIn('python tools/validate_content.py --output-dir scenario-evidence/content',ci)
        self.assertIn('needs: [test, install, publication, scenario]',ci)

    def test_package_and_local_references(self):
        self.assertEqual(validator.validate(ROOT),[])

if __name__=='__main__': unittest.main()
