"""Task 3 offline previews and explicitly authorized, budgeted API experiments."""

import argparse
import json
from pathlib import Path
import sys

from core import ROOT, METHODS, DIMENSIONS, ExperimentError
from prompting import render


def load_config(path=None):
    config = json.loads(Path(path or ROOT / 'config/experiment.json').read_text(encoding='utf-8'))
    if config['task'] != 3 or config['methods'] != list(METHODS):
        raise ExperimentError('Unsupported experiment configuration')
    if set(config['rubric']['dimensions']) != set(DIMENSIONS):
        raise ExperimentError('Rubric dimensions changed')
    if config['agent']['max_calls'] != 3:
        raise ExperimentError('This experiment requires a three-call agent bound')
    return config


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', help='JSON configuration path')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('check', help='offline configuration/template check, no env read')
    preview = commands.add_parser('preview', help='print an unfilled template, no model call')
    preview.add_argument('--method', choices=METHODS, required=True)
    execute = commands.add_parser('run', help='budgeted live inference, explicit opt-in required')
    execute.add_argument('--dataset', required=True, help='JSONL with id/instruction/input/output')
    execute.add_argument('--output', required=True, help='directory within local_artifacts/ or results/raw/')
    execute.add_argument('--methods', nargs='+', choices=METHODS, default=list(METHODS))
    execute.add_argument('--workers', type=int, default=3)
    execute.add_argument('--allow-paid', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.command == 'run' and not args.allow_paid:
            raise ExperimentError('Explicit --allow-paid is required')
        config = load_config(args.config)
        if args.command == 'preview':
            print('OFFLINE TEMPLATE PREVIEW — NOT A MODEL RESPONSE\n')
            method = 'agent' if args.method == 'agent_no_feedback' else args.method
            print(render(method, config))
            if args.method == 'agent_no_feedback':
                print('\nAblation: identical prompt/limit; inspect observations withheld by runtime.')
        elif args.command == 'check':
            for method in ('zero_shot', 'few_shot', 'chain_of_thought', 'agent'):
                render(method, config)
            print('Offline configuration/template check passed. No env read or API call.')
            print('Run tests/offline_smoke.py for mocked budget/parser/agent checks.')
        else:
            from runner import run
            summary = run(args.dataset, args.output, args.methods, config, args.workers, allow_paid=True)
            print(json.dumps(summary, sort_keys=True))
            return 0 if summary['statuses']['success'] == summary['completed_predictions'] else 1
        return 0
    except Exception as exc:
        # Never print external exception text, config contents or credential values.
        print(f'Operation failed ({type(exc).__name__}). Inspect configuration and local journals; no automatic retry.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
