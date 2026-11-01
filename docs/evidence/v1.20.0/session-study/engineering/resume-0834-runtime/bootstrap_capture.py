#!/usr/bin/env python3
import argparse, datetime, hashlib, json, pathlib, subprocess, sys
p=argparse.ArgumentParser()
p.add_argument("--name", required=True)
p.add_argument("--cwd", default="/tmp")
p.add_argument("command", nargs=argparse.REMAINDER)
a=p.parse_args()
cmd=a.command[1:] if a.command and a.command[0]=="--" else a.command
root=pathlib.Path(__file__).parent
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(cmd,cwd=a.cwd,capture_output=True)
stdout=root/(a.name+".stdout")
stderr=root/(a.name+".stderr")
stdout.write_bytes(r.stdout)
stderr.write_bytes(r.stderr)
record={"command":cmd,"cwd":a.cwd,"started_at":started,"finished_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"returncode":r.returncode,"stdout":str(stdout),"stderr":str(stderr),"stdout_sha256":hashlib.sha256(r.stdout).hexdigest(),"stderr_sha256":hashlib.sha256(r.stderr).hexdigest(),"capture":"bootstrap capture used before repository capture_command.py available"}
(root/(a.name+".status.json")).write_text(json.dumps(record,indent=2)+"\n")
sys.stdout.buffer.write(r.stdout)
sys.stderr.buffer.write(r.stderr)
raise SystemExit(r.returncode)
