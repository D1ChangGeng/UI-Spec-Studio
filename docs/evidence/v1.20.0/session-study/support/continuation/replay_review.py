#!/usr/bin/env python3
"""Replay retained independent-review cohorts and verify original file bytes."""
from pathlib import Path
import argparse
import hashlib
import json
from replay_snapshot import safe, extract
from large_archives import restore_large_files
from review_snapshot_io import read_snapshot

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    chain = []
    path = safe(repo, args.snapshot)
    while True:
        data = read_snapshot(path)
        chain.append((path.parent, data))
        reference = data.get("previous_snapshot")
        if reference is None:
            break
        path = safe(repo, reference["path"])
        if digest(path) != reference["sha256"]:
            raise ValueError("Previous review snapshot differs")
    args.output.mkdir(parents=True, exist_ok=False)
    for directory, data in reversed(chain):
        for item in data["archives"].get("member_inventory_parts", []):
            inventory = safe(directory, item["file"])
            if inventory.stat().st_size != item["bytes"] or digest(inventory) != item["sha256"]:
                raise ValueError("Review member inventory differs")
            rows = json.loads(inventory.read_text())
            if len(rows) != item["members"]:
                raise ValueError("Review member inventory count differs")
            if any(data["file_hashes"].get(row["path"]) != row["sha256"] for row in rows):
                raise ValueError("Review member inventory differs from original file hashes")
        for item in data["archives"]["archives"]:
            archive = safe(directory, item["file"])
            if digest(archive) != item["sha256"]:
                raise ValueError("Review archive differs")
            extract(archive, args.output)
        restore_large_files(data["archives"].get("split_files", []), directory, args.output, safe)
        for name in data["deleted_since_previous"]:
            safe(args.output, name).unlink(missing_ok=True)
    actual = {p.relative_to(args.output).as_posix(): digest(p)
              for p in args.output.rglob("*") if p.is_file()}
    if actual != chain[0][1]["file_hashes"]:
        raise ValueError("Reconstructed review files differ from the original snapshot")
    print(json.dumps({"status": "passed", "cohorts": len(chain), "verified_files": len(actual),
                      "scope": "Original review file reconstruction only; not an additional product review."}, indent=2))

if __name__ == "__main__":
    main()
