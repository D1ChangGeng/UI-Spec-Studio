import { readSettings, saveSettings, subscribeSettings, setFailureMode } from './settings-store.js';
import { createSaveNotification } from './save-notification.js';

const ids = {displayName:'business-name',organization:'business-id',location:'location',email:'email',weeklyDigest:'weekly-digest',publicProfile:'public-profile'};
const status = document.querySelector('#save-status');
const save = document.querySelector('#save-settings');
const params = new URLSearchParams(location.search);
const zh = params.get('lang') === 'zh';
const copy = zh ? {
  idle:'更改仅保存在当前浏览器中。', pending:'保存期间可以继续编辑。',
  newer:'较新的编辑尚未保存。', clean:'没有尚未保存的更改。',
  error:'你可以继续编辑表单。', invalid:'请修改标记的字段。'
} : {
  idle:'Changes are saved only in this browser.', pending:'You can keep editing while this version saves.',
  newer:'Your newer edits are not saved yet.', clean:'No unsaved changes.',
  error:'You can keep editing this form.', invalid:'Review the marked fields.'
};
const fieldNames = zh
  ? {displayName:'显示名称',organization:'机构',location:'地点',email:'电子邮件'}
  : {displayName:'Display name',organization:'Organization',location:'Location',email:'Email'};
const errorTranslations = {
  'Add a display name.':'请填写显示名称。',
  'Use 100 characters or fewer.':'请使用不超过 100 个字符。',
  'Use 180 characters or fewer.':'请使用不超过 180 个字符。',
  'Enter a complete email address.':'请输入完整的电子邮件地址。'
};
const fieldLabel = key => fieldNames[key] || key;
const fieldError = text => zh ? (errorTranslations[text] || text) : text;
let baseline;
let currentEvent = null;
let latestOperation = 0;
let pending = false;
let rejectedSubmitRecovery = false;
let initiatingControl = save;

function draft() {
  return Object.fromEntries(Object.entries(ids).map(([key,id]) => {
    const el = document.getElementById(id);
    return [key,el.type === 'checkbox' ? el.checked : el.value];
  }));
}
function matches(a,b) { return b && Object.keys(ids).every(key => a[key] === b[key]); }
function load() {
  const data = readSettings();
  baseline = {...data};
  for (const [key,id] of Object.entries(ids)) {
    const el = document.getElementById(id);
    if (el.type === 'checkbox') el.checked = data[key]; else el.value = data[key];
  }
}
function updateSummary() {
  const values = draft();
  const state = currentEvent?.status;
  if (state === 'pending') status.textContent = matches(values,currentEvent.snapshot) ? copy.pending : copy.newer;
  else if (state === 'invalid' && document.querySelector('.form-control.is-invalid')) status.textContent = copy.invalid;
  else if (state === 'error') status.textContent = copy.error;
  else status.textContent = matches(values,baseline) ? (state === 'success' ? copy.clean : copy.idle) : copy.newer;
}
function clearFieldError(key) {
  const el = document.getElementById(ids[key]);
  if (!el) return;
  const errorId = `${el.id}-error`;
  el.classList.remove('is-invalid');
  el.removeAttribute('aria-invalid');
  const describedBy = (el.getAttribute('aria-describedby') || '').split(' ').filter(id => id && id !== errorId);
  if (describedBy.length) el.setAttribute('aria-describedby',describedBy.join(' '));
  else el.removeAttribute('aria-describedby');
  document.getElementById(errorId)?.remove();
}
function clearFieldErrors() { Object.keys(ids).forEach(clearFieldError); }
function showFieldErrors(errors) {
  clearFieldErrors();
  for (const [key,text] of Object.entries(errors)) {
    const el = document.getElementById(ids[key]);
    if (!el) continue;
    const feedback = document.createElement('div');
    feedback.id = `${el.id}-error`;
    feedback.className = 'invalid-feedback';
    feedback.textContent = fieldError(text);
    el.insertAdjacentElement('afterend',feedback);
    el.classList.add('is-invalid');
    el.setAttribute('aria-invalid','true');
    el.setAttribute('aria-describedby',[el.getAttribute('aria-describedby'),feedback.id].filter(Boolean).join(' '));
  }
  const invalidElements = Object.keys(errors).map(key => document.getElementById(ids[key])).filter(Boolean);
  if (rejectedSubmitRecovery && !invalidElements.includes(document.activeElement)) {
    const firstInvalid = invalidElements[0];
    firstInvalid?.focus();
    // Keep rejected-submit recovery clear of the fixed toast while inheriting
    // the source's native smooth/reduced-motion scrolling behavior.
    firstInvalid?.scrollIntoView({block:'center'});
  }
}
function restoreFocus() {
  const target = initiatingControl?.isConnected && !initiatingControl.disabled ? initiatingControl : save;
  target.focus();
}
try { load(); status.textContent = copy.idle; } catch (error) { status.textContent = error.message; }

subscribeSettings(event => {
  if (!Number.isInteger(event.operationId) || event.operationId < latestOperation) return;
  latestOperation = event.operationId;
  currentEvent = event;
  pending = event.status === 'pending';
  // The native disabled visual state, aria-disabled and the guarded handler keep
  // the initiating button focusable while preventing a duplicate submission.
  save.classList.toggle('disabled',pending);
  save.setAttribute('aria-disabled',String(pending));
  save.setAttribute('aria-busy',String(pending));
  status.dataset.state = event.status;
  if (event.status === 'invalid') showFieldErrors(event.fieldErrors);
  if (event.status === 'pending') clearFieldErrors();
  if (event.status === 'success') baseline = {...event.settings};
  updateSummary();
});
createSaveNotification({subscribeSettings,saveSettings,zh,fieldLabel,fieldError,restoreFocus});

save.addEventListener('click',async () => {
  if (pending) return;
  initiatingControl = save;
  rejectedSubmitRecovery = true;
  const operation = saveSettings(draft());
  rejectedSubmitRecovery = false; // Validation is emitted synchronously by the store.
  try { await operation; } catch { /* Authoritative events supply all feedback. */ }
});
for (const [key,id] of Object.entries(ids)) {
  document.getElementById(id).addEventListener('input',() => { clearFieldError(key); updateSummary(); });
}
document.querySelector('#cancel-settings').addEventListener('click',() => {
  try { load(); clearFieldErrors(); if (!pending) currentEvent = null; updateSummary(); }
  catch (error) { status.textContent = error.message; }
});
document.querySelector('#focus-email').addEventListener('click',()=>document.querySelector('#email').focus());
document.querySelector('#language-toggle').addEventListener('click',()=>{params.set('lang',zh?'en':'zh');location.search=params.toString();});
document.querySelector('#theme-toggle').addEventListener('click',()=>{const dark=document.documentElement.getAttribute('data-bs-theme')==='dark';document.documentElement.setAttribute('data-bs-theme',dark?'light':'dark');localStorage.setItem('tabler-theme',dark?'light':'dark');});
window.fieldnotes = { readSettings, saveSettings, setFailureMode, draft };
if (zh) {
  document.documentElement.lang='zh-CN';
  const dictionary={
    'Account Settings':'账户设置','My Account':'我的账户','Profile Details':'个人资料','Business Profile':'工作资料','Display name':'显示名称','Organization':'机构','Location':'地点','Email':'电子邮件','Edit email':'编辑邮箱','Notifications':'通知','My Notifications':'我的通知','Privacy':'隐私','Public profile':'公开个人资料','Save changes':'保存更改','Cancel':'取消','Switch theme':'切换主题','Business settings':'工作设置',
    'Receive a weekly digest of research notes shared with your workspace.':'每周接收工作区共享研究笔记的摘要。',
    'Weekly digest is enabled':'已开启每周摘要','Weekly digest is disabled':'已关闭每周摘要',
    'Allow other members of this research workspace to find your profile. Your email remains private.':'允许研究工作区的其他成员找到你的个人资料。电子邮箱仍为私密信息。',
    "You're currently visible":'当前可见',"You're currently invisible":'当前不可见',
    'This contact will be shown to others publicly, so choose it carefully.':'此邮箱用于工作区通知，不会显示在公开个人资料中。'
  };
  const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  while(walker.nextNode()){const node=walker.currentNode;const source=node.textContent.trim();if(dictionary[source])node.textContent=node.textContent.replace(source,dictionary[source]);}
} else {
  for(const el of document.querySelectorAll('.card-subtitle')) if(el.textContent.trim()==='This contact will be shown to others publicly, so choose it carefully.') el.textContent='This email receives workspace notifications and stays private.';
}
