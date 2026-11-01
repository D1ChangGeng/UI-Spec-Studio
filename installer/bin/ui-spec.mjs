#!/usr/bin/env node
// Self-contained distribution installer: never clones or downloads a source repository.
import { readFile, writeFile, readdir, mkdir, mkdtemp, rename, rm, lstat, open } from 'node:fs/promises';
import { createHash, randomUUID } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { homedir } from 'node:os';
import { dirname, join, resolve, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createPresentation } from '../lib/experience.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const payload = join(root, 'payload');
const receiptFile = '.ui-spec-install.json';
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const usage = 'UI Spec Studio — lightweight Skill and Harness installer\n'
  + 'Usage: ui-spec install|status|uninstall [--agent HOST] [--project PATH|--global]\n'
  + '  install: --upgrade | --migrate | --adopt | --dry-run | --no-tui | --yes\n'
  + '  all commands: --lang en|zh | --json | --no-tui\n'
  + 'Existing unmanaged installations require interactive consent or explicit --migrate.\n';

function fail(message) { throw new Error(message); }
function parse(argv) {
  const action = argv.shift();
  if (!action || ['--help', '-h', 'help'].includes(action)) return { action: 'help' };
  if (!['install', 'status', 'uninstall'].includes(action)) fail(`Unknown action: ${action}`);
  const out = { action, agent: null, project: null, global: false, upgrade: false, migrate: false, adopt: false, yes: false, noTui: false, json: false, lang: null, dryRun: false };
  const once = new Set();
  while (argv.length) {
    const arg = argv.shift();
    if (once.has(arg)) fail(`Repeated flag: ${arg}`);
    once.add(arg);
    if (arg === '--agent') out.agent = argv.shift() || fail('Missing --agent value');
    else if (arg === '--project') out.project = argv.shift() || fail('Missing --project value');
    else if (arg === '--global') out.global = true;
    else if (arg === '--upgrade') out.upgrade = true;
    else if (arg === '--migrate') out.migrate = true;
    else if (arg === '--adopt') out.adopt = true;
    else if (arg === '--yes') out.yes = true;
    else if (arg === '--no-tui') out.noTui = true;
    else if (arg === '--json') out.json = true;
    else if (arg === '--lang') out.lang = argv.shift() || fail('Missing --lang value');
    else if (arg === '--dry-run') out.dryRun = true;
    else fail(`Unknown option: ${arg}`);
  }
  if (out.lang && !['zh', 'en', 'zh-CN', 'en-US'].includes(out.lang)) fail('Use --lang en or --lang zh');
  if (out.migrate && out.adopt) fail('--migrate and --adopt are mutually exclusive');
  if ((out.migrate || out.adopt || out.upgrade || out.yes) && action !== 'install') fail('Install-only option used with ' + action);
  if (out.project && out.global) fail('--project and --global are mutually exclusive');
  if (out.json) out.noTui = true;
  return out;
}
function safeRelative(p) {
  if (typeof p !== 'string' || !p || p.includes('\\') || isAbsolute(p) || p.split('/').some((x) => !x || x === '.' || x === '..')) fail(`Unsafe bundle path: ${p}`);
  return p;
}
async function regular(path) {
  try { const st = await lstat(path); if (!st.isFile() || st.isSymbolicLink()) fail(`Refusing non-regular file: ${path}`); return await readFile(path); }
  catch (e) { if (e.code === 'ENOENT') return null; throw e; }
}
async function assertSafeDestination(path, boundary, allowLeafLink = false) {
  const abs = resolve(path);
  const guard = resolve(boundary);
  if (abs !== guard && !abs.startsWith(guard + (process.platform === 'win32' ? '\\' : '/')))
    fail('Skill path must stay inside the explicitly selected Harness scope');
  let current = abs;
  // Check the user-selected project/Harness root and every child path, but not
  // the operating system ancestors. macOS /var -> /private/var is a normal,
  // trusted system path alias, not a project-installed Skill symlink.
  while (true) {
    try {
      const st = await lstat(current);
      if (st.isSymbolicLink()) {
        if (!(allowLeafLink && current === abs)) fail('Refusing linked destination ancestor: ' + current);
      } else if (!st.isDirectory()) fail('Refusing non-directory Skill destination: ' + current);
    } catch (e) { if (e.code !== 'ENOENT') throw e; }
    if (current === guard) break;
    current = dirname(current);
  }
}
async function listFiles(base, sub = '') {
  const result = [];
  for (const ent of await readdir(join(base, sub), { withFileTypes: true })) {
    const rel = sub ? `${sub}/${ent.name}` : ent.name;
    if (ent.isDirectory()) result.push(...await listFiles(base, rel));
    else if (ent.isFile()) result.push(rel);
    else fail(`Refusing linked or unusual file: ${join(base, rel)}`);
  }
  return result.sort();
}
async function verifyBundle() {
  const registry = JSON.parse((await readFile(join(root, 'harnesses.json'))).toString());
  const manifest = JSON.parse((await readFile(join(payload, 'manifest.json'))).toString());
  if (registry.schema_version !== 1 || manifest.schema_version !== 1 || !manifest.files || !Object.keys(registry.harnesses || {}).length) fail('Invalid distribution manifest');
  const declared = Object.keys(manifest.files).sort();
  const actual = (await listFiles(payload)).filter((x) => x !== 'manifest.json');
  if (JSON.stringify(declared) !== JSON.stringify(actual)) fail('Distribution contains unexpected or missing files');
  for (const rel of declared) {
    safeRelative(rel);
    if (!/^[a-f0-9]{64}$/.test(manifest.files[rel]) || sha(await readFile(join(payload, ...rel.split('/')))) !== manifest.files[rel]) fail(`Invalid distribution content: ${rel}`);
  }
  return { registry, manifest };
}
async function inspectTarget(target, versionFiles) {
  const old = await regular(join(target, receiptFile));
  const exists = await lstat(target).then(() => true, (e) => { if (e.code === 'ENOENT') return false; throw e; });
  if (!exists) return { exists: false, clean: false, identical: false };
  if (!old) fail(`Existing unowned Skill directory; refusing to overwrite: ${target}`);
  let receipt;
  try { receipt = JSON.parse(old.toString('utf8')); } catch { fail('Unreadable installation receipt'); }
  if (receipt.schema_version !== 1 || !receipt.files || typeof receipt.version !== 'string') fail('Unknown installation receipt');
  const recorded = Object.keys(receipt.files).sort();
  const actual = (await listFiles(target)).filter((x) => x !== receiptFile).sort();
  if (JSON.stringify(recorded) !== JSON.stringify(actual)) fail('Existing Skill has untracked or missing files; no changes made');
  for (const rel of recorded) {
    safeRelative(rel);
    if (!/^[a-f0-9]{64}$/.test(receipt.files[rel]) || sha(await readFile(join(target, ...rel.split('/')))) !== receipt.files[rel]) fail(`Existing Skill was modified: ${rel}`);
  }
  return { exists: true, clean: true, identical: receipt.version === versionFiles.version && JSON.stringify(receipt.files) === JSON.stringify(versionFiles.files), version: receipt.version };
}
function findPython() {
  for (const cmd of (process.platform === 'win32' ? ['py', 'python', 'python3'] : ['python3', 'python'])) {
    const prefix = cmd === 'py' ? ['-3'] : [];
    const test = spawnSync(cmd, [...prefix, '-c', 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)'], { encoding: 'utf8' });
    if (test.status === 0) return { cmd, prefix };
  }
  fail('Codex adapter requires Python 3.11+; no files changed');
}
function runAdapter(config, action, options, preflight = false) {
  if (!config.adapter) return;
  const entry = safeRelative(config.adapter.entry);
  if (!entry.startsWith('adapters/')) fail('Invalid adapter entry');
  const flags = options.global ? ['--user'] : ['--project', options.projectRoot];
  const runtime = config.adapter.runtime === 'python'
    ? findPython()
    : config.adapter.runtime === 'node'
      ? { cmd: process.execPath, prefix: [] }
      : fail(`Unsupported adapter runtime: ${config.adapter.runtime}`);
  const args = [...runtime.prefix, join(payload, ...entry.split('/')), action, ...flags];
  if (action === 'install' && options.upgrade) args.push('--upgrade');
  if (preflight) args.push('--dry-run');
  const result = spawnSync(runtime.cmd, args, { encoding: 'utf8', maxBuffer: 1024 * 1024 * 5 });
  if (result.status !== 0) fail(`Harness adapter ${action} failed (no Skill changes retained):\n${result.stderr || result.stdout || result.error}`);
  if (!preflight) process.stdout.write(result.stdout);
}
function skillDirectory(spec, options) {
  const home = homedir();
  if (!options.global) return { target: resolve(options.projectRoot, ...safeRelative(spec.project_skill_dir).split('/')), boundary: options.projectRoot };
  let base;
  if (spec.user_base === 'home') base = home;
  else if (spec.user_base === 'xdg-config') base = process.env.XDG_CONFIG_HOME || (process.platform === 'win32' && process.env.APPDATA) || join(home, '.config');
  else if (spec.user_base === 'env-fallback' && spec.user_env && spec.user_fallback)
    base = process.env[spec.user_env] || join(home, safeRelative(spec.user_fallback));
  else fail('Invalid Harness user-scope configuration');
  return { target: resolve(base, ...safeRelative(spec.user_skill_dir).split('/')), boundary: base };
}
async function main() {
  const options = parse(process.argv.slice(2));
  if (options.action === 'help') { process.stdout.write(usage); return; }
  options.projectRoot = resolve(options.project || process.cwd());
  const { registry, manifest } = await verifyBundle();
  const spec = registry.harnesses[options.agent];
  if (!spec) fail(`Unsupported Harness: ${options.agent}; supported: ${Object.keys(registry.harnesses).join(', ')}`);
  const { target, boundary } = skillDirectory(spec, options);
  await assertSafeDestination(target, boundary);
  const files = Object.fromEntries(Object.entries(manifest.files).filter(([p]) => p.startsWith('skill/')).map(([p, hash]) => [p.slice(6), hash]));
  const installed = await inspectTarget(target, { version: manifest.version, files });
  const plan = { action: options.action, version: manifest.version, agent: options.agent, scope: options.global ? 'user' : 'project', skill: target, skill_files: Object.keys(files).length, adapter: spec.adapter?.entry || null, previously_installed: installed.exists };
  if (options.action === 'status') { process.stdout.write(JSON.stringify({ ...plan, status: installed.exists ? (installed.identical ? 'current' : 'outdated') : 'absent' }, null, 2) + '\n'); return; }
  if (options.action === 'install' && installed.exists && !installed.identical && !options.upgrade) fail('A different managed Skill is installed; retry explicitly with --upgrade');
  if (options.dryRun) { if (options.action === 'install') runAdapter(spec, 'install', options, true); process.stdout.write(JSON.stringify({ ...plan, dry_run: true }, null, 2) + '\n'); return; }
  if (options.action === 'uninstall') {
    // A separately installed native adapter is not owned by this Skill receipt.
    // An absent managed Skill must never remove its native Harness registrations.
    if (!installed.exists) {
      process.stdout.write(JSON.stringify({ ...plan, result: 'not-installed' }, null, 2) + '\n'); return;
    }
    if (spec.adapter) runAdapter(spec, 'uninstall', options);
    await rm(target, { recursive: true });
    process.stdout.write(JSON.stringify({ ...plan, result: 'uninstalled' }, null, 2) + '\n'); return;
  }
  runAdapter(spec, 'install', options, true);
  if (installed.identical) {
    if (spec.adapter) runAdapter(spec, 'install', options);
    process.stdout.write(JSON.stringify({ ...plan, result: 'already-current' }, null, 2) + '\n'); return;
  }
  await mkdir(dirname(target), { recursive: true });
  const staging = await mkdtemp(join(dirname(target), '.ui-spec-stage-'));
  let backup = null;
  let swapped = false;
  try {
    for (const rel of Object.keys(files)) {
      safeRelative(rel);
      const dst = join(staging, ...rel.split('/'));
      await mkdir(dirname(dst), { recursive: true });
      await writeFile(dst, await readFile(join(payload, 'skill', ...rel.split('/'))));
    }
    await writeFile(join(staging, receiptFile), JSON.stringify({ schema_version: 1, version: manifest.version, files }, null, 2) + '\n');
    if (installed.exists) {
      backup = join(dirname(target), `.ui-spec-backup-${process.pid}-${Date.now()}`);
      await rename(target, backup);
    }
    await rename(staging, target);
    swapped = true;
    if (spec.adapter) runAdapter(spec, 'install', options);
    if (backup) await rm(backup, { recursive: true });
    process.stdout.write(JSON.stringify({ ...plan, result: installed.exists ? 'upgraded' : 'installed' }, null, 2) + '\n');
  } catch (err) {
    if (swapped) await rm(target, { recursive: true, force: true });
    if (backup) await rename(backup, target);
    throw err;
  } finally { await rm(staging, { recursive: true, force: true }); }
}
main().catch((err) => { console.error(`ui-spec: ${err.message}`); process.exitCode = 1; });
