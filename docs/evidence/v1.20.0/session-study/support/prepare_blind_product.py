#!/usr/bin/env python3
"""Prepare condition-masked, byte-identical product materials for independent review."""
from pathlib import Path
import argparse,hashlib,json,shutil,struct,sys
from replay_snapshot import extract

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cell',required=True);a=p.parse_args()
    root=Path('/workspace/scratch/708e8b7f118e');repo=root/'UI-Spec-Studio';study=repo/'docs/evidence/v1.20.0/session-study';review=root/'ui-study/review-pack'
    assignment=next(x for x in json.loads((study/'coordination/blind-allocation.json').read_text())['products'] if x['cell_id']==a.cell)
    label=assignment['anonymous_id'];task=assignment['task'];run=study/'runs'/a.cell;product=json.loads((run/'product-evidence.json').read_text());snapshot=json.loads((run/'snapshot.json').read_text())
    replay=root/'ui-study/replay-audit'/a.cell;out=review/'products'/label
    out.mkdir(parents=True,exist_ok=False)
    shutil.copytree(replay/'app',out/'app')
    shutil.copyfile(replay/'TASK.md',out/'TASK.md');shutil.copyfile(replay/'INPUT.md',out/'ORIGINAL-INPUT.md')
    foundation=review/'foundations'/task
    if not foundation.exists():
        foundation.mkdir(parents=True)
        for path in sorted((study/'inputs').glob(task+'-input*.zip')):extract(path,foundation)
    captures=[];mapping=[]
    viewed={x['screenshot']['sha256'] for x in product['viewed_screenshots']}
    for i,ref in enumerate(product['screenshots'],1):
        source=repo/ref['path'];target=out/'captures'/f'{i:03d}.png';target.parent.mkdir(exist_ok=True)
        shutil.copyfile(source,target);raw=target.read_bytes();width,height=struct.unpack('>II',raw[16:24])
        captures.append({'file':target.relative_to(out).as_posix(),'width':width,'height':height,'sha256':ref['sha256'],'opened_by_producer':ref['sha256'] in viewed})
        mapping.append({'anonymous_file':target.relative_to(review).as_posix(),'original':ref,'original_state_label':source.relative_to(run/'artifacts').as_posix()})
    write(out/'capture-index.json',{'product':label,'task_family':task,'captures':captures,'scope':'Original captured pixels copied byte for byte. Producer viewing is recorded separately from independent review; captured states may span explicitly disclosed repair iterations.'})
    port=4500+int(label[1:])
    command=f'python3 -m http.server {port} --bind 127.0.0.1 --directory app'+('/dist' if task=='T2' else '')
    if task=='T3':command=f'cd app && PORT={port} ./start.sh'
    note=f'''# Product {label}\n\nRead TASK.md and ORIGINAL-INPUT.md for the unchanged task and supplied foundation contract. The app/ directory contains the frozen delivered product. Condition labels, role instructions, agent identities and producer judgments are withheld during initial review.\n\n## Preview\n\nFrom this product directory: {command}\n\nFor an interactive test that can change files or stored data, use a separate disposable copy. Do not edit this frozen product. The browser, Playwright and CJK font conditions are supplied in the common reviewer instructions. All content and service fixtures are synthetic and local.\n\n## Evidence\n\nThe PNGs listed in capture-index.json are actual captured pixels. Inspect the app at intended dimensions and meaningful states, using the original task rather than treating the number of captures as quality. A shared original source foundation is available at ../../foundations/{task}/.\n\nThe raw producer logs and self-assessment are withheld for the first blind judgment; they remain retained in the public study record and will be available for a separate evidence audit. Some captures precede narrowly scoped later state repairs; the delivered source is the frozen final product. Direct re-observation can resolve uncertainty.\n'''
    (out/'README.md').write_text(note)
    material={'schema_version':1,'kind':'coordinator-derived blinding map; not a tool output','anonymous_id':label,'cell_id':a.cell,'task':task,'product_evidence_sha256':digest(run/'product-evidence.json'),'snapshot_sha256':digest(run/'snapshot.json'),'app_files':{p.relative_to(out).as_posix():digest(p) for p in sorted((out/'app').rglob('*')) if p.is_file()},'capture_mapping':mapping,'masking':'Final app, original task/input and source foundation are available. No ALLOCATION, method, role files, cell identity, producer FINAL or producer visual judgment is supplied during initial review. Absolute metadata is absent from the neutral index.','limitations':'Source choices and product differences are inherently visible. Shared host access is controlled by instructions rather than a separate filesystem security boundary.'}
    write(study/'coordination'/f'blind-materials-{label}.json',material)
    print(json.dumps({'anonymous_product':label,'cell_id':a.cell,'app_files':len(material['app_files']),'captures':len(captures),'port':port}))
if __name__=='__main__':main()
