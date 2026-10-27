"""Run the fixed HW2 Problem 2(b) experiment from any working directory."""

import argparse
from pathlib import Path

import algorithms
from framework import run_experiment


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=base / "data_cache")
    parser.add_argument("--output-dir", type=Path, default=base / "results")
    args = parser.parse_args()
    run_experiment(algorithms, args.data_dir, args.output_dir)
