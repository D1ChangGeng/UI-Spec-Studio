import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const runtime=process.env.UI_EVAL_RUNTIME;
const {chromium}=require(path.join(runtime,'node_modules/playwright'));
const root=path.resolve(process.argv[2]),task=process.argv[3],out=path.resolve(process.argv[4]),dist=path.join(root,'dist');
fs.mkdirSync(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2','.woff':'font/woff','.ttf':'font/ttf','.json':'application/json'};
const server=http.createServer((req,res)=>{try{const name=decodeURIComponent(new URL(req.url,'http://local').pathname);let f=path.resolve(dist,'.'+name);if(!f.startsWith(dist+path.sep)&&f!==dist){res.writeHead(403).end();return;}if(!fs.existsSync(f)||fs.statSync(f).isDirectory())f=path.join(dist,'index.html');res.setHeader('Content-Type',mime[path.extname(f)]||'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.writeHead(404).end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const browser=await chromium.launch({headless:true,executablePath:process.env.UI_EVAL_CHROMIUM||path.join(runtime,'browsers/chromium-1161/chrome-linux/chrome'),args:['--no-sandbox']});
const result={task,started_at:new Date().toISOString(),browser:browser.version(),scope:'Uniform stable-geometry final-state screenshots; no CSS or application source altered.',captures:[],errors:[]};
let page,ctx;
async function settle(locator){await locator.waitFor({state:'visible'});let last,stable=0,observed=[];const start=Date.now();while(Date.now()-start<6000){const q=await locator.evaluate(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,opacity:Number(getComputedStyle(e).opacity)};});observed.push({ms:Date.now()-start,...q});if(last&&['x','y','w','h','opacity'].every(k=>Math.abs(last[k]-q[k])<.15)&&q.opacity>.98)stable++;else stable=0;last=q;if(stable>=6)return {settled:true,samples:observed};await page.waitForTimeout(80);}return {settled:false,samples:observed};}
async function snap(label,target){await page.evaluate(()=>document.fonts.ready);const stable=await settle(target||page.locator('body'));const file=label+'.png';await page.screenshot({path:path.join(out,file)});result.captures.push({file,label,viewport:page.viewportSize(),captured_at:new Date().toISOString(),geometry:stable,overflow:await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}))});}
const t=id=>page.getByTestId(id);

async function toggleThemeViaVisibleRoute(){
 let openedHistory=false;
 if(!(await t('theme-toggle').isVisible()) && await t('history-toggle').isVisible()){
  await t('history-toggle').click();openedHistory=true;
  result.selectorAdaptations??=[];
  result.selectorAdaptations.push({id:'T1-mobile-theme-route-20261028',group_id:typeof active==='undefined'?null:active?.id,viewport:page.viewportSize(),route:['history-toggle','theme-toggle','Escape'],scope:'Open the existing public navigation before using its unchanged theme hook; no application or assertion change.'});
 }
 await t('theme-toggle').click();
 if(openedHistory){await page.keyboard.press('Escape');await t('theme-toggle').waitFor({state:'hidden'});}
}

try{
for(const [width,height] of [[1440,900],[900,900],[390,844]]){
 ctx=await browser.newContext({viewport:{width,height},deviceScaleFactor:1,locale:'en-US',colorScheme:'light'});page=await ctx.newPage();page.setDefaultTimeout(7000);page.on('pageerror',e=>result.errors.push({width,error:e.message}));
 await page.goto('http://127.0.0.1:'+server.address().port,{waitUntil:'networkidle'});
 if(task==='T1'){
  for(let appearance=0;appearance<2;appearance++){
   if(appearance)await toggleThemeViaVisibleRoute();const prefix=width+'-'+(appearance?'alternate':'initial');
   await snap(prefix+'-conversation');await t('source-s1').first().click();await snap(prefix+'-source',t('source-dialog'));await t('source-close').click();await t('source-dialog').waitFor({state:'hidden'});
  }
 }else if(task==='T2'){
  for(let appearance=0;appearance<2;appearance++){
   if(appearance)await toggleThemeViaVisibleRoute();const prefix=width+'-'+(appearance?'alternate':'initial');
   for(const view of ['overview','projects','schedule']){await t('nav-'+view).click();await snap(prefix+'-'+view,t(view+'-view'));}
   await t('nav-projects').click();await t('project-open-PRJ-001').click();await snap(prefix+'-detail',t('project-detail'));await t('detail-close').click();await t('project-detail').waitFor({state:'hidden'});
  }
 }else{
  await snap(width+'-notebook');await t('citation-heat-mapping').click();await t('source-metadata').waitFor({state:'visible'});await snap(width+'-compact',t('source-sheet'));await t('source-expand').click();await snap(width+'-expanded',t('source-sheet'));await t('sheet-source-shade-access').click();await page.waitForTimeout(700);await snap(width+'-second-source',t('source-sheet'));
 }
 await ctx.close();ctx=null;
}
}catch(e){result.errors.push({error:e.message,viewport:page?.viewportSize()});try{await snap('interrupted')}catch{}}
finally{if(ctx)await ctx.close();await browser.close();server.close();}
result.finished_at=new Date().toISOString();fs.writeFileSync(path.join(out,'settled.json'),JSON.stringify(result,null,2));console.log(JSON.stringify({task,captures:result.captures.length,errors:result.errors}));
