/* Fieldnote. Storage confirms success; the card only presents that confirmed state. */
(() => {
'use strict';
const $ = id => document.getElementById(id), root=document.documentElement;
const KEY='ui-spec-temporal-note-v1';
const copy={
en:{edition:'A little room to think.',eyebrow:'ONE QUESTION. A FEW GOOD NOTES.',pageTitle:'Keep an idea<br> in view.',intro:'A place for the evidence, the loose ends, and what you want to find out next.',subject:'ENERGY / CITIES',question:'How can cities reduce peak heating demand?',localOnly:'Your note stays in this browser.',fieldnote:'FIELDNOTE No. 001',yourNote:'YOUR RESEARCH NOTE',editorTitle:'Follow the thought.',noteLabel:'Your research note',noteHint:'Evidence, questions, next steps.',save:'Save note',return:'Keep editing',shortcut:'⌘ / Ctrl + Enter to save',disclosure:'Local demo · A small space for an unfinished thought.',controls:'About this demo',delay:'Notes save only in this browser, with a 0.9 second demo delay. Unsaved edits remain here until you reload.',clear:'Clear local note',draft:'Draft',savedFace:'Saved note',viewSaved:'View saved note ↗',backDraft:'Back to draft ↶',none:'No saved note yet',savedKicker:'SAVED IN THIS BROWSER',savedTitle:'An idea to return to.',saving:'Saving in this browser…',saved:'Saved in this browser. Ready when you are.',earlier:'Submitted version saved. Your newer edits are still a draft.',edited:'Unsaved changes.',failed:'Couldn’t save this note. Your draft is still here.',unavailable:'Couldn’t read the saved note. Retry reading or clear local data to continue.',clearFailed:'Couldn’t clear the note. Your saved note and draft are still here.',cleared:'Local note cleared.',read:'Saved note is available again.',retrySave:'Try saving again',retryRead:'Try reading again',retryClear:'Try clearing again',tooLong:'Over the 600-character limit. Shorten your note to save; your text is still here.',empty:'Nothing saved yet.',emptyHint:'Return to your draft and save a note.',unknown:'Saved note unavailable.',dark:'Switch to dark theme',light:'Switch to light theme',date:'Saved',limit:'characters',savingButton:'Saving…',editing:'Draft / unsaved changes'},
zh:{edition:'留一点空间，好好想。',eyebrow:'一个问题，几条值得留下的笔记。',pageTitle:'让想法<br>留在眼前。',intro:'记录证据、未解的问题，以及下一步想探究的方向。',subject:'能源 / 城市',question:'城市如何降低高峰供热需求？',localOnly:'笔记仅保存在此浏览器。',fieldnote:'研究笔记 No. 001',yourNote:'你的研究笔记',editorTitle:'顺着思路，继续写。',noteLabel:'研究笔记',noteHint:'证据、问题、下一步。',save:'保存笔记',return:'继续编辑',shortcut:'⌘ / Ctrl + Enter 保存',disclosure:'本地演示 · 为未完成的想法留个位置。',controls:'关于此演示',delay:'笔记仅保存在此浏览器。保存含 0.9 秒演示延迟。刷新页面前，未保存的修改会保留在这里。',clear:'清除本地笔记',draft:'草稿',savedFace:'已存笔记',viewSaved:'查看已存笔记 ↗',backDraft:'返回草稿 ↶',none:'还没有已存笔记',savedKicker:'已保存在此浏览器',savedTitle:'留待回看的想法。',saving:'正在保存到此浏览器…',saved:'已保存在此浏览器，可随时回看。',earlier:'提交版本已保存，之后的修改仍为草稿。',edited:'修改尚未保存。',failed:'未能保存笔记，草稿仍保留在这里。',unavailable:'无法读取已存笔记。请重试读取，或清除本地数据后继续。',clearFailed:'无法清除笔记，已存笔记和草稿仍保留。',cleared:'本地笔记已清除。',read:'已重新读取笔记。',retrySave:'重试保存',retryRead:'重试读取',retryClear:'重试清除',tooLong:'超过 600 字限制。请缩短后保存，输入内容仍保留。',empty:'还没有已存笔记。',emptyHint:'返回草稿并保存笔记。',unknown:'暂时无法读取已存笔记。',dark:'切换深色主题',light:'切换浅色主题',date:'保存于',limit:'字',savingButton:'保存中…',editing:'草稿 / 尚未保存'}
};
let locale='en',face='front',status='',saved=null,ready=false,pending=null,touched=false,epoch=0,focusIntent=null,selection={start:0,end:0,scroll:0};
const reduced=matchMedia('(prefers-reduced-motion: reduce)'),systemDark=matchMedia('(prefers-color-scheme: dark)');
root.dataset.theme=systemDark.matches?'dark':'light';
const t=k=>copy[locale][k];
$('note-text').value='Compare city demand patterns and check which evidence supports each explanation.';
function render(){
 const text=$('note-text').value,over=text.length>600;
 $('note-limit').textContent=`${text.length} / 600`; $('note-limit').dataset.overLimit=String(over);
 $('note-text').setAttribute('aria-invalid',String(over));
 $('save').disabled=!!pending||!ready||over; $('save').setAttribute('aria-busy',String(!!pending));
 $('save').firstElementChild.textContent=t(pending?'savingButton':'save');
 $('note-card').classList.toggle('is-saving',!!pending);
 $('face-label').textContent=t(face==='back'?'savedFace':touched&&text!==saved?.text?'editing':'draft');
 $('flip').textContent=t(face==='back'?'backDraft':saved?'viewSaved':'none');
 $('flip').disabled=!saved&&face==='front'; $('flip').setAttribute('aria-pressed',String(face==='back'));
 $('saved-kicker').textContent=t(saved&&ready?'savedKicker':ready?'none':'unknown');
 $('saved-title').textContent=t(saved&&ready?'savedTitle':ready?'empty':'unknown');
 $('saved-text').textContent=ready?(saved?saved.text:t('emptyHint')):t('unavailable');
 $('saved-date').textContent=saved?.updatedAt&&Number.isFinite(Date.parse(saved.updatedAt))?`${t('date')} ${new Intl.DateTimeFormat(locale==='zh'?'zh-CN':'en',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}).format(new Date(saved.updatedAt))}`:saved?t('localOnly'):'';
 $('status').textContent=status?t(status):''; $('status-area').dataset.status=status;
 const retry={failed:'retrySave',unavailable:'retryRead',clearFailed:'retryClear'}[status];
 const wasRetry=document.activeElement===$('retry');
 $('retry').hidden=!retry;if(retry)$('retry').textContent=t(retry);
 if(wasRetry&&!retry)$('save').focus({preventScroll:true});
}
function announce(next){status=next;render()}
function finishFocus(){
 if(!focusIntent)return;
 const target=focusIntent;focusIntent=null;
 if(face==='front'&&target==='editor'){
  $('note-text').focus({preventScroll:true});$('note-text').setSelectionRange(selection.start,selection.end);$('note-text').scrollTop=selection.scroll;
 }else if(face==='back'&&target==='saved')$('saved-title').focus({preventScroll:true});
}
function turn(next,focus=null){
 if(next===face){if(focus){focusIntent=focus;finishFocus()}return}
 if(next==='back'&&!saved)return;
 epoch++;
 if(face==='front'){selection={start:$('note-text').selectionStart,end:$('note-text').selectionEnd,scroll:$('note-text').scrollTop}}
 if($('note-card').contains(document.activeElement))$('flip').focus({preventScroll:true});
 face=next;focusIntent=focus;
 $('note-card').dataset.face=face;
 $('card-front').inert=face!=='front';$('card-back').inert=face!=='back';
 $('card-front').setAttribute('aria-hidden',String(face!=='front'));$('card-back').setAttribute('aria-hidden',String(face!=='back'));
 render();
 if(reduced.matches)finishFocus();
}
$('note-card').addEventListener('transitionend',e=>{if(e.target===$('note-card')&&e.propertyName==='transform')finishFocus()});
function read(initial=false){
 try{
  const raw=localStorage.getItem(KEY),v=raw===null?null:JSON.parse(raw);
  if(v!==null&&(!v||v.id!=='heating-study'||typeof v.title!=='string'||typeof v.text!=='string'||v.text.length>600))throw Error('Invalid saved note');
  saved=v;ready=true;if(v&&!touched)$('note-text').value=v.text;
  announce(initial?'':'read');
 }catch(e){ready=false;announce('unavailable')}
}
function save(){
 if(pending||!ready)return;
 if($('note-text').value.length>600){announce('tooLong');$('note-text').focus();return}
 const record={id:'heating-study',title:t('question'),text:$('note-text').value,updatedAt:new Date().toISOString()};
 const attempt={record,epoch,timer:null};pending=attempt;announce('saving');
 attempt.timer=setTimeout(()=>{
  if(pending!==attempt)return;
  try{
   localStorage.setItem(KEY,JSON.stringify(record));saved=record;pending=null;
   const unchanged=$('note-text').value===record.text;
   announce(unchanged?'saved':'earlier');
   if(unchanged&&epoch===attempt.epoch){touched=false;turn('back','saved')}
  }catch(e){pending=null;announce('failed');if(face==='back')turn('front','editor')}
 },900);
}
function clear(){
 if(pending)clearTimeout(pending.timer);pending=null;
 try{localStorage.removeItem(KEY);turn('front','editor');saved=null;ready=true;touched=false;$('note-text').value='';selection={start:0,end:0,scroll:0};announce('cleared')}
 catch(e){announce('clearFailed');if(face==='back')turn('front');$('retry').focus()}
}
function localize(){
 root.lang=locale==='zh'?'zh-CN':'en';
 document.querySelectorAll('[data-copy]').forEach(e=>{if(e.dataset.copy==='pageTitle')e.innerHTML=t(e.dataset.copy);else e.textContent=t(e.dataset.copy)});
 document.title=locale==='en'?'Fieldnote · A place for an idea':'Fieldnote · 让想法留在眼前';
 $('locale-toggle').textContent=locale==='en'?'中文':'EN';$('locale-toggle').setAttribute('aria-label',locale==='en'?'切换中文':'Switch to English');
 $('theme-toggle').setAttribute('aria-label',t(root.dataset.theme==='dark'?'light':'dark'));
 $('card-front').setAttribute('aria-label',t('noteLabel'));$('card-back').setAttribute('aria-label',t('savedFace'));render();
}
$('note-text').addEventListener('input',()=>{touched=true;if(!pending&&ready&&!['failed','clearFailed'].includes(status))status=$('note-text').value.length>600?'tooLong':'edited';render()});
$('save').addEventListener('click',save);
$('flip').addEventListener('click',()=>turn(face==='front'?'back':'front'));
$('return').addEventListener('click',()=>turn('front','editor'));
$('retry').addEventListener('click',()=>{if(status==='failed')save();else if(status==='unavailable')read();else if(status==='clearFailed')clear()});
$('clear').addEventListener('click',clear);
$('theme-toggle').addEventListener('click',()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';localize()});
$('locale-toggle').addEventListener('click',()=>{locale=locale==='en'?'zh':'en';localize()});
$('note-text').addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();save()}});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&face==='back'){e.preventDefault();turn('front','editor')}});
 document.querySelector('.brand').addEventListener('click',e=>{e.preventDefault();turn('front','editor')});
 const syncMotion=()=>{root.classList.toggle('is-reduced',reduced.matches);if(reduced.matches)finishFocus()};reduced.addEventListener('change',syncMotion);
 syncMotion();read(true);localize();
})();
