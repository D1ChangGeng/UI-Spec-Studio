import { readSettings, saveSettings, subscribeSettings, setFailureMode } from './settings-store.js';
import { createSaveNotification } from './save-notification.js';

const ids = {displayName:'business-name',organization:'business-id',location:'location',email:'email',weeklyDigest:'weekly-digest',publicProfile:'public-profile'};
const status = document.querySelector('#save-status');
const save = document.querySelector('#save-settings');
const params = new URLSearchParams(location.search);
const zh = params.get('lang') === 'zh';
const copy = zh
  ? {idle:'更改仅保存在当前浏览器中。',pending:'正在保存…',success:'已保存在当前浏览器。',error:'更改尚未保存。',invalid:'请修正标记的字段。',dirty:'当前表单有未保存的更改。'}
  : {idle:'Changes are saved only in this browser.',pending:'Saving…',success:'Saved in this browser.',error:'Changes have not been saved.',invalid:'Correct the marked fields.',dirty:'The form has unsaved changes.'};
const fieldNames = zh
  ? {displayName:'显示名称',organization:'机构',location:'地点',email:'电子邮件'}
  : {displayName:'Display name',organization:'Organization',location:'Location',email:'Email'};
const errorTranslations = {
  'Add a display name.':'请填写显示名称。',
  'Use 100 characters or fewer.':'请使用不超过 100 个字符。',
  'Use 180 characters or fewer.':'请使用不超过 180 个字符。',
  'Enter a complete email address.':'请输入完整的电子邮件地址。'
};
let latestOperation = 0;
let currentEvent = null;
let lastField = document.getElementById(ids.displayName);
function draft() {
  return Object.fromEntries(Object.entries(ids).map(([key,id]) => {
    const el = document.getElementById(id);
    return [key, el.type === 'checkbox' ? el.checked : el.value];
  }));
}
function sameValues(a, b) { return Object.keys(ids).every(key => a[key] === b[key]); }
function clearFieldError(key) {
  const el = document.getElementById(ids[key]);
  el.classList.remove('is-invalid');
  el.removeAttribute('aria-invalid');
  const feedback = document.getElementById(ids[key] + '-error');
  if (feedback) feedback.textContent = '';
}
function clearErrors() { Object.keys(ids).forEach(clearFieldError); }
function load() {
  const data = readSettings();
  for (const [key,id] of Object.entries(ids)) {
    const el = document.getElementById(id);
    if (el.type === 'checkbox') el.checked = data[key];
    else el.value = data[key];
  }
  clearErrors();
}
function restoreFeedbackFocus() {
  // A retry starts synchronously; Save is already disabled at this point.
  const target = !save.disabled ? save : lastField;
  target.focus();
}
const notification = createSaveNotification({zh, fieldNames, restoreFocus:restoreFeedbackFocus});
try { load(); status.textContent = copy.idle; } catch (error) { status.textContent = error.message; }
subscribeSettings(event => {
  // Validation also consumes an operation ID. Never let an older completion
  // replace a newer rejected submission or a newer result.
  if (event.operationId < latestOperation) return;
  latestOperation = event.operationId;
  currentEvent = event;
  save.disabled = event.status === 'pending';
  save.setAttribute('aria-busy', String(event.status === 'pending'));
  status.dataset.state = event.status;
  status.textContent = event.status === 'success' && !sameValues(draft(), event.settings)
    ? copy.dirty : copy[event.status] || copy.idle;
  if (event.status === 'pending') clearErrors();
  let firstInvalid;
  if (event.status === 'invalid') {
    clearErrors();
    for (const key of Object.keys(ids)) {
      const message = event.fieldErrors[key];
      if (!message) continue;
      const el = document.getElementById(ids[key]);
      el.classList.add('is-invalid');
      el.setAttribute('aria-invalid', 'true');
      document.getElementById(ids[key] + '-error').textContent = zh ? errorTranslations[message] || message : message;
      firstInvalid ||= el;
    }
  }
  notification.render(event);
  if (firstInvalid && document.activeElement !== firstInvalid) firstInvalid.focus();
});
for (const [key,id] of Object.entries(ids)) {
  const el = document.getElementById(id);
  el.addEventListener('focus', () => { lastField = el; });
  el.addEventListener('input', () => {
    clearFieldError(key);
    if (currentEvent?.status !== 'pending') status.textContent = copy.dirty;
  });
}
save.addEventListener('click', async () => {
  try { await saveSettings(draft()); } catch { /* Store events own feedback. */ }
});
document.querySelector('#cancel-settings').addEventListener('click', () => {
  try { load(); status.textContent = currentEvent?.status === 'pending' ? copy.pending : copy.idle; }
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
