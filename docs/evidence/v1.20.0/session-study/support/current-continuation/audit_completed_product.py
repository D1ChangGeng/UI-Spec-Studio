#!/usr/bin/env python3
"""Check retained supplementary refs, actual view returns and anonymous pack bytes."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--run',type=Path,required=True)
    parser.add_argument('--mapping',type=Path,required=True)
    parser.add_argument('--pack',type=Path,required=True)
    args=parser.parse_args()
    repo=args.repo.resolve();runpath=args.run.resolve()
    run=json.loads(runpath.read_text());snapshot=json.loads((runpath.parent/'snapshot.json').read_text())
    sys.path.insert(0,str(repo/'tools'))
    from check_adaptive_release import artifact,candidate_identity,EvidenceError,BASE
    from session_simulation_evidence import SessionEvidence
    checked=set()
    def walk(value):
        if isinstance(value,dict):
            if 'path' in value and 'sha256' in value:
                artifact(repo,value);checked.add(value['path'])
            for child in value.values():walk(child)
        elif isinstance(value,list):
            for child in value:walk(child)
    check=SessionEvidence(repo,{},artifact,candidate_identity,EvidenceError,BASE)
    primary=check.participant(run)
    for child in run['children']:check.participant(child,parent=primary)
    check.product(run['product_evidence_index'],run['cell_id'],primary)
    product=json.loads(artifact(repo,run['product_evidence_index']))
    walk(run);walk(product);walk(json.loads(artifact(repo,run['execution_audit'])))
    views=[]
    for view in product['viewed_screenshots']:
        exports=json.loads(artifact(repo,view['view_export']))
        calls=exports if isinstance(exports,list) else [exports]
        screenshot_raw=artifact(repo,view['screenshot'])
        matches=[]
        for call in calls:
            if call.get('tool')!='view_image':continue
            original=Path(call.get('arguments',{}).get('path',''))
            try:relative=original.relative_to(Path(snapshot['source_workspace'])).as_posix()
            except ValueError:continue
            if snapshot['workspace_files'].get(relative)!=view['screenshot']['sha256']:continue
            url=call.get('result',{}).get('image_url')
            if not isinstance(url,str) or ';base64,' not in url:raise ValueError('Actual PNG return absent')
            raw=base64.b64decode(url.split(';base64,',1)[1],validate=True)
            if not raw.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Actual returned PNG invalid')
            matches.append({'screenshot_sha256':sha(screenshot_raw),'returned_png_sha256':sha(raw),'return_byte_identical':raw==screenshot_raw})
        if not matches:raise ValueError('Primary screenshot has no matching actual view request')
        views.extend(matches)
    source=Path(snapshot['source_workspace'])
    actual={p.relative_to(source).as_posix():sha(p.read_bytes()) for p in source.rglob('*') if p.is_file() and not p.is_symlink()
            and not any(x in {'.git','__pycache__','.pytest_cache'} for x in p.relative_to(source).parts)
            and not p.relative_to(source).as_posix().startswith('app/node_modules/')}
    if actual!=snapshot['workspace_files']:raise ValueError('Source changed after immutable snapshot')
    failed=[]
    for path in sorted(source.rglob('command.json')):
        if 'node_modules' in path.parts:continue
        data=json.loads(path.read_text())
        code=data.get('returncode')
        if code not in (None,0):failed.append({'path':path.relative_to(source).as_posix(),'returncode':code,'status':data.get('status')})
    mapping=json.loads(args.mapping.read_text());pack=args.pack.resolve()
    if mapping['product_evidence_sha256']!=run['product_evidence_index']['sha256']:raise ValueError('Anonymous mapping product mismatch')
    for name,digest in mapping['app_files'].items():
        path=pack/'products'/mapping['anonymous_id']/name
        if sha(path.read_bytes())!=digest:raise ValueError('Anonymous app byte mismatch')
    for item in mapping['capture_mapping']:
        if sha((pack/item['anonymous_file']).read_bytes())!=item['original']['sha256']:raise ValueError('Anonymous capture byte mismatch')
    for original,target in [('TASK.md','TASK.md'),('INPUT.md','ORIGINAL-INPUT.md')]:
        raw=(pack/'products'/mapping['anonymous_id']/target).read_bytes()
        if sha(raw)!=snapshot['workspace_files'][original]:raise ValueError('Anonymous task/input byte mismatch')
    report={'status':'passed','kind':'coordinator supplementary archive/record/anonymous-pack consistency; not independent product judgment',
            'cell_id':run['cell_id'],'attempt_kind':run['attempt_kind'],'verified_repository_refs':len(checked),
            'verified_source_files':len(actual),'primary_actual_view_returns':views,'children':len(run['children']),
            'retained_nonzero_command_results':failed,'anonymous_product':mapping['anonymous_id'],
            'verified_anonymous_app_files':len(mapping['app_files']),'verified_anonymous_captures':len(mapping['capture_mapping']),
            'candidate_identity':candidate_identity(repo),'scope':'Retained participant/child/product refs, matching original screenshot requests and returned PNG data, immutable source readback, and anonymous pack byte identities. Nonzero original command results are preserved without converting them into an automatic acceptance judgment.'}
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
