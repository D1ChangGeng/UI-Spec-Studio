// Render authoritative settings events through the selected native Tabler Toast.
// Persistence, validation and operation IDs remain owned by settings-store.js.
export function createSaveNotification({subscribeSettings, saveSettings, zh, fieldLabel, fieldError, restoreFocus}) {
  const element = document.getElementById('save-notification');
  const message = document.getElementById('save-notification-message');
  const time = document.getElementById('save-notification-time');
  const action = document.getElementById('save-notification-action');
  const retry = document.getElementById('retry-save');
  const close = element.querySelector('[data-bs-dismiss="toast"]');
  const toast = window.tabler.Toast.getOrCreateInstance(element, {autohide:false});
  let latestOperation = 0;
  let failedSnapshot = null;
  let hiding = false;
  let wantsVisible = false;
  const copy = zh ? {
    pending:'正在保存更改。正在将本次提交的版本保存在当前浏览器中。',
    success:'更改已保存。本次提交的版本仅保存在当前浏览器中。',
    error:'保存未完成。草稿仍然保留。重试将保存此前提交的版本。',
    invalid:'请检查个人资料字段。',
    pendingTime:'正在保存…', errorTime:'未保存', invalidTime:'检查字段',
    retry:'重试保存', close:'关闭保存提示'
  } : {
    pending:'Saving changes. This submitted version is being saved in this browser.',
    success:'Changes saved. This submitted version is saved only in this browser.',
    error:'Save did not complete. Your submitted draft is still available. Retry saves that version.',
    invalid:'Check profile fields.',
    pendingTime:'Saving…', errorTime:'Not saved', invalidTime:'Check fields',
    retry:'Retry save', close:'Close save notification'
  };
  retry.textContent = copy.retry;
  close.setAttribute('aria-label', copy.close);

  // Keep the upstream close interaction and transition. A result arriving during
  // native dismissal waits for hidden.bs.toast instead of racing its callback.
  element.addEventListener('hide.bs.toast', () => {
    hiding = true;
    wantsVisible = false;
    if (element.contains(document.activeElement)) restoreFocus();
  });
  element.addEventListener('hidden.bs.toast', () => {
    hiding = false;
    if (wantsVisible) toast.show();
  });

  retry.addEventListener('click', async () => {
    if (!failedSnapshot || action.hidden) return;
    // Never replace the user's newer live form with this submitted snapshot.
    const snapshot = {...failedSnapshot};
    try { await saveSettings(snapshot); } catch { /* The store emits the outcome. */ }
  });

  return subscribeSettings(event => {
    if (!Number.isInteger(event.operationId) || event.operationId < latestOperation) return;
    if (!['pending','success','error','invalid'].includes(event.status)) return;
    latestOperation = event.operationId;
    failedSnapshot = event.status === 'error' ? {...event.snapshot} : null;
    if (event.status !== 'error' && action.contains(document.activeElement)) restoreFocus();
    action.hidden = event.status !== 'error';
    element.dataset.state = event.status;
    element.dataset.operationId = String(event.operationId);
    let text = copy[event.status];
    if (event.status === 'invalid') {
      const field = Object.keys(event.fieldErrors)[0];
      text += zh ? `${fieldLabel(field)}：${fieldError(event.fieldErrors[field])}`
                 : ` ${fieldLabel(field)}: ${fieldError(event.fieldErrors[field])}`;
    }
    message.textContent = text;
    time.textContent = event.status === 'success'
      ? new Intl.DateTimeFormat(zh ? 'zh-CN' : 'en', {hour:'2-digit',minute:'2-digit',second:'2-digit'}).format(new Date(event.savedAt))
      : copy[`${event.status}Time`];
    if (event.status === 'success') time.title = event.savedAt;
    else time.removeAttribute('title');
    wantsVisible = true;
    if (!hiding && !toast.isShown()) toast.show();
  });
}
