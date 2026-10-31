#!/usr/bin/env python3
"""Retain an unconfirmed workset and stage its unchanged registered input."""
from pathlib import Path
import argparse, datetime, hashlib, json, sys
ROOT=Path("/workspace/scratch/e1cfe6e447ee")
REPO=ROOT/"UI-Spec-Studio"
STUDY=REPO/"docs/evidence/v1.20.0/session-study"
sys.path.insert(0,str(STUDY/"support/continuation"))
from large_archives import archive_with_large_files, write_json
from replay_snapshot import extract
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files(w):return sorted(p for p in w.rglob("*") if p.is_file() and not set(p.relative_to(w).parts)&{".git","__pycache__",".pytest_cache"} and not p.relative_to(w).as_posix().startswith("app/node_modules/"))
p=argparse.ArgumentParser();p.add_argument("cells",nargs="+");a=p.parse_args()
plan=json.loads((STUDY/"registration.json").read_text())
for name in a.cells:
 c=next(x for x in plan["cells"] if x["id"]==name);w=Path(c["work_package"])
 out=STUDY/"incomplete-attempts"/(name+"-before-takeover");out.mkdir(parents=True,exist_ok=False)
 paths=files(w);before={p.relative_to(w).as_posix():digest(p) for p in paths}
 changed=[p for p in paths if before[p.relative_to(w).as_posix()]!=c["workspace_files"].get(p.relative_to(w).as_posix())]
 overlay=archive_with_large_files(w,changed,out,"workspace-overlay")
 snapshot={"schema_version":1,"cell_id":name,"captured_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"kind":"coordinator byte snapshot of unconfirmed prior attempt, not a completion record","source_workspace":str(w),"workspace_files":before,"workspace_modes":{p.relative_to(w).as_posix():oct(p.stat().st_mode&0o777) for p in paths},"changed_or_added":[p.relative_to(w).as_posix() for p in changed],"deleted_paths":sorted(set(c["workspace_files"])-set(before)),"method_changes":{n:before.get("method/"+n) for n,h in c["method_files"].items() if before.get("method/"+n)!=h},"role_changes":{role:before.get("roles/"+role+".toml") for role,h in c["role_instruction_files"].items() if before.get("roles/"+role+".toml")!=h},"overlay":overlay,"excluded":"app/node_modules, .git, __pycache__, .pytest_cache; external Python/browser/font runtime"}
 assert before=={p.relative_to(w).as_posix():digest(p) for p in files(w)},"Workset changed during snapshot"
 write_json(out/"snapshot.json",snapshot)
 write_json(out/"ATTEMPT-STATUS.json",{"cell_id":name,"status":"terminal_notification_unavailable_to_takeover","observed_final_report":(w/"FINAL.md").exists(),"counted_as_completed_run":False,"scope":"Original files retained before a fresh attempt. This does not assert the previous agent's current engine state."})
 stage=ROOT/"ui-study/staged"/name;stage.mkdir(parents=True,exist_ok=False)
 for ref in c["input_artifacts"]:
  z=REPO/ref["path"];assert digest(z)==ref["sha256"]
  prefix="method/" if z.name.startswith("method-v") else ("roles/" if z.name=="distributed-role-instructions.zip" else "")
  extract(z,stage,prefix)
 assert {p.relative_to(stage).as_posix():digest(p) for p in stage.rglob("*") if p.is_file()}==c["workspace_files"]
 print(json.dumps({"cell":name,"retained_files":len(before),"changed_files":len(changed),"staged_files":len(c["workspace_files"]),"method_changes":len(snapshot["method_changes"]),"role_changes":len(snapshot["role_changes"])},sort_keys=True),flush=True)

