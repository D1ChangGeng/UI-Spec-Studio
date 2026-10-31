#!/usr/bin/env python3
"""Check retained completed-cell identities without asserting release acceptance."""
from pathlib import Path
import argparse, hashlib, json, sys

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',type=Path,required=True)
    a=p.parse_args(); repo=a.repo.resolve();sys.path.insert(0,str(repo/'tools'))
    from check_adaptive_release import artifact,candidate_identity,EvidenceError,BASE
    from session_simulation_evidence import SessionEvidence
    from package import source_files
    study=repo/'docs/evidence/v1.20.0/session-study'
    plan=json.loads((study/'registration.json').read_text())
    assert candidate_identity(repo)==plan['candidate_source_identity']
    allowed={p.relative_to(repo).as_posix() for p in source_files(repo)}
    check=SessionEvidence(repo,{},artifact,candidate_identity,EvidenceError,BASE)
    checked=set(); results=[]
    def walk(obj):
        if isinstance(obj,dict):
            if 'path' in obj and 'sha256' in obj:
                artifact(repo,obj)
                if obj['path'] not in allowed:raise ValueError('Evidence omitted from source distribution: '+obj['path'])
                checked.add(obj['path'])
            for v in obj.values():walk(v)
        elif isinstance(obj,list):
            for v in obj:walk(v)
    for path in sorted((study/'runs').glob('*/run.json')):
        run=json.loads(path.read_text());agent=check.participant(run)
        for child in run['children']:check.participant(child,parent=agent)
        check.product(run['product_evidence_index'],run['cell_id'],agent)
        for ref in [run['product_evidence_index'],run['execution_audit']]:walk(json.loads(artifact(repo,ref)))
        walk(run)
        results.append({'cell_id':run['cell_id'],'agent_id':agent,'actual_children':len(run['children'])})
    print(json.dumps({'status':'passed','candidate_source_identity':candidate_identity(repo),'completed_cells':results,'verified_required_artifacts':len(checked),'scope':'Coordinator consistency and packaging check only. Not independent product judgment, engine attestation, or release approval.'},indent=2))
if __name__=='__main__':main()
