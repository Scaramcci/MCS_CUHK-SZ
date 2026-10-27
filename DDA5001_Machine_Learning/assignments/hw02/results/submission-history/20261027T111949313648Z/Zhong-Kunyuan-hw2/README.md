# DDA5001 Homework 2 — Kunyuan Zhong

Student ID: 226040255.

## Contents
- DDA5001_HW2_answers.pdf: English answers, derivations, numerical checks,
  four optimizer-learning figures, results table, two heat maps, discussion
  and assistance disclosure.
- p2/: completed numerical algorithms, original fixed framework/runner/tests,
  and verify.py for the small gradient/update checks.
- p3/: completed numerical algorithms, original fixed framework/runner/tests,
  and verify.py for the small fitting/population-error checks.
- figures/: the six figures embedded in the PDF, including both P3 heat maps.
- requirements.txt: unchanged teacher package versions.
- requirements-frozen.txt: complete dependencies used for the actual runs.

## Run
Use Python 3.12 and a fresh virtual environment. From this extracted folder:

```bash
python -m venv .venv
# Activate .venv for your operating system before the following commands.
python -m pip install -r requirements-frozen.txt
python -m unittest discover -s p2 -v
python p2/verify.py
python p2/run.py
python -m unittest discover -s p3 -v
python p3/verify.py
python p3/run.py
```

Run P2 and P3 test discovery separately: both original directories contain
same-named modules, so they must not be flattened or combined into one module
search path. No dataset is required for either small verification script.

Digits is bundled with scikit-learn. The P2 runner downloads and caches the
original Dry Bean CSV automatically:
https://archive.ics.uci.edu/static/public/602/data.csv
SHA-256: c91a086bb4357e69409d23287ec22be1be9512145cead1d8ca988c918be38fcb
If the download is blocked, save that exact CSV as p2/data_cache/dry_bean.csv.
The framework verifies its checksum. Do not substitute another dataset version.
The runner also accepts --data-dir PATH and --output-dir PATH.

The P3 runner generates the fixed synthetic experiments using seed 666 and
1000 trials per cell and saves its results in p3/results by default. Rare large
errors are retained. Plot colors saturate at +/-0.25 only; underlying numbers
are neither clipped nor smoothed. Both original frameworks are unchanged.

Datasets, virtual environments, caches and raw trial archives are intentionally
excluded, as required by the assignment. The provided figures and report were
produced by actual runs with the fixed teacher settings; no test-set tuning was
performed. All 15 public tests, the small numerical checks and complete P2/P3
experiments were independently reproduced in a fresh offline environment.

AI-assisted implementation and writing are disclosed in the PDF. The AI case
currently identifies the genuine coordinating-agent/coding-agent exchanges;
it does not represent them as prompts authored by the student.
