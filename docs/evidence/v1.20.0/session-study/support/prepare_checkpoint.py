#!/usr/bin/env python3
"""Describe a committed evidence checkpoint for content-addressed GitHub delivery."""
from pathlib import Path
import argparse,json,subprocess

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    def git(*args):return subprocess.check_output(['git','-C',str(a.repo),*args])
    base=git('rev-parse',a.base).decode().strip();head=git('rev-parse','HEAD').decode().strip()
    names=git('diff','--name-status','--no-renames','-z',base,head).decode().split('\0');rows=[]
    for i in range(0,len(names)-1,2):
        status,path=names[i:i+2]
        if status=='D':rows.append({'path':path,'mode':'100644','type':'blob','sha':None,'delete':True});continue
        mode,kind,sha=git('ls-tree',head,'--',path).decode().split('\t')[0].split()
        if kind!='blob' or mode not in {'100644','100755'}:raise ValueError('Unexpected file type: '+path)
        raw=git('cat-file','blob',sha)
        if len(raw)>11700000:raise ValueError('Blob exceeds safe connector request size: '+path)
        try:raw.decode('utf-8');is_text=True
        except UnicodeError:is_text=False
        rows.append({'path':path,'mode':mode,'type':kind,'sha':sha,'bytes':len(raw),'text':is_text})
    result={'repo':str(a.repo.resolve()),'repository_full_name':'D1ChangGeng/UI-Spec-Studio','branch_name':'work/v1.20.0-recovery-20261101','base_commit':base,'base_tree':git('rev-parse',base+'^{tree}').decode().strip(),'local_head':head,'local_tree':git('rev-parse',head+'^{tree}').decode().strip(),'message':git('log','-1','--format=%B').decode().strip(),'files':rows}
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'local_head':head,'tree':result['local_tree'],'files':len(rows),'bytes':sum(x.get('bytes',0) for x in rows),'deletes':sum(x.get('delete',False) for x in rows)}))
if __name__=='__main__':main()
