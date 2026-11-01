"""Scoped public Codex app-server transport and evidence checks.

Only standard JSON-RPC notifications/read methods are used. Safe wire lines are
stored byte-for-byte; mixed envelopes containing reasoning have a separately
labelled projection. Neither a projection nor returned agent prose proves a tool
call. This module never reads authentication or changes CODEX_HOME.
"""
from __future__ import annotations
import collections
import hashlib
import json
import os
from pathlib import Path
import queue
import subprocess
import threading
import time

TOOLS={'commandExecution','mcpToolCall','dynamicToolCall','collabAgentToolCall',
       'subAgentActivity','webSearch','imageView','fileChange'}
WORK_TOOLS=TOOLS-{'collabAgentToolCall','subAgentActivity'}
ROLES={'C':{'ui_researcher'},'D':{'ui_researcher'},
       'E-challenger':{'ui_researcher','ui_challenger'},
       'E-observer':{'ui_researcher','ui_experience_observer'},
       'F-integrator':{'ui_integrator'}}
ALL_ROLES={'ui_researcher','ui_integrator','ui_challenger','ui_experience_observer'}
REASONING_NOTIFICATIONS=['item/reasoning/textDelta','item/reasoning/summaryTextDelta',
                         'item/reasoning/summaryPartAdded']

class AppServerError(ValueError):pass
class ApprovalBlocked(AppServerError):pass

def digest(raw):return hashlib.sha256(raw).hexdigest()
def write_json(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def json_lines(raw):
    result=[]
    for line in raw.splitlines():
        if line.strip():
            obj=json.loads(line)
            if not isinstance(obj,dict):raise AppServerError('JSON-RPC record must be an object')
            result.append(obj)
    return result

def contains_reasoning(value):
    if isinstance(value,dict):
        if 'reasoning' in str(value.get('type','')).lower() or 'encrypted_content' in value:return True
        return any(contains_reasoning(x) for x in value.values())
    return isinstance(value,list) and any(contains_reasoning(x) for x in value)

def public_projection(value):
    if isinstance(value,dict):
        if 'reasoning' in str(value.get('type','')).lower() or 'encrypted_content' in value:return None
        return {k:public_projection(v) for k,v in value.items()}
    if isinstance(value,list):
        return [public_projection(v) for v in value if not (isinstance(v,dict) and
            ('reasoning' in str(v.get('type','')).lower() or 'encrypted_content' in v))]
    return value

def successful_work(item):
    if item.get('type') not in WORK_TOOLS:return False
    if item.get('status') not in {None,'completed'} or item.get('error') or item.get('isError'):return False
    if item.get('type')=='dynamicToolCall' and item.get('success') is not True:return False
    return item.get('type')!='commandExecution' or item.get('exitCode')==0

def inspect_evidence(requests,wire,row):
    """Check native facts only; no assessment of research depth or UI quality."""
    problems=[];calls={};metadata={};turns={};turn_starts=set();items={};starts=set();ends=set();usage={};root=None
    policy_response=None;spawned={};resolved_models={};parent_turns=[]
    for request in requests:
        if 'method' in request and 'id' in request:
            if request['id'] in calls:problems.append('duplicate client request id')
            calls[request['id']]=request
        if isinstance(request.get('result'),dict) and request['result'].get('decision') in {'accept','acceptForSession'}:
            problems.append('client supplied an approval instead of native review')
    def item_record(tid,turn,item,complete=False):
        if not isinstance(item,dict) or item.get('type') not in TOOLS:return
        key=(tid,item.get('id'));items[key]={'thread_id':tid,'turn_id':turn,'item':item}
        if complete and item.get('type')!='subAgentActivity':ends.add(key)
        if complete and item.get('status') in {'inProgress','pending','pendingInit'}:problems.append('completed item still has nonterminal tool status')
        if item.get('status') in {'declined','denied','rejected'}:problems.append('native tool approval was denied')
        if item.get('type')=='collabAgentToolCall' and item.get('tool')=='spawnAgent' and item.get('status')=='completed':
            if item.get('senderThreadId')!=tid:problems.append('spawn sender differs from native event scope')
            for child in item.get('receiverThreadIds',[]):spawned[child]=tid
        if item.get('type')=='subAgentActivity' and item.get('model'):
            resolved_models[item.get('agentThreadId')]=item['model']
    for obj in wire:
        if contains_reasoning(obj):problems.append('reasoning content present in public wire')
        method=obj.get('method');params=obj.get('params') or {}
        if method=='thread/started':
            thread=params.get('thread',{});metadata[thread.get('id')]=thread
        elif method in {'turn/started','turn/completed'}:
            turn=params.get('turn',{});key=(params.get('threadId'),turn.get('id'))
            if method=='turn/started':turn_starts.add(key)
            else:turns[key]=turn
        elif method in {'item/started','item/completed'}:
            item=params.get('item',{});key=(params.get('threadId'),item.get('id'))
            if method=='item/started' and item.get('type') in TOOLS-{'subAgentActivity'}:starts.add(key)
            item_record(params.get('threadId'),params.get('turnId'),item,method=='item/completed')
        elif method=='thread/tokenUsage/updated':usage[params.get('threadId')]=params.get('tokenUsage')
        elif method=='error' and params.get('willRetry') is not True:problems.append('native error notification')
        elif method and 'id' in obj:problems.append('unhandled server request or user approval')
        if 'error' in obj and obj.get('id') in calls and calls[obj['id']]['method']!='account/usage/read':
            problems.append('native RPC failed: '+calls[obj['id']]['method'])
        if 'result' not in obj or obj.get('id') not in calls:continue
        request=calls[obj['id']];kind=request['method'];result=obj['result'];p=request.get('params',{})
        if not isinstance(result,dict):raise AppServerError('native result must be an object')
        if kind=='thread/start':
            thread=result.get('thread',{});tid=thread.get('id')
            if root is not None:problems.append('more than one new parent thread')
            root=tid;metadata[tid]=thread;policy_response=result
            if p.get('ephemeral')!=(row.get('session_persistence','ephemeral')=='ephemeral'):problems.append('session persistence differs from registration')
            if p.get('model')!=row['main_model']:problems.append('parent requested model differs from registration')
            if p.get('experimentalRawEvents'):problems.append('internal raw events must not be enabled')
            if p.get('sandbox')!='workspace-write' or p.get('approvalPolicy')!='on-request' or p.get('approvalsReviewer')!='auto_review':
                problems.append('parent permission request differs from the frozen safe policy')
        elif kind=='thread/read':
            thread=result.get('thread',{})
            if thread.get('id')!=p.get('threadId'):problems.append('metadata response has the wrong thread')
            metadata[thread.get('id')]=thread
        elif kind=='turn/start':
            parent_turns.append((p.get('threadId'),result.get('turn',{}).get('id')))
            sandbox=p.get('sandboxPolicy',{})
            if sandbox.get('type')!='workspaceWrite' or sandbox.get('networkAccess') is not row.get('network_access',False):
                problems.append('turn sandbox/network differs from registration')
        elif kind=='thread/turns/list':
            for turn in result.get('data',[]):turns[(p.get('threadId'),turn.get('id'))]=turn
        elif kind=='thread/items/read':
            expected=set(p.get('itemIds',[]));returned=set()
            for entry in result.get('data',[]):
                item=entry.get('item',{});returned.add(item.get('id'))
                if entry.get('turnId')!=p.get('turnId'):problems.append('tool readback turn differs from request')
                item_record(p.get('threadId'),entry.get('turnId'),item,True)
            if expected!=returned:problems.append('incomplete native item readback')
    if not root or len(parent_turns)!=1 or parent_turns[0][0]!=root:
        problems.append('exactly one newly started parent turn is required')
    elif parent_turns[0] not in turns:problems.append('started parent turn has no native completion')
    participants={root}|set(spawned)
    for request in calls.values():
        if request.get('params',{}).get('threadId') not in participants|{None}:
            problems.append('request reads or controls a thread outside this run subtree')
    for child,parent in spawned.items():
        if parent not in participants or child==root:problems.append('child has no matching parent lineage')
        current=parent;seen={child}
        while current in spawned:
            if current in seen:problems.append('cyclic child lineage');break
            seen.add(current);current=spawned[current]
        if current!=root:problems.append('child is outside this run subtree')
    persistent=row.get('session_persistence','ephemeral')=='persistent'
    for tid in participants:
        if not tid:continue
        meta=metadata.get(tid,{})
        if not meta:problems.append('missing native thread metadata')
        if meta.get('model')!=(row['main_model'] if tid==root else row['subagent_model']):problems.append('native configured model differs from registration or is unknown')
        if tid in resolved_models and resolved_models[tid]!=(row['main_model'] if tid==root else row['subagent_model']):
            problems.append('native creation-resolved model differs from registration')
        expected_effort=row.get('main_effort' if tid==root else 'subagent_effort')
        if expected_effort is not None and meta.get('reasoningEffort')!=expected_effort:problems.append('native reasoning effort differs from registration or is unknown')
        if meta.get('ephemeral') is not (not persistent):problems.append('native persistence differs from registration')
        if tid!=root:
            source=meta.get('source',{}).get('subAgent',{}) if isinstance(meta.get('source'),dict) else {}
            source=source.get('thread_spawn',{}) if isinstance(source,dict) else {}
            if meta.get('parentThreadId')!=spawned[tid] or source.get('parent_thread_id')!=spawned[tid]:problems.append('native child parent metadata differs from spawn')
            if 'agentRole' not in meta or 'agent_role' not in source:problems.append('native role metadata is absent, not an observed null binding')
            if source.get('agent_role')!=meta.get('agentRole'):problems.append('native role metadata disagrees')
            if not any(t==tid and successful_work(record['item']) and (t,i) in ends for (t,i),record in items.items()):
                problems.append('child has no successful native work-tool completion')
        owned=[(key,turn) for key,turn in turns.items() if key[0]==tid]
        if not owned or any(turn.get('status')!='completed' or turn.get('error') is not None for _,turn in owned):
            problems.append('parent or child turn failed, was interrupted, or has no terminal completion')
        if not persistent and any(key not in turn_starts for key,_ in owned):problems.append('missing live turn start')
        total=usage.get(tid,{}).get('total',{}) if isinstance(usage.get(tid),dict) else {}
        if any(type(total.get(k)) is not int or total[k]<0 for k in ('inputTokens','cachedInputTokens','outputTokens','totalTokens')):
            problems.append('missing or invalid native token usage')
    if not persistent and (starts!=ends):problems.append('incomplete live tool lifecycle')
    if turn_starts-set(turns):problems.append('started parent or child turn is unfinished')
    if any(tid not in participants for tid,_ in items):problems.append('tool record is outside this run subtree')
    roles={tid:metadata.get(tid,{}).get('agentRole') for tid in spawned}
    condition=row['condition'];required=ROLES.get(condition,set())
    if condition in {'A','F-main'} and spawned:problems.append('main-agent-only condition spawned a child')
    elif condition=='B':
        expected_role=row.get('generic_role_binding','default')
        if not roles or any(role!=expected_role for role in roles.values()):problems.append('generic arm needs its frozen observed native default-role binding')
    elif condition in ROLES:
        if set(roles.values())!=required:problems.append('required specialist intervention or native role binding is missing')
    elif condition=='G-final-runtime' and any(role not in ALL_ROLES for role in roles.values()):
        problems.append('final-runtime child has an unregistered role')
    if policy_response:
        sandbox=policy_response.get('sandbox',{})
        if policy_response.get('approvalPolicy')!='on-request' or policy_response.get('approvalsReviewer')!='auto_review':
            problems.append('native approval routing was not confirmed')
        if sandbox.get('type')!='workspaceWrite' or sandbox.get('networkAccess') is not row.get('network_access',False):
            problems.append('native sandbox/network policy was not confirmed')
    return {'thread_id':root,'child_thread_ids':sorted(spawned),'actual_auxiliary_agent_count':len(spawned),
            'completed_turns':sum(t.get('status')=='completed' for (tid,_),t in turns.items() if tid==root),
            'native_roles':roles,'native_metadata':metadata,'native_usage_by_thread':usage,
            'native_model_metadata':{tid:{'configured':metadata.get(tid,{}).get('model'),
                'resolved_at_creation':resolved_models.get(tid),'per_response_model':None} for tid in participants if tid},
            'tool_items':list(items.values()),'evidence_errors':sorted(set(problems))}

class Client:
    def __init__(self,process,out,deadline,persistence):
        self.process=process;self.out=out;self.deadline=deadline;self.persistence=persistence
        self.queue=queue.Queue();self.responses={};self.requests=[];self.events=[];self.counter=0;self.sequence=0
        self.root=None;self.children=set();self.metadata_read=set();self.pending_children=set();self.completed=set();self.active_turns={}
        self.failures=[];self.approval_blocked=False;self.filters=collections.Counter();self.malformed_lines=0
        self.files={name:(out/name).open('wb') for name in ['requests.jsonl','wire.jsonl','wire-index.jsonl','projections.jsonl']}
        self.reader_thread=threading.Thread(target=self.reader,daemon=True);self.reader_thread.start()
    def reader(self):
        try:
            for line in iter(self.process.stdout.readline,b''):self.queue.put(line)
        finally:self.queue.put(None)
    def append(self,name,obj):
        raw=(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n').encode();self.files[name].write(raw);self.files[name].flush()
    def send(self,obj):
        self.requests.append(obj);self.append('requests.jsonl',obj)
        self.process.stdin.write((json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n').encode());self.process.stdin.flush()
    def pump(self,timeout=None):
        remaining=self.deadline-time.monotonic()
        if remaining<=0:raise subprocess.TimeoutExpired('app-server turn',0)
        try:raw=self.queue.get(timeout=min(remaining,timeout or remaining))
        except queue.Empty:raise subprocess.TimeoutExpired('app-server response',remaining)
        if raw is None:raise AppServerError('app-server stream ended before evidence collection finished')
        self.sequence+=1
        try:
            obj=json.loads(raw)
            if not isinstance(obj,dict):raise ValueError('JSON-RPC object required')
        except (ValueError,UnicodeError) as exc:
            self.malformed_lines+=1
            with (self.out/'private-unparsed-wire.bin').open('ab') as failed:failed.write(raw)
            self.append('wire-index.jsonl',{'sequence':self.sequence,'sha256':digest(raw),
                'retention':'unparsed_private_diagnostic_not_public_wire'})
            raise AppServerError('malformed app-server wire; original bytes quarantined for private review') from exc
        method=obj.get('method','response');params=obj.get('params') or {}
        record={'sequence':self.sequence,'sha256':digest(raw),'method':method}
        if 'reasoning' in method.lower() or method.startswith('rawResponse'):
            record['retention']='omitted_reasoning_or_internal_event'
        elif contains_reasoning(obj):
            record['retention']='projection_reasoning_removed'
            self.append('projections.jsonl',{'sequence':self.sequence,'original_sha256':record['sha256'],
                'derived':True,'reason':'reasoning items removed','message':public_projection(obj)})
        elif method.startswith('account/'):
            record['retention']='omitted_account_notification'
        else:
            record['retention']='original_wire_line';self.files['wire.jsonl'].write(raw);self.files['wire.jsonl'].flush();self.events.append(obj)
        self.filters[record['retention']]+=1;self.append('wire-index.jsonl',record)
        if method in {'item/started','item/completed'}:
            item=params.get('item',{})
            if item.get('type')=='collabAgentToolCall' and item.get('tool')=='spawnAgent':
                for tid in item.get('receiverThreadIds',[]):
                    self.children.add(tid);self.pending_children.add(tid)
        if method=='turn/started':
            self.active_turns[params.get('threadId')]=params.get('turn',{}).get('id');self.completed.discard(params.get('threadId'))
        if method=='turn/completed':
            tid=params.get('threadId');self.completed.add(tid);self.active_turns.pop(tid,None)
        if 'id' in obj and ('result' in obj or 'error' in obj):self.responses[obj['id']]=obj
        elif 'id' in obj and method:
            self.approval_blocked=True
            if method in {'item/commandExecution/requestApproval','item/fileChange/requestApproval'}:
                self.send({'id':obj['id'],'result':{'decision':'cancel'}})
            else:self.send({'id':obj['id'],'error':{'code':-32000,'message':'This evidence client cannot grant approval, supply credentials, or execute client-side tools.'}})
            raise ApprovalBlocked('native runtime requested an unresolved client approval or external client capability')
        return obj
    def request(self,method,params):
        self.counter+=1;ident=self.counter;self.send({'id':ident,'method':method,'params':params})
        while ident not in self.responses:self.pump()
        response=self.responses.pop(ident)
        if 'error' in response:raise AppServerError(method+': '+str(response['error']))
        return response['result']
    def read_children(self):
        while self.pending_children:
            tid=self.pending_children.pop()
            if tid in self.metadata_read:continue
            self.request('thread/read',{'threadId':tid,'includeTurns':False});self.metadata_read.add(tid)
            # Ephemeral threads cannot resume or page history on tested 0.166.
            if self.persistence=='persistent':self.request('thread/resume',{'threadId':tid,'excludeTurns':True})
    def page_history(self,tid):
        for method,extra in [('thread/turns/list',{'itemsView':'notLoaded'}),('thread/items/list',{})]:
            cursor=None;seen=set()
            while True:
                params={'threadId':tid,'limit':100,'sortDirection':'asc',**extra}
                if cursor:params['cursor']=cursor
                result=self.request(method,params)
                if method=='thread/items/list':
                    grouped=collections.defaultdict(list)
                    for entry in result.get('data',[]):
                        item=entry.get('item',{})
                        if not contains_reasoning(item):grouped[entry['turnId']].append(item['id'])
                    for turn,ids in grouped.items():
                        self.request('thread/items/read',{'threadId':tid,'turnId':turn,'itemIds':ids})
                cursor=result.get('nextCursor')
                if not cursor:break
                if cursor in seen:raise AppServerError('repeated history cursor')
                seen.add(cursor)
    def close(self):
        for stream in self.files.values():stream.close()

def execute(*,command,row,workspace,out,env,stop_process,prompt,identity=None,on_cancel=None):
    """Run one fresh parent. Callers preserve the returned failed attempt too."""
    out.mkdir(parents=True);started=time.monotonic();deadline=started+row['timeout_seconds']
    client=None;process=None;status='evidence_incomplete';interrupted=False;errors=[];costs={};cleanup={};code=None
    persistence=row.get('session_persistence','ephemeral')
    with (out/'stderr.log').open('wb') as stderr:
        try:
            process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=stderr,
                cwd=workspace,env=env,start_new_session=(os.name!='nt'))
            client=Client(process,out,deadline,persistence)
            client.request('initialize',{'clientInfo':{'name':'ui_spec_study','version':'1.0.0'},'capabilities':{
                'experimentalApi':True,'explicitGatewayOauth':True,'optOutNotificationMethods':REASONING_NOTIFICATIONS}})
            client.send({'method':'initialized','params':{}})
            result=client.request('thread/start',{'cwd':str(workspace),'model':row['main_model'],
                'sandbox':'workspace-write','approvalPolicy':'on-request','approvalsReviewer':'auto_review',
                'ephemeral':persistence=='ephemeral','historyMode':'paginated'})
            client.root=result['thread']['id']
            client.request('turn/start',{'threadId':client.root,'input':[{'type':'text','text':prompt}],
                'effort':row['main_effort'],'sandboxPolicy':{'type':'workspaceWrite','writableRoots':[str(workspace)],
                    'networkAccess':row.get('network_access',False)}})
            while client.root not in client.completed or not client.children<=client.completed:
                client.read_children()
                if client.root in client.completed and client.children<=client.completed:break
                client.pump()
            client.read_children()
            client.request('thread/read',{'threadId':client.root,'includeTurns':False})
            if persistence=='persistent':
                for tid in [client.root,*sorted(client.children)]:client.page_history(tid)
            for tid in [client.root,*sorted(client.children)]:
                costs[tid]={'native_usage_usd':None,'estimated_usage_usd':None,
                    'source':'not_available_in_standard_execution_notifications',
                    'boundary':'No billing request or token-to-dollar estimate was made.'}
            status='captured'
        except KeyboardInterrupt:
            interrupted=True;status='interrupted'
            if on_cancel:on_cancel()
        except subprocess.TimeoutExpired as exc:
            status='timed_out';errors.append(str(exc))
            if on_cancel:on_cancel()
        except ApprovalBlocked as exc:status='approval_blocked';errors.append(str(exc))
        except (AppServerError,OSError,ValueError,KeyError,TypeError) as exc:errors.append(str(exc))
        finally:
            if process:
                try:
                    if status=='captured':
                        process.stdin.close()
                        try:code=process.wait(timeout=5)
                        except subprocess.TimeoutExpired:code=stop_process(process)
                    else:code=stop_process(process)
                    cleanup={'direct_child_reaped':True,'returncode':code}
                except KeyboardInterrupt:
                    interrupted=True;status='interrupted'
                    if on_cancel:on_cancel()
                    try:
                        code=stop_process(process);cleanup={'direct_child_reaped':True,'returncode':code}
                    except (OSError,subprocess.SubprocessError) as exc:
                        code=process.poll();cleanup={'direct_child_reaped':code is not None,'returncode':code,'error':str(exc)};errors.append(str(exc))
                except (OSError,subprocess.SubprocessError) as exc:
                    code=process.poll();cleanup={'direct_child_reaped':code is not None,'returncode':code,'error':str(exc)};errors.append(str(exc))
                if client:client.reader_thread.join(timeout=1)
                for stream in (process.stdin,process.stdout):
                    if stream and not stream.closed:
                        try:stream.close()
                        except OSError as exc:errors.append(str(exc))
            if client:client.close()
    inspected={'thread_id':client.root if client else None,'completed_turns':0,'child_thread_ids':[],
               'native_usage_by_thread':{},'actual_auxiliary_agent_count':0}
    if client:
        try:inspected=inspect_evidence(client.requests,client.events,row);errors+=inspected['evidence_errors']
        except (AppServerError,ValueError,TypeError,KeyError,AttributeError) as exc:errors.append('native evidence analysis failed: '+str(exc))
        except KeyboardInterrupt:
            interrupted=True;status='interrupted'
            if on_cancel:on_cancel()
    if code not in (None,0):errors.append('app-server process did not exit successfully')
    if status=='captured':status='process_completed' if not errors else 'evidence_incomplete'
    result={**inspected,'status':status,'interrupted':interrupted,'returncode':code,
        'elapsed_seconds':round(time.monotonic()-started,3),'process_cleanup':cleanup,
        'failure_events':len(set(errors)),'malformed_lines':client.malformed_lines if client else 0,'evidence_errors':sorted(set(errors)),
        'reported_usage':[inspected.get('native_usage_by_thread',{}).get(inspected.get('thread_id'))],
        'total_subagent_usage':None,'native_cost_by_thread':costs,'native_total_cost_usd':None,
        'usage_boundary':'Native per-thread totals are retained separately; no inferred child-cost sum or token-to-dollar estimate.',
        'history_capture':'live_only_no_pagination' if persistence=='ephemeral' else 'live_and_public_paged_readback'}
    write_json(out/'native-summary.json',result)
    files={name:{'path':name,'sha256':digest((out/name).read_bytes())} for name in
           ['requests.jsonl','wire.jsonl','wire-index.jsonl','projections.jsonl','native-summary.json','stderr.log'] if (out/name).is_file()}
    manifest={'schema_version':1,'transport':'app-server','derived':False,'root_thread_id':result['thread_id'],
        'session_persistence':persistence,'profile_mode':row.get('profile_mode'),'network_access':row.get('network_access',False),
        'study_identity':identity,
        'history_capture':result['history_capture'],'files':files,
        'retention':'wire.jsonl contains selected original standard JSON-RPC lines. Reasoning is omitted; mixed envelopes are explicitly derived projections with original-line hashes.',
        'internal_raw_events':False,'filters':dict(client.filters) if client else {}}
    private=out/'private-unparsed-wire.bin'
    if private.exists():manifest['private_diagnostic']={'path':private.name,'sha256':digest(private.read_bytes()),
        'publication':'not a public evidence artifact; may contain unclassified private content'}
    write_json(out/'evidence-manifest.json',manifest)
    return result

def verify_manifest(manifest,load_artifact,row,run,events_bytes):
    """Verify hashed native sources; the human execution audit remains separate."""
    if manifest.get('schema_version')!=1 or manifest.get('transport')!='app-server' or manifest.get('derived') is not False:
        raise AppServerError('unknown or derived native evidence manifest')
    if manifest.get('internal_raw_events') is not False:raise AppServerError('internal raw events are not release evidence')
    for key in ('profile_mode','session_persistence','network_access'):
        if manifest.get(key)!=row.get(key):raise AppServerError('native manifest differs from frozen '+key)
    expected={key:run.get(key) for key in ('cell_id','registration_sha256','input_workspace_identity','task_sha256')}
    if manifest.get('study_identity')!=expected:raise AppServerError('native evidence belongs to a different study identity')
    files=manifest.get('files',{});loaded={name:load_artifact(reference) for name,reference in files.items()}
    for name in ('wire.jsonl','requests.jsonl','wire-index.jsonl'):
        if name not in loaded:raise AppServerError('native evidence source missing: '+name)
    wire=loaded['wire.jsonl']
    if wire!=events_bytes or run.get('events',{}).get('derived') is not False or run.get('events',{}).get('format')!='codex-app-server-jsonrpc':
        raise AppServerError('declared events must be the fixed original native wire, not a CLI projection')
    index=json_lines(loaded['wire-index.jsonl'])
    expected_hashes=[r['sha256'] for r in index if r.get('retention')=='original_wire_line']
    if [digest(line) for line in wire.splitlines(keepends=True)]!=expected_hashes:
        raise AppServerError('native wire differs from its original-line index')
    result=inspect_evidence(json_lines(loaded['requests.jsonl']),json_lines(wire),row)
    if result['thread_id']!=run.get('thread_id') or manifest.get('root_thread_id')!=result['thread_id']:
        raise AppServerError('native parent identity differs from run record')
    if result['evidence_errors']:raise AppServerError('; '.join(result['evidence_errors']))
    return result
