#!/usr/bin/env python3
"""Freeze an actual independent-review cohort without altering original outputs."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import shutil
from large_archives import archive_with_large_files

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--cohort", required=True)
    args = parser.parse_args()
    if not args.cohort.startswith("cohort-") or not args.cohort[7:].isdigit():
        raise ValueError("Use an explicit cohort-NN identifier")
    repo, source = args.repo.resolve(), args.source.resolve()
    review = repo / "docs/evidence/v1.20.0/session-study/review"
    review.mkdir(exist_ok=True)
    target = review / args.cohort
    prior = sorted(review.glob("cohort-*/snapshot.json"))
    previous = json.loads(prior[-1].read_text()) if prior else None
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
    archives = archive_with_large_files(source, changed, target, "original-review")
    direct = dict(previous.get("direct_artifacts", {})) if previous else {}
    for path in changed:
        relative = path.relative_to(source).as_posix()
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
        "direct_artifacts": direct,
        "scope": "Original reviewer reports, exact available tool outputs, command stdout/stderr, scripts, traces and captures. Raw Markdown/Python direct exports use .txt; archive entries preserve original names and bytes.",
        "exclusions": "Disposable duplicate application copies, dependency caches and bytecode. The reviewed application source and original product captures remain in each frozen product snapshot. No browser profile, credentials or hidden reasoning are included.",
    }
    (target / "snapshot.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"cohort": args.cohort, "files": len(files), "changed": len(changed),
                      "bytes": sum(p.stat().st_size for p in changed),
                      "direct_artifacts": len(direct), "snapshot": str(target / "snapshot.json")}, indent=2))

if __name__ == "__main__":
    main()
