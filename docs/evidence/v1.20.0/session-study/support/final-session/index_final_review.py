#!/usr/bin/env python3
"""Link an actual anonymous review to frozen product images without judging it."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "continuation"))
from review_snapshot_io import read_snapshot
import argparse
import base64
import hashlib
import json


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--reviewer', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    study = repo / 'docs/evidence/v1.20.0/session-study'
    snapshot_path = args.snapshot.resolve()
    snapshot = read_snapshot(snapshot_path)
    source = Path(snapshot['source_workspace'])

    def read_ref(reference):
        path = (repo / reference['path']).resolve()
        path.relative_to(repo)
        raw = path.read_bytes()
        if digest(raw) != reference['sha256']:
            raise ValueError('Retained reference differs: ' + reference['path'])
        return raw

    def reference(path):
        return {'path': path.relative_to(repo).as_posix(),
                'sha256': digest(path.read_bytes())}

    records_ref = snapshot['direct_artifacts']['products.json']
    raw_records = read_ref(records_ref)
    if digest(raw_records) != snapshot['file_hashes']['products.json']:
        raise ValueError('Reviewer records differ from the frozen snapshot')
    records = json.loads(raw_records)
    if isinstance(records, dict):
        records = records['products']
    if not isinstance(records, list) or not records:
        raise ValueError('Actual structured product observations are required')

    products = {}
    for path in list((study / 'runs').glob('*/product-evidence.json')) + list((study / 'supplementary-runs').glob('*/product-evidence.json')):
        value = json.loads(path.read_text())
        if value['cell_id'] in products:
            raise ValueError('Duplicate current product evidence')
        products[value['cell_id']] = (path, value)

    rows, seen = [], set()
    for record in records:
        label = record['anonymous_product']
        if label in seen:
            raise ValueError('Duplicate reviewer product: ' + label)
        seen.add(label)
        mapping_path = study / 'coordination' / ('blind-materials-' + label + '.json')
        supplemental_map = study / 'coordination/final-session' / ('blind-materials-' + label + '.json')
        if supplemental_map.is_file(): mapping_path = supplemental_map
        mapping = json.loads(mapping_path.read_text())
        product_path, product = products[mapping['cell_id']]
        if digest(product_path.read_bytes()) != mapping['product_evidence_sha256']:
            raise ValueError('Anonymous materials identify a different product')
        captures = {item['anonymous_file']: item['original']
                    for item in mapping['capture_mapping']}
        allowed_images = {(item['path'], item['sha256'])
                          for item in product['screenshots']}
        originals = record['viewed_original_files']
        exports = record['view_exports']
        if not originals or len(originals) != len(exports):
            raise ValueError('Every original viewing needs its actual export')
        views = []
        for original_path, export_path in zip(originals, exports):
            marker = '/review-pack/'
            if marker not in original_path:
                raise ValueError('Original view is outside the anonymous review pack')
            relative_original = original_path.split(marker, 1)[1]
            image_ref = captures[relative_original]
            if (image_ref['path'], image_ref['sha256']) not in allowed_images:
                raise ValueError('Original image is absent from the final product index')
            original_bytes = read_ref(image_ref)
            if not original_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
                raise ValueError('Original image is not retained PNG data')
            export_relative = Path(export_path).relative_to(source).as_posix()
            export_ref = snapshot['direct_artifacts'][export_relative]
            export_bytes = read_ref(export_ref)
            if digest(export_bytes) != snapshot['file_hashes'][export_relative]:
                raise ValueError('View return differs from the reviewer snapshot')
            payload = json.loads(export_bytes)
            calls = payload if isinstance(payload, list) else [payload]
            matches = [call for call in calls if isinstance(call, dict)
                       and call.get('tool') == 'view_image'
                       and call.get('arguments', {}).get('path') == original_path]
            if not matches:
                raise ValueError('No actual view_image request for the original PNG')
            returned_images=[]
            for call in matches:
                url = call.get('result', {}).get('image_url')
                if not isinstance(url, str) or not url.startswith('data:') or ';base64,' not in url:
                    raise ValueError('Actual image return is missing')
                returned = base64.b64decode(url.split(';base64,', 1)[1], validate=True)
                if not returned.startswith(b'\x89PNG\r\n\x1a\n'):
                    raise ValueError('Actual tool return is not PNG image data')
                returned_images.append({'sha256':digest(returned),'byte_identical_to_original':returned==original_bytes,'scope':'Actual image-tool returned PNG. If bytes differ, the request identity is linked but display resizing/encoding is not represented as unchanged original pixels.'})
            views.append({'viewer_agent_id': args.reviewer,
                          'screenshot': image_ref,
                          'returned_images': returned_images,
                          'view_export': {**export_ref, 'source': 'view_image',
                                          'scope': 'Actual independent reviewer request and validated PNG return for the original frozen anonymous product capture; request path and retained original hashes match. Returned-image identity and byte-equality status are recorded separately; resized or re-encoded display output is not described as unchanged original pixels.',
                                          'export_kind': 'faithful_conversation_export',
                                          'synthetic': False}})
        findings = record['findings']
        if not isinstance(findings, str):
            findings = json.dumps(findings, ensure_ascii=False)
        if not findings.strip():
            raise ValueError('Reviewer findings cannot be empty')
        rows.append({'cell_id': mapping['cell_id'],
                     'anonymous_product': label,
                     'supplementary_attempt_id': mapping.get('supplementary_attempt_id'),
                     'product_evidence_sha256': mapping['product_evidence_sha256'],
                     'judgment': record['judgment'], 'findings': findings,
                     'viewed_screenshots': views,
                     'original_reviewer_record': record,
                     'reviewer_records': records_ref,
                     'anonymous_material_map': reference(mapping_path)})

    output = {'schema_version': 1,
              'kind': 'coordinator-derived correspondence over actual reviewer output; not a review outcome',
              'agent_id': args.reviewer, 'review_snapshot': reference(snapshot_path),
              'reviewer_records': records_ref, 'reviewed_products': rows,
              'scope': 'Links anonymous original PNG views to frozen product identities. Findings and judgments are copied from the reviewer; additional reviewer captures remain separate. This index does not supply acceptance.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        raise ValueError('Do not overwrite an existing correspondence index')
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'products': len(rows), 'original_view_exports': sum(len(row['viewed_screenshots']) for row in rows), 'output': str(args.output)}))


if __name__ == '__main__':
    main()
