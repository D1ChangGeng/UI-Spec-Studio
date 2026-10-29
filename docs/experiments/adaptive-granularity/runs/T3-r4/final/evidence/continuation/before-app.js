/* Fieldnote. Storage is the authority; motion follows confirmed state. */
(() => {
'use strict';
const $ = id => document.getElementById(id);
const root = document.documentElement;
const KEY = 'ui-spec-temporal-note-v1';
  const COPY = {
    en: {skip:'Skip to note',savedNotes:'Saved note',eyebrow:'Research / Local demo',pageTitle:'Keep an idea in view',subject:'Energy / Cities',question:'How can cities reduce peak heating demand?',context:'Working context',draftBoundary:'Preview of your current note',showContext:'See context',showFront:'Back to question',pause:'Pause decoration',resume:'Resume decoration',quiet:'Decoration paused',noteLabel:'Your research note',noteHint:'Keep evidence and open questions together.',save:'Save note',localOnly:'Only in this browser',return:'Return to editing',disclosure:'Interactive local demo. The save includes a 900 ms preview delay.',controls:'Preview controls',clear:'Clear local demo data',saving:'Saving in this browser…',saved:'Note saved in this browser.',earlier:'The submitted version is saved. Save again to keep your new edits.',edited:'Your changes have not been saved.',failed:'The note could not be saved. Your text is still here.',retrySave:'Try saving again',unavailable:'Saved data could not be read. Clear demo data or try reading again before saving.',retryRead:'Try reading again',clearFailed:'Demo data could not be cleared. Your text is still here.',retryClear:'Try clearing again',cleared:'Local demo data cleared.',empty:'No saved note yet',emptyHint:'Save your note, then return here to read it.',read:'Saved data is available again.',dark:'Switch to dark theme',light:'Switch to light theme',preview:'Note preview',edit:'Edit note',lengthCount:'{count} / 600 characters',lengthExceeded:'{count} / 600 characters. Shorten the note to save.',tooLong:'Shorten the note to 600 characters before saving. Your text is still here.',pendingLabel:'Save in progress',savingNewer:'Saving a newer version. The previous saved note remains visible.',failedExisting:'The newer version could not be saved. The previous saved note is unchanged. Return to editing to retry.',notSaved:'Note not saved',returnToRetry:'Return to editing to try again. Your text remains in the editor.',unknownTitle:'Saved note unavailable',unknownHint:'The saved note could not be read. Return to editing to retry or clear the demo data. Your current text remains available.'},
    zh: {skip:'跳到笔记',savedNotes:'已存笔记',eyebrow:'研究 / 本地演示',pageTitle:'让研究线索清晰可见',subject:'能源 / 城市',question:'城市如何降低高峰供热需求？',context:'研究背景',draftBoundary:'当前笔记的预览',showContext:'查看背景',showFront:'返回问题',pause:'暂停装饰动效',resume:'继续装饰动效',quiet:'装饰动效已暂停',noteLabel:'研究笔记',noteHint:'把已有证据和待解问题放在一起',save:'保存笔记',localOnly:'仅保存在此浏览器',return:'返回编辑',disclosure:'本地交互演示，保存过程含 900 毫秒预览延迟。',controls:'预览设置',clear:'清除本地演示数据',saving:'正在保存到此浏览器…',saved:'笔记已保存在此浏览器。',earlier:'提交的版本已保存。当前修改仍需再次保存。',edited:'当前修改尚未保存。',failed:'未能保存笔记。输入内容仍在页面中。',retrySave:'重试保存',unavailable:'暂时无法读取已存数据。请清除演示数据或重试读取后再保存。',retryRead:'重试读取',clearFailed:'未能清除演示数据。输入内容仍在页面中。',retryClear:'重试清除',cleared:'本地演示数据已清除。',empty:'还没有已存笔记',emptyHint:'保存笔记后，可回到这里查看',read:'已重新读取本地数据。',dark:'切换深色主题',light:'切换浅色主题',preview:'笔记预览',edit:'编辑笔记',lengthCount:'{count} / 600 字',lengthExceeded:'已输入 {count} 字，最多 600 字。请缩短后再保存。',tooLong:'请缩短至 600 字以内再保存。当前输入仍在页面中。',pendingLabel:'正在保存',savingNewer:'正在保存新版本，下面仍显示上一次保存的内容。',failedExisting:'未能保存新版本，之前保存的内容仍保留。请返回编辑重试。',notSaved:'笔记尚未保存',returnToRetry:'请返回编辑重试。输入内容仍保留在编辑区。',unknownTitle:'暂时无法读取已存笔记',unknownHint:'请返回编辑重试读取，或在预览设置中清除演示数据。当前输入仍保留在编辑区。'}
  };

Object.assign(COPY.en,{eyebrow:'YOUR PERSONAL FIELDNOTES',pageTitle:'Keep an idea in view.',intro:'A place for the evidence, and the questions it opens.',fieldStudy:'FIELD STUDY 001',notebook:'THE WORKING NOTEBOOK',noteLabel:'Your research note',noteHint:'Keep evidence and open questions together.',draftLabel:'DRAFT · NOT SAVED',savedDraft:'SAVED · UP TO DATE',showSaved:'Read saved note ↗',showEdit:'Return to editing ↶',savedBadge:'✓ Saved in this browser',emptyBadge:'No saved note yet',unavailableBadge:'Saved note unavailable',draftFace:'01 / DRAFT',savedFace:'02 / SAVED NOTE',disclosure:'Local demo. Saved notes stay in this browser; unsaved edits do not survive a reload.',controls:'Demo settings',delay:'Saving includes a 900 ms demonstration delay.',lengthCount:'{count} / 600',lengthExceeded:'{count} / 600 · Too long',failed:'Couldn’t save this note. Your draft is still here; the saved version is unchanged.',earlier:'Your submitted version is saved. Your newer edits are still a draft.',savingNewer:'Saving your update. This is the previous saved version.',notSaved:'This note has not been saved yet.',read:'Saved data is available again.',savingButton:'Saving…'});
Object.assign(COPY.zh,{eyebrow:'个人研究笔记',pageTitle:'让想法清晰可见',intro:'记录已有证据，也留下新的问题。',fieldStudy:'研究课题 001',notebook:'研究笔记本',noteLabel:'研究笔记',draftLabel:'草稿 · 尚未保存',savedDraft:'已保存 · 最新版本',showSaved:'查看已存笔记 ↗',showEdit:'返回编辑 ↶',savedBadge:'✓ 已保存在此浏览器',emptyBadge:'还没有已存笔记',unavailableBadge:'暂时无法读取笔记',draftFace:'01 / 草稿',savedFace:'02 / 已存笔记',disclosure:'本地演示。已存笔记保留在此浏览器中；未保存的修改会在刷新后丢失。',controls:'演示设置',delay:'保存过程含 900 毫秒演示延迟。',lengthCount:'{count} / 600 字',lengthExceeded:'{count} / 600 · 已超限',savingButton:'正在保存…'});
let locale='en',face='front',saved=null,pending=null,status='',storageReady=false,touched=false;
let turn=0,selection={start:0,end:0,scroll:0},intent=0;
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
const t=key=>COPY[locale][key];
$('note-text').value='Compare city demand patterns and check which evidence supports each explanation.';
function remember(){selection={start:$('note-text').selectionStart,end:$('note-text').selectionEnd,scroll:$('note-text').scrollTop};}
function update(){
 const draft=$('note-text').value,over=draft.length>600;
 $('note-limit').textContent=t(over?'lengthExceeded':'lengthCount').replace('{count}',draft.length);
 $('note-limit').dataset.overLimit=over;
 $('note-text').setAttribute('aria-invalid',String(over));
 $('note-hint').textContent=over?t('tooLong'):t('noteHint');
 $('save').disabled=!storageReady||over;
 $('save').setAttribute('aria-disabled',String(!!pending||!storageReady||over));
 $('save').setAttribute('aria-busy',String(!!pending));
 $('save-label').textContent=t(pending?'savingButton':'save');
 $('draft-label').textContent=t(saved&&saved.text===draft?'savedDraft':'draftLabel');
 $('saved-kicker').textContent=t(!storageReady?'unavailableBadge':saved?'savedBadge':'emptyBadge');
 $('saved-text').textContent=!storageReady?t('unknownHint'):saved?saved.text:t(pending?'saving':'emptyHint');
 $('saved-foot').textContent=t(!storageReady?'unavailableBadge':saved?'localOnly':'notSaved');
 $('face-label').textContent=t(face==='front'?'draftFace':'savedFace');
 $('flip').textContent=t(face==='front'?'showSaved':'showEdit');
 $('flip').setAttribute('aria-pressed',String(face==='back'));
 $('draft-dot').classList.toggle('active',face==='front');$('saved-dot').classList.toggle('active',face==='back');
 const retryMap={failed:'retrySave',unavailable:'retryRead',clearFailed:'retryClear'};
 const retryFocused=document.activeElement===$('retry');
 $('retry').hidden=!retryMap[status];if(retryMap[status])$('retry').textContent=t(retryMap[status]);
 $('status').textContent=face==='back'&&pending&&saved?t('savingNewer'):status==='failed'&&!saved?(locale==='en'?'Couldn’t save this note. Your draft is still here.':'未能保存笔记。输入内容仍在页面中。'):status?t(status):'';
 $('status-area').dataset.status=status;
 if(retryFocused&&$('retry').hidden)$('flip').focus({preventScroll:true});
}
function announce(next){status=next;update();}
function setFace(next,focus=true){
 intent++;if(next===face){if(focus&&next==='front')$('note-text').focus({preventScroll:true});return;}
 if(face==='front')remember();
 const previous=face;face=next;const token=++turn;
 const active=document.activeElement;
 if($('card-'+previous).contains(active)||active===$('saved-link')||active===document.querySelector('.brand'))$('flip').focus({preventScroll:true});
 $('card-front').inert=true;$('card-back').inert=true;
 $('card-front').setAttribute('aria-hidden','true');$('card-back').setAttribute('aria-hidden','true');
 $('note-card').dataset.face=next;$('note-card').dataset.motion='turning';update();
 const finish=()=>{
  if(token!==turn)return;
  $('note-card').dataset.motion='settled';
  $('card-front').inert=next!=='front';$('card-back').inert=next!=='back';
  $('card-front').setAttribute('aria-hidden',String(next!=='front'));$('card-back').setAttribute('aria-hidden',String(next!=='back'));
  if(!focus)return;
  // Do not steal focus if the person moved to a utility while the card turned.
  if(document.activeElement!==$('flip')&&!$('card-'+previous).contains(document.activeElement))return;
  if(next==='front'){
   if(!$('retry').hidden){$('retry').focus({preventScroll:true});return;}
   $('note-text').focus({preventScroll:true});$('note-text').setSelectionRange(selection.start,selection.end);$('note-text').scrollTop=selection.scroll;
  }else $('saved-text').focus({preventScroll:true});
 };
 // Native CSS reversal retains the current presentation. Animation promises follow the active turn.
 const animations=$('note-card').getAnimations();
 if(reduced.matches||!animations.length)setTimeout(finish,reduced.matches?110:0);
 else Promise.allSettled(animations.map(a=>a.finished)).then(finish);
}
function read(initial=false){
 try{
  const raw=localStorage.getItem(KEY),value=raw===null?null:JSON.parse(raw);
  if(value!==null&&(!value||value.id!=='heating-study'||typeof value.title!=='string'||typeof value.text!=='string'||value.text.length>600))throw Error('Invalid record');
  saved=value;storageReady=true;if(value&&!touched)$('note-text').value=value.text;
  if(!initial)status='read';
 }catch(e){storageReady=false;status='unavailable';}
 update();
}
function save(){
 if(pending||!storageReady)return;
 if($('note-text').value.length>600){announce('tooLong');$('note-text').focus();return;}
 remember();
 const record={id:'heating-study',title:t('question'),text:$('note-text').value};
 const attempt={record,intent,timer:null};pending=attempt;announce('saving');
 attempt.timer=setTimeout(()=>{
  if(pending!==attempt)return;
  try{
   localStorage.setItem(KEY,JSON.stringify(record));saved=record;pending=null;
   const unchanged=$('note-text').value===record.text;announce(unchanged?'saved':'earlier');
   if(unchanged&&face==='front'&&intent===attempt.intent)setFace('back');
  }catch(e){pending=null;announce('failed');}
 },900);
}
function clear(){
 if(pending)clearTimeout(pending.timer);pending=null;
 try{localStorage.removeItem(KEY);saved=null;storageReady=true;touched=false;$('note-text').value='';announce('cleared');setFace('front');}
 catch(e){announce('clearFailed');setFace('front');$('retry').focus({preventScroll:true});}
 update();
}
function renderLocale(){
 root.lang=locale==='zh'?'zh-CN':'en';document.title=locale==='en'?'Fieldnote · A place for an idea':'Fieldnote · 研究笔记';
 document.querySelectorAll('[data-i18n]').forEach(e=>e.textContent=t(e.dataset.i18n));
 if(locale==='zh')document.querySelectorAll('[data-i18n=question]').forEach(e=>e.textContent='城市如何降低\n高峰供热需求？');
 $('locale-toggle').textContent=locale==='en'?'中文':'EN';$('locale-toggle').setAttribute('aria-label',locale==='en'?'切换中文':'Switch to English');
 $('theme-toggle').setAttribute('aria-label',t(root.dataset.theme==='dark'?'light':'dark'));
 $('saved-text').setAttribute('aria-label',t('savedNotes'));
 update();
}
$('note-text').addEventListener('input',()=>{touched=true;if(!pending&&storageReady&&!['failed','clearFailed'].includes(status))status='edited';update();});
$('note-text').addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();save();}});
$('save').addEventListener('click',save);
$('retry').addEventListener('click',()=>{if(status==='failed')save();else if(status==='unavailable')read();else if(status==='clearFailed')clear();});
$('flip').addEventListener('click',()=>setFace(face==='front'?'back':'front'));
$('saved-link').addEventListener('click',()=>setFace('back'));
$('return').addEventListener('click',()=>setFace('front'));
$('clear').addEventListener('click',clear);
document.querySelector('.brand').addEventListener('click',e=>{e.preventDefault();setFace('front');});
$('locale-toggle').addEventListener('click',()=>{locale=locale==='en'?'zh':'en';renderLocale();});
$('theme-toggle').addEventListener('click',()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';renderLocale();});
reduced.addEventListener('change',()=>{
 turn++;$('note-card').dataset.motion='settled';
 $('card-front').inert=face!=='front';$('card-back').inert=face!=='back';
 $('card-front').setAttribute('aria-hidden',String(face!=='front'));$('card-back').setAttribute('aria-hidden',String(face!=='back'));
 if(document.activeElement===$('flip')){if(face==='back')$('saved-text').focus({preventScroll:true});else {$('note-text').focus({preventScroll:true});$('note-text').setSelectionRange(selection.start,selection.end);$('note-text').scrollTop=selection.scroll;}}
});
read(true);renderLocale();
})();
