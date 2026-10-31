from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,zipfile
repo=Path("/workspace/scratch/708e8b7f118e/UI-Spec-Studio")
sys.path.insert(0,str(repo/"tools"))
from package import archive
out=Path("/workspace/scratch/708e8b7f118e/validation-work/adapter-preflight")
out.mkdir(exist_ok=False)
source=repo/"integrations/codex"
asset=out/"ui-spec-codex-1.20.0.zip"
items=[("ui-spec-codex/"+p.relative_to(source).as_posix(),p.read_bytes()) for p in source.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix!=".pyc"]
items.append(("ui-spec-codex/LICENSE",(repo/"LICENSE").read_bytes()))
archive(asset,items)
asset_hash=hashlib.sha256(asset.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory(prefix="ui-spec-standalone-check-") as td:
    base=Path(td);bundle=base/"bundle"
    with zipfile.ZipFile(asset) as z:z.extractall(bundle)
    install=bundle/"ui-spec-codex/install.py";project=base/"product"
    (project/".codex").mkdir(parents=True)
    original=b"# user fixture; preserve exactly\\nmodel = \\"existing-choice\\"\\n".decode("unicode_escape").encode()
    (project/".codex/config.toml").write_bytes(original)
    (project/"AGENTS.md").write_text("Existing project instructions.\n")
    results=[]
    for action,extra in [("install",["--dry-run"]),("install",[]),("status",[]),("install",[])]:
        cmd=[sys.executable,str(install),action,"--project",str(project),*extra]
        r=subprocess.run(cmd,text=True,capture_output=True)
        print(json.dumps({"command":cmd,"returncode":r.returncode,"stdout":r.stdout,"stderr":r.stderr}))
        if r.returncode:raise RuntimeError("CLI failed")
        results.append({"action":action,"extra":extra,"returncode":r.returncode})
    manifest=json.loads((bundle/"ui-spec-codex/manifest.json").read_text())
    roles={}
    for name,entry in manifest["roles"].items():
        path=project/".codex"/entry["path"]
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual==entry["sha256"]
        roles[name]=actual
    assert len(roles)==4
    assert (project/".codex/config.toml").read_bytes().startswith(original)
    assert (project/"AGENTS.md").read_text()=="Existing project instructions.\n"
    cmd=[sys.executable,str(install),"uninstall","--project",str(project)]
    r=subprocess.run(cmd,text=True,capture_output=True)
    print(json.dumps({"command":cmd,"returncode":r.returncode,"stdout":r.stdout,"stderr":r.stderr}))
    if r.returncode:raise RuntimeError("Uninstall failed")
    assert (project/".codex/config.toml").read_bytes()==original
    assert not list((project/".codex/agents").glob("*.toml"))
    summary={"asset":asset.name,"asset_sha256":asset_hash,"status":"passed","roles_verified":roles,"operations":results+[{"action":"uninstall","returncode":r.returncode}],"scope":"Actual standalone archive extraction and CLI lifecycle in a disposable fixture; no native model execution or role-binding claim. The full suite separately covers upgrade/conflict fixtures."}
    (out/"report.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
