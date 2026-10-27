from pathlib import Path, PurePosixPath
import hashlib,json,re,shutil,subprocess,urllib.request
R=Path('/tmp/craft-tasks');R.mkdir(exist_ok=True)
P=Path('/tmp/craft-build');P.mkdir(exist_ok=True)
seen=set();deps={'react','react-dom','esbuild','tailwindcss','@tailwindcss/cli','tw-animate-css','clsx','tailwind-merge'};records=[]
def read(url):
 if not url.startswith(('https://r.assistant-ui.com/','https://ui.shadcn.com/','https://raw.githubusercontent.com/')):raise ValueError('Unsupported source '+url)
 return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'UI-Spec-Studio research'}),timeout=60).read()
def registry(url):
 if url in seen:return
 seen.add(url);raw=read(url);data=json.loads(raw)
 records.append({'url':url,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'kind':'registry item fetched for this run'})
 for dep in data.get('dependencies',[]):
  if not re.fullmatch(r'(@[a-zA-Z0-9_.-]+/)?[a-zA-Z0-9_.-]+(@[0-9a-zA-Z.^~<>=|* -]+)?',dep):raise ValueError(dep)
  deps.add(dep)
 for f in data.get('files',[]):
  target=f.get('target')
  if not target:
   path='/'+f['path']
   if '/assistant-ui/' in path:target='components/assistant-ui/'+path.split('/assistant-ui/',1)[1]
   elif '/ui/' in path:target='components/ui/'+path.split('/ui/',1)[1]
   elif path.endswith('utils.ts'):target='lib/utils.ts'
   else:raise ValueError('Unmapped registry path '+path)
  target=target.replace('~/','')
  p=PurePosixPath(target)
  if p.is_absolute() or '..' in p.parts or p.suffix not in {'.ts','.tsx','.css'}:raise ValueError('Unsafe file '+target)
  file=P/target;file.parent.mkdir(parents=True,exist_ok=True);file.write_text(f['content'],encoding='utf-8')
  records.append({'source':url,'file':target,'sha256':hashlib.sha256(f['content'].encode()).hexdigest(),'kind':'unaltered registry source'})
 for dep in data.get('registryDependencies',[]):
  if dep.startswith('https://'):next_url=dep
  elif dep.startswith('@assistant-ui/'):next_url='https://r.assistant-ui.com/'+dep.split('/',1)[1]+'.json'
  elif re.fullmatch('[a-z0-9-]+',dep):next_url='https://ui.shadcn.com/r/styles/new-york/'+dep+'.json'
  else:raise ValueError('Unsupported registry dependency '+dep)
  registry(next_url)
try:
 for url in ['https://r.assistant-ui.com/thread.json','https://r.assistant-ui.com/thread-list.json','https://ui.shadcn.com/r/styles/new-york/drawer.json']:registry(url)
 (P/'lib').mkdir(exist_ok=True)
 (P/'lib/utils.ts').write_text('import {clsx} from "clsx";import {twMerge} from "tailwind-merge";export function cn(...inputs:any[]){return twMerge(clsx(inputs));}',encoding='utf-8')
 for name,target in [('app.tsx','App.tsx'),('style.css','style.css')]:shutil.copyfile(Path('.research')/name,P/target)
 (P/'tsconfig.json').write_text(json.dumps({'compilerOptions':{'jsx':'react-jsx','baseUrl':'.','paths':{'@/*':['./*']}}}),encoding='utf-8')
 subprocess.run(['npm','init','-y'],cwd=P,check=True)
 subprocess.run(['npm','install','--ignore-scripts','--save-exact',*sorted(deps)],cwd=P,check=True)
 (R/'dist').mkdir(exist_ok=True)
 subprocess.run(['node','-e',"require('esbuild').buildSync({entryPoints:['App.tsx'],bundle:true,outfile:'/tmp/craft-tasks/dist/app.js',jsx:'automatic',minify:false,define:{'process.env.NODE_ENV':'\"production\"'}})"],cwd=P,check=True)
 subprocess.run(['npx','--no-install','@tailwindcss/cli','-i','style.css','-o',str(R/'dist/style.css')],cwd=P,check=True)
 (R/'dist/index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Source-adoption task study</title><link rel="stylesheet" href="style.css"><body><div id="root"></div><script src="app.js"></script></body></html>',encoding='utf-8')
 shutil.copyfile(P/'package-lock.json',R/'build-lock.json')
 for source,dest in [('https://raw.githubusercontent.com/assistant-ui/assistant-ui/main/LICENSE','assistant-ui-LICENSE'),('https://raw.githubusercontent.com/shadcn-ui/ui/main/LICENSE.md','shadcn-LICENSE.md'),('https://raw.githubusercontent.com/emilkowalski/vaul/main/LICENSE.md','vaul-LICENSE.md')]:
  try:(R/dest).write_bytes(read(source))
  except Exception as e:records.append({'url':source,'license_fetch_error':str(e)})
 shutil.copytree(P/'components',R/'source/components',dirs_exist_ok=True)
 shutil.copyfile(P/'App.tsx',R/'source/App.tsx');shutil.copyfile(P/'style.css',R/'source/style.css')
except Exception as e:
 (R/'build-error.txt').write_text(repr(e),encoding='utf-8');raise
finally:
 (R/'source-identity.json').write_text(json.dumps({'scope':'Current maintainer Agent authored trial adapters using actual registry blocks; not an independent or blinded model experiment. Backend responses are identified fixtures, not a live model.','records':records},indent=2)+'\n',encoding='utf-8')
