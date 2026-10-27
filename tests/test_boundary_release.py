"""Current source continuity checks, separate from historical snapshot evidence."""
from __future__ import annotations
import ast
import base64
import hashlib
import json
from pathlib import Path
import unittest
import zlib
from test_tools import ROOT


class BoundaryReleaseTests(unittest.TestCase):
    def test_current_runtime_changes_have_explicit_dispositions(self):
        record=json.loads((ROOT/'docs/evidence/v1.15.0/continuity.json').read_text(encoding='utf-8'))
        frozen=json.loads((ROOT/'docs/evidence/v1.15.0/baseline-runtime.json').read_text(encoding='utf-8'))
        payload=zlib.decompress(base64.b64decode(frozen['payload']))
        self.assertEqual(hashlib.sha256(payload).hexdigest(),frozen['payload_sha256'])
        prior=json.loads(payload)
        self.assertEqual(set(prior),{r['path'] for r in record['files']})
        current_frozen=json.loads((ROOT/'docs/evidence/v1.16.0/baseline-runtime.json').read_text(encoding='utf-8'))
        current_payload=zlib.decompress(base64.b64decode(current_frozen['payload']))
        self.assertEqual(hashlib.sha256(current_payload).hexdigest(),current_frozen['payload_sha256'])
        historical_current=json.loads(current_payload)
        for row in record['files']:
            before=prior[row['path']].encode();current=historical_current[row['path']].encode('utf-8')
            self.assertEqual(hashlib.sha256(before).hexdigest(),row['before_sha256'])
            self.assertEqual(hashlib.sha256(current).hexdigest(),row['current_sha256'])
            if row['disposition']=='unchanged':self.assertEqual(current,before)
            elif row['disposition']=='append-only':self.assertTrue(current.startswith(before))
            else:self.assertTrue(row['reason'])
        for item in record['professional_responsibility_transfers']:
            self.assertIn(item['specificity'],(ROOT/item['agent_source']).read_text(encoding='utf-8'))

    def test_existing_historical_evidence_is_not_relabelled(self):
        record=json.loads((ROOT/'docs/evidence/v1.15.0/continuity.json').read_text(encoding='utf-8'))
        for item in record['historical_evidence_unchanged']:
            self.assertEqual(hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest(),item['sha256'])

    def test_detailed_methods_remain_in_installed_guidance(self):
        paths={'references/evidence-map.md':['Theoretical','Meaningful Revisions','Evidence Archive'],
               'references/evidence-actions.md':['Gap-to-action rules','The Agent interprets structural observations'],
               'references/evidence-records.md':['candidate_unrepresented_categories','no mechanical two-name minimum','global snapshot change does not mechanically invalidate'],
               'SKILL.md':['four responsibilities','read all eight common references in full']}
        for path,fragments in paths.items():
            text=(ROOT/'skills/ui-spec'/path).read_text(encoding='utf-8').lower()
            for fragment in fragments:self.assertIn(fragment.lower(),text)


    def test_boundary_text_readers_declare_utf8(self):
        # A Windows cp1252 default must not decode UTF-8 method references.
        names = ['tests/test_boundary_release.py'] + [
            f'skills/ui-spec/scripts/{name}.py' for name in
            ('structural_records', 'check_design_evidence', 'check_manifest',
             'check_file_integrity', 'prepare', 'find_resources')]
        for name in names:
            source = (ROOT / name).read_text(encoding='utf-8')
            for node in ast.walk(ast.parse(source)):
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and node.func.attr == 'read_text'):
                    with self.subTest(path=name, line=node.lineno):
                        self.assertTrue(any(
                            k.arg == 'encoding' and isinstance(k.value, ast.Constant)
                            and k.value.value == 'utf-8' for k in node.keywords))

if __name__=='__main__':unittest.main()
