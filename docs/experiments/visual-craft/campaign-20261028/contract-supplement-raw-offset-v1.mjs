import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const runtime=process.env.UI_EVAL_RUNTIME||'/workspace/scratch/cb73faf0411c/ui-eval-runtime';
const moduleDir=path.dirname(new URL(import.meta.url).pathname);
const fixtureBase=fs.existsSync(path.join(moduleDir,'fixtures'))?path.join(moduleDir,'fixtures'):path.resolve(moduleDir,'../fixtures');
const {chromium,expect}=require(path.join(runtime,'node_modules/playwright'));
const root=path.resolve(process.argv[2]), task=process.argv[3], out=path.resolve(process.argv[4]);
fs.mkdirSync(out,{recursive:true});
const build=path.join(root,'dist');
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2','.woff':'font/woff','.json':'application/json','.gif':'image/gif','.avif':'image/avif','.ttf':'font/ttf','.otf':'font/otf','.mp4':'video/mp4','.webm':'video/webm'};
const server=http.createServer((req,res)=>{let p=path.join(build,decodeURIComponent(new URL(req.url,'http://local').pathname));if(!p.startsWith(build)){res.writeHead(403);res.end();return;}if(!fs.existsSync(p)||fs.statSync(p).isDirectory())p=path.join(build,'index.html');try{res.setHeader('Content-Type',mime[path.extname(p)]||'application/octet-stream');res.end(fs.readFileSync(p));}catch{res.writeHead(404);res.end('Missing build')}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch({headless:true,executablePath:process.env.UI_EVAL_CHROMIUM||path.join(runtime,'browsers/chromium-1161/chrome-linux/chrome'),args:['--no-sandbox']});
const result={task,root,startedAt:new Date().toISOString(),browser:browser.version(),viewportConditions:[[1440,900],[900,900],[390,844]],groups:[],captures:[],pageErrors:[],consoleErrors:[],requests:[],diagnostics:{},selectorAdaptations:[]};
let ctx,page,active;
const t=id=>page.getByTestId(id);
function ok(condition,message,details){active.assertions.push({pass:!!condition,message,details});if(!condition)throw new Error(message+(details?' '+JSON.stringify(details):''));}
async function equalText(locator,expected,message){await locator.waitFor({state:'visible'});const actual=(await locator.textContent()).trim();ok(actual.includes(expected),message,{expected,actual});}
async function restored(locator,message){await page.waitForFunction(e=>document.activeElement===e,await locator.elementHandle(),{timeout:1500});ok(true,message);}
async function visible(locator){await locator.waitFor({state:'visible',timeout:5000});return true;}
async function count(locator,n,message){await page.waitForTimeout(100);ok(await locator.count()===n,message,{expected:n,actual:await locator.count()});}
async function start(query='',contextOverrides={}){
 if(ctx)await ctx.close();ctx=await browser.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1,locale:'en-US',reducedMotion:'no-preference',...contextOverrides});page=await ctx.newPage();page.setDefaultTimeout(5000);
 page.on('pageerror',e=>result.pageErrors.push({group:active?.id,message:e.message}));page.on('console',m=>{if(m.type()==='error')result.consoleErrors.push({group:active?.id,text:m.text()})});page.on('requestfailed',r=>result.requests.push({url:r.url(),failure:r.failure()}));
 await page.goto(origin+'/'+query,{waitUntil:'networkidle',timeout:15000});await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(150);
}
async function capture(name,extra={}){const file=name+'.png';await page.screenshot({path:path.join(out,file)});result.captures.push({file,viewport:page.viewportSize(),time:new Date().toISOString(),...extra});}
async function noOverflow(){const d=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth}));ok(d.scroll<=d.width+1,'No page-level horizontal overflow',d);}
async function group(id,name,fn){active={id,name,assertions:[],status:'running'};result.groups.push(active);const begin=Date.now();try{await start();await fn();active.status='pass';}catch(e){active.status='fail';active.error=e.message;try{await capture('failure-'+id)}catch{}}active.elapsedMs=Date.now()-begin;fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(result,null,2));}
async function select(locator,value){const tag=await locator.evaluate(e=>e.tagName);if(tag==='SELECT'){try{await locator.selectOption({label:value});}catch{await locator.selectOption(value)}}else{await locator.click();await page.getByRole('option',{name:value,exact:true}).click();}}
async function history(id){if(!(await t(id).isVisible())&&await t('history-toggle').count())await t('history-toggle').click();await t(id).click();}
async function waitAssistant(n){await page.waitForFunction(n=>document.querySelectorAll('[data-testid="assistant-message"]').length===n,n,{timeout:7000});}
async function openT1Source(){const opener=t('source-s1').first();await opener.click();await visible(t('source-dialog'));return opener;}
async function themeVisual(){const before=await page.locator('body').evaluate(e=>[...e.querySelectorAll('*')].filter(x=>x.getBoundingClientRect().width>0).slice(0,100).map(x=>[getComputedStyle(x).color,getComputedStyle(x).backgroundColor]));await t('theme-toggle').click();await page.waitForTimeout(300);const after=await page.locator('body').evaluate(e=>[...e.querySelectorAll('*')].filter(x=>x.getBoundingClientRect().width>0).slice(0,100).map(x=>[getComputedStyle(x).color,getComputedStyle(x).backgroundColor]));let changed=0;for(let i=0;i<Math.min(before.length,after.length);i++)if(JSON.stringify(before[i])!==JSON.stringify(after[i]))changed++;ok(changed>=5,'Theme changes visible surface/text styles',{changedElements:changed});}
async function quietMotion(){await page.emulateMedia({reducedMotion:'reduce'});await page.waitForTimeout(500);const a=await page.evaluate(()=>document.getAnimations().map(x=>({duration:x.effect?.getTiming().duration,iterations:String(x.effect?.getTiming().iterations),state:x.playState})).filter(x=>x.state==='running'&&(x.iterations==='Infinity'||x.duration>500)));ok(a.length===0,'No long-running nonessential motion under reduced-motion idle condition',{animations:a});}
async function keyboardTo(id){for(let i=0;i<100;i++){const match=await page.evaluate(id=>document.activeElement?.getAttribute('data-testid')===id,id);if(match)return true;await page.keyboard.press('Tab')}return false;}


result.scope='Uniform supplement for published contract conditions omitted from the initial runner. Original observations and frozen applications are unchanged. Group IDs join the original ten acceptance groups; these are not additional independent task samples.';
const norm=s=>s.replace(/\s+/g,' ').trim();
async function contained(dialog,n=24){for(let i=0;i<n;i++){await page.keyboard.press('Tab');ok(await dialog.evaluate(e=>e.contains(document.activeElement)),'Keyboard focus stays within open dialog');}}
async function completeText(locator,value,label){const actual=norm(await locator.textContent());ok(actual.includes(norm(value)),label);}

if(task==='T1'){
 const {SOURCES}=await import('file://'+path.join(fixtureBase,'T1/src/domain.js'));
 await group('04','Every source complete and modal focus contained',async()=>{
  for(const source of SOURCES){await t('source-'+source.id).first().click();await visible(t('source-dialog'));await completeText(t('source-dialog'),source.title,'Exact source title '+source.id);await completeText(t('source-dialog'),source.publisher,'Exact publisher '+source.id);await completeText(t('source-dialog'),source.body,'Complete source text '+source.id);await contained(t('source-dialog'));await page.keyboard.press('Escape');await t('source-dialog').waitFor({state:'hidden'});await restored(t('source-'+source.id).first(),'Focus returns to matching source '+source.id);}
 });
 await group('09','Both themes in research and source surfaces at all widths',async()=>{
  for(const [w,h] of [[1440,900],[900,900],[390,844]]){
   await page.setViewportSize({width:w,height:h});await noOverflow();
   const colors=[];
   for(let pass=0;pass<2;pass++){
    await openT1Source();await noOverflow();colors.push(await t('source-dialog').evaluate(e=>[e,...e.querySelectorAll('*')].filter(x=>x.getBoundingClientRect().width>0).map(x=>[getComputedStyle(x).color,getComputedStyle(x).backgroundColor])));await capture('09-source-'+w+'-theme-'+pass);await t('source-close').click();await themeVisual();
   }
   ok(JSON.stringify(colors[0])!==JSON.stringify(colors[1]),'Source surface changes with selected theme at '+w);
   await history('thread-t-quiet');await equalText(t('messages'),'Support a steady reading rhythm','History remains usable at '+w);await history('thread-t-seed');
  }
 });
}

if(task==='T2'){
 const {INITIAL_PROJECTS}=await import('file://'+path.join(fixtureBase,'T2/src/domain.js'));
 const first=INITIAL_PROJECTS[0],note='Interview synthesis ready for partner review.';
 const open=async()=>{await t('project-open-PRJ-001').click();await visible(t('project-detail'));};
 const close=async()=>{await t('detail-close').click();await t('project-detail').waitFor({state:'hidden'});};
 const clear=async()=>{if(await t('clear-filters').isEnabled())await t('clear-filters').click();else{ok((await t('search-input').inputValue())==='','Already clear search');const v=await t('status-filter').evaluate(e=>e.value||e.textContent);ok(/^all\b/i.test(v.trim()),'Already All status');}};
 const results=async(count)=>{const text=await t('results-count').textContent();const numbers=text.match(/\d+/g)?.map(Number);ok(numbers?.length>=2&&numbers[0]===count&&numbers[1]===12,'Correct result count',{text,expected:[count,12]});};
 const otherStatuses=async()=>{for(const p of INITIAL_PROJECTS.slice(1))await equalText(t('project-status-'+p.id),p.status,'Unrelated status preserved '+p.id);};
 await group('02','Exact complete result count',async()=>{await t('nav-projects').click();await results(12);});
 await group('03','Search result counts',async()=>{await t('nav-projects').click();await t('search-input').fill(first.title);await results(1);await t('search-input').fill('');await results(12);});
 await group('04','Filtered result counts and statuses',async()=>{await t('nav-projects').click();await select(t('status-filter'),'Planned');await results(4);for(const p of INITIAL_PROJECTS.filter(x=>x.status==='Planned'))await equalText(t('project-status-'+p.id),'Planned','Visible matching status '+p.id);await clear();await results(12);});
 await group('06','Full project metadata and focus containment',async()=>{
  await t('nav-projects').click();await open();await completeText(t('detail-summary'),first.summary,'Complete seeded description');
  for(const method of first.methods)await completeText(t('project-detail'),method,'Project method '+method);
  for(const [id,expected] of [['detail-start',first.startDate],['detail-due',first.dueDate]]){const actual=await t(id).evaluate(e=>e.getAttribute('datetime')||e.getAttribute('data-date'));ok(actual===expected,'Exact detail date '+id,{actual,expected});}
  await completeText(t('detail-notes'),first.notes[0].body,'Complete original note');await contained(t('project-detail'));await page.keyboard.press('Escape');await t('project-detail').waitFor({state:'hidden'});await restored(t('project-open-PRJ-001'),'Focus return after full keyboard traversal');
 });
 await group('07','Status change preserves other project states',async()=>{await t('nav-projects').click();await open();await select(t('detail-status'),'Review');const value=await t('detail-status').evaluate(e=>e.value||e.textContent);ok(value.includes('Review'),'Detail status updated');await close();await otherStatuses();await t('nav-schedule').click();await otherStatuses();});
 await group('08','Original note remains after status and append chain',async()=>{await t('nav-projects').click();await open();await select(t('detail-status'),'Review');await t('note-input').fill(note);await t('note-save').click();await count(t('project-note'),2,'Exactly two notes');await completeText(t('detail-notes'),first.notes[0].body,'Original note unchanged after append');await close();await open();await completeText(t('detail-notes'),first.notes[0].body,'Original note unchanged after reopen');await completeText(t('detail-notes'),note,'Acceptance note retained after reopen');});
 await group('09','Complete reload state preservation',async()=>{
  await t('nav-projects').click();await open();await select(t('detail-status'),'Review');await t('note-input').fill(note);await t('note-save').click();await page.reload({waitUntil:'networkidle'});await t('nav-projects').click();await otherStatuses();await open();await completeText(t('detail-notes'),first.notes[0].body,'Original note persists');await completeText(t('detail-notes'),first.owner,'Original author persists');await completeText(t('detail-notes'),note,'New note persists');await completeText(t('detail-notes'),'You','New note author persists');
 });
 await group('10','Three complete views across widths and both themes',async()=>{
  for(const [w,h] of [[1440,900],[900,900],[390,900]]){
   await page.setViewportSize({width:w,height:h});
   for(const theme of ['light','dark']){
    if(await t('app-shell').getAttribute('data-theme')!==theme)await themeVisual();
    ok(await page.locator('html').getAttribute('data-theme')===theme,'Document root theme '+theme);
    for(const view of ['overview','projects','schedule']){
     await t('nav-'+view).click();await visible(t(view+'-view'));await clear();await t('search-input').fill(first.title);await results(1);await noOverflow();await open();await visible(t('note-input'));await noOverflow();await capture('10-'+w+'-'+theme+'-'+view+'-detail');await close();await clear();await select(t('status-filter'),'Planned');await results(4);await clear();await results(12);await noOverflow();
    }
    await t('nav-overview').click();await capture('10-'+w+'-'+theme+'-overview');await page.reload({waitUntil:'networkidle'});ok(await t('app-shell').getAttribute('data-theme')===theme,'Selected theme persists after reload '+theme+' '+w);ok(await page.locator('html').getAttribute('data-theme')===theme,'Root theme persists '+theme+' '+w);
   }
  }
  await page.setViewportSize({width:390,height:844});await page.emulateMedia({reducedMotion:'reduce'});
  for(const view of ['overview','projects','schedule']){await t('nav-'+view).click();await open();await quietMotion();await close();await noOverflow();}
 });
}

if(task==='T3'){
 const vm=await import('node:vm');
 const source=fs.readFileSync(path.join(fixtureBase,'T3/src/domain.js'),'utf8').replace(/\bexport /g,'');
 const records=vm.runInNewContext(source+'\nRECORDS');
 const open=async(id)=>{await t('citation-'+id).click();await t('source-metadata').waitFor({state:'visible',timeout:7000});};
 const close=async()=>{await t('source-close').click();await t('source-sheet').waitFor({state:'hidden'});};
 await group('01','All three source identities and full texts',async()=>{
  for(const record of Object.values(records)){
   await open(record.id);await completeText(t('source-title'),record.title,'Correct title '+record.id);for(const author of record.authors)await completeText(t('source-metadata'),author,'Correct author '+record.id+' '+author);await completeText(t('source-metadata'),record.publication,'Correct publication '+record.id);await completeText(t('source-sheet'),record.summary,'Complete summary '+record.id);
   for(const section of record.sections){await completeText(t('source-content'),section.heading,'Section retained '+record.id+' '+section.heading);for(const paragraph of section.paragraphs)await completeText(t('source-content'),paragraph,'Complete paragraph retained '+record.id);}
   await t('source-content').evaluate(e=>e.scrollTop=e.scrollHeight);await capture('01-complete-'+record.id);await close();
  }
 });
 await group('04','Reading position remains at its valid offset across modes',async()=>{
  await open('heat-mapping');await t('source-content').evaluate(e=>e.scrollTop=180);const before=await t('source-content').evaluate(e=>e.scrollTop);await t('source-expand').click();await page.waitForTimeout(600);const after=await t('source-content').evaluate(e=>({top:e.scrollTop,max:e.scrollHeight-e.clientHeight}));ok(Math.abs(after.top-Math.min(before,after.max))<=2,'Reading offset preserved, allowing only valid scroll-range clamping',{before,after});
 });
 await group('06','Reversed drag returns to the existing reading sheet',async()=>{
  await open('heat-mapping');const initial=await t('source-sheet').boundingBox();const box=await t('source-drag-handle').boundingBox(),x=box.x+box.width/2,y=box.y+box.height/2;await page.mouse.move(x,y);await page.mouse.down();for(const dy of [40,100,190,120,60,12]){await page.mouse.move(x,y+dy,{steps:4});await page.waitForTimeout(30);}await page.mouse.up();await page.waitForTimeout(700);await visible(t('source-sheet'));const final=await t('source-sheet').boundingBox();ok(Math.abs(final.y-initial.y)<8,'Reversed drag settles at original position',{initialY:initial.y,finalY:final.y});await t('source-note').fill('Still operable after a reversed drag');await close();
 });
 await group('10','Low-impact navigation count remains intact',async()=>{await equalText(t('nav-saved'),'Library','Requested label retained');await equalText(t('nav-saved'),'24','Original count retained');await t('nav-saved').click();await equalText(t('nav-saved'),'24','Count remains after activation');});
}
result.finishedAt=new Date().toISOString();result.functionalPasses=result.groups.filter(x=>x.status==='pass').length;result.functionalTotal=result.groups.length;
result.rawPageErrorCount=result.pageErrors.length;result.uniquePageErrors=[...new Set(result.pageErrors.map(x=>x.message))];
result.diagnostics.buildFiles=[];function walk(p){for(const name of fs.readdirSync(p)){const f=path.join(p,name);if(fs.statSync(f).isDirectory())walk(f);else result.diagnostics.buildFiles.push({file:path.relative(build,f),bytes:fs.statSync(f).size,sha256:crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')});}}if(fs.existsSync(build))walk(build);
fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(result,null,2));await browser.close();server.close();console.log(JSON.stringify({task,passed:result.functionalPasses,total:result.functionalTotal,captures:result.captures.length,errors:result.uniquePageErrors,failures:result.groups.filter(x=>x.status==='fail').map(x=>({id:x.id,error:x.error}))},null,2));
