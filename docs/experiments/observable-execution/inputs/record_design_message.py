#!/usr/bin/env python3
"""Archive one actual outward message and its contemporary source for study replay.

This experiment-only recorder does not choose message timing or assess design.
Invoke from one isolated workspace, then send its returned message through the
host's commentary/final channel and the coordinator relay without rewriting it.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import zipfile


def record(root: Path, message: str, channel: str) -> dict:
    root = root.resolve(strict=True)
    if channel not in ('commentary', 'final') or not message.strip():
        raise ValueError('Use an actual nonempty outward message and channel')
    log = root/'outward'
    log.mkdir(exist_ok=True)
    number = len(list(log.glob('message-*.json'))) + 1
    identity = f'message-{number:03d}'
    target = log/f'{identity}.json'
    if target.exists():
        raise ValueError('Preserve an existing message')
    files = {}
    capture = log/f'{identity}-source.zip'
    with zipfile.ZipFile(capture, 'x', compression=zipfile.ZIP_DEFLATED) as bundle:
        for source in sorted((root/'app').rglob('*')):
            relative = source.relative_to(root)
            if source.is_symlink() or any(x in {'node_modules','.git','dist','__pycache__'} for x in relative.parts):
                continue
            if source.is_file():
                content = source.read_bytes()
                files[relative.as_posix()] = hashlib.sha256(content).hexdigest()
                bundle.writestr(relative.as_posix(), content)
    entry = {'id':identity, 'channel':channel,
             'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'text':message, 'text_sha256':hashlib.sha256(message.encode()).hexdigest(),
             'source_archive':capture.name,'source_files':files}
    target.write_text(json.dumps(entry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return entry


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--message-file',type=Path,required=True)
    parser.add_argument('--channel',choices=['commentary','final'],default='commentary')
    args=parser.parse_args()
    result=record(args.root,args.message_file.read_text(encoding='utf-8'),args.channel)
    print(json.dumps({'id':result['id'],'channel':result['channel'],'text':result['text'],
                      'text_sha256':result['text_sha256']},ensure_ascii=False))


if __name__=='__main__':
    main()
