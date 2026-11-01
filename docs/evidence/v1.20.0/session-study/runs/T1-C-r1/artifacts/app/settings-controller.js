import { readSettings, saveSettings, validateSettings, subscribeSettings, setFailureMode } from './settings-store.js';

// All mutations and validation remain owned by settings-store.js.
const ids = {displayName:'business-name', organization:'business-id', location:'location', email:'email', weeklyDigest:'weekly-digest', publicProfile:'public-profile'};
const errorsByField = {displayName:'name-error', organization:'organization-error', location:'location-error', email:'email-error'};
const form = document.querySelector('#settings-form');
const status = document.querySelector('#save-status');
const save = document.querySelector('#save-settings');
const cancel = document.querySelector('#cancel-settings');
const params = new URLSearchParams(location.search);
let locale = params.get('lang') === 'zh' ? 'zh' : 'en';
let persisted;
let pending = false;
let restoreSaveFocus = false;
let readFailed = false;
let state = 'idle';
let fieldErrors = {};
const copy = {
  en: {
    accountSettings:'Account settings', sections:'Settings sections', businessSettings:'Business settings', myAccount:'My account', myNotifications:'My notifications', privacy:'Privacy', plans:'Plans', billing:'Billing & invoices', experience:'Experience', feedback:'Give feedback',
    localHint:'Settings are saved only in this browser.', profileDetails:'Profile details', displayName:'Display name', nameHint:'Required · up to 100 characters', organization:'Organization', organizationHint:'Optional · up to 180 characters', location:'Location', locationHint:'Optional · up to 100 characters', email:'Email', emailHint:'Receives workspace notifications. Always private.', notifications:'Notifications', digestHint:'Receive a weekly digest of research notes shared with your workspace.', weeklyDigest:'Weekly digest', privacyHint:'Let members of this research workspace find your profile. Your email stays private.', publicProfile:'Public profile', cancel:'Cancel', save:'Save changes', retry:'Retry save', saving:'Saving…', dark:'Use dark theme', light:'Use light theme',
    idle:'No unsaved changes.', dirty:'You have unsaved changes.', pending:'Saving submitted changes… You can keep editing.', success:'Changes saved in this browser.', savedNewer:'Submitted changes saved. Your newer edits still need saving.', error:'Save did not complete. Your draft is preserved. Choose Retry save.', invalid:'Check the highlighted fields, then save again.', cancelled:'Last saved settings restored.', readError:'Saved settings could not be read. Existing browser data has been preserved.',
    'Add a display name.':'Add a display name.', 'Use 100 characters or fewer.':'Use 100 characters or fewer.', 'Use 180 characters or fewer.':'Use 180 characters or fewer.', 'Enter a complete email address.':'Enter a complete email address.'
  },
  zh: {
    accountSettings:'账户设置', sections:'设置导航', businessSettings:'工作设置', myAccount:'我的账户', myNotifications:'我的通知', privacy:'隐私', plans:'方案', billing:'账单与发票', experience:'使用体验', feedback:'提供反馈',
    localHint:'设置仅保存在当前浏览器中。', profileDetails:'个人资料', displayName:'显示名称', nameHint:'必填 · 最多 100 个字符', organization:'机构', organizationHint:'选填 · 最多 180 个字符', location:'地点', locationHint:'选填 · 最多 100 个字符', email:'电子邮箱', emailHint:'用于接收工作区通知，始终保持私密。', notifications:'通知', digestHint:'每周接收工作区共享研究笔记的摘要。', weeklyDigest:'每周摘要', privacyHint:'允许研究工作区的成员找到你的个人资料。电子邮箱始终保持私密。', publicProfile:'公开个人资料', cancel:'取消', save:'保存更改', retry:'重试保存', saving:'正在保存…', dark:'使用深色主题', light:'使用浅色主题',
    idle:'没有未保存的更改。', dirty:'有未保存的更改。', pending:'正在保存已提交的更改…你可以继续编辑。', success:'更改已保存到当前浏览器。', savedNewer:'已提交的更改已保存。之后的编辑仍需保存。', error:'保存未完成。草稿仍然保留，请选择“重试保存”。', invalid:'请检查标出的字段，然后重新保存。', cancelled:'已恢复上次保存的设置。', readError:'无法读取已保存的设置。浏览器中的原有数据已保留。',
    'Add a display name.':'请填写显示名称。', 'Use 100 characters or fewer.':'请使用 100 个或更少的字符。', 'Use 180 characters or fewer.':'请使用 180 个或更少的字符。', 'Enter a complete email address.':'请输入完整的电子邮箱地址。'
  }
};
const t = key => copy[locale][key] || key;
function draft() {
  return Object.fromEntries(Object.entries(ids).map(([key,id]) => {
    const el = document.getElementById(id);
    return [key, el.type === 'checkbox' ? el.checked : el.value];
  }));
}
function differs(a,b) { return !b || Object.keys(ids).some(key => a[key] !== b[key]); }
function fitTextareas() {
  // Preserve the Tabler control skin; adapt only its height to the actual text.
  for (const el of form.querySelectorAll('[data-autogrow]')) {
    el.style.height = 'auto';
    const css = getComputedStyle(el);
    el.style.height = `${el.scrollHeight + parseFloat(css.borderTopWidth) + parseFloat(css.borderBottomWidth)}px`;
  }
}
function populate(data) {
  for (const [key,id] of Object.entries(ids)) {
    const el = document.getElementById(id);
    if (el.type === 'checkbox') el.checked = data[key]; else el.value = data[key];
  }
  fitTextareas();
}
function renderErrors() {
  for (const [key,errorId] of Object.entries(errorsByField)) {
    const control = document.getElementById(ids[key]);
    const message = fieldErrors[key];
    control.classList.toggle('is-invalid', Boolean(message));
    if (message) control.setAttribute('aria-invalid','true'); else control.removeAttribute('aria-invalid');
    document.getElementById(errorId).textContent = message ? t(message) : '';
  }
}
function renderStatus() {
  const text = t(state);
  if (status.textContent !== text) status.textContent = text;
  status.dataset.state = state;
  const color = ['invalid','error','readError'].includes(state) ? 'danger' : ['success','cancelled','savedNewer'].includes(state) ? 'success' : 'info';
  status.className = `alert alert-minor alert-${color} text-${color}-emphasis mb-3`;
  save.disabled = pending || readFailed;
  cancel.disabled = pending || readFailed;
  save.setAttribute('aria-busy', String(pending));
  save.classList.toggle('btn-loading', pending);
  save.textContent = t(pending ? 'saving' : state === 'error' ? 'retry' : 'save');
}
function themeLabel() {
  const dark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
  document.querySelector('#theme-toggle').textContent = t(dark ? 'light' : 'dark');
}
function renderLocale() {
  document.documentElement.lang = locale === 'zh' ? 'zh-CN' : 'en';
  document.title = `Fieldnotes — ${t('accountSettings')}`;
  for (const el of document.querySelectorAll('[data-i18n]')) el.textContent = t(el.dataset.i18n);
  for (const el of document.querySelectorAll('[data-i18n-aria]')) el.setAttribute('aria-label', t(el.dataset.i18nAria));
  const language = document.querySelector('#language-toggle');
  language.textContent = locale === 'zh' ? 'English' : '中文';
  language.lang = locale === 'zh' ? 'en' : 'zh-CN';
  language.setAttribute('aria-label',locale === 'zh' ? 'Switch to English' : '切换到中文');
  themeLabel(); renderErrors(); renderStatus(); fitTextareas();
}
try { persisted = readSettings(); populate(persisted); }
catch { readFailed = true; state = 'readError'; }
renderLocale();

subscribeSettings(event => {
  if (event.status === 'pending') restoreSaveFocus = document.activeElement === save;
  pending = event.status === 'pending';
  if (event.status === 'invalid') {
    fieldErrors = {...event.fieldErrors}; state = 'invalid'; renderErrors();
    const first = Object.keys(ids).find(key => fieldErrors[key]);
    if (first) {
      const control = document.getElementById(ids[first]);
      control.focus({preventScroll:true});
      control.scrollIntoView({block:'center', behavior:'instant'});
    }
  } else if (event.status === 'pending') {
    fieldErrors = {}; renderErrors(); state = 'pending';
  } else if (event.status === 'success') {
    persisted = {...event.settings};
    // Never replace edits made after submission with the completed snapshot.
    state = differs(draft(), persisted) ? 'savedNewer' : 'success';
  } else state = 'error';
  renderStatus();
  if (!pending && restoreSaveFocus && document.activeElement === document.body) save.focus({preventScroll:true});
  if (!pending) restoreSaveFocus = false;
});
form.addEventListener('submit', async event => {
  event.preventDefault();
  if (pending || readFailed) return;
  try { await saveSettings(draft()); } catch { /* The authoritative event renders recovery. */ }
});
form.addEventListener('input', event => {
  const key = Object.keys(ids).find(key => ids[key] === event.target.id);
  if (!key) return;
  if (fieldErrors[key]) { delete fieldErrors[key]; renderErrors(); }
  if (!pending && !readFailed && state !== 'error') state = Object.keys(fieldErrors).length ? 'invalid' : differs(draft(),persisted) ? 'dirty' : 'idle';
  renderStatus(); fitTextareas();
});
// Use authoritative rules after leaving an edited field; no premature errors on entry.
form.addEventListener('focusout', event => {
  const key = Object.keys(errorsByField).find(key => ids[key] === event.target.id);
  // A blur that begins a button activation must not move its pointer target.
  if (!key || readFailed || event.relatedTarget?.closest('button') || event.target.value === persisted?.[key]) return;
  const message = validateSettings(draft())[key];
  if (message) fieldErrors[key] = message; else delete fieldErrors[key];
  renderErrors();
});
cancel.addEventListener('click', () => {
  if (pending) return;
  try { persisted = readSettings(); populate(persisted); fieldErrors = {}; state = 'cancelled'; renderErrors(); renderStatus(); }
  catch { readFailed = true; state = 'readError'; renderStatus(); }
});
document.querySelector('#language-toggle').addEventListener('click', () => {
  locale = locale === 'zh' ? 'en' : 'zh'; params.set('lang',locale);
  history.replaceState(null,'',`${location.pathname}?${params}${location.hash}`);
  renderLocale();
});
document.querySelector('#theme-toggle').addEventListener('click', () => {
  const theme = document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-bs-theme',theme);
  localStorage.setItem('tabler-theme',theme); params.set('theme',theme);
  history.replaceState(null,'',`${location.pathname}?${params}${location.hash}`);
  themeLabel();
});
for (const link of document.querySelectorAll('#settings-section-nav a[href^="#"]:not([href="#"])')) {
  link.addEventListener('click', event => {
    event.preventDefault();
    for (const sibling of document.querySelectorAll('#settings-section-nav a')) {
      sibling.classList.toggle('active',sibling === link);
      if (sibling === link) sibling.setAttribute('aria-current','location'); else sibling.removeAttribute('aria-current');
    }
    history.replaceState(null,'',link.hash);
    const toggle = document.querySelector('#settings-nav-toggle');
    const heading = document.querySelector(link.hash);
    if (getComputedStyle(toggle).display !== 'none' && toggle.getAttribute('aria-expanded') === 'true') {
      const panel = document.querySelector('#settings-nav-panel');
      const hide = () => window.tabler.bootstrap.Collapse.getOrCreateInstance(panel).hide();
      // Collapse ignores methods mid-transition; queue a fast section selection.
      if (panel.classList.contains('collapsing')) panel.addEventListener('shown.bs.collapse',hide,{once:true});
      else hide();
      panel.addEventListener('hidden.bs.collapse',() => {
        if (document.activeElement === heading) heading.scrollIntoView({block:'start',behavior:'instant'});
      },{once:true});
    }
    heading.focus();
  });
}
window.addEventListener('resize', fitTextareas);
document.fonts.ready.then(fitTextareas);
window.fieldnotes = { readSettings, saveSettings, setFailureMode, draft };
