#!/usr/bin/env python3
"""Check declared UI coverage and evidence references; does not judge rendered UI."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

LIMITS = (
    "This checks recorded structure and local evidence references only. "
    "It does not run a browser, inspect pixels, authenticate approvals, "
    "or independently verify behavior or source revision claims."
)
ID = re.compile(r"^[a-z0-9][a-z0-9_-]{0,79}$")
STATUSES = {"planned", "pass", "fail", "blocked", "waived"}
MODES = {"service", "local", "static"}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _safe_file(root: Path, value: Any) -> bool:
    if not _text(value) or Path(value).is_absolute():
        return False
    try:
        path = (root / value).resolve(strict=True)
        path.relative_to(root)
        return path.is_file() and path.stat().st_size > 0
    except (OSError, ValueError, RuntimeError):
        return False


def validate(data: Any, root: Path, mode: str = "draft") -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    required: set[str] = set()
    satisfied: set[str] = set()
    if mode not in {"draft", "review", "finish"}:
        raise ValueError("Mode must be draft, review, or finish")
    root = root.resolve()

    def report() -> dict[str, Any]:
        return {"ok": not errors, "mode": mode, "errors": errors, "warnings": warnings,
                "coverage": {"required": len(required), "satisfied": len(required & satisfied),
                             "pending": sorted(required - satisfied)}, "limits": LIMITS}

    if not isinstance(data, dict):
        errors.append("Manifest must be a JSON object")
        return report()
    if type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    for field in ("project", "revision"):
        if not _text(data.get(field)):
            errors.append(f"{field} must be a nonempty string")
    if not isinstance(data.get("phase"), str) or data.get("phase") not in {"init", "shape", "iterate", "audit", "finish"}:
        errors.append("phase must be init, shape, iterate, audit, or finish")
    if data.get("design_system_path") is not None and not _safe_file(root, data["design_system_path"]):
        errors.append("design_system_path must reference a nonempty local file")

    tables: dict[str, list[dict[str, Any]]] = {}
    for field in ("viewports", "variants", "routes", "journeys", "requirements", "checks", "approvals", "connections", "exceptions"):
        value = data.get(field)
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            errors.append(f"{field} must be a list of objects")
            tables[field] = []
        else:
            tables[field] = value

    def index(field: str) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for item in tables[field]:
            key = item.get("id")
            if not isinstance(key, str) or not ID.fullmatch(key):
                errors.append(f"{field}: id must be a short lowercase identifier")
            elif key in result:
                errors.append(f"{field}: duplicate id {key}")
            else:
                result[key] = item
        return result

    views, variants, routes, journeys, checks = (index(k) for k in ("viewports", "variants", "routes", "journeys", "checks"))
    for key, view in views.items():
        for dimension in ("width", "height"):
            n = view.get(dimension)
            if type(n) is not int or n < 1 or n > 20000:
                errors.append(f"viewports.{key}.{dimension}: expected a positive CSS pixel integer <= 20000")
    for key, variant in variants.items():
        for field in ("locale", "theme"):
            if not _text(variant.get(field)):
                errors.append(f"variants.{key}.{field}: specify the supported value (or default)")
    if not views or not variants:
        errors.append("Declare at least one viewport and one variant")

    states: dict[str, set[str]] = {}
    critical: dict[str, set[str]] = {}
    for key, route in routes.items():
        for field in ("path", "purpose"):
            if not _text(route.get(field)):
                errors.append(f"routes.{key}.{field}: provide a nonempty value")
        raw = route.get("states", [])
        if not isinstance(raw, list) or any(not isinstance(x, str) or not ID.fullmatch(x) for x in raw):
            errors.append(f"routes.{key}.states: expected state identifiers")
            raw = []
        states[key] = set(raw)
        if not raw or len(raw) != len(states[key]):
            errors.append(f"routes.{key}: provide distinct states")
        if not isinstance(route.get("primary_state"), str) or route.get("primary_state") not in states[key]:
            errors.append(f"routes.{key}: primary_state must belong to states")
        raw_critical = route.get("critical_states", [])
        if not isinstance(raw_critical, list) or any(not isinstance(x, str) for x in raw_critical):
            errors.append(f"routes.{key}.critical_states: expected a list of state identifiers")
            raw_critical = []
        critical[key] = set(raw_critical)
        if not critical[key] <= states[key]:
            errors.append(f"routes.{key}: critical_states must belong to states")
        if isinstance(route.get("primary_state"), str) and route.get("primary_state") in states[key]:
            for view in views:
                for variant in variants:
                    required.add(f"visual:{key}:{route['primary_state']}:{view}:{variant}")
        for state in critical[key]:
            for variant in variants:
                required.add(f"critical:{key}:{state}:{variant}")
    for key, journey in journeys.items():
        linked = journey.get("routes")
        if not isinstance(linked, list) or not linked or any(not isinstance(x, str) or x not in routes for x in linked):
            errors.append(f"journeys.{key}: routes must reference existing route IDs")
        if not _text(journey.get("outcome")):
            errors.append(f"journeys.{key}: describe the observable outcome")
        for variant in variants:
            required.add(f"journey:{key}:{variant}")

    def visual_key(item: dict[str, Any]) -> str | None:
        r, state, view, variant = (item.get(f) for f in ("route", "state", "viewport", "variant"))
        if any(not isinstance(x, str) for x in (r, state, view, variant)):
            return None
        if r not in routes or state not in states.get(r, set()) or view not in views or variant not in variants:
            return None
        return f"visual:{r}:{state}:{view}:{variant}"

    for requirement in tables["requirements"]:
        key = visual_key(requirement)
        if key is None:
            errors.append("requirements: unknown or incomplete route/state/viewport/variant")
        else:
            required.add(key)
    if mode == "finish":
        required.update(f"integration:{key}" for key in routes)
    if mode in {"review", "finish"} and not routes:
        errors.append("Review/finish requires an explicit nonempty route inventory")
    if mode == "finish" and not journeys:
        errors.append("Finish requires at least one actual user journey")

    exceptions: dict[str, dict[str, Any]] = {}
    for exc in tables["exceptions"]:
        target = exc.get("target")
        if not _text(target) or any(not _text(exc.get(f)) for f in ("reason", "approved_by", "reference")):
            errors.append("exceptions: target, reason, approved_by, reference are required")
        elif target in exceptions:
            errors.append(f"exceptions: duplicate target {target}")
        else:
            exceptions[target] = exc
    used_exceptions: set[str] = set()
    check_targets: dict[str, str] = {}
    successful: dict[str, dict[str, Any]] = {}
    for key, check in checks.items():
        kind = check.get("kind")
        target: str | None = None
        if kind == "visual":
            target = visual_key(check)
        elif kind == "journey":
            j, variant = check.get("journey"), check.get("variant")
            if isinstance(j, str) and isinstance(variant, str) and j in journeys and variant in variants:
                target = f"journey:{j}:{variant}"
        elif kind == "integration":
            r = check.get("route")
            if isinstance(r, str) and r in routes:
                target = f"integration:{r}"
        if target is None:
            errors.append(f"checks.{key}: unknown kind or invalid target references")
            continue
        if target in check_targets:
            errors.append(f"checks.{key}: duplicate target {target}; retain one current result")
        check_targets[target] = key
        status = check.get("status")
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f"checks.{key}: invalid status")
            continue
        accepted = False
        if status == "pass":
            before = len(errors)
            if check.get("revision") != data.get("revision"):
                errors.append(f"checks.{key}: evidence revision is stale")
            evidence = check.get("evidence")
            if not isinstance(evidence, list) or not evidence or any(not _safe_file(root, e) for e in evidence):
                errors.append(f"checks.{key}: pass requires nonempty evidence files inside the project")
            if not _text(check.get("reviewer")):
                errors.append(f"checks.{key}: record who performed the check")
            if kind == "visual" and check.get("inspected") is not True:
                errors.append(f"checks.{key}: visual pass requires recorded image inspection")
            if kind in {"journey", "integration"} and not _text(check.get("outcome")):
                errors.append(f"checks.{key}: record the observed result")
            if kind == "integration" and (not isinstance(check.get("data_mode"), str) or check.get("data_mode") not in MODES):
                errors.append(f"checks.{key}: integration requires service, local, or static behavior")
            accepted = before == len(errors)
            if accepted:
                successful[key] = check
        elif status == "waived":
            if target not in exceptions:
                errors.append(f"checks.{key}: waiver requires a matching approved exception")
            else:
                used_exceptions.add(target)
                accepted = True
        elif status in {"fail", "blocked"}:
            if not _text(check.get("reason")):
                errors.append(f"checks.{key}: {status} needs a reason")
            if mode in {"review", "finish"}:
                errors.append(f"checks.{key}: {status} remains open")
        if accepted:
            satisfied.add(target)
            if kind == "visual":
                satisfied.add(f"critical:{check['route']}:{check['state']}:{check['variant']}")
    for target in exceptions:
        if target not in used_exceptions:
            warnings.append(f"Unused exception: {target}")

    if mode == "finish":
        design_revision = data.get("design_revision")
        if not _text(design_revision):
            errors.append("Finish requires design_revision identifying the accepted SPEC")
        approved: set[str] = set()
        for approval in tables["approvals"]:
            scope = approval.get("routes")
            if not isinstance(scope, list) or not scope or any(not isinstance(x, str) or x not in routes for x in scope):
                errors.append("approvals: routes must reference the selected scope")
                continue
            if approval.get("revision") != design_revision:
                errors.append("approvals: reference the accepted design_revision")
            elif not _text(approval.get("by")) or not _text(approval.get("reference")):
                errors.append("approvals: record approver and source of approval")
            else:
                approved.update(scope)
        for route in routes:
            if route not in approved:
                errors.append(f"routes.{route}: missing scoped design approval")
        connected: set[str] = set()
        for connection in tables["connections"]:
            route = connection.get("route")
            if not isinstance(route, str) or route not in routes:
                errors.append("connections: unknown route")
                continue
            if route in connected:
                errors.append(f"connections.{route}: duplicate connection")
            ids = connection.get("check_ids")
            if not isinstance(connection.get("mode"), str) or connection.get("mode") not in MODES or not all(_text(connection.get(f)) for f in ("owner", "contract")):
                errors.append(f"connections.{route}: document mode, trusted owner and contract")
                continue
            if not isinstance(ids, list) or not ids or any(not isinstance(x, str) or x not in successful for x in ids):
                errors.append(f"connections.{route}: reference actual passing integration checks")
                continue
            if any(successful[x].get("kind") != "integration" or successful[x].get("route") != route
                   or successful[x].get("data_mode") != connection["mode"] for x in ids):
                errors.append(f"connections.{route}: integration check must match route and mode")
                continue
            connected.add(route)
        for route in routes:
            if route not in connected:
                errors.append(f"routes.{route}: actual connection verification pending")
    if mode in {"review", "finish"}:
        errors.extend(f"Missing completed case: {key}" for key in sorted(required - satisfied))
    if not routes:
        warnings.append("No routes inventoried yet; this is an initialization record")
    return report()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--manifest", default=".ui-spec/manifest.json")
    parser.add_argument("--mode", choices=("draft", "review", "finish"), default="draft")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        root = args.project_root.resolve(strict=True)
        if not root.is_dir() or not _safe_file(root, args.manifest):
            raise ValueError("Manifest must be a nonempty file inside the project")
        data = json.loads((root / args.manifest).read_text(encoding="utf-8"))
        result = validate(data, root, args.mode)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"Recorded coverage check: {'PASS' if result['ok'] else 'PENDING / INVALID'} ({args.mode})")
            for entry in result["errors"]:
                print(f"ERROR: {entry}")
            for entry in result["warnings"]:
                print(f"NOTE: {entry}")
            print(json.dumps(result["coverage"], ensure_ascii=False))
            print(LIMITS)
        return 0 if result["ok"] else 1
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"check_manifest: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
