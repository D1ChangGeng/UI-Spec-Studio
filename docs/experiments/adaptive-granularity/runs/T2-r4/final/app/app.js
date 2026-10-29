/* Meridian's local fixture adapter. No network requests or file reads.
 * Cancellation ownership extends the token/timer approach in the supplied
 * reference-project/app.js; thread, streaming and persistence state are new. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const root = document.documentElement, reader = $('reader');
  const KEY = 'meridian-workspace-v1';
  const mobile = matchMedia('(max-width:700px)'), modalSource = matchMedia('(max-width:1100px)');
  let state = {threads: [], activeId: ''}, timer = null, requestToken = 0, generation = null;
  let saveTimer, lastSourceTrigger, sourceProfile = 'heat', sourceIndex = 0, sourceContext = null;
  const id = () => 'm' + Date.now().toString(36) + Math.random().toString(36).slice(2,7);
  const svg = name => `<svg aria-hidden="true"><use href="#i-${name}"/></svg>`;
  const profiles = {
    heat: {title:'A cooler city starts at street level.', short:'A cooler city', prompt:'How can cities cool down without using more energy?',
      intro:'Begin with the places where people spend time: the walk to a bus stop, a school courtyard, a small square. A useful cooling strategy brings shade, water and living ground into these everyday spaces.',
      sections:[['Start with shade, then connect it','Think in routes as well as destinations. A leafy park is more useful when people can reach it along shaded streets. Prioritize the gaps between homes, schools, shops and public transport before adding isolated green spaces.'],['Make room for living ground','Trees need room below the pavement as well as above it. Combine planting with permeable surfaces and rainwater capture, then give maintenance a place in the plan from the beginning. The design should work through both dry and wet seasons.'],['Measure the experience, not just the map','A practical pilot compares a few places through the day. Record shade, surface conditions and how people use each space. Pair measurements with conversations about who can rest, wait and move comfortably.']],
      quote:'The useful question is not “How many trees?” but “Where can someone find relief?”',
      ending:'A good next step is to choose one neighborhood route and map its exposed sections, gathering places and maintenance constraints. That turns a broad ambition into a specific, testable first project.',
      sources:[['Cooling streets','A field guide to everyday shade','Start with a familiar route','A street is a sequence of small experiences. The shade at a crossing, a place to sit and the walk between them deserve to be considered together.'],['Living ground','Notes on soil, water and planting','Design beyond the tree canopy','A planting plan also depends on soil volume, water and long-term care. This illustrative note connects visible landscape decisions with the systems below them.'],['Neighborhood notes','A simple observation notebook','Compare before scaling','Observe the same locations at different times and invite the people who use them to describe the difficult parts of a journey. A small pilot can reveal where a larger plan needs to change.']]},
    energy: {title:'Storage is a question of time.',short:'Storing tomorrow’s energy',prompt:'Where does long-duration energy storage fit?',
      intro:'The starting point is the gap you need to bridge. Moving solar energy into the evening is a different task from preparing for several days of low renewable output. Those tasks should be compared on their own terms.',
      sections:[['Name the job before the technology','Describe the power required, the length of each discharge and how often the system will be used. A technology that suits frequent short cycles may be a poor fit for occasional extended operation.'],['Look at the whole system','Compare storage with flexible demand, transmission and a mix of generation. The most useful option depends on what the surrounding system already provides, and on which constraint is genuinely difficult to meet.'],['Keep the operating assumptions visible','Costs depend on use, lifetime, efficiency and the value of reliability. Keep those assumptions beside the comparison so that an attractive headline figure does not quietly decide the outcome.']],
      quote:'A useful comparison begins with the service needed, then asks what can provide it.',
      ending:'For a first study, write two scenarios: one evening shift and one extended low-output period. Compare the same candidate options against both, and note which assumptions change the result.',
      sources:[['Time & energy','A storage planning workbook','Choose the duration deliberately','This fictional workbook groups storage needs by the service delivered. It emphasizes discharge length, repetition and the surrounding energy system.'],['System choices','Comparing flexibility options','Widen the comparison','Demand flexibility and connections to neighboring systems can change the job storage must do. The options should be compared using a consistent service definition.'],['Assumptions log','An illustrative evaluation template','Make the model inspectable','Record the assumptions that drive a comparison, identify which are uncertain, and revisit them when conditions change.']]},
    walk: {title:'Walkability is a chain of small invitations.',short:'A neighborhood on foot',prompt:'What makes a neighborhood worth walking through?',
      intro:'A pleasant walk depends on more than distance. A useful destination, an understandable route and somewhere to pause all help the journey feel worthwhile. Study those relationships together.',
      sections:[['Put everyday destinations within reach','Begin with the trips people already need to make. Look at the connection between homes, groceries, schools, parks and transit, rather than treating walking as a separate leisure activity.'],['Make the difficult moments easier','Crossings, narrow pavements and exposed waits can determine whether a whole route feels usable. Pay attention to the experience of someone moving slowly, pushing a stroller or using a mobility aid.'],['Leave space for life along the way','A bench, a tree, a visible doorway and a lively ground floor create reasons to stay. Useful streets let people move through and spend time without those activities constantly competing.']],
      quote:'A route feels walkable when its least comfortable part still welcomes you.',
      ending:'Choose a short everyday trip and walk it at different times. Note where you hesitate, where you would stop and what makes each crossing feel clear. Use those observations to set the first design priorities.',
      sources:[['Everyday routes','A walking study notebook','Start with an ordinary trip','This fictional notebook follows everyday journeys and records comfort, clarity and useful destinations along the way.'],['A place to pause','Notes on the public realm','Pay attention to the edges','The small spaces beside a route can make it welcoming. This synthetic excerpt considers shade, seating and visible activity.'],['Street observations','An inclusive review checklist','Look from different perspectives','Different walking speeds and mobility needs reveal different barriers. The same route should be considered from more than one point of view.']]},
    general: {title:'Give the question a useful shape.',short:'A new line of inquiry',
      intro:'This local demo cannot research a new topic, but it can show a useful path through it: define what you need to decide, collect comparable evidence and keep uncertainty visible.',
      sections:[['Set a clear boundary','Name the decision, the people affected and the time horizon. A smaller, well-defined question is easier to test than a broad topic with an implied answer.'],['Compare explanations, not just examples','Look for the mechanism behind a claim. Ask what else could explain the same observation and what evidence would distinguish the alternatives.'],['Keep a record of what could change your mind','Separate observations, assumptions and interpretations. A useful synthesis explains both its current conclusion and the missing evidence that could revise it.']],
      quote:'The next good question often matters more than the first confident answer.',
      ending:'Try a follow-up that narrows the audience, place or decision. In this demonstration, the response remains an authored example; no live sources have been retrieved.',
      sources:[['Question notes','An illustrative research framework','Define the decision','A research question becomes useful when it connects to a decision or an understanding the reader can act on.'],['Evidence notes','A comparison worksheet','Preserve the alternatives','This synthetic source encourages comparing explanations against the same observations, while tracking important differences in context.'],['Uncertainty log','A record of open questions','Keep revision possible','An honest summary makes room for the evidence that is still missing and names a useful next step.']]}
  };
  function profileFor(text) {
    const q = text.toLowerCase();
    if (/solar|batter|storage|energy storage|duration/.test(q)) return 'energy';
    if (/walk|neighbo|pedestrian/.test(q)) return 'walk';
    if (/cool|heat|cities|trees|shade|nature|climate/.test(q)) return 'heat';
    return 'general';
  }
  function current() { return state.threads.find(t => t.id === state.activeId); }
  function announce(text) { $('feedback').textContent = text; }
  function save() {
    clearTimeout(saveTimer);
    try { localStorage.setItem(KEY,JSON.stringify(state)); }
    catch { announce('Browser storage is unavailable. This session is still usable.'); }
  }
  function scheduleSave() { clearTimeout(saveTimer); saveTimer=setTimeout(save,180); }
  function createThread() {
    return {id:id(),title:'New thread',messages:[],draft:'',files:[],scroll:0,created:Date.now()};
  }
  try {
    const s=JSON.parse(localStorage.getItem(KEY)||'null');
    if (s && Array.isArray(s.threads) && s.threads.every(t=>t.id && Array.isArray(t.messages))) state=s;
  } catch { /* Start clean if the local record is unreadable. */ }
  if (!current()) { const t=createThread();state.threads.push(t);state.activeId=t.id; }
  for (const t of state.threads) for (const m of t.messages) {
    if (m.status==='pending'||m.status==='streaming') m.status='stopped';
  }
  function make(tag,className,text) { const n=document.createElement(tag);if(className)n.className=className;if(text!==undefined)n.textContent=text;return n; }
  function button(label,action,cls) { const n=make('button',cls,label);n.type='button';n.onclick=action;return n; }
  function rememberDraft() { const t=current();t.draft=$('question').value;t.scroll=reader.scrollTop;scheduleSave(); }
  function updateControls() {
    const running=generation && generation.threadId===state.activeId;
    $('send').hidden=!!running;$('stop').hidden=!running;
    $('send').disabled=!$('question').value.trim();
  }
  function resizeFallback() {
    if (!CSS.supports('field-sizing','content')) {
      $('question').style.height='auto';
      $('question').style.height=Math.min($('question').scrollHeight,mobile.matches?125:170)+'px';
    }
  }
  function renderHistory() {
    const term=$('thread-search').value.toLowerCase(), list=$('history-list');list.replaceChildren();
    const threads=state.threads.filter(t=>(t.messages.length || t.draft?.trim() || t.files?.length) && !t.example).slice().reverse();
    for (const t of threads.filter(t=>(t.title+' '+t.draft).toLowerCase().includes(term))) {
      const title=t.messages.length?t.title:(t.draft?.trim().split('\n')[0]||'Untitled draft');
      const b=button(title,()=>switchThread(t.id),'history-item'+(t.id===state.activeId?' active':''));
      b.title=title;if(t.id===state.activeId)b.setAttribute('aria-current','page');
      const count=t.messages.filter(m=>m.role==='user').length;
      b.append(make('small','',count?count+' question'+(count===1?'':'s'):'Draft'));list.append(b);
    }
    $('history-empty').hidden=!!list.children.length;
    $('history-empty').textContent=term?'No matching threads.':'A place to return to your questions.';
  }
  function renderAttachments() {
    const holder=$('attachment-chips');holder.replaceChildren();holder.hidden=!current().files.length;
    current().files.forEach((name,i)=>{
      const chip=make('div','attachment-chip'),span=make('span','',name);span.title=name;
      const remove=button('',()=>{current().files.splice(i,1);renderAttachments();save();$('attach').focus();});remove.innerHTML=svg('x');remove.setAttribute('aria-label','Remove '+name);chip.append(span,remove);holder.append(chip);
    });
  }
  function buildBlocks(key,long=false,follow=false) {
    const p=profiles[key],blocks=[];
    const add=(tag,text)=>blocks.push({tag,text,visible:''});
    add('h2',follow?'A closer look at the same question':p.title);
    add('p',follow?'Continuing this illustrative thread, the most useful next step is to make the comparison specific. Here is the same framework with the practical choices brought forward.':p.intro);
    p.sections.forEach(([h,t])=>{add('h3',h);add('p',t);});
    add('blockquote',p.quote);add('p',p.ending);
    if(long) {
      const extra=[['A practical first pass','Write down what you know, what you assume and what you still need to learn. Keep those categories separate. Compare a modest pilot with a broader rollout, and identify the parts that are easy to reverse.'],['The questions behind the decision','Who benefits first? Who carries the cost or maintenance work? What changes across seasons, locations or patterns of use? These questions help turn a general proposal into a useful conversation.'],['Look for the difficult case','A promising idea deserves to be examined where it is least likely to work. Use that case to understand its limits, rather than relying only on an appealing example.'],['Keep the next step small enough to learn from','Choose an experiment with a clear observation period, a responsible owner and a way to record what changed. Decide in advance what result would support expansion and what would call for a different approach.']];
      const details=[
        'Choose a manageable place to begin and describe what a useful outcome would look like. Invite the people who will live with the decision to help define that outcome. Their experience can reveal constraints that a broad plan would otherwise miss.',
        'Keep a short record of the tradeoffs. When one option improves comfort but adds maintenance, make both sides visible. A comparison becomes more useful when it explains what has to remain true for the preferred option to work.',
        'Seek out an example that challenges the initial idea. Compare its context with the more promising cases: the available resources, the people involved and the conditions over time. A difference between those cases can be a useful clue, rather than a reason to dismiss either one.',
        'Return to the original question after the first observation period. Keep what the evidence supports, revise the parts that did not hold, and decide whether the next step should be larger, smaller or simply different. Learning is part of the outcome.'
      ];
      extra.forEach(([h,t],i)=>{add('h3',h);add('p',t);add('p',details[i]);});
    }
    return blocks;
  }
  function makeMessage(m) {
    if(m.role==='user') {
      const n=make('div','message user',m.text);n.dataset.message=m.id;
      if(m.files?.length){const f=make('div','user-files');for(const name of m.files)f.append(make('span','file-label',name));n.append(f);}return n;
    }
    const a=make('article','message answer');a.dataset.message=m.id;a.setAttribute('aria-label','Meridian illustrative answer');
    const byline=make('div','answer-byline');byline.innerHTML='<span class="answer-mark" aria-hidden="true">m</span><span>Meridian</span><small>ILLUSTRATIVE ANSWER</small>';a.append(byline);
    const content=make('div','answer-content');
    for(const [i,b] of (m.blocks||[]).entries()) {const n=make(b.tag,'',b.visible);n.dataset.block=i;n.dataset.anchor=m.id+'-'+i;n.dataset.empty=String(!b.visible);if(b.visible===b.text)addInlineCitation(m,i,n);if(sourceContext?.messageId===m.id&&sourceContext.blockIndex===i)n.classList.add('cited-paragraph');content.append(n);}
    a.append(content);a.append(make('div','answer-footer'));updateFooter(m,a);return a;
  }
  function messageNode(m) {return document.querySelector(`[data-message="${m.id}"]`);}
  function addInlineCitation(m,index,node){
    const source=[3,5,7].indexOf(index);if(source<0||node.querySelector('.inline-citation'))return;
    const b=button(String(source+1),()=>openSource(m.profile,source,b,m,index),'inline-citation');
    b.dataset.citation=m.id+'-'+index;b.setAttribute('aria-label',`Read source ${source+1} for this paragraph`);node.append(document.createTextNode(' '),b);
  }
  function updateFooter(m,node=messageNode(m)) {
    if(!node)return;const f=node.querySelector('.answer-footer');f.replaceChildren();
    node.dataset.status=m.status;
    if(m.status==='pending'||m.status==='streaming'){
      const line=make('div','pending-label');line.append(make('span','pending-dot'),make('span','',m.status==='pending'?'Considering your question…':'Writing your answer…'));f.append(line);return;
    }
    if(m.status==='error'||m.status==='stopped') {
      const box=make('div','answer-state');box.append(make('strong','',m.status==='error'?'A small interruption.':'Response stopped.'));
      box.append(make('p','',m.status==='error'?'This simulated failure kept your question intact. Try again to continue.':'The text so far is yours to read. You can try again or ask a new question.'));
      const retry=button('Try again',()=>retryMessage(m));retry.insertAdjacentHTML('afterbegin',svg('retry'));box.append(retry);f.append(box);return;
    }
    const row=make('div','sources-row');
    profiles[m.profile].sources.forEach((s,i)=>{
      const b=button('',()=>openSource(m.profile,i,b,m,3+i*2),'source-chip');b.append(make('span','source-number',String(i+1)),document.createTextNode(s[0]));b.setAttribute('aria-label',`Read illustrative source ${i+1}: ${s[0]}`);row.append(b);
    });f.append(row);
    const actions=make('div','answer-actions');
    const copy=button('Copy',async()=>{try{await navigator.clipboard.writeText(m.blocks.map(b=>b.visible).join('\n\n'));announce('Answer copied.');}catch{announce('Copy is unavailable. You can select and copy the answer.');}});copy.insertAdjacentHTML('afterbegin',svg('copy'));
    const retry=button('Try again',()=>retryMessage(m));retry.insertAdjacentHTML('afterbegin',svg('retry'));
    actions.append(copy,retry,make('span','complete-note','3 illustrative sources · Local demo'));f.append(actions);
  }
  function renderThread(restore=true) {
    const t=current(),has=t.messages.length>0;$('workspace').classList.toggle('empty',!has);$('welcome').hidden=has;$('suggestions').hidden=has;
    $('thread-title').textContent=t.title;document.title=(has?t.title+' — ':'')+'Meridian';
    $('messages').replaceChildren(...t.messages.map(makeMessage));$('question').value=t.draft||'';
    renderAttachments();updateControls();resizeFallback();renderHistory();
    $('latest').hidden=true;announce('');
    if(restore) requestAnimationFrame(()=>{reader.scrollTop=t.scroll||0;updateLatest();});
    else {reader.scrollTop=0;updateLatest();}
  }
  function nearBottom(){return reader.scrollHeight-reader.scrollTop-reader.clientHeight<90;}
  function updateLatest() {$('latest').hidden=nearBottom()||!current().messages.length;}
  function toBottom(){reader.scrollTop=reader.scrollHeight;current().scroll=reader.scrollTop;updateLatest();}
  reader.addEventListener('scroll',()=>{current().scroll=reader.scrollTop;updateLatest();scheduleSave();},{passive:true});
  $('latest').onclick=toBottom;
  function finish(m,status) {
    clearTimeout(timer);generation=null;m.status=status;
    const heldAnchor=$('source-dialog').open?readingAnchor():null;
    if(messageNode(m))messageNode(m).style.minHeight='';
    messageNode(m)?.querySelector('.stream-active')?.classList.remove('stream-active');
    const follow=nearBottom()&&!$('source-dialog').open;updateFooter(m);updateControls();syncSourceState();if(follow)toBottom();else restoreAnchor(heldAnchor);save();
    announce(status==='complete'?'Answer ready. You can follow a source or keep exploring.':status==='error'?'The demo response failed. Try again is available.':'Response stopped.');
  }
  function stopGeneration(){
    requestToken++;clearTimeout(timer);
    if(generation){const t=state.threads.find(t=>t.id===generation.threadId);const m=t.messages.find(m=>m.id===generation.messageId);finish(m,'stopped');}
  }
  function startGeneration(m,mode='normal') {
    stopGeneration();const token=++requestToken;
    generation={threadId:state.activeId,messageId:m.id};m.responseMode=mode==='failure'?'normal':mode;m.status='pending';m.blocks=[];
    const old=messageNode(m),retainedHeight=$('source-dialog').open&&old?old.getBoundingClientRect().height:0;
    const fresh=makeMessage(m);if(retainedHeight)fresh.style.minHeight=retainedHeight+'px';
    if(old)old.replaceWith(fresh);else $('messages').append(fresh);updateControls();syncSourceState();if(!$('source-dialog').open)toBottom();save();
    announce('Your question is saved. Preparing an illustrative answer.');
    timer=setTimeout(()=>{
      if(token!==requestToken)return;
      if(mode==='failure'){finish(m,'error');return;}
      const t=current(),follow=t.messages.filter(x=>x.role==='user').length>1;
      m.blocks=buildBlocks(m.profile,mode==='long',follow);m.status='streaming';
      const n=messageNode(m);if(n){const next=makeMessage(m);if(retainedHeight)next.style.minHeight=retainedHeight+'px';n.replaceWith(next);}syncSourceState();
      let index=0,offset=0;
      function tick(){
        if(token!==requestToken)return;
        const b=m.blocks[index],words=b.text.match(/\S+\s*/g)||[],count=mode==='slow'?4:9;
        const chunk=words.slice(offset,offset+count).join('');offset+=count;b.visible+=chunk;
        const followLatest=nearBottom()&&!$('source-dialog').open,el=messageNode(m)?.querySelector(`[data-block="${index}"]`);
        if(el){el.dataset.empty='false';el.classList.add('stream-active');el.append(document.createTextNode(chunk));}
        if(followLatest)toBottom();else updateLatest();
        if(offset>=words.length){el?.classList.remove('stream-active');if(el)addInlineCitation(m,index,el);index++;offset=0;}
        if(index>=m.blocks.length){finish(m,'complete');return;}
        scheduleSave();timer=setTimeout(tick,mode==='slow'?220:105);
      }tick();
    },mode==='slow'?2000:650);
  }
  function sendQuestion() {
    if(generation)return;const text=$('question').value.trim();if(!text)return;
    const t=current(),key=profileFor(text),u={id:id(),role:'user',text,files:[...t.files]};
    const previous=t.messages.filter(m=>m.role==='assistant').at(-1);
    const profile=key==='general'&&previous?previous.profile:key;
    const m={id:id(),role:'assistant',profile,questionId:u.id,status:'pending',blocks:[]};
    if(!t.messages.length)t.title=text.length>65?text.slice(0,62)+'…':text;
    t.messages.push(u,m);t.draft='';t.files=[];
    $('question').value='';resizeFallback();renderAttachments();
    $('workspace').classList.remove('empty');$('welcome').hidden=true;$('suggestions').hidden=true;
    $('thread-title').textContent=t.title;document.title=t.title+' — Meridian';
    $('messages').append(makeMessage(u));renderHistory();
    const mode=$('next-response').value;$('next-response').value='normal';startGeneration(m,mode);
  }
  function retryMessage(m){if(generation)stopGeneration();startGeneration(m,m.responseMode||'normal');if(!$('source-dialog').open)$('question').focus();}
  $('composer').onsubmit=e=>{e.preventDefault();sendQuestion();};
  $('question').oninput=()=>{rememberDraft();resizeFallback();updateControls();renderHistory();};
  $('question').onkeydown=e=>{if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();if(!generation)sendQuestion();}};
  $('stop').onclick=()=>{stopGeneration();$('question').focus();};
  function closeNav(){if($('nav-dialog').open)$('nav-dialog').close();}
  function switchThread(threadId){rememberDraft();stopGeneration();closeSource();state.activeId=threadId;renderThread();save();closeNav();}
  function newThread(){rememberDraft();stopGeneration();closeSource();const t=createThread();state.threads.push(t);state.activeId=t.id;renderThread(false);save();closeNav();$('question').focus();}
  $('new-thread').onclick=newThread;$('new-mobile').onclick=newThread;
  $('thread-search').oninput=renderHistory;
  document.querySelectorAll('[data-prompt]').forEach(b=>b.onclick=()=>{$('question').value=b.dataset.prompt;rememberDraft();sendQuestion();$('question').focus();});
  document.querySelectorAll('[data-example]').forEach(b=>b.onclick=()=>{
    const key=b.dataset.example;let t=state.threads.find(x=>x.example===key);
    if(!t){t=createThread();t.example=key;t.title=profiles[key].short;const u={id:id(),role:'user',text:profiles[key].prompt,files:[]};const m={id:id(),role:'assistant',profile:key,questionId:u.id,status:'complete',blocks:buildBlocks(key)};m.blocks.forEach(b=>b.visible=b.text);t.messages=[u,m];state.threads.push(t);}
    switchThread(t.id);
  });
  $('attach').onclick=()=>$('file-picker').click();
  $('file-picker').onchange=()=>{const names=[...$('file-picker').files].map(f=>f.name);current().files=[...current().files,...names];$('file-picker').value='';renderAttachments();renderHistory();save();announce(names.length+' filename'+(names.length===1?'':'s')+' added. File contents stay unread.');$('question').focus();};
  function themeLabel() {$('theme-label').textContent=root.dataset.theme==='dark'?'Light appearance':'Dark appearance';$('theme').setAttribute('aria-label','Switch to '+(root.dataset.theme==='dark'?'light':'dark')+' appearance');}
  $('theme').onclick=()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';try{localStorage.setItem('meridian-theme',root.dataset.theme);}catch{}themeLabel();};themeLabel();
  const demoOpen=()=>$('demo-dialog').showModal();$('demo-open').onclick=demoOpen;$('demo-open-top').onclick=demoOpen;
  $('demo-close').onclick=()=>$('demo-dialog').close();$('demo-done').onclick=()=>$('demo-dialog').close();
  function placeNav(){const content=$('nav-content');if(!mobile.matches){closeNav();$('desktop-nav').append(content);}else $('nav-dialog').append(content);}
  $('nav-open').onclick=()=>{$('nav-dialog').showModal();};$('nav-close').onclick=closeNav;mobile.addEventListener('change',placeNav);placeNav();
  function readingAnchor(){const bounds=reader.getBoundingClientRect();const candidates=[...reader.querySelectorAll('[data-anchor]')];const el=candidates.find(n=>n.getBoundingClientRect().bottom>bounds.top+8&&n.getBoundingClientRect().top<bounds.bottom);return el?{id:el.dataset.anchor,top:el.getBoundingClientRect().top}:null;}
  function restoreAnchor(a){if(!a)return;requestAnimationFrame(()=>{const n=reader.querySelector(`[data-anchor="${a.id}"]`);if(n)reader.scrollTop+=n.getBoundingClientRect().top-a.top;});}
  function sourceMessage(){return current().messages.find(m=>m.id===sourceContext?.messageId);}
  function syncSourceState(){
    const m=sourceMessage(),control=$('source-generation-action');if(!m)return;
    const running=m.status==='pending'||m.status==='streaming',retry=m.status==='stopped'||m.status==='error';
    $('source-live-label').textContent=running?'Answer is still arriving':retry?'Response stopped':'Answer is ready';
    control.hidden=!(running||retry);control.textContent=running?'Stop response':'Try again';control.onclick=running?stopGeneration:()=>retryMessage(m);
  }
  function markCitedParagraph(){document.querySelectorAll('.cited-paragraph').forEach(n=>n.classList.remove('cited-paragraph'));if(sourceContext)reader.querySelector(`[data-anchor="${sourceContext.messageId}-${sourceContext.blockIndex}"]`)?.classList.add('cited-paragraph');}
  function renderSource(){
    const p=profiles[sourceProfile],s=p.sources[sourceIndex];$('source-tabs').replaceChildren();
    p.sources.forEach((_,i)=>{const b=button(String(i+1),()=>{sourceIndex=i;if(sourceContext){sourceContext.blockIndex=3+i*2;sourceContext.text=sourceMessage()?.blocks[sourceContext.blockIndex]?.text||'';}renderSource();markCitedParagraph();$('source-tabs').children[i].focus();});b.setAttribute('aria-label','Illustrative source '+(i+1));b.setAttribute('aria-pressed',String(i===sourceIndex));$('source-tabs').append(b);});
    $('source-context').textContent=sourceContext?.text||'Read this source alongside the answer.';syncSourceState();
    const body=$('source-body');body.replaceChildren();
    body.append(make('span','source-type','SOURCE '+String(sourceIndex+1).padStart(2,'0')+' · SYNTHETIC EXCERPT'),make('h3','',s[1]),make('div','source-meta','Meridian reading collection · Demonstration material'),make('blockquote','',s[2]),make('p','',s[3]),make('h4','','Why it appears here'),make('p','','Read this perspective alongside the answer’s practical next step. It highlights the assumptions to check before turning an idea into a plan, and the smaller observations that can make that plan more useful.'),make('h4','','A question to take back'),make('p','','Which part of this explanation would you want to check before using it to make a decision?'),make('p','source-disclaimer','This is fictional demonstration text, not a published document or an independently verified source. No external page has been retrieved.'));
  }
  function openSource(key,index,trigger,message=null,blockIndex=null){const anchor=readingAnchor();lastSourceTrigger=trigger;sourceProfile=key;sourceIndex=index;if(message)sourceContext={messageId:message.id,blockIndex,text:message.blocks[blockIndex]?.text||''};renderSource();const d=$('source-dialog');if(d.open)d.close();if(modalSource.matches)d.showModal();else{d.show();$('app').classList.add('has-source');}markCitedParagraph();restoreAnchor(anchor);$('source-return').focus();}
  function returnFocus(){const citation=sourceContext&&reader.querySelector(`[data-citation="${sourceContext.messageId}-${sourceContext.blockIndex}"]`);const target=lastSourceTrigger?.isConnected?lastSourceTrigger:citation||$('question');target.focus({preventScroll:true});}
  function closeSource(){const d=$('source-dialog');if(!d.open)return;const anchor=readingAnchor();d.close();$('app').classList.remove('has-source');restoreAnchor(anchor);returnFocus();updateLatest();}
  $('source-close').onclick=closeSource;
  $('source-return').onclick=closeSource;
  $('source-dialog').addEventListener('close',()=>{$('app').classList.remove('has-source');if(!$('source-dialog').open)returnFocus();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&$('source-dialog').open&&!modalSource.matches)closeSource();});
  modalSource.addEventListener('change',()=>{if($('source-dialog').open)openSource(sourceProfile,sourceIndex,lastSourceTrigger);});
  window.addEventListener('pagehide',()=>{rememberDraft();save();});
  renderThread();save();
})();
