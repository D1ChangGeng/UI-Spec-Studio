"""Explicit synthetic protocol records for mechanics tests; never Agent evidence."""
import copy
import hashlib
import json

def transcript(row,root='TEST-DOUBLE-parent'):
    requests=[];wire=[];counter=0
    def rpc(method,params,result):
        nonlocal counter
        counter+=1;requests.append({'id':counter,'method':method,'params':params});wire.append({'id':counter,'result':result})
    def event(method,params):wire.append({'method':method,'params':copy.deepcopy(params)})
    def meta(tid,role=None,parent=None):
        return {'id':tid,'model':row['main_model'] if parent is None else row['subagent_model'],
            'reasoningEffort':row.get('main_effort' if parent is None else 'subagent_effort','low'),
            'ephemeral':row.get('session_persistence','ephemeral')=='ephemeral','agentRole':role,'parentThreadId':parent,
            'source':'appServer' if parent is None else {'subAgent':{'thread_spawn':{'parent_thread_id':parent,'agent_role':role,'depth':1}}}}
    def usage(tid,turn):event('thread/tokenUsage/updated',{'threadId':tid,'turnId':turn,'tokenUsage':{'total':{
        'inputTokens':10,'cachedInputTokens':0,'outputTokens':1,'totalTokens':11},'last':{}}})
    def turn(tid,ident,status):event('turn/started' if status=='inProgress' else 'turn/completed',{
        'threadId':tid,'turn':{'id':ident,'status':status,'error':None,'items':[]}})
    def tool(tid,turn_id,item):
        started=copy.deepcopy(item);started['status']='inProgress'
        event('item/started',{'threadId':tid,'turnId':turn_id,'item':started})
        event('item/completed',{'threadId':tid,'turnId':turn_id,'item':item})
    policy={'type':'workspaceWrite','networkAccess':row.get('network_access',False)}
    rpc('initialize',{'clientInfo':{'name':'MECHANICAL TEST ONLY','version':'fixture'}},{'userAgent':'TEST DOUBLE'})
    requests.append({'method':'initialized','params':{}})
    rpc('thread/start',{'model':row['main_model'],'sandbox':'workspace-write','approvalPolicy':'on-request',
        'approvalsReviewer':'auto_review','ephemeral':row.get('session_persistence','ephemeral')=='ephemeral'},
        {'thread':meta(root),'approvalPolicy':'on-request','approvalsReviewer':'auto_review','sandbox':policy})
    rpc('turn/start',{'threadId':root,'sandboxPolicy':policy,'input':[{'type':'text','text':'synthetic fixture only'}]},
        {'turn':{'id':'parent-turn','status':'inProgress'}})
    turn(root,'parent-turn','inProgress')
    roles={'B':[row.get('generic_role_binding','default')],'C':['ui_researcher'],'D':['ui_researcher'],
        'E-challenger':['ui_researcher','ui_challenger'],'E-observer':['ui_researcher','ui_experience_observer'],
        'F-integrator':['ui_integrator']}.get(row['condition'],[])
    for n,role in enumerate(roles):
        child=root+'-child-'+str(n);ct='child-turn-'+str(n)
        tool(root,'parent-turn',{'type':'collabAgentToolCall','id':'spawn-'+str(n),'tool':'spawnAgent',
            'status':'completed','senderThreadId':root,'receiverThreadIds':[child],'model':row['subagent_model']})
        rpc('thread/read',{'threadId':child,'includeTurns':False},{'thread':meta(child,role,root)})
        turn(child,ct,'inProgress')
        tool(child,ct,{'type':'commandExecution','id':'fixture-tool','command':'synthetic fixture, never executed',
            'status':'completed','aggregatedOutput':'explicit mechanical test double','exitCode':0})
        usage(child,ct);turn(child,ct,'completed')
    usage(root,'parent-turn');turn(root,'parent-turn','completed')
    return requests,wire

def encoded(records):return b''.join((json.dumps(x,separators=(',',':'))+'\n').encode() for x in records)
def manifest_files(row,run):
    requests,wire=transcript(row,run['thread_id']);raw=encoded(wire)
    index=[{'sequence':i+1,'retention':'original_wire_line','sha256':hashlib.sha256(line).hexdigest()}
           for i,line in enumerate(raw.splitlines(keepends=True))]
    return {'wire.jsonl':raw,'requests.jsonl':encoded(requests),'wire-index.jsonl':encoded(index)}
