#!/usr/bin/env python3
"""Run a project command and retain actual command/output evidence."""
import datetime,hashlib,json,os,pathlib,subprocess,sys,time
args=sys.argv[1:]
if args and args[0]=='--':args=args[1:]
if not args:raise SystemExit('usage: python tools/run.py -- command args...')
root=pathlib.Path(__file__).resolve().parents[1]
folder=root/'evidence'/'commands';folder.mkdir(parents=True,exist_ok=True)
start=time.time(); stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
record={'started_at':stamp,'argv':args,'cwd':os.getcwd()}
index=len(list(folder.glob('*.json')))+1
try:
 p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 out=p.stdout;record['exit_code']=p.returncode
except Exception as e:
 out=(repr(e)+'\n').encode();record['exit_code']=127
record.update(elapsed_seconds=round(time.time()-start,3),output_sha256=hashlib.sha256(out).hexdigest(),output_file=f'{index:04}.txt')
(folder/f'{index:04}.txt').write_bytes(out)
(folder/f'{index:04}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
sys.stdout.buffer.write(out);raise SystemExit(record['exit_code'])
