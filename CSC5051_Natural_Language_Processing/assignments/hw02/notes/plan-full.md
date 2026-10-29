# Full Task 3 implementation and experiment plan

Role / Executor: Planner `/root`; 2026-10-28, Asia/Shanghai.
Authorization: user requested the complete project after a successful real hello call; local configured budget is CNY 10. English report and separate independent Verifier/Reviewer remain required. This plan supersedes the scope restriction in historical [foundation plan](plan.md), whose original acceptance remains a historical scaffold check.

## Sources and research

Teacher requirements: Assignment_2.pdf p. 1 §3 (three prompting methods, agent comparison, same evaluation data/settings); p. 3 §3.3 (quality criteria, D to D'); p. 4 §§4–5 (concise English-by-user-choice PDF, template, cases, results, analysis; 2026-11-06 23:59 UTC+8). Course notebook zero-based cells20–25 supply zero/few/CoT techniques. Originals remain untouched. [Research](research-full.md) supplies verified dataset, pricing, API and template sources.

Use original English GPT-4 Alpaca at commit `38b93b75a80b019cc3aad362ca6f5bb0c3908959`, data/alpaca_gpt4_data.json. Record downloaded SHA-256, source commit/URL and retrieval date. Public data are CC BY-NC 4.0, for this noncommercial coursework. Data remain under ignored data/; raw API responses remain ignored results/raw/ or local_artifacts/.

## Design fixed before test runs

- Select 40 distinct eligible source records deterministically (seed20261028), with 8 development and 32 test originals. Eligibility bounds record length for affordable evaluation; document exact filter in metadata. Make one controlled corruption per original, balanced across four defect families: empty output, unrelated substituted response, instruction echo and excessive repetition. Development has16 records, test64. Exact manifests and split hashes are frozen before requests.
- Originals are *unaltered*, not gold-clean labels. Controlled corruptions are explicit synthetic diagnostics derived from actual source records. Labels never enter model prompts or tools. Report original retention, corruption rejection, paired discrimination and abstention separately, with no claim of human-ground-truth accuracy, natural-data quality improvement or downstream training improvement. Off-topic/echo/repetition labels are operational defects with limitations, not universal human judgments.
- All five methods run on identical test records: zero_shot, few_shot, chain_of_thought, adaptive agent, agent_no_feedback ablation. Shared four-dimension rubric and JSON schema; draft 0/1/2/null scores, keep all2, reject any0, review otherwise. Report threshold sensitivity by recomputing from recorded scores, clearly distinguishing post-hoc policy analysis from new model runs.
- Hand-authored few-shot examples are clearly labelled and independent of held-out test data. CoT explicitly requests criterion-wise assessment with a concise final explanation. Disable the provider's hidden reasoning via reasoning_effort=none for every condition so the comparison concerns the requested prompts/workflow.
- Adaptive agent chooses finish, inspect or reassess from observations; inspect provides structural checks only (length, repetition, lexical overlap, format), not oracle labels. Max3 model calls. No-feedback ablation uses the same prompt and call limit, withholds observations. Save decision/action/observation trace and measure actual branching; do not assume tool use or benefit.
- API endpoint/model are loaded from local env as data; actual returned model from hello was deepseek-v4-1-flash-260910. temperature0; explicit max_completion_tokens768; workers3. Provider version drift is recorded. Remote API nondeterminism remains even with temperature0.

## Budget and reliability

Reserve using documented worst-case peak prices: CNY2/M input and8/M output; no cache discount. Per-call upper input token allowance is UTF8 serialized-message bytes+512; output cap768. Cross-process file lock plus persistent ledger reserve before network, reconcile using usage, and retain reservation if billing is uncertain. Fail closed when projected cumulative cost exceeds user limit. Include prior hello conservative charge0.000430 CNY. Cost is an estimate from published rates, not the provider invoice.

No automatic retries. Resume from immutable cached responses/predictions; uncertain requests cannot be silently reissued. Never print/save API keys; reject redirects. Budget, parser and agent branch tests use mock responses. Paid pilot initially uses development data, then freeze experiment fingerprint and run test once. Any development-based revisions are recorded before test; test failures due to integration bugs are retained as failures and corrected runs distinguish versions.

## Staged implementation and ownership

1. Researcher verifies sources into notes/research-full.md (no API calls). Planner records this plan. Parent prepares src/prepare_data.py, src/analyze.py and data/metadata; Implementer owns core src modules except those two, tests, prompts, config, README and notes/implementation-full.md. Neither alters the other's files concurrently.
2. Implementer supplies CLI check, preview, run with explicit --allow-paid, persistent budget/cache, strict schema and error status, adaptive agent, ablation, exact run command and offline tests. Parent downloads fixed source and prepares split. No live run before core budget checks pass.
3. Parent executes a bounded development pilot, then the frozen test matrix; stores raw responses, prompts/settings/code hashes, timing, usage/cost and errors. Analyzer produces reproducible summary, cleaned original subset per method, case-index records and chart-ready tables. Cleaned datasets are local-only and distinguish model-selected from independently verified clean data.
4. Independent Verifier inspects frozen code, designs meaningful tests and reproduces parsing/statistics and data splits from cached outputs in a fresh stdlib environment. Verifier may run a very small extra live sample only if essential and specifically coordinated against the same ledger; cached-result reproduction is distinct from repeated stochastic API outputs. Failures return to author, then re-verification.
5. Report Writer (parent after reading role) writes concise English report using the teacher Overleaf template if accessible, includes dataset/limitations, prompts, adaptive traces, quantitative tables/plots, representative cases, ablation/threshold sensitivity and references. Each claim links to evidence in notes/report-evidence.md. A missing template cannot be silently called satisfied; produce the rest and explicitly request only that resource if retrieval fails.
6. Assemble the exact PDF and optional source-code supplement in submission only after verification and report QA. Exclude keys, caches, raw datasets and internal role notes from the supplement; retain local source/input reproducibility instructions. Independently recompute hashes and inspect exact package with a Reviewer distinct from Verifier and creators. Reviewer must view rendered PDF and actual archive manifest. User uploads Blackboard.

## Acceptance

Automated: meaningful unit/negative tests pass; raw and summary metrics agree; same record ids for five methods; dev/test base ids disjoint; corruption labels not prompt-visible; cost ledger within10CNY; original hashes unchanged; no secret in deliverables; data ignored. Derive outputs with recorded commands and source/config hashes. Captured experiment failures remain immutable.

Manual: three genuinely distinct prompt strategies; agent actions actually depend on observations with honest trace analysis; real data and synthetic diagnostics clearly separated; no unearned accuracy/quality/training claims; English report cites trustworthy sources; independent roles and exact final package review complete. Completion and Ready require evidence, not just successful script exit.

## Current dependencies

API works; key and budget configured. Dataset download and template retrieval are execution steps now. No full-assignment results existed at plan creation. The plan author may execute implementation/analysis/report tasks but cannot issue independent verification or review conclusions.

## Execution resolution (2026-10-28)

Dataset and exact Overleaf template downloaded and hashed. The implemented
inspection tool exposes empty fields, character/word counts and repetition
statistics; the earlier illustrative lexical-overlap/format list was not used
as an additional tool. Pilot-v1 had3uppercase-enum failures and no tool use.
Development-only prompt revisions made the lowercase contract explicit and
requested conditional inspect; pilot-v2 passed40/40 with real inspection.
Final held-out fingerprint94c3955aea076ccdeccad0a6dae0caae85118d43872c9c2919e909bc68dc0f99
produced318valid+2invalid outcomes from320predictions, with no retries/tuning on
test. Both agent variants missed3length-triggered checks; the report discloses
that the policy is prompt-instructed rather than enforced. Cumulative cost
estimate0.948306CNY. Independent Verifier passed code/evidence/statistics scope;
six-page English report and exact final package proceed to distinct Reviewer.
