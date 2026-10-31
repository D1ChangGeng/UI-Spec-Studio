"""Mechanical installer/role regression tests; not independent Agent experiments."""
from __future__ import annotations
import importlib.util,json,os,shutil,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
ADAPTER=ROOT/'integrations/codex'
spec=importlib.util.spec_from_file_location('ui_spec_adapter_install',ADAPTER/'install.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name);self.root=self.base/'project/.codex'
        self.source=self.base/'source';shutil.copytree(ADAPTER,self.source)
    def run_install(self,**kw): return mod.execute(self.root,'install',self.source,**kw)
    def new_version(self,version='1.20.1',role='ui_researcher'):
        p=self.source/f'agents/{role}.toml';p.write_bytes(p.read_bytes()+b'\n# checked update\n')
        m=self.source/'manifest.json';d=json.loads(m.read_text());d['version']=version
        d['roles'][role]['sha256']=mod.digest(p.read_bytes());m.write_text(json.dumps(d))
    def test_all_four_default_after_explicit_install(self):
        self.assertFalse(self.run_install()['conflicts'])
        self.assertEqual(sorted(p.stem for p in (self.root/'agents').glob('*.toml')),sorted(mod.ROLES))
        record, _ = mod.receipt(self.root)
        self.assertEqual(sorted(record['files']),sorted(f'agents/{name}.toml' for name in mod.ROLES))
    def test_previous_with_optional_flag_is_compatible_noop(self):
        self.run_install(with_optional=True)
        self.assertEqual(sorted(p.stem for p in (self.root/'agents').glob('*.toml')),sorted(mod.ROLES))
    def test_transition_from_previous_two_role_install(self):
        # A user of the previous candidate can explicitly install the revised adapter
        # without overwriting the two already-owned, unchanged role files.
        self.run_install()
        old, _ = mod.receipt(self.root)
        for name in mod.OPTIONAL:
            rel = f'agents/{name}.toml'
            (self.root/rel).unlink()
            old['files'].pop(rel)
        (self.root/mod.RECEIPT).write_bytes(mod._receipt_bytes(old['version'],old['files']))
        (self.root/'config.toml').unlink() # older candidate did not register roles
        result = self.run_install()
        self.assertFalse(result['conflicts'])
        self.assertEqual(sorted(p.stem for p in (self.root/'agents').glob('*.toml')),sorted(mod.ROLES))
        self.assertEqual(result['changed_files'],4) # new roles + config + ownership receipt
    def test_manifest_must_default_install_every_role(self):
        path = self.source/'manifest.json'
        obj = json.loads(path.read_text())
        obj['roles']['ui_challenger']['default_install'] = False
        path.write_text(json.dumps(obj))
        with self.assertRaises(mod.InstallError): self.run_install()
        self.assertFalse(self.root.exists())
    def test_dry_run_creates_nothing(self):
        r=self.run_install(dry_run=True);self.assertGreater(r['changed_files'],0);self.assertFalse(self.root.exists())
    def test_idempotent(self):
        self.run_install();before={p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(self.run_install()['changed_files'],0)
        self.assertEqual(before,{p.relative_to(self.root):p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
    def test_conflict_writes_nothing_else(self):
        p=self.root/'agents/ui_researcher.toml';p.parent.mkdir(parents=True);p.write_text('personal')
        self.assertTrue(self.run_install()['conflicts']);self.assertFalse((self.root/'agents/ui_integrator.toml').exists());self.assertEqual(p.read_text(),'personal')
    def test_identical_unmanaged_is_not_owned(self):
        p=self.root/'agents/ui_researcher.toml';p.parent.mkdir(parents=True);p.write_bytes((self.source/'agents/ui_researcher.toml').read_bytes())
        self.run_install();state,_=mod.receipt(self.root);self.assertNotIn('agents/ui_researcher.toml',state['files'])
        mod.execute(self.root,'uninstall',self.source);self.assertTrue(p.exists())
    def test_upgrade_requires_explicit_option(self):
        self.run_install();self.new_version();self.assertTrue(self.run_install()['conflicts'])
    def test_owned_upgrade_succeeds(self):
        self.run_install();self.new_version();self.assertFalse(self.run_install(upgrade=True)['conflicts'])
        self.assertEqual(mod.receipt(self.root)[0]['version'],'1.20.1')
    def test_modified_owned_not_overwritten(self):
        self.run_install();p=self.root/'agents/ui_researcher.toml';p.write_text('edited locally')
        self.new_version();self.assertTrue(self.run_install(upgrade=True)['conflicts']);self.assertEqual(p.read_text(),'edited locally')
    def test_downgrade_requires_review(self):
        self.run_install();self.new_version('1.19.0')
        with self.assertRaises(mod.InstallError): self.run_install(upgrade=True)
        self.assertFalse(self.run_install(upgrade=True,allow_downgrade=True)['conflicts'])
    def test_downgrade_flag_needs_upgrade(self):
        with self.assertRaises(mod.InstallError): self.run_install(allow_downgrade=True)
    def test_uninstall_preserves_modified(self):
        self.run_install();p=self.root/'agents/ui_researcher.toml';p.write_text('my work')
        r=mod.execute(self.root,'uninstall',self.source)
        self.assertTrue(r['conflicts']);self.assertEqual(p.read_text(),'my work');self.assertFalse((self.root/'agents/ui_integrator.toml').exists())
    def test_uninstall_owned_only(self):
        self.run_install();p=self.root/'agents/custom.toml';p.write_text('other')
        mod.execute(self.root,'uninstall',self.source);self.assertEqual(p.read_text(),'other');self.assertFalse((self.root/mod.RECEIPT).exists())
    def test_uninstall_dry_run(self):
        self.run_install();mod.execute(self.root,'uninstall',self.source,dry_run=True)
        self.assertTrue((self.root/'agents/ui_researcher.toml').is_file())
    def test_uninstall_empty_scope_does_not_create(self):
        self.assertEqual(mod.execute(self.root,'uninstall',self.source)['changed_files'],0);self.assertFalse(self.root.exists())
    def test_missing_owned_file_forgotten(self):
        self.run_install();(self.root/'agents/ui_researcher.toml').unlink()
        self.assertFalse(mod.execute(self.root,'uninstall',self.source)['conflicts'])
    def test_tampered_bundle_rejected(self):
        p=self.source/'agents/ui_researcher.toml';p.write_text('tampered')
        with self.assertRaises(mod.InstallError): self.run_install()
        self.assertFalse(self.root.exists())
    def test_invalid_manifest_rejected(self):
        (self.source/'manifest.json').write_text('{')
        with self.assertRaises(mod.InstallError): self.run_install()
    def test_manifest_role_path_traversal_rejected(self):
        p=self.source/'manifest.json';d=json.loads(p.read_text());d['roles']['ui_researcher']['path']='../outside';p.write_text(json.dumps(d))
        with self.assertRaises(mod.InstallError): self.run_install()
    def test_receipt_traversal_rejected(self):
        self.run_install();p=self.root/mod.RECEIPT;d=json.loads(p.read_text());d['files']['../outside']={'sha256':'0'*64};p.write_text(json.dumps(d))
        with self.assertRaises(mod.InstallError): mod.execute(self.root,'uninstall',self.source)
    def test_bad_receipt_json_rejected(self):
        p=self.root/mod.RECEIPT;p.parent.mkdir(parents=True);p.write_text('{')
        with self.assertRaises(mod.InstallError): self.run_install()
    def test_directory_collision_rejected(self):
        (self.root/'agents/ui_researcher.toml').mkdir(parents=True)
        with self.assertRaises(mod.InstallError): self.run_install()
    def test_symlink_destination_rejected(self):
        self.root.mkdir(parents=True);target=self.base/'other';target.mkdir()
        try:(self.root/'agents').symlink_to(target,target_is_directory=True)
        except OSError:self.skipTest('Symlink privilege unavailable')
        with self.assertRaises(mod.InstallError):self.run_install()
        self.assertEqual(list(target.iterdir()),[])
    def test_symlink_source_rejected(self):
        p=self.source/'agents/ui_researcher.toml';b=p.read_bytes();p.unlink();other=self.base/'external';other.write_bytes(b)
        try:p.symlink_to(other)
        except OSError:self.skipTest('Symlink privilege unavailable')
        with self.assertRaises(mod.InstallError):self.run_install()
    def test_install_lock_respected(self):
        p=self.root/mod.LOCK;p.parent.mkdir(parents=True);p.write_text('other writer')
        with self.assertRaises(mod.InstallError):self.run_install()
        self.assertEqual(p.read_text(),'other writer')
    def test_transaction_rolls_back_operational_failure(self):
        original=mod.atomic;counter=[0]
        def fail_second(path,data):
            counter[0]+=1
            if counter[0]==2:raise OSError('test-only simulated disk failure')
            return original(path,data)
        with patch.object(mod,'atomic',side_effect=fail_second):
            with self.assertRaises(OSError):self.run_install()
        self.assertFalse((self.root/'agents/ui_researcher.toml').exists());self.assertFalse((self.root/mod.RECEIPT).exists());self.assertFalse((self.root/mod.LOCK).exists())
    def test_transaction_checks_before_identity(self):
        p=self.root/'agents/x';p.parent.mkdir(parents=True);p.write_bytes(b'user')
        with self.assertRaises(mod.InstallError):mod.transact(self.root,[('agents/x',b'old',b'new')])
        self.assertEqual(p.read_bytes(),b'user')
    def test_status_reports_modified_and_missing(self):
        self.run_install();(self.root/'agents/ui_researcher.toml').write_text('mine');(self.root/'agents/ui_integrator.toml').unlink()
        states={r['state'] for r in mod.execute(self.root,'status',self.source)['operations']}
        self.assertEqual(states,{'missing','modified_retained','owned_unchanged'})
    def test_existing_config_roundtrip_and_agents_preserved(self):
        try:import tomllib
        except ImportError:self.skipTest('Merging an existing user config requires Python 3.11+')
        self.root.mkdir(parents=True);cfg=self.root/'config.toml';original=b'# user setting\nmodel = "chosen-model"\n[agents]\nenabled = false\nmax_threads = 2\n';cfg.write_bytes(original)
        agent=self.root.parent/'AGENTS.md';agent.write_text('user instructions')
        self.assertFalse(self.run_install()['conflicts'])
        self.assertTrue(cfg.read_bytes().startswith(original))
        parsed=tomllib.loads(cfg.read_text());self.assertEqual(parsed['model'],'chosen-model');self.assertFalse(parsed['agents']['enabled'])
        for role in mod.ROLES:self.assertEqual(parsed['agents'][role]['config_file'],f'agents/{role}.toml')
        self.assertEqual(agent.read_text(),'user instructions')
        mod.execute(self.root,'uninstall',self.source);self.assertEqual(cfg.read_bytes(),original)
    def test_new_config_is_removed_on_uninstall(self):
        self.run_install();self.assertTrue((self.root/'config.toml').is_file())
        mod.execute(self.root,'uninstall',self.source);self.assertFalse((self.root/'config.toml').exists())
    def test_existing_config_user_edits_outside_registration_survive(self):
        try:import tomllib
        except ImportError:self.skipTest('Merging an existing user config requires Python 3.11+')
        self.run_install();cfg=self.root/'config.toml';cfg.write_bytes(b'# new user comment\n'+cfg.read_bytes())
        self.assertFalse(self.run_install()['conflicts'])
        self.assertFalse(mod.execute(self.root,'uninstall',self.source)['conflicts'])
        self.assertEqual(cfg.read_bytes(),b'# new user comment\n')
    def test_modified_registration_prevents_removing_referenced_roles(self):
        self.run_install();cfg=self.root/'config.toml';cfg.write_text(cfg.read_text().replace('agents/ui_researcher.toml','agents/personal.toml'))
        self.assertTrue(mod.execute(self.root,'uninstall',self.source)['conflicts'])
        self.assertEqual(len(list((self.root/'agents').glob('*.toml'))),4)
        self.assertTrue(self.run_install()['conflicts'])
    def test_unmanaged_registration_conflict_writes_no_roles(self):
        self.root.mkdir(parents=True);cfg=self.root/'config.toml';original=b'[agents.ui_researcher]\nconfig_file = "personal.toml"\n';cfg.write_bytes(original)
        self.assertTrue(self.run_install()['conflicts'])
        self.assertEqual(cfg.read_bytes(),original);self.assertFalse((self.root/'agents').exists())
    def test_invalid_config_is_preserved(self):
        self.root.mkdir(parents=True);cfg=self.root/'config.toml';cfg.write_bytes(b'not valid TOML')
        self.assertTrue(self.run_install()['conflicts']);self.assertEqual(cfg.read_bytes(),b'not valid TOML')
        self.assertFalse((self.root/'agents').exists())
    def test_registration_receipt_tampering_rejected(self):
        self.run_install();p=self.root/mod.RECEIPT;d=json.loads(p.read_text());d['registration']['block']='unowned';p.write_text(json.dumps(d))
        with self.assertRaises(mod.InstallError):mod.execute(self.root,'uninstall',self.source)
    def test_legacy_receipt_upgrades_without_overwriting_existing_config(self):
        try:import tomllib
        except ImportError:self.skipTest('Merging an existing user config requires Python 3.11+')
        self.run_install();record,_=mod.receipt(self.root)
        (self.root/mod.RECEIPT).write_bytes(mod._receipt_bytes(record['version'],record['files']))
        original=b'model = "mine"\n';(self.root/'config.toml').write_bytes(original)
        self.assertFalse(self.run_install()['conflicts'])
        self.assertTrue((self.root/'config.toml').read_bytes().startswith(original))
    def test_user_scope_honors_codex_home(self):
        with patch.dict(os.environ,{'CODEX_HOME':str(self.base/'custom home')}):
            self.assertEqual(mod.codex_root(None,True),self.base/'custom home')
    def test_explicit_scope_is_required(self):
        for project,user in [(None,False),('project',True)]:
            with self.subTest(project=project,user=user),self.assertRaises(mod.InstallError):mod.codex_root(project,user)
    def test_all_default_roles_retained_after_repeat(self):
        self.run_install();self.run_install();self.assertEqual(len(list((self.root/'agents').glob('*.toml'))),4)
    def test_invalid_relative_path_rejected(self):
        for rel in ('../a','/tmp/a','a\\b'):
            with self.subTest(rel=rel),self.assertRaises(mod.InstallError):mod.safe(self.root,rel)
    def test_roles_do_not_pin_model_or_permissions(self):
        try:import tomllib
        except ImportError:self.skipTest('TOML parser requires Python 3.11+')
        for name,raw in mod.bundle(self.source)[1].items():
            d=tomllib.loads(raw.decode());self.assertEqual(d['name'],name)
            self.assertEqual(set(d),{'name','description','developer_instructions'})
            self.assertIn('main agent',d['developer_instructions'])
    def test_all_roles_are_valid_toml(self):
        try:import tomllib
        except ImportError:self.skipTest('TOML parser requires Python 3.11+')
        for name,raw in mod.bundle(self.source)[1].items():
            d=tomllib.loads(raw.decode());self.assertTrue(d['description'].strip());self.assertTrue(d['developer_instructions'].strip())
    def test_config_example_parses(self):
        try:import tomllib
        except ImportError:self.skipTest('TOML parser requires Python 3.11+')
        d=tomllib.loads((self.source/'config.example.toml').read_text());self.assertEqual(d['agents']['max_concurrent_threads_per_session'],3)
        self.assertNotIn('default_subagent_model',d['agents'])

if __name__=='__main__':unittest.main()
