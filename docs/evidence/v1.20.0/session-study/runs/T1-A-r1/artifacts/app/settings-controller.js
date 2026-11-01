import { readSettings, saveSettings, subscribeSettings, setFailureMode } from './settings-store.js';

const ids = {displayName:'business-name', organization:'business-id', location:'location', email:'email', weeklyDigest:'weekly-digest', publicProfile:'public-profile'};
const form = document.querySelector('#settings-form');
const status = document.querySelector('#save-status');
const save = document.querySelector('#save-settings');
const cancel = document.querySelector('#cancel-settings');
let lang = new URLSearchParams(location.search).get('lang') === 'zh' ? 'zh' : 'en';
let baseline, pendingSnapshot, pendingFocus;
let phase = 'idle', fieldErrors = {}, readError = false;
const messages = {
  en: {
    accountSettings:'Account settings', myAccount:'My account', profileDetails:'Profile details',
    businessSettings:'Business settings', notifications:'Notifications', privacy:'Privacy', plans:'Plans',
    billing:'Billing & invoices', experience:'Experience', feedback:'Give feedback', sections:'Settings sections',
    profileContext:'Your identity in this research workspace.',
    displayName:'Display name', organization:'Organization', location:'Location', email:'Email',
    nameHint:'Required · Up to 100 characters.', organizationHint:'Optional · Up to 180 characters.',
    locationHint:'Optional · Up to 100 characters.', emailHint:'Required · Used for notifications. Always private.',
    notificationsHelp:'Receive a weekly digest of research notes shared with your workspace.',
    weeklyDigest:'Weekly digest', publicProfile:'Public profile', profileVisible:'Visible to workspace members',
    privacyHelp:'Let other workspace members find your profile. Your email stays private.',
    cancel:'Cancel', save:'Save changes', retry:'Retry save', saving:'Saving…',
    idle:'Settings are saved only in this browser.', dirty:'You have unsaved changes.',
    pending:'Saving your changes…',
    pendingNew:'Saving the submitted version. Your newer edits will need another save.',
    success:'Your changes are saved in this browser.',
    savedNew:'Submitted changes saved. Your newer edits are still unsaved.',
    error:'Save did not complete. Your draft is still here. Retry when ready.',
    invalid:'Check the highlighted fields, then save again.',
    restored:'Unsaved changes discarded. Last saved settings restored.',
    unreadable:'Saved settings could not be read. Your stored data has been preserved. Reload to try again.',
    dark:'Use dark theme', light:'Use light theme',
    requiredName:'Add a display name.', nameLength:'Use 100 characters or fewer.',
    organizationLength:'Use 180 characters or fewer.', locationLength:'Use 100 characters or fewer.',
    emailInvalid:'Enter a complete email address.'
  },
  zh: {
    accountSettings:'账户设置', myAccount:'我的账户', profileDetails:'个人资料',
    businessSettings:'工作设置', notifications:'通知', privacy:'隐私', plans:'方案',
    billing:'账单与发票', experience:'使用体验', feedback:'提供反馈', sections:'设置导航',
    profileContext:'你在研究工作区中的身份信息。',
    displayName:'显示名称', organization:'机构', location:'地点', email:'电子邮箱',
    nameHint:'必填 · 最多 100 个字符。', organizationHint:'选填 · 最多 180 个字符。',
    locationHint:'选填 · 最多 100 个字符。', emailHint:'必填 · 用于接收通知，始终保持私密。',
    notificationsHelp:'每周接收工作区共享研究笔记的摘要。',
    weeklyDigest:'每周摘要', publicProfile:'公开个人资料', profileVisible:'对工作区成员可见',
    privacyHelp:'允许工作区的其他成员找到你的个人资料。电子邮箱始终保持私密。',
    cancel:'取消', save:'保存更改', retry:'重试保存', saving:'正在保存…',
    idle:'设置仅保存在当前浏览器中。', dirty:'你有尚未保存的更改。',
    pending:'正在保存你的更改…',
    pendingNew:'正在保存已提交的版本。之后的编辑仍需再次保存。',
    success:'更改已保存到当前浏览器。',
    savedNew:'已提交的更改已保存。之后的编辑尚未保存。',
    error:'保存未完成。草稿仍然保留，可以重试。',
    invalid:'请检查标出的字段，然后重新保存。',
    restored:'已放弃未保存的更改，恢复上次保存的设置。',
    unreadable:'无法读取已保存的设置。原有数据已保留，请重新加载后重试。',
    dark:'使用深色主题', light:'使用浅色主题',
    requiredName:'请填写显示名称。', nameLength:'请使用不超过 100 个字符。',
    organizationLength:'请使用不超过 180 个字符。', locationLength:'请使用不超过 100 个字符。',
    emailInvalid:'请输入完整的电子邮箱地址。'
  }
};
const t = key => messages[lang][key] || key;
function draft() {
  return Object.fromEntries(Object.entries(ids).map(([key,id]) => {
    const el = document.getElementById(id);
    return [key,el.type === 'checkbox' ? el.checked : el.value];
  }));
}
function same(a,b) { return Object.keys(ids).every(key => a?.[key] === b?.[key]); }
function dirty() { return Boolean(baseline) && !same(draft(),baseline); }
// Content-height adapter only; Tabler retains the complete form-control treatment.
function fitText(elements = form.querySelectorAll('textarea')) {
  for (const el of elements) {
    el.style.height = 'auto';
    el.style.height = (el.scrollHeight + 2) + 'px';
  }
}
function showIdentity() {
  const name = String(baseline?.displayName || '');
  document.querySelector('#saved-name').textContent = name;
  const initials = name.trim().split(/\s+/u).filter(Boolean).slice(0,2).map(part => Array.from(part)[0]).join('');
  document.querySelector('#profile-avatar').textContent = initials || 'FN';
}
function load() {
  baseline = readSettings();
  for (const [key,id] of Object.entries(ids)) {
    const el = document.getElementById(id);
    if (el.type === 'checkbox') el.checked = baseline[key];
    else el.value = baseline[key];
  }
  readError = false;
  showIdentity();
  fitText();
}
function errorCopy(key, message) {
  if (key === 'email') return t('emailInvalid');
  if (key === 'displayName') return t(message === 'Add a display name.' ? 'requiredName' : 'nameLength');
  return t(key + 'Length');
}
function renderErrors() {
  let changed = false;
  for (const [key,id] of Object.entries(ids)) {
    const el = document.getElementById(id), feedback = document.getElementById(key + '-error');
    if (!feedback) continue;
    const message = fieldErrors[key];
    if (el.classList.contains('is-invalid') !== Boolean(message)) changed = true;
    el.classList.toggle('is-invalid',Boolean(message));
    if (message) el.setAttribute('aria-invalid','true');
    else el.removeAttribute('aria-invalid');
    feedback.textContent = message ? errorCopy(key,message) : '';
  }
  if (changed) fitText();
}
function renderStatus() {
  let key = phase;
  if (readError) key = 'unreadable';
  else if (phase === 'pending' && !same(draft(),pendingSnapshot)) key = 'pendingNew';
  else if (phase === 'success' && dirty()) key = 'savedNew';
  else if (phase === 'idle' && dirty()) key = 'dirty';
  const color = {error:'danger',invalid:'danger',unreadable:'danger',success:'success',savedNew:'warning',pending:'info',pendingNew:'info'}[key];
  status.className = 'alert mb-3' + (color ? ' alert-' + color + ' text-' + color + '-emphasis' : '');
  status.textContent = t(key);
  status.dataset.state = phase;
  status.dataset.message = key;
  const pending = phase === 'pending';
  save.disabled = pending || readError;
  cancel.disabled = pending || readError;
  // Keep the inherited loading button's footprint while its label is hidden.
  if (!pending) save.textContent = t(phase === 'error' ? 'retry' : 'save');
  save.classList.toggle('btn-loading',pending);
  save.setAttribute('aria-label',pending ? t('saving') : save.textContent);
  save.setAttribute('aria-busy',String(pending));
}
function renderLanguage() {
  document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
  document.title = 'Fieldnotes — ' + t('accountSettings');
  document.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
  const language = document.querySelector('#language-toggle');
  language.textContent = lang === 'zh' ? 'English' : '中文';
  language.lang = lang === 'zh' ? 'en' : 'zh-CN';
  language.setAttribute('aria-label',lang === 'zh' ? 'English — 切换为英语' : '中文 — Switch to Chinese');
  document.querySelector('#settings-nav').setAttribute('aria-label',t('accountSettings'));
  document.querySelector('#theme-toggle').textContent = t(document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark');
  renderErrors(); renderStatus(); fitText();
}
subscribeSettings(event => {
  phase = event.status;
  if (event.status === 'invalid') {
    fieldErrors = event.fieldErrors;
    renderErrors(); renderStatus();
    document.getElementById(ids[Object.keys(fieldErrors)[0]]).focus();
    return;
  }
  if (event.status === 'pending') {
    pendingSnapshot = event.snapshot;
    pendingFocus = document.activeElement === save ? save : null;
    fieldErrors = {};
    renderErrors();
  }
  if (event.status === 'success') { baseline = event.settings; showIdentity(); }
  renderStatus();
  if (['success','error'].includes(event.status)) {
    if (pendingFocus && document.activeElement === document.body) pendingFocus.focus({preventScroll:true});
    pendingFocus = null;
  }
});
form.addEventListener('submit',async event => {
  event.preventDefault();
  if (phase === 'pending' || readError) return;
  try { await saveSettings(draft()); } catch { /* Store subscription renders the actual result. */ }
});
form.addEventListener('input',event => {
  const key = Object.keys(ids).find(key => ids[key] === event.target.id);
  if (!key) return;
  delete fieldErrors[key]; renderErrors();
  if (event.target.tagName === 'TEXTAREA') fitText([event.target]);
  if (!['pending','error'].includes(phase)) phase = Object.keys(fieldErrors).length ? 'invalid' : 'idle';
  renderStatus();
});
cancel.addEventListener('click',() => {
  if (phase === 'pending') return;
  try { load(); fieldErrors = {}; phase = 'restored'; renderErrors(); }
  catch { readError = true; }
  renderStatus();
});
document.querySelector('#language-toggle').addEventListener('click',() => {
  lang = lang === 'zh' ? 'en' : 'zh';
  const url = new URL(location.href); url.searchParams.set('lang',lang);
  history.replaceState({},'',url); renderLanguage();
});
document.querySelector('#theme-toggle').addEventListener('click',() => {
  const theme = document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-bs-theme',theme);
  try { localStorage.setItem('tabler-theme',theme); } catch { /* Theme remains usable in this tab. */ }
  const url = new URL(location.href); url.searchParams.set('theme',theme);
  history.replaceState({},'',url); renderLanguage();
});
document.querySelectorAll('#settings-nav a[href^="#"]').forEach(link => {
  link.addEventListener('click',event => {
    const href = link.getAttribute('href');
    if (href === '#') return;
    const target = document.querySelector(href);
    if (!target) return;
    event.preventDefault();
    document.querySelectorAll('#settings-nav a').forEach(item => {
      item.classList.toggle('active',item === link);
      if (item === link) item.setAttribute('aria-current','location');
      else item.removeAttribute('aria-current');
    });
    const url = new URL(location.href); url.hash = target.id; history.replaceState({},'',url);
    target.focus(); target.scrollIntoView({block:'start'});
  });
});
window.addEventListener('resize',() => fitText());
window.addEventListener('beforeunload',event => {
  if (dirty() || phase === 'pending') { event.preventDefault(); event.returnValue = ''; }
});
window.fieldnotes = { readSettings, saveSettings, setFailureMode, draft };
try { load(); } catch { readError = true; }
renderLanguage();

