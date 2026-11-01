#!/usr/bin/env python3
"""Retain actual command stdout/stderr for the session study, without environment dumps."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    parser.add_argument('--cwd',required=True)
    parser.add_argument('--timeout',type=int,default=600)
    parser.add_argument('command',nargs=argparse.REMAINDER)
    args=parser.parse_args()
    command=args.command[1:] if args.command[:1]==['--'] else args.command
    if not command:parser.error('command required')
    output=Path(args.output);output.mkdir(parents=True,exist_ok=False)
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic()
    metadata={'schema_version':1,'evidence_kind':'original_subprocess_capture','command':command,'cwd':args.cwd,'started_at':start,'timeout_seconds':args.timeout,'environment':'inherited; values not exported'}
    with (output/'stdout.txt').open('wb') as out,(output/'stderr.txt').open('wb') as err:
        try:
            result=subprocess.run(command,cwd=args.cwd,stdout=out,stderr=err,timeout=args.timeout,check=False)
            metadata.update(status='completed',returncode=result.returncode)
        except subprocess.TimeoutExpired:
            metadata.update(status='timed_out',returncode=124)
        except OSError as exc:
            err.write(str(exc).encode());metadata.update(status='failed_to_start',returncode=127)
    metadata.update(ended_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_seconds=round(time.monotonic()-clock,6))
    metadata['artifacts']={name:{'bytes':(output/name).stat().st_size,'sha256':hashlib.sha256((output/name).read_bytes()).hexdigest()} for name in ('stdout.txt','stderr.txt')}
    (output/'command.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    for name,stream in [('stdout.txt',sys.stdout.buffer),('stderr.txt',sys.stderr.buffer)]:
        stream.write((output/name).read_bytes());stream.flush()
    print(json.dumps({'capture':str(output),'returncode':metadata['returncode'],'wall_seconds':metadata['wall_seconds']}))
    return metadata['returncode']

if __name__=='__main__':raise SystemExit(main())
