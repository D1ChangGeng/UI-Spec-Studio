// Execute within functions.exec with MANIFEST (parsed prepare_checkpoint output)
// and LABEL (a unique checkpoint key). This is delivery tooling, not agent evidence.
// All dependency mutations are sequential; independent local reads are bounded.
if (!/^[a-z0-9-]+$/.test(LABEL)) throw Error('Invalid checkpoint label');
const namespace='github_sync_'+LABEL;
const files=MANIFEST.files;
if(files.some(f=>f.path.includes('/provider-originals-audit-')))throw Error('Private recovery original must remain outside public delivery');
let known={...(load('takeover_uploaded_objects')||{}),...(load('extra_uploaded_blobs')||{})};
if(Array.isArray(known))known=Object.fromEntries(known.map(x=>[x,true]));
const receipts=[];
function checkResponse(result){if(result.isError)throw Error('GitHub connector error; original response retained');return result.structuredContent;}
async function readParts(sha,bytes){
  if(!/^[0-9a-f]{40}$/.test(sha))throw Error('Invalid object identity');
  const parts=[],unit=720000;
  for(let offset=0;offset<bytes;offset+=unit*8){
    const responses=await Promise.allSettled(Array.from({length:Math.min(8,Math.ceil((bytes-offset)/unit))},(_,i)=>{
      const start=offset+i*unit,end=Math.min(bytes,start+unit);
      return tools.exec_command({cmd:"python3 - <<'PY'\nimport subprocess,base64\nb=subprocess.check_output(['git','-C','/workspace/scratch/e1cfe6e447ee/UI-Spec-Studio','cat-file','blob','"+sha+"'])\nprint(base64.b64encode(b["+start+":"+end+"]).decode())\nPY",shell:"/bin/bash",workdir:"/workspace/scratch/e1cfe6e447ee/UI-Spec-Studio",max_output_tokens:5000000}).then(result=>({result,start,end}));
    }));
    for(const row of responses){
      if(row.status!=='fulfilled')throw row.reason;
      const {result,start,end}=row.value;const data=result.output.trim();
      if(result.exit_code!==0||data.length!==4*Math.ceil((end-start)/3))throw Error('Truncated object read');
      parts.push(data);
    }
  }
  const data=parts.join('');if(data.length!==4*Math.ceil(bytes/3))throw Error('Incorrect base64 size');return data;
}
const unique=[...new Map(files.filter(f=>!f.delete&&!known[f.sha]&&(!f.text||f.bytes>180000)).map(f=>[f.sha,f])).values()];
for(let i=0;i<unique.length;i++){
  const file=unique[i],content=await readParts(file.sha,file.bytes);
  const response=await tools.mcp__codex_apps__github_create_blob({repository_full_name:MANIFEST.repository_full_name,encoding:'base64',content});
  receipts.push({tool:'github_create_blob',request_scope:{sha:file.sha,bytes:file.bytes,encoding:'base64'},response});store(namespace+'_receipts',receipts);
  if(checkResponse(response)?.sha!==file.sha)throw Error('Uploaded blob differs from local Git object');
  known[file.sha]=true;store('extra_uploaded_blobs',known);
  if((i+1)%25===0)notify({checkpoint:LABEL,uploaded:i+1,total:unique.length});
}
const textFiles=[...new Map(files.filter(f=>!f.delete&&!known[f.sha]&&f.text&&f.bytes<=180000).map(f=>[f.sha,f])).values()];
const readGroups=[];let group=[],bytes=0;
for(const file of textFiles){if(bytes+file.bytes>150000&&group.length){readGroups.push(group);group=[];bytes=0;}group.push(file);bytes+=file.bytes;}
if(group.length)readGroups.push(group);
const textBodies={};
for(let offset=0;offset<readGroups.length;offset+=4){
  const responses=await Promise.allSettled(readGroups.slice(offset,offset+4).map(group=>tools.exec_command({cmd:"python3 - <<'PY'\nimport json,subprocess\nshas="+JSON.stringify(group.map(x=>x.sha))+"\nprint(json.dumps({s:subprocess.check_output(['git','-C','/workspace/scratch/e1cfe6e447ee/UI-Spec-Studio','cat-file','blob',s]).decode('utf-8') for s in shas},ensure_ascii=False))\nPY",shell:"/bin/bash",workdir:"/workspace/scratch/e1cfe6e447ee/UI-Spec-Studio",max_output_tokens:5000000})));
  for(const row of responses){if(row.status!=='fulfilled')throw row.reason;if(row.value.exit_code!==0)throw Error('Text object read failed');Object.assign(textBodies,JSON.parse(row.value.output));}
}
const entries=files.map(file=>file.delete?{path:file.path,mode:file.mode,type:'blob',sha:null}:known[file.sha]?{path:file.path,mode:file.mode,type:'blob',sha:file.sha}:{path:file.path,mode:file.mode,type:'blob',content:textBodies[file.sha]});
for(const entry of entries)if(!('sha' in entry)&&typeof entry.content!=='string')throw Error('Missing object content');
const batches=[];let batch=[],characters=0;
for(const entry of entries){const size=JSON.stringify(entry).length;if(characters+size>4000000&&batch.length){batches.push(batch);batch=[];characters=0;}batch.push(entry);characters+=size;}
if(batch.length)batches.push(batch);
let tree=MANIFEST.base_tree;
for(const entries of batches){
  const response=await tools.mcp__codex_apps__github_create_tree({repository_full_name:MANIFEST.repository_full_name,base_tree_sha:tree,tree_elements:entries});
  receipts.push({tool:'github_create_tree',request_scope:{base_tree_sha:tree,entries:entries.length},response});store(namespace+'_receipts',receipts);
  tree=checkResponse(response)?.sha;if(!tree)throw Error('Missing returned tree');
}
if(tree!==MANIFEST.local_tree)throw Error('Remote tree differs from committed local tree; branch is unchanged');
const commitResponse=await tools.mcp__codex_apps__github_create_commit({repository_full_name:MANIFEST.repository_full_name,parent_sha:MANIFEST.base_commit,tree_sha:tree,message:MANIFEST.message});
receipts.push({tool:'github_create_commit',response:commitResponse});store(namespace+'_receipts',receipts);
const commit=checkResponse(commitResponse)?.sha;if(!commit)throw Error('Missing returned commit');
store(namespace+'_commit',{commit,tree,local_head:MANIFEST.local_head});
const updateResponse=await tools.mcp__codex_apps__github_update_ref({repository_full_name:MANIFEST.repository_full_name,branch_name:MANIFEST.branch_name,expected_sha:MANIFEST.base_commit,force:false,sha:commit});
receipts.push({tool:'github_update_ref',response:updateResponse});store(namespace+'_receipts',receipts);checkResponse(updateResponse);
for(const file of files)if(file.sha)known[file.sha]=true;store('extra_uploaded_blobs',known);
text({checkpoint:LABEL,remote_commit:commit,tree,files:files.length,uploaded_objects:unique.length});
