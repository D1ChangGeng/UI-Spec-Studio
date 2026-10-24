/* Authored scenario logic. All research responses are deterministic fixtures. */
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const root = document.documentElement;
  let timer = null;
  let activeRequest = 0;
  let lastQuestion = '';
  let returnFocus = null;
  function cancel(message) {
    activeRequest += 1;
    clearTimeout(timer);
    timer = null;
    document.querySelector('.pending')?.remove();
    $('stop').hidden = true;
    $('send').hidden = false;
    $('send').disabled = !$('question').value.trim();
    if (message) $('feedback').textContent = message;
  }
  function openDialog(dialog) {
    returnFocus = document.activeElement;
    dialog.showModal();
  }
  function closeDialog(dialog) { dialog.close(); }
  ['decision-dialog', 'source-dialog', 'history-dialog'].forEach((id) => $(id).addEventListener('close', () => returnFocus?.focus()));
  $('decision-open').onclick = () => openDialog($('decision-dialog'));
  $('decision-close').onclick = () => closeDialog($('decision-dialog'));
  $('history').onclick = () => openDialog($('history-dialog'));
  $('history-close').onclick = () => closeDialog($('history-dialog'));
  document.querySelectorAll('[data-history]').forEach((button) => button.onclick = () => {
    closeDialog($('history-dialog'));
    if (root.dataset.model === 'documents') openNote(button.dataset.history);
    else { resetConversation(); $('question').value = button.dataset.history; $('send').disabled = false; }
  });
  $('source-close').onclick = () => closeDialog($('source-dialog'));
  $('theme').onclick = () => {
    const dark = root.dataset.theme !== 'dark';
    root.dataset.theme = dark ? 'dark' : 'light';
    $('theme').textContent = dark ? '浅色' : '深色';
    $('theme').setAttribute('aria-label', dark ? '切换浅色主题' : '切换深色主题');
  };
  document.querySelectorAll('input[name=model]').forEach((input) => input.addEventListener('change', () => {
    cancel();
    const documents = input.value === 'documents';
    root.dataset.model = input.value;
    $('conversation').hidden = documents;
    $('documents').hidden = !documents;
    $('evidence').hidden = documents;
    $('nav-label').textContent = documents ? '资料集合' : '最近对话';
    $('model-description').textContent = documents ? '从持久资料发起，编辑、组织并重新发现知识。' : '从问题发起，在同一条对话中追问并核对来源。';
    $('breadcrumb').textContent = documents ? '研究 / 资料集合' : '研究 / 对话';
    $('new').querySelector('span').textContent = documents ? '新建笔记' : '新建研究';
    $('preference').textContent = `当前预览：${documents ? '资料空间' : '对话研究'} · 产品方向待确认`;
    $('feedback').textContent = '';
  }));
  function resetConversation() {
    cancel(); root.classList.remove('has-result'); $('thread').replaceChildren(); $('thread').hidden = true;
    document.querySelector('.welcome').hidden = false;
    $('suggestions').hidden = false; $('question').value = ''; $('send').disabled = true;
    $('feedback').textContent = ''; $('question').focus();
  }
  $('new').onclick = () => root.dataset.model === 'documents' ? openNote('新建研究笔记') : resetConversation();
  document.querySelectorAll('[data-prompt]').forEach((button) => button.onclick = () => {
    $('question').value = button.dataset.prompt; $('send').disabled = false; $('question').focus();
  });
  document.querySelectorAll('[data-topic]').forEach((button) => button.onclick = () => {
    if (root.dataset.model === 'documents') openNote(button.textContent.split('今天')[0].trim());
    else { resetConversation(); $('question').value = button.dataset.topic; $('send').disabled = false; }
  });
  $('question').addEventListener('input', () => { $('send').disabled = !$('question').value.trim(); });
  $('question').addEventListener('keydown', (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter' && !event.isComposing && $('stop').hidden) {
      event.preventDefault(); $('composer').requestSubmit();
    }
  });
  function submit(question, repeated = false) {
    cancel();
    const token = activeRequest;
    lastQuestion = question; root.classList.add('has-result');
    document.querySelector('.welcome').hidden = true; $('suggestions').hidden = true;
    $('thread').hidden = false; $('feedback').textContent = '';
    if (!repeated) {
      const user = document.createElement('div'); user.className = 'message user'; user.textContent = question; $('thread').append(user);
    }
    const pending = document.createElement('p'); pending.className = 'pending'; pending.setAttribute('role', 'status'); pending.textContent = '正在组织示例结果…'; $('thread').append(pending);
    $('send').hidden = true; $('stop').hidden = false;
    const mode = $('response').value;
    timer = setTimeout(() => {
      if (token !== activeRequest) return;
      cancel();
      const answer = document.createElement('article'); answer.className = 'message answer';
      if (mode === 'error') {
        answer.classList.add('error'); answer.textContent = '演示请求失败。问题已保留，可重试。';
        const retry = document.createElement('button'); retry.textContent = '重试'; retry.onclick = () => { answer.remove(); submit(question, true); }; answer.append(retry);
      } else {
        const label = document.createElement('span'); label.className = 'response-label'; label.textContent = 'STUDY · 演示回答'; answer.append(label);
        const amount = mode === 'long' ? 10 : 2;
        for (let i = 0; i < amount; i++) {
          const p = document.createElement('p');
          p.textContent = i === 0 ? '先明确分析边界，再比较可行方案。对于这个问题，可以从需求变化、可调节资源和实施条件三个方向组织材料。' : '将结论与来源放在一起检查：哪些是已知事实，哪些仍是待验证的假设？此处内容仅用于展示长短文本、阅读顺序和来源交互。';
          answer.append(p);
        }
        const source = document.createElement('button'); source.className = 'source-button'; source.textContent = '查看演示来源 01'; source.onclick = () => openDialog($('source-dialog')); answer.append(source);
        if ($('question').value.trim() === question) $('question').value = '';
        $('send').disabled = !$('question').value.trim();
      }
      $('thread').append(answer);
      $('feedback').textContent = mode === 'error' ? '可调整模拟响应后重试。' : '示例结果已就绪，可继续追问。';
    }, mode === 'slow' ? 1800 : 180);
  }
  $('composer').addEventListener('submit', (event) => {
    event.preventDefault(); const question = $('question').value.trim();
    if (question && $('stop').hidden) submit(question);
  });
  $('stop').onclick = () => cancel('已停止示例请求，输入已保留。');
  function openNote(title) {
    $('collection').hidden = true; $('editor').hidden = false;
    $('note-title').value = title; $('save-status').textContent = '修改仅保存在当前浏览器的示例空间';
    try {
      const saved = JSON.parse(localStorage.getItem('ui-spec-study-note') || 'null');
      if (saved && saved.title === title && typeof saved.body === 'string') $('note-body').value = saved.body;
      else $('note-body').value = '这是可编辑的示例笔记。记录问题、材料与尚待验证的结论。';
    } catch { $('save-status').textContent = '当前浏览器未提供可用的本地记录。'; }
    $('note-title').focus();
  }
  document.querySelectorAll('[data-doc]').forEach((button) => button.onclick = () => openNote(button.dataset.doc));
  $('create-note').onclick = () => openNote('新建研究笔记');
  $('back').onclick = () => { $('editor').hidden = true; $('collection').hidden = false; $('create-note').focus(); };
  $('save-note').onclick = () => {
    try {
      localStorage.setItem('ui-spec-study-note', JSON.stringify({title:$('note-title').value, body:$('note-body').value}));
      $('save-status').textContent = '已保存到本地示例空间';
    } catch { $('save-status').textContent = '保存不可用；输入仍保留在当前页面。'; }
  };
})();
