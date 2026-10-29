"""Offline behavioral tests. All API responses and credentials here are synthetic."""

from concurrent.futures import ThreadPoolExecutor
import contextlib
import copy
import io
import json
from pathlib import Path
import socket
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from agent import evaluate_with_agent, structural_feedback
from budget import BudgetExceeded, BudgetLedger
from client import APIClient, IncompleteRequest, NoRedirect, ProviderFailure
from core import DIMENSIONS, ExperimentError, InvalidAssessment, parse_assessment, parse_env, read_jsonl
from main import load_config, main
from prompting import messages_for
from runner import evaluate
import runner

PRICING = {'input_cny_per_million': '2', 'output_cny_per_million': '8', 'prior_spend_cny_upper_bound': '0.000430'}
SETTINGS = {'temperature': 0, 'reasoning_effort': 'none', 'max_completion_tokens': 768, 'max_input_tokens_bound': 24000, 'timeout_seconds': 10, 'allowed_requested_model': 'synthetic-test-model', 'expected_returned_model': 'synthetic-test-model'}
CREDS = {'DEEPSEEK_API_KEY': 'synthetic-test-secret', 'DEEPSEEK_MODEL': 'synthetic-test-model', 'DEEPSEEK_BASE_URL': 'https://example.invalid/v3'}
ROW = {'id': 'record', 'instruction': 'Add two integers; output the number.', 'input': '2, 3', 'output': '5', 'hidden_label': 'NEVER_SEND_THIS'}
GOOD = {'scores': dict.fromkeys(DIMENSIONS, 2), 'decision': 'keep', 'reason': 'The sum and format match.'}


def provider(content=None, inp=50, out=60, finish='stop'):
    return {'model': 'synthetic-test-model', 'choices': [{'finish_reason': finish, 'message': {'content': content or json.dumps(GOOD)}}], 'usage': {'prompt_tokens': inp, 'completion_tokens': out}}


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.no_socket = patch.object(socket, 'socket', side_effect=AssertionError('No network in offline tests'))
        self.no_socket.start()

    def tearDown(self):
        self.no_socket.stop()
        self.temp.cleanup()

    def ledger(self, limit='10'):
        return BudgetLedger(self.root / 'ledger.jsonl', limit, PRICING)

    def client(self, transport):
        return APIClient(CREDS, SETTINGS, self.ledger(), self.root / 'requests', allow_paid=True, transport=transport)

    def test_env_is_inert_data(self):
        path = self.root / '.env'
        path.write_text('DEEPSEEK_API_KEY="$(touch MUST_NOT_EXIST)"\nEXPERIMENT_BUDGET_CNY=10\n')
        parsed = parse_env(path)
        self.assertEqual(parsed['DEEPSEEK_API_KEY'], '$(touch MUST_NOT_EXIST)')
        self.assertFalse((self.root / 'MUST_NOT_EXIST').exists())

    def test_schema_and_decision(self):
        self.assertEqual(parse_assessment(json.dumps(GOOD)), GOOD)
        for value in (True, '2', 3, -1, 0.5):
            bad = copy.deepcopy(GOOD)
            bad['scores']['clarity'] = value
            with self.assertRaises(InvalidAssessment):
                parse_assessment(json.dumps(bad))
        bad = copy.deepcopy(GOOD)
        bad['scores']['correctness'] = None
        with self.assertRaises(InvalidAssessment):
            parse_assessment(json.dumps(bad))
        bad['decision'] = 'review'
        self.assertEqual(parse_assessment(json.dumps(bad))['decision'], 'review')
        bad['scores']['correctness'] = 0
        bad['decision'] = 'Reject'
        with self.assertRaises(InvalidAssessment):
            parse_assessment(json.dumps(bad))
        bad['decision'] = 'reject'
        self.assertEqual(parse_assessment(json.dumps(bad))['decision'], 'reject')
        for text in ('```json\n' + json.dumps(GOOD) + '\n```', '{"scores":{},"scores":{}}', '{"x":NaN}'):
            with self.assertRaises(InvalidAssessment):
                parse_assessment(text)

    def test_invalid_budget_before_transport(self):
        for value in ('', '0', '-1', '11', 'NaN', 'Infinity', True):
            with self.assertRaises(ExperimentError):
                BudgetLedger(self.root / 'bad.jsonl', value, PRICING)

    def test_concurrent_reservations_respect_ceiling(self):
        ledger = self.ledger('0.020')
        def reserve(i):
            try:
                return ledger.reserve(1000, 768, str(i))[1]
            except BudgetExceeded:
                return 0
        with ThreadPoolExecutor(max_workers=8) as pool:
            amounts = list(pool.map(reserve, range(20)))
        self.assertLessEqual(sum(amounts) + 430, 20000)
        self.assertEqual(ledger.snapshot()['spent_or_reserved_micro_cny'], sum(amounts) + 430)
        self.assertEqual(sum(x > 0 for x in amounts), 2)

    def test_success_cache_prevents_duplicate_call(self):
        invoked = []
        def transport(payload):
            invoked.append(payload)
            return provider()
        client = self.client(transport)
        a = client.complete([{'role': 'user', 'content': 'test'}], {'id': 'same'})
        b = client.complete([{'role': 'user', 'content': 'test'}], {'id': 'same'})
        self.assertFalse(a['cached'])
        self.assertTrue(b['cached'])
        self.assertEqual(len(invoked), 1)
        self.assertEqual(client.ledger.snapshot()['spent_or_reserved_micro_cny'], 430 + 580)

    def test_timeout_keeps_reservation_and_refuses_retry(self):
        invoked = []
        def transport(_):
            invoked.append(True)
            raise TimeoutError(CREDS['DEEPSEEK_API_KEY'])
        client = self.client(transport)
        with self.assertRaises(ProviderFailure):
            client.complete([{'role': 'user', 'content': 'test'}], 'timeout')
        with self.assertRaises(IncompleteRequest):
            client.complete([{'role': 'user', 'content': 'test'}], 'timeout')
        self.assertEqual(len(invoked), 1)
        self.assertGreater(client.ledger.snapshot()['spent_or_reserved_micro_cny'], 430)
        combined = ''.join(p.read_text() for p in self.root.rglob('*.jsonl'))
        self.assertNotIn(CREDS['DEEPSEEK_API_KEY'], combined)

    def test_missing_usage_retains_reservation(self):
        response = provider()
        del response['usage']
        client = self.client(lambda _: response)
        with self.assertRaises(ProviderFailure):
            client.complete([{'role': 'user', 'content': 'test'}], 'unknown-charge')
        events = read_jsonl(self.root / 'ledger.jsonl')
        self.assertEqual([e['event'] for e in events], ['initialize', 'reserve'])

    def test_concurrent_duplicate_request_is_sent_once(self):
        invoked = []
        def transport(_):
            invoked.append(True)
            return provider()
        client = self.client(transport)
        with ThreadPoolExecutor(max_workers=4) as pool:
            answers = list(pool.map(lambda _: client.complete([{'role': 'user', 'content': 'same'}], 'same'), range(8)))
        self.assertEqual(len(invoked), 1)
        self.assertEqual(sum(not answer['cached'] for answer in answers), 1)

    def test_usage_excess_freezes_future_reservations(self):
        client = self.client(lambda _: provider(inp=10000))
        with self.assertRaises(BudgetExceeded):
            client.complete([{'role': 'user', 'content': 'test'}], 'too-many')
        with self.assertRaises(BudgetExceeded):
            client.ledger.reserve(100, 100, 'next')
        self.assertTrue(client.ledger.snapshot()['requires_reconciliation'])

    def test_model_drift_blocks_followup_calls(self):
        changed = provider()
        changed['model'] = 'unpriced-model'
        client = self.client(lambda _: changed)
        with self.assertRaises(BudgetExceeded):
            client.complete([{'role': 'user', 'content': 'test'}], 'changed-model')
        self.assertTrue(client.ledger.snapshot()['requires_reconciliation'])
        with self.assertRaises(ExperimentError):
            APIClient({**CREDS, 'DEEPSEEK_MODEL': 'other-request'}, SETTINGS, client.ledger, self.root / 'requests', allow_paid=True)

    def test_truncation_is_not_success_and_still_charged(self):
        client = self.client(lambda _: provider(finish='length'))
        result = evaluate(ROW, 'zero_shot', load_config(), client, 'test', threading.Event())
        self.assertEqual(result['status'], 'error')
        self.assertIsNone(result['assessment'])
        self.assertEqual(result['usage']['completion_tokens'], 60)
        self.assertEqual(result['cost_micro_cny'], 580)

    def test_invalid_json_is_not_success_and_still_charged(self):
        client = self.client(lambda _: provider(content='not JSON'))
        result = evaluate(ROW, 'zero_shot', load_config(), client, 'test', threading.Event())
        self.assertEqual(result['status'], 'invalid')
        self.assertEqual(result['cost_micro_cny'], 580)

    def test_response_secret_redacted_in_artifacts(self):
        client = self.client(lambda _: provider(content=CREDS['DEEPSEEK_API_KEY']))
        result = client.complete([{'role': 'user', 'content': 'test'}], 'secret')
        self.assertEqual(result['content'], '[REDACTED]')
        self.assertNotIn(CREDS['DEEPSEEK_API_KEY'], ''.join(p.read_text() for p in self.root.rglob('*.jsonl')))

    def test_no_labels_in_prompts_or_tools(self):
        config = load_config()
        for method in ('zero_shot', 'few_shot', 'chain_of_thought', 'agent'):
            self.assertNotIn('NEVER_SEND_THIS', json.dumps(messages_for(method, config, ROW)))
        self.assertNotIn('NEVER_SEND_THIS', json.dumps(structural_feedback(ROW)))

    def test_agent_observation_and_ablation(self):
        for feedback in (True, False):
            seen = []
            def call(messages, step):
                seen.append(copy.deepcopy(messages))
                content = {'action': 'inspect', 'reason': 'Check repetition.'} if step == 0 else {'action': 'finish', 'assessment': GOOD}
                return {'request_id': str(step), 'content': json.dumps(content)}
            assessment, trace = evaluate_with_agent(ROW, load_config(), call, feedback)
            self.assertEqual(assessment, GOOD)
            self.assertEqual([x['action'] for x in trace], ['inspect', 'finish'])
            self.assertEqual('character_counts' in seen[1][-1]['content'], feedback)
            self.assertEqual('withheld' in seen[1][-1]['content'], not feedback)

    def test_agent_three_call_limit_and_reassess_branch(self):
        calls = []
        def call(messages, step):
            calls.append(step)
            return {'request_id': str(step), 'content': json.dumps({'action': 'reassess', 'reason': 'Uncertain.'})}
        with self.assertRaises(InvalidAssessment) as error:
            evaluate_with_agent(ROW, load_config(), call)
        self.assertEqual(calls, [0, 1, 2])
        self.assertEqual(len(error.exception.trace), 3)

    def test_agent_immediate_finish(self):
        calls = []
        def call(messages, step):
            calls.append(step)
            return {'request_id': 'one', 'content': json.dumps({'action': 'finish', 'assessment': GOOD})}
        result, trace = evaluate_with_agent(ROW, load_config(), call)
        self.assertEqual(calls, [0])
        self.assertEqual(result['decision'], 'keep')

    def test_redirect_and_opt_in_rejected(self):
        with self.assertRaises(ProviderFailure):
            NoRedirect().redirect_request(None, None, 302, '', {}, 'https://other.invalid')
        with self.assertRaises(ExperimentError):
            APIClient(CREDS, SETTINGS, self.ledger(), self.root / 'requests')
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(['run', '--dataset', 'not-read', '--output', 'not-created']), 2)
        self.assertFalse((self.root / 'not-created').exists())

    def test_runner_resume_and_method_matrix(self):
        dataset = self.root / 'records.jsonl'
        dataset.write_text(json.dumps(ROW) + '\n')
        env = self.root / '.env'
        env.write_text('\n'.join(f'{k}={v}' for k, v in {**CREDS, 'EXPERIMENT_BUDGET_CNY': '10'}.items()))
        invoked = []
        def transport(payload):
            invoked.append(payload)
            if 'exactly one JSON action' in payload['messages'][1]['content']:
                action = {'action': 'inspect', 'reason': 'Check structure.'} if len(payload['messages']) == 2 else {'action': 'finish', 'assessment': GOOD}
                return provider(json.dumps(action))
            return provider()
        def factory(credentials, settings, ledger, cache_dir, allow_paid):
            return APIClient(credentials, {**settings, 'allowed_requested_model': 'synthetic-test-model', 'expected_returned_model': 'synthetic-test-model'}, ledger, cache_dir, allow_paid=allow_paid, transport=transport)
        output = self.root / 'local_artifacts/run'
        with patch.object(runner, 'ROOT', self.root), patch.object(runner, 'code_hashes', return_value={'synthetic': 'test'}), \
             patch.object(runner, 'APIClient', side_effect=factory), contextlib.redirect_stdout(io.StringIO()):
            first = runner.run(dataset, output, load_config()['methods'], load_config(), 3, True, env)
            second = runner.run(dataset, output, load_config()['methods'], load_config(), 3, True, env)
        self.assertEqual(first['statuses']['success'], 5)
        self.assertEqual(second['completed_predictions'], 5)
        self.assertEqual(len(invoked), 7)
        self.assertNotIn('NEVER_SEND_THIS', json.dumps(invoked))
        predictions = read_jsonl(output / 'predictions.jsonl')
        self.assertEqual(len({(r['id'], r['method']) for r in predictions}), 5)
        self.assertTrue(all(r['usage']['prompt_tokens'] > 0 for r in predictions))


if __name__ == '__main__':
    unittest.main(verbosity=2)
