// Mature terminal interaction primitives supplied by @clack/prompts (MIT).
// Non-TTY and CI keep stable machine-readable output without animations.
export async function createPresentation({ noTui = false, json = false, lang, version }) {
  const chinese = (lang || Intl.DateTimeFormat().resolvedOptions().locale).toLowerCase().startsWith('zh');
  const tr = (en, zh) => chinese ? zh : en;
  const eligible = !noTui && !json && !!process.stdin.isTTY && !!process.stdout.isTTY && process.env.CI !== 'true';
  let p = null;
  if (eligible) {
    try { p = await import('@clack/prompts'); }
    catch { /* Optional dependency can be skipped for fully offline installation. */ }
  }
  const active = Boolean(p);
  return {
    active, tr,
    intro() { if (active) p.intro('UI SPEC STUDIO  v' + version); },
    info(message) { if (active) p.log.info(message); },
    warning(message) { if (active) p.log.warn(message); },
    success(message) { if (active) p.log.success(message); },
    summary(message, heading = tr('Installation plan', '安装方案')) {
      if (active) p.note(message, heading);
    },
    async step(message, fn, finished = tr('Done', '完成')) {
      if (!active) return await fn();
      const spin = p.spinner();
      spin.start(message);
      try { const result = await fn(); spin.stop(finished); return result; }
      catch (err) { spin.stop(tr('Action failed', '操作失败')); throw err; }
    },
    async copyFiles(total, operation) {
      if (!active) return await operation(() => {});
      const bar = p.progress({ max: total });
      bar.start(tr('Preparing ' + total + ' Skill files', '正在准备 ' + total + ' 个 Skill 文件'));
      try {
        const result = await operation(() => bar.advance(1));
        bar.stop(tr('All files copied and verified', '所有 Skill 文件已复制并验证'));
        return result;
      } catch (err) {
        bar.stop(tr('File preparation failed', '文件准备失败'));
        throw err;
      }
    },
    async chooseAgent(names) {
      if (!active) throw new Error(tr('Select a Harness with --agent or use an interactive terminal', '请通过 --agent 指定宿主，或使用交互终端'));
      const value = await p.select({
        message: tr('Which coding Harness will use UI Spec Studio?', '将 UI Spec Studio 安装到哪个编码宿主？'),
        options: names.map(name => ({ value: name, label: name })),
      });
      if (p.isCancel(value)) { p.cancel(tr('No files changed', '未修改任何文件')); return null; }
      return value;
    },
    async resolveExisting({ kind, identical, version: installed, path }) {
      if (!active) return null;
      p.note([
        tr('Existing version: ', '已有版本：') + (installed || tr('unknown', '未知')),
        tr('Type: ', '类型：') + (kind === 'legacy-link' ? tr('link/junction', '链接 / Junction') : tr('unmanaged folder', '未托管目录')),
        tr('Files match this release: ', '与新版本文件一致：') + (identical ? tr('yes', '是') : tr('no / unverified', '否 / 未验证')),
        tr('Location: ', '位置：') + path,
      ].join('\n'), tr('Existing installation', '检测到已有安装'));
      const options = [];
      if (identical && kind !== 'legacy-link') options.push({
        value: 'adopt', label: tr('Adopt identical files; no replacement', '接管相同文件，不重新复制'),
        hint: tr('Original files remain on uninstall', '卸载时保留原有文件'),
      });
      options.push({
        value: 'migrate', label: tr('Back up existing installation, then update', '备份原安装后更新（推荐）'),
        hint: tr('Reversible; original restored on uninstall', '可恢复，卸载时自动还原旧安装'),
      }, {
        value: 'keep', label: tr('Keep existing installation unchanged', '保留现有安装，不作修改'),
      });
      const value = await p.select({ message: tr('How should this Skill be handled?', '如何处理这个 Skill？'), options });
      if (p.isCancel(value)) { p.cancel(tr('No files changed', '未修改任何文件')); return 'keep'; }
      return value;
    },
    async resolveUpgrade(installed) {
      if (!active) return null;
      const value = await p.select({
        message: tr('Managed version ' + installed + ' detected', '检测到已托管的 ' + installed),
        options: [
          { value: 'upgrade', label: tr('Upgrade to this release', '升级到当前版本') },
          { value: 'keep', label: tr('Keep existing version', '保留现有版本') },
        ],
      });
      if (p.isCancel(value)) { p.cancel(tr('No files changed', '未修改任何文件')); return 'keep'; }
      return value;
    },
    end(message) { if (active) p.outro(message); },
    error(message) { if (active) p.log.error(message); },
  };
}
