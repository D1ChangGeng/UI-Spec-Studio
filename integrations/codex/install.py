#!/usr/bin/env python3
"""Non-destructive, ownership-aware installation of all four explicit Codex roles.

Python 3.10+, standard library only; merging an existing config requires 3.11+.
Registers four roles in an owned config.toml block, preserving other settings.
It does not alter AGENTS.md, credentials, permissions, models or Skill files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from contextlib import contextmanager

SOURCE = Path(__file__).absolute().parent
# Explicit install selects all distributed roles. Invocation remains on-demand.
ROLES = ('ui_researcher', 'ui_integrator', 'ui_challenger', 'ui_experience_observer')
# Retained for callers of the older development candidate; it no longer controls selection.
CORE = ROLES[:2]
OPTIONAL = ROLES[2:]
RECEIPT = 'ui-spec-studio/installation.json'
LOCK = 'ui-spec-studio/install.lock'
CONFIG = 'config.toml'
CONFIG_BEGIN = '# >>> UI Spec Studio managed role registrations >>>\n'
CONFIG_END = '# <<< UI Spec Studio managed role registrations <<<\n'
VERSION_RE = re.compile(r'\d+\.\d+\.\d+\Z')
HASH_RE = re.compile(r'[a-f0-9]{64}\Z')


class InstallError(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def regular(path: Path) -> bytes | None:
    if path.is_symlink():
        raise InstallError(f'Refusing symlink: {path}')
    if not path.exists():
        return None
    if not path.is_file():
        raise InstallError(f'Expected a regular file: {path}')
    return path.read_bytes()


def safe(root: Path, relative: str) -> Path:
    rel = PurePosixPath(relative)
    if rel.is_absolute() or '\\' in relative or '..' in rel.parts or not rel.parts:
        raise InstallError(f'Unsafe relative path: {relative}')
    root = root.absolute()
    # Refuse existing links/junctions throughout the destination ancestry.
    for part in (root, *root.parents):
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise InstallError(f'Refusing linked destination ancestor: {part}')
    path = root
    for name in rel.parts:
        path = path / name
        if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
            raise InstallError(f'Refusing linked destination: {path}')
    return path


def codex_root(project: str | None, user: bool) -> Path:
    if bool(project) == bool(user):
        raise InstallError('Select exactly one explicit --project PATH or --user scope')
    if project:
        return Path(project).expanduser().absolute() / '.codex'
    return Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex'))).expanduser().absolute()


def bundle(source: Path = SOURCE) -> tuple[str, dict[str, bytes]]:
    manifest_bytes = regular(safe(source, 'manifest.json'))
    if manifest_bytes is None:
        raise InstallError('Adapter manifest is missing')
    try:
        data = json.loads(manifest_bytes)
    except (ValueError, UnicodeError) as exc:
        raise InstallError('Adapter manifest is not readable JSON') from exc
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise InstallError('Unsupported adapter manifest')
    version = data.get('version', '')
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise InstallError('Invalid adapter version')
    rows = data.get('roles')
    if not isinstance(rows, dict) or set(rows) != set(ROLES):
        raise InstallError('Manifest must identify exactly the four distributed roles')
    result = {}
    for name in ROLES:
        row = rows[name]
        expected_path = f'agents/{name}.toml'
        if not isinstance(row, dict) or row.get('path') != expected_path:
            raise InstallError(f'Invalid role path: {name}')
        if row.get('default_install') is not True:
            raise InstallError(f'All distributed roles must be installed by default: {name}')
        content = regular(safe(source, expected_path))
        if content is None or digest(content) != row.get('sha256'):
            raise InstallError(f'Role bytes differ from adapter manifest: {name}')
        result[name] = content
    return version, result


def receipt(root: Path) -> tuple[dict, bytes | None]:
    raw = regular(safe(root, RECEIPT))
    if raw is None:
        return {'schema_version': 1, 'version': None, 'files': {}, 'registration': None}, None
    try:
        data = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise InstallError('Existing ownership receipt is unreadable; preserve it for inspection') from exc
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise InstallError('Unknown ownership receipt format')
    if not isinstance(data.get('version'), str) or not VERSION_RE.fullmatch(data['version']):
        raise InstallError('Invalid installed version in receipt')
    rows = data.get('files')
    allowed = {f'agents/{name}.toml' for name in ROLES}
    if not isinstance(rows, dict) or not set(rows).issubset(allowed):
        raise InstallError('Ownership receipt contains unsupported paths')
    for rel, row in rows.items():
        if not isinstance(row, dict) or not isinstance(row.get('sha256'), str) or not HASH_RE.fullmatch(row['sha256']):
            raise InstallError(f'Invalid owned file identity: {rel}')
    registration=data.get('registration')
    if registration is not None:
        if not isinstance(registration,dict) or not isinstance(registration.get('block'),str) or type(registration.get('created_file')) is not bool:
            raise InstallError('Invalid managed config registration receipt')
        block=registration['block'].encode('utf-8')
        if not registration['block'].lstrip('\n').startswith(CONFIG_BEGIN) or not registration['block'].endswith(CONFIG_END) or digest(block)!=registration.get('sha256'):
            raise InstallError('Invalid managed config registration identity')
    data['registration']=registration
    return data, raw


def _receipt_bytes(version: str, files: dict, registration:dict|None=None) -> bytes:
    return (json.dumps({'schema_version': 1, 'version': version, 'files': files, 'registration':registration}, indent=2, sort_keys=True)+'\n').encode()


def config_block(available:dict[str,bytes])->bytes:
    lines=[CONFIG_BEGIN.rstrip('\n')]
    for name in ROLES:
        match=re.search(r'^description\s*=\s*("[^\n]*")\s*$',available[name].decode('utf-8'),re.M)
        if not match:raise InstallError(f'Role description must be a single TOML basic string: {name}')
        try:description=json.loads(match[1])
        except ValueError as exc:raise InstallError(f'Unsupported role description string: {name}') from exc
        lines.extend((f'[agents.{name}]',f'description = {json.dumps(description)}',f'config_file = "agents/{name}.toml"',''))
    return ('\n'.join(lines)+CONFIG_END).encode('utf-8')


def validate_existing_config(raw:bytes)->None:
    if not raw.strip():return
    try:import tomllib
    except ImportError as exc:
        raise InstallError('Merging existing config.toml requires Python 3.11+ for TOML validation; no files changed') from exc
    try:data=tomllib.loads(raw.decode('utf-8'))
    except (ValueError,UnicodeError) as exc:raise InstallError('Existing config.toml is not valid TOML; no files changed') from exc
    agents=data.get('agents',{})
    if not isinstance(agents,dict):raise InstallError('Existing agents configuration cannot be extended safely')
    if any(name in agents for name in ROLES):raise InstallError('Existing UI Spec role registration is unmanaged; no configuration overwritten')
    # An inline root table cannot be extended by later [agents.role] tables.
    if re.search(r'^\s*(?:agents|"agents"|\'agents\')\s*=',raw.decode('utf-8'),re.M):
        raise InstallError('Inline or assigned agents configuration requires manual integration; no files changed')


def plan_registration(root:Path,old:dict,available:dict[str,bytes]|None,action:str)->tuple[dict|None,tuple|None,str]:
    raw=regular(safe(root,CONFIG));registration=old.get('registration')
    existing=raw or b''
    if registration:
        block=registration['block'].encode('utf-8')
        if raw is None:
            if action=='uninstall':return None,None,'forget_missing_registration'
            prefix=b''
        elif existing.count(block)!=1:
            raise InstallError('Managed config registration was modified; preserve it and referenced roles for review')
        else:prefix=existing.replace(block,b'',1)
    else:
        prefix=existing
        if CONFIG_BEGIN.encode() in existing or CONFIG_END.encode() in existing:
            raise InstallError('Unowned UI Spec config markers found; no configuration overwritten')
    if action=='uninstall':
        if not registration:return None,None,'no_owned_registration'
        after=None if not prefix and registration['created_file'] else prefix
        return None,(CONFIG,raw,after) if raw!=after else None,'remove_owned_registration'
    validate_existing_config(prefix)
    new_block=config_block(available)
    if registration and raw is not None:
        leading=block[:len(block)-len(block.lstrip(b'\n'))]
        new_block=leading+new_block
        after=existing.replace(block,new_block,1)
        created_file=registration['created_file']
    else:
        new_block=(b'\n' if prefix else b'')+new_block
        after=prefix+new_block
        created_file=raw is None
    # A parsed before/after comparison protects all settings outside the block.
    try:import tomllib
    except ImportError:pass
    else:
        try:parsed=tomllib.loads(after.decode('utf-8'))
        except (ValueError,UnicodeError) as exc:raise InstallError('Merged role registration is not valid TOML; no files changed') from exc
        for name in ROLES:
            if parsed.get('agents',{}).get(name,{}).get('config_file')!=f'agents/{name}.toml':
                raise InstallError('Merged role registration did not preserve the required source path')
    record={'block':new_block.decode('utf-8'),'sha256':digest(new_block),'created_file':created_file}
    return record,(CONFIG,raw,after) if raw!=after else None,'register_roles' if not registration else 'owned_registration_unchanged' if raw==after else 'update_owned_registration'


def plan(root: Path, action: str, source: Path = SOURCE, *, with_optional=False,
         upgrade=False, allow_downgrade=False) -> tuple[dict, list[tuple[str, bytes | None, bytes | None]]]:
    if action not in {'install', 'uninstall', 'status'}:
        raise InstallError('Unknown action')
    old, old_raw = receipt(root)
    report = {'action': action, 'root': str(root), 'installed_version': old['version'],
              'operations': [], 'conflicts': [], 'runtime_discovery_verified': False}
    changes = []
    owned = dict(old['files'])
    if action == 'status':
        for rel, row in owned.items():
            raw = regular(safe(root, rel))
            state = 'missing' if raw is None else 'owned_unchanged' if digest(raw)==row['sha256'] else 'modified_retained'
            report['operations'].append({'path': rel, 'state': state})
        if old.get('registration'):
            raw=regular(safe(root,CONFIG));block=old['registration']['block'].encode('utf-8')
            state='missing' if raw is None else 'owned_unchanged' if raw.count(block)==1 else 'modified_retained'
            report['operations'].append({'path':CONFIG,'state':state,'scope':'managed role block only'})
        return report, changes
    if action == 'uninstall':
        try:registration,config_change,state=plan_registration(root,old,None,'uninstall')
        except InstallError as exc:
            report['conflicts'].append({'path':CONFIG,'reason':str(exc)});return report,[]
        if config_change:changes.append(config_change)
        report['operations'].append({'path':CONFIG,'state':state})
        for rel, row in old['files'].items():
            raw = regular(safe(root, rel))
            if raw is not None and digest(raw) != row['sha256']:
                report['conflicts'].append({'path': rel, 'reason': 'modified; retained'})
                continue
            if raw is not None:
                changes.append((rel, raw, None))
            owned.pop(rel)
            report['operations'].append({'path': rel, 'state': 'remove_owned' if raw is not None else 'forget_missing'})
        new_raw = _receipt_bytes(old['version'], owned,registration) if owned else None
        if new_raw != old_raw:
            changes.append((RECEIPT, old_raw, new_raw))
        return report, changes
    version, available = bundle(source)
    report['candidate_version'] = version
    if allow_downgrade and not upgrade:
        raise InstallError('--allow-downgrade also requires --upgrade')
    if old['version'] and tuple(map(int,version.split('.'))) < tuple(map(int,old['version'].split('.'))) and not allow_downgrade:
        raise InstallError('Downgrade requires reviewed --upgrade --allow-downgrade')
    # --with-optional is an accepted legacy no-op; all four roles are always selected.
    for name in ROLES:
        rel, new = f'agents/{name}.toml', available[name]
        raw = regular(safe(root, rel))
        row = owned.get(rel)
        if row and raw is not None and digest(raw) != row['sha256']:
            report['conflicts'].append({'path':rel,'reason':'owned file modified; not overwritten'})
        elif raw == new:
            report['operations'].append({'path':rel,'state':'already_owned' if row else 'identical_unmanaged_preserved'})
        elif raw is not None and not row:
            report['conflicts'].append({'path':rel,'reason':'unmanaged existing file; not overwritten'})
        elif raw is not None and not upgrade:
            report['conflicts'].append({'path':rel,'reason':'managed upgrade requires --upgrade'})
        else:
            changes.append((rel,raw,new))
            owned[rel]={'sha256':digest(new)}
            report['operations'].append({'path':rel,'state':'install' if raw is None else 'upgrade_owned'})
    try:registration,config_change,state=plan_registration(root,old,available,'install')
    except InstallError as exc:
        report['conflicts'].append({'path':CONFIG,'reason':str(exc)})
    else:
        if config_change:changes.append(config_change)
        report['operations'].append({'path':CONFIG,'state':state,'scope':'managed role block only'})
    if report['conflicts']:
        # Installation is all-or-nothing, even when other requested roles are absent.
        return report, []
    new_raw = _receipt_bytes(version,owned,registration) if owned or registration else old_raw
    if new_raw != old_raw:
        changes.append((RECEIPT,old_raw,new_raw))
    return report,changes


@contextmanager
def lock(root: Path):
    path = safe(root,LOCK)
    path.parent.mkdir(parents=True,exist_ok=True)
    try:
        fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except FileExistsError as exc:
        raise InstallError('Another install may be active. Inspect the existing lock; it is not removed automatically.') from exc
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as stream:
            stream.write(json.dumps({'pid':os.getpid()}))
        yield
    finally:
        path.unlink(missing_ok=True)


def atomic(path: Path, data: bytes | None):
    if data is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.ui-spec-',dir=str(path.parent))
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(data);stream.flush();os.fsync(stream.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def transact(root: Path, changes):
    written=[]
    try:
        for rel,before,after in changes:
            path=safe(root,rel)
            if regular(path)!=before:
                raise InstallError(f'Concurrent change detected; refusing replacement: {rel}')
            atomic(path,after)
            written.append((rel,before,after))
    except BaseException as exc:
        retained=[]
        for rel,before,after in reversed(written):
            try:
                path=safe(root,rel)
                if regular(path)==after: atomic(path,before)
                else: retained.append(rel)
            except OSError: retained.append(rel)
        if retained:
            raise InstallError('Transaction failed; concurrent/failed rollback files preserved: '+', '.join(retained)) from exc
        raise


def execute(root: Path, action: str, source: Path=SOURCE, *, dry_run=False,
            with_optional=False,upgrade=False,allow_downgrade=False) -> dict:
    options=dict(with_optional=with_optional,upgrade=upgrade,allow_downgrade=allow_downgrade)
    report,changes=plan(root,action,source,**options)
    report['dry_run']=dry_run
    report['changed_files']=len(changes)
    if action=='status' or dry_run or (action=='install' and report['conflicts']):
        return report
    if not changes: return report
    with lock(root):
        report,changes=plan(root,action,source,**options)
        report.update(dry_run=False,changed_files=len(changes))
        if action=='install' and report['conflicts']: return report
        transact(root,changes)
    return report


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('install','status','uninstall'))
    scope=parser.add_mutually_exclusive_group(required=True)
    scope.add_argument('--project');scope.add_argument('--user',action='store_true')
    parser.add_argument('--with-optional',action='store_true',help=argparse.SUPPRESS) # legacy no-op
    parser.add_argument('--upgrade',action='store_true')
    parser.add_argument('--allow-downgrade',action='store_true')
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args(argv)
    try:
        report=execute(codex_root(args.project,args.user),args.action,dry_run=args.dry_run,
                       with_optional=args.with_optional,upgrade=args.upgrade,allow_downgrade=args.allow_downgrade)
        print(json.dumps(report,indent=2))
        return 2 if report['conflicts'] else 0
    except (InstallError,OSError,UnicodeError) as exc:
        print(f'ui-spec adapter: {exc}',file=sys.stderr);return 2


if __name__=='__main__':
    raise SystemExit(main())
