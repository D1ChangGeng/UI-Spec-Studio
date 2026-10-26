#!/usr/bin/env python3
"""Read-only checks and three views of an optional design-evidence record."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlsplit

FORMAT = "ui-spec-evidence/1"
LEVELS = {f"L{i}" for i in range(6)}
KINDS = {"text", "visual", "temporal", "implementation", "runtime"}
ROLES = {"reference", "candidate", "demo", "trial", "integrated"}
DOMAINS = {
    "visual": {"visual"}, "temporal": {"temporal"},
    "engineering": {"implementation", "runtime"}, "task": {"runtime"},
}
ACTIONS = {"research", "inspect", "compare", "trial", "implement", "expand",
           "verify", "revise", "ask", "finish"}
LIMITS = [
    "Checks declarations and local file consistency, not truth or completeness of research.",
    "Does not fetch URLs, view pixels, play media, run an agent or judge visual quality.",
    "Cannot authenticate approval or establish actual use from a path or dependency entry.",
    "Open or blocked records may be structurally valid; success is not design acceptance.",
    "Change impact lists review candidates; it does not mutate evidence or approval.",
]


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def local_file(root: Path, value: object) -> Path:
    if not nonempty(value) or "\\" in value or ":" in value or "\x00" in value:
        raise ValueError("Use a project-relative POSIX file path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in {"..", "~"} for p in path.parts):
        raise ValueError("Path must stay inside the project")
    target = root.joinpath(*path.parts)
    # Reject even internal symlinks: recorded file identity must be unambiguous.
    for candidate in [target, *target.parents]:
        if candidate == root:
            break
        if candidate.is_symlink():
            raise ValueError("Evidence paths must not traverse symlinks")
    resolved = target.resolve(strict=True)
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError("Expected an existing regular project file")
    return resolved


def affected_objects(data: dict, changed: list[str]) -> set[str]:
    """Return declared dependency and containing-scope review targets, not a state transition."""
    objects = {o["id"]: o for o in data.get("objects", [])}
    affected = set(changed)
    unknown = affected - objects.keys()
    if unknown:
        raise ValueError(f"Unknown changed objects: {', '.join(sorted(unknown))}")
    edges = [(oid, obj["parent"]) for oid, obj in objects.items() if obj.get("parent")]
    for row in data.get("relations", []):
        a, b, kind = row["from"], row["to"], row["type"]
        if kind in {"affects", "appears_in"}:
            edges.append((a, b))
        elif kind == "depends_on":
            edges.append((b, a))
        elif kind == "shares":
            edges.extend([(a, b), (b, a)])
    while True:
        expanded = affected | {b for a, b in edges if a in affected}
        if expanded == affected:
            return affected
        affected = expanded


def _validate(data: object, project_root: Path) -> dict:
    root = project_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Project root must be a directory")
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return {"ok": False, "errors": ["Record must be an object"], "warnings": [], "limits": LIMITS}
    if data.get("format") != FORMAT:
        errors.append(f"format must be {FORMAT}")
    if not nonempty(data.get("revision")):
        errors.append("Record needs an explicit current product/source revision")

    def fail(where: str, message: str) -> None:
        errors.append(f"{where}: {message}")

    def table(key: str, required: bool = False) -> dict[str, dict]:
        rows = data.get(key, [])
        out: dict[str, dict] = {}
        if not isinstance(rows, list):
            fail(key, "Expected a list"); return out
        if required and not rows:
            fail(key, "At least one entry is needed for this opt-in profile")
        for i, item in enumerate(rows):
            where = f"{key}[{i}]"
            if not isinstance(item, dict) or not nonempty(item.get("id")):
                fail(where, "Expected an object with a nonempty id"); continue
            name = item["id"]
            if name in out:
                fail(where, f"Duplicate id {name}")
            else:
                out[name] = item
        return out

    objects = table("objects", True)
    conditions = table("conditions")
    evidence = table("evidence")
    decisions = table("decisions", True)

    def refs(value: object, known: dict, where: str, required: bool = False) -> list[str]:
        if not isinstance(value, list) or any(not nonempty(x) for x in value):
            fail(where, "Expected a list of reference IDs"); return []
        if required and not value:
            fail(where, "Reference list is empty")
        if len(value) != len(set(value)):
            fail(where, "Duplicate references")
        for x in value:
            if x not in known:
                fail(where, f"Unknown reference {x}")
        return [x for x in value if x in known]

    def location(value: object, where: str) -> Path | None:
        if not isinstance(value, dict) or len(value) != 1 or not ({"path", "url"} & value.keys()):
            fail(where, "Use exactly one path or url"); return None
        if "path" in value:
            try:
                return local_file(root, value["path"])
            except (ValueError, OSError, RuntimeError) as exc:
                fail(where, str(exc)); return None
        raw = value["url"]
        try:
            u = urlsplit(raw) if isinstance(raw, str) else None
            if not u or u.scheme not in {"https", "http"} or not u.hostname or u.username or u.password:
                raise ValueError("Expected an HTTP(S) source URL without credentials")
            _ = u.port
        except (ValueError, TypeError):
            fail(where, "Invalid remote source URL"); return None
        warnings.append(f"{where}: remote availability and content not checked")
        return None

    def exception(value: object, where: str) -> None:
        if not isinstance(value, dict):
            fail(where, "An explicit exception record is required"); return
        for key in ("by", "source", "reason", "scope"):
            if not nonempty(value.get(key)):
                fail(where, f"Exception needs {key}")
        warnings.append(f"{where}: authority and approval authenticity require independent review")

    for oid, obj in objects.items():
        if obj.get("level") not in LEVELS or not nonempty(obj.get("title")):
            fail(oid, "Object needs level L0–L5 and a title")
        parent = obj.get("parent")
        if parent is not None and (not isinstance(parent, str) or parent not in objects):
            fail(oid, "Unknown parent")
        seen = {oid}; current = parent
        while isinstance(current, str) and current in objects:
            if current in seen:
                fail(oid, "Containment cycle"); break
            seen.add(current); current = objects[current].get("parent")
    for cid, condition in conditions.items():
        if not nonempty(condition.get("description")):
            fail(cid, "Condition needs its actual viewing/use description")

    relations = data.get("relations", [])
    if not isinstance(relations, list):
        fail("relations", "Expected a list"); relations = []
    for i, rel in enumerate(relations):
        if not isinstance(rel, dict):
            fail(f"relations[{i}]", "Expected an object"); continue
        if rel.get("type") not in {"affects", "depends_on", "appears_in", "precedes", "transitions_to", "shares"}:
            fail(f"relations[{i}]", "Unknown relationship type")
        refs([rel.get("from"), rel.get("to")], objects, f"relations[{i}]")

    for eid, item in evidence.items():
        if item.get("kind") not in KINDS or item.get("role") not in ROLES:
            fail(eid, "Unknown evidence kind or source role")
        if item.get("status") not in {"acquired", "observed"}:
            fail(eid, "Evidence status must be acquired or observed")
        refs(item.get("objects", []), objects, eid + ".objects", True)
        refs(item.get("conditions", []), conditions, eid + ".conditions")
        path = location(item.get("location"), eid)
        if item.get("status") == "observed" and not nonempty(item.get("observation")):
            fail(eid, "Observed evidence needs the actual inspected portion and observation")
        if item.get("kind") == "temporal" and item.get("status") == "observed":
            if not nonempty(item.get("window")) or not nonempty(item.get("method")):
                fail(eid, "Temporal observation needs its actual window and viewing method")
        if "sha256" in item:
            digest = item["sha256"]
            if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
                fail(eid, "Invalid SHA-256")
            elif path and hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                fail(eid, "Local evidence digest differs")

    for did, decision in decisions.items():
        d_objects = refs(decision.get("objects", []), objects, did + ".objects", True)
        for key in ("purpose", "question"):
            if not nonempty(decision.get(key)):
                fail(did, f"Decision needs {key}")
        refs(decision.get("evidence", []), evidence, did + ".evidence")
        comparison = decision.get("comparison")
        if comparison is not None:
            if not isinstance(comparison, dict) or comparison.get("state") not in {"planned", "compared"}:
                fail(did, "Unknown comparison state")
            elif comparison["state"] == "compared":
                alternatives = comparison.get("alternatives", [])
                if not isinstance(alternatives, list) or any(not nonempty(x) for x in alternatives):
                    fail(did, "Compared alternatives must be named"); alternatives = []
                if len(set(alternatives)) < 2:
                    fail(did, "A declared comparison needs distinct named alternatives")
                compared = refs(comparison.get("evidence", []), evidence, did + ".comparison.evidence", True)
                if not any(evidence[e].get("status") == "observed" for e in compared):
                    fail(did, "Comparison needs observed support, not only acquired sources")
                if not nonempty(comparison.get("rationale")):
                    fail(did, "Comparison needs observed differences and conditions")
        adoption = decision.get("implementation")
        if adoption is not None:
            if not isinstance(adoption, dict) or adoption.get("state") not in {"proposed", "trialed", "adopted"}:
                fail(did, "Unknown implementation state")
            else:
                paths = adoption.get("paths", [])
                if not isinstance(paths, list):
                    fail(did, "Implementation paths must be a list"); paths = []
                if adoption["state"] in {"trialed", "adopted"}:
                    if not paths:
                        fail(did, "Trialed/adopted implementation needs actual local paths")
                    adopted = refs(adoption.get("evidence", []), evidence, did + ".implementation.evidence", True)
                    if adoption["state"] == "trialed" and not any(
                        evidence[e].get("status") == "observed" and evidence[e].get("role") == "trial"
                        and evidence[e].get("product_revision") == data.get("revision")
                        for e in adopted
                    ):
                        fail(did, "Trial needs observed current-project trial evidence")
                for p in paths:
                    location({"path": p}, did + ".implementation")
        approval = decision.get("approval")
        if approval is not None:
            if not isinstance(approval, dict) or approval.get("status") not in {"pending", "provisional", "approved"}:
                fail(did, "Unknown approval state")
            elif approval["status"] == "approved":
                if not nonempty(approval.get("source")) or not nonempty(approval.get("scope")):
                    fail(did, "Approval needs actual source and scope")
                warnings.append(f"{did}: owner approval is declared, not authenticated")

        checks = decision.get("checks", [])
        if not isinstance(checks, list):
            fail(did, "Checks must be a list"); checks = []
        for i, check in enumerate(checks):
            where = f"{did}.checks[{i}]"
            if not isinstance(check, dict):
                fail(where, "Expected an object"); continue
            if check.get("status") not in {"planned", "pass", "fail", "blocked", "waived"}:
                fail(where, "Unknown check status")
            if check.get("domain") not in DOMAINS:
                fail(where, "Unknown verification domain")
            es = refs(check.get("evidence", []), evidence, where + ".evidence")
            os = refs(check.get("objects", d_objects), objects, where + ".objects", True)
            cs = refs(check.get("conditions", []), conditions, where + ".conditions", check.get("status") == "pass")
            if any(x not in d_objects for x in os):
                fail(where, "Check broadens beyond this decision's declared objects")
            if check.get("status") == "waived":
                exception(check.get("exception"), where)
            if check.get("status") == "pass":
                if check.get("revision") != data.get("revision"):
                    fail(where, "Passing check is stale or lacks the current revision")
                if not nonempty(check.get("finding")):
                    fail(where, "Passing check needs its scoped observed finding")
                role = check.get("role", "integrated")
                if role not in {"trial", "integrated"}:
                    fail(where, "Current-project check must identify trial or integrated scope")
                suitable = [evidence[e] for e in es if evidence[e].get("status") == "observed"
                            and evidence[e].get("kind") in DOMAINS.get(check.get("domain"), set())
                            and evidence[e].get("role") == role
                            and evidence[e].get("product_revision") == data.get("revision")]
                # Every declared object-condition pair must have a matching observation.
                if not suitable or any(not any(o in e.get("objects", []) and c in e.get("conditions", [])
                                               for e in suitable) for o in os for c in cs):
                    fail(where, "Pass lacks observed, matching-domain/object/condition/revision evidence")

        gaps = decision.get("gaps", [])
        if not isinstance(gaps, list):
            fail(did, "Gaps must be a list"); gaps = []
        gap_ids: set[str] = set(); unresolved: list[dict] = []
        for i, gap in enumerate(gaps):
            where = f"{did}.gaps[{i}]"
            if not isinstance(gap, dict) or not nonempty(gap.get("id")):
                fail(where, "Expected a gap with id"); continue
            if gap["id"] in gap_ids:
                fail(where, "Duplicate gap id")
            gap_ids.add(gap["id"])
            if gap.get("status") not in {"open", "blocked", "resolved", "waived"} or gap.get("impact") not in {"low", "standard", "high"}:
                fail(where, "Unknown gap status or impact")
            refs(gap.get("objects", d_objects), objects, where + ".objects", True)
            if not nonempty(gap.get("question")):
                fail(where, "Gap needs a question")
            if gap.get("status") in {"open", "blocked"}:
                unresolved.append(gap)
                if gap.get("impact") == "high" and not nonempty(gap.get("next_action")):
                    fail(where, "Important gap needs a concrete next evidence-producing action")
            if gap.get("status") == "resolved":
                refs(gap.get("resolution_evidence", []), evidence, where + ".resolution_evidence", True)
            if gap.get("status") == "waived":
                exception(gap.get("exception"), where)
        action = decision.get("next_action")
        if not isinstance(action, dict) or action.get("kind") not in ACTIONS or not nonempty(action.get("reason")):
            fail(did, "Decision needs a supported next action and reason")
        else:
            scope = refs(action.get("objects", d_objects), objects, did + ".next_action.objects", True)
            if action["kind"] in {"expand", "finish"}:
                for key in ("judgment", "choice"):
                    if not nonempty(decision.get(key)):
                        fail(did, f"Expansion/finish needs an explicit {key}")
                for gap in unresolved:
                    if gap.get("impact") == "high" and set(scope) & affected_objects(data, gap.get("objects", d_objects)):
                        fail(did, "Dependent expansion/finish contradicts an unresolved high-impact gap")
                if unresolved and not any(set(scope) & affected_objects(data, g.get("objects", d_objects)) for g in unresolved):
                    if not nonempty(action.get("independent_reason")):
                        fail(did, "Independent progress needs its dependency explanation")

    challenges = data.get("coverage_challenges", [])
    if not isinstance(challenges, list):
        fail("coverage_challenges", "Expected a list"); challenges = []
    for i, row in enumerate(challenges):
        where = f"coverage_challenges[{i}]"
        if not isinstance(row, dict):
            fail(where, "Expected an object"); continue
        if row.get("disposition") not in {"include", "exclude", "open"}:
            fail(where, "Expected include, exclude or open")
        for key in ("discovery", "reason"):
            if not nonempty(row.get(key)):
                fail(where, f"Coverage challenge needs {key}")
        refs(row.get("evidence", []), evidence, where + ".evidence")
        refs(row.get("objects", []), objects, where + ".objects")
        if row.get("disposition") == "open" and not nonempty(row.get("next_action")):
            fail(where, "Open coverage discovery needs its next action")

    requirements = data.get("required_checks", [])
    pending_coverage = []
    if not isinstance(requirements, list):
        fail("required_checks", "Expected a list"); requirements = []
    for i, requirement in enumerate(requirements):
        where = f"required_checks[{i}]"
        if not isinstance(requirement, dict):
            fail(where, "Expected an object"); continue
        oid, cid, domain = (requirement.get(k) for k in ("object", "condition", "domain"))
        if not isinstance(oid, str) or oid not in objects or not isinstance(cid, str) or cid not in conditions or not isinstance(domain, str) or domain not in DOMAINS:
            fail(where, "Unknown required object, condition or domain"); continue
        required_role = requirement.get("role", "integrated")
        if required_role not in {"trial", "integrated"}:
            fail(where, "Required check role must be trial or integrated"); continue
        matching = [c for d in decisions.values() for c in d.get("checks", [])
                    if isinstance(c, dict) and oid in c.get("objects", d.get("objects", []))
                    and cid in c.get("conditions", []) and c.get("domain") == domain
                    and c.get("role", "integrated") == required_role]
        if not any(c.get("status") in {"pass", "waived"} for c in matching):
            pending_coverage.append(requirement)
            for did, decision in decisions.items():
                action = decision.get("next_action", {})
                if isinstance(action, dict) and action.get("kind") == "finish" and set(action.get("objects", decision.get("objects", []))) & affected_objects(data, [oid]):
                    fail(did, "Finish includes a required condition whose check is missing or unresolved")

    return {"ok": not errors, "errors": errors, "warnings": warnings, "limits": LIMITS,
            "pending_coverage": pending_coverage,
            "counts": {"objects": len(objects), "evidence": len(evidence), "decisions": len(decisions)}}


def validate(data: object, project_root: Path) -> dict:
    """Return a diagnostic for malformed declarations; root/read failures remain input errors."""
    try:
        return _validate(data, project_root)
    except (TypeError, AttributeError, KeyError) as exc:
        return {"ok": False, "errors": [f"Malformed field type or required field: {exc}"],
                "warnings": [], "limits": LIMITS}


def project_view(data: dict, view: str, changed: list[str] | None = None) -> dict:
    """Filter the same records; never rewrite status or manufacture a quality score."""
    objects = {o["id"]: o for o in data.get("objects", [])}
    affected = affected_objects(data, changed or [])
    decisions = data.get("decisions", [])
    if view == "overview":
        result = {"objects": list(objects.values()), "coverage_challenges": data.get("coverage_challenges", []),
                  "decisions": [{k: d.get(k) for k in ("id", "objects", "purpose", "question", "gaps", "next_action")} for d in decisions]}
    elif view == "execution":
        result = {"decisions": [{k: d.get(k) for k in ("id", "objects", "implementation", "checks", "approval", "gaps", "next_action")} for d in decisions]}
    elif view == "detail":
        result = {"decisions": decisions, "evidence": data.get("evidence", []), "conditions": data.get("conditions", []), "relations": data.get("relations", [])}
    else:
        raise ValueError("Unknown view")
    result["review_candidates_after_change"] = sorted(affected)
    result["affected_decisions"] = [d["id"] for d in decisions if affected.intersection(d["objects"])]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--record", default=".ui-spec/design-evidence.json", help="Project-relative JSON file")
    parser.add_argument("--view", choices=("overview", "detail", "execution"), default="overview")
    parser.add_argument("--changed", action="append", default=[], help="Changed object ID; repeat as needed")
    args = parser.parse_args()
    try:
        root = args.project_root.resolve(strict=True)
        data = json.loads(local_file(root, args.record).read_text(encoding="utf-8"))
        result = validate(data, root)
        if result["ok"]:
            result["view"] = project_view(data, args.view, args.changed)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1
    except (OSError, ValueError, TypeError, RuntimeError, RecursionError) as exc:
        print(f"check_design_evidence: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
