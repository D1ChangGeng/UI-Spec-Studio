import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import {createRequire} from 'node:module';
const runtime=process.env.UI_EVAL_RUNTIME||'/workspace/scratch/cb73faf0411c/ui-eval-runtime';
process.env.PLAYWRIGHT_BROWSERS_PATH=path.join(runtime,'browsers');
const require=createRequire(import.meta.url);
const {chromium}=require(path.join(runtime,'node_modules/playwright'));
const root=path.resolve(process.argv[2]),task=process.argv[3],out=path.resolve(process.argv[4]),dist=path.join(root,'dist');fs.mkdirSync(out,{recursive:true});
const server=http.createServer((req,res)=>{let p=path.join(dist,new URL(req.url,'http://local').pathname);if(!p.startsWith(dist)){res.writeHead(403);res.end();return;}if(!fs.existsSync(p)||fs.statSync(p).isDirectory())p=path.join(dist,'index.html');res.setHeader('Content-Type',({'.js':'text/javascript','.css':'text/css','.html':'text/html','.svg':'image/svg+xml','.woff2':'font/woff2'})[path.extname(p)]||'application/octet-stream');res.end(fs.readFileSync(p));});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({headless:true,executablePath:process.env.UI_EVAL_CHROMIUM||path.join(runtime,'browsers/chromium-1161/chrome-linux/chrome'),args:['--no-sandbox']});
const ctx=await browser.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1,recordVideo:{dir:path.join(out,'video'),size:{width:1440,height:900}}});
const page=await ctx.newPage();page.setDefaultTimeout(6000);const frames=[],events=[],errors=[];page.on('pageerror',e=>errors.push(e.message));const origin='http://127.0.0.1:'+server.address().port;
const t=id=>page.getByTestId(id);let counter=0,epoch=performance.now();
async function snap(label){const start=performance.now();const file=String(++counter).padStart(3,'0')+'-'+label+'.png';await page.screenshot({path:path.join(out,file)});const geometry=await page.evaluate(()=>[...document.querySelectorAll('[role=dialog],[data-testid=source-sheet],[data-testid=pending]')].map(e=>{const r=e.getBoundingClientRect();return {testId:e.getAttribute('data-testid'),x:r.x,y:r.y,width:r.width,height:r.height,opacity:getComputedStyle(e).opacity,transform:getComputedStyle(e).transform}}));frames.push({file,label,sampleStartedMs:start-epoch,sampleEndedMs:performance.now()-epoch,geometry});}
async function sequence(label,trigger,delays=[0,80,200,450,900]){events.push({event:label,startedMs:performance.now()-epoch});const begin=performance.now();await trigger();for(const delay of delays){const remaining=delay-(performance.now()-begin);if(remaining>0)await page.waitForTimeout(remaining);await snap(label+'-'+delay);}}
try{
 await page.goto(origin,{waitUntil:'networkidle'});await page.evaluate(()=>document.fonts.ready);await page.waitForTimeout(300);epoch=performance.now();await snap('initial');
 if(task==='T1'){
  await sequence('source-open',()=>t('source-s1').first().click());
  await sequence('source-close',()=>t('source-close').click());
  await t('new-thread').click();await t('composer').fill('Trace the waiting and answer experience');await sequence('request',()=>t('send').click(),[0,150,400,800,1400]);
 }else if(task==='T2'){
  await t('nav-projects').click();await sequence('detail-open',()=>t('project-open-PRJ-001').click());
  await sequence('detail-close',()=>t('detail-close').click());
  await sequence('view-schedule',()=>t('nav-schedule').click(),[0,100,400,800]);
 }else if(task==='T3'){
  await sequence('sheet-open',()=>t('citation-heat-mapping').click(),[0,100,300,650,1100]);
  await sequence('expand',()=>t('source-expand').click(),[0,80,200,450,800]);
  await sequence('reverse',async()=>{await t('source-expand').click();await page.waitForTimeout(70);await t('source-expand').click()},[0,100,300,650,1000]);
  const box=await t('source-drag-handle').boundingBox();events.push({event:'drag',startedMs:performance.now()-epoch});await page.mouse.move(box.x+box.width/2,box.y+box.height/2);await page.mouse.down();for(const y of [20,60,120,220,330]){await page.mouse.move(box.x+box.width/2,box.y+box.height/2+y,{steps:4});await snap('drag-'+y);}await page.mouse.up();await page.waitForTimeout(900);await snap('drag-settled');
 }
}catch(e){errors.push(e.message);try{await snap('interrupted')}catch{}}
const video=page.video();await ctx.close();const videoPath=await video.path();await browser.close();server.close();
fs.writeFileSync(path.join(out,'timeline.json'),JSON.stringify({task,scope:'Natural-clock scripted interaction video plus timestamped samples; sample cadence is affected by capture overhead. No FPS conclusion.',startedAt:new Date().toISOString(),viewport:{width:1440,height:900},events,frames,video:path.relative(out,videoPath),errors},null,2));
console.log(JSON.stringify({task,frames:frames.length,video:videoPath,errors}));
