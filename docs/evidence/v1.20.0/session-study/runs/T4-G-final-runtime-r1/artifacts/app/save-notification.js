// Tabler 1.7.1 action-toast integration. The source shell is in index.html.
// Tabler copyright (c) 2018-2026 The Tabler Authors, MIT; see LICENSE.
import { saveSettings } from './settings-store.js';

export function createSaveNotification({ zh, returnFocus, fieldName }) {
  const root = document.querySelector('#save-notification');
  const message = document.querySelector('#save-notification-message');
  const time = document.querySelector('#save-notification-time');
  const actions = document.querySelector('#save-notification-actions');
  const retry = document.querySelector('#retry-save');
  const close = root.querySelector('[data-bs-dismiss="toast"]');
  const toast = window.tabler.bootstrap.Toast.getOrCreateInstance(root, { autohide: false });
  const formatTime = value => new Intl.DateTimeFormat(zh ? 'zh-CN' : 'en', {hour:'2-digit',minute:'2-digit',second:'2-digit'}).format(new Date(value));
  let latestOperation = 0;
  let failedSnapshot = null;
  let hiding = false;
  let reopen = false;
  let restoreAfterHide = false;
  close.setAttribute('aria-label', zh ? '关闭保存提示' : 'Close save feedback');
  retry.textContent = zh ? '重试保存' : 'Retry save';

  root.addEventListener('hide.bs.toast', () => {
    hiding = true;
    restoreAfterHide = root.contains(document.activeElement);
  });
  root.addEventListener('hidden.bs.toast', () => {
    hiding = false;
    if (restoreAfterHide && (root.contains(document.activeElement) || document.activeElement === document.body)) returnFocus();
    restoreAfterHide = false;
    if (reopen) { reopen = false; toast.show(); }
  });
  retry.addEventListener('click', () => {
    if (!failedSnapshot) return;
    // Retry exactly the submitted snapshot. Later form edits remain owned by the form.
    const snapshot = { ...failedSnapshot };
    saveSettings(snapshot).catch(() => {});
  });

  return {
    render(event) {
      if (event.operationId < latestOperation) return;
      latestOperation = event.operationId;
      const isError = event.status === 'error';
      if (!isError && actions.contains(document.activeElement)) returnFocus();
      failedSnapshot = isError ? { ...event.snapshot } : null;
      actions.hidden = !isError;
      root.dataset.state = event.status;
      root.dataset.operationId = String(event.operationId);
      time.textContent = event.savedAt ? formatTime(event.savedAt) : (zh ? '刚刚' : 'Now');
      if (event.savedAt) time.setAttribute('title', event.savedAt); else time.removeAttribute('title');
      const firstField = Object.keys(event.fieldErrors || {})[0];
      const content = zh ? {
        pending: '正在保存更改。正在将本次提交的版本保存到当前浏览器。',
        success: '更改已保存。本次提交的版本仅保存在当前浏览器中。',
        error: '保存未完成。草稿仍然保留。重试将保存上次提交的版本。',
        invalid: `请检查个人资料字段：${fieldName(firstField)}。`
      } : {
        pending: 'Saving changes. Saving the submitted version in this browser.',
        success: 'Changes saved. The submitted version is saved only in this browser.',
        error: 'Save did not complete. Your draft is preserved. Retry saves the previously submitted version.',
        invalid: `Check profile fields: ${fieldName(firstField)}.`
      };
      message.textContent = content[event.status];
      if (hiding) reopen = true;
      else if (!root.classList.contains('show')) toast.show();
    },
    formatTime
  };
}
