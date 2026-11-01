// Save feedback adapter. Visual shell: Tabler 1.7.1 action-bearing Toast (MIT).
// Persistence and validation remain exclusively in settings-store.js.
export function createSaveNotification({ saveSnapshot, zh, fieldLabel, fieldError, fallbackFocus }) {
  const element = document.getElementById('save-notification');
  const message = document.getElementById('save-notification-message');
  const time = document.getElementById('save-notification-time');
  const actions = document.getElementById('save-notification-actions');
  const retry = document.getElementById('retry-save');
  const close = element.querySelector('[data-bs-dismiss="toast"]');
  const toast = window.tabler.Toast.getOrCreateInstance(element, { autohide: false });
  const clock = new Intl.DateTimeFormat(zh ? 'zh-CN' : 'en', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  let latestOperation = 0;
  let failedSnapshot = null;
  let returnFocus = null;
  let hiding = false;
  let showAfterHide = false;
  let restoreAfterHide = false;
  close.setAttribute('aria-label', zh ? '关闭保存通知' : 'Close save notification');
  retry.textContent = zh ? '重试保存' : 'Retry save';

  function restoreFocus() {
    const target = returnFocus?.isConnected && !returnFocus.disabled ? returnFocus : fallbackFocus();
    target?.focus();
  }
  element.addEventListener('hide.bs.toast', () => {
    hiding = true;
    restoreAfterHide = element.contains(document.activeElement);
  });
  element.addEventListener('hidden.bs.toast', () => {
    hiding = false;
    if (restoreAfterHide && (document.activeElement === document.body || element.contains(document.activeElement))) restoreFocus();
    restoreAfterHide = false;
    if (showAfterHide) {
      showAfterHide = false;
      toast.show();
    }
  });
  retry.addEventListener('click', () => {
    if (!failedSnapshot || element.dataset.state !== 'error') return;
    // Copy the authoritative failed snapshot; never silently read a newer form draft.
    void saveSnapshot({ ...failedSnapshot });
  });

  return {
    render(event) {
      if (event.operationId < latestOperation) return;
      latestOperation = event.operationId;
      if (!element.contains(document.activeElement) && document.activeElement !== document.body) returnFocus = document.activeElement;
      if (event.status !== 'error' && actions.contains(document.activeElement)) restoreFocus();
      failedSnapshot = event.status === 'error' ? { ...event.snapshot } : null;
      actions.hidden = event.status !== 'error';
      element.dataset.state = event.status;
      element.dataset.operationId = String(event.operationId);
      time.textContent = event.status === 'success' ? clock.format(new Date(event.savedAt)) : (zh ? '现在' : 'Now');
      if (event.status === 'success') {
        time.setAttribute('title', new Date(event.savedAt).toLocaleString(zh ? 'zh-CN' : 'en'));
      } else time.removeAttribute('title');
      const firstField = Object.keys(event.fieldErrors || {})[0];
      const words = zh ? {
        pending: '正在保存更改。正在将本次提交的版本保存到当前浏览器。',
        success: '更改已保存。本次提交的版本已保存在当前浏览器，保存时间见上方。',
        error: '保存未完成。草稿仍然保留。重试将保存失败时提交的版本。',
        invalid: firstField ? '请检查个人资料字段。' + fieldLabel(firstField) + '：' + fieldError(event.fieldErrors[firstField]) : ''
      } : {
        pending: 'Saving changes. This submitted version is being saved in this browser.',
        success: 'Changes saved. This submitted version is saved in this browser at the time shown above.',
        error: 'Save did not complete. Your draft is preserved. Retry saves the version from the failed attempt.',
        invalid: firstField ? 'Check profile fields. ' + fieldLabel(firstField) + ': ' + fieldError(event.fieldErrors[firstField]) : ''
      };
      message.textContent = words[event.status] || '';
      if (hiding) showAfterHide = true;
      else if (!element.classList.contains('show')) toast.show();
    }
  };
}

