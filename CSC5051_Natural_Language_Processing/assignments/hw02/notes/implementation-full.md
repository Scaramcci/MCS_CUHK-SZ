# Full Task 3 core implementation handoff

Role / executor: Implementer `/root/implementer`; 2026-10-28, Asia/Shanghai.
Input Git revision: `037368d345026e4fe5c3e1a53a31b9f931853f78`, `master`, with
existing unrelated uncommitted work preserved. This work supersedes the scaffold
execution restriction under the user's explicit full-project authorization.
Sources: [full plan](plan-full.md), [research](research-full.md), root/course rules,
`agents/implementer.md`, Assignment_2.pdf pp.1,3–4 and tutorial cells20–25.

Status: core implementation and **offline self-checks completed**; no real API
experiment was executed by this Implementer. Parent coordinates data, paid runs,
analysis and reporting. No independent verification/review conclusion is issued.

## Implemented behavior

- Standard-library code with inert `.env` parsing, strict JSON assessment schema,
  decision consistency checks, and model-field whitelisting. The model receives
  only instruction/input/output, never record ids or evaluation metadata.
- Three baseline templates share a rubric/output schema; few-shot demonstrations
  are hand-authored illustrative examples. CoT requests criterion-wise assessment
  before a concise final justification.
- Adaptive agent chooses finish/inspect/reassess, max3 model calls. Inspect
  exposes only observable structural statistics. The no-feedback ablation has
  the same prompt and limit, but withholds inspect observations. The real action
  distribution and effects remain to be measured, not presumed.
- HTTPS OpenAI-compatible client with redirects disabled, explicit paid opt-in,
  no automatic retries, temperature0, reasoning_effort none, completion cap768.
  Requested-model settings are bound to the nonsecret current `.env` model;
  returned model must match the canonical version verified by the parent's hello
  call. Drift stops future calls and is retained as a reconciliation anomaly.
- Cross-process locked append-only ledger in integer micro-CNY. Reserve input
  UTF8 serialized-message bytes+512 and the completion cap before sending.
  Rates2/8 CNY per million, no discounts; initial prior cost0.000430 CNY;
  configured project budget must be positive and <=10 CNY. Lowered budget cannot
  raise the original ceiling; changed rates/prior cost require reconciliation.
- Usage settles reservations; timeout/missing usage retains them. A usage/model
  anomaly freezes future reservations. Reported costs are estimates, not invoices;
  unexpected model drift requires review of the affected charge estimate.
- Immutable request event journals and cached valid provider responses; an
  incomplete or failed prior request cannot be silently reissued. Prediction
  resume skips terminal rows, including failures, and reconstructs missing rows
  from cached calls. Source/config/dataset changes require a new run directory.
- Max3 worker threads; run-directory lock prevents concurrent writers; each
  request has a separate lock. Global budget/cache are shared across runs.

Current source modules: `core.py`, `budget.py`, `client.py`, `prompting.py`,
`agent.py`, `runner.py`, `main.py`. Parent owns `prepare_data.py` and `analyze.py`.
README and `.env.example` now describe real-run opt-in rather than scaffold-only
behavior. The actual `.env` was not edited. Its model field was checked without
printing secret values. Historical scaffold tests were copied intact to
`tests/history/offline_smoke_scaffold.py.txt`; `tests/offline_smoke.py` now runs
the current offline suite. Historical results and original teacher files remain.

## Interfaces for the coordinating agent

Run from hw02:

```bash
python3 src/main.py check
python3 src/main.py preview --method zero_shot
python3 tests/offline_smoke.py
python3 src/main.py run --dataset data/processed/test.jsonl \
  --output local_artifacts/runs/test-v1 \
  --methods zero_shot few_shot chain_of_thought agent agent_no_feedback \
  --workers 3 --allow-paid
```

The paid command above is a usage example, not a command this role ran. Optional
`--config path.json` belongs before the subcommand. Input is JSONL with unique
nonempty string `id`, and string `instruction`, `input`, `output`; extra fields
are not model-visible. Outputs must be within `local_artifacts/` or `results/raw/`.

`predictions.jsonl` is append-only with id, method, status(success/invalid/error/
budget_exhausted), assessment/null, dataset_sha256, experiment_fingerprint,
latency_seconds(sum of request latencies), wall_seconds, usage(prompt_tokens/
completion_tokens), cost_micro_cny, cost_cny_upper_bound, calls, call_details and
trace. Each call retains request ID, usage, cost basis, model and finish metadata
when available. Failures with known usage remain charged; uncertainty retains
reserved cost. Invalid/truncated/error outputs must be excluded from successful
quality decisions. Keep them in failure denominators when reporting completion.

`run.json` records provenance; `sessions.jsonl` records completion/status counts
and cumulative ledger snapshot. Global state is `results/raw/budget.jsonl` and
`results/raw/requests/<request-hash>.jsonl`. Do not erase state to bypass a failed
request or release a possibly billed reservation. Re-running uses caches and is
not a fresh stochastic experiment. Exceptions and console output omit external
error text; saved JSON recursively redacts the configured key.

## Actual offline evidence

Evidence directory: [full-selfcheck-20261028T221727+0800](../results/full-selfcheck-20261028T221727+0800/).
`run.json` records exact commands, Python/platform and original-source hashes;
numbered stdout/stderr files preserve actual outputs. Tested runtime: Python3.14.7
on Linux; no third-party packages, GPU or network required.

- `python3 tests/offline_smoke.py`: exit0, **19 tests passed**.
- `python3 src/main.py check`: exit0.
- `preview --method` for each of five method IDs: exit0.
- `run --dataset not-read --output not-created` without paid opt-in: expected exit2.

Tests exercise concurrent budget reservations, duplicate-request locking,
retained timeout/missing-usage reservations, returned-model/usage-bound freezes,
inert env values, strict numerical/JSON schema, consistent decisions, redaction,
redirect rejection, metadata exclusion, valid/invalid/truncated outputs, agent
finish/inspect/reassess/bounded-stop branches, feedback suppression, five-method
runner output and resume without extra transport calls. Socket creation is
blocked; provider responses and test keys are synthetic. These test decisions
and synthetic counts are not experimental model results.

All executed full-core tests passed. An initial combined patch was rejected
because it attempted delete+add of the same path; no partial patch was applied,
and the edit was reapplied correctly. No experiment failure is hidden by this
implementation record.

## Version and handoff

Authored file hashes: [authored-files.json](../results/full-selfcheck-20261028T221727+0800/authored-files.json).
Runtime source/config/prompts are frozen for the parent to run the development
pilot, followed by the held-out experiment only after any development revisions
are separately recorded and frozen. Any repair changes fingerprints and requires
appropriate rechecks. Old scaffold verification applies only to its old version.

Pending: parent dataset preparation and source hashes; real API development
pilot and fixed test run; results analysis/filter outputs; independent Verifier;
English report with exact template; final package assembly and distinct Reviewer.
This handoff is not Ready approval and does not claim the assignment completed.

## Prepared-data configuration freeze — 2026-10-28 22:28 UTC+8

The parent prepared data/source.json and data/processed/manifest.json. This
Implementer read those metadata files and independently recomputed the raw source
and dev/pilot/test file hashes and row counts before updating only the dataset
configuration and related README text. Source commit is
`38b93b75a80b019cc3aad362ca6f5bb0c3908959`; source SHA-256 is
`0bd4f62585d494b794deb043ce0baddfec02f27696857c57c9c238d6eff35a18`.
Local source path: `data/raw/alpaca_gpt4_data.json`,52,002 records. Test has64 rows
(32 unaltered+32 diagnostic corruptions), development16 rows, pilot8 development
rows. Config now records actual provenance, eligibility, seed, split paths,
counts and hashes. No dataset or preparation/analysis script was edited.

This configuration change supersedes the earlier config hash for subsequent
paid runs; previous evidence remains unchanged. Experiment status remains
implemented_pending_experiments. The parent confirmed requested Ark endpoint
mapping to the expected canonical returned model, so the existing binding stands.

Checks rerun: `python3 src/main.py check` exit0 and
`python3 tests/offline_smoke.py` exit0(19 tests). New command evidence and frozen
runtime/source/config hashes are under
[full-datafreeze-20261028T222806+0800](../results/full-datafreeze-20261028T222806+0800/),
including `run.json` and `source-config-manifest.json`. No API calls were made.
Runtime source/config/prompts are again frozen for the parent's development pilot.

## Development-driven prompt refinement — 2026-10-28 22:33 UTC+8

Input evidence: `local_artifacts/runs/dev-pilot-v1/predictions.jsonl`, SHA-256
`d6c2abf25e9e7a28250de77cdc1e971bbfc9883601fb0824331622c1077f7606`.
This Implementer inspected only these development outputs and their referenced
request journals. Of40 predictions,37 were valid and3 were invalid CoT outputs;
all three used the nonconforming capitalized decision `Reject`. All16 agent and
ablation predictions chose finish on the first call, so that pilot did not
observe tool-feedback behavior. These are actual development observations,
not held-out test results; no test results informed this revision.

Changes: the shared output contract now explicitly enumerates lowercase JSON
strings `keep`, `review`, `reject` and disallows capitalized variants. The strict
parser was preserved; the regression test now verifies that `Reject` fails while
`reject` with a zero score succeeds. The agent prompt now requires a conditional
inspect action for empty output, output over120 words(or uncertain length near
that threshold), or apparent repeated sentences/paragraphs. Other records can
finish immediately or reassess. After inspection it must consume the available
observation(or acknowledge withholding), then finish/reassess within the same
three-call limit. It must not present estimates as observed measurements or
repeat the same inspection. The ablation uses exactly the same revised prompt.
The new policy remains model-directed and its actual compliance/benefit must be
measured in the next pilot; no claim of successful adaptive behavior is made yet.

Changed files are `src/prompting.py`, `prompts/agent.txt`, `tests/test_core.py`,
README and this appended note. No parser, dataset, budget or runtime code was
changed. Check exit0 and all19 offline tests pass. New preserved evidence:
[full-pilot-refinement-20261028T223313+0800](../results/full-pilot-refinement-20261028T223313+0800/),
including `development-evidence.json`, real command stdout/stderr, `run.json`, and
`source-config-manifest.json`. Previous pilot/results/manifests remain unchanged.
The revised runtime/prompt version is frozen for the parent's dev-pilot-v2.
No API calls were made by this role during the refinement.
