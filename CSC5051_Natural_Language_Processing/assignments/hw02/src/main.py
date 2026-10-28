"""Offline scaffold checks and prompt preview. No API client or env loading."""

import argparse
import json
from pathlib import Path
from string import Template
import sys

ROOT = Path(__file__).resolve().parents[1]
METHODS = ("zero_shot", "few_shot", "chain_of_thought")
OUTPUT_CONTRACT = (
    'Return one JSON object with keys "scores", "decision", and "reason". '
    '"scores" must contain instruction_following, correctness, '
    'relevance_completeness and clarity, each 0, 1, 2 or null. '
    '"decision" must be keep, reject or review using the rubric rule. '
    '"reason" is a concise explanation, not a claim of external verification.'
)
RECORD_SLOTS = json.dumps(
    {"instruction": "<INSTRUCTION>", "input": "<INPUT_OR_EMPTY_STRING>",
     "output": "<RESPONSE_TO_EVALUATE>"}, indent=2
)


def load_config():
    config = json.loads((ROOT / "config/experiment.json").read_text(encoding="utf-8"))
    if (config["status"] != "scaffold_only" or config["task"] != 3
            or config["methods"] != list(METHODS)):
        raise ValueError("unsupported scaffold configuration")
    return config


def preview(method, config):
    template = Template((ROOT / "prompts" / f"{method}.txt").read_text(encoding="utf-8"))
    return template.substitute(
        rubric="Shared draft rubric:\n" + json.dumps(config["rubric"], indent=2),
        output_contract=OUTPUT_CONTRACT, record=RECORD_SLOTS,
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="check local configuration and templates")
    p = commands.add_parser("preview", help="print a template, not a model response")
    p.add_argument("--method", choices=METHODS, required=True)
    commands.add_parser("run", help="unavailable: experiments are not implemented")
    args = parser.parse_args(argv)
    if args.command == "run":
        print("Unavailable: scaffold only; API execution and budget enforcement are not implemented.", file=sys.stderr)
        return 2
    try:
        config = load_config()
        if args.command == "preview":
            print("OFFLINE TEMPLATE PREVIEW — NOT A MODEL RESPONSE\n")
            print(preview(args.method, config))
        else:
            for method in METHODS:
                preview(method, config)
            print("Scaffold check passed: Task 3 configuration and three templates load.")
            print("No dataset required. .env is not read. No API call made.")
            print("Agent, experiments, evaluation and final report remain unimplemented.")
        return 0
    except (OSError, ValueError, KeyError, TypeError):
        # Do not interpolate file contents, config values or environment data.
        print("Scaffold check failed: inspect the local JSON configuration and prompt templates.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
