#!/usr/bin/env python3
"""Index an actual fresh reviewer; copy judgments only from retained reviewer JSON."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'continuation'))
from review_snapshot_io import read_snapshot


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('configuration', type=Path)
    args = parser.parse_args()
    cfg = json.loads(args.configuration.read_text())
    repo = Path(cfg['repo']).resolve()
    output = (repo / cfg['output_directory']).resolve()
    output.relative_to(repo / 'docs/evidence/v1.20.0/session-study/continuation-2100')
    if (output / 'review.json').exists():
        raise FileExistsError('Existing participant indexes must not be overwritten')
    output.mkdir(parents=True, exist_ok=True)
    snapshot_path = (repo / cfg['snapshot_repository_path']).resolve()
    snapshot = read_snapshot(snapshot_path)
    source = Path(snapshot['source_workspace'])

    def reference(path):
        path = path.resolve()
        path.relative_to(repo)
        return {'path': path.relative_to(repo).as_posix(), 'sha256': digest(path.read_bytes())}

    def read_ref(ref):
        path = (repo / ref['path']).resolve()
        path.relative_to(repo)
        raw = path.read_bytes()
        if digest(raw) != ref['sha256']:
            raise ValueError('Retained reference differs: ' + ref['path'])
        return raw

    def original(name):
        ref = snapshot['direct_artifacts'][name]
        raw = read_ref(ref)
        if digest(raw) != snapshot['file_hashes'][name]:
            raise ValueError('Reviewer source differs from snapshot: ' + name)
        return ref, raw

    def export(ref, tool, scope):
        return {**ref, 'source': tool, 'scope': scope,
                'export_kind': 'faithful_conversation_export', 'synthetic': False}

    reviewer = cfg['reviewer_agent_id']
    spawn_ref = reference(repo / cfg['spawn_repository_path'])
    completion_ref = reference(repo / cfg['completion_repository_path'])
    spawn = json.loads(read_ref(spawn_ref))
    completion = json.loads(read_ref(completion_ref))
    if (spawn['result']['task_name'] != reviewer or spawn['request']['fork_turns'] != 'none'
            or completion.get('agent_id') != reviewer or completion.get('message_type') != 'FINAL_ANSWER'):
        raise ValueError('Actual fresh reviewer spawn and FINAL_ANSWER are required')
    prompt_ref = reference(repo / cfg['prompt_repository_path'])
    if read_ref(prompt_ref) != spawn['request']['message'].encode():
        raise ValueError('Review prompt must preserve the exact actual dispatch')
    products, prohibited = {}, {cfg.get('parent_agent_id', '/root')}
    for name in cfg['run_records']:
        path = repo / name
        run = json.loads(path.read_text())
        if run['cell_id'] in products:
            raise ValueError('Duplicate supplied run')
        prohibited.update([run['agent_id'], run['parent_agent_id']])
        prohibited.update(child['agent_id'] for child in run['children'])
        product = json.loads(read_ref(run['product_evidence_index']))
        products[run['cell_id']] = (run, product)
    if reviewer in prohibited:
        raise ValueError('Reviewer is not independent of supplied runs/coordinators')
    mappings = {}
    for name in cfg['mapping_repository_paths']:
        path = repo / name
        mapping = json.loads(path.read_text())
        if mapping['anonymous_id'] in mappings:
            raise ValueError('Duplicate anonymous mapping')
        mappings[mapping['anonymous_id']] = (mapping, reference(path))
    records_ref, records_raw = original(cfg.get('products_file', 'products.json'))
    records = json.loads(records_raw)
    if isinstance(records, dict):
        records = records['products']
    rows, seen, tools = [], set(), []
    for record in records:
        label = record['anonymous_product']
        mapping, mapping_ref = mappings[label]
        cell = mapping['cell_id']
        run, product = products[cell]
        if cell in seen or mapping['product_evidence_sha256'] != run['product_evidence_index']['sha256']:
            raise ValueError('Review maps duplicate or different frozen product')
        seen.add(cell)
        allowed = {(ref['path'], ref['sha256']) for ref in product['screenshots']}
        capture_map = {item['anonymous_file']: item['original'] for item in mapping['capture_mapping']}
        originals, exports = record['viewed_original_files'], record['view_exports']
        if not originals or len(originals) != len(exports):
            raise ValueError('Every original screenshot view needs its actual export')
        views = []
        for original_path, export_path in zip(originals, exports):
            matches = [ref for name, ref in capture_map.items() if original_path.endswith('/' + name)]
            if len(matches) != 1:
                raise ValueError('Original image does not uniquely match anonymous map: ' + original_path)
            image_ref = matches[0]
            if (image_ref['path'], image_ref['sha256']) not in allowed:
                raise ValueError('Original screenshot is outside frozen product index')
            if not read_ref(image_ref).startswith(b'\x89PNG\r\n\x1a\n'):
                raise ValueError('Original retained image is not PNG')
            relative = Path(export_path).relative_to(source).as_posix()
            view_ref, raw = original(relative)
            payload = json.loads(raw)
            calls = payload if isinstance(payload, list) else [payload]
            calls = [call for call in calls if isinstance(call, dict)
                     and call.get('tool') == 'view_image'
                     and call.get('arguments', {}).get('path') == original_path]
            if not calls:
                raise ValueError('Actual image request does not identify original screenshot')
            for call in calls:
                url = call.get('result', {}).get('image_url')
                if not isinstance(url, str) or ';base64,' not in url:
                    raise ValueError('Actual viewed image return is missing')
                returned = base64.b64decode(url.split(';base64,', 1)[1], validate=True)
                if not returned.startswith(b'\x89PNG\r\n\x1a\n'):
                    raise ValueError('Actual viewed image return is not PNG')
            tool = export(view_ref, 'view_image', 'Actual independent reviewer request and returned PNG pixels for the mapped original frozen product capture. Tool resizing, if present, remains part of the original return.')
            tools.append(tool)
            views.append({'viewer_agent_id': reviewer, 'screenshot': image_ref, 'view_export': tool})
        findings = record['findings']
        if not isinstance(findings, str):
            findings = json.dumps(findings, ensure_ascii=False)
        if not findings.strip():
            raise ValueError('Reviewer findings are empty')
        rows.append({'cell_id': cell, 'anonymous_product': label,
                     'product_evidence_sha256': mapping['product_evidence_sha256'],
                     'findings': findings, 'viewed_screenshots': views,
                     'original_reviewer_record': record, 'reviewer_records': records_ref,
                     'anonymous_material_map': mapping_ref})
    if seen != set(products):
        raise ValueError('Reviewer must cover exactly every supplied completed product')
    declaration_ref, declaration_raw = original(cfg['declaration_file'])
    declaration = json.loads(declaration_raw)
    required = ['outcome', 'reviewed_at', 'condition_blind', 'blinding_limitations',
                'scope', 'limitations', 'final_runtime_acceptance']
    if any(key not in declaration for key in required):
        raise ValueError('Reviewer-authored acceptance declaration lacks required fields')
    # No default acceptance, repaired disposition or positive outcome is invented.
    result_ref, _ = original(cfg.get('result_file', 'FINAL.md'))
    for name in cfg.get('additional_tool_exports', []):
        ref, _ = original(name)
        tools.append(export(ref, 'actual reviewer tool as named in retained record',
                            'Original actual reviewer tool request/return, retained byte for byte.'))
    review = {'schema_version': 1, 'kind': 'independent_product_review',
              'agent_id': reviewer, 'parent_agent_id': cfg.get('parent_agent_id', '/root'),
              'fork_turns': 'none', 'status': 'completed', 'prompt': prompt_ref,
              'spawn': export(spawn_ref, 'collaboration.spawn_agent', 'Exact actual fresh reviewer dispatch request and returned canonical ID.'),
              'completion': export(completion_ref, 'collaboration FINAL_ANSWER notification', 'Exact actual terminal reviewer notification; export timestamp is not inferred execution time.'),
              'tool_outputs': tools, 'result': result_ref, 'reviewed_products': rows,
              'review_declaration': declaration_ref, 'review_snapshot': reference(snapshot_path),
              **{key: declaration[key] for key in required}}
    (output / 'review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    (output / 'index-configuration.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'reviewer': reviewer, 'products': len(rows), 'original_view_exports': len(tools),
                      'outcome': review['outcome'], 'output': str(output / 'review.json')}))


if __name__ == '__main__':
    main()
