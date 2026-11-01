#!/usr/bin/env python3
"""Preserve observed study files as byte-verified, bounded ZIP members."""
from pathlib import Path
import argparse, hashlib, io, json, zipfile

def digest(raw): return hashlib.sha256(raw).hexdigest()
def write_json(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")

def bounded_archives(source, paths, output, stem, limit=8_000_000):
    output.mkdir(parents=True,exist_ok=True)
    groups=[]; current=[]; total=22
    for path in sorted(paths,key=lambda p:p.relative_to(source).as_posix()):
        if path.is_symlink(): raise ValueError("Symlink requires explicit review: "+str(path))
        name=path.relative_to(source).as_posix(); raw=path.read_bytes()
        buffer=io.BytesIO()
        with zipfile.ZipFile(buffer,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            z.writestr(name,raw)
        estimate=len(buffer.getvalue())+len(name.encode())*2+200
        if estimate>limit: raise ValueError("A single compressed member exceeds the bound: "+name)
        if current and total+estimate>limit: groups.append(current);current=[];total=22
        current.append((name,raw));total+=estimate
    if current:groups.append(current)
    artifacts=[];members=[]
    for number,items in enumerate(groups,1):
        archive=output/(stem+f"-part-{number:02d}.zip")
        if archive.exists():raise FileExistsError(archive)
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for name,raw in items:
                info=zipfile.ZipInfo(name,date_time=(2026,11,1,0,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.create_system=3
                info.external_attr=0o100644<<16
                z.writestr(info,raw)
                members.append({"path":name,"bytes":len(raw),"sha256":digest(raw),"archive":archive.name})
        with zipfile.ZipFile(archive) as z:
            if z.testzip() is not None:raise ValueError("Archive CRC failed")
            for name,raw in items:
                if z.read(name)!=raw:raise ValueError("Archive member differs")
        raw=archive.read_bytes()
        if len(raw)>limit:raise ValueError("Actual archive exceeds bound")
        artifacts.append({"file":archive.name,"bytes":len(raw),"sha256":digest(raw),"members":len(items)})
    return {"archives":artifacts,"members":members}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("source",type=Path);p.add_argument("output",type=Path);p.add_argument("--stem",default="original-files")
    p.add_argument("--list",type=Path)
    a=p.parse_args()
    paths=[a.source/line for line in a.list.read_text().splitlines()] if a.list else [f for f in a.source.rglob("*") if f.is_file() and "__pycache__" not in f.parts]
    report=bounded_archives(a.source,paths,a.output,a.stem)
    write_json(a.output/(a.stem+"-inventory.json"),report)
    print(json.dumps({"archives":report["archives"],"total_members":len(report["members"])}))
if __name__=="__main__":main()
