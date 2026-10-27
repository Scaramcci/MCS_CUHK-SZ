"""Run the fixed Problem 3 experiment after completing algorithms.py."""

import argparse
from pathlib import Path

from framework import run_experiment


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent/"results")
    args = parser.parse_args()
    run_experiment(args.output_dir)
