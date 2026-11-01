#!/usr/bin/env python3
"""Local adapter inspection; no credential inspection, model calls or GUI claims."""
from __future__ import annotations
import argparse,json,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).absolute().parent))
import install

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    s=p.add_mutually_exclusive_group(required=True)
    s.add_argument('--project');s.add_argument('--user',action='store_true')
    a=p.parse_args(argv)
    report={'check_scope':'local files and CLI version only','role_spawn':'not_tested','model_access':'not_tested',
            'tool_inheritance':'not_tested','gui_observation':'not_tested','authenticated_agent_runs':0}
    try:
        root=install.codex_root(a.project,a.user)
        version,roles=install.bundle()
        report.update(adapter_version=version,distributed_roles=list(roles),installation=install.execute(root,'status'))
        executable=shutil.which('codex');report['codex_executable']=executable
        if executable:
            result=subprocess.run([executable,'--version'],capture_output=True,text=True,timeout=10,check=False)
            report['codex_version']={'returncode':result.returncode,'stdout':result.stdout.strip()[:200]}
        else: report['codex_version']=None
        try:
            import tomllib
            for name,data in roles.items():
                obj=tomllib.loads(data.decode())
                for key in ('name','description','developer_instructions'):
                    if not isinstance(obj.get(key),str) or not obj[key].strip(): raise ValueError(f'Missing {key}: {name}')
                if obj['name']!=name: raise ValueError(f'Role name mismatch: {name}')
            report['toml_syntax']='parsed'
            config=install.regular(install.safe(root,'config.toml'))
            parsed=tomllib.loads(config.decode()) if config is not None else {}
            entries=parsed.get('agents',{})
            report['native_registration']={name:'configured' if isinstance(entries,dict) and isinstance(entries.get(name),dict) and entries[name].get('config_file')==f'agents/{name}.toml' else 'missing_or_different' for name in roles}
        except ImportError:
            report['toml_syntax']='not_parsed: Python 3.11+ provides tomllib; installation uses manifest integrity only'
            report['native_registration']='not_parsed; inspect managed-block status and run a native smoke'
        print(json.dumps(report,indent=2));return 0
    except (OSError,ValueError,subprocess.SubprocessError) as e:
        report['error']=str(e);print(json.dumps(report,indent=2));return 2
if __name__=='__main__': raise SystemExit(main())
