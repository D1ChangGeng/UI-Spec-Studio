"""Current source continuity checks, separate from historical snapshot evidence."""
from __future__ import annotations
import base64
import hashlib
import json
from pathlib import Path
import unittest
import zlib
from test_tools import ROOT


class BoundaryReleaseTests(unittest.TestCase):
    def test_current_runtime_changes_have_explicit_dispositions(self):
        record=json.loads((ROOT/'docs/evidence/v1.15.0/continuity.json').read_text())
        frozen=json.loads((ROOT/'docs/evidence/v1.15.0/baseline-runtime.json').read_text())
        payload=zlib.decompress(base64.b64decode(frozen['payload']))
        self.assertEqual(hashlib.sha256(payload).hexdigest(),frozen['payload_sha256'])
        prior=json.loads(payload)
        self.assertEqual(set(prior),{r['path'] for r in record['files']})
        for row in record['files']:
            before=prior[row['path']].encode();current=(ROOT/row['path']).read_bytes()
            self.assertEqual(hashlib.sha256(before).hexdigest(),row['before_sha256'])
            self.assertEqual(hashlib.sha256(current).hexdigest(),row['current_sha256'])
            if row['disposition']=='unchanged':self.assertEqual(current,before)
            elif row['disposition']=='append-only':self.assertTrue(current.startswith(before))
            else:self.assertTrue(row['reason'])
        for item in record['professional_responsibility_transfers']:
            self.assertIn(item['specificity'],(ROOT/item['agent_source']).read_text())

    def test_existing_historical_evidence_is_not_relabelled(self):
        record=json.loads((ROOT/'docs/evidence/v1.15.0/continuity.json').read_text())
        for item in record['historical_evidence_unchanged']:
            self.assertEqual(hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest(),item['sha256'])

    def test_detailed_methods_remain_in_installed_guidance(self):
        paths={'references/evidence-map.md':['Theoretical','Meaningful Revisions','Evidence Archive'],
               'references/evidence-actions.md':['Gap-to-action rules','The Agent interprets structural observations'],
               'references/evidence-records.md':['candidate_unrepresented_categories','no mechanical two-name minimum','global snapshot change does not mechanically invalidate'],
               'SKILL.md':['four responsibilities','read all eight common references in full']}
        for path,fragments in paths.items():
            text=(ROOT/'skills/ui-spec'/path).read_text().lower()
            for fragment in fragments:self.assertIn(fragment.lower(),text)


if __name__=='__main__':unittest.main()
