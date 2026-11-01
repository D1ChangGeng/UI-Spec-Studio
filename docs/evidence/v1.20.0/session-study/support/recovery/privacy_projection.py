#!/usr/bin/env python3
"""Keep session-bearing research originals private and publish explicit projections."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import re
import shutil
import zipfile
from urllib.parse import parse_qsl, quote, urlsplit


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--private-archive', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--cell', required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    if args.output.exists() or args.private_archive.exists() or args.report.exists():
        raise FileExistsError('Use fresh projection, private archive and report paths')
    files = sorted(p for p in source.rglob('*') if p.is_file() and not p.is_symlink())
    originals = {p.relative_to(source).as_posix(): sha(p.read_bytes()) for p in files}
    tokens, header_names, query_names = set(), set(), set()
    for path in files:
        if path.suffix != '.json':
            continue
        try:
            value = json.loads(path.read_text())
        except (ValueError, UnicodeError):
            continue
        if not isinstance(value, dict):
            continue
        headers = value.get('headers', {})
        if isinstance(headers, dict):
            for key, text in headers.items():
                if key.lower() in {'set-cookie', 'cookie'}:
                    header_names.add(key.lower())
                    for name, token in re.findall(r'(?:^|[,;]\s*)([^=;,\s]+)=([^;,\r\n]*)', str(text)):
                        if name.lower() in {'path', 'domain', 'expires', 'max-age', 'samesite'}:
                            continue
                        token = token.strip().strip('"')
                        if len(token) >= 8:
                            tokens.add(token)
                elif key.lower() in {'authorization', 'proxy-authorization', 'x-api-key'}:
                    header_names.add(key.lower())
                    token = str(text).strip()
                    if len(token) >= 8:
                        tokens.add(token)
        for key in ('url', 'final_url'):
            for name, token in parse_qsl(urlsplit(value.get(key, '')).query, keep_blank_values=True):
                if name.lower() in {'token', 'access_token', 'refresh_token', 'session_id', 'dd-api-key', 'client_id'} and len(token) >= 8:
                    query_names.add(name)
                    tokens.add(token)
    if not tokens:
        raise ValueError('No concrete session-bearing values found; projection not justified')
    variants = set(tokens) | {quote(token, safe='') for token in tokens}
    variants |= {json.dumps(token, ensure_ascii=False)[1:-1] for token in tokens}
    ordered = sorted(variants, key=lambda token: (-len(token), token))
    shutil.copytree(source, args.output, copy_function=shutil.copy2)
    changed = []
    for path in files:
        raw = path.read_bytes()
        try:
            text = raw.decode('utf-8')
        except UnicodeError:
            continue
        replacement = text
        for token in ordered:
            replacement = replacement.replace(token, '[WITHHELD_SESSION_VALUE]')
        if replacement == text:
            continue
        relative = path.relative_to(source).as_posix()
        if relative.startswith(('app/', 'method/', 'roles/')):
            raise ValueError('Unexpected product/method/role source match; requires manual review')
        projected = replacement.encode('utf-8')
        if path.suffix == '.json':
            json.loads(projected)
        (args.output / relative).write_bytes(projected)
        changed.append({'path': relative, 'original_sha256': sha(raw),
                        'public_sha256': sha(projected), 'original_bytes': len(raw),
                        'public_bytes': len(projected)})
    if not changed:
        raise ValueError('Detected values produced no privacy projection')
    args.private_archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.private_archive, 'w', zipfile.ZIP_DEFLATED) as archive:
        for row in changed:
            archive.writestr(row['path'], (source / row['path']).read_bytes())
        archive.writestr('ORIGINAL-WORKSPACE-HASHES.json', json.dumps(originals, ensure_ascii=False, indent=2) + '\n')
        archive.writestr('README.txt',
            'Private, unchanged research originals for ' + args.cell + '.\n'
            'These files contain response cookies/session identifiers from isolated signed-out public-source observations. Do not publish them.\n'
            'Reconstruct the public workspace from its registered inputs and public overlay, then overlay only the original evidence/ paths in this ZIP. '
            'The result must match every path/SHA-256 in ORIGINAL-WORKSPACE-HASHES.json. No product, method, role, screenshot or image-return bytes are changed by the public projection.\n')
    with zipfile.ZipFile(args.private_archive) as archive:
        assert archive.testzip() is None
        for row in changed:
            assert sha(archive.read(row['path'])) == row['original_sha256']
    actual = {p.relative_to(args.output).as_posix(): sha(p.read_bytes())
              for p in args.output.rglob('*') if p.is_file()}
    assert set(actual) == set(originals)
    assert {name for name in actual if actual[name] != originals[name]} == {row['path'] for row in changed}
    record = {'schema_version': 1, 'kind': 'explicit coordinator privacy projection; not an original tool response',
              'cell_id': args.cell, 'recorded_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'source_workspace': str(source), 'public_projection_workspace': str(args.output),
              'private_archive_name': args.private_archive.name,
              'private_archive_sha256': sha(args.private_archive.read_bytes()),
              'private_archive_bytes': args.private_archive.stat().st_size,
              'original_workspace_file_count': len(originals), 'changed_file_count': len(changed),
              'matched_header_names': sorted(header_names), 'matched_query_parameter_names': sorted(query_names),
              'replacement': '[WITHHELD_SESSION_VALUE]', 'files': changed,
              'scope': 'Only exact session-bearing values and their encoded forms are replaced in the public copies. Original participant files remain unchanged and the private ZIP retains every affected original byte. All product/method/role source, screenshots, image-view returns, outcome reports and unaffected evidence remain original. This is a publication projection, not another participant execution or revised result.',
              'private_reconstruction': 'Apply original evidence/ members from the private ZIP over the reconstructed public workspace; verify all original hashes in ORIGINAL-WORKSPACE-HASHES.json. The private ZIP is delivered to the repository owner separately, not uploaded to public GitHub.'}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: record[key] for key in ('cell_id', 'original_workspace_file_count', 'changed_file_count', 'private_archive_name', 'private_archive_bytes', 'private_archive_sha256')}, indent=2))


if __name__ == '__main__':
    main()
