// Authoritative browser-local application state. UI code subscribes to events.
export const STORAGE_KEY = 'fieldnotes-settings-v1';
export const INITIAL_SETTINGS = Object.freeze({
  displayName: 'Mei Lin · 林玫',
  organization: 'Fieldnotes Research / 城市日常研究小组',
  location: 'Singapore / 新加坡',
  email: 'mei.lin@example.invalid',
  weeklyDigest: true,
  publicProfile: false,
});
let failNext = new URLSearchParams(location.search).get('fail') === 'once';
const bus = new EventTarget();
let sequence = 0;
function emit(detail) { bus.dispatchEvent(new CustomEvent('change', {detail})); }
export function subscribeSettings(listener) {
  const handler = event => listener(event.detail);
  bus.addEventListener('change',handler);
  return () => bus.removeEventListener('change',handler);
}
export function readSettings() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return {...INITIAL_SETTINGS};
  const parsed = JSON.parse(raw);
  if (parsed.schemaVersion !== 1 || !parsed.settings) throw new Error('Stored settings are unreadable. Your existing value has been preserved.');
  return {...INITIAL_SETTINGS, ...parsed.settings};
}
export function validateSettings(draft) {
  const errors = {};
  if (!String(draft.displayName || '').trim()) errors.displayName = 'Add a display name.';
  if (String(draft.displayName || '').length > 100) errors.displayName = 'Use 100 characters or fewer.';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(draft.email || ''))) errors.email = 'Enter a complete email address.';
  if (String(draft.organization || '').length > 180) errors.organization = 'Use 180 characters or fewer.';
  if (String(draft.location || '').length > 100) errors.location = 'Use 100 characters or fewer.';
  return errors;
}
export function setFailureMode(value = true) { failNext = Boolean(value); }
export async function saveSettings(draft) {
  const errors = validateSettings(draft);
  const operationId = ++sequence;
  if (Object.keys(errors).length) {
    const error = Object.assign(new Error('Check the profile fields.'), {fieldErrors: errors, code:'validation'});
    emit({status:'invalid', operationId, fieldErrors:errors, draft:{...draft}, error});
    throw error;
  }
  const snapshot = {...INITIAL_SETTINGS, ...draft};
  emit({status:'pending', operationId, snapshot});
  await new Promise(resolve => setTimeout(resolve, 750));
  try {
    if (failNext) { failNext = false; throw new Error('The local save failed once. Your draft is still available.'); }
    const savedAt = new Date().toISOString();
    localStorage.setItem(STORAGE_KEY, JSON.stringify({schemaVersion:1, settings:snapshot, savedAt}));
    const result = {settings:snapshot, savedAt, operationId};
    emit({status:'success', ...result});
    return result;
  } catch (error) {
    emit({status:'error', operationId, snapshot, error});
    throw error;
  }
}
