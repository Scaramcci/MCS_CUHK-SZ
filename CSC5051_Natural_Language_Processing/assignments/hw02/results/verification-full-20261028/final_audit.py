"""Independent read-only reconciliation of final held-out and global raw evidence."""
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone
import copy,hashlib,json,math,os,platform,socket,statistics,subprocess,sys,threading
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
LOCAL=ROOT/'local_artifacts/verification-20261028'; PY=LOCAL/'venv/bin/python'
sys.path.insert(0,str(ROOT/'src'))
from runner import evaluate
from prompting import messages_for
from core import canonical,fingerprint

def rows(p):return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def exact(left,right):
    if isinstance(left,float) or isinstance(right,float):assert math.isclose(left,right,rel_tol=1e-12,abs_tol=1e-12),(left,right)
    elif isinstance(left,dict):
        assert left.keys()==right.keys(),(left.keys(),right.keys())
        for k in left:exact(left[k],right[k])
    elif isinstance(left,list):
        assert len(left)==len(right)
        for a,b in zip(left,right):exact(a,b)
    else:assert left==right,(left,right)
runpath=ROOT/'local_artifacts/runs/test-v1'
run=json.loads((runpath/'run.json').read_text()); cfg=json.loads((ROOT/'config/experiment.json').read_text())
assert cfg==run['config']
assert run['experiment_fingerprint']=='94c3955aea076ccdeccad0a6dae0caae85118d43872c9c2919e909bc68dc0f99'
assert all(sha(ROOT/p)==h for p,h in run['source_hashes'].items())
assert fingerprint({k:v for k,v in run.items() if k not in ('experiment_fingerprint','started_at','workers')})==run['experiment_fingerprint']
assert sha(ROOT/'data/processed/test.jsonl')==run['dataset_sha256']
dataset=rows(ROOT/'data/processed/test.jsonl'); byid={r['id']:r for r in dataset}
ps=rows(runpath/'predictions.jsonl');methods=run['methods']
assert len(ps)==320 and len({(p['id'],p['method']) for p in ps})==320
assert {(p['id'],p['method']) for p in ps}=={(i,m) for i in byid for m in methods}
assert Counter(p['status'] for p in ps)=={'success':318,'invalid':2}
assert all(p['dataset_sha256']==run['dataset_sha256'] and p['experiment_fingerprint']==run['experiment_fingerprint'] for p in ps)
# Parse every request/response journal and reconcile every reservation/settlement independently.
journals={};provider_results={};reservation_requests={}
for path in sorted((ROOT/'results/raw/requests').glob('*.jsonl')):
    events=rows(path);rid=path.stem
    assert [e['event'] for e in events]==['request','provider_response','response'],rid
    req,raw,response=events;payload=req['payload'];wire=raw['response'];result=response['result']
    assert req['request_id']==rid==result['request_id']
    assert req['reservation_id']==result['reservation_id']
    assert wire['model']==result['returned_model']==cfg['settings']['expected_returned_model']
    assert payload['model']==cfg['settings']['allowed_requested_model']
    assert payload['reasoning_effort']=='none' and payload['temperature']==0 and payload['max_completion_tokens']==768
    assert wire['choices'][0]['finish_reason']==result['finish_reason']=='stop'
    assert wire['choices'][0]['message']['content']==result['content']
    for k in ('prompt_tokens','completion_tokens'):assert wire['usage'][k]==result['usage'][k]
    assert result['usage']['prompt_tokens']<=req['input_bound']
    assert result['usage']['completion_tokens']<=768
    assert wire['usage'].get('completion_tokens_details',{}).get('reasoning_tokens',0)==0
    assert req['input_bound']==len(canonical(payload['messages']).encode())+512
    assert result['cost_micro_cny']==2*result['usage']['prompt_tokens']+8*result['usage']['completion_tokens']
    assert req['reserved_micro_cny']==2*req['input_bound']+8*768
    assert result['latency_seconds']==raw['latency_seconds'] and result['latency_seconds']>=0
    assert not result['cached']
    assert req['reservation_id'] not in reservation_requests
    journals[rid]=events;provider_results[rid]=result;reservation_requests[req['reservation_id']]=rid
ledger=rows(ROOT/'results/raw/budget.jsonl');assert ledger[0]['event']=='initialize'
assert ledger[0]['prior']==430 and ledger[0]['limit']==10000000 and ledger[0]['rates']=={'input':'2','output':'8'}
amounts={};settled=set();maximum=430
for event in ledger[1:]:
    reservation=event['reservation_id']; rid=reservation_requests[reservation]
    req=journals[rid][0];result=provider_results[rid]
    if event['event']=='reserve':
        assert reservation not in amounts
        assert event['request_id']==rid and event['amount']==req['reserved_micro_cny']
        amounts[reservation]=event['amount']
    else:
        assert event['event']=='settle' and reservation in amounts and reservation not in settled
        assert not event['exceeded_reservation']
        assert event['amount']==result['cost_micro_cny']
        assert event['input_tokens']==result['usage']['prompt_tokens'] and event['output_tokens']==result['usage']['completion_tokens']
        amounts[reservation]=event['amount'];settled.add(reservation)
    maximum=max(maximum,430+sum(amounts.values()))
    assert 430+sum(amounts.values())<=10000000
assert set(amounts)==settled==set(reservation_requests)
assert 430+sum(amounts.values())==948306
# Full prediction raw-response replay through the frozen parser and workflow, without HTTP/client/ledger.
class Replay:
    secrets=()
    def __init__(self,p):self.p=p;self.index=0
    def complete(self,messages,context):
        detail=self.p['call_details'][self.index];rid=detail['request_id'];req=journals[rid][0]
        assert req['payload']['messages']==messages
        assert fingerprint({'context':context,'url':run['endpoint'],'payload':req['payload']})==rid
        self.index+=1
        return copy.deepcopy(provider_results[rid])
with patch.object(socket,'socket',side_effect=AssertionError('Network forbidden')),patch.object(socket,'getaddrinfo',side_effect=AssertionError('DNS forbidden')):
    for p in ps:
        replay=Replay(p)
        replayed=evaluate(byid[p['id']],p['method'],cfg,replay,run['experiment_fingerprint'],threading.Event())
        for k in ('assessment','status','usage','cost_micro_cny','cost_cny_upper_bound','calls','call_details','trace','latency_seconds'):
            exact(replayed[k],p[k])
        assert replay.index==len(p['call_details'])==p['calls']
        # Actual first-request record contains exactly permitted fields, no evaluation metadata.
        first=journals[p['call_details'][0]['request_id']][0]['payload']['messages']
        supplied=json.loads(first[1]['content'].rsplit('Record to assess:\n',1)[1])
        assert supplied=={k:byid[p['id']][k] for k in ('instruction','input','output')}
        assert first[0]['role']=='system'
# Every paid request maps to exactly one prediction across both pilots and test; no hidden/double count.
all_predictions=[];run_totals={};used=set()
for name in ('dev-pilot-v1','dev-pilot-v2','test-v1'):
    predictions=rows(ROOT/f'local_artifacts/runs/{name}/predictions.jsonl');all_predictions+=predictions
    run_totals[name]={'predictions':len(predictions),'status':dict(Counter(p['status'] for p in predictions)),'calls':sum(p['calls'] for p in predictions),'cost_micro_cny':sum(p['cost_micro_cny'] for p in predictions)}
    for p in predictions:
        for detail in p['call_details']:
            rid=detail['request_id'];assert rid not in used;used.add(rid)
            exact(detail,{k:v for k,v in provider_results[rid].items() if k!='content'})
assert used==set(journals)
assert sum(p['cost_micro_cny'] for p in all_predictions)+430==948306
# Independently computed descriptive metric oracle (does not call summarize).
def dec(p):return p['assessment']['decision'] if p['status']=='success' else 'failed'
def cnt(group):return {k:sum(dec(p)==k for p in group) for k in ('keep','review','reject','failed')}
summary=json.loads((ROOT/'results/test-v1/summary.json').read_text())
independent={};missed={};call_ids=[]
for m in methods:
    group=[p for p in ps if p['method']==m];original=[p for p in group if byid[p['id']]['variant']=='unaltered'];diag=[p for p in group if byid[p['id']]['variant']=='synthetic_corruption']
    assert len(original)==len(diag)==32
    defects={d:[p for p in diag if byid[p['id']]['defect']==d] for d in ('empty','off_topic','instruction_echo','excessive_repetition')}
    assert all(len(g)==8 for g in defects.values())
    pairs={}
    for p in group:pairs.setdefault(byid[p['id']]['base_id'],{})[byid[p['id']]['variant']]=p
    actions=Counter(t['action'] for p in group for t in p['trace'])
    ls=sorted(p['latency_seconds'] for p in group)
    sensitivity={}
    for name,minsum in [('strict_all_2',8),('sum_at_least_7',7),('all_at_least_1',4)]:
        def selected(g):
            total=0
            for p in g:
                if p['status']!='success':continue
                scores=p['assessment']['scores'].values()
                if None not in scores and min(scores)>=1 and sum(scores)>=minsum:total+=1
            return total
        sensitivity[name]={'original_kept':selected(original),'diagnostic_kept':selected(diag)}
    oracle={'n':64,'statuses':dict(sorted(Counter(p['status'] for p in group).items())),'original_n':32,'original_decisions':cnt(original),'diagnostic_n':32,'diagnostic_decisions':cnt(diag),'paired_keep_original_reject_diagnostic':sum(dec(pair['unaltered'])=='keep' and dec(pair['synthetic_corruption'])=='reject' for pair in pairs.values()),'pairs_n':32,'per_defect':{d:cnt(g) for d,g in sorted(defects.items())},'calls':sum(p['calls'] for p in group),'prompt_tokens':sum(p['usage']['prompt_tokens'] for p in group),'completion_tokens':sum(p['usage']['completion_tokens'] for p in group),'cost_micro_cny':sum(p['cost_micro_cny'] for p in group),'mean_latency_seconds':sum(ls)/64,'median_latency_seconds':(ls[31]+ls[32])/2,'p95_latency_seconds':statistics.quantiles(ls,n=100,method='inclusive')[94],'actions':dict(sorted(actions.items())),'records_inspected':sum(any(t['action']=='inspect' for t in p['trace']) for p in group),'records_reassessed':sum(any(t['action']=='reassess' for t in p['trace']) for p in group),'threshold_sensitivity':sensitivity}
    exact(oracle,summary['methods'][m]);independent[m]=oracle
    retained=sorted(p['id'] for p in original if dec(p)=='keep')
    selected=[{k:byid[i][k] for k in ('instruction','input','output')} for i in retained]
    selected_bytes=(json.dumps(selected,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
    assert (ROOT/f'data/selected/test-v1/{m}.json').read_bytes()==selected_bytes
    selection=json.loads((ROOT/f'results/test-v1/{m}-selection.json').read_text())
    assert selection['ids']==retained and selection['count']==len(retained) and selection['sha256']==hashlib.sha256(selected_bytes).hexdigest()
    if m.startswith('agent'):
        missed[m]=[{'id':p['id'],'word_count':len(byid[p['id']]['output'].split())} for p in group if (not byid[p['id']]['output'].strip() or len(byid[p['id']]['output'].split())>120 or byid[p['id']]['defect']=='excessive_repetition') and not any(t['action']=='inspect' for t in p['trace'])]
lookup={(p['id'],p['method']):p for p in ps}
for comparison,item in summary['decision_differences'].items():
    left,right=comparison.split('_vs_');changes=[r['id'] for r in dataset if dec(lookup[r['id'],left])!=dec(lookup[r['id'],right])]
    assert item=={'changed_n':len(changes),'changed_ids':changes}
assert summary['provenance']['prediction_sha256']==sha(runpath/'predictions.jsonl')
assert summary['provenance']['analysis_source_sha256']==sha(ROOT/'src/analyze.py')
# Re-run actual analysis CLI to isolated destinations; compare every produced byte.
cmd=[str(PY),'-B','src/analyze.py','--dataset','data/processed/test.jsonl','--run','local_artifacts/runs/test-v1','--output',str(OUT/'reproduced-test-analysis'),'--cleaned-output',str(LOCAL/'selected-test-v1')]
r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'PYTHONDONTWRITEBYTECODE':'1'})
(OUT/'final-analysis-stdout.txt').write_text(r.stdout);(OUT/'final-analysis-stderr.txt').write_text(r.stderr)
assert r.returncode==0
for p in (OUT/'reproduced-test-analysis').glob('*.json'):assert p.read_bytes()==(ROOT/'results/test-v1'/p.name).read_bytes()
for p in (LOCAL/'selected-test-v1').glob('*.json'):assert p.read_bytes()==(ROOT/'data/selected/test-v1'/p.name).read_bytes()
# Fresh tests after final prompt refinement; preserve initial evidence separately.
commands=[]
for script in ('tests/offline_smoke.py',str(OUT/'independent_tests.py')):
    cmdtest=[str(PY),'-B',script]; t=subprocess.run(cmdtest,cwd=ROOT,text=True,capture_output=True,env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'TMPDIR':str(LOCAL),'PYTHONDONTWRITEBYTECODE':'1'})
    n=len(commands);(OUT/f'final-tests-{n}-stdout.txt').write_text(t.stdout);(OUT/f'final-tests-{n}-stderr.txt').write_text(t.stderr)
    commands.append({'command':cmdtest,'exit':t.returncode});assert t.returncode==0
assert all(sha(ROOT/p)==h for p,h in run['source_hashes'].items())
record={'executor':'/root/verifier','time':datetime.now(timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'fingerprint':run['experiment_fingerprint'],'prediction_sha256':sha(runpath/'predictions.jsonl'),'input_hashes':{p:sha(ROOT/p) for p in sorted(set(run['source_hashes'])|{'config/experiment.json','src/prepare_data.py','src/analyze.py','tests/test_core.py'})},'runs':run_totals,'global_journals':len(journals),'global_ledger_micro_cny':430+sum(amounts.values()),'global_highest_spent_plus_reservations_micro_cny':maximum,'ledger_sha256':sha(ROOT/'results/raw/budget.jsonl'),'final_matrix_rows':len(ps),'replayed_predictions':len(ps),'independent_statistics_match':True,'analysis_bytes_match':True,'selected_dataset_bytes_match':True,'analysis_command':cmd,'analysis_exit':r.returncode,'fresh_test_commands':commands,'missed_prompt_inspection_triggers':missed,'invalid_predictions':[{'id':p['id'],'method':p['method'],'calls':p['calls'],'status':p['status']} for p in ps if p['status']!='success'],'scope':'Offline exact-result reconciliation, not independent live model repetition or human quality validation'}
(OUT/'final-run.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
(OUT/'independent-statistics.json').write_text(json.dumps(independent,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','predictions':len(ps),'raw_journals':len(journals),'ledger_micro_cny':948306,'test_cost_micro_cny':run_totals['test-v1']['cost_micro_cny'],'test_calls':run_totals['test-v1']['calls'],'known_inference_failures':record['invalid_predictions'],'missed_trigger_counts':{m:len(a) for m,a in missed.items()}},indent=2))
