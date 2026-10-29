"""Independent offline checks; mocked calls/fixtures are not experiment evidence."""
import copy, itertools, json, multiprocessing, os, socket, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from core import DIMENSIONS, ExperimentError, InvalidAssessment, parse_assessment, parse_env, canonical
from budget import BudgetLedger, BudgetExceeded
from client import APIClient, ProviderFailure, IncompleteRequest
from prompting import messages_for
from agent import structural_feedback,evaluate_with_agent
from main import load_config
from analyze import summarize,percentile
RATES={'input_cny_per_million':'2','output_cny_per_million':'8','prior_spend_cny_upper_bound':'0.000430'}
CREDS={'DEEPSEEK_API_KEY':'verifier-public-synthetic-key','DEEPSEEK_MODEL':'mock','DEEPSEEK_BASE_URL':'https://example.invalid/v3'}
SETTINGS={'temperature':0,'reasoning_effort':'none','max_completion_tokens':768,'max_input_tokens_bound':24000,'timeout_seconds':2,'allowed_requested_model':'mock','expected_returned_model':'mock'}
GOOD={'scores':dict.fromkeys(DIMENSIONS,2),'decision':'keep','reason':'Synthetic assessment.'}
def reserve_worker(path):
    b=BudgetLedger(path,'0.01',RATES)
    try:b.reserve(1000,100,'independent-worker')
    except BudgetExceeded:pass
class IndependentTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'local_artifacts/verification-20261028')
        self.d=Path(self.temp.name)
        self.patches=[patch.object(socket,'socket',side_effect=AssertionError('No network')),patch.object(socket,'getaddrinfo',side_effect=AssertionError('No DNS'))]
        for p in self.patches:p.start()
    def tearDown(self):
        for p in self.patches:p.stop()
        self.temp.cleanup()
    def test_exhaustive_rubric_decisions(self):
        for scores in itertools.product([0,1,2,None],repeat=4):
            expected='reject' if any(x==0 for x in scores) else 'keep' if scores==(2,2,2,2) else 'review'
            a={'scores':dict(zip(DIMENSIONS,scores)),'decision':expected,'reason':'Fixture.'}
            self.assertEqual(parse_assessment(json.dumps(a))['decision'],expected)
            for wrong in {'keep','review','reject'}-{expected}:
                a['decision']=wrong
                with self.assertRaises(InvalidAssessment):parse_assessment(json.dumps(a))
    def test_label_mutation_cannot_change_prompts_or_feedback(self):
        row={'id':'idA','instruction':'Write a greeting.','input':'','output':'Hello.'}
        other={**row,'id':'idB','variant':'synthetic_corruption','hidden_label':'FROZEN_LABEL_SENTINEL','source_index':123,'base_id':'BASE_SENTINEL','split':'test','defect':'DETECT_SENTINEL'}
        for method in ('zero_shot','few_shot','chain_of_thought','agent'):
            self.assertEqual(messages_for(method,load_config(),row),messages_for(method,load_config(),other))
        self.assertEqual(structural_feedback(row),structural_feedback(other))
    def test_process_budget_lock(self):
        path=self.d/'ledger.jsonl'; b=BudgetLedger(path,'0.01',RATES)
        ctx=multiprocessing.get_context('fork')
        ps=[ctx.Process(target=reserve_worker,args=(path,)) for _ in range(12)]
        for p in ps:p.start()
        for p in ps:p.join(10);self.assertEqual(p.exitcode,0)
        self.assertEqual(b.snapshot()['spent_or_reserved_micro_cny'],430+3*2800)
    def test_budget_reinit_and_double_settlement(self):
        path=self.d/'ledger.jsonl'; b=BudgetLedger(path,'0.01',RATES)
        rid,_=b.reserve(10,10,'x');self.assertEqual(b.settle(rid,5,3),34)
        with self.assertRaises(ExperimentError):b.settle(rid,5,3)
        self.assertEqual(BudgetLedger(path,'10',RATES).snapshot()['limit_micro_cny'],10000)
        with self.assertRaises(ExperimentError):BudgetLedger(path,'10',{**RATES,'input_cny_per_million':'1'})
    def test_response_failure_cache_and_cost(self):
        b=BudgetLedger(self.d/'ledger.jsonl','10',RATES); invoked=[]
        def transport(payload):
            invoked.append(True)
            return {'model':'mock','usage':{'prompt_tokens':10,'completion_tokens':20},'choices':[]}
        client=APIClient(CREDS,SETTINGS,b,self.d/'requests',True,transport)
        with self.assertRaises(ProviderFailure):client.complete([{'role':'user','content':'test'}],'ctx')
        with self.assertRaises(IncompleteRequest):client.complete([{'role':'user','content':'test'}],'ctx')
        self.assertEqual(len(invoked),1);self.assertEqual(b.snapshot()['spent_or_reserved_micro_cny'],610)
    def test_no_usage_retains_reserved_even_after_restart(self):
        path=self.d/'ledger.jsonl';b=BudgetLedger(path,'10',RATES)
        client=APIClient(CREDS,SETTINGS,b,self.d/'requests',True,lambda _: {'model':'mock','choices':[]})
        messages=[{'role':'user','content':'test'}]
        with self.assertRaises(ProviderFailure):client.complete(messages,'ctx')
        expected=430+2*(len(canonical(messages).encode())+512)+8*768
        self.assertEqual(BudgetLedger(path,'10',RATES).snapshot()['spent_or_reserved_micro_cny'],expected)
    def test_partial_agent_failure_preserves_trace(self):
        def call(messages,step):
            if step:return {'content':'broken json','request_id':'second'}
            return {'content':json.dumps({'action':'inspect','reason':'Inspect structure.'}),'request_id':'first'}
        with self.assertRaises(InvalidAssessment) as error:
            evaluate_with_agent({'id':'x','instruction':'x','input':'','output':'y'},load_config(),call)
        self.assertEqual([x['action'] for x in error.exception.trace],['inspect'])
    def fixture(self):
        rows=[];ps=[]
        for i,(original,diagnostic) in enumerate([('keep','reject'),('review','keep'),('error','reject')]):
            for variant,d in [('unaltered',original),('synthetic_corruption',diagnostic)]:
                ident=f'{i}-{variant}';rows.append({'id':ident,'base_id':str(i),'variant':variant,'defect':None if variant=='unaltered' else 'empty'})
                a=copy.deepcopy(GOOD)
                if d=='review':a['scores']['correctness']=1
                if d=='reject':a['scores']['correctness']=0
                a['decision']=d
                ps.append({'id':ident,'method':'zero_shot','status':'error' if d=='error' else 'success','assessment':None if d=='error' else a,'latency_seconds':len(ps)+1,'trace':[],'calls':1,'usage':{'prompt_tokens':2,'completion_tokens':3},'cost_micro_cny':28})
        return rows,ps
    def test_analysis_oracle_counts_failures_pairs_thresholds(self):
        rows,ps=self.fixture();s=summarize(rows,ps,['zero_shot'])['methods']['zero_shot']
        self.assertEqual(s['original_decisions'],{'keep':1,'review':1,'reject':0,'failed':1})
        self.assertEqual(s['diagnostic_decisions'],{'keep':1,'review':0,'reject':2,'failed':0})
        self.assertEqual(s['paired_keep_original_reject_diagnostic'],1)
        self.assertEqual(s['pairs_n'],3);self.assertEqual(s['calls'],6)
        self.assertEqual(s['cost_micro_cny'],168);self.assertEqual(s['median_latency_seconds'],3.5)
        self.assertAlmostEqual(s['p95_latency_seconds'],5.75)
        self.assertEqual(s['threshold_sensitivity']['sum_at_least_7'],{'original_kept':2,'diagnostic_kept':1})
    def test_analysis_rejects_missing_duplicate_and_foreign_predictions(self):
        rows,ps=self.fixture()
        for bad in (ps[:-1],ps+[ps[0]],[{**ps[0],'id':'other'}]+ps[1:]):
            with self.assertRaises(ValueError):summarize(rows,bad,['zero_shot'])
    def test_env_duplicates_and_unmatched_quotes_fail(self):
        p=self.d/'mock.env'
        for text in ('DEEPSEEK_API_KEY=a\nDEEPSEEK_API_KEY=b\n','DEEPSEEK_API_KEY="unfinished\n'):
            p.write_text(text)
            with self.assertRaises(ExperimentError):parse_env(p)
if __name__=='__main__':unittest.main(verbosity=2)
