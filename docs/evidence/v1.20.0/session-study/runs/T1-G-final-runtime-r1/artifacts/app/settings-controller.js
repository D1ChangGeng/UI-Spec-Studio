import { readSettings, saveSettings, subscribeSettings, setFailureMode, validateSettings } from './settings-store.js';

// Tabler owns visual treatments. This adapter owns draft, focus and localized feedback.
const ids = {displayName:'business-name', organization:'business-id', location:'location', email:'email', weeklyDigest:'weekly-digest', publicProfile:'public-profile'};
const fields = Object.fromEntries(Object.entries(ids).map(([key,id]) => [key, document.getElementById(id)]));
const form = document.getElementById('settings-form');
const status = document.getElementById('save-status');
const save = document.getElementById('save-settings');
const cancel = document.getElementById('cancel-settings');
const language = document.getElementById('language-toggle');
const theme = document.getElementById('theme-toggle');
let locale = new URLSearchParams(location.search).get('lang') === 'zh' ? 'zh' : 'en';
let persisted, phase = 'idle', pending = false, fieldErrors = {}, storageUnavailable = false, restoreSaveFocus = false;
const messages = {
 en: {
  accountSettings:'Account Settings', myAccount:'My Account', profileDetails:'Profile details', profileIntro:'Your identity in the research workspace.',
  displayName:'Display name', organization:'Organization', location:'Location', email:'Email', nameHelp:'Required · up to 100 characters', orgHelp:'Optional · up to 180 characters', locationHelp:'Optional · up to 100 characters', emailHelp:'Receives workspace notifications. Always private.',
  notifications:'Notifications', notificationHelp:'Receive a weekly digest of research notes shared with your workspace.', weeklyOn:'Weekly digest is enabled', weeklyOff:'Weekly digest is disabled',
  publicProfile:'Public profile', privacyHelp:'Allow other members of this research workspace to find your profile. Your email remains private.', publicOn:'Your profile will be visible', publicOff:'Your profile will be private',
  businessSettings:'Business settings', myNotifications:'My Notifications', privacy:'Privacy', plans:'Plans', billing:'Billing & Invoices', experience:'Experience', feedback:'Give Feedback', cancel:'Cancel', save:'Save changes', retry:'Try again', saving:'Saving…', dark:'Dark theme', light:'Light theme',
  idle:'Changes are saved only in this browser.', dirty:'You have unsaved changes. Save to apply them in this browser.', pending:'Saving submitted changes… You can keep editing.', success:'Changes saved in this browser.', successMore:'Submitted changes saved. Your newer edits still need saving.', error:'Save did not complete. Your draft is preserved. Try again.', invalid:'Check the highlighted fields, then save again.', restored:'Restored your last saved settings.', readError:'Saved settings could not be read. The stored value has been preserved; saving is unavailable.',
  'Add a display name.':'Add a display name.', 'Use 100 characters or fewer.':'Use 100 characters or fewer.', 'Use 180 characters or fewer.':'Use 180 characters or fewer.', 'Enter a complete email address.':'Enter a complete email address.'
 },
 zh: {
  accountSettings:'账户设置', myAccount:'我的账户', profileDetails:'个人资料', profileIntro:'你在研究工作区中的身份信息。',
  displayName:'显示名称', organization:'机构', location:'地点', email:'电子邮箱', nameHelp:'必填 · 最多 100 个字符', orgHelp:'选填 · 最多 180 个字符', locationHelp:'选填 · 最多 100 个字符', emailHelp:'用于接收工作区通知，始终保持私密。',
  notifications:'通知', notificationHelp:'每周接收工作区共享研究笔记的摘要。', weeklyOn:'已开启每周摘要', weeklyOff:'已关闭每周摘要',
  publicProfile:'公开个人资料', privacyHelp:'允许研究工作区的其他成员找到你的个人资料。电子邮箱仍为私密信息。', publicOn:'你的个人资料将公开', publicOff:'你的个人资料将保持私密',
  businessSettings:'工作设置', myNotifications:'我的通知', privacy:'隐私', plans:'套餐', billing:'账单与发票', experience:'使用体验', feedback:'提供反馈', cancel:'取消', save:'保存更改', retry:'重试', saving:'正在保存…', dark:'深色主题', light:'浅色主题',
  idle:'更改仅保存在当前浏览器中。', dirty:'有尚未保存的更改。保存后将在当前浏览器中生效。', pending:'正在保存已提交的更改… 你可以继续编辑。', success:'更改已保存到当前浏览器。', successMore:'已提交的更改已保存，之后的编辑仍需保存。', error:'保存未完成。草稿已保留，请重试。', invalid:'请检查标出的字段，然后重新保存。', restored:'已恢复上次保存的设置。', readError:'无法读取已保存的设置。原有数据已保留，暂时无法保存。',
  'Add a display name.':'请输入显示名称。', 'Use 100 characters or fewer.':'请使用不超过 100 个字符。', 'Use 180 characters or fewer.':'请使用不超过 180 个字符。', 'Enter a complete email address.':'请输入完整的电子邮箱地址。'
 }
};
const t = key => messages[locale][key] || key;
function draft() { return Object.fromEntries(Object.entries(fields).map(([key,el]) => [key, el.type === 'checkbox' ? el.checked : el.value])); }
function isDirty() { return !!persisted && Object.entries(draft()).some(([key,value]) => value !== persisted[key]); }
function load() {
 persisted = readSettings();
 for (const [key,el] of Object.entries(fields)) {
  if (el.type === 'checkbox') el.checked = persisted[key]; else el.value = persisted[key];
  if (el.tagName === 'TEXTAREA') window.tabler.Autosize.getOrCreateInstance(el).update();
 }
}
function renderErrors() {
 for (const [key,el] of Object.entries(fields)) {
  const feedback = document.getElementById(`${el.id}-error`);
  if (!feedback) continue;
  const message = fieldErrors[key];
  el.classList.toggle('is-invalid', !!message);
  if (message) el.setAttribute('aria-invalid','true'); else el.removeAttribute('aria-invalid');
  feedback.textContent = message ? t(message) : '';
  // Reuse the helper-text slot so validation does not displace the next control.
  el.parentElement.querySelectorAll('.form-hint').forEach(hint => hint.classList.toggle('d-none', !!message));
 }
}
function renderStatus() {
 let key = phase;
 if (phase === 'success' && isDirty()) key = 'successMore';
 if ((phase === 'idle' || phase === 'dirty') && isDirty()) key = 'dirty';
 if (phase === 'dirty' && !isDirty()) key = 'idle';
 const color = ['error','invalid','readError'].includes(phase) ? 'danger' : phase === 'success' ? 'success' : 'info';
 status.className = `alert alert-${color} mb-3 text-body`;
 status.dataset.state = phase;
 const message = t(key);
 if (status.textContent !== message) status.textContent = message;
 save.textContent = t(pending ? 'saving' : phase === 'error' ? 'retry' : 'save');
 save.disabled = pending || storageUnavailable;
 cancel.disabled = pending || storageUnavailable;
 save.setAttribute('aria-busy', String(pending));
}
function syncThemeLabel() { theme.textContent = t(document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark'); }
function translate() {
 document.documentElement.lang = locale === 'zh' ? 'zh-CN' : 'en';
 document.title = `Fieldnotes — ${t('accountSettings')}`;
 document.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
 document.querySelectorAll('[data-settings-nav]').forEach((el,i) => el.setAttribute('aria-label',t(i === 0 ? 'businessSettings' : 'experience')));
 language.textContent = locale === 'en' ? '中文' : 'English';
 language.lang = locale === 'en' ? 'zh-CN' : 'en';
 syncThemeLabel(); renderErrors(); renderStatus();
}
try { load(); } catch { storageUnavailable = true; phase = 'readError'; }
subscribeSettings(event => {
 if (event.status === 'pending') restoreSaveFocus = document.activeElement === save;
 phase = event.status;
 pending = event.status === 'pending';
 if (event.status === 'invalid') {
  fieldErrors = {...event.fieldErrors}; renderErrors();
  const first = Object.keys(ids).find(key => fieldErrors[key]);
  if (first) fields[first].focus();
 } else if (event.status === 'pending') { fieldErrors = {}; renderErrors(); }
 else if (event.status === 'success') { persisted = {...event.settings}; }
 renderStatus();
 if (event.status === 'success' || event.status === 'error') {
  // Restore only abandoned button focus; never steal focus from continued editing.
  if (restoreSaveFocus && document.activeElement === document.body) save.focus({preventScroll:true});
  restoreSaveFocus = false;
 }
});
form.addEventListener('submit', async event => {
 event.preventDefault();
 if (pending || storageUnavailable) return;
 try { await saveSettings(draft()); } catch { /* Store events own every result. */ }
});
for (const [key,el] of Object.entries(fields)) {
 el.addEventListener('input', () => {
  if (fieldErrors[key]) { delete fieldErrors[key]; renderErrors(); }
  if (!pending && !['error','readError'].includes(phase)) phase = Object.keys(fieldErrors).length ? 'invalid' : 'dirty';
  renderStatus();
 });
 el.addEventListener('blur', event => {
  // Submit/restore owns this transition; avoid moving its target between pointer down/up.
  if ([save, cancel].includes(event.relatedTarget) || el.type === 'checkbox' || pending || storageUnavailable) return;
  const error = validateSettings(draft())[key];
  if (error) fieldErrors[key] = error; else delete fieldErrors[key];
  renderErrors();
 });
}
cancel.addEventListener('click', () => {
 if (pending || storageUnavailable) return;
 try { load(); fieldErrors = {}; phase = 'restored'; renderErrors(); renderStatus(); }
 catch { storageUnavailable = true; phase = 'readError'; renderStatus(); }
});
language.addEventListener('click', () => {
 locale = locale === 'zh' ? 'en' : 'zh';
 const url = new URL(location.href); url.searchParams.set('lang',locale); history.replaceState(null,'',url);
 translate();
});
theme.addEventListener('click', () => {
 const next = document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
 document.documentElement.setAttribute('data-bs-theme',next);
 try { localStorage.setItem('tabler-theme',next); } catch { /* Theme remains usable without storage. */ }
 const url = new URL(location.href); url.searchParams.set('theme',next); history.replaceState(null,'',url);
 syncThemeLabel();
});
// Other upstream theme affordances may also update the shared theme.
new MutationObserver(syncThemeLabel).observe(document.documentElement,{attributes:true,attributeFilter:['data-bs-theme']});
document.querySelectorAll('[data-settings-nav] a[href^="#"]').forEach(link => {
 const target = document.querySelector(link.getAttribute('href') === '#' ? '#nonexistent' : link.getAttribute('href'));
 if (!target) return;
 link.addEventListener('click', () => {
  document.querySelectorAll('[data-settings-nav] a').forEach(item => { item.classList.remove('active'); item.removeAttribute('aria-current'); });
  link.classList.add('active'); link.setAttribute('aria-current','location');
  target.focus();
 });
});
window.fieldnotes = {readSettings, saveSettings, setFailureMode, draft};
translate();
