#!/usr/bin/env python3
"""Scan exact evidence bytes for sensitive fields; output paths/categories only."""
import argparse
import collections
import datetime
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import parse_qsl, urlsplit
import zipfile

SENSITIVE = {'authorization', 'proxy-authorization', 'cookie', 'set-cookie', 'x-api-key',
             'access_token', 'refresh_token', 'session_id', 'id_token', 'client_secret', 'private_key'}
QUERY = {'token', 'access_token', 'refresh_token', 'session_id', 'api_key', 'apikey', 'sig', 'signature', 'x-amz-signature'}
EMAIL = re.compile(r'(?<![\w.+-])[A-Za-z0-9.!#$%&\'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+')
SECRET = [('private_key_material', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')),
          ('github_token_shape', re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b')),
          ('aws_access_key_shape', re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')),
          ('openai_key_shape', re.compile(r'\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{35,}\b'))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--commit-only', action='store_true')
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    names = subprocess.check_output(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', args.commit], cwd=repo).decode().splitlines()
    study = repo / 'docs/evidence/v1.20.0/session-study'
    roots = ['coordination/final-session', 'engineering/final-session', 'review/coordinator-final',
             'supplementary-runs', 'support/final-session',
             'incomplete-attempts/T2-E-observer-r1-terminal-unavailable-1230',
             'incomplete-attempts/T3-C-r1-terminal-unavailable-1230']
    artifacts = [('commit:' + name, subprocess.check_output(['git', 'show', args.commit + ':' + name], cwd=repo)) for name in names]
    if not args.commit_only:
        artifacts.extend(('worktree:' + path.relative_to(repo).as_posix(), path.read_bytes())
                         for root in roots for path in sorted((study / root).rglob('*')) if path.is_file())
        # Split payload ZIPs are byte fragments, not complete nested archives.
        # Scan each reassembled original too, after validating every stored piece.
        for root in roots:
            snapshot_path = study / root / 'snapshot.json'
            if not snapshot_path.is_file():
                continue
            snapshot = json.loads(snapshot_path.read_text())
            for record in snapshot.get('overlay', {}).get('split_files', []):
                chunks = []
                for part in record['parts']:
                    part_path = snapshot_path.parent / part['file']
                    raw = part_path.read_bytes()
                    if hashlib.sha256(raw).hexdigest() != part['sha256']:
                        raise ValueError('Split archive hash differs')
                    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                        piece = archive.read(part['member'])
                    if hashlib.sha256(piece).hexdigest() != part['payload_sha256']:
                        raise ValueError('Split payload hash differs')
                    chunks.append(piece)
                raw = b''.join(chunks)
                if len(raw) != record['bytes'] or hashlib.sha256(raw).hexdigest() != record['sha256']:
                    raise ValueError('Reassembled original identity differs')
                artifacts.append(('reassembled:' + snapshot_path.parent.relative_to(repo).as_posix() + '!' + record['path'], raw))
    findings, inventory = [], []
    counters = collections.Counter()

    def scan(label, raw, depth=0):
        inventory.append({'path': label, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
        counters['inspected_objects'] += 1
        if raw.startswith(b'PK\x03\x04') and depth < 3:
            try:
                with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                    for name in archive.namelist():
                        if not name.endswith('/'):
                            scan(label + '!' + name, archive.read(name), depth + 1)
            except zipfile.BadZipFile:
                category = 'expected_split_payload_fragment_scanned_after_reassembly' if 'large-object-' in label and label.endswith('!payload') else 'unreadable_zip'
                findings.append({'path': label, 'category': category})
            return
        try:
            text = raw.decode('utf-8')
        except UnicodeError:
            counters['binary_objects'] += 1
            return
        counters['text_objects'] += 1
        flags = collections.Counter()
        scanned_text = re.sub(r'data:[^\s\";]+;base64,[A-Za-z0-9+/=]+', '[RETAINED_BINARY_IMAGE_PAYLOAD]', text)
        for category, expression in SECRET:
            flags[category] += len(expression.findall(scanned_text))
        if '@' in scanned_text:
            flags['email_address_shape_for_manual_scope_review'] += len(set(EMAIL.findall(scanned_text)))
        # URL queries are checked independently of the surrounding export shape.
        for url in re.findall(r'https?://[^\s\"<>]+', scanned_text):
            try:
                for name, value in parse_qsl(urlsplit(url).query, keep_blank_values=True):
                    if name.lower() in QUERY and len(value) >= 8 and not any(part in value for part in ['WITHHELD', '<', '${']):
                        flags['sensitive_url_query:' + name.lower()] += 1
            except ValueError:
                pass

        def walk(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    normalized = str(key).lower().replace('-', '_')
                    normalized_sensitive = {key.replace('-', '_') for key in SENSITIVE}
                    if normalized in normalized_sensitive and isinstance(child, str) and child.strip() and not any(marker in child for marker in ['WITHHELD', '<redacted>', '[REDACTED]']):
                        flags['sensitive_json_field:' + str(key).lower()] += 1
                    walk(child)
            elif isinstance(value, list):
                # CDP/Playwright header arrays use {name, value} objects.
                for child in value:
                    if isinstance(child, dict) and str(child.get('name', '')).lower() in SENSITIVE and child.get('value'):
                        flags['sensitive_header_array:' + str(child['name']).lower()] += 1
                    walk(child)
        try:
            walk(json.loads(text))
        except (ValueError, RecursionError):
            if label.endswith(('.jsonl', '.network', '.trace', '.har')):
                for line in text.splitlines():
                    try:
                        walk(json.loads(line))
                    except (ValueError, RecursionError):
                        pass
        for category, count in flags.items():
            if count:
                findings.append({'path': label, 'category': category, 'occurrences': count})
    for index, (label, raw) in enumerate(artifacts):
        scan(label, raw)
        print(json.dumps({'scanned_top_level': index + 1, 'total_top_level': len(artifacts)}), flush=True)
    report = {'schema_version': 1, 'kind': 'coordinator privacy-pattern audit; manual context review required for matches',
              'commit': args.commit, 'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'commit_changed_files': len(names), 'top_level_objects': len(artifacts),
              'counts': dict(counters), 'flagged_objects': len({row['path'] for row in findings}),
              'findings': findings,
              'scope': 'Exact changed files in specified commit plus named pre-existing final-session evidence trees, including nested ZIP members. Paths/categories/counts only; no matched values or image pixels are printed. Binary pixels are not OCR-scanned. Pattern absence cannot establish absence of all personal or organization information; visible synthetic product/task context requires separate scope review.'}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    (output / 'scanned-identities.json').write_text(json.dumps(inventory, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
