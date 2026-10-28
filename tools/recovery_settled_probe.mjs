import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(path.join(process.env.UI_EVAL_RUNTIME,'node_modules/playwright'));
const app=path.resolve(process.argv[2]),out=path.resolve(process.argv[3]);fs.mkdirSync(out,{recursive:true});
const root=path.join(app,'dist');
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.woff2':'font/woff2','.woff':'font/woff','.ttf':'font/ttf','.svg':'image/svg+xml','.png':'image/png'};
const server=http.createServer((req,res)=>{try{const url=new URL(req.url,'http://local');let file=path.resolve(root,'.'+decodeURIComponent(url.pathname));if(file!==root&&!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}if(!fs.existsSync(file)||fs.statSync(file).isDirectory())file=path.join(root,'index.html');res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.writeHead(404).end();}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch({headless:true,executablePath:process.env.UI_EVAL_CHROMIUM,args:['--no-sandbox']});const rows=[];
try{
 for(const theme of ['light','dark']){
  const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,locale:'en-US',reducedMotion:'no-preference'});
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));page.setDefaultTimeout(7000);
  await page.goto(origin,{waitUntil:'networkidle'});await page.evaluate(()=>document.fonts.ready);
  if(await page.getByTestId('app-shell').getAttribute('data-theme')!==theme)await page.getByTestId('theme-toggle').click();
  await page.getByTestId('nav-projects').click();await page.getByTestId('project-open-PRJ-001').click();
  const modal=page.getByTestId('project-detail');await modal.waitFor({state:'visible'});const samples=[];const start=performance.now();
  let stable=false;
  for(let i=0;i<30;i++){
   const s=await modal.evaluate(e=>{const r=e.getBoundingClientRect(),c=getComputedStyle(e);return{x:r.x,y:r.y,w:r.width,h:r.height,transform:c.transform,opacity:c.opacity,activeAnimations:e.getAnimations({subtree:false}).filter(a=>a.playState==='running').length}});
   s.elapsedMs=performance.now()-start;samples.push(s);
   if(samples.length>=4&&s.elapsedMs>=500&&s.activeAnimations===0&&s.opacity==='1'&&samples.slice(-4).every(a=>['x','y','w','h'].every(k=>Math.abs(a[k]-s[k])<.1))){stable=true;break;}
   await page.waitForTimeout(100);
  }
  const geometry=await modal.boundingBox(),filename=theme+'-390-settled.png';await page.screenshot({path:path.join(out,filename)});
  rows.push({theme,viewport:{width:390,height:844},browser:browser.version(),stable,samples,geometry,contained:geometry.x>=-1&&geometry.x+geometry.width<=391,errors,file:filename,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(out,filename))).digest('hex')});
  await context.close();
 }
 fs.writeFileSync(path.join(out,'settled-observations.json'),JSON.stringify({kind:'post-outcome-diagnostic-not-preregistered-score',scope:'Supplementary 390px stable-state inspection. No source repair, no primary score change, no new Agent run or blind aesthetic judgment.',browser:browser.version(),rows},null,2)+'\n');
}finally{await browser.close();server.close();}
