/* A content-design fixture with real browser-local writes and source-owned messages. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const root = document.documentElement;
  const KEY = 'ui-spec-content-note-v1';
  let locale = 'zh';
  let status = '';
  let pending = null;
  const copy = {
    zh: {
      brandSubtitle:'研究笔记',eyebrow:'研究空间 / 笔记',scope:'本地演示',step:'记录想法',pageTitle:'把研究线索整理成笔记',pageIntro:'先记下问题和背景。之后可以回到同一份笔记继续整理。',titleLabel:'笔记标题',titleHint:'用一句话写清想研究的问题',titlePlaceholder:'例如：城市供热如何降低高峰负荷？',bodyLabel:'背景与线索',optional:'选填',bodyHint:'补充已有材料、疑问或仍需核查的判断',bodyPlaceholder:'记下材料、想法或需要验证的线索…',save:'保存笔记',saving:'正在保存到此浏览器…',saved:'笔记已保存在此浏览器。',savedEarlier:'上一版已保存。当前修改仍需再次保存。',edited:'当前修改尚未保存。',missing:'填写笔记标题后再保存。',failed:'当前无法保存这份笔记。输入内容仍在页面中。',retry:'重试保存',storage:'仅保存在当前浏览器',asideStep:'继续研究',asideTitle:'最近保存',asideIntro:'已保存的笔记会显示在这里，便于继续编辑。',recentEmpty:'还没有保存的笔记',recentEmptyHint:'保存后可在此查看',recentSaved:'已保存 · 当前浏览器',disclosure:'这是交互演示。笔记会保存在此浏览器中，不会发送到外部服务。',previewSettings:'预览状态设置',failureSwitch:'模拟存储失败',loadLong:'填写较长标题',reset:'清除本地演示数据',fixtureLabel:'内容与交互状态实例 · 本地运行',langButton:'EN',langAria:'Switch to English',themeDark:'切换深色主题',themeLight:'切换浅色主题',resetDone:'本地演示数据已清除。',longTitle:'比较不同城市在能源供应高峰期间如何调节供热需求，并梳理可供进一步核查的具体研究证据',htmlTitle:'研究笔记 · 内容设计实例',skip:'跳到主要内容'
    },
    en: {
      brandSubtitle:'Research notes',eyebrow:'Research / Notes',scope:'Local demo',step:'Capture an idea',pageTitle:'Turn a research lead into a note',pageIntro:'Start with the question and its context. Return to the same note as your research develops.',titleLabel:'Note title',titleHint:'Name the question you want to investigate',titlePlaceholder:'For example: How can cities reduce peak heating demand?',bodyLabel:'Context and leads',optional:'Optional',bodyHint:'Add sources, open questions, or assumptions to check',bodyPlaceholder:'Capture the source material or questions to verify…',save:'Save note',saving:'Saving in this browser…',saved:'Note saved in this browser.',savedEarlier:'An earlier version was saved. Save again to keep your new edits.',edited:'You have unsaved changes.',missing:'Add a note title before saving.',failed:'This note could not be saved. Your text is still here.',retry:'Try saving again',storage:'Saved only in this browser',asideStep:'Continue your work',asideTitle:'Recently saved',asideIntro:'Saved notes appear here so you can return to your work.',recentEmpty:'No notes saved yet',recentEmptyHint:'Your note will appear after saving',recentSaved:'Saved · This browser',disclosure:'This is an interactive demo. Notes stay in this browser and are not sent to an external service.',previewSettings:'Preview state controls',failureSwitch:'Simulate a storage failure',loadLong:'Use a longer example title',reset:'Clear local demo data',fixtureLabel:'Content and state example · Local demo',langButton:'中文',langAria:'切换到中文',themeDark:'Switch to dark theme',themeLight:'Switch to light theme',resetDone:'Local demo data cleared.',longTitle:'Compare how different cities manage district-heating demand during peak energy use and identify which evidence needs to be verified',htmlTitle:'Research notes · Content design example',skip:'Skip to main content'
    }
  };
  function t(name){return copy[locale][name];}
  function showStatus(next){
    status=next; const el=$('state-message');
    el.textContent= next ? t(next) : '';
    el.parentElement.dataset.status=['missing','failed'].includes(next) ? 'error' : next;
    $('retry').hidden=next!=='failed';
  }
  function getSaved(){
    try {const data=JSON.parse(localStorage.getItem(KEY)||'null');
      return data && typeof data.title==='string' && typeof data.body==='string' ? data : null;
    } catch {return null;}
  }
  function renderSaved(){
    const data=getSaved();
    $('recent-title').textContent=data?.title||t('recentEmpty');
    $('recent-meta').textContent=data?t('recentSaved'):t('recentEmptyHint');
  }
  function renderLocale(){
    root.lang=locale==='zh'?'zh-CN':'en'; document.title=t('htmlTitle');
    for(const element of document.querySelectorAll('[data-i18n]')) element.textContent=t(element.dataset.i18n);
    $('skip').textContent=t('skip');
    $('locale-toggle').textContent=t('langButton');$('locale-toggle').setAttribute('aria-label',t('langAria'));
    $('note-title').placeholder=t('titlePlaceholder');$('note-body').placeholder=t('bodyPlaceholder');
    document.querySelector('.context-panel').setAttribute('aria-label', locale==='zh'?'研究笔记预览':'Research note preview');
    $('theme-toggle').setAttribute('aria-label',t(root.dataset.theme==='dark'?'themeLight':'themeDark'));
    showStatus(status);renderSaved();
  }
  function submit(){
    if(pending) clearTimeout(pending);
    const title=$('note-title').value.trim(),body=$('note-body').value;
    if(!title){
      $('note-title').setAttribute('aria-invalid','true');
      $('title-error').hidden=false;$('title-error').textContent=t('missing');showStatus('');
      $('note-title').focus();return;
    }
    $('title-error').hidden=true;$('note-title').removeAttribute('aria-invalid');
    $('save').disabled=true;showStatus('saving');
    const snapshot=JSON.stringify({title,body});
    pending=setTimeout(()=>{
      pending=null;
      if($('simulate-failure').checked){showStatus('failed');}
      else {
        try {localStorage.setItem(KEY,snapshot);showStatus(JSON.stringify({title:$('note-title').value.trim(),body:$('note-body').value})===snapshot?'saved':'savedEarlier');renderSaved();}
        catch{showStatus('failed');}
      }
      $('save').disabled=false;
    },140);
  }
  $('note-form').addEventListener('submit',e=>{e.preventDefault();submit();});
  $('retry').addEventListener('click',submit);
  function markEdited(){if(status==='saved'||status==='savedEarlier')showStatus('edited');}
  $('note-body').addEventListener('input',markEdited);
  $('note-title').addEventListener('input',()=>{markEdited();
    if($('note-title').value.trim()){$('title-error').hidden=true;$('note-title').removeAttribute('aria-invalid');if(status==='missing')showStatus('');}
  });
  $('locale-toggle').addEventListener('click',()=>{locale=locale==='zh'?'en':'zh';renderLocale();if(!$('title-error').hidden)$('title-error').textContent=t('missing');});
  $('theme-toggle').addEventListener('click',()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';renderLocale();});
  $('long-example').addEventListener('click',()=>{$('note-title').value=t('longTitle');$('note-title').dispatchEvent(new Event('input'));$('note-title').focus();});
  $('reset').addEventListener('click',()=>{
    if(pending){clearTimeout(pending);pending=null;$('save').disabled=false;}
    try{localStorage.removeItem(KEY);}catch{}
    $('note-title').value='';$('note-body').value='';$('title-error').hidden=true;$('note-title').removeAttribute('aria-invalid');
    renderSaved();$('state-message').textContent=t('resetDone');status='';$('retry').hidden=true;
  });
  const saved=getSaved();if(saved){$('note-title').value=saved.title;$('note-body').value=saved.body;}
  renderLocale();
})();
