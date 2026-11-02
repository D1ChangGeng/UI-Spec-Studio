"""Publication structure, generation and knowledge links; aesthetics require viewing."""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
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
            self.assertIn("```bash\nnpx --yes ui-spec-studio@latest\n```", text)
            for path in art.outputs(ROOT):self.assertIn(path.relative_to(ROOT).as_posix(),text)
            self.assertIn('docs/design/README-SPEC.md',text)

    def test_art_is_in_source_archive(self):
        with tempfile.TemporaryDirectory() as td:
            result=package.build(ROOT,Path(td),include_evidence=False)
            with zipfile.ZipFile(result[0]) as z:
                for path in art.outputs(ROOT):
                    self.assertEqual(z.read('ui-spec-studio/'+path.relative_to(ROOT).as_posix()),path.read_bytes())

    def test_patterns_stay_self_contained(self):
        with tempfile.TemporaryDirectory() as td:
            result=package.build(ROOT,Path(td),include_evidence=False)
            with zipfile.ZipFile(result[1]) as z:
                self.assertIn('ui-spec/references/patterns.md',z.namelist())
                self.assertFalse(any('/docs/assets/' in name for name in z.namelist()))

    def test_source_archive_keeps_replay_checksum_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'repo';root.mkdir()
            (root/'VERSION').write_text('1.20.0\n')
            skill=root/'skills/ui-spec';skill.mkdir(parents=True)
            (skill/'SKILL.md').write_text('# Test fixture\n')
            evidence=root/'docs/evidence/campaign';evidence.mkdir(parents=True)
            content=b'fixed evidence fixture\n'
            (evidence/'events.jsonl').write_bytes(content)
            checksum=(hashlib.sha256(content).hexdigest()+'  events.jsonl\n').encode()
            (evidence/'MANIFEST.sha256').write_bytes(checksum)
            outputs=package.build(root,Path(td)/'dist')
            with zipfile.ZipFile(outputs[0]) as archive:
                self.assertEqual(archive.read('ui-spec-studio/docs/evidence/campaign/MANIFEST.sha256'),checksum)
                self.assertEqual(archive.read('ui-spec-studio/docs/evidence/campaign/events.jsonl'),content)

    def test_professional_foundation_is_complete_not_size_capped(self):
        # Inspectable professional content takes priority over an arbitrary byte limit.
        self.assertEqual(len(validator.COMMON), 8)
        for name in validator.COMMON:
            text = (ROOT / f"skills/ui-spec/references/{name}.md").read_text(encoding="utf-8")
            self.assertIn("# ", text)
            self.assertIn("## ", text)
        self.assertTrue((ROOT / "docs/CONTENT-INTEGRITY.md").is_file())

    def test_published_standalone_adapter_installs_its_four_verified_roles(self):
        with tempfile.TemporaryDirectory() as temporary:
            base=Path(temporary).resolve()
            outputs=package.build(ROOT,base/'dist',include_evidence=False)
            version=(ROOT/'VERSION').read_text().strip()
            adapter=next(p for p in outputs if p.name==f'ui-spec-codex-{version}.zip')
            checksums=(base/'dist/SHA256SUMS.txt').read_text()
            self.assertIn(f'{hashlib.sha256(adapter.read_bytes()).hexdigest()}  {adapter.name}\n',checksums)
            with zipfile.ZipFile(adapter) as archive:
                archive.extractall(base/'extracted')
                self.assertEqual(archive.read('ui-spec-codex/LICENSE'),(ROOT/'LICENSE').read_bytes())
            standalone=base/'extracted/ui-spec-codex'
            project=base/'consumer'
            result=subprocess.run([sys.executable,str(standalone/'install.py'),'install','--project',str(project)],
                                  cwd=base,capture_output=True,text=True,check=False)
            self.assertEqual(result.returncode,0,result.stderr+result.stdout)
            manifest=json.loads((standalone/'manifest.json').read_text())
            self.assertEqual(set(manifest['roles']),{'ui_researcher','ui_integrator','ui_challenger','ui_experience_observer'})
            for role,entry in manifest['roles'].items():
                actual=project/'.codex'/entry['path']
                self.assertTrue(entry['default_install'])
                self.assertEqual(hashlib.sha256(actual.read_bytes()).hexdigest(),entry['sha256'])
            self.assertTrue((standalone/'launch.py').is_file())

    def test_runtime_covers_design_and_medium(self):
        entry=(ROOT/'skills/ui-spec/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('read all eight common references in full',entry)
        self.assertIn('references/patterns.md',entry)
        self.assertIn('README',entry)
        self.assertIn('The host controls activation',entry)

    def test_preview_source_parses_without_optional_imports(self):
        ast.parse((ROOT/'tools/preview_readme.py').read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
