#!/usr/bin/env node
// Self-contained distribution installer: never clones or downloads a source repository.
import { readFile, writeFile, readdir, mkdir, mkdtemp, rename, rm, rmdir, lstat, readlink, open } from 'node:fs/promises';
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
function helpText(lang) {
  const chinese = (lang || Intl.DateTimeFormat().resolvedOptions().locale).toLowerCase().startsWith('zh');
  return (chinese ? [
    'UI Spec Studio',
    '安装：npx --yes ui-spec-studio@latest',
    '',
    '用法：ui-spec install|status|uninstall [选项]',
    '  --agent TOOL       Codex、Claude Code、Cursor 或 OpenCode',
    '  --project PATH     安装到指定项目（默认当前项目）',
    '  --global           安装到当前用户的所有项目',
    '  --migrate          备份并替换旧安装',
    '  --upgrade          更新由本安装器安装的版本',
    '  --adopt            保留并使用一致的现有文件',
    '  --dry-run          仅预览，不修改文件',
    '  --lang en|zh       选择语言',
    '  --no-tui | --json  非交互模式',
  ] : [
    'UI Spec Studio',
    'Install: npx --yes ui-spec-studio@latest',
    '',
    'Usage: ui-spec install|status|uninstall [options]',
    '  --agent TOOL       Codex, Claude Code, Cursor or OpenCode',
    '  --project PATH     Install into a project (default: current project)',
    '  --global           Install for all projects of this user',
    '  --migrate          Back up and replace an existing installation',
    '  --upgrade          Update a version installed by this tool',
    '  --adopt            Keep and use identical existing files',
    '  --dry-run          Preview without changing files',
    '  --lang en|zh       Choose a language',
    '  --no-tui | --json  Non-interactive output',
  ]).join('\n') + '\n';
}

function fail(message) { throw new Error(message); }
function parse(argv) {
  const helpLanguage = (() => {
    const index = argv.indexOf('--lang');
    return index >= 0 ? argv[index + 1] : null;
  })();
  const first = argv.shift();
  const action = (!first || (first.startsWith('-') && !['-h', '--help', '--version', '-V'].includes(first)))
    ? 'install' : first;
  if (first?.startsWith('-') && action === 'install') argv.unshift(first);
  if (['--help', '-h', 'help'].includes(action) || argv.includes('--help') || argv.includes('-h'))
    return { action: 'help', lang: helpLanguage };
  if (['--version', '-V', 'version'].includes(action)) return { action: 'version' };
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
async function isLinked(path, stat) {
  if (stat.isSymbolicLink()) return true;
  // Some Windows filesystem providers report junctions as directories from
  // lstat even though readlink still identifies their reparse-point target.
  if (process.platform === 'win32' && stat.isDirectory()) {
    try { await readlink(path); return true; }
    catch (e) {
      if (['EINVAL', 'UNKNOWN', 'ENOTSUP', 'EACCES'].includes(e.code)) return false;
      if (e.code === 'ENOENT') throw e;
      throw e;
    }
  }
  return false;
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
      if (await isLinked(current, st)) {
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
    if (await isLinked(join(base, rel), await lstat(join(base, rel)))) fail('Refusing linked or unusual file: ' + rel);
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
function legacyVersion(content) {
  const body = content.toString('utf8');
  const header = /^---\r?\n([\s\S]*?)\r?\n---/m.exec(body)?.[1] || '';
  if (!/^name:\s*ui-spec\s*$/m.test(header)) fail('Existing directory is not a recognizable ui-spec Skill; refusing to replace it');
  return /^\s*version:\s*["']?(\d+\.\d+\.\d+)/m.exec(header)?.[1] || null;
}
function backupLocation(target, backupName) {
  if (!/^ui-spec-\d{8}T\d{6}Z-[a-f0-9]{8}$/.test(backupName)) fail('Invalid backup identity in the installation receipt');
  return join(dirname(dirname(target)), 'ui-spec-studio', 'backups', backupName);
}
async function inspectTarget(target, next) {
  let stat;
  try { stat = await lstat(target); }
  catch (e) { if (e.code === 'ENOENT') return { exists: false, kind: 'absent', identical: false }; throw e; }
  if (await isLinked(target, stat)) return { exists: true, kind: 'legacy-link', identical: false, version: null };
  if (!stat.isDirectory()) fail('Existing Skill path is not a directory or link: ' + target);
  const old = await regular(join(target, receiptFile));
  if (!old) {
    const entry = await regular(join(target, 'SKILL.md'));
    if (!entry) fail('Existing directory has no regular SKILL.md; no changes made: ' + target);
    const version = legacyVersion(entry);
    let identical = false;
    try {
      const actual = await listFiles(target);
      const expected = Object.keys(next.files).sort();
      if (JSON.stringify(actual) === JSON.stringify(expected)) {
        identical = true;
        for (const name of expected) {
          const observed = await regular(join(target, ...name.split('/')));
          if (!observed || sha(observed) !== next.files[name]) { identical = false; break; }
        }
      }
    } catch (e) {
      if (!/Refusing linked or unusual file/.test(String(e.message))) throw e;
    }
    return { exists: true, kind: 'legacy', identical, version };
  }
  let receipt;
  try { receipt = JSON.parse(old.toString('utf8')); } catch { fail('Unreadable managed receipt; preserve the directory for inspection'); }
  if (![1, 2].includes(receipt.schema_version) || !receipt.files || typeof receipt.version !== 'string')
    fail('Unrecognized managed installation receipt; no changes made');
  const recorded = Object.keys(receipt.files).sort();
  const actual = (await listFiles(target)).filter(name => name !== receiptFile).sort();
  if (JSON.stringify(recorded) !== JSON.stringify(actual)) fail('Managed Skill has added or missing files; no changes made');
  for (const rel of recorded) {
    safeRelative(rel);
    const hash = receipt.files[rel];
    if (!/^[a-f0-9]{64}$/.test(hash) || sha(await readFile(join(target, ...rel.split('/')))) !== hash)
      fail('Managed Skill contains a modified file: ' + rel);
  }
  if (receipt.migration) backupLocation(target, receipt.migration.backupName);
  return {
    exists: true, kind: 'managed', version: receipt.version,
    identical: receipt.version === next.version && JSON.stringify(receipt.files) === JSON.stringify(next.files),
    migration: receipt.migration || null, adopted: receipt.adopted === true,
  };
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
  if (preflight) return;
  try { return JSON.parse(result.stdout); } catch { return { output: result.stdout.trim() }; }
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
function receiptBytes(version, files, extra = {}) {
  return JSON.stringify({ schema_version: 2, version, files, ...extra }, null, 2) + '\n';
}
async function exists(path) {
  try { return await lstat(path); } catch (e) { if (e.code === 'ENOENT') return null; throw e; }
}
async function exclusive(target, fn) {
  const parent = dirname(target);
  await mkdir(parent, { recursive: true });
  const lockName = join(parent, '.ui-spec-install.lock');
  let file;
  try { file = await open(lockName, 'wx', 0o600); }
  catch (e) {
    if (e.code === 'EEXIST') fail('Another installation may be running. Inspect the lock file: ' + lockName);
    throw e;
  }
  try { await file.writeFile(String(process.pid) + '\n'); return await fn(); }
  finally { await file.close(); await rm(lockName, { force: true }); }
}
async function safeBackup(target, boundary) {
  const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '').replace('.000','');
  const backupName = 'ui-spec-' + stamp + '-' + randomUUID().replace(/-/g, '').slice(0, 8);
  const destination = backupLocation(target, backupName);
  await assertSafeDestination(dirname(destination), boundary);
  await mkdir(dirname(destination), { recursive: true });
  if (await exists(destination)) fail('Backup location already exists: ' + destination);
  return { backupName, destination };
}
async function stageSkill(target, files, receipt, onFile = () => {}) {
  const staging = await mkdtemp(join(dirname(target), '.ui-spec-stage-'));
  try {
    for (const rel of Object.keys(files)) {
      safeRelative(rel);
      const dest = join(staging, ...rel.split('/'));
      await mkdir(dirname(dest), { recursive: true });
      await writeFile(dest, await readFile(join(payload, 'skill', ...rel.split('/'))));
      if (sha(await readFile(dest)) !== files[rel]) fail('Staged file failed SHA-256 verification: ' + rel);
      onFile(rel);
    }
    await writeFile(join(staging, receiptFile), receiptBytes(receipt.version, files, receipt.extra));
    return staging;
  } catch (err) {
    await rm(staging, { recursive: true, force: true });
    throw err;
  }
}
function show(ui, options, result, heading) {
  if (!ui.active || options.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    ui.summary([
      ui.tr('Harness', '宿主') + ': ' + result.agent,
      ui.tr('Scope', '范围') + ': ' + result.scope,
      ui.tr('Skill files', 'Skill 文件') + ': ' + result.skill_files,
      ui.tr('Destination', '目标目录') + ': ' + result.skill,
      ...(result.status ? [ui.tr('Status', '状态') + ': ' + result.status] : []),
      ...(result.installed_version ? [ui.tr('Installed version', '已安装版本') + ': ' + result.installed_version] : []),
      ...(result.backup ? [ui.tr('Saved original', '原安装备份') + ': ' + result.backup] : []),
    ].join('\n'), heading);
    const unchanged = ['cancelled', 'not-installed', 'unmanaged-preserved', 'status'].includes(result.result);
    ui.end(unchanged ? ui.tr('No changes made', '未作修改') : ui.tr('Ready — restart your coding agent if necessary', '安装完成；如有需要请重新启动编码 Agent'));
  }
}
let currentPresentation = null;
async function main() {
  const options = parse(process.argv.slice(2));
  if (options.action === 'help') { process.stdout.write(helpText(options.lang)); return; }
  if (options.action === 'version') {
    const pkg = JSON.parse((await readFile(join(root, 'package.json'))).toString());
    console.log(pkg.name + ' ' + pkg.version);
    return;
  }
  options.projectRoot = resolve(options.project || process.cwd());
  const pkg = JSON.parse((await readFile(join(root, 'package.json'))).toString());
  const ui = await createPresentation({ ...options, version: pkg.version });
  currentPresentation = ui;
  ui.intro();
  const { registry, manifest } = await ui.step(
    ui.tr('Checking release integrity', '校验正式分发包'),
    verifyBundle,
    ui.tr('Release verified', '安装包校验通过')
  );
  if (!options.agent) {
    options.agent = await ui.chooseAgent(Object.keys(registry.harnesses));
    if (!options.agent) return;
  }
  if (options.action === 'install' && !options.project && !options.global) {
    const choice = await ui.chooseScope(options.projectRoot, resolve(homedir()));
    if (choice === 'cancel') return;
    if (choice === 'user') options.global = true;
  }
  const spec = registry.harnesses[options.agent];
  if (!spec) fail('Unsupported Harness: ' + options.agent + '; choose ' + Object.keys(registry.harnesses).join(', '));
  const { target, boundary } = skillDirectory(spec, options);
  await assertSafeDestination(target, boundary, true);
  const files = Object.fromEntries(
    Object.entries(manifest.files).filter(([name]) => name.startsWith('skill/'))
      .map(([name, hash]) => [name.slice(6), hash])
  );
  const installed = await ui.step(
    ui.tr('Inspecting Harness and existing Skill', '检查宿主与现有 Skill'),
    () => inspectTarget(target, { version: manifest.version, files }),
    ui.tr('Environment inspected', '环境检查完成')
  );
  const plan = {
    action: options.action, version: manifest.version, agent: options.agent,
    scope: options.global ? 'user' : 'project', skill: target, skill_files: Object.keys(files).length,
    adapter: spec.adapter?.entry || null, previously_installed: installed.exists,
  };
  ui.info(ui.tr('npm has already downloaded the compact release package; no repository clone is used.',
    'npm 已下载轻量发布包；不会克隆源码仓库。'));
  if (!options.global && options.projectRoot === resolve(homedir())) ui.warning(
    ui.tr('Current directory is your home folder; this is a project-scoped install. Use --global for user scope.',
      '当前目录是用户主目录；本次属于项目级安装。如需用户级安装请使用 --global。'));
  ui.summary([
    ui.tr('Harness', '宿主') + ': ' + options.agent,
    ui.tr('Scope', '范围') + ': ' + plan.scope,
    ui.tr('Target', '目标') + ': ' + target,
    ui.tr('Runtime files', '运行时文件') + ': ' + Object.keys(files).length,
    ui.tr('Native adapter', '原生适配器') + ': ' + (spec.adapter ? 'Codex / ' + spec.adapter.runtime : ui.tr('not needed', '无需安装')),
  ].join('\n'));
  if (options.action === 'status') {
    const status = !installed.exists ? 'absent' : installed.kind === 'managed'
      ? (installed.identical ? 'current' : 'outdated') : installed.kind;
    show(ui, options, { ...plan, status, installed_version: installed.version || null, result: 'status' }, ui.tr('Installation status', '安装状态'));
    return;
  }
  if (options.action === 'uninstall' && installed.kind !== 'managed') {
    show(ui, options, { ...plan, result: installed.exists ? 'unmanaged-preserved' : 'not-installed' }, ui.tr('No managed Skill removed', '没有删除未托管 Skill'));
    return;
  }
  let decision = 'install';
  if (options.action === 'install' && installed.kind !== 'managed' && installed.exists) {
    if (options.adopt) {
      if (!installed.identical || installed.kind !== 'legacy') fail('--adopt requires an unmodified byte-identical legacy Skill; use --migrate for other installations');
      decision = 'adopt';
    } else if (options.migrate) {
      decision = 'migrate';
    } else if (options.dryRun) {
      decision = 'migration-required';
    } else {
      decision = await ui.resolveExisting({ ...installed, path: target });
      if (decision === null) fail('An existing Skill was found. Use --migrate to back it up before replacement, or --adopt for identical files.');
    }
  } else if (options.action === 'install' && installed.kind === 'managed' && !installed.identical) {
    if (options.upgrade) decision = 'upgrade';
    else if (options.dryRun) decision = 'upgrade-required';
    else {
      decision = await ui.resolveUpgrade(installed.version);
      if (decision === null) fail('Existing managed version ' + installed.version + ': use --upgrade to update.');
    }
  }
  if (decision === 'upgrade') options.upgrade = true;
  if (decision === 'keep') {
    show(ui, options, { ...plan, result: 'cancelled' }, ui.tr('Existing installation preserved', '保留旧安装'));
    return;
  }
  if (options.dryRun) {
    if (options.action === 'install') {
      await ui.step(ui.tr('Checking native adapter plan', '预检原生适配器'),
        () => runAdapter(spec, 'install', options, true), ui.tr('Preflight complete', '预检完成'));
    }
    const result = { ...plan, dry_run: true, decision, installed_version: installed.version || null };
    if (!ui.active || options.json) console.log(JSON.stringify(result, null, 2));
    else {
      ui.summary([
        ui.tr('Action', '操作') + ': ' + result.action,
        ui.tr('Strategy', '执行策略') + ': ' + decision,
        ui.tr('Harness', '宿主') + ': ' + result.agent,
        ui.tr('Target', '目标目录') + ': ' + result.skill,
        ui.tr('Runtime files', '运行时文件') + ': ' + result.skill_files,
      ].join('\n'), ui.tr('Dry run — no files written', '预览：未写入任何文件'));
      ui.end(ui.tr('No changes', '未作修改'));
    }
    return;
  }
  if (options.action === 'install') await ui.step(
    ui.tr('Checking native Harness adapter', '检查宿主原生适配器'),
    () => runAdapter(spec, 'install', options, true), ui.tr('Adapter ready', '适配器就绪')
  );
  const outcome = await exclusive(target, async () => {
    // Refresh managed and legacy identity inside the lock.
    const current = await inspectTarget(target, { version: manifest.version, files });
    if (current.kind !== installed.kind || current.version !== installed.version || current.identical !== installed.identical)
      fail('Installation changed during preparation; no changes made, please retry');
    if (options.action === 'uninstall') {
      let recovered = null;
      if (current.migration) {
        recovered = backupLocation(target, current.migration.backupName);
        await assertSafeDestination(dirname(recovered), boundary);
        if (!await exists(recovered)) fail('Original backup is missing; refusing uninstall: ' + recovered);
      }
      await ui.step(ui.tr('Removing native Harness registration', '卸载宿主原生配置'),
        () => runAdapter(spec, 'uninstall', options), ui.tr('Native registration handled', '原生配置已处理'));
      if (current.adopted) {
        await rm(join(target, receiptFile));
        return { ...plan, result: 'adopted-copy-preserved' };
      }
      if (recovered) {
        const holding = join(dirname(target), '.ui-spec-remove-' + randomUUID().slice(0, 8));
        await rename(target, holding);
        try { await rename(recovered, target); }
        catch (err) { await rename(holding, target); throw err; }
        await rm(holding, { recursive: true });
        // Remove only empty installer-created backup directories.
        try { await rmdir(dirname(recovered)); await rmdir(dirname(dirname(recovered))); }
        catch (e) { if (!['ENOTEMPTY', 'EEXIST', 'ENOENT'].includes(e.code)) throw e; }
        return { ...plan, result: 'original-restored', backup: target };
      }
      await rm(target, { recursive: true });
      return { ...plan, result: 'uninstalled' };
    }
    if (decision === 'migration-required' || decision === 'upgrade-required')
      fail('Explicit migration or upgrade required');
    if (current.kind === 'managed' && current.identical) {
      await ui.step(ui.tr('Checking installed Harness roles', '检查已安装的宿主角色'),
        () => runAdapter(spec, 'install', options), ui.tr('Already current', '当前版本已就绪'));
      return { ...plan, result: 'already-current' };
    }
    if (decision === 'adopt') {
      if (!current.identical || current.kind !== 'legacy') fail('Adoption identity changed; no files written');
      await writeFile(join(target, receiptFile), receiptBytes(manifest.version, files, { adopted: true }), { flag: 'wx' });
      try {
        await ui.step(ui.tr('Registering native Harness roles', '注册原生宿主角色'),
          () => runAdapter(spec, 'install', options), ui.tr('Native roles registered', '原生角色已注册'));
      } catch (err) { await rm(join(target, receiptFile), { force: true }); throw err; }
      return { ...plan, result: 'adopted-without-replacement' };
    }
    let migration = current.migration || null;
    let backup = null;
    let temporaryBackup = false;
    if (decision === 'migrate' || current.adopted) {
      const reserved = await safeBackup(target, boundary);
      migration = { backupName: reserved.backupName };
      backup = reserved.destination;
    } else if (current.kind === 'managed' && !current.identical) {
      backup = join(dirname(target), '.ui-spec-managed-' + randomUUID().slice(0, 8));
      temporaryBackup = true;
    }
    const receipt = { version: manifest.version, extra: {
      ...(migration ? { migration } : {}),
    } };
    const staging = await ui.copyFiles(Object.keys(files).length,
      advance => stageSkill(target, files, receipt, advance));
    let moved = false, swapped = false;
    try {
      if (current.exists) {
        if (!backup) fail('Missing replacement backup location');
        await rename(target, backup);
        moved = true;
      }
      await rename(staging, target);
      swapped = true;
      await ui.step(ui.tr('Registering native Harness components', '注册宿主原生组件'),
        () => runAdapter(spec, 'install', options), ui.tr('Native components ready', '原生组件已就绪'));
      if (backup && temporaryBackup) await rm(backup, { recursive: true });
      return { ...plan, result: current.exists ? 'upgraded' : 'installed',
        ...(migration ? { backup: backupLocation(target, migration.backupName) } : {}) };
    } catch (err) {
      if (swapped) await rm(target, { recursive: true, force: true });
      if (moved) await rename(backup, target);
      throw err;
    } finally { await rm(staging, { recursive: true, force: true }); }
  });
  show(ui, options, outcome, ui.tr('Installation complete', '安装完成'));
}
main().catch(err => {
  if (currentPresentation?.active) {
    currentPresentation.error(err.message);
    currentPresentation.end(currentPresentation.tr('Installer stopped; review the message above', '安装已停止，请查看上方错误信息'));
  } else console.error('ui-spec: ' + err.message);
  process.exitCode = 1;
});
