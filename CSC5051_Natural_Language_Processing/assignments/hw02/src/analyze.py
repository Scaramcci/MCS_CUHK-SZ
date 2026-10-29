"""Recompute descriptive diagnostics from immutable completed API predictions.

Unaltered originals are NOT gold-positive labels. Synthetic diagnostic rejection
is deliberately not called natural-data accuracy. No network or credentials.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import statistics

from core import METHODS, read_jsonl, sha256_file, validate_assessment


def frozen(path, value):
    data = (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise ValueError('Preserve prior analysis; choose a new output directory')
    if not path.exists():
        path.write_bytes(data)


def percentile(values, fraction):
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lo = int(position)
    return ordered[lo] + (ordered[min(lo + 1, len(ordered) - 1)] - ordered[lo]) * (position - lo)


def summarize(dataset, predictions, methods):
    rows = {r['id']: r for r in dataset}
    if len(rows) != len(dataset):
        raise ValueError('Duplicate dataset ids')
    lookup = {(p['id'], p['method']): p for p in predictions}
    expected = {(i, m) for i in rows for m in methods}
    if len(lookup) != len(predictions) or set(lookup) != expected:
        raise ValueError('Incomplete, duplicate, or unexpected prediction matrix')
    for p in predictions:
        if p['status'] == 'success':
            validate_assessment(p['assessment'])
    def decision(p):
        return p['assessment']['decision'] if p['status'] == 'success' else 'failed'
    result = {}
    for method in methods:
        ps = [lookup[i, method] for i in rows]
        original = [p for p in ps if rows[p['id']]['variant'] == 'unaltered']
        diagnostics = [p for p in ps if rows[p['id']]['variant'] == 'synthetic_corruption']
        counts = lambda group: {d: sum(decision(p) == d for p in group) for d in ('keep', 'review', 'reject', 'failed')}
        pairs = {}
        for p in ps:
            row = rows[p['id']]
            pairs.setdefault(row['base_id'], {})[row['variant']] = p
        if any(set(pair) != {'unaltered', 'synthetic_corruption'} for pair in pairs.values()):
            raise ValueError('Each source must have exactly two variants')
        latencies = [p['latency_seconds'] for p in ps]
        actions = Counter(step['action'] for p in ps for step in p['trace'])
        defects = sorted({rows[p['id']]['defect'] for p in diagnostics})
        sensitivity = {}
        for name, threshold in [('strict_all_2', 8), ('sum_at_least_7', 7), ('all_at_least_1', 4)]:
            def retained(p):
                if p['status'] != 'success':
                    return False
                scores = list(p['assessment']['scores'].values())
                return all(v is not None and v >= 1 for v in scores) and sum(scores) >= threshold
            sensitivity[name] = {'original_kept': sum(retained(p) for p in original),
                'diagnostic_kept': sum(retained(p) for p in diagnostics)}
        result[method] = {
            'n': len(ps), 'statuses': dict(sorted(Counter(p['status'] for p in ps).items())),
            'original_n': len(original), 'original_decisions': counts(original),
            'diagnostic_n': len(diagnostics), 'diagnostic_decisions': counts(diagnostics),
            'paired_keep_original_reject_diagnostic': sum(decision(pair['unaltered']) == 'keep' and decision(pair['synthetic_corruption']) == 'reject' for pair in pairs.values()),
            'pairs_n': len(pairs),
            'per_defect': {d: counts([p for p in diagnostics if rows[p['id']]['defect'] == d]) for d in defects},
            'calls': sum(p['calls'] for p in ps),
            'prompt_tokens': sum(p['usage']['prompt_tokens'] for p in ps),
            'completion_tokens': sum(p['usage']['completion_tokens'] for p in ps),
            'cost_micro_cny': sum(p['cost_micro_cny'] for p in ps),
            'mean_latency_seconds': statistics.mean(latencies),
            'median_latency_seconds': statistics.median(latencies),
            'p95_latency_seconds': percentile(latencies, .95),
            'actions': dict(sorted(actions.items())),
            'records_inspected': sum(any(s['action'] == 'inspect' for s in p['trace']) for p in ps),
            'records_reassessed': sum(any(s['action'] == 'reassess' for s in p['trace']) for p in ps),
            'threshold_sensitivity': sensitivity,
        }
    differences = {}
    for left, right in [('zero_shot', 'few_shot'), ('zero_shot', 'chain_of_thought'), ('zero_shot', 'agent'), ('agent', 'agent_no_feedback')]:
        if left in methods and right in methods:
            changed = [i for i in rows if decision(lookup[i, left]) != decision(lookup[i, right])]
            differences[left + '_vs_' + right] = {'changed_n': len(changed), 'changed_ids': changed}
    return {'methods': result, 'decision_differences': differences,
        'interpretation': 'Descriptive synthetic diagnostic rejection and unaltered-original retention; no human gold labels, no natural-data accuracy or downstream gain estimate.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, required=True)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--cleaned-output', type=Path, required=True)
    args = parser.parse_args()
    # Data-derived outputs must remain local; summaries may be tracked.
    root = Path(__file__).resolve().parents[1]
    cleaned = args.cleaned_output.resolve()
    if not any((root / p).resolve() in cleaned.parents for p in ('data', 'local_artifacts')):
        raise ValueError('Cleaned datasets must stay under local data/ or local_artifacts/')
    run = json.loads((args.run / 'run.json').read_text())
    digest = sha256_file(args.dataset)
    if digest != run['dataset_sha256']:
        raise ValueError('Run and analysis datasets differ')
    dataset = read_jsonl(args.dataset)
    predictions = read_jsonl(args.run / 'predictions.jsonl')
    if any(p['dataset_sha256'] != digest or p['experiment_fingerprint'] != run['experiment_fingerprint'] for p in predictions):
        raise ValueError('Prediction provenance differs')
    result = summarize(dataset, predictions, run['methods'])
    result['provenance'] = {'dataset_sha256': digest, 'experiment_fingerprint': run['experiment_fingerprint'],
        'prediction_sha256': sha256_file(args.run / 'predictions.jsonl'), 'analysis_source_sha256': sha256_file(__file__)}
    frozen(args.output / 'summary.json', result)
    lookup = {r['id']: r for r in dataset}
    for method in run['methods']:
        retained = [p['id'] for p in predictions if p['method'] == method and p['status'] == 'success' and p['assessment']['decision'] == 'keep' and lookup[p['id']]['variant'] == 'unaltered']
        retained.sort()
        # D' contains only model-selected original triples, never diagnostic corruptions.
        selected = [{k: lookup[i][k] for k in ('instruction', 'input', 'output')} for i in retained]
        frozen(cleaned / (method + '.json'), selected)
        frozen(args.output / (method + '-selection.json'), {'method': method, 'ids': retained,
            'count': len(retained), 'sha256': sha256_file(cleaned / (method + '.json')),
            'status': 'Model-selected subset; not independently verified clean data.'})
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
