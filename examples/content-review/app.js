/* A content-design fixture with real browser-local writes and source-owned messages. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const root = document.documentElement;
  const KEY = 'ui-spec-content-note-v1';
  let locale = 'zh';
  let status = '';
  let pending = null;
  let savedRecord = null;
  let storageState = 'unknown';
  let draftEdited = false;
  let draftTouched = false;
  let retryAction = null;
  const copy = {
    zh: {
      brandSubtitle:'研究笔记',eyebrow:'研究空间 / 笔记',scope:'本地演示',step:'记录想法',pageTitle:'把研究线索整理成笔记',pageIntro:'先记下问题和背景，再回来继续完善。',titleLabel:'笔记标题',titleHint:'用一句话写清想研究的问题',titlePlaceholder:'例如：城市供热如何降低高峰负荷？',bodyLabel:'背景与线索',optional:'选填',bodyHint:'补充已有材料、疑问或仍需核查的判断',bodyPlaceholder:'记下材料、想法或需要验证的线索…',save:'保存笔记',saving:'正在保存到此浏览器…',saved:'笔记已保存在此浏览器。',savedEarlier:'上一版已保存。当前修改仍需再次保存。',edited:'当前修改尚未保存。',missing:'填写笔记标题后再保存。',failed:'当前无法保存这份笔记。输入内容仍在页面中。',retry:'重试保存',storage:'仅保存在当前浏览器',asideStep:'继续研究',asideTitle:'最近保存',asideIntro:'已保存的笔记会显示在这里，便于继续编辑。',recentEmpty:'还没有保存的笔记',recentEmptyHint:'保存后可在此查看',recentSaved:'已保存 · 当前浏览器',disclosure:'这是交互演示。笔记会保存在此浏览器中，不会发送到外部服务。',previewSettings:'预览状态设置',failureSwitch:'模拟写入失败',slowSwitch:'延迟写入 1 秒',loadLong:'填写较长标题',reset:'清除本地演示数据',fixtureLabel:'内容与交互状态实例 · 本地运行',langButton:'EN',langAria:'EN · Switch to English',themeDark:'切换深色主题',themeLight:'切换浅色主题',resetDone:'本地演示数据已清除。',clearFailed:'未能清除本地演示数据。当前输入仍在页面中，请重试。',clearRetry:'重试清除',readFailed:'暂时无法读取已保存的笔记。当前输入仍在页面中，请重试读取后再保存。',invalidStored:'已保存的笔记数据无法识别。请在预览设置中清除本地演示数据后再保存。',readRetry:'重试读取',readRecovered:'已重新读取本地笔记。',readRecoveredEmpty:'本地存储已恢复，尚无已保存的笔记。',readRecoveredEmptyDraft:'本地存储已恢复。当前输入尚未保存。',readRecoveredDraft:'已重新读取本地笔记。当前输入仍在页面中，保存后会替换已存内容。',recentUnreadable:'暂时无法读取笔记',recentUnreadableHint:'重试读取后可确认已保存的内容',longTitle:'比较不同城市在能源供应高峰期间如何调节供热需求，并梳理可供进一步核查的具体研究证据',htmlTitle:'研究笔记 · 内容设计实例',skip:'跳到主要内容'
    },
    en: {
      brandSubtitle:'Research notes',eyebrow:'Research / Notes',scope:'Local demo',step:'Capture an idea',pageTitle:'Turn a research lead into a note',pageIntro:'Start with the question and its context. Return to the same note as your research develops.',titleLabel:'Note title',titleHint:'Name the question you want to investigate',titlePlaceholder:'For example: Reducing peak demand',bodyLabel:'Context and leads',optional:'Optional',bodyHint:'Add sources, open questions, or assumptions to check',bodyPlaceholder:'Capture the source material or questions to verify…',save:'Save note',saving:'Saving in this browser…',saved:'Note saved in this browser.',savedEarlier:'An earlier version was saved. Save again to keep your new edits.',edited:'You have unsaved changes.',missing:'Add a note title before saving.',failed:'This note could not be saved. Your text is still here.',retry:'Try saving again',storage:'Saved only in this browser',asideStep:'Continue your work',asideTitle:'Recently saved',asideIntro:'Saved notes appear here so you can return to your work.',recentEmpty:'No notes saved yet',recentEmptyHint:'Your note will appear after saving',recentSaved:'Saved · This browser',disclosure:'This is an interactive demo. Notes stay in this browser and are not sent to an external service.',previewSettings:'Preview state controls',failureSwitch:'Simulate a write failure',slowSwitch:'Delay the write by 1 second',loadLong:'Use a longer example title',reset:'Clear local demo data',fixtureLabel:'Content and state example · Local demo',langButton:'中文',langAria:'切换到中文',themeDark:'Switch to dark theme',themeLight:'Switch to light theme',resetDone:'Local demo data cleared.',clearFailed:'Local demo data could not be cleared. Your text is still here. Try again.',clearRetry:'Try clearing again',readFailed:'Saved notes could not be read. Your text is still here. Try reading again before saving.',invalidStored:'The saved note data is not readable. Clear local demo data in the preview controls before saving.',readRetry:'Try reading again',readRecovered:'The local note has been read again.',readRecoveredEmpty:'Local storage is available again. No notes have been saved.',readRecoveredEmptyDraft:'Local storage is available again. Your current text has not been saved.',readRecoveredDraft:'The local note has been read again. Your current text is still here. Saving will replace the stored note.',recentUnreadable:'Saved note unavailable',recentUnreadableHint:'Try reading again to check the saved content',longTitle:'Compare how different cities manage district-heating demand during peak energy use and identify which evidence needs to be verified',htmlTitle:'Research notes · Content design example',skip:'Skip to main content'
    }
  };
  function t(name) { return copy[locale][name]; }

  function updateControls() {
    $('save').disabled = pending !== null || storageState !== 'ready';
    $('save').setAttribute('aria-busy', String(pending !== null));
  }

  function showStatus(next) {
    status = next;
    const retry = $('retry');
    const retryHadFocus = document.activeElement === retry;
    const actions = {failed:'save', readFailed:'read', invalidStored:'read', clearFailed:'clear'};
    retryAction = actions[next] || null;
    $('state-message').textContent = next ? t(next) : '';
    $('state-message').parentElement.dataset.status = retryAction ? 'error' : next;
    retry.hidden = retryAction === null;
    const labels = {save:'retry', read:'readRetry', clear:'clearRetry'};
    if (retryAction) retry.textContent = t(labels[retryAction]);
    // A disappearing recovery control must leave focus on a usable task element.
    if (retryHadFocus && retry.hidden) $('note-title').focus();
  }

  function renderSaved() {
    if (storageState !== 'ready') {
      $('recent-title').textContent = t('recentUnreadable');
      $('recent-meta').textContent = t('recentUnreadableHint');
      return;
    }
    $('recent-title').textContent = savedRecord ? savedRecord.title : t('recentEmpty');
    $('recent-meta').textContent = t(savedRecord ? 'recentSaved' : 'recentEmptyHint');
  }

  function readStored(initial = false) {
    try {
      const raw = localStorage.getItem(KEY);
      const data = raw === null ? null : JSON.parse(raw);
      if (raw !== null && (!data || typeof data.title !== 'string' ||
          !data.title.trim() || data.title.length > 150 ||
          typeof data.body !== 'string' || data.body.length > 3000)) {
        throw new SyntaxError('Unrecognized note data');
      }
      savedRecord = data;
      storageState = 'ready';
      if (!draftTouched) {
        $('note-title').value = data ? data.title : '';
        $('note-body').value = data ? data.body : '';
      }
      if (!initial) {
        showStatus(draftTouched
          ? (data ? 'readRecoveredDraft' : 'readRecoveredEmptyDraft')
          : (data ? 'readRecovered' : 'readRecoveredEmpty'));
      }
    } catch (error) {
      storageState = 'unavailable';
      showStatus(error instanceof SyntaxError ? 'invalidStored' : 'readFailed');
    }
    renderSaved();
    updateControls();
  }

  function renderLocale() {
    root.lang = locale === 'zh' ? 'zh-CN' : 'en';
    document.title = t('htmlTitle');
    for (const element of document.querySelectorAll('[data-i18n]')) {
      element.textContent = t(element.dataset.i18n);
    }
    $('skip').textContent = t('skip');
    $('locale-toggle').textContent = t('langButton');
    $('locale-toggle').setAttribute('aria-label', t('langAria'));
    $('locale-toggle').lang = locale === 'zh' ? 'en' : 'zh-CN';
    $('note-title').placeholder = t('titlePlaceholder');
    $('note-body').placeholder = t('bodyPlaceholder');
    document.querySelector('.context-panel').setAttribute('aria-label',
      locale === 'zh' ? '研究笔记预览' : 'Research note preview');
    $('theme-toggle').setAttribute('aria-label',
      t(root.dataset.theme === 'dark' ? 'themeLight' : 'themeDark'));
    if (!$('title-error').hidden) $('title-error').textContent = t('missing');
    showStatus(status);
    renderSaved();
  }

  function clearFieldError() {
    $('title-error').hidden = true;
    $('title-error').textContent = '';
    $('note-title').removeAttribute('aria-invalid');
  }

  function currentRecord() {
    return {title:$('note-title').value.trim(), body:$('note-body').value};
  }

  function submit() {
    // Repeated submits preserve the in-flight attempt; a reset can cancel it.
    if (pending !== null || storageState !== 'ready') return;
    const record = currentRecord();
    if (!record.title) {
      $('note-title').setAttribute('aria-invalid', 'true');
      $('title-error').hidden = false;
      $('title-error').textContent = t('missing');
      showStatus('');
      $('note-title').focus();
      return;
    }
    clearFieldError();
    const snapshot = JSON.stringify(record);
    const operation = {timer:null};
    pending = operation;
    showStatus('saving');
    updateControls();
    // These authored delays expose pending behavior; they are not latency measurements.
    const delay = $('simulate-slow').checked ? 1000 : 140;
    operation.timer = setTimeout(() => {
      if (pending !== operation) return;
      pending = null;
      try {
        if ($('simulate-failure').checked) throw new Error('Simulated write failure');
        localStorage.setItem(KEY, snapshot);
        savedRecord = record;
        draftEdited = JSON.stringify(currentRecord()) !== snapshot;
        draftTouched = draftEdited;
        showStatus(draftEdited ? 'savedEarlier' : 'saved');
        renderSaved();
      } catch {
        showStatus('failed');
      }
      updateControls();
    }, delay);
  }

  function clearStored() {
    if (pending !== null) {
      clearTimeout(pending.timer);
      pending = null;
    }
    updateControls();
    try {
      localStorage.removeItem(KEY);
    } catch {
      showStatus('clearFailed');
      return;
    }
    savedRecord = null;
    storageState = 'ready';
    draftEdited = false;
    draftTouched = false;
    $('note-title').value = '';
    $('note-body').value = '';
    clearFieldError();
    renderSaved();
    showStatus('resetDone');
    updateControls();
  }

  function markEdited() {
    draftTouched = true;
    const record = currentRecord();
    draftEdited = savedRecord
      ? JSON.stringify(record) !== JSON.stringify(savedRecord)
      : Boolean(record.title || record.body);
    if (['saved', 'savedEarlier', 'edited', 'resetDone', 'readRecovered', 'readRecoveredDraft', 'readRecoveredEmpty', 'readRecoveredEmptyDraft'].includes(status)) {
      showStatus(draftEdited ? 'edited' : (savedRecord ? 'saved' : ''));
    }
  }

  $('note-form').addEventListener('submit', event => { event.preventDefault(); submit(); });
  $('retry').addEventListener('click', () => {
    if (retryAction === 'save') submit();
    else if (retryAction === 'read') readStored();
    else if (retryAction === 'clear') clearStored();
  });
  $('note-body').addEventListener('input', markEdited);
  $('note-title').addEventListener('input', () => {
    markEdited();
    if ($('note-title').value.trim()) clearFieldError();
  });
  $('locale-toggle').addEventListener('click', () => {
    locale = locale === 'zh' ? 'en' : 'zh';
    renderLocale();
  });
  $('theme-toggle').addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    renderLocale();
  });
  $('long-example').addEventListener('click', () => {
    $('note-title').value = t('longTitle');
    $('note-title').dispatchEvent(new Event('input'));
    $('note-title').focus();
  });
  $('reset').addEventListener('click', clearStored);
  readStored(true);
  renderLocale();
})();
