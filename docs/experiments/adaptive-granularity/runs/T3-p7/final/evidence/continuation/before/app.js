(() => {
'use strict';
const $=id=>document.getElementById(id),root=document.documentElement,KEY='ui-spec-temporal-note-v1';
const C={en:{skip:'Skip to note',savedNotes:'Saved note',eyebrow:'A SMALL SPACE FOR BIG QUESTIONS',subject:'Energy & cities',pageTitle:'Keep an idea <br>in view.',intro:'A thought worth keeping. A question worth coming back to.',questionLabel:'YOUR QUESTION',question:'How can cities reduce peak heating demand?',localOnly:'Stored only in this browser',draft:'YOUR DRAFT',savedFace:'SAVED NOTE',noteLabel:'An idea in progress',noteHint:'Keep evidence and open questions together.',unsaved:'Not saved yet',changes:'Unsaved changes',unchanged:'Saved version',save:'Save note ↗',savingButton:'Saving…',savedTitle:'An idea, kept.',savedKicker:'Saved in this browser',edit:'Edit note ↶',viewSaved:'View saved note ↗',backDraft:'Back to your draft ↶',footer:'A little room to think.',settings:'Local demo',disclosure:'Saved notes stay in this browser. Unsaved drafts last until this page closes. Saving includes a short demo delay.',clear:'Clear saved note and draft',saving:'Saving in this browser… You can keep writing.',saved:'Note saved in this browser.',earlier:'Submitted version saved. Your newer edits are in the draft — save again to keep them.',edited:'Your changes have not been saved.',failed:'Could not save. Your draft is still here; the saved note is unchanged.',failedFirst:'Could not save. Your draft is still here.',retrySave:'Try saving again',unavailable:'Saved note could not be read. Your draft is still here.',retryRead:'Try reading again',clearFailed:'Could not clear the local note. Your draft is still here.',retryClear:'Try clearing again',cleared:'Saved note and draft cleared.',emptySaved:'This saved note is empty.',empty:'No saved note yet. Save your draft to keep it here.',read:'Saved note is available again.',dark:'Switch to dark theme',light:'Switch to light theme',limit:'{n} / 600',tooLong:'Shorten to 600 characters to save. All your text is still here.',pendingOld:'Saving a new version. This is your previous saved note.'},zh:{skip:'跳到笔记',savedNotes:'已存笔记',eyebrow:'给大问题，留一点空间',subject:'能源与城市',pageTitle:'让想法<br>留在眼前。',intro:'值得留下的想法，值得再想的问题。',questionLabel:'研究问题',question:'城市如何降低高峰供热需求？',localOnly:'仅保存在此浏览器',draft:'当前草稿',savedFace:'已存笔记',noteLabel:'正在形成的想法',noteHint:'把已有证据和待解问题放在一起。',unsaved:'尚未保存',changes:'有未保存的修改',unchanged:'已保存的版本',save:'保存笔记 ↗',savingButton:'正在保存…',savedTitle:'想法，已留下。',savedKicker:'已保存在此浏览器',edit:'编辑笔记 ↶',viewSaved:'查看已存笔记 ↗',backDraft:'返回草稿 ↶',footer:'给思考留一点空间。',settings:'本地演示',disclosure:'已存笔记仅保存在此浏览器。未保存的草稿会在关闭页面后丢失。保存过程含短暂的演示延迟。',clear:'清除已存笔记和草稿',saving:'正在保存到此浏览器… 可以继续编辑。',saved:'笔记已保存在此浏览器。',earlier:'提交的版本已保存。新的修改仍在草稿中，请再次保存。',edited:'修改尚未保存。',failed:'未能保存。草稿仍在，之前保存的笔记保持不变。',failedFirst:'未能保存。草稿仍在。',retrySave:'重试保存',unavailable:'无法读取已存笔记。草稿仍在。',retryRead:'重试读取',clearFailed:'无法清除本地笔记。草稿仍在。',retryClear:'重试清除',cleared:'已存笔记和草稿已清除。',emptySaved:'这条已存笔记为空。',empty:'还没有已存笔记。保存草稿后可在这里查看。',read:'已可读取保存的笔记。',dark:'切换深色主题',light:'切换浅色主题',limit:'{n} / 600 字',tooLong:'请缩短至 600 字以内再保存。所有输入仍保留。',pendingOld:'正在保存新版本。这里显示上次保存的笔记。'}};
let locale='en',saved=null,ready=false,pending=null,status='',face='front',touched=false,turn=0,focusTimer=null,selection={start:0,end:0,scroll:0};
const reduced=matchMedia('(prefers-reduced-motion: reduce)'),t=k=>C[locale][k];
$('note-text').value='Compare city demand patterns and check which evidence supports each explanation.';
root.dataset.theme=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
function render(){
 root.lang=locale==='en'?'en':'zh-CN';document.title=locale==='en'?'Fieldnote · A place for an idea':'Fieldnote · 给想法留个位置';
 document.querySelectorAll('[data-i18n]').forEach(e=>{if(e.id==='page-title')e.innerHTML=t(e.dataset.i18n);else e.textContent=t(e.dataset.i18n)});
 $('locale-toggle').textContent=locale==='en'?'中文':'EN';$('locale-toggle').setAttribute('aria-label',locale==='en'?'中文 · 切换中文':'EN · Switch to English');
 $('theme-toggle').setAttribute('aria-label',t(root.dataset.theme==='light'?'dark':'light'));$('card-front').setAttribute('aria-label',t('noteLabel'));$('card-back').setAttribute('aria-label',t('savedNotes'));document.querySelector('.note-workspace').setAttribute('aria-label',t('noteLabel'));
 $('face-label').textContent=t(face==='front'?'draft':'savedFace');$('flip').textContent=t(face==='front'?'viewSaved':'backDraft');$('flip').setAttribute('aria-pressed',String(face==='back'));
 $('flip').disabled=face==='front'&&(!saved||!ready)&&!$('card-space').classList.contains('turning');$('saved-link').disabled=!saved||!ready;
 $('save').textContent=t(pending?'savingButton':'save');$('save').disabled=!!pending||!ready||$('note-text').value.length>600;$('save').setAttribute('aria-busy',String(!!pending));
 $('saved-text').textContent=saved?(saved.text||t('emptySaved')):t('empty');$('saved-kicker').textContent=t(pending&&saved?'pendingOld':'savedKicker');
 $('note-limit').textContent=t('limit').replace('{n}',$('note-text').value.length);const over=$('note-text').value.length>600;$('note-text').setAttribute('aria-invalid',String(over));document.querySelector('.editor-meta').dataset.over=String(over);
 $('draft-state').textContent=t(!saved?'unsaved':saved.text===$('note-text').value?'unchanged':'changes');
 $('status').textContent=over?t('tooLong'):status?t(status==='failed'&&!saved?'failedFirst':status):'';$('status-area').dataset.status=status;
 const retryWasFocused=document.activeElement===$('retry');const actions={failed:'retrySave',unavailable:'retryRead',clearFailed:'retryClear'};$('retry').hidden=!actions[status];if(actions[status])$('retry').textContent=t(actions[status]);if(retryWasFocused&&$('retry').hidden){if(face==='front'&&!$('card-front').inert)$('note-text').focus({preventScroll:true});else if(!$('flip').disabled)$('flip').focus({preventScroll:true});}
 document.querySelectorAll('.face-dots i').forEach((e,i)=>e.classList.toggle('active',i===(face==='back'?1:0)));
}
function announce(s){status=s;render()}
function finish(id){if(id!==turn)return;$('card-space').classList.remove('turning');$('card-front').inert=face!=='front';$('card-back').inert=face!=='back';if(document.activeElement===$('flip')){if(face==='front'){$('note-text').focus({preventScroll:true});$('note-text').setSelectionRange(selection.start,selection.end);$('note-text').scrollTop=selection.scroll;}else $('saved-title').focus({preventScroll:true});}render();}
function setFace(next){
 if(next==='back'&&(!saved||!ready))return;
 if(next===face)return;
 if(face==='front')selection={start:$('note-text').selectionStart,end:$('note-text').selectionEnd,scroll:$('note-text').scrollTop};
 face=next;const id=++turn;clearTimeout(focusTimer);
 $('flip').disabled=false;$('flip').focus({preventScroll:true});
 $('card-front').inert=true;$('card-back').inert=true;$('card-front').setAttribute('aria-hidden',String(face!=='front'));$('card-back').setAttribute('aria-hidden',String(face!=='back'));
 $('card-space').classList.add('turning');$('note-card').dataset.face=face;render();
 if(reduced.matches)finish(id);else focusTimer=setTimeout(()=>finish(id),720);
}
$('note-card').addEventListener('transitionend',e=>{if(e.target===$('note-card')&&e.propertyName==='transform'){clearTimeout(focusTimer);finish(turn)}});
function read(initial=false){try{const raw=localStorage.getItem(KEY),v=raw===null?null:JSON.parse(raw);if(v!==null&&(!v||v.id!=='heating-study'||typeof v.title!=='string'||typeof v.text!=='string'||v.text.length>600))throw Error('Invalid record');saved=v;ready=true;if(saved&&!touched)$('note-text').value=saved.text;if(!initial)status='read';}catch(_){ready=false;status='unavailable'}render()}
function save(){
 if(pending||!ready)return;if($('note-text').value.length>600){announce('tooLong');return}
 const record={id:'heating-study',title:t('question'),text:$('note-text').value};const attempt={record,timer:null,turn};pending=attempt;announce('saving');
 attempt.timer=setTimeout(()=>{if(pending!==attempt)return;try{localStorage.setItem(KEY,JSON.stringify(record));saved=record;pending=null;const same=$('note-text').value===record.text;announce(same?'saved':'earlier');if(same&&turn===attempt.turn)setFace('back')}catch(_){pending=null;announce('failed');if(face==='front'&&document.activeElement===$('save'))$('retry').focus({preventScroll:true})}},650);
}
function clear(){if(pending)clearTimeout(pending.timer);pending=null;try{localStorage.removeItem(KEY);if(face==='back')setFace('front');saved=null;ready=true;touched=false;document.querySelector('details').open=false;$('note-text').value='';announce('cleared')}catch(_){announce('clearFailed')}if(face==='front'&&!$('card-space').classList.contains('turning'))$('note-text').focus({preventScroll:true})}
$('note-text').addEventListener('input',()=>{touched=true;if(!pending&&!['failed','unavailable','clearFailed'].includes(status))status='edited';render()});
$('save').addEventListener('click',save);$('retry').addEventListener('click',()=>{if(status==='failed')save();else if(status==='unavailable')read();else if(status==='clearFailed')clear()});
$('flip').addEventListener('click',()=>setFace(face==='front'?'back':'front'));$('return').addEventListener('click',()=>setFace('front'));$('saved-link').addEventListener('click',()=>setFace('back'));$('clear').addEventListener('click',clear);
$('locale-toggle').addEventListener('click',()=>{locale=locale==='en'?'zh':'en';render()});$('theme-toggle').addEventListener('click',()=>{root.dataset.theme=root.dataset.theme==='light'?'dark':'light';render()});document.querySelector('.brand').addEventListener('click',e=>{e.preventDefault();setFace('front')});
$('note-text').addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();save()}});
reduced.addEventListener('change',()=>{if(reduced.matches){clearTimeout(focusTimer);finish(turn)}});
document.querySelector('.skip').addEventListener('click',e=>{if(face==='back'){e.preventDefault();setFace('front')}});
read(true);
})();
