// Clack owns interactive presentation; headless output remains machine-readable.
const toolNames = {
  codex: 'Codex',
  'claude-code': 'Claude Code',
  cursor: 'Cursor',
  opencode: 'OpenCode',
};

export async function createPresentation({ noTui = false, json = false, lang, version }) {
  const chinese = (lang || Intl.DateTimeFormat().resolvedOptions().locale).toLowerCase().startsWith('zh');
  const tr = (en, zh) => chinese ? zh : en;
  const name = (id) => toolNames[id] || id;
  const eligible = !noTui && !json && !!process.stdin.isTTY && !!process.stdout.isTTY && process.env.CI !== 'true';
  let p = null;
  if (eligible) {
    try { p = await import('@clack/prompts'); }
    catch { /* Offline or headless installation must remain available. */ }
  }
  const active = Boolean(p);
  const cancel = () => p.cancel(tr('Cancelled', '已取消'));
  return {
    active, tr, name,
    intro() { if (active) p.intro('UI SPEC STUDIO  v' + version); },
    info(message) { if (active) p.log.info(message); },
    warning(message) { if (active) p.log.warn(message); },
    success(message) { if (active) p.log.success(message); },
    summary(message, heading = tr('Details', '详细信息')) {
      if (active) p.note(message, heading);
    },
    async step(message, fn, finished = tr('Done', '完成')) {
      if (!active) return await fn();
      const spin = p.spinner();
      spin.start(message);
      try { const result = await fn(); spin.stop(finished); return result; }
      catch (err) { spin.stop(tr('Could not complete', '未能完成')); throw err; }
    },
    async copyFiles(total, operation) {
      if (!active) return await operation(() => {});
      const bar = p.progress({ max: total });
      bar.start(tr('Installing UI Spec Studio', '正在安装 UI Spec Studio'));
      try {
        const result = await operation(() => bar.advance(1));
        bar.stop(tr('Files verified', '文件校验完成'));
        return result;
      } catch (err) {
        bar.stop(tr('Installation failed', '安装失败'));
        throw err;
      }
    },
    async chooseScope(projectRoot, homeRoot) {
      if (!active) return 'project';
      const isHome = projectRoot.toLowerCase() === homeRoot.toLowerCase();
      const project = {
        value: 'project',
        label: tr('This project', '当前项目'),
        hint: projectRoot,
      };
      const user = {
        value: 'user',
        label: tr('All my projects', '当前用户的所有项目'),
      };
      const chosen = await p.select({
        message: tr('Where should it be installed?', '安装到哪里？'),
        options: isHome ? [user, project] : [project, user],
      });
      if (p.isCancel(chosen)) { cancel(); return 'cancel'; }
      return chosen;
    },
    async chooseAgent(ids) {
      if (!active) throw new Error(tr('Choose a tool with --agent, or use an interactive terminal.',
        '请使用 --agent 指定工具，或在交互终端中安装。'));
      const value = await p.select({
        message: tr('Which tool will you use?', '在哪个工具中使用？'),
        options: ids.map(id => ({ value: id, label: name(id) })),
      });
      if (p.isCancel(value)) { cancel(); return null; }
      return value;
    },
    async resolveExisting({ kind, identical, version: installed, path }) {
      if (!active) return null;
      p.note([
        ...(installed ? [tr('Installed version: ', '已有版本：') + installed] : []),
        tr('Location: ', '位置：') + path,
        ...(kind === 'legacy-link' ? [tr('The existing installation uses a linked folder.',
          '现有安装使用了目录链接。')] : []),
        ...(identical ? [tr('Its files already match this version.', '文件与当前版本一致。')] : []),
      ].join('\n'), tr('Existing installation', '检测到已有安装'));
      const options = [];
      if (identical && kind !== 'legacy-link') options.push({
        value: 'adopt',
        label: tr('Keep and use these files', '直接使用现有文件'),
        hint: tr('No replacement; these files remain on uninstall', '不替换文件，卸载后仍会保留'),
      });
      options.push({
        value: 'migrate',
        label: tr('Back up and update', '备份并更新'),
        hint: tr('The previous installation is restored on uninstall', '卸载时恢复原安装'),
      }, {
        value: 'keep',
        label: tr('Keep the current version', '保留当前版本'),
      });
      const value = await p.select({
        message: tr('What would you like to do with the existing version?', '如何处理已有版本？'),
        options,
      });
      if (p.isCancel(value)) { cancel(); return 'keep'; }
      return value;
    },
    async resolveUpgrade(installed) {
      if (!active) return null;
      const value = await p.select({
        message: tr('Installed version: ' + installed, '已有版本：' + installed),
        options: [
          { value: 'upgrade', label: tr('Update to ' + version, '更新到 ' + version) },
          { value: 'keep', label: tr('Keep the current version', '保留当前版本') },
        ],
      });
      if (p.isCancel(value)) { cancel(); return 'keep'; }
      return value;
    },
    end(message) { if (active) p.outro(message); },
    error(message) { if (active) p.log.error(message); },
  };
}
