"""Publication structure, generation and knowledge links; aesthetics require viewing."""
from __future__ import annotations
import ast
from pathlib import Path
import tempfile
import unittest
import zipfile
from test_tools import ROOT, load, package, validator

art = load('readme_art_test', 'tools/readme_art.py')


class PublicationTests(unittest.TestCase):
    def test_generated_art_is_current(self):
        for path, content in art.outputs(ROOT).items():
            self.assertEqual(path.read_text(encoding='utf-8'), content)

    def test_four_distinct_asset_variants(self):
        values=list(art.outputs().values())
        self.assertEqual(len(values),4)
        self.assertEqual(len(set(values)),4)

    def test_assets_are_passive_and_accessible(self):
        for path in art.outputs(ROOT):
            self.assertEqual(validator.check_svg(path),[])

    def test_svg_active_content_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'unsafe.svg'
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><title>x</title><script>alert(1)</script></svg>')
            self.assertTrue(validator.check_svg(path))

    def test_external_svg_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'external.svg'
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><title>x</title><path fill="url(https://example.test/x)"/></svg>')
            self.assertTrue(validator.check_svg(path))

    def test_entity_declaration_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'entity.svg';path.write_text('<!DOCTYPE svg [<!ENTITY x "value">]><svg/>')
            self.assertTrue(validator.check_svg(path))

    def test_html_image_sources_are_validated(self):
        parsed=validator.ImageLinks()
        parsed.feed('<picture><source srcset="one.svg, two.svg 2x"><img src="fallback.svg" alt="meaning"></picture>')
        self.assertEqual(parsed.targets,['one.svg','two.svg','fallback.svg'])
        self.assertEqual(parsed.errors,[])

    def test_alt_text_required(self):
        parsed=validator.ImageLinks();parsed.feed('<img src="a.svg">')
        self.assertTrue(parsed.errors)

    def test_readme_contains_native_command_and_all_variants(self):
        for name in ['README.md','README.zh-CN.md']:
            text=(ROOT/name).read_text(encoding='utf-8')
            self.assertIn('```bash\nnpx skills add D1ChangGeng/UI-Spec-Studio --skill ui-spec\n```',text)
            for path in art.outputs(ROOT):self.assertIn(path.relative_to(ROOT).as_posix(),text)
            self.assertIn('docs/design/README-SPEC.md',text)

    def test_art_is_in_source_archive(self):
        with tempfile.TemporaryDirectory() as td:
            result=package.build(ROOT,Path(td))
            with zipfile.ZipFile(result[0]) as z:
                for path in art.outputs(ROOT):
                    self.assertEqual(z.read('ui-spec-studio/'+path.relative_to(ROOT).as_posix()),path.read_bytes())

    def test_patterns_stay_self_contained(self):
        with tempfile.TemporaryDirectory() as td:
            result=package.build(ROOT,Path(td))
            with zipfile.ZipFile(result[1]) as z:
                self.assertIn('ui-spec/references/patterns.md',z.namelist())
                self.assertFalse(any('/docs/assets/' in name for name in z.namelist()))

    def test_professional_foundation_is_complete_not_size_capped(self):
        # Inspectable professional content takes priority over an arbitrary byte limit.
        self.assertEqual(len(validator.COMMON), 8)
        for name in validator.COMMON:
            text = (ROOT / f"skills/ui-spec/references/{name}.md").read_text(encoding="utf-8")
            self.assertIn("# ", text)
            self.assertIn("## ", text)
        self.assertTrue((ROOT / "docs/CONTENT-INTEGRITY.md").is_file())

    def test_runtime_covers_design_and_medium(self):
        entry=(ROOT/'skills/ui-spec/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('read all eight common references in full',entry)
        self.assertIn('references/patterns.md',entry)
        self.assertIn('README',entry)
        self.assertIn('The host controls activation',entry)

    def test_preview_source_parses_without_optional_imports(self):
        ast.parse((ROOT/'tools/preview_readme.py').read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
