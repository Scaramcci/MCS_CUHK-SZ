# CSC5051 HW02 Task 3: reproducible code supplement

The required deliverable is the accompanying English PDF. This code supplement
is optional under Assignment_2.pdf p.4. It contains the actual experiment code,
prompts, frozen configuration, tests, compact results, and report source.
The user uploads the files to Blackboard; no automatic submission is performed.

## Results and limits

The frozen test-v1 run evaluated 64 records with five methods (320 judgments):
318 strict-valid and two malformed JSON outputs, retained as failures.
Zero-shot/few-shot/stepwise/agent/no-feedback selected25/27/25/27/27 of32
unaltered originals. None kept a constructed diagnostic. Originals are not
human gold positives, and the selected datasets are not certified clean.
The two agents missed three prompt-requested length checks each. Agent feedback
did not improve aggregate counts over the no-feedback ablation.

Test cost estimate: CNY0.774406; both pilots plus the prior hello call bring
the cumulative estimate to CNY0.948306, below the authorized10CNY ceiling.
This uses peak list rates2/8CNY per million input/output tokens, not an invoice.
See `results/test-v1/summary.json` and `execution.json` for the evidence summary.
The config's pending-experiment status is its immutable pre-run snapshot;
actual execution state is recorded in these separate results.

## Files and dependencies

- `src/`: data preparation, strict API client, budget ledger, adaptive agent,
  runner, offline analysis, and report-table/plot generation.
- `prompts/`, `config/`: exact final prompts and experiment settings.
- `tests/test_core.py`, `tests/offline_smoke.py`:19 offline tests; no credentials
  or external calls. Independent verification is recorded in the local project,
  outside this submission supplement.
- `results/`: compact summaries, selections (IDs/hashes, no source triples),
  and actual execution metadata. Original raw outputs remain local.
- `report/latex/`: English report source, generated tables, and teacher-derived
  style files. `src/render_results.py` recreates `results.tex` from summary JSON.
- `.env.example`: placeholders only. Never include the real `.env` in a package.

Core: Python3.9+ standard library on Linux (`fcntl` is required), actually
tested on Python3.14.7. No GPU or pip packages are needed. Report: TeX Live with
pdflatex, BibTeX, PGFPlots/TikZ, listings, booktabs, hyperref, and Times fonts;
tested with TeX Live2025/Debian. Bibliography and style files are included.

## Recover the source and deterministic split

Source: English GPT-4 Alpaca, original repository
https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM
at commit38b93b75a80b019cc3aad362ca6f5bb0c3908959.
The data licence is CC BY-NC4.0, for research/noncommercial use:
https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM/blob/main/DATA_LICENSE

From this supplement directory, with public Internet access:

```bash
mkdir -p data/raw
curl -fL 'https://raw.githubusercontent.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM/38b93b75a80b019cc3aad362ca6f5bb0c3908959/data/alpaca_gpt4_data.json' -o data/raw/alpaca_gpt4_data.json
python3 src/prepare_data.py
python3 src/main.py check
python3 tests/offline_smoke.py
```

The script rejects bytes whose SHA-256 differs from
`0bd4f62585d494b794deb043ce0baddfec02f27696857c57c9c238d6eff35a18`.
It deterministically creates `data/processed/{dev,pilot,test}.jsonl` and
`manifest.json`. Test SHA-256:
`5973af0e5ae8b2b4569171beb43281d2cc614547a69e204cf7c82dc555583dbf`.
It never silently overwrites a changed split. Sampling seed20261028; full
eligibility and diagnostic-generation rules are in `src/prepare_data.py`.

## Optional new paid execution

Create `.env` from `.env.example` and fill the key, HTTPS base URL, deployment
model ID and budget. The original endpoint was Volcengine Ark, returning
`deepseek-v4-1-flash-260910`; the config binds the allowed deployment and
expected returned model. If using a different account/model, explicitly change
these fields and verify applicable pricing; that is a different experiment.
Do not print credentials. This run is opt-in and billed by the provider.

```bash
python3 src/main.py run --dataset data/processed/test.jsonl \
  --output local_artifacts/runs/new-test \
  --methods zero_shot few_shot chain_of_thought agent agent_no_feedback \
  --workers 3 --allow-paid
python3 src/analyze.py --dataset data/processed/test.jsonl \
  --run local_artifacts/runs/new-test --output results/new-test \
  --cleaned-output data/selected/new-test
```

Any invalid/error prediction gives the runner a nonzero exit code even when
the complete matrix was saved. Inspect `sessions.jsonl`; do not erase failures.
There are no automatic retries. Preserve `results/raw/budget.jsonl` and request
journals across runs. Resume skips terminal outcomes and uses valid cached
responses; never reset the ledger to evade the budget. Its hard ceiling is10CNY
and its original prior allowance is0.000430CNY. Paid API outputs may change even
with temperature0; newly generated results are not the original run evidence.

The original project's full raw responses and predictions are intentionally
local-only, as required by repository data policy. With those local files,
the original deterministic analysis command is:

```bash
python3 src/analyze.py --dataset data/processed/test.jsonl \
  --run local_artifacts/runs/test-v1 --output results/test-v1 \
  --cleaned-output data/selected/test-v1
```

The independent verifier reproduced every summary and selected-data byte from
these local outputs. The distributable supplement alone contains no raw
responses, source dataset or selected triples; new API results cannot be used
to claim an exact reproduction of the original stochastic judgments.

## Rebuild the report without API access

```bash
python3 src/render_results.py
cd report/latex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The included compact test summary is sufficient for the report tables/plot.
Cases refer to source indices39766 and49960. The teacher template was retrieved
from https://www.overleaf.com/read/jpcrtgzjjdry#36db1a; source archive SHA-256
`44f988836ade08d4593780f4b99a46c55e93690e0ae3402d8f2e1aa2b02e48a0`.
Only a working copy was adapted. See the PDF for source citations, methods,
two development revisions, observed failures, and AI assistance disclosure.
