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
function scopeLabel(ui, scope) {
  return scope === 'user'
    ? ui.tr('All my projects', '当前用户的所有项目')
    : ui.tr('This project', '当前项目');
}
function statusLabel(ui, status) {
  const names = {
    absent: ui.tr('Not installed', '未安装'),
    current: ui.tr('Up to date', '已是当前版本'),
    outdated: ui.tr('Update available', '可更新'),
    legacy: ui.tr('Installed previously', '已有旧安装'),
    'legacy-link': ui.tr('Installed via linked folder', '已有链接安装'),
  };
  return names[status] || status;
}
function actionLabel(ui, decision) {
  const names = {
    install: ui.tr('Install', '安装'),
    migrate: ui.tr('Back up and update', '备份并更新'),
    adopt: ui.tr('Keep existing files', '使用现有文件'),
    upgrade: ui.tr('Update', '更新'),
    'migration-required': ui.tr('Backup and update required', '需先备份并更新'),
    'upgrade-required': ui.tr('Update required', '需要更新'),
  };
  return names[decision] || decision;
}
function show(ui, options, result) {
  if (!ui.active || options.json) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }
  const tr = ui.tr;
  const location = tr('Location', '位置') + ': ' + result.skill;
  const context = [
    tr('Tool', '工具') + ': ' + ui.name(result.agent),
    tr('Install for', '安装范围') + ': ' + scopeLabel(ui, result.scope),
    location,
  ];
  let title, lines, ending;
  switch (result.result) {
    case 'status':
      title = tr('Installation status', '安装状态');
      lines = [
        tr('Status', '状态') + ': ' + statusLabel(ui, result.status),
        ...(result.installed_version ? [tr('Version', '版本') + ': ' + result.installed_version] : []),
        ...context,
      ];
      ending = tr('Checked', '查询完成');
      break;
    case 'installed':
    case 'upgraded':
      title = result.result === 'installed'
        ? tr('Installed ' + result.version, '已安装 ' + result.version)
        : tr('Updated to ' + result.version, '已更新到 ' + result.version);
      lines = [...context, ...(result.backup
        ? [tr('Previous version backed up', '旧版备份位置') + ': ' + result.backup] : [])];
      ending = tr('Restart ' + ui.name(result.agent) + ' if it is already open',
        '如 ' + ui.name(result.agent) + ' 已打开，请重新启动后使用');
      break;
    case 'already-current':
      title = tr('Already up to date', '已是当前版本');
      lines = context;
      ending = tr('No update needed', '无需更新');
      break;
    case 'adopted-without-replacement':
      title = tr('Existing files are ready to use', '现有文件已可使用');
      lines = context;
      ending = tr('Original files were kept', '保留了原有文件');
      break;
    case 'original-restored':
      title = tr('Previous installation restored', '已恢复原安装');
      lines = [location];
      ending = tr('Done', '完成');
      break;
    case 'uninstalled':
      title = tr('Uninstalled', '已卸载');
      lines = [location];
      ending = tr('Done', '完成');
      break;
    case 'adopted-copy-preserved':
      title = tr('Existing files kept', '已保留原有文件');
      lines = [location];
      ending = tr('Done', '完成');
      break;
    case 'unmanaged-preserved':
      title = tr('Installation left unchanged', '已有安装未修改');
      lines = [
        tr('This installation was created by another installer and was not removed.',
          '此版本由其他安装方式创建，本次未卸载。'),
        location,
      ];
      ending = tr('No files changed', '未修改文件');
      break;
    case 'not-installed':
      title = tr('Not installed', '未找到安装');
      lines = [location];
      ending = tr('No files changed', '未修改文件');
      break;
    case 'cancelled':
      title = tr('Existing version kept', '已保留当前版本');
      lines = [location];
      ending = tr('No files changed', '未修改文件');
      break;
    default:
      title = tr('Completed', '已完成');
      lines = context;
      ending = tr('Done', '完成');
  }
  ui.summary(lines.join('\n'), title);
  ui.end(ending);
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
  // Validate bundled files before any installation choice; no extra progress screen.
  const { registry, manifest } = await verifyBundle();
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
  const installed = await inspectTarget(target, { version: manifest.version, files });
  const plan = {
    action: options.action, version: manifest.version, agent: options.agent,
    scope: options.global ? 'user' : 'project', skill: target, skill_files: Object.keys(files).length,
    adapter: spec.adapter?.entry || null, previously_installed: installed.exists,
  };
  if (options.action === 'install' && !options.global && options.projectRoot === resolve(homedir())) {
    ui.warning(ui.tr(
      'This project is your home folder. Choose --global to install for all your projects.',
      '当前项目指向用户主目录。如需在所有项目中使用，请选择 --global。'
    ));
  }
  if (options.action === 'status') {
    const status = !installed.exists ? 'absent' : installed.kind === 'managed'
      ? (installed.identical ? 'current' : 'outdated') : installed.kind;
    show(ui, options, { ...plan, status, installed_version: installed.version || null, result: 'status' });
    return;
  }
  if (options.action === 'uninstall' && installed.kind !== 'managed') {
    show(ui, options, { ...plan, result: installed.exists ? 'unmanaged-preserved' : 'not-installed' });
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
    show(ui, options, { ...plan, result: 'cancelled' });
    return;
  }
  if (options.dryRun) {
    if (options.action === 'install' && spec.adapter) {
      await ui.step(ui.tr('Checking Codex setup', '检查 Codex 环境'),
        () => runAdapter(spec, 'install', options, true), ui.tr('Codex ready', 'Codex 已就绪'));
    }
    const result = { ...plan, dry_run: true, decision, installed_version: installed.version || null };
    if (!ui.active || options.json) console.log(JSON.stringify(result, null, 2));
    else {
      ui.summary([
        ui.tr('Action', '操作') + ': ' + actionLabel(ui, decision),
        ui.tr('Tool', '工具') + ': ' + ui.name(result.agent),
        ui.tr('Install for', '安装范围') + ': ' + scopeLabel(ui, result.scope),
        ui.tr('Location', '位置') + ': ' + result.skill,
      ].join('\n'), ui.tr('Preview', '预览'));
      ui.end(ui.tr('No files changed', '未修改文件'));
    }
    return;
  }
  if (options.action === 'install' && spec.adapter) await ui.step(
    ui.tr('Checking Codex setup', '检查 Codex 环境'),
    () => runAdapter(spec, 'install', options, true), ui.tr('Codex ready', 'Codex 已就绪')
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
      if (spec.adapter) await ui.step(ui.tr('Removing Codex roles', '移除 Codex 角色'),
        () => runAdapter(spec, 'uninstall', options), ui.tr('Codex roles removed', 'Codex 角色已移除'));
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
      if (spec.adapter) await ui.step(ui.tr('Checking Codex roles', '检查 Codex 角色'),
        () => runAdapter(spec, 'install', options), ui.tr('Roles ready', '角色已就绪'));
      return { ...plan, result: 'already-current' };
    }
    if (decision === 'adopt') {
      if (!current.identical || current.kind !== 'legacy') fail('Adoption identity changed; no files written');
      await writeFile(join(target, receiptFile), receiptBytes(manifest.version, files, { adopted: true }), { flag: 'wx' });
      try {
        if (spec.adapter) await ui.step(ui.tr('Setting up Codex roles', '配置 Codex 角色'),
          () => runAdapter(spec, 'install', options), ui.tr('Codex roles ready', 'Codex 角色已就绪'));
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
      if (spec.adapter) await ui.step(ui.tr('Setting up Codex roles', '配置 Codex 角色'),
        () => runAdapter(spec, 'install', options), ui.tr('Codex roles ready', 'Codex 角色已就绪'));
      if (backup && temporaryBackup) await rm(backup, { recursive: true });
      return { ...plan, result: current.exists ? 'upgraded' : 'installed',
        ...(migration ? { backup: backupLocation(target, migration.backupName) } : {}) };
    } catch (err) {
      if (swapped) await rm(target, { recursive: true, force: true });
      if (moved) await rename(backup, target);
      throw err;
    } finally { await rm(staging, { recursive: true, force: true }); }
  });
  show(ui, options, outcome);
}
main().catch(err => {
  if (currentPresentation?.active) {
    currentPresentation.error(err.message);
    currentPresentation.end(currentPresentation.tr('Installer stopped; review the message above', '安装已停止，请查看上方错误信息'));
  } else console.error('ui-spec: ' + err.message);
  process.exitCode = 1;
});
