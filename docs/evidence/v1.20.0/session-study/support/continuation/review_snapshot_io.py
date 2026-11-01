"""Read/write bounded coordinator review inventories without dropping originals."""
from pathlib import Path
import hashlib
import json


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_snapshot(path):
    path = Path(path).resolve()
    result = json.loads(path.read_text())
    for key, is_mapping in (("file_hashes", True), ("changed_or_added", False)):
        parts = result.get(key + "_parts")
        if parts is None:
            continue
        if key in result:
            raise ValueError("Ambiguous inline and split review inventory")
        combined = {} if is_mapping else []
        for part in parts:
            source = (path.parent / part["file"]).resolve()
            source.relative_to(path.parent)
            raw = source.read_bytes()
            if len(raw) != part["bytes"] or digest(raw) != part["sha256"]:
                raise ValueError("Review inventory part differs")
            value = json.loads(raw)
            expected_type = dict if is_mapping else list
            if not isinstance(value, expected_type) or len(value) != part["entries"]:
                raise ValueError("Review inventory part shape differs")
            if is_mapping:
                if set(combined).intersection(value):
                    raise ValueError("Duplicate review inventory path")
                combined.update(value)
            else:
                combined.extend(value)
        if len(combined) != result[key + "_count"]:
            raise ValueError("Review inventory count differs")
        result[key] = combined
    return result


def write_snapshot(path, value, *, threshold=2_500_000, entries_per_part=4000):
    path = Path(path)
    result = dict(value)
    for key in ("file_hashes", "changed_or_added"):
        original = result[key]
        if len(json.dumps(original, ensure_ascii=False).encode()) <= threshold:
            continue
        entries = list(original.items()) if isinstance(original, dict) else original
        parts = []
        for offset in range(0, len(entries), entries_per_part):
            selected = entries[offset:offset + entries_per_part]
            body = dict(selected) if isinstance(original, dict) else selected
            part = path.parent / f"{key.replace('_', '-')}-{offset // entries_per_part + 1:03d}.json"
            if part.exists():
                raise FileExistsError(part)
            raw = (json.dumps(body, ensure_ascii=False, indent=2) + "\n").encode()
            part.write_bytes(raw)
            parts.append({"file": part.name, "bytes": len(raw),
                          "sha256": digest(raw), "entries": len(body)})
        del result[key]
        result[key + "_parts"] = parts
        result[key + "_count"] = len(original)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")

