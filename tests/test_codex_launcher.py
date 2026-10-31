"""Launcher boundary checks using a local process fixture, not Agent experiments."""
from __future__ import annotations

import importlib.util
import contextlib
import io
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / 'integrations/codex'
spec = importlib.util.spec_from_file_location('ui_spec_codex_launcher', ADAPTER / 'launch.py')
launch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launch)


@unittest.skipIf(launch.tomllib is None, 'Launcher needs the Python 3.11+ TOML parser')
class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # Canonicalize only the test-owned root, including macOS's /var alias.
        # Deliberately supplied project/role symlinks still exercise rejection.
        self.base = Path(self.temp.name).resolve()
        self.project = self.base / 'product with spaces'
        self.project.mkdir()
        self.codex = self.project / '.codex'
        result = launch.install.execute(self.codex, 'install')
        self.assertFalse(result['conflicts'])

    def build(self, args=None):
        return launch.command(str(self.project), False, sys.executable, args or [])

    def snapshot(self):
        return {p.relative_to(self.project).as_posix(): p.read_bytes()
                for p in self.project.rglob('*') if p.is_file()}

    def test_dry_run_prints_only_argv_without_writes_or_starting_codex(self):
        before = self.snapshot()
        prompt = 'Keep spaces, $(), `backticks`, and semicolons; literal.'
        result = subprocess.run([sys.executable, str(ADAPTER / 'launch.py'), '--project', str(self.project),
                                 '--codex-executable', sys.executable, '--dry-run', '--', 'exec',
                                 '--model', 'chosen-model', '--sandbox', 'read-only', '--', prompt],
                                text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        argv = json.loads(result.stdout)
        self.assertIsInstance(argv, list)
        tail = ['exec', '--model', 'chosen-model', '--sandbox', 'read-only', '--', prompt]
        self.assertEqual(argv[-len(tail):], tail)
        self.assertEqual(argv[1:3], ['--enable', 'multi_agent'])
        self.assertIn('agents.enabled=true', argv)
        self.assertEqual(sum('config_file=' in item for item in argv), 4)
        self.assertEqual(self.snapshot(), before)

    def test_native_registration_precedes_subcommand_and_keeps_other_options(self):
        args = ['exec', '-c', 'agents.default_subagent_model="chosen-child"', '-c', 'approval_policy="on-request"', '-']
        argv, cwd = self.build(args)
        self.assertEqual(cwd, self.project)
        self.assertEqual(argv[-len(args):], args)
        prefix = argv[:-len(args)]
        self.assertFalse(any('model=' in item or 'sandbox' in item or 'trust_level' in item for item in prefix))
        for role in launch.install.ROLES:
            self.assertIn(f'agents.{role}.config_file=' + json.dumps(str(self.codex / 'agents' / f'{role}.toml')), prefix)

    def test_role_configuration_overrides_are_rejected_without_mutation(self):
        path = self.codex / 'agents/ui_researcher.toml'
        original = path.read_bytes()
        for setting in ('model = "user-selected-model"', 'model_reasoning_effort = "high"',
                        'sandbox_mode = "danger-full-access"', '[mcp_servers.extra]\ncommand = "other"'):
            raw = original + ('\n' + setting + '\n').encode()
            with self.subTest(setting=setting):
                path.write_bytes(raw)
                with self.assertRaisesRegex(ValueError, 'unsupported configuration keys'):
                    self.build()
                self.assertEqual(path.read_bytes(), raw)

    def test_config_discovery_is_not_required(self):
        (self.codex / 'config.toml').unlink()
        self.assertEqual(sum('config_file=' in arg for arg in self.build()[0]), 4)
        self.assertFalse((self.codex / 'config.toml').exists())

    def test_missing_role_and_missing_project_are_rejected_without_creation(self):
        (self.codex / 'agents/ui_challenger.toml').unlink()
        with self.assertRaisesRegex(ValueError, 'missing'):
            self.build()
        absent = self.base / 'not-created'
        with self.assertRaisesRegex(ValueError, 'does not exist'):
            launch.command(str(absent), False, sys.executable, [])
        self.assertFalse(absent.exists())

    def test_invalid_toml_identity_and_required_fields_are_rejected(self):
        path = self.codex / 'agents/ui_integrator.toml'
        bad = ['invalid = [', 'name="another_role"\ndescription="d"\ndeveloper_instructions="i"',
               'name="ui_integrator"\ndescription=""\ndeveloper_instructions="i"',
               'name="ui_integrator"\ndescription="d"']
        for content in bad:
            with self.subTest(content=content):
                path.write_text(content)
                with self.assertRaises(ValueError):
                    self.build()

    def test_symlink_role_and_symlink_project_are_rejected(self):
        path = self.codex / 'agents/ui_researcher.toml'
        outside = self.base / 'outside.toml'
        outside.write_bytes(path.read_bytes())
        path.unlink()
        try:
            path.symlink_to(outside)
        except OSError:
            self.skipTest('Symlink creation unavailable')
        with self.assertRaisesRegex(ValueError, 'link'):
            self.build()
        path.unlink()
        path.write_bytes(outside.read_bytes())
        linked = self.base / 'linked-project'
        linked.symlink_to(self.project, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'link'):
            launch.command(str(linked), False, sys.executable, [])

    def test_parent_traversal_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unsafe'):
            launch.command(str(self.project / '..' / self.project.name), False, sys.executable, [])

    def test_role_overrides_are_rejected_in_all_cli_config_forms(self):
        attempts = [
            ['-c', 'agents.ui_researcher.config_file="other.toml"'],
            ['--config', 'agents."ui_integrator".model="other"'],
            ['--config=agents.ui_challenger={description="other"}'],
            ['-cagents.ui_experience_observer.description="other"'],
            ['-c=agents.ui_researcher.model="other"'],
            ['-c', 'agents = {max_threads=1}'],
            ['-c', '"agents" . "ui_researcher" . description = "other"'],
        ]
        for args in attempts:
            with self.subTest(args=args), self.assertRaisesRegex(ValueError, 'conflict'):
                self.build(['exec'] + args)

    def test_working_directory_and_multi_agent_conflicts_are_rejected(self):
        attempts = [['-C', '/elsewhere'], ['--cd=/elsewhere'], ['-C/elsewhere'],
                    ['--disable', 'multi_agent'], ['--disable=multi_agent'],
                    ['-c', 'agents.enabled=false'], ['-c', 'features.multi_agent=false'],
                    ['-c', 'features={multi_agent=false}']]
        for args in attempts:
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.build(args)

    def test_native_option_terminator_preserves_literal_prompt(self):
        args = ['exec', '--', '--config=agents.ui_researcher.model=literal', '-C', 'literal']
        self.assertEqual(self.build(args)[0][-len(args):], args)

    def test_unrelated_role_and_native_model_settings_remain_available(self):
        args = ['-c', 'agents.other_role.description="other"', '-c', 'agents.enabled=true',
                '-c', 'features.apps=false', '--disable', 'memories', '-m', 'chosen-model']
        self.assertEqual(self.build(args)[0][-len(args):], args)

    def test_user_scope_keeps_current_working_directory_and_environment(self):
        environment = dict(os.environ)
        with patch.object(launch.install, 'codex_root', return_value=self.codex) as scope:
            argv, cwd = launch.command(None, True, sys.executable, [])
        scope.assert_called_once_with(None, True)
        self.assertEqual(cwd, Path.cwd())
        self.assertEqual(dict(os.environ), environment)
        self.assertEqual(sum('config_file=' in arg for arg in argv), 4)

    def test_missing_executable_fails_clearly(self):
        with self.assertRaisesRegex(ValueError, 'not found'):
            launch.command(str(self.project), False, str(self.base / 'missing-codex'), [])

    @unittest.skipUnless(os.name == 'posix', 'Executable process fixture uses a POSIX shebang')
    def test_real_process_preserves_arguments_stdin_cwd_and_exit_status(self):
        fake = self.base / 'fixture codex'
        fake.write_text(f'#!{sys.executable}\nimport json,os,sys\nprint(json.dumps({{"args":sys.argv[1:],"cwd":os.getcwd(),"stdin":sys.stdin.read()}}))\nsys.exit(7)\n')
        fake.chmod(0o755)
        prompt = 'literal `touch never-created` $(touch never-created);'
        result = subprocess.run([sys.executable, str(ADAPTER / 'launch.py'), '--project', str(self.project),
                                 '--codex-executable', str(fake), '--', 'exec', '--', prompt],
                                input='input preserved\n', text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 7, result.stderr)
        observed = json.loads(result.stdout)
        self.assertEqual(observed['cwd'], str(self.project))
        self.assertEqual(observed['stdin'], 'input preserved\n')
        self.assertEqual(observed['args'][-3:], ['exec', '--', prompt])
        self.assertFalse((self.project / 'never-created').exists())

    @unittest.skipUnless(os.name == 'posix', 'Foreground process-group signal check is POSIX-specific')
    def test_ctrl_c_reaches_child_and_retains_its_exit_status(self):
        fake = self.base / 'interrupt-fixture'
        fake.write_text(f'#!{sys.executable}\nimport signal,sys\nsignal.signal(signal.SIGINT,lambda *_:sys.exit(42))\nprint("READY",flush=True)\nsignal.pause()\n')
        fake.chmod(0o755)
        proc = subprocess.Popen([sys.executable, str(ADAPTER / 'launch.py'), '--project', str(self.project),
                                 '--codex-executable', str(fake)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True)
        try:
            self.assertTrue(select.select([proc.stdout], [], [], 8)[0], 'Child did not become ready')
            self.assertEqual(proc.stdout.readline().strip(), 'READY')
            os.killpg(proc.pid, signal.SIGINT)
            proc.communicate(timeout=8)
            self.assertEqual(proc.returncode, 42)
        finally:
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.communicate()


class ParserAvailabilityTests(unittest.TestCase):
    def test_missing_parser_is_rejected_without_writes_or_process_start(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / 'not-created'
            errors = io.StringIO()
            with patch.object(launch, 'tomllib', None), patch.object(launch.subprocess, 'Popen') as process, \
                    contextlib.redirect_stderr(errors):
                code = launch.main(['--project', str(project), '--codex-executable', sys.executable, '--dry-run'])
            self.assertEqual(code, 2)
            self.assertIn('Python 3.11+', errors.getvalue())
            process.assert_not_called()
            self.assertFalse(project.exists())


if __name__ == '__main__':
    unittest.main()
