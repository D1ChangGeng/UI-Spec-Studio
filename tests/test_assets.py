"""Asset source and distribution checks; browser/production evidence is separate."""
from __future__ import annotations
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from test_tools import ROOT, load, package, validator

assets = load('asset_checks', 'tools/validate_assets.py')


class AssetTests(unittest.TestCase):
    def test_seventh_reference_is_complete_and_direct(self):
        self.assertEqual(len(validator.COMMON), 8)
        self.assertIn('visual-assets', validator.COMMON)
        entry = (ROOT / 'skills/ui-spec/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('references/visual-assets.md', entry)
        self.assertIn('read all eight common references in full', entry)

    def test_asset_method_covers_distinct_routes_and_roles(self):
        text = (ROOT / 'skills/ui-spec/references/visual-assets.md').read_text(encoding='utf-8')
        for phrase in ('third-party', 'wordmark', '2D-to-3D', 'Procedural/parametric',
                       'static rendering', 'pre-rendered animation', 'real-time 3D',
                       'editable master', 'delivery variants', 'reduced-motion'):
            self.assertIn(phrase, text)

    def test_sources_have_explicit_research_scope(self):
        text = (ROOT / 'skills/ui-spec/references/asset-sources.md').read_text(encoding='utf-8')
        self.assertIn('2026-10-25', text)
        self.assertIn('not execution of each tool', text)
        self.assertIn('current latest-page direct fetch was unavailable', text)

    def test_original_icon_blob_is_unchanged(self):
        data = (ROOT / 'examples/asset-review/search.svg').read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        self.assertEqual(digest, '03e442a5440cff92c219fe3a3c1f2b0788d30701')

    def test_icon_is_passive_and_uses_semantic_color(self):
        svg = ET.fromstring((ROOT / 'examples/asset-review/search.svg').read_bytes())
        self.assertEqual(svg.get('viewBox'), '0 0 24 24')
        self.assertEqual(svg.get('stroke'), 'currentColor')
        self.assertEqual({e.tag.rsplit('}', 1)[-1] for e in svg}, {'path', 'circle'})

    def test_copied_icon_has_applicable_notices(self):
        text = (ROOT / 'examples/asset-review/THIRD-PARTY.md').read_text(encoding='utf-8')
        for value in ('Lucide Icons and Contributors', 'Cole Bemis', 'ISC License', 'MIT License'):
            self.assertIn(value, text)

    def test_inventory_matches_real_bytes(self):
        records = assets.source_inventory()
        self.assertEqual(len(records), 7)
        for row in records:
            data = (ROOT / row['path']).read_bytes()
            self.assertEqual(len(data), row['bytes'])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row['sha256'])

    def test_inventory_rejects_missing_source(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                assets.source_inventory(Path(td))

    def test_shared_assets_reused_without_installable_font_distribution(self):
        files = package.source_files(ROOT)
        # Archived Agent applications retain their licensed font bytes for replay.
        # The portable Skill and the shared publication/example assets still do
        # not distribute fonts. Keep this exception tied to the actual study.
        fonts = [p for p in files if p.suffix.lower() in {'.ttf', '.otf', '.woff', '.woff2'}]
        self.assertEqual({p.relative_to(ROOT).as_posix() for p in fonts}, {
            'docs/experiments/adaptive-granularity/runs/T1-r4/final/app/vendor/inter-latin.woff2',
            'docs/experiments/adaptive-granularity/runs/T1-m9/final/app/vendor/InterVariable.woff2',
        })
        for path in fonts:
            self.assertTrue(path.is_relative_to(ROOT / 'docs/experiments/adaptive-granularity/runs'))
            self.assertEqual(path.suffix, '.woff2')
            license_text = (path.parent / 'INTER-LICENSE.txt').read_text(encoding='utf-8')
            self.assertIn('SIL OPEN FONT LICENSE', license_text)
        html = (ROOT / 'examples/asset-review/index.html').read_text(encoding='utf-8')
        for name in assets.SVG_NAMES:
            self.assertIn('../../docs/assets/' + name, html)

    def test_review_semantics_and_unique_ids(self):
        class Reader(HTMLParser):
            def __init__(self):
                super().__init__(); self.ids = []; self.values = {}
            def handle_starttag(self, tag, attrs):
                values = dict(attrs)
                if 'id' in values:
                    self.ids.append(values['id']); self.values[values['id']] = values
        reader = Reader()
        reader.feed((ROOT / 'examples/asset-review/index.html').read_text(encoding='utf-8'))
        self.assertEqual(len(reader.ids), len(set(reader.ids)))
        self.assertTrue(reader.values['hero']['alt'])
        self.assertEqual(reader.values['motion-stage']['aria-hidden'], 'true')
        self.assertEqual(reader.values['search-button']['aria-label'], 'Search the sample')

    def test_asset_record_has_delivery_and_authority(self):
        text = (ROOT / 'skills/ui-spec/assets/templates/asset-record.md').read_text(encoding='utf-8')
        for phrase in ('Source and allowed use', 'editable master', 'Delivery variants', 'approval source/scope'):
            self.assertIn(phrase, text)

    def test_asset_runtime_is_self_contained(self):
        with tempfile.TemporaryDirectory() as td:
            archives = package.build(ROOT, Path(td))
            with zipfile.ZipFile(archives[1]) as bundle:
                for path in ('references/visual-assets.md', 'references/asset-sources.md', 'assets/templates/asset-record.md'):
                    self.assertIn('ui-spec/' + path, bundle.namelist())
            with zipfile.ZipFile(archives[0]) as bundle:
                for path in ('index.html', 'styles.css', 'app.js', 'search.svg', 'THIRD-PARTY.md'):
                    self.assertIn('ui-spec-studio/examples/asset-review/' + path, bundle.namelist())

    def test_http_asset_checks_are_in_release_gate(self):
        text = (ROOT / '.github/workflows/validate.yml').read_text(encoding='utf-8')
        self.assertIn('needs: [test, install, publication, scenario]', text)
        self.assertIn('python tools/validate_assets.py --output-dir scenario-evidence/assets', text)
        self.assertNotIn('--in-memory', text)

    def test_offline_evidence_is_distinct(self):
        text = (ROOT / 'tools/validate_assets.py').read_text(encoding='utf-8')
        self.assertIn('offline_render_pass_http_pending', text)
        self.assertIn('blocked HTTP illustration', text)
