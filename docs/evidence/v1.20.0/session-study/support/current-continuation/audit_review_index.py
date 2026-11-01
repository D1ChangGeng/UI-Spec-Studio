#!/usr/bin/env python3
"""Verify final reviewer refs, frozen cohort identity and deterministic schema projection."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'continuation'))
from review_snapshot_io import read_snapshot


def sha(raw):return hashlib.sha256(raw).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--configuration',type=Path,required=True)
    args=parser.parse_args();repo=args.repo.resolve();cfg=json.loads(args.configuration.read_text())
    out=repo/cfg['output_directory'];review=json.loads((out/'review.json').read_text())
    snapshot_path=repo/cfg['snapshot_repository_path'];snapshot=read_snapshot(snapshot_path)
    source=Path(snapshot['source_workspace'])
    sys.path.insert(0,str(repo/'tools'))
    from check_adaptive_release import artifact,candidate_identity,EvidenceError,BASE
    from session_simulation_evidence import SessionEvidence
    check=SessionEvidence(repo,{},artifact,candidate_identity,EvidenceError,BASE)
    checked=set()
    def walk(value):
        if isinstance(value,dict):
            if 'path' in value and 'sha256' in value:
                artifact(repo,value);checked.add(value['path'])
            for child in value.values():walk(child)
        elif isinstance(value,list):
            for child in value:walk(child)
    products={};parents=set()
    for name in cfg['run_records']:
        run=json.loads((repo/name).read_text());primary=check.participant(run);parents.add(run['parent_agent_id'])
        for child in run['children']:check.participant(child,parent=primary)
        products[run['cell_id']]=(run['product_evidence_index'],check.product(run['product_evidence_index'],run['cell_id'],primary))
    agent=check.participant(review)
    if agent in parents:raise ValueError('Reviewer is a supplied coordinator')
    if len(products)!=16 or len(review['reviewed_products'])!=16:raise ValueError('Core review must retain original sixteen products')
    seen=set()
    for row in review['reviewed_products']:
        cell=row['cell_id']
        if cell in seen or cell not in products or row['product_evidence_sha256']!=products[cell][0]['sha256']:raise ValueError('Core product mapping differs')
        seen.add(cell);check.views(row['viewed_screenshots'],products[cell][1],agent)
    if seen!=set(products):raise ValueError('Core reviewer coverage differs')
    walk(review)
    declaration=json.loads(artifact(repo,review['review_declaration']))
    if review['original_reviewer_declaration']!=declaration:raise ValueError('Original declaration was altered')
    for key in ['outcome','reviewed_at','condition_blind','blinding_limitations']:
        if review[key]!=declaration[key]:raise ValueError('Reviewer judgment field changed: '+key)
    projection=json.loads(artifact(repo,review['declaration_projection']));walk(projection)
    def compare(original,projected,pointer=''):
        if isinstance(original,dict):
            for key,value in original.items():
                here=pointer+'/'+key
                if key in {'scope','limitations'} and isinstance(value,list):
                    if projected[key]!='\n'.join(value):raise ValueError('Ordered original text was changed: '+here)
                elif key=='repair_evidence':
                    if len(projected[key])!=len(value):raise ValueError('No-repair verification item lost')
                    for old,new in zip(value,projected[key]):
                        if old['kind']!=new['kind'] or old['path']!=new['original_source_path']:raise ValueError('No-repair evidence attribution changed')
                        relative=Path(old['path']).relative_to(source).as_posix()
                        if new['sha256']!=snapshot['file_hashes'][relative]:raise ValueError('No-repair verification bytes changed')
                        artifact(repo,new)
                else:compare(value,projected[key],here)
        elif isinstance(original,list):
            if len(original)!=len(projected):raise ValueError('Original list length changed')
            for i,(old,new) in enumerate(zip(original,projected)):compare(old,new,pointer+'/'+str(i))
        elif original!=projected:raise ValueError('Reviewer value changed: '+pointer)
    compare(declaration,{**declaration,**{key:review[key] for key in ['scope','limitations','final_runtime_acceptance']}})
    eligible={p.relative_to(source).as_posix():sha(p.read_bytes()) for p in source.rglob('*')
              if p.is_file() and not p.is_symlink() and not any(part in {'node_modules','.git','__pycache__','.pytest_cache'} for part in p.relative_to(source).parts)}
    if eligible!=snapshot['file_hashes']:raise ValueError('Eligible reviewer source inventory differs from frozen snapshot')
    links={p.relative_to(source).as_posix():os.readlink(p) for p in source.rglob('*') if p.is_symlink()}
    if links!=snapshot.get('symbolic_links',{}):raise ValueError('Reviewer symbolic link metadata differs')
    core=json.loads((source/'products.json').read_text());supplementary=json.loads((source/'supplementary-products.json').read_text())
    if len(core)!=16 or len(supplementary)!=2:raise ValueError('Original/supplementary cohorts were rebound')
    report={'status':'passed','kind':'coordinator participant/view/ref/projection/source consistency; not a new reviewer judgment',
            'reviewer':agent,'core_products':len(core),'separate_supplementary_products':len(supplementary),
            'verified_repository_refs':len(checked),'eligible_reviewer_source_files':len(eligible),'symbolic_links':len(links),
            'projection_operations':len(projection['transforms']),'normalized_text_fields':sum('join every' in row['operation'] for row in projection['transforms']),
            'no_repair_verification_lists':sum('map each actual' in row['operation'] for row in projection['transforms']),
            'final_report_sha256':review['result']['sha256'],'original_declaration_sha256':review['review_declaration']['sha256'],
            'outcome':review['outcome'],'condition_blind':review['condition_blind'],'reviewed_at':review['reviewed_at'],
            'candidate_identity':candidate_identity(repo),
            'scope':'No reviewer outcome, findings, scope text, exclusions or repair judgment authored here. Every original ordered list entry and no-repair verification item retained; original/supplementary cohorts stay separate. Supplied input symlink targets are recorded without traversal; actual dependency/git/bytecode/test caches excluded; disposable/stateful copies included.'}
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
