#!/usr/bin/env python3
"""Freeze matched instruction-ablation inputs. Never execute or score Agent runs."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MATERIAL = ROOT / 'docs/experiments/design-evidence'
STRUCTURE_ENTRY = '''\n## Multiscale evidence structure for this task\n\nRead [the evidence map](references/evidence-map.md) and use its scales, coverage\nchallenge and evidence-linked decision relations for consequential work. Use\nexisting records and proportional depth; fixed serialization is optional.\n'''
ACTION_ENTRY = '''\n## Evidence-to-action coupling for this task\n\nRead [the action rules](references/evidence-actions.md) before consequential\ncommitments. Important gaps change the next actual action and limit dependent\ncommitments while allowing independent work and bounded revealing trials.\n'''


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def snapshot(root: Path) -> dict[str, bytes]:
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Baseline must be a real directory')
    result = {}
    for p in sorted(root.rglob('*')):
        if p.is_symlink():
            raise ValueError('Baseline must not contain symlinks')
        if '__pycache__' in p.parts or p.suffix == '.pyc':
            continue
        if p.is_file():
            result[p.relative_to(root).as_posix()] = p.read_bytes()
    return result


def build(baseline: Path, output: Path) -> dict:
    expected = json.loads((MATERIAL/'baseline-identity.json').read_text(encoding='utf-8'))
    source = snapshot(baseline)
    actual = {p: digest(b) for p,b in source.items()}
    if actual != expected['files']:
        raise ValueError('Baseline file identity differs from the complete v1.13.0 skill')
    # Resolve only the parent; preserve symlink/nonexisting leaf checks.
    if output.exists() or output.is_symlink():
        raise ValueError('Output must not exist; existing experiments are preserved')
    parent = output.parent.resolve(strict=True)
    if not parent.is_dir():
        raise ValueError('Output parent must exist')
    output = parent / output.name
    if output.is_relative_to(baseline.resolve()):
        raise ValueError('Output must be outside the baseline')
    structure = (ROOT/'skills/ui-spec/references/evidence-map.md').read_text(encoding='utf-8')
    pointer = 'Read the [action rules](evidence-actions.md) when choosing what to do with a\nconsequential gap. '
    if structure.count(pointer) != 1 or structure.count('## Tool boundary') != 1:
        raise ValueError('Treatment boundaries changed; revise and review the experiment isolation')
    structure = structure.replace(pointer, '').split('## Tool boundary')[0].rstrip()+'\n'
    if 'evidence-actions.md' in structure or 'check_design_evidence' in structure:
        raise ValueError('Action/checker treatment leaks into structure arm')
    action = (ROOT/'skills/ui-spec/references/evidence-actions.md').read_bytes()
    tasks = json.loads((MATERIAL/'tasks.json').read_text(encoding='utf-8'))
    arms = {}
    for name in ('baseline', 'structure', 'structure-action'):
        files = dict(source)
        if name != 'baseline':
            files['SKILL.md'] += STRUCTURE_ENTRY.encode()
            files['references/evidence-map.md'] = structure.encode()
        if name == 'structure-action':
            files['SKILL.md'] += ACTION_ENTRY.encode()
            files['references/evidence-actions.md'] = action
        arms[name] = files
    record = {'status': 'prepared_not_run', 'baseline': {k:v for k,v in expected.items() if k!='files'},
              'scope': 'Instruction-only module ablation, not the full production v1.14 distribution',
              'arms': {name:{p:digest(b) for p,b in files.items()} for name,files in arms.items()},
              'cells': [], 'model_runs_executed': 0,
              'required_before_execution': 'Freeze identical task inputs and authorized runner/tool conditions; see PROTOCOL.md'}
    stage = Path(tempfile.mkdtemp(prefix='.ui-spec-experiment-', dir=parent))
    try:
        for task in tasks:
            tid = task['id']; prompt_name = task['prompt']
            if not isinstance(tid, str) or not tid.isalnum() or Path(prompt_name).name != prompt_name:
                raise ValueError('Unsafe task identity or prompt path')
            prompt = (MATERIAL/prompt_name).read_bytes()
            for name, files in arms.items():
                cell = stage/'cells'/f'{tid}-{name}'
                for relative, content in files.items():
                    dest = cell/'ui-spec'/relative
                    dest.parent.mkdir(parents=True, exist_ok=True); dest.write_bytes(content)
                (cell/'TASK.md').write_bytes(prompt)
                entry = {'task':tid, 'arm':name, 'status':'prepared_not_run',
                         'prompt_sha256':digest(prompt), 'inputs_to_freeze':task['inputs_to_freeze']}
                # Evaluator metadata is not part of the participant skill or prompt.
                record['cells'].append(entry)
        (stage/'EXPERIMENT.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        (stage/'PROTOCOL.md').write_bytes((MATERIAL/'PROTOCOL.md').read_bytes())
        stage.rename(output)
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return record


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline',type=Path,required=True,help='Exact local v1.13.0 skill directory')
    parser.add_argument('--output',type=Path,required=True,help='New directory; never overwrite')
    args=parser.parse_args()
    try:
        result=build(args.baseline,args.output)
        print(json.dumps({'status':result['status'],'cells':len(result['cells']),
                          'model_runs_executed':0,'output':str(args.output)},indent=2))
        return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(f'prepare_design_experiment: {exc}',file=__import__('sys').stderr)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
