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
      brandSubtitle:'研究笔记', eyebrow:'研究空间 / 笔记', scope:'本地演示',
      step:'记录想法', pageTitle:'把研究线索整理成笔记',
      pageIntro:'先记下问题和背景，再回来继续完善。',
      titleLabel:'笔记标题', titleHint:'用一句话写清想研究的问题',
      titlePlaceholder:'例如：如何降低供热高峰负荷？',
      bodyLabel:'背景与线索', optional:'选填',
      bodyHint:'补充已有材料、疑问或仍需核查的判断',
      bodyPlaceholder:'记下材料、想法或需要验证的线索…',
      save:'保存笔记', savingButton:'正在保存…',
      saveHint:'每次保存会替换上一版。离开此页前请保存。',
      missing:'填写笔记标题后再保存。', retry:'重试保存',
      storage:'手动保存 · 仅此浏览器', asideStep:'继续研究', asideTitle:'最近保存',
      asideIntro:'这里显示上次保存的标题。重新打开此页时，会载入已保存的笔记。',
      recentEmpty:'还没有保存的笔记', recentEmptyHint:'保存成功后，标题会显示在这里',
      recentSaved:'上次保存的版本 · 此浏览器',
      disclosure:'这是交互演示。笔记只保存在此浏览器中，不会发送到外部服务。清除浏览器数据会删除笔记。',
      previewSettings:'预览状态设置', failureSwitch:'模拟写入失败',
      slowSwitch:'延迟写入 1 秒', loadLong:'填写较长标题', reset:'清除本地演示数据',
      resetHint:'清除会删除已保存的笔记，并清空当前输入。需要保留时，请先复制文本。',
      fixtureLabel:'内容与交互状态实例 · 本地运行',
      langButton:'EN', langAria:'EN · Switch to English',
      themeDark:'切换深色主题', themeLight:'切换浅色主题',
      clearRetry:'重试清除', readRetry:'重试读取',
      recentUnreadable:'暂时无法读取笔记', recentUnreadableHint:'重试读取后可确认已保存的内容',
      longTitle:'比较不同城市在能源供应高峰期间如何调节供热需求，并梳理可供进一步核查的具体研究证据',
      htmlTitle:'研究笔记 · 内容设计实例', skip:'跳到主要内容'
    },
    en: {
      brandSubtitle:'Research notes', eyebrow:'Research / Notes', scope:'Local demo',
      step:'Capture an idea', pageTitle:'Turn a research lead into a note',
      pageIntro:'Start with the question and its context. Return to the same note as your research develops.',
      titleLabel:'Note title', titleHint:'Name the question you want to investigate',
      titlePlaceholder:'e.g. Peak heating demand',
      bodyLabel:'Context and leads', optional:'Optional',
      bodyHint:'Add sources, open questions, or assumptions to check',
      bodyPlaceholder:'Capture the source material or questions to verify…',
      save:'Save note', savingButton:'Saving…',
      saveHint:'Each save replaces the previous version. Save before leaving this page.',
      missing:'Add a note title before saving.', retry:'Try saving again',
      storage:'Manual save · This browser only', asideStep:'Continue your work', asideTitle:'Recently saved',
      asideIntro:'The last saved title appears here. Reopening this page loads that saved note.',
      recentEmpty:'No note saved yet', recentEmptyHint:'The title appears here after a successful save',
      recentSaved:'Last saved version · This browser',
      disclosure:'This is an interactive demo. The note stays in this browser and is not sent to an external service. Clearing browser data deletes the note.',
      previewSettings:'Preview state controls', failureSwitch:'Simulate a write failure',
      slowSwitch:'Delay the write by 1 second', loadLong:'Use a longer example title', reset:'Clear local demo data',
      resetHint:'Clearing deletes the saved note and empties the current fields. Copy any text you want to keep first.',
      fixtureLabel:'Content and state example · Local demo',
      langButton:'中文', langAria:'切换到中文',
      themeDark:'Switch to dark theme', themeLight:'Switch to light theme',
      clearRetry:'Try clearing again', readRetry:'Try reading again',
      recentUnreadable:'Saved note unavailable', recentUnreadableHint:'Try reading again to check the saved content',
      longTitle:'Compare how different cities manage district-heating demand during peak energy use and identify which evidence needs to be verified',
      htmlTitle:'Research notes · Content design example', skip:'Skip to main content'
    }
  };
  // A short outcome leads each message; the detail explains the consequence or recovery.
  // These statements describe the existing single-note, manual localStorage contract.
  const messages = {
    zh: {
      empty:['尚未保存笔记', '内容不会自动保存，请先填写标题。'],
      loaded:['已载入上次保存的笔记', '可以继续编辑；修改后需要再次保存。'],
      saving:['正在保存到此浏览器…', '可以继续编辑；新修改需再次保存。'],
      saved:['已保存到此浏览器', '重新打开此页时，会载入这份笔记。'],
      savedEarlier:['已保存点击时的版本', '保存期间的新修改尚未保存。请再次保存，更新本地版本。'],
      edited:['有尚未保存的修改', '当前修改仍只在此页。刷新或关闭页面前，请先保存。'],
      failed:['保存未完成', '输入仍在此页，尚未保存。请重试；若仍失败，先复制文本备份，再检查浏览器的存储设置。刷新或关闭页面会丢失未保存的修改。'],
      simulatedFailure:['本次模拟保存失败', '输入仍在此页，尚未保存。在「预览状态设置」中关闭「模拟写入失败」，再重试保存。离开此页前请先保存或复制文本。'],
      resetDone:['本地演示数据已清除', '已保存的笔记和当前输入均已清空，可以开始新笔记。'],
      clearFailed:['未能清除本地演示数据', '当前输入仍在此页。可以重试清除；需要保留的文本请先复制备份。'],
      readFailed:['暂时无法读取已保存的笔记', '保存已暂停，以免覆盖未能读取的内容。请重试读取；当前输入仍在此页，离开前请先复制备份。'],
      invalidStored:['已保存的笔记格式无法识别', '保存已暂停。可先重试读取；若仍失败，先复制当前输入，再到「预览状态设置」清除本地演示数据。清除也会清空当前输入。'],
      readRecovered:['已重新读取本地笔记', '上次保存的内容已载入。修改后需要再次保存。'],
      readRecoveredEmpty:['已恢复读取，尚无已保存的笔记', '填写标题后即可保存。内容不会自动保存。'],
      readRecoveredEmptyDraft:['已恢复读取，当前输入尚未保存', '输入已保留。选择「保存笔记」，将它保存在此浏览器中。'],
      readRecoveredDraft:['已恢复读取，当前输入已保留', '「最近保存」显示上次保存的标题。再次保存会用当前输入替换已保存的笔记。']
    },
    en: {
      empty:['No note saved yet', 'Add a title to begin. Changes are not saved automatically.'],
      loaded:['Last saved note loaded', 'Continue editing. Save again to keep any changes.'],
      saving:['Saving in this browser…', 'You can keep editing. Changes made during this save will need another save.'],
      saved:['Saved in this browser', 'Reopen this page to continue editing this note.'],
      savedEarlier:['The version you submitted was saved', 'Edits made while saving are still unsaved. Save again to keep those changes.'],
      edited:['You have unsaved changes', 'These edits are only on this page. Save before refreshing or closing it.'],
      failed:['The note could not be saved', 'Your text is still here and is unsaved. Try again. If it still fails, copy your text before checking browser storage settings. Refreshing or closing the page loses unsaved edits.'],
      simulatedFailure:['This save failure was simulated', 'Your text is still here and is unsaved. Turn off "Simulate a write failure" in "Preview state controls", then try saving again. Save or copy your text before leaving.'],
      resetDone:['Local demo data cleared', 'The saved note and current fields are empty. You can start a new note.'],
      clearFailed:['Local demo data could not be cleared', 'Your current text is still here. Try clearing again. Copy any text you want to keep first.'],
      readFailed:['The saved note could not be read', 'Saving is paused to avoid overwriting unread content. Try reading again. Your current text is still here; copy it before leaving.'],
      invalidStored:['The saved note has an unreadable format', 'Saving is paused. Try reading again. If it still fails, copy your current text, then clear local demo data in "Preview state controls". Clearing also empties the current fields.'],
      readRecovered:['Local note read successfully', 'The last saved content is loaded. Save again after editing.'],
      readRecoveredEmpty:['Reading restored; no note saved yet', 'Add a title to save a note. Changes are not saved automatically.'],
      readRecoveredEmptyDraft:['Reading restored; your text is unsaved', 'Your input is still here. Choose "Save note" to keep it in this browser.'],
      readRecoveredDraft:['Reading restored; your input is unchanged', '"Recently saved" shows the stored title. Saving now replaces the stored note with your current input.']
    }
  };
  function t(name) { return copy[locale][name]; }

  function updateControls() {
    $('save').disabled = pending !== null || storageState !== 'ready';
    $('save').setAttribute('aria-busy', String(pending !== null));
    $('save-label').textContent = t(pending !== null ? 'savingButton' : 'save');
  }

  function showStatus(next) {
    status = next;
    const retry = $('retry');
    const retryHadFocus = document.activeElement === retry;
    const actions = {failed:'save', simulatedFailure:'save', readFailed:'read', invalidStored:'read', clearFailed:'clear'};
    retryAction = actions[next] || null;
    const [heading, detail] = messages[locale][next] || ['', ''];
    // Avoid re-announcing the same unsaved message on every keystroke.
    if ($('state-message').textContent !== heading) $('state-message').textContent = heading;
    if ($('state-detail').textContent !== detail) $('state-detail').textContent = detail;
    $('state-detail').hidden = !detail;
    $('save-status').parentElement.dataset.status = retryAction ? 'error' : next;
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
      if (initial) {
        showStatus(data ? 'loaded' : 'empty');
      } else {
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
    updateControls();
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
        showStatus($('simulate-failure').checked ? 'simulatedFailure' : 'failed');
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
    if (['', 'empty', 'loaded', 'saved', 'savedEarlier', 'edited', 'resetDone', 'readRecovered', 'readRecoveredDraft', 'readRecoveredEmpty', 'readRecoveredEmptyDraft'].includes(status)) {
      showStatus(draftEdited ? 'edited' : (savedRecord ? 'saved' : 'empty'));
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
