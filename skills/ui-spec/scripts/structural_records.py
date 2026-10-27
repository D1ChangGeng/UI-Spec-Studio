"""Local record observations shared by the optional inspectors; no design policy."""
from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

REPORT_FORMAT = "ui-spec-structure-report/1"
LIMITS = [
    "Describes the supplied record, not professional sufficiency, correctness, readiness or completion.",
    "Declared statuses, actions, observations and approvals are not authenticated execution facts.",
    "No browser, pixel, media, model, service or network inspection is performed.",
    "Absent categories are vocabulary hints; task applicability and unknown scope are not assessed.",
    "Relations are declared links, not proven causes, defects or mandatory rechecks.",
    "Local file metadata does not prove observation, adoption or quality; digests are not compared here.",
    "Reports are read-only. Agent judgment and scoped independent verification determine actual work.",
]


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def local_path(root: Path, value: Any) -> Path:
    """Resolve a relative path without following symlinks or permitting root escapes."""
    if not text(value) or any(c in value for c in ("\\", ":", "\x00")):
        raise ValueError("Not a project-relative POSIX path")
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in {"..", "~"} for part in p.parts):
        raise ValueError("Path is outside the permitted project-relative namespace")
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Project root is not a directory")
    target = root.joinpath(*p.parts)
    for candidate in (target, *target.parents):
        if candidate == root:
            break
        if candidate.is_symlink():
            raise ValueError("Path traverses a symlink; target was not inspected")
    resolved = target.resolve(strict=False)
    if not resolved.is_relative_to(root):
        raise ValueError("Path resolves outside the project")
    return resolved


def local_file(root: Path, value: Any) -> Path:
    target = local_path(root, value)
    if not target.is_file():
        raise ValueError("Path does not identify an existing regular project file")
    return target


def read_record(root: Path, path: str) -> Any:
    def constant(value: str) -> None:
        raise ValueError(f"Non-JSON numeric constant: {value}")
    def pairs(items: list[tuple[str, Any]]) -> dict:
        result = {}
        for k, v in items:
            if k in result:
                raise ValueError(f"Duplicate JSON field: {k}")
            result[k] = v
        return result
    return json.loads(local_file(root, path).read_text(encoding="utf-8"),
                      parse_constant=constant, object_pairs_hook=pairs)


def unreadable(path: str, exc: Exception) -> dict:
    return {"report_format": REPORT_FORMAT, "record_readability": "unreadable",
            "record_source": {"path": path},
            "structural_findings": [{"path": "$", "code": "record_read_problem", "message": str(exc)}],
            "limits": list(LIMITS)}


class Observation:
    """Observe shapes and declared references. Never evaluate their design meaning."""
    def __init__(self, data: Any, root: Path):
        self.data = data
        self.root = root.resolve(strict=True)
        if not self.root.is_dir():
            raise ValueError("Project root is not a directory")
        self.findings: list[dict] = []
        self.fields: list[dict] = []
        self.files: list[dict] = []
        self.references: list[dict] = []
        self.revisions: list[dict] = []
        self.actions: list[dict] = []
        self.row_paths: dict[int, str] = {}
        self.ambiguous: dict[int, set[str]] = {}

    def row_path(self, item: dict, fallback: str) -> str:
        return self.row_paths.get(id(item), fallback)

    def note(self, path: str, code: str, message: str) -> None:
        self.findings.append({"path": path, "code": code, "message": message})

    def field(self, item: dict, key: str, path: str, expected: type | tuple[type, ...] = str,
              *, identity: bool = False) -> Any:
        where = f"{path}.{key}"
        if key not in item:
            self.fields.append({"path": where, "presence": "not_declared"})
            if identity:
                self.note(where, "identity_not_declared", "No identifier was declared for this record")
            return None
        value = item[key]
        empty = value is None or value == "" or value == [] or value == {}
        self.fields.append({"path": where, "presence": "empty" if empty else "declared"})
        if value is None:
            if identity:
                self.note(where, "identifier_empty", "The declared identifier is empty")
        elif not isinstance(value, expected) or (expected is int and type(value) is not int):
            self.note(where, "field_shape", f"Field has type {type(value).__name__}; declared profile uses {expected}")
        elif identity and not text(value):
            self.note(where, "identifier_empty", "The declared identifier is empty")
        return value

    def rows(self, owner: dict, key: str, path: str = "$") -> list[dict]:
        value = self.field(owner, key, path, list)
        if value is None:
            return []
        if not isinstance(value, list):
            return []
        rows = []
        for i, row in enumerate(value):
            if not isinstance(row, dict):
                self.note(f"{path}.{key}[{i}]", "record_shape", "List entry is not an object")
            else:
                self.row_paths[id(row)] = f"{path}.{key}[{i}]"
                rows.append(row)
        return rows

    def table(self, key: str) -> tuple[list[dict], dict[str, dict]]:
        rows = self.rows(self.data, key)
        index: dict[str, dict] = {}
        self.ambiguous[id(index)] = set()
        for i, row in enumerate(rows):
            where = self.row_path(row, f"$.{key}[{i}]")
            value = self.field(row, "id", where, identity=True)
            if text(value):
                if value in index:
                    self.ambiguous[id(index)].add(value)
                    self.note(where + ".id", "duplicate_id", f"ID {value!r} occurs more than once; lookup is ambiguous")
                else:
                    index[value] = row
        return rows, index

    def ref(self, value: Any, known: dict, path: str) -> None:
        if not text(value):
            self.note(path, "reference_shape", "Reference is not a nonempty ID string")
            return
        state = "ambiguous" if value in self.ambiguous.get(id(known), set()) else ("resolved" if value in known else "unresolved")
        self.references.append({"path": path, "id": value, "resolution": state})
        if state == "ambiguous":
            self.note(path, "ambiguous_reference", f"More than one target declares ID {value!r}")
        if state == "unresolved":
            self.note(path, "unresolved_reference", f"No target with ID {value!r} is declared in this record scope")

    def refs(self, item: dict, key: str, known: dict, path: str) -> list[str]:
        value = self.field(item, key, path, list)
        if not isinstance(value, list):
            return []
        for i, entry in enumerate(value):
            self.ref(entry, known, f"{path}.{key}[{i}]")
        return [x for x in value if text(x)]

    def strings(self, item: dict, key: str, path: str) -> list[str]:
        value = self.field(item, key, path, list)
        if not isinstance(value, list):
            return []
        for i, entry in enumerate(value):
            if not isinstance(entry, str):
                self.note(f"{path}.{key}[{i}]", "field_shape", "List entry is not a string")
        return [x for x in value if isinstance(x, str)]

    def string_items(self, item: dict, key: str, path: str) -> list[tuple[int, str]]:
        """Keep source indices when reporting malformed list entries beside valid paths."""
        self.strings(item, key, path)
        value = item.get(key)
        return [(i, v) for i, v in enumerate(value) if isinstance(v, str)] if isinstance(value, list) else []

    def file(self, value: Any, path: str) -> None:
        try:
            target = local_path(self.root, value)
            if not target.exists():
                kind, size = "not_found", None
            elif target.is_file():
                kind, size = "regular_file", target.stat().st_size
            elif target.is_dir():
                kind, size = "directory", None
            else:
                kind, size = "other", None
            self.files.append({"field": path, "path": value, "filesystem_kind": kind,
                               "bytes": size, "content_inspection": "not_performed"})
            if kind != "regular_file":
                self.note(path, "local_file_reference", f"Referenced path is {kind}")
        except (OSError, ValueError, RuntimeError) as exc:
            self.files.append({"field": path, "path": value, "filesystem_kind": "not_inspected", "reason": str(exc)})
            self.note(path, "path_not_inspected", str(exc))

    def location(self, value: Any, path: str) -> None:
        if value is None:
            return
        if not isinstance(value, dict):
            self.note(path, "location_shape", "Location is not an object with path or url")
            return
        keys = {k for k in ("path", "url") if k in value}
        if len(keys) != 1:
            self.note(path, "location_shape", "Location has no unique path/url field")
        if "path" in value:
            self.file(value["path"], path + ".path")
        if "url" in value:
            raw = value["url"]
            try:
                u = urlsplit(raw) if isinstance(raw, str) else None
                if not u or u.scheme not in {"http", "https"} or not u.hostname or u.username or u.password:
                    raise ValueError("URL is not a credential-free HTTP(S) reference")
                _ = u.port
                self.files.append({"field": path + ".url", "url": raw, "availability": "not_fetched"})
            except (TypeError, ValueError) as exc:
                self.note(path + ".url", "url_shape", str(exc))

    def revision(self, item: dict, path: str) -> None:
        for key in ("revision", "product_revision", "source_revision", "design_revision"):
            if key in item:
                self.field(item, key, path)
                self.revisions.append({"field": f"{path}.{key}", "declared_revision": item[key]})

    def action(self, item: dict, path: str) -> None:
        if "next_action" not in item:
            return
        action = self.field(item, "next_action", path, (dict, str))
        self.actions.append({"field": path + ".next_action", "declared_value": action})

    def report(self, kind: str) -> dict:
        data = self.data if isinstance(self.data, dict) else {}
        return {"report_format": REPORT_FORMAT, "inspector": kind,
                "record_readability": "readable",
                "record_source": {"declared_format": data.get("format", data.get("schema_version")),
                                  "declared_revision": data.get("revision"),
                                  "record_origin": data.get("record_origin"), "scope": "supplied_record"},
                "structural_findings": self.findings, "field_observations": self.fields,
                "reference_observations": self.references, "file_observations": self.files,
                "revision_declarations": self.revisions, "declared_actions": self.actions,
                "limits": list(LIMITS)}
