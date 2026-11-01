#!/usr/bin/env python3
"""Freeze an actual independent-review cohort without altering original outputs."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "continuation"))
import argparse
import datetime
import hashlib
import json
import shutil
from large_archives import archive_with_large_files
from review_snapshot_io import read_snapshot, write_snapshot

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--cohort", required=True)
    parser.add_argument("--review-series", required=True)
    parser.add_argument("--product-snapshots", type=Path, required=True, help="JSON list of repository-relative frozen completed-product snapshot paths")
    args = parser.parse_args()
    if not args.cohort.startswith("cohort-") or not args.cohort[7:].isdigit():
        raise ValueError("Use an explicit cohort-NN identifier")
    repo, source = args.repo.resolve(), args.source.resolve()
    if Path(args.review_series).name != args.review_series:
        raise ValueError("Review series must be a single directory name")
    review = repo / "docs/evidence/v1.20.0/session-study/continuation-2100/review" / args.review_series
    review.mkdir(parents=True, exist_ok=True)
    review.mkdir(exist_ok=True)
    target = review / args.cohort
    prior = sorted(review.glob("cohort-*/snapshot.json"))
    if prior:
        raise ValueError("Fresh reviewer requires a fresh review series; no prior identity/output inheritance")
    previous = None
    if target.exists():
        raise ValueError("An existing frozen cohort must not be overwritten")
    target.mkdir()
    files = sorted(
        p for p in source.rglob("*")
        if p.is_file() and not p.is_symlink()
        and not any(part in {"disposable", "__pycache__", ".git", "node_modules", ".pytest_cache"}
                    for part in p.relative_to(source).parts)
    )
    hashes = {p.relative_to(source).as_posix(): digest(p) for p in files}
    old = previous["file_hashes"] if previous else {}
    changed = [p for p in files if hashes[p.relative_to(source).as_posix()] != old.get(p.relative_to(source).as_posix())]
    # Reuse existing immutable product bytes by hash, without treating them as
    # reviewer actions. Every borrowed file retains its exact original name/hash.
    borrowed_sources = []
    available = {}
    for name in json.loads(args.product_snapshots.read_text()):
        path = (repo / name).resolve()
        path.relative_to(repo)
        product_snapshot = json.loads(path.read_text())
        index = len(borrowed_sources)
        borrowed_sources.append({"cell_id": product_snapshot["cell_id"],
                                 "snapshot": {"path": path.relative_to(repo).as_posix(),
                                              "sha256": digest(path)}})
        for original, identity in product_snapshot["workspace_files"].items():
            available.setdefault(identity, (index, original))
    borrowed = {}
    for path in changed:
        relative = path.relative_to(source).as_posix()
        if hashes[relative] in available:
            index, original = available[hashes[relative]]
            borrowed[relative] = {"source_index": index, "original_path": original,
                                  "sha256": hashes[relative]}
    retained_changes = [path for path in changed if path.relative_to(source).as_posix() not in borrowed]
    archives = archive_with_large_files(source, retained_changes, target, "original-review")
    borrowed_parts = []
    entries = list(borrowed.items())
    for offset in range(0, len(entries), 4000):
        part = target / f"borrowed-files-{offset // 4000 + 1:03d}.json"
        selected = dict(entries[offset:offset + 4000])
        part.write_text(json.dumps(selected, ensure_ascii=False, indent=2) + "\n")
        borrowed_parts.append({"file": part.name, "sha256": digest(part),
                               "bytes": part.stat().st_size, "entries": len(selected)})
    # A large set of reviewer working copies can make the duplicate member
    # inventory exceed the connector's object bound. Keep every row in small
    # hashed JSON parts; file_hashes remains the full reconstruction contract.
    if len(json.dumps(archives.get("members", [])).encode()) > 3_000_000:
        members = archives.pop("members")
        archives["member_inventory_parts"] = []
        for offset in range(0, len(members), 5000):
            part = target / f"member-inventory-{offset // 5000 + 1:03d}.json"
            rows = members[offset:offset + 5000]
            part.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n")
            archives["member_inventory_parts"].append({
                "file": part.name, "bytes": part.stat().st_size,
                "sha256": digest(part), "members": len(rows),
            })
    direct = dict(previous.get("direct_artifacts", {})) if previous else {}
    for path in retained_changes:
        relative = path.relative_to(source).as_posix()
        # Stateful reviewer copies remain byte-complete in the immutable
        # archives; avoid duplicating their entire dependency/source trees as
        # direct navigation exports.
        if relative.startswith("copies/"):
            continue
        if path.suffix not in {".json", ".jsonl", ".png", ".md", ".txt", ".log", ".py"}:
            continue
        if path.stat().st_size > 11_000_000:
            continue
        exported = relative + ".txt" if path.suffix in {".md", ".py"} else relative
        destination = target / "raw" / exported
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
        direct[relative] = {
            "path": destination.relative_to(repo).as_posix(),
            "sha256": hashes[relative],
        }
    for relative in set(old) - set(hashes):
        direct.pop(relative, None)
    result = {
        "schema_version": 1,
        "kind": "coordinator byte snapshot of actual reviewer output; not a synthetic tool transcript",
        "cohort": args.cohort,
        "captured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_workspace": str(source),
        "file_hashes": hashes,
        "changed_or_added": [p.relative_to(source).as_posix() for p in changed],
        "deleted_since_previous": sorted(set(old) - set(hashes)),
        "previous_snapshot": {
            "path": prior[-1].relative_to(repo).as_posix(),
            "sha256": digest(prior[-1]),
        } if previous else None,
        "archives": archives,
        "borrowed_sources": borrowed_sources,
        "borrowed_inventory_parts": borrowed_parts,
        "borrowed_files_count": len(borrowed),
        "borrowed_scope": "Byte-identical files reused from existing immutable product snapshots. No input or original reviewer output is discarded: custom replay_review.py reconstructs borrowed bytes before applying the retained review overlay. Hash reuse establishes byte identity only, not a reviewer action or judgment.",
        "direct_artifacts": direct,
        "scope": "Original reviewer reports, exact available tool outputs, command stdout/stderr, scripts, traces and captures. Raw Markdown/Python direct exports use .txt; archive entries preserve original names and bytes.",
        "direct_export_policy": "Reviewer-created copies/ trees are archive-only; their full original paths and hashes remain in file_hashes and are verified by reconstruction.",
        "exclusions": "Directories literally named disposable, node_modules, .git, __pycache__ or .pytest_cache, and symbolic links. Other reviewer-created application copies, including copies/ and their exercised persistence states, are retained. The original reviewed application source and original product captures also remain in each frozen product snapshot. No browser profile, credentials or hidden reasoning are included.",
    }
    write_snapshot(target / "snapshot.json", result)
    print(json.dumps({"cohort": args.cohort, "files": len(files), "changed": len(changed),
                      "bytes": sum(p.stat().st_size for p in changed),
                      "direct_artifacts": len(direct), "borrowed_files": len(borrowed), "snapshot": str(target / "snapshot.json")}, indent=2))

if __name__ == "__main__":
    main()
