# HW02 — Task 3: LLMs as a Data Quality Evaluator

Status: **implementation, real experiments, analysis and English report completed;
independent technical verification and exact final-package review passed;
Ready for user upload**. The scaffold-only phase is historical. See [full plan](notes/plan-full.md),
[verified sources](notes/research-full.md), and [implementation handoff](notes/implementation-full.md).
The English report and exact final submission package have their own review gates.

## Completed experiment

The frozen held-out run evaluated64rows across five methods:320judgments,
318valid and2malformed-JSON failures retained honestly. Three prompt techniques
(zero-shot, few-shot, stepwise CoT), a feedback agent, and a no-feedback ablation
were implemented and run. The second development pilot passed40/40after the
first pilot exposed uppercase decisions and unused tools.

| Method | Original keep /32 | Diagnostic reject /32 | Paired /32 | Invalid /64 |
| --- | ---: | ---: | ---: | ---: |
| Zero-shot |25|27|20|0|
| Few-shot |27|25|21|0|
| Stepwise CoT |25|25|20|0|
| Agent |27|27|23|1|
| No feedback |27|27|22|1|

Originals are not gold-positive labels. No method kept a diagnostic. Actual
agent inspection counts18/17; both agents skipped three prompt-requested length
checks. Feedback did not improve aggregate decisions over the ablation.
See [verified summary](results/test-v1/summary.json),
[independent verification](notes/verification-full.md), and
[report evidence](notes/report-evidence.md). The separate Reviewer approved the
exact files in [final package review](notes/review-full.md). Upload the required
`submission/CSC5051_HW02_Task3_Report.pdf` and optional
`submission/CSC5051_HW02_Task3_Code.zip` to Blackboard yourself. Ready applies
to those reviewed bytes, not an upload or instructor approval.

Conservative cost: **CNY0.948306total**, including both pilots and prior hello;
held-out experiment CNY0.774406. This is a list-rate estimate, not an invoice.
No further paid runs are needed for this version. Full raw evidence stays local
in `local_artifacts/runs/` and `results/raw/`; five selected D' datasets are in
`data/selected/test-v1/`. These are model-selected candidates, not certified clean.

[Supplement instructions](report/SUPPLEMENT_README.md) provide dataset retrieval,
preparation, offline checks, paid opt-in, analysis and PDF rebuild commands.
The frozen config retains its pre-run pending status to preserve its fingerprint;
execution records, not that historical label, establish completion.

## Task and source requirements

[Assignment_2.pdf](requirement/Assignment_2.pdf), p. 1 §3 requires at least three
prompting techniques and agent/non-agent comparisons on the same evaluation
data/settings. Page 3 §3.3 asks for justified data-quality criteria and a filtered
D' from D. Page 4 §§4–5 requires a concise PDF report, prompts and rationale,
agent workflow, representative cases, results and analysis; code is optional.
Deadline: **2026-11-06 23:59 UTC+8**. English is the user's choice; the user uploads
to Blackboard after final package review.

The saved tutorial notebook is the course material: zero-based cells20–25 cover
zero-shot, few-shot and chain-of-thought prompting; other cells show API calls and
Tasks1/2. Its exact path is ignored because it contains a potential credential.
The original bytes are preserved and its cells are not executed. The exact
teacher Overleaf link is recorded in the research note; its downloaded template
is retained under `requirement/overleaf-template/`. Report authorship remains
separate from this core implementation.

## Structure

| Path | Purpose |
| --- | --- |
| `.env` | Ignored local API/provider/model/budget values; never commit |
| `.env.example` | Configuration field names only |
| `config/experiment.json` | Shared rubric, model parameters, verified price assumptions |
| `prompts/` | Zero-shot, few-shot, stepwise CoT and adaptive agent prompts |
| `src/main.py` | Offline checks/previews and explicit paid run command |
| `src/core.py`, `budget.py`, `client.py` | Strict parsing, redaction, persistent reservations, HTTPS requests |
| `src/agent.py`, `prompting.py`, `runner.py` | Adaptive actions, prompt construction, concurrent/resumable runs |
| `src/prepare_data.py`, `src/analyze.py` | Data preparation and cached-output analysis, authored by the coordinating agent |
| `tests/` | Synthetic offline behavioral tests; old scaffold test under `history/` |
| `data/`, `local_artifacts/`, `results/raw/` | Ignored local data, predictions and request/budget journals |
| `notes/`, `results/` | Role records and lightweight actual-run evidence |
| `report/` | English report work; not automatically a reviewed final submission |

## Environment and local commands

Python3.9+ standard library on Linux (file locks use `fcntl`); no package install
is required. The dataset-preparation script uses a deterministic recorded seed.
Model calls remain remotely nondeterministic even at temperature0.

From this hw02 directory:

```bash
python3 src/main.py check
python3 src/main.py preview --method zero_shot
python3 src/main.py preview --method few_shot
python3 src/main.py preview --method chain_of_thought
python3 src/main.py preview --method agent
python3 tests/offline_smoke.py
```

Check/preview do not read `.env` and make no API calls. Tests use synthetic
credentials and mock responses, with socket creation blocked. These checks do
not measure model quality or certify the final assignment.

For real experiments, the local `.env` needs `DEEPSEEK_API_KEY`,
`DEEPSEEK_BASE_URL`, `DEEPSEEK_MODEL`, and `EXPERIMENT_BUDGET_CNY`. Values are parsed
as data with optional matching quotes; no shell expansion, `source`, `eval` or
execution occurs. Keep the existing key local; never paste it into logs/reports.
The provider field names are historical: the current verified provider is
Volcengine Ark and the model is DeepSeek-V4.1-Flash-260910. HTTPS is mandatory and
redirects are rejected. No environment override changes the saved file silently.

The following command is an execution example; use the actual prepared split
and a new run directory. The coordinating agent records every actual command.

```bash
python3 src/main.py run --dataset data/processed/test.jsonl \
  --output local_artifacts/runs/test-v1 \
  --methods zero_shot few_shot chain_of_thought agent agent_no_feedback \
  --workers 3 --allow-paid
```

Input must be JSONL with unique nonempty string `id` and string
`instruction`, `input`, `output`. Only the three text fields enter model prompts.
The runner does not download datasets. Preparation/analysis command contracts
are documented in their own scripts and actual execution records.

## Methods, decisions and evaluation boundaries

All methods share four quality dimensions scored0/1/2/null. The deterministic
rule rejects if any dimension is0, keeps only if all are2, and reviews otherwise.
An output claiming an inconsistent decision fails validation. Few-shot examples
are hand-authored illustrations separate from evaluation data. CoT explicitly
asks for ordered criterion assessment and a concise final explanation. Provider
thinking is disabled equally for all conditions with `reasoning_effort=none`;
`max_completion_tokens=768` caps each response.

The adaptive agent chooses `finish`, `inspect`, or `reassess` with at most three
model calls. Its development-refined policy requires an inspection before a
final decision for empty output, output over120 words(or uncertain near-threshold
length), or apparent sentence/paragraph repetition. Other records may finish
immediately or be reassessed. After inspection it uses available observations,
or explicitly acknowledges withheld observations, without repeating the same
inspection. The inspect tool reports empty fields, lengths and repetition;
it sees no hidden quality labels. `agent_no_feedback` has the same prompt and
call limit, but tool observations are withheld. Actual action traces determine
whether tool use occurred and whether it helped; the implementation does not
assume a benefit. Invalid schema, unfinished agents, truncated responses and
network failures are not successful quality decisions.

The prepared input is English GPT-4 Alpaca at commit
`38b93b75a80b019cc3aad362ca6f5bb0c3908959`, stored in
`data/raw/alpaca_gpt4_data.json`. Its SHA-256 is
`0bd4f62585d494b794deb043ce0baddfec02f27696857c57c9c238d6eff35a18`.
The source has52,002 records. A deterministic eligibility filter selects40
distinct base records: development16 rows(8 unaltered+8 controlled corruptions),
test64 rows(32 unaltered+32 controlled corruptions), and an8-row development
pilot. The pilot is a subset of development, not a separate held-out test.
Split hashes, sampling seed20261028 and eligibility rules are pinned in
`config/experiment.json` and `data/processed/manifest.json`.
Unaltered source records are not human-certified clean examples.
Report corruption rejection and natural retention separately; retention alone
cannot establish quality improvement or downstream training gains. Keep
prompt development separate from the frozen test subset. Dataset licence,
source/version/SHA-256, preparation seed and actual split sizes are recorded by
the preparation step; data remain local and are not included in Git.

## Budget, logs and resume

The user ceiling is **10 CNY cumulative**, including an initial conservative
hello-call allowance of0.000430 CNY. `results/raw/budget.jsonl` is the append-only
project ledger, protected across processes by file locks. Each request reserves
its serialized message UTF8 byte count+512 input tokens plus the full completion
cap before sending. The verified peak rates are2 CNY/M input and8 CNY/M output;
cache/off-peak discounts are ignored. Recorded cost is an upper estimate from
published rates, not an invoice.

Valid usage settles the reservation. Timeout/unknown usage retains it; no
request is automatically retried. Exceeding any usage bound stops future
reservations and requires reconciliation. Lowering the env budget cannot raise
the ledger's original ceiling. Changing ledger rates/prior spend is rejected.

Each request has an immutable event journal under `results/raw/requests/` with
sanitized request/response, usage and timing. Successful cached responses can be
replayed without another charge. An interrupted/failed request cannot be silently
resent. Preserve its journal and reconcile deliberately. Run directories contain:

- `run.json`: frozen source/config/dataset fingerprints and settings.
- `predictions.jsonl`: one terminal entry per record/method, including status,
  assessment, timing, usage, cost estimate, calls and action trace.
- `sessions.jsonl`: completion counts and cumulative ledger snapshots.

Re-running the same command resumes missing predictions and leaves terminal
successes/failures intact. A changed source/config/dataset fingerprint requires a
new output directory; previous evidence is preserved. Resume is reconstruction
from cached calls, not an independent repeat of stochastic model inference.
Never delete the ledger/cache to retry. Raw records and filtered datasets remain
under ignored local paths; compact summaries and provenance can be tracked.

## Independent workflow and delivery

Implementer self-tests are not independent verification. A separate Verifier
checks frozen code/data/results, then the Report Writer uses real evidence for
the English report. A different Reviewer inspects the exact final PDF/package.
Historical scaffold records remain in `notes/implementation.md`,
`notes/verification.md`, `notes/review.md`; they do not approve the expanded code.
Only the eventual reviewed files belong in `submission/`.
