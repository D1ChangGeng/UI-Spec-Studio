import { saveSettings } from './settings-store.js';

// State adapter for the MIT Tabler 1.7.1 action-toast markup in index.html.
// All surface, transition and dismissal behavior remains with tabler.Toast.
export function createSaveNotification({zh, fieldNames, restoreFocus}) {
  const element = document.getElementById('save-notification');
  const message = document.getElementById('save-notification-message');
  const time = document.getElementById('save-notification-time');
  const actions = document.getElementById('save-notification-actions');
  const retry = document.getElementById('retry-save');
  const close = document.getElementById('save-notification-close');
  const toast = tabler.Toast.getOrCreateInstance(element, {autohide:false});
  const copy = zh ? {
    pending:'正在保存更改。正在将已提交的版本保存到当前浏览器。',
    success:'更改已保存。此版本仅存储在当前浏览器中。',
    error:'保存未完成。草稿仍然保留。重试将保存失败的版本。',
    invalid:name => `请检查个人资料字段。请先检查${name}。`,
    retry:'重试保存',close:'关闭保存通知',now:'刚刚'
  } : {
    pending:'Saving changes. The submitted version is being saved in this browser.',
    success:'Changes saved. This version is stored only in this browser.',
    error:'Save did not complete. Your draft is still available. Retry saves the failed version.',
    invalid:name => `Check profile fields. Start with ${name}.`,
    retry:'Retry save',close:'Close save notification',now:'Just now'
  };
  close.setAttribute('aria-label', copy.close);
  retry.textContent = copy.retry;
  let latestOperation = 0;
  let failedSnapshot = null;
  let renderVersion = 0;
  let hiding = false;
  let hideVersion = 0;
  let returnAfterHide = false;

  element.addEventListener('hide.bs.toast', () => {
    hiding = true;
    hideVersion = renderVersion;
    returnAfterHide = element.contains(document.activeElement);
  });
  element.addEventListener('hidden.bs.toast', () => {
    hiding = false;
    if (returnAfterHide && (document.activeElement === document.body || element.contains(document.activeElement))) restoreFocus();
    returnAfterHide = false;
    // A newer authoritative event can arrive during the native hide transition.
    if (renderVersion !== hideVersion) toast.show();
  });
  retry.addEventListener('click', async () => {
    if (!failedSnapshot) return;
    const snapshot = {...failedSnapshot};
    // Do not dismiss here: only the authoritative pending event replaces error.
    try { await saveSettings(snapshot); } catch { /* Store events own feedback. */ }
  });
  return {
    render(event) {
      if (event.operationId < latestOperation) return;
      latestOperation = event.operationId;
      renderVersion++;
      const firstField = Object.keys(fieldNames).find(key => event.fieldErrors?.[key]);
      message.textContent = event.status === 'invalid' ? copy.invalid(fieldNames[firstField] || (zh ? '标记的字段' : 'the marked field')) : copy[event.status];
      time.textContent = event.status === 'success'
        ? new Date(event.savedAt).toLocaleTimeString(zh ? 'zh-CN' : 'en', {hour:'2-digit',minute:'2-digit'})
        : copy.now;
      time.title = event.status === 'success' ? new Date(event.savedAt).toLocaleString(zh ? 'zh-CN' : 'en') : '';
      failedSnapshot = event.status === 'error' ? {...event.snapshot} : null;
      if (event.status !== 'error' && document.activeElement === retry) restoreFocus();
      actions.hidden = event.status !== 'error';
      element.dataset.state = event.status;
      element.dataset.operationId = String(event.operationId);
      // Existing visible feedback updates in place; the source owns its entrance.
      if (!hiding && !toast.isShown()) toast.show();
    }
  };
}
