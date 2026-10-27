#!/usr/bin/env python3
"""Validate portable package structure, metadata and local reference integrity."""
from __future__ import annotations
import json
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
COMMON = ("workflow", "analysis", "principles", "component-sourcing", "interaction-and-variants", "verification", "visual-assets", "content-design")
REQUIRED = ["docs/CONTENT-DESIGN.md", "docs/REVIEW-v1.6.0.md", "skills/ui-spec/references/content-sources.md", "skills/ui-spec/assets/templates/content-decisions.md", "examples/content-review/index.html", "examples/content-review/README.md", "tools/validate_content.py", "docs/VISUAL-ASSETS.md", "docs/REVIEW-v1.5.0.md", "skills/ui-spec/references/asset-sources.md", "skills/ui-spec/assets/templates/asset-record.md", "examples/asset-review/index.html", "examples/asset-review/README.md", "tools/validate_assets.py", "examples/product-intent/FOUNDATION.md", "examples/product-intent/foundation.json", "docs/DESIGN-DECISIONS.md", "docs/REVIEW-v1.4.0.md", "skills/ui-spec/assets/templates/design-decisions.md", "examples/product-intent/index.html", "examples/product-intent/styles.css", "examples/product-intent/app.js", "examples/product-intent/tokens.css", "examples/product-intent/README.md", "examples/product-intent/THIRD-PARTY.md", "tools/validate_scenario.py", "README.md", "README.zh-CN.md", "LICENSE", "VERSION", "AGENTS.md", "SECURITY.md", "CONTRIBUTING.md",
            "skills/ui-spec/SKILL.md", "skills/ui-spec/LICENSE", "skills/ui-spec/scripts/prepare.py",
            "skills/ui-spec/scripts/check_manifest.py", "docs/INSTALL.md", "docs/GUIDE.md", "docs/MODEL.md",
            "docs/WRITING.md", "docs/REVIEW.md", "docs/MANIFEST.md", "docs/RESEARCH.md", "docs/EVALUATION.md",
            "docs/PUBLISHING.md", "docs/PROFESSIONAL-MODEL.md", "docs/REVIEW-v1.2.0.md",
            "docs/RESOURCE-REUSE.md", "docs/REVIEW-v1.3.0.md", "skills/ui-spec/references/resource-catalog.md",
            "skills/ui-spec/assets/resource-catalog.json", "skills/ui-spec/scripts/find_resources.py",
            "skills/ui-spec/assets/templates/resource-adoption.md", "docs/design/README-SPEC.md", "skills/ui-spec/references/patterns.md", "skills/ui-spec/references/integration.md",
            *[f"skills/ui-spec/references/{name}.md" for name in COMMON]]
REQUIRED += ["docs/VISUAL-INSPECTION.md", "docs/REVIEW-v1.7.0.md",
             "examples/temporal-review/index.html", "examples/temporal-review/styles.css",
             "examples/temporal-review/app.js", "examples/temporal-review/README.md",
             "tools/validate_temporal.py"]
REQUIRED += ["docs/PRODUCT-ALIGNMENT.md", "docs/REVIEW-v1.8.0.md"]
REQUIRED += ["docs/REVIEW-v1.9.0.md"]
REQUIRED += ["docs/REVIEW-v1.10.0.md"]
REQUIRED += ["docs/ART-DIRECTION.md", "docs/REVIEW-v1.11.0.md"]
REQUIRED += ["docs/EXPERIENCE-RESEARCH.md", "docs/REVIEW-v1.12.0.md"]
REQUIRED += ["docs/CONTENT-INTEGRITY.md", "docs/REVIEW-v1.13.0.md",
             "docs/evidence/v1.13.0/lineage.json",
             "tests/test_content_integrity.py"]
REQUIRED += ["docs/DESIGN-EVIDENCE.md", "docs/REVIEW-v1.14.0.md",
             "skills/ui-spec/references/evidence-map.md", "skills/ui-spec/references/evidence-actions.md",
             "skills/ui-spec/references/evidence-records.md", "skills/ui-spec/scripts/check_design_evidence.py",
             "skills/ui-spec/assets/templates/design-evidence.json", "tests/test_design_evidence.py",
             "tests/test_multiscale_release.py", "tools/prepare_design_experiment.py",
             "docs/experiments/design-evidence/PROTOCOL.md", "docs/experiments/design-evidence/baseline-identity.json",
             "docs/evidence/v1.14.0/source-preservation.json", "docs/evidence/v1.14.0/engineering-checks.json"]
REQUIRED += ["docs/STRUCTURAL-INSPECTION.md", "docs/REVIEW-v1.15.0.md",
             "docs/evidence/v1.15.0/continuity.json",
             "skills/ui-spec/scripts/structural_records.py",
             "skills/ui-spec/scripts/check_file_integrity.py",
             "skills/ui-spec/assets/design-coverage-categories.json"]
IGNORED = {".git", "dist", "node_modules", "__pycache__", ".pytest_cache"}



class ImageLinks(HTMLParser):
    """Read passive image sources from native Markdown HTML."""
    def __init__(self):
        super().__init__(); self.targets=[]; self.errors=[]
    def handle_starttag(self, tag, attrs):
        values=dict(attrs)
        if tag == 'img':
            if not values.get('alt'): self.errors.append('Image requires meaningful alt text')
            if values.get('src'): self.targets.append(values['src'])
        if tag == 'source' and values.get('srcset'):
            for item in values['srcset'].split(','):
                target=item.strip().split()
                if target: self.targets.append(target[0])


def check_svg(path: Path) -> list[str]:
    """Publication SVG is static local geometry with no embedded active content."""
    errors=[]
    try:
        text=path.read_text(encoding='utf-8')
        if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
            return ['SVG must use literal self-contained markup']
        root=ET.fromstring(text)
    except (OSError, UnicodeError, ET.ParseError) as exc:
        return [f'Invalid SVG: {exc}']
    if root.tag != '{http://www.w3.org/2000/svg}svg' or not root.get('viewBox'):
        errors.append('SVG needs its namespace and responsive viewBox')
    if not any(e.tag.endswith('}title') and e.text for e in root):
        errors.append('SVG needs a descriptive title')
    for element in root.iter():
        name=element.tag.rsplit('}',1)[-1].lower()
        if name in {'script','foreignobject','image','use','style','animate','animatetransform','set'}:
            errors.append(f'Publication SVG must be inert geometry: {name}')
        for attr,value in element.attrib.items():
            local=attr.rsplit('}',1)[-1].lower()
            if local.startswith('on') or local in {'href','src'} or 'url(' in value.lower():
                errors.append(f'Publication SVG must be self-contained: {local}')
    return errors

def validate(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for name in REQUIRED:
        path = root / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size == 0:
            errors.append(f"Required regular file missing or empty: {name}")
    skill = root / "skills/ui-spec/SKILL.md"
    if not skill.is_file() or skill.is_symlink():
        return errors
    try:
        text = skill.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return errors + [f"SKILL.md read failed: {exc}"]
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append("SKILL.md requires YAML frontmatter")
    else:
        header = match.group(1)
        def scalar(name: str) -> str:
            value = re.search(rf"^{re.escape(name)}:\s*(.+)$", header, re.M)
            if not value:
                return ""
            raw = value.group(1).strip()
            try:
                parsed = json.loads(raw) if raw.startswith('"') else raw
            except ValueError:
                errors.append(f"Invalid scalar: {name}")
                return ""
            return parsed if isinstance(parsed, str) else ""
        name = scalar("name")
        if name != skill.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append("Skill name must match its directory and Agent Skills naming rules")
        if not 1 <= len(scalar("description")) <= 1024:
            errors.append("Description must have 1–1024 characters")
        if len(scalar("compatibility")) > 500:
            errors.append("Compatibility must have <= 500 characters")
    # The entry is a navigational document, not a hard information-volume ceiling.
    # Move detailed methods into installed references without deleting their content.
    for name in COMMON:
        if f"references/{name}.md" not in text:
            errors.append(f"Entry must directly link the common reference: {name}")
    version_path = root / "VERSION"
    if version_path.is_file():
        version = version_path.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
            errors.append("VERSION must use major.minor.patch")
        if f'version: "{version}"' not in text:
            errors.append("Skill metadata and VERSION must match")
        if not (root / "docs/releases" / f"v{version}.md").is_file():
            errors.append("Version-specific release notes are required")
    for md in root.rglob("*.md"):
        if any(p in IGNORED for p in md.relative_to(root).parts):
            continue
        if md.is_symlink():
            errors.append(f"Package Markdown must be a regular file: {md.relative_to(root)}")
            continue
        try:
            body = md.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"Markdown read failed: {md.relative_to(root)}: {exc}")
            continue
        images=ImageLinks();images.feed(body)
        errors.extend(f'{md.relative_to(root)}: {message}' for message in images.errors)
        targets=re.findall(r"\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", body)+images.targets
        for target in targets:
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            target = unquote(target.split("#", 1)[0])
            try:
                candidate = (md.parent / target).resolve()
                candidate.relative_to(root)
            except (ValueError, OSError, RuntimeError):
                errors.append(f"Reference leaves repository or cannot resolve: {md.relative_to(root)} -> {target}")
                continue
            if not candidate.exists():
                errors.append(f"Broken local link: {md.relative_to(root)} -> {target}")
            if md.is_relative_to(skill.parent) and not candidate.is_relative_to(skill.parent):
                errors.append(f"Installed skill reference leaves its bundle: {target}")
    for svg in (root / 'docs/assets').glob('*.svg'):
        errors.extend(f'{svg.relative_to(root)}: {message}' for message in check_svg(svg))
    return errors


if __name__ == "__main__":
    problems = validate()
    if problems:
        print("\n".join(problems), file=sys.stderr)
        raise SystemExit(1)
    print("Package structure, metadata, common-reference links and local paths: PASS")
