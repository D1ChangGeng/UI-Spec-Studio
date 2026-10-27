"""Distribution/integrity and experiment-preparation checks, not Agent experiments."""
from __future__ import annotations
import hashlib
import base64
import zlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj

prep=load('experiment_preparation',ROOT/'tools/prepare_design_experiment.py')
package=load('multiscale_package',ROOT/'tools/package.py')


def restored_baseline() -> dict:
    record=json.loads((ROOT/'docs/evidence/v1.14.0/source-preservation.json').read_text())
    # v1.14 preservation is historical evidence; the 1.15 boundary correction
    # legitimately changes helper behavior. Freeze rather than relabel that evidence.
    frozen=json.loads((ROOT/'docs/evidence/v1.15.0/baseline-runtime.json').read_text())
    raw=zlib.decompress(base64.b64decode(frozen['payload']))
    if hashlib.sha256(raw).hexdigest()!=frozen['payload_sha256']:
        raise ValueError('Frozen historic runtime differs')
    previous=json.loads(raw)
    out={}
    for row in record['files']:
        current=previous[row['path']].encode()
        if row['mode']=='append-only':
            original=current[:row['before_bytes']]
        elif row['mode']=='unchanged':
            original=current
        else:
            text=current.decode()
            for replacement in row['reverse_replacements']:
                if text.count(replacement['new'])!=1:raise ValueError('Entry edit no longer reversible')
                text=text.replace(replacement['new'],replacement['old'])
            original=text.encode()
        if hashlib.sha256(original).hexdigest()!=row['before_sha256']:
            raise ValueError('Historical runtime content altered: '+row['path'])
        out[row['path'].removeprefix('skills/ui-spec/')]=original
    return out


class MultiscaleReleaseTests(unittest.TestCase):
    def test_frozen_v114_preservation_and_experiment_baseline_retained(self):
        original=restored_baseline()
        expected=json.loads((prep.MATERIAL/'baseline-identity.json').read_text())['files']
        self.assertEqual({p:prep.digest(b) for p,b in original.items()},expected)

    def test_new_method_and_helper_are_in_standalone_bundle(self):
        with tempfile.TemporaryDirectory() as td:
            result=package.build(ROOT,Path(td))
            with zipfile.ZipFile(result[1]) as z:
                for path in ('references/evidence-map.md','references/evidence-actions.md',
                             'references/evidence-records.md','scripts/check_design_evidence.py',
                             'assets/templates/design-evidence.json'):
                    self.assertEqual(z.read('ui-spec/'+path),(ROOT/'skills/ui-spec'/path).read_bytes())

    def test_eight_references_and_existing_records_not_replaced(self):
        entry=(ROOT/'skills/ui-spec/SKILL.md').read_text()
        self.assertIn('read all eight common references in full',entry)
        self.assertIn('a schema or new document is optional',entry)
        self.assertNotIn('design-evidence.json',(ROOT/'skills/ui-spec/scripts/prepare.py').read_text())

    def test_experiment_preparation_is_matched_and_not_execution(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td)/'baseline';base.mkdir()
            for path,blob in restored_baseline().items():
                p=base/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(blob)
            before=prep.snapshot(base)
            out=Path(td)/'experiment'
            report=prep.build(base,out)
            self.assertEqual(report['status'],'prepared_not_run')
            self.assertEqual(report['model_runs_executed'],0)
            self.assertEqual(len(report['cells']),18)
            self.assertEqual(before,prep.snapshot(base))
            self.assertEqual(report['arms']['baseline'],{p:prep.digest(b) for p,b in before.items()})
            for task in ('T01','T02','T03','T04','T05','T06'):
                prompts=[(out/'cells'/f'{task}-{a}'/'TASK.md').read_bytes() for a in report['arms']]
                self.assertTrue(all(p==prompts[0] for p in prompts))
                a=out/'cells'/f'{task}-structure'/'ui-spec'
                b=out/'cells'/f'{task}-structure-action'/'ui-spec'
                self.assertFalse((a/'references/evidence-actions.md').exists())
                self.assertFalse((a/'scripts/check_design_evidence.py').exists())
                self.assertNotIn('evidence-actions.md',(a/'references/evidence-map.md').read_text())
                self.assertEqual((a/'references/evidence-map.md').read_bytes(),(b/'references/evidence-map.md').read_bytes())
            with self.assertRaisesRegex(ValueError,'must not exist'):prep.build(base,out)

    def test_baseline_identity_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td)/'baseline';base.mkdir();(base/'SKILL.md').write_text('Not the actual baseline')
            with self.assertRaisesRegex(ValueError,'identity differs'):prep.build(base,Path(td)/'output')
            self.assertFalse((Path(td)/'output').exists())

    def test_symlink_baseline_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);base=root/'base';base.mkdir();(base/'other.md').symlink_to(root/'missing')
            with self.assertRaisesRegex(ValueError,'symlinks'):prep.snapshot(base)

    def test_experiment_files_remain_outside_installed_skill(self):
        with tempfile.TemporaryDirectory() as td:
            result=package.build(ROOT,Path(td))
            with zipfile.ZipFile(result[1]) as z:
                self.assertFalse(any('experiments/' in n for n in z.namelist()))
            with zipfile.ZipFile(result[0]) as z:
                self.assertIn('ui-spec-studio/docs/experiments/design-evidence/PROTOCOL.md',z.namelist())


if __name__=='__main__':unittest.main()
