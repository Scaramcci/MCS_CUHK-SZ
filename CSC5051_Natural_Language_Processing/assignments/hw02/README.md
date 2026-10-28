# HW02 — Task 3: LLMs as a Data Quality Evaluator

Status: **foundation scaffold only**. The local CLI loads configuration and
previews three starter prompt templates. Dataset filtering, API calls, evaluation,
agent execution, experimental results and the final report are not implemented.
See [implementation and self-check record](notes/implementation.md) for the
authored version. Independent verification/review records, when produced, live
in `notes/`; this README does not certify their outcomes.

## Requirements and sources

- [Teacher assignment](requirement/Assignment_2.pdf), p. 1 §3: compare at least
  three prompting techniques and non-agent/agent approaches on the same evaluation data.
- Same PDF, p. 3 §3.3: define and justify quality criteria; select a cleaner D'
  from D. English or Chinese GPT-4 Alpaca are suggested datasets.
- Same PDF, p. 4 §4–5: concise PDF report using the Overleaf template, with prompts,
  rationale, agent workflow, representative cases, real results and comparisons.
  Code is optional supplementary material. Deadline: 2026-11-06 23:59 UTC+8.
- User decisions (2026-10-28): Task 3, English report, scaffold now, API and
  spending limit later. User uploads to Blackboard.

The saved course notebook in `requirement/` is the tutorial material: zero-based
cells 20–25 introduce zero-shot, few-shot and chain-of-thought prompting. It
demonstrates API calls and Tasks 1/2, but does not supply a Task 3 pipeline.
Its bytes are preserved; its exact path is locally Git-ignored because it
contains a potential credential. It is not executed or copied into this scaffold.
The teacher's Overleaf template is still needed before the final report.

## Structure

| Path | Purpose |
| --- | --- |
| `.env` | Ignored local values for the future API client |
| `.env.example` | Blank configuration field reference |
| `config/experiment.json` | Common draft rubric, methods and provisional settings |
| `prompts/` | Three starter templates, adapted from notebook cells 20–25 |
| `src/main.py` | Offline check and template preview |
| `src/agent.py` | Explicitly unimplemented agent extension contract |
| `report/outline.md` | English planning outline; no claimed results |
| `notes/`, `results/` | Internal role records and actual offline check evidence |

The rubric, 0–2 scale, decision rule and seed are draft project choices, not
teacher mandates. Few-shot demonstrations are hand-authored illustrations,
not experimental data or model output. All templates share the same rubric and
output schema; `preview` prints unfilled record slots.

## Local setup and commands

Python 3.8+ and its standard library are sufficient. No package install is needed.
Run from this hw02 directory:

```bash
python3 src/main.py check
python3 src/main.py preview --method zero_shot
python3 src/main.py preview --method few_shot
python3 src/main.py preview --method chain_of_thought
```

These commands require neither a dataset nor an API key. `check` checks local
structure, not model quality or API connectivity. `python3 src/main.py run`
always exits with code 2: live execution is unavailable even with credentials
and a budget. Filling `.env` cannot enable experiments in this version.

Open the existing **`.env` in this directory** in your editor and fill
`DEEPSEEK_API_KEY`; also supply the intended `DEEPSEEK_BASE_URL` and
`DEEPSEEK_MODEL`. Leave unknown fields blank and tell the assistant your budget
when ready. `EXPERIMENT_BUDGET_CNY` is reserved for that agreed limit. The scaffold
does not read `.env` yet; it does not execute it as shell code or validate the
provider. Keep secret values local. Never replace an existing `.env` with the
example just to update configuration.

## Next phase

After API configuration and explicit spending authorization, implement the client
and budget controls, acquire/fingerprint the selected dataset and define a frozen
evaluation split. Candidate: English GPT-4 Alpaca; source URL/version/hash and
sample size are undecided. Expected local input path: `data/raw/alpaca.json`;
create it only when data is acquired. Data and raw outputs remain local under
ignored `data/` or `local_artifacts/`. No dataset is present or backed up here.

Define independently assessable quality labels and meaningful quality metrics;
use development data for prompt tuning and demonstrations, keeping held-out
evaluation data separate. Then implement and compare the three techniques and
a feedback-driven agent, retain real run evidence, and write the English report.
The current templates have not been validated experimentally.

Continue with separate Implementer, Verifier, Report Writer and Reviewer roles.
No final PDF or `submission/` package exists; final package review must inspect
the eventual exact files after implementation and reporting are complete.

Planning inputs: [plan](notes/plan.md), [source review and hashes](notes/research.md).
