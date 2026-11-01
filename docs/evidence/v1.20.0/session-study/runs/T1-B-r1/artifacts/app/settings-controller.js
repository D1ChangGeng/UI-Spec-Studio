import { readSettings, validateSettings, saveSettings, subscribeSettings, setFailureMode } from './settings-store.js';

// Business state stays in settings-store.js. This adapter owns draft presentation.
const ids = {displayName:'business-name', organization:'business-id', location:'location', email:'email', weeklyDigest:'weekly-digest', publicProfile:'public-profile'};
const fields = Object.fromEntries(Object.entries(ids).map(([key,id]) => [key, document.getElementById(id)]));
const form = document.querySelector('#settings-form');
const status = document.querySelector('#save-status');
const save = document.querySelector('#save-settings');
const cancel = document.querySelector('#cancel-settings');
const language = document.querySelector('#language-toggle');
const theme = document.querySelector('#theme-toggle');
let lang = new URLSearchParams(location.search).get('lang') === 'zh' ? 'zh' : 'en';
let persisted;
let pendingSnapshot;
let state = 'idle';
let fieldErrors = {};
let readable = true;
let restoreSaveFocus = false;

const messages = {
  en: {
    idle:'Your settings are saved only in this browser.', dirty:'You have unsaved changes.',
    pending:'Saving your submitted changes…', pendingNew:'Saving your submitted changes… New edits will need another save.',
    success:'Changes saved in this browser.', successNew:'Submitted changes saved. Your newer edits still need to be saved.',
    error:'Save did not complete. Your draft is preserved. Select Retry save to try again.',
    invalid:'Check the highlighted fields, then save again.', restored:'Unsaved changes discarded. Your saved settings are restored.',
    loadError:'Saved settings could not be read. The existing stored value has been preserved. Reload to try again.',
    save:'Save changes', saving:'Saving…', retry:'Retry save', cancel:'Cancel',
    dark:'Use dark theme', light:'Use light theme',
  },
  zh: {
    idle:'设置仅保存在当前浏览器中。', dirty:'你有尚未保存的更改。',
    pending:'正在保存已提交的更改…', pendingNew:'正在保存已提交的更改… 新编辑的内容需要再次保存。',
    success:'更改已保存到当前浏览器。', successNew:'已提交的更改已保存。新编辑的内容仍需再次保存。',
    error:'保存未完成，草稿仍然保留。请选择“重试保存”。',
    invalid:'请检查标出的字段，然后再次保存。', restored:'已放弃未保存的更改，并恢复已保存的设置。',
    loadError:'无法读取已保存的设置，原有数据未被改动。请重新加载后重试。',
    save:'保存更改', saving:'正在保存…', retry:'重试保存', cancel:'取消',
    dark:'使用深色主题', light:'使用浅色主题',
  },
};
const translations = {
  'Account Settings':'账户设置', 'My Account':'我的账户', 'Profile Details':'个人资料',
  'Business settings':'工作设置', 'My Notifications':'我的通知', 'Privacy':'隐私',
  'Plans':'方案', 'Billing & Invoices':'账单与发票', 'Experience':'使用体验', 'Give Feedback':'提供反馈',
  'Display name (required)':'显示名称（必填）', 'Organization':'机构', 'Location':'地点',
  'Email':'电子邮件', 'Email (required)':'电子邮件（必填）', 'Edit email':'编辑邮箱',
  'Notifications':'通知', 'Public profile':'公开个人资料',
  'Changes apply when you save and stay in this browser.':'更改在保存后生效，且仅保存在当前浏览器中。',
  'Use up to 100 characters.':'最多可输入 100 个字符。',
  'This email receives workspace notifications and stays private.':'此邮箱用于接收工作区通知，不会显示在公开个人资料中。',
  'Receive a weekly digest of research notes shared with your workspace.':'每周接收工作区共享研究笔记的摘要。',
  'Receive weekly digest':'接收每周摘要', 'No weekly digest':'不接收每周摘要',
  'Allow other members of this research workspace to find your profile. Your email remains private.':'允许研究工作区的其他成员找到你的个人资料。电子邮箱仍为私密信息。',
  'Allow members to find my profile':'允许成员找到我的个人资料', 'Keep my profile hidden':'隐藏我的个人资料',
};
const errorTranslations = {
  'Add a display name.':'请输入显示名称。',
  'Use 100 characters or fewer.':'请使用不超过 100 个字符。',
  'Use 180 characters or fewer.':'请使用不超过 180 个字符。',
  'Enter a complete email address.':'请输入完整的电子邮件地址。',
};
// Retain each original text node so changing locale never replaces controls or drafts.
const textNodes=[];
const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
while(walker.nextNode()) {
  const node=walker.currentNode;
  const original=node.textContent;
  const key=original.trim();
  if(translations[key] && !node.parentElement.closest('#save-status')) textNodes.push({node,original,key});
}

function draft() {
  return Object.fromEntries(Object.entries(fields).map(([key,el]) => [key,el.type === 'checkbox' ? el.checked : el.value]));
}
function equal(a,b) { return Boolean(a && b) && Object.keys(ids).every(key=>a[key]===b[key]); }
function load() {
  persisted=readSettings();
  for(const [key,el] of Object.entries(fields)) {
    if(el.type==='checkbox') el.checked=persisted[key]; else el.value=persisted[key];
  }
}
function renderErrors() {
  for(const [key,el] of Object.entries(fields)) {
    const feedback=document.getElementById(`${ids[key]}-error`);
    if(!feedback) continue;
    const error=fieldErrors[key];
    feedback.textContent=error ? (lang==='zh' ? errorTranslations[error] || error : error) : '';
    el.classList.toggle('is-invalid',Boolean(error));
    if(error) el.setAttribute('aria-invalid','true'); else el.removeAttribute('aria-invalid');
  }
}
function renderStatus() {
  const copy=messages[lang];
  const dirty=!equal(draft(),persisted);
  const pending=state==='pending';
  let message=state;
  if(pending && !equal(draft(),pendingSnapshot)) message='pendingNew';
  if(state==='success' && dirty) message='successNew';
  if(state==='idle' && dirty) message='dirty';
  status.textContent=copy[message] || copy.idle;
  status.dataset.state=state;
  const color=['error','invalid','loadError'].includes(state) ? 'danger' : state==='success' && !dirty ? 'success' : 'info';
  status.className=`alert alert-${color} text-body mb-3`;
  save.disabled=pending || !readable;
  cancel.disabled=pending || !readable;
  save.classList.toggle('btn-loading',pending);
  save.setAttribute('aria-busy',String(pending));
  const saveLabel=document.createElement('span');
  saveLabel.textContent=pending ? copy.saving : state==='error' ? copy.retry : copy.save;
  save.replaceChildren(saveLabel); // Tabler btn-loading hides child content beneath its spinner.
  cancel.textContent=copy.cancel;
}
function renderTheme() {
  const dark=document.documentElement.getAttribute('data-bs-theme')==='dark';
  theme.textContent=messages[lang][dark?'light':'dark'];
}
function renderLocale() {
  document.documentElement.lang=lang==='zh'?'zh-CN':'en';
  document.title=lang==='zh'?'Fieldnotes — 账户设置':'Fieldnotes — Account settings';
  for(const {node,original,key} of textNodes) node.textContent=lang==='zh'?original.replace(key,translations[key]):original;
  for(const nav of document.querySelectorAll('nav[aria-label]')) {
    const original=nav.dataset.originalLabel || nav.getAttribute('aria-label');
    nav.dataset.originalLabel=original;
    nav.setAttribute('aria-label',lang==='zh'?translations[original]||original:original);
  }
  language.textContent=lang==='zh'?'English':'中文';
  language.lang=lang==='zh'?'en':'zh-CN';
  renderTheme(); renderErrors(); renderStatus();
}

try { load(); } catch { readable=false; state='loadError'; }
subscribeSettings(event=>{
  state=event.status;
  if(state==='pending') {
    restoreSaveFocus=document.activeElement===save;
    pendingSnapshot=event.snapshot; fieldErrors={};
  }
  if(state==='invalid') fieldErrors=event.fieldErrors;
  if(state==='success') persisted=event.settings;
  renderErrors(); renderStatus();
  if(state==='error' || state==='success') {
    if(restoreSaveFocus && document.activeElement===document.body) save.focus({preventScroll:true});
    restoreSaveFocus=false;
  }
  if(state==='invalid') {
    const first=fields[Object.keys(ids).find(key=>fieldErrors[key])];
    first?.focus({preventScroll:true});
    first?.scrollIntoView({block:'center',behavior:'instant'});
  }
});
form.addEventListener('submit',async event=>{
  event.preventDefault();
  if(state==='pending' || !readable) return;
  try { await saveSettings(draft()); } catch { /* Store facts already updated the UI. */ }
});
for(const [key,el] of Object.entries(fields)) {
  el.addEventListener('input',()=>{
    delete fieldErrors[key];
    if(!['pending','error'].includes(state)) state='idle';
    renderErrors(); renderStatus();
  });
  if(el.type!=='checkbox') el.addEventListener('blur',event=>{
    // Keep an action target stationary between pointerdown and click.
    // Submission runs the same authoritative validation immediately afterward.
    if(event.relatedTarget?.closest('button')) return;
    const error=validateSettings(draft())[key];
    if(error) fieldErrors[key]=error; else delete fieldErrors[key];
    renderErrors();
  });
}
cancel.addEventListener('click',()=>{
  if(state==='pending') return;
  try { load(); fieldErrors={}; state='restored'; renderErrors(); renderStatus(); }
  catch { readable=false; state='loadError'; renderStatus(); }
});
document.querySelector('#focus-email').addEventListener('click',()=>fields.email.focus());
language.addEventListener('click',()=>{
  lang=lang==='zh'?'en':'zh';
  const url=new URL(location.href);url.searchParams.set('lang',lang);history.replaceState(null,'',url);
  renderLocale();
});
theme.addEventListener('click',()=>{
  const next=document.documentElement.getAttribute('data-bs-theme')==='dark'?'light':'dark';
  document.documentElement.setAttribute('data-bs-theme',next);
  localStorage.setItem('tabler-theme',next);
  const url=new URL(location.href);url.searchParams.set('theme',next);history.replaceState(null,'',url);
  renderTheme();
});
for(const link of document.querySelectorAll('a[href="#profile-heading"],a[href="#notifications-heading"],a[href="#privacy-heading"]')) {
  link.addEventListener('click',event=>{
    event.preventDefault();
    const target=document.querySelector(link.getAttribute('href'));
    target.focus();target.scrollIntoView({block:'start'});
    for(const peer of link.parentElement.querySelectorAll('a')) {peer.classList.remove('active');peer.removeAttribute('aria-current');}
    link.classList.add('active');link.setAttribute('aria-current','location');
  });
}
window.fieldnotes={readSettings,saveSettings,setFailureMode,draft};
renderLocale();
