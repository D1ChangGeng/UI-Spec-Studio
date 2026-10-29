/* Authored temporal fixture. Animation follows local intent; saved text follows Storage. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const root = document.documentElement;
  const KEY = 'ui-spec-temporal-note-v1';
  const COPY = {
    en: {skip:'Skip to note',savedNotes:'Saved note',eyebrow:'Research / Local demo',pageTitle:'Keep an idea in view',subject:'Energy / Cities',question:'How can cities reduce peak heating demand?',context:'Working context',draftBoundary:'Preview of your current note',showContext:'See context',showFront:'Back to question',pause:'Pause decoration',resume:'Resume decoration',quiet:'Decoration paused',noteLabel:'Your research note',noteHint:'Keep evidence and open questions together.',save:'Save note',localOnly:'Only in this browser',return:'Return to editing',disclosure:'Interactive local demo. The save includes a 900 ms preview delay.',controls:'Preview controls',clear:'Clear local demo data',saving:'Saving in this browser…',saved:'Note saved in this browser.',earlier:'The submitted version is saved. Save again to keep your new edits.',edited:'Your changes have not been saved.',failed:'The note could not be saved. Your text is still here.',retrySave:'Try saving again',unavailable:'Saved data could not be read. Clear demo data or try reading again before saving.',retryRead:'Try reading again',clearFailed:'Demo data could not be cleared. Your text is still here.',retryClear:'Try clearing again',cleared:'Local demo data cleared.',empty:'No saved note yet',emptyHint:'Save your note, then return here to read it.',read:'Saved data is available again.',dark:'Switch to dark theme',light:'Switch to light theme',preview:'Note preview',edit:'Edit note',lengthCount:'{count} / 600 characters',lengthExceeded:'{count} / 600 characters. Shorten the note to save.',tooLong:'Shorten the note to 600 characters before saving. Your text is still here.',pendingLabel:'Save in progress',savingNewer:'Saving a newer version. The previous saved note remains visible.',failedExisting:'The newer version could not be saved. The previous saved note is unchanged. Return to editing to retry.',notSaved:'Note not saved',returnToRetry:'Return to editing to try again. Your text remains in the editor.',unknownTitle:'Saved note unavailable',unknownHint:'The saved note could not be read. Return to editing to retry or clear the demo data. Your current text remains available.'},
    zh: {skip:'跳到笔记',savedNotes:'已存笔记',eyebrow:'研究 / 本地演示',pageTitle:'让研究线索清晰可见',subject:'能源 / 城市',question:'城市如何降低高峰供热需求？',context:'研究背景',draftBoundary:'当前笔记的预览',showContext:'查看背景',showFront:'返回问题',pause:'暂停装饰动效',resume:'继续装饰动效',quiet:'装饰动效已暂停',noteLabel:'研究笔记',noteHint:'把已有证据和待解问题放在一起',save:'保存笔记',localOnly:'仅保存在此浏览器',return:'返回编辑',disclosure:'本地交互演示，保存过程含 900 毫秒预览延迟。',controls:'预览设置',clear:'清除本地演示数据',saving:'正在保存到此浏览器…',saved:'笔记已保存在此浏览器。',earlier:'提交的版本已保存。当前修改仍需再次保存。',edited:'当前修改尚未保存。',failed:'未能保存笔记。输入内容仍在页面中。',retrySave:'重试保存',unavailable:'暂时无法读取已存数据。请清除演示数据或重试读取后再保存。',retryRead:'重试读取',clearFailed:'未能清除演示数据。输入内容仍在页面中。',retryClear:'重试清除',cleared:'本地演示数据已清除。',empty:'还没有已存笔记',emptyHint:'保存笔记后，可回到这里查看',read:'已重新读取本地数据。',dark:'切换深色主题',light:'切换浅色主题',preview:'笔记预览',edit:'编辑笔记',lengthCount:'{count} / 600 字',lengthExceeded:'已输入 {count} 字，最多 600 字。请缩短后再保存。',tooLong:'请缩短至 600 字以内再保存。当前输入仍在页面中。',pendingLabel:'正在保存',savingNewer:'正在保存新版本，下面仍显示上一次保存的内容。',failedExisting:'未能保存新版本，之前保存的内容仍保留。请返回编辑重试。',notSaved:'笔记尚未保存',returnToRetry:'请返回编辑重试。输入内容仍保留在编辑区。',unknownTitle:'暂时无法读取已存笔记',unknownHint:'请返回编辑重试读取，或在预览设置中清除演示数据。当前输入仍保留在编辑区。'}
  };
  let locale = 'en', face = 'front', status = '', pending = null;
  let saved = null, storageReady = false, touched = false, paused = false;
  let hiddenOrbitTime = null;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const t = key => COPY[locale][key];
  $('note-text').value = 'Compare city demand patterns and check which evidence supports each explanation.';

  function announce(next) {
    status = next;
    const retryFocused = document.activeElement === $('retry');
    const actions = {failed:'retrySave',unavailable:'retryRead',clearFailed:'retryClear'};
    $('status').textContent = next ? t(next) : '';
    $('status-area').dataset.status = next;
    $('retry').hidden = !actions[next];
    if (actions[next]) $('retry').textContent = t(actions[next]);
    if (retryFocused && $('retry').hidden) $('note-text').focus();
    $('save').disabled = pending !== null || !storageReady || $('note-text').value.length > 600;
    $('save').setAttribute('aria-busy', String(pending !== null));
    collection();
  }
  function preview() {
    const text = $('note-text').value;
    $('preview-note').textContent = text || t('emptyHint');
    const over = text.length > 600;
    $('note-limit').textContent = t(over ? 'lengthExceeded' : 'lengthCount').replace('{count}', text.length);
    $('note-limit').dataset.overLimit = String(over);
    $('note-text').setAttribute('aria-invalid', String(over));
    $('save').disabled = pending !== null || !storageReady || over;
  }
  function collection() {
    const record = saved || pending?.record;
    $('saved-kicker').textContent = storageReady && !saved && pending ? t('pendingLabel') : t('localOnly');
    $('saved-title').textContent = !storageReady ? t('unknownTitle') : record ? record.title : t(status === 'failed' ? 'notSaved' : 'empty');
    $('saved-text').textContent = !storageReady ? t('unknownHint') : record ? record.text : t(status === 'failed' ? 'returnToRetry' : 'emptyHint');
    const message = !storageReady ? '' : pending ? t(saved ? 'savingNewer' : 'saving')
      : status === 'failed' && saved ? t('failedExisting') : status ? t(status) : '';
    $('collection-status').textContent = message;
    $('collection-status').dataset.status = status;
  }
  function read(initial=false) {
    try {
      const raw = localStorage.getItem(KEY);
      const value = raw === null ? null : JSON.parse(raw);
      if (value !== null && (!value || value.id !== 'heating-study' || typeof value.title !== 'string' || typeof value.text !== 'string' || value.text.length > 600)) throw new Error('Invalid saved record');
      saved = value;
      storageReady = true;
      if (value && !touched) $('note-text').value = value.text;
      if (!initial) announce('read');
    } catch (_) {
      storageReady = false;
      announce('unavailable');
    }
    preview(); collection(); announce(status);
  }
  function motion() {
    root.classList.toggle('is-paused', paused || reduced.matches || document.hidden || !$('collection').hidden);
    $('motion-toggle').textContent = t(reduced.matches ? 'quiet' : paused ? 'resume' : 'pause');
    $('motion-toggle').setAttribute('aria-pressed', String(paused || reduced.matches));
    $('motion-toggle').disabled = reduced.matches;
  }
  function setFace(next) {
    face = next;
    $('note-card').dataset.face = face;
    $('card-front').inert = face !== 'front';
    $('card-back').inert = face !== 'back';
    $('card-front').setAttribute('aria-hidden', String(face !== 'front'));
    $('card-back').setAttribute('aria-hidden', String(face !== 'back'));
    $('flip').setAttribute('aria-pressed', String(face === 'back'));
    $('flip').textContent = t(face === 'front' ? 'showContext' : 'showFront');
  }
  function renderLocale() {
    root.lang = locale === 'zh' ? 'zh-CN' : 'en';
    document.title = locale === 'zh' ? 'Study · 笔记预览' : 'Study · Note preview';
    document.querySelectorAll('[data-i18n]').forEach(e => {e.textContent = t(e.dataset.i18n);});
    $('locale-toggle').textContent = locale === 'en' ? '中文' : 'EN';
    $('locale-toggle').setAttribute('aria-label', locale === 'en' ? '中文 · 切换中文' : 'EN · Switch to English');
    $('locale-toggle').lang = locale === 'en' ? 'zh-CN' : 'en';
    $('theme-toggle').setAttribute('aria-label', t(root.dataset.theme === 'dark' ? 'light' : 'dark'));
    document.querySelector('.preview').setAttribute('aria-label', t('preview'));
    document.querySelector('.editor-fields').setAttribute('aria-label', t('edit'));
    $('note-card').setAttribute('aria-label', t('question'));
    setFace(face); preview(); collection(); motion(); announce(status);
  }
  function save() {
    if (pending !== null || !storageReady) return;
    if ($('note-text').value.length > 600) {announce('tooLong'); $('note-text').focus(); return;}
    const record = {id:'heating-study',title:t('question'),text:$('note-text').value};
    const attempt = {record,timer:null};
    pending = attempt;
    announce('saving');
    attempt.timer = setTimeout(() => {
      if (pending !== attempt) return;
      try {
        localStorage.setItem(KEY, JSON.stringify(record));
        saved = record;
        pending = null;
        announce($('note-text').value === record.text ? 'saved' : 'earlier');
        collection();
      } catch (_) {
        pending = null;
        announce('failed');
      }
    }, 900);
  }
  function clear() {
    if (pending) clearTimeout(pending.timer);
    pending = null;
    try {
      localStorage.removeItem(KEY);
      saved = null; storageReady = true; touched = false;
      $('note-text').value = '';
      announce('cleared');
    } catch (_) {
      announce('clearFailed');
      if (!$('collection').hidden) {
        showCollection(false);
        $('retry').focus();
      }
    }
    preview(); collection();
  }
  function showCollection(open) {
    const orbit = document.querySelector('.orbit-arm');
    if (open && $('collection').hidden) {
      hiddenOrbitTime = orbit.getAnimations()[0]?.currentTime ?? null;
    }
    $('collection').hidden = !open;
    $('editor').hidden = open;
    motion();
    // A display:none ancestor recreates its CSS animation. Resume at the phase
    // the user left, including a deliberately paused decoration.
    if (!open && hiddenOrbitTime !== null) {
      const animation = orbit.getAnimations()[0];
      if (animation) animation.currentTime = hiddenOrbitTime;
      hiddenOrbitTime = null;
    }
    if (open) {collection(); $('collection-title').focus();}
    else if (!$('retry').hidden) $('retry').focus();
    else $('note-text').focus();
  }
  $('flip').addEventListener('click', () => setFace(face === 'front' ? 'back' : 'front'));
  $('motion-toggle').addEventListener('click', () => {paused = !paused; motion();});
  $('note-text').addEventListener('input', () => {
    touched = true; preview();
    if (!pending && storageReady && !['failed','clearFailed'].includes(status)) announce('edited');
  });
  $('save').addEventListener('click', save);
  $('retry').addEventListener('click', () => {
    if (status === 'failed') save(); else if (status === 'unavailable') read(); else if (status === 'clearFailed') clear();
  });
  $('clear').addEventListener('click', clear);
  $('saved-link').addEventListener('click', () => showCollection(true));
  $('return').addEventListener('click', () => showCollection(false));
  document.querySelector('.brand').addEventListener('click', event => {event.preventDefault(); showCollection(false);});
  $('locale-toggle').addEventListener('click', () => {locale = locale === 'en' ? 'zh' : 'en'; renderLocale();});
  $('theme-toggle').addEventListener('click', () => {root.dataset.theme = root.dataset.theme === 'light' ? 'dark' : 'light'; renderLocale();});
  document.addEventListener('visibilitychange', motion);
  reduced.addEventListener('change', motion);
  read(true); renderLocale();
})();
