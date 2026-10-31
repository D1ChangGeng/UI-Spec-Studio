import { readSettings, saveSettings, subscribeSettings, setFailureMode } from './settings-store.js';
import { createSaveNotification } from './save-notification.js';

const ids = {displayName:'business-name',organization:'business-id',location:'location',email:'email',weeklyDigest:'weekly-digest',publicProfile:'public-profile'};
const status = document.querySelector('#save-status');
const save = document.querySelector('#save-settings');
const params = new URLSearchParams(location.search);
const zh = params.get('lang') === 'zh';
const copy = zh ? {idle:'更改仅保存在当前浏览器中。',pending:'本次提交正在保存。',error:'未写入本次提交的版本。',invalid:'请修正已标出的字段。'} : {idle:'Changes are saved only in this browser.',pending:'The submitted version is being saved.',error:'The submitted version was not written.',invalid:'Correct the marked fields.'};
const names = zh ? {displayName:'显示名称',organization:'机构',location:'地点',email:'电子邮件'} : {displayName:'Display name',organization:'Organization',location:'Location',email:'Email'};
const errorsZh = {'Add a display name.':'请填写显示名称。','Use 100 characters or fewer.':'请使用不超过 100 个字符。','Use 180 characters or fewer.':'请使用不超过 180 个字符。','Enter a complete email address.':'请填写完整的电子邮件地址。'};
let latestOperation = 0;
let pending = false;
let initiatingControl = save;
function draft() { return Object.fromEntries(Object.entries(ids).map(([key,id])=>{const el=document.getElementById(id);return [key,el.type==='checkbox'?el.checked:el.value];})); }
function clearErrors() {
  for (const id of Object.values(ids)) {
    const field = document.getElementById(id);
    field.classList.remove('is-invalid');
    field.removeAttribute('aria-invalid');
    const described = (field.getAttribute('aria-describedby') || '').split(/\s+/).filter(value => value && value !== `${id}-error`);
    if (described.length) field.setAttribute('aria-describedby', described.join(' ')); else field.removeAttribute('aria-describedby');
    document.getElementById(`${id}-error`)?.remove();
  }
}
function showErrors(fieldErrors) {
  clearErrors();
  for (const [key, message] of Object.entries(fieldErrors)) {
    const field = document.getElementById(ids[key]);
    if (!field) continue;
    const feedback = document.createElement('div');
    feedback.id = `${field.id}-error`;
    feedback.className = 'invalid-feedback';
    feedback.textContent = zh ? (errorsZh[message] || message) : message;
    field.insertAdjacentElement('afterend', feedback);
    field.classList.add('is-invalid');
    field.setAttribute('aria-invalid', 'true');
    field.setAttribute('aria-describedby', [field.getAttribute('aria-describedby'), feedback.id].filter(Boolean).join(' '));
  }
  const first = document.getElementById(ids[Object.keys(fieldErrors)[0]]);
  if (first) {
    // Native focus scrolling can leave a narrow-screen field behind the fixed toast.
    // Center the recovery target while retaining Tabler's field and toast styling.
    first.scrollIntoView({ block: 'center', behavior: 'instant' });
    if (document.activeElement !== first) first.focus({ preventScroll: true });
  }
}
function load() { const data=readSettings(); for(const [key,id] of Object.entries(ids)){const el=document.getElementById(id); if(el.type==='checkbox')el.checked=data[key];else el.value=data[key];} }
function returnFocus() {
  const target = initiatingControl?.isConnected && !initiatingControl.disabled ? initiatingControl : save;
  target.focus();
}
const notification = createSaveNotification({zh, returnFocus, fieldName: key => names[key] || (zh ? '个人资料' : 'Profile')});
try { load(); status.textContent=copy.idle; } catch(error) { status.textContent=error.message; }
subscribeSettings(event => {
  if (event.operationId < latestOperation) return;
  latestOperation = event.operationId;
  pending = event.status === 'pending';
  // Native Tabler disabled styling plus aria-disabled keeps keyboard focus stable.
  save.classList.toggle('disabled', pending);
  save.setAttribute('aria-disabled', String(pending));
  save.setAttribute('aria-busy', String(pending));
  if (event.status === 'invalid') showErrors(event.fieldErrors);
  else if (event.status === 'pending') clearErrors();
  if (event.status === 'success') {
    const changed = Object.keys(ids).some(key => draft()[key] !== event.settings[key]);
    const savedTime = notification.formatTime(event.savedAt);
    status.textContent = zh ? `上次保存：${savedTime}。${changed ? '之后的编辑尚未保存。' : ''}` : `Last saved: ${savedTime}.${changed ? ' Later edits are not saved yet.' : ''}`;
  } else status.textContent = copy[event.status] || copy.idle;
  status.dataset.state = event.status;
  notification.render(event);
});
save.addEventListener('click', async () => {
  if (pending) return;
  initiatingControl = save;
  try { await saveSettings(draft()); } catch {}
});
document.querySelector('#cancel-settings').addEventListener('click',()=>{try{load();clearErrors();status.textContent=copy.idle;status.dataset.state='idle';}catch(error){status.textContent=error.message;}});
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
