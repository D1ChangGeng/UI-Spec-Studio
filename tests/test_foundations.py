"""Foundation provenance and authored contracts; model quality is separate."""
import json
import unittest
from test_tools import ROOT

class FoundationTests(unittest.TestCase):
    def test_foundation_identity_and_scope(self):
        data=json.loads((ROOT/'examples/product-intent/foundation.json').read_text(encoding='utf-8'))
        self.assertEqual(data['granularity'],'page')
        self.assertEqual(data['method'],'cross-stack design transfer')
        self.assertEqual(data['approval'],'pending')
        self.assertEqual(data['source_blob'],'0f22e7855a954269ecdee0fd9963240c966e1bc1')
        self.assertGreaterEqual(len(data['preserved']),5)
        self.assertGreaterEqual(len(data['alternatives']),2)
    def test_method_has_distinct_granularity_and_adoption(self):
        text=(ROOT/'skills/ui-spec/references/component-sourcing.md').read_text(encoding='utf-8')
        self.assertIn('highest appropriate reuse level',text)
        self.assertIn('Reuse granularity and adoption method are separate choices',text)
        self.assertIn('page/application templates and design systems',text)
    def test_entry_establishes_the_default_before_execution(self):
        text=(ROOT/'skills/ui-spec/SKILL.md').read_text(encoding='utf-8')
        self.assertLess(text.index('Start from mature design work'),text.index('Choose the operation'))
        self.assertIn('Theory explains quality, fit and tradeoffs',text)
        self.assertIn('highest appropriate reuse level',text)
    def test_example_identifies_inherited_relationships(self):
        text=(ROOT/'examples/product-intent/FOUNDATION.md').read_text(encoding='utf-8')
        for term in ('page-level','48rem','28px','22px','runtime','comparison probe'):
            self.assertIn(term,text.lower())
