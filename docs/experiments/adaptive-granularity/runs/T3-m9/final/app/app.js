/* Fieldnote. Storage confirms success; the card only presents that confirmed state. */
(() => {
'use strict';
const $ = id => document.getElementById(id), root=document.documentElement;
const LEGACY_KEY='ui-spec-temporal-note-v1', KEY='fieldnote-collection-v1';
const copy={
en:{edition:'A little room to think.',eyebrow:'ONE QUESTION. A FEW GOOD NOTES.',pageTitle:'Keep an idea<br> in view.',intro:'A place for the evidence, the loose ends, and what you want to find out next.',subject:'ENERGY / CITIES',question:'How can cities reduce peak heating demand?',localOnly:'Your note stays in this browser.',fieldnote:'FIELDNOTE No. 001',yourNote:'YOUR RESEARCH NOTE',editorTitle:'Follow the thought.',noteLabel:'Your research note',noteHint:'Evidence, questions, next steps.',save:'Save note',return:'Keep editing',shortcut:'⌘ / Ctrl + Enter to save',disclosure:'Local demo · A small space for an unfinished thought.',controls:'About this demo',delay:'Notes save only in this browser, with a 0.9 second demo delay. Unsaved edits remain here until you reload.',clear:'Clear local note',draft:'Draft',savedFace:'Saved note',viewSaved:'View saved note ↗',backDraft:'Back to draft ↶',none:'No saved note yet',savedKicker:'SAVED IN THIS BROWSER',savedTitle:'An idea to return to.',saving:'Saving in this browser…',saved:'Saved in this browser. Ready when you are.',earlier:'Submitted version saved. Your newer edits are still a draft.',edited:'Unsaved changes.',failed:'Couldn’t save this note. Your draft is still here.',unavailable:'Couldn’t read the saved note. Retry reading or clear local data to continue.',clearFailed:'Couldn’t clear the note. Your saved note and draft are still here.',cleared:'Local note cleared.',read:'Saved note is available again.',retrySave:'Try saving again',retryRead:'Try reading again',retryClear:'Try clearing again',tooLong:'Over the 600-character limit. Shorten your note to save; your text is still here.',empty:'Nothing saved yet.',emptyHint:'Return to your draft and save a note.',unknown:'Saved note unavailable.',dark:'Switch to dark theme',light:'Switch to light theme',date:'Saved',limit:'characters',savingButton:'Saving…',editing:'Draft / unsaved changes'},
zh:{edition:'留一点空间，好好想。',eyebrow:'一个问题，几条值得留下的笔记。',pageTitle:'让想法<br>留在眼前。',intro:'记录证据、未解的问题，以及下一步想探究的方向。',subject:'能源 / 城市',question:'城市如何降低高峰供热需求？',localOnly:'笔记仅保存在此浏览器。',fieldnote:'研究笔记 No. 001',yourNote:'你的研究笔记',editorTitle:'顺着思路，继续写。',noteLabel:'研究笔记',noteHint:'证据、问题、下一步。',save:'保存笔记',return:'继续编辑',shortcut:'⌘ / Ctrl + Enter 保存',disclosure:'本地演示 · 为未完成的想法留个位置。',controls:'关于此演示',delay:'笔记仅保存在此浏览器。保存含 0.9 秒演示延迟。刷新页面前，未保存的修改会保留在这里。',clear:'清除本地笔记',draft:'草稿',savedFace:'已存笔记',viewSaved:'查看已存笔记 ↗',backDraft:'返回草稿 ↶',none:'还没有已存笔记',savedKicker:'已保存在此浏览器',savedTitle:'留待回看的想法。',saving:'正在保存到此浏览器…',saved:'已保存在此浏览器，可随时回看。',earlier:'提交版本已保存，之后的修改仍为草稿。',edited:'修改尚未保存。',failed:'未能保存笔记，草稿仍保留在这里。',unavailable:'无法读取已存笔记。请重试读取，或清除本地数据后继续。',clearFailed:'无法清除笔记，已存笔记和草稿仍保留。',cleared:'本地笔记已清除。',read:'已重新读取笔记。',retrySave:'重试保存',retryRead:'重试读取',retryClear:'重试清除',tooLong:'超过 600 字限制。请缩短后保存，输入内容仍保留。',empty:'还没有已存笔记。',emptyHint:'返回草稿并保存笔记。',unknown:'暂时无法读取已存笔记。',dark:'切换深色主题',light:'切换浅色主题',date:'保存于',limit:'字',savingButton:'保存中…',editing:'草稿 / 尚未保存'}
};
Object.assign(copy.en,{allNotes:'All notes',collectionEyebrow:'YOUR BROWSER-LOCAL NOTEBOOK',collectionTitle:'Your fieldnotes.',collectionIntro:'Keep the useful pieces. Pick up the thread.',newNote:'＋ New note',collectionBoundary:'Saved here · Unsaved drafts last until reload',emptyCollection:'A little room for your first idea.',emptyCollectionHint:'No notes saved yet. Start a note and make it yours.',firstNote:'Write your first note ↗',backCollection:'← All notes',sessionDraft:'Draft · this session',tileSaved:'Saved in this browser',tileFailed:'Not saved · open to retry',tilePending:'Saving…',blankNote:'An empty page, ready for a thought.',notes:'notes',collectionFailed:'A note could not be saved. Open the marked card to retry.',waiting:'Another note is saving…'});
Object.assign(copy.zh,{allNotes:'全部笔记',collectionEyebrow:'此浏览器中的笔记本',collectionTitle:'你的研究笔记。',collectionIntro:'留下有用的线索，随时接着想。',newNote:'＋ 新建笔记',collectionBoundary:'本地保存 · 刷新后未存草稿将丢失',emptyCollection:'为第一个想法留个位置。',emptyCollectionHint:'还没有已存笔记，开始记录你的想法。',firstNote:'写下第一条笔记 ↗',backCollection:'← 全部笔记',sessionDraft:'草稿 · 本次会话',tileSaved:'已保存在此浏览器',tileFailed:'未保存 · 打开重试',tilePending:'保存中…',blankNote:'空白的一页，等待你的想法。',notes:'条笔记',collectionFailed:'有笔记未能保存。请打开标记的卡片重试。',waiting:'另一条笔记正在保存…'});
let records=[],currentId=null,collectionScroll=0,routeEpoch=0,routeTransition=null;
const drafts=new Map(),states=new Map(),tiles=new Map();
let locale='en',face='front',status='',saved=null,ready=false,pending=null,touched=false,epoch=0,focusIntent=null,selection={start:0,end:0,scroll:0};
const reduced=matchMedia('(prefers-reduced-motion: reduce)'),systemDark=matchMedia('(prefers-color-scheme: dark)');
root.dataset.theme=systemDark.matches?'dark':'light';
const t=k=>copy[locale][k];
$('note-text').value='';
function render(){
 saved=records.find(n=>n.id===currentId)||null;
 const pendingHere=pending?.record.id===currentId;
 const text=$('note-text').value,over=text.length>600;
 $('note-limit').textContent=`${text.length} / 600`; $('note-limit').dataset.overLimit=String(over);
 $('note-text').setAttribute('aria-invalid',String(over));
 $('save').disabled=!!pending||!ready||over; $('save').setAttribute('aria-busy',String(!!pendingHere));
 $('save').firstElementChild.textContent=t(pendingHere?'savingButton':pending?'waiting':'save');
 $('note-card').classList.toggle('is-saving',!!pendingHere);
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
 if(wasRetry&&!retry&&!$('main').hidden)$('save').focus({preventScroll:true});
 const note=drafts.get(currentId)||saved; $('note-number').textContent=(locale==='zh'?'研究笔记 No. ':'FIELDNOTE No. ')+String(note?.serial||1).padStart(3,'0');
 $('note-card').dataset.recordId=currentId||'';
 $('clear').hidden=$('main').hidden;
 renderCollection();
}
function announce(next){status=next;render()}
function finishFocus(){
 if(!focusIntent||$('main').hidden)return;
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
function remember(){
 if(!currentId)return;const old=drafts.get(currentId)||saved||{};
 drafts.set(currentId,{...old,id:currentId,text:$('note-text').value,selection:{start:$('note-text').selectionStart,end:$('note-text').selectionEnd,scroll:$('note-text').scrollTop}});
 states.set(currentId,status);
}
function renderCollection(){
 const items=new Map(records.map(n=>[n.id,n]));for(const [id,n] of drafts)items.set(id,n);
 const ordered=[...items.values()].sort((a,b)=>a.serial-b.serial);
 const draftCount=[...drafts.values()].filter(d=>!records.some(n=>n.id===d.id&&n.text===d.text)).length;
 $('note-count').textContent=!ready?(locale==='zh'?'暂时无法读取':'Collection unavailable'):locale==='zh'?`${records.length} 条已存${draftCount?' · '+draftCount+' 条草稿':''}`:`${records.length} saved${draftCount?' · '+draftCount+' drafts':''}`;
 $('empty-state').hidden=ordered.length>0||!ready;
 $('new-note').disabled=!ready;$('empty-new').disabled=!ready;
 $('collection-retry').hidden=ready;
 $('collection-status').textContent=!ready?t('unavailable'):[...states.values()].includes('failed')?t('collectionFailed'):'';
 for(const n of ordered){
  let tile=tiles.get(n.id);
  if(!tile){tile=document.createElement('button');tile.type='button';tile.className='note-tile';tile.dataset.noteId=n.id;tile.innerHTML='<span class="tile-top"><span class="label"></span><span aria-hidden="true">↗</span></span><span class="tile-text"></span><span class="tile-state"></span>';tile.addEventListener('click',()=>openNote(n.id));tiles.set(n.id,tile);$('note-grid').append(tile)}
  const persisted=records.find(r=>r.id===n.id),failed=states.get(n.id)==='failed';
  tile.querySelector('.label').textContent=`No. ${String(n.serial).padStart(3,'0')}`;
  tile.querySelector('.tile-text').textContent=n.text||t('blankNote');
  tile.querySelector('.tile-state').textContent=t(pending?.record.id===n.id?'tilePending':failed?'tileFailed':!persisted||persisted.text!==n.text?'sessionDraft':'tileSaved');
  tile.classList.toggle('selected',n.id===currentId);tile.classList.toggle('failed',failed);
  tile.setAttribute('aria-label',`${locale==='zh'?'打开笔记':'Open note'} ${n.serial}: ${n.text.slice(0,90)||t('blankNote')}`);
 }
 for(const [id,tile] of tiles)if(!items.has(id)){tile.remove();tiles.delete(id)}
}
function navigate(update,focus){
 const token=++routeEpoch;routeTransition?.skipTransition();
 const apply=()=>{if(token===routeEpoch)update()};
 if(reduced.matches||!document.startViewTransition){apply();focus();return}
 const vt=document.startViewTransition(apply);routeTransition=vt;vt.ready.catch(()=>{});vt.finished.then(()=>{if(token===routeEpoch){routeTransition=null;focus()}}).catch(()=>{});
}
function loadNote(id){
 currentId=id;saved=records.find(n=>n.id===id)||null;
 const draft=drafts.get(id)||saved;drafts.set(id,{...draft});
 $('note-text').value=draft.text;selection=draft.selection||{start:0,end:0,scroll:0};touched=!saved||draft.text!==saved.text;status=states.get(id)|| (touched?'edited':'');
 focusIntent=null;face='front';epoch++;
 $('note-card').classList.add('resetting');$('note-card').dataset.face='front';$('card-front').inert=false;$('card-back').inert=true;$('card-front').setAttribute('aria-hidden','false');$('card-back').setAttribute('aria-hidden','true');
 render();void $('note-card').offsetWidth;$('note-card').classList.remove('resetting');
}
function openNote(id){
 if(!$('main').hidden)remember();else collectionScroll=scrollY;
 for(const tile of tiles.values())tile.style.viewTransitionName='none';
 if(tiles.has(id))tiles.get(id).style.viewTransitionName='active-note';
 navigate(()=>{loadNote(id);$('collection').hidden=true;$('main').hidden=false;$('clear').hidden=false;scrollTo(0,0)},()=>{focusIntent='editor';finishFocus()});
}
function showCollection(){
 if($('main').hidden)return;remember();epoch++;focusIntent=null;renderCollection();
 for(const [id,tile] of tiles)tile.style.viewTransitionName=id===currentId?'active-note':'none';
 navigate(()=>{$('main').hidden=true;$('collection').hidden=false;$('clear').hidden=true;scrollTo(0,collectionScroll)},()=>{(tiles.get(currentId)||$('collection-title')).focus({preventScroll:true})});
}
function createNote(){
 if(!ready)return;const serial=Math.max(0,...records.map(n=>n.serial),...[...drafts.values()].map(n=>n.serial))+1;
 const id=crypto.randomUUID();drafts.set(id,{id,serial,text:'',title:t('question'),createdAt:new Date().toISOString()});renderCollection();openNote(id);
}
function valid(n){return n&&typeof n.id==='string'&&typeof n.title==='string'&&typeof n.text==='string'&&n.text.length<=600}
function read(initial=false){
 try{
  const raw=localStorage.getItem(KEY);let values;
  if(raw===null){const legacy=localStorage.getItem(LEGACY_KEY);const v=legacy?JSON.parse(legacy):null;if(v&&!valid(v))throw Error('Invalid legacy note');values=v?[{...v,serial:1}]:[]}
  else values=JSON.parse(raw);
  if(!Array.isArray(values)||values.some(n=>!valid(n))||new Set(values.map(n=>n.id)).size!==values.length)throw Error('Invalid collection');
  records=values.map((n,i)=>({...n,serial:Number.isInteger(n.serial)&&n.serial>0?n.serial:i+1}));ready=true;
  if(!initial)announce('read');else render();
 }catch(e){ready=false;announce('unavailable')}
}
function save(){
 if(pending||!ready||!currentId)return;
 if($('note-text').value.length>600){announce('tooLong');$('note-text').focus();return}
 remember();const draft=drafts.get(currentId);
 const record={id:currentId,serial:draft.serial,title:t('question'),text:$('note-text').value,createdAt:draft.createdAt||new Date().toISOString(),updatedAt:new Date().toISOString()};
 const attempt={record,epoch,timer:null};pending=attempt;states.set(currentId,'saving');announce('saving');
 attempt.timer=setTimeout(()=>{
  if(pending!==attempt)return;
  try{
   const next=records.some(n=>n.id===record.id)?records.map(n=>n.id===record.id?record:n):[...records,record];
   localStorage.setItem(KEY,JSON.stringify(next));records=next;pending=null;
   const text=currentId===record.id?$('note-text').value:drafts.get(record.id)?.text;
   const unchanged=text===record.text;states.set(record.id,unchanged?'saved':'earlier');
   if(currentId===record.id){announce(unchanged?'saved':'earlier');if(unchanged&&epoch===attempt.epoch&&!$('main').hidden){touched=false;turn('back','saved')}}else render();
  }catch(e){pending=null;states.set(record.id,'failed');if(currentId===record.id){announce('failed');if(face==='back')turn('front','editor')}else render()}
 },900);
}
function clear(){
 if(!currentId)return;const id=currentId;
 if(pending?.record.id===id){clearTimeout(pending.timer);pending=null}
 try{const next=records.filter(n=>n.id!==id);localStorage.setItem(KEY,JSON.stringify(next));records=next;drafts.delete(id);states.delete(id);currentId=null;saved=null;$('note-text').value='';ready=true;status='cleared';$('main').hidden=true;$('collection').hidden=false;render();$('collection-title').focus()}
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
$('note-text').addEventListener('input',()=>{touched=true;if(!pending&&ready&&!['failed','clearFailed'].includes(status))status=$('note-text').value.length>600?'tooLong':'edited';remember();render()});
$('save').addEventListener('click',save);
$('flip').addEventListener('click',()=>turn(face==='front'?'back':'front'));
$('return').addEventListener('click',()=>turn('front','editor'));
$('retry').addEventListener('click',()=>{if(status==='failed')save();else if(status==='unavailable')read();else if(status==='clearFailed')clear()});
$('clear').addEventListener('click',clear);
$('theme-toggle').addEventListener('click',()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';localize()});
$('locale-toggle').addEventListener('click',()=>{locale=locale==='en'?'zh':'en';localize()});
$('note-text').addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();save()}});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('main').hidden){e.preventDefault();if(face==='back')turn('front','editor');else showCollection()}});
 document.querySelector('.brand').addEventListener('click',e=>{e.preventDefault();showCollection()});
 $('all-notes').addEventListener('click',showCollection);$('back-collection').addEventListener('click',showCollection);$('new-note').addEventListener('click',createNote);$('empty-new').addEventListener('click',createNote);$('collection-retry').addEventListener('click',()=>read());
 const syncMotion=()=>{root.classList.toggle('is-reduced',reduced.matches);if(reduced.matches)finishFocus()};reduced.addEventListener('change',syncMotion);
 syncMotion();read(true);localize();
})();
