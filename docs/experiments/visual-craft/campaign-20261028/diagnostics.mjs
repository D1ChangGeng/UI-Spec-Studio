import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const runtime=process.env.UI_EVAL_RUNTIME||'/workspace/scratch/cb73faf0411c/ui-eval-runtime';
const {chromium}=require(path.join(runtime,'node_modules/playwright'));
const root=path.resolve(process.argv[2]),task=process.argv[3],out=path.resolve(process.argv[4]),dist=path.join(root,'dist');
fs.mkdirSync(out,{recursive:true});
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2','.woff':'font/woff','.ttf':'font/ttf','.otf':'font/otf','.json':'application/json'};
const server=http.createServer((req,res)=>{let file=path.join(dist,decodeURIComponent(new URL(req.url,'http://local').pathname));if(!file.startsWith(dist)){res.writeHead(403);res.end();return}if(!fs.existsSync(file)||fs.statSync(file).isDirectory())file=path.join(dist,'index.html');try{res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file))}catch{res.writeHead(404);res.end()}});
await new Promise(r=>server.listen(0,'127.0.0.1',r));
const origin='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch({headless:true,executablePath:process.env.UI_EVAL_CHROMIUM||path.join(runtime,'browsers/chromium-1161/chrome-linux/chrome'),args:['--no-sandbox']});
const result={task,createdAt:new Date().toISOString(),scope:'Asset and external-network diagnostic; no speed, FPS or production device comparison. Locally served uncompressed HTTP.',conditions:[]};
try{
 for(const blockExternal of [false,true]){
  const ctx=await browser.newContext({viewport:{width:1440,height:900},deviceScaleFactor:1});
  const page=await ctx.newPage();page.setDefaultTimeout(5000);
  const row={blockExternal,requests:[],blocked:[],pageErrors:[],consoleErrors:[]};
  page.on('request',r=>row.requests.push({url:r.url().replace(origin,'LOCAL'),type:r.resourceType()}));
  page.on('pageerror',e=>row.pageErrors.push(e.message));page.on('console',m=>{if(m.type()==='error')row.consoleErrors.push(m.text())});
  if(blockExternal)await ctx.route('**/*',route=>{const url=route.request().url();if(url.startsWith(origin)||url.startsWith('data:')||url.startsWith('blob:'))return route.continue();row.blocked.push(url);return route.abort()});
  try{
   await page.goto(origin,{waitUntil:'networkidle',timeout:15000});await page.evaluate(()=>document.fonts.ready);
   const test=id=>page.getByTestId(id);
   if(task==='T1')await test('source-s1').first().click();
   if(task==='T2'){await test('nav-projects').click();await test('project-open-PRJ-001').click()}
   if(task==='T3'){await test('citation-heat-mapping').click();await test('source-metadata').waitFor({state:'visible'})}
   await page.waitForTimeout(500);
   row.render=await page.evaluate(()=>({textLength:document.body.innerText.length,dialogCount:document.querySelectorAll('[role=dialog]').length,fonts:[...document.fonts].map(f=>({family:f.family,status:f.status,style:f.style,weight:f.weight})),resources:performance.getEntriesByType('resource').map(r=>({url:r.name,type:r.initiatorType,transferBytes:r.transferSize,encodedBodyBytes:r.encodedBodySize,decodedBodyBytes:r.decodedBodySize}))}));
   row.render.resources.forEach(r=>{r.url=r.url.replace(origin,'LOCAL')});
   const locals=[...new Set(row.requests.filter(r=>r.url.startsWith('LOCAL')).map(r=>new URL(r.url.replace('LOCAL',origin)).pathname))];
   row.requestedLocalFiles=locals.map(name=>{const file=path.join(dist,decodeURIComponent(name));return {path:name,bytes:fs.existsSync(file)&&fs.statSync(file).isFile()?fs.statSync(file).size:null}});
   row.requestedLocalBytes=row.requestedLocalFiles.reduce((a,r)=>a+(r.bytes||0),0);
   row.localFileByteScope='Requested static resources in the initial and one primary detail state; root HTML served at / is omitted from this sum.';
   await page.screenshot({path:path.join(out,blockExternal?'external-network-blocked.png':'ordinary-network.png')});
  }catch(e){row.error=e.message}
  result.conditions.push(row);await ctx.close();
 }
}finally{await browser.close();server.close()}
fs.writeFileSync(path.join(out,'diagnostics.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify({task,conditions:result.conditions.map(r=>({blockExternal:r.blockExternal,blocked:r.blocked.length,requestedLocalBytes:r.requestedLocalBytes,errors:r.pageErrors,error:r.error}))}));
