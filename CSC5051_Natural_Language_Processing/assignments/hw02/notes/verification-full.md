# Independent full-project technical verification

Role / executor: Verifier `/root/verifier`, 2026-10-28, Asia/Shanghai.
Independence: this agent authored neither the implementation, data preparation,
analysis, prompts nor report. Earlier scaffold verification covered a different
version and is not reused as full-project approval.

Final verdict: **PASS for the frozen implementation and recorded experiment/analysis
consistency, with the observed inference failures and policy-compliance limitations
below.** This is not human validation of data quality, a claim of model superiority,
or final report/submission-package approval.

Scope: independent offline verification followed by final held-out predictions,
raw journals, ledger, statistics and selected-data reconciliation.
No live API requests, secret-file reads, dependency installs or source edits.
Applied the research-workflow and implementation-validation skills in Direct mode;
repository role restrictions determine output paths and independent ownership.

Inputs: root/course rules and READMEs; `agents/verifier.md`; teacher PDF pp.1–4
and prior relevant-page inspection; `notes/plan-full.md`, `research-full.md`,
`implementation-full.md`; actual src, config, prompt and test files. No narrower
AGENTS/override files were found. Branch is `master`; unrelated changes preserved.

## Initial passed offline checks

Evidence: [offline-run.json](../results/verification-full-20261028/offline-run.json).
It contains exact arguments/cwd/exit codes, Python/platform, hashes of all 16
source/config/prompt/test files, original hashes, preparation comparison and
numbered captured stdout/stderr. The initial pre-check manifest is also retained.
A fresh standard-library-only venv was created with `python3 -m venv --without-pip`
under ignored `local_artifacts/verification-20261028/venv`; no packages installed.

Actual runner (from repository root):

```bash
CSC5051_Natural_Language_Processing/assignments/hw02/local_artifacts/verification-20261028/venv/bin/python -B CSC5051_Natural_Language_Processing/assignments/hw02/results/verification-full-20261028/run_checks.py
```

Exit 0. Ten subprocess commands passed: author's offline test suite (19 tests),
independent suite (10 tests), configuration check, five previews, paid opt-in
refusal (expected exit 2), and independent data preparation. The independent
suite also ran directly once before the retained combined run, exit 0.

Independent tests cover:

- All 256 combinations of four scores from 0/1/2/null, accepted rule and both
  incorrect alternatives for each combination.
- Metadata/id/label mutation leaves all four model prompt types and structural
  feedback byte-identical; model visibility is exactly the three text fields.
- Twelve concurrent processes share one ledger: exactly three 2,800-micro-CNY
  reservations fit the 10,000-micro-CNY ceiling including 430 prior spend.
- Ceiling persists across reopening, changed rates fail, duplicate settlement
  fails, missing usage retains the full bound after reopening.
- Known-usage malformed response stays charged and cannot silently retry.
- Agent retains the inspect trace when a later action is invalid.
- A hand-calculated six-row synthetic metric fixture verifies failures in
  denominators, pair discrimination, threshold sensitivity, totals, median and
  interpolated p95; incomplete/duplicate/foreign predictions are rejected.
- Duplicate env assignments and unterminated quoted values fail. Only synthetic
  credentials were used. Sockets and DNS were blocked during both test suites
  (independent suite explicitly blocks both; author suite blocks sockets).

Real source data were read locally, not printed. `prepare_data.py` regenerated
all dev/pilot/test JSONL and manifest bytes exactly into an isolated ignored
verification directory. Independently confirmed each unaltered triple equals its
raw source record, every corruption implements its declared transform, off-topic
outputs equal their indicated donor, development/test base ids are disjoint,
and pilot ids form a development subset. Original PDF, notebook and downloaded
source SHA-256 match the recorded fingerprints. No source/data original modified.

## Initial failed checks

None in completed offline checks. At that stage held-out results remained pending.

## Initial open checks / limitations (subsequently resolved below)

- Parent reports pilot-v1 had three strict-schema CoT failures and agent immediate
  finishes; the original run is retained. A development-only prompt revision and
  second pilot precede the held-out freeze. This report does not verify unreceived
  final results or assume prompt changes are successful.
- Pending: final source/config hash freeze, same 64 ids across all five methods,
  actual raw-response parsing and agent trace reconciliation, usage/cost/ledger
  totals, final analysis reproduction and model-selected D' provenance.
- Python compatibility executed only on the runtime in offline-run.json. No
  independent stochastic live rerun, human quality annotations or downstream
  training validation is claimed. Synthetic diagnostic success does not establish
  natural-data accuracy or training quality improvement.
- Report/PDF and exact final package require a different independent Reviewer.

The parent subsequently supplied the final experiment paths and fingerprint.
The completed offline evidence is retained unchanged; the final checks follow.


## Final frozen version and actual execution

Final experiment: `local_artifacts/runs/test-v1`.
Fingerprint: `94c3955aea076ccdeccad0a6dae0caae85118d43872c9c2919e909bc68dc0f99`.
Prediction SHA-256: `6ed539add527c61eddf7f79d9f797c841115db982dd8fb884b24da459376127e`.
Current runtime/prompt hashes and config exactly match run.json; its fingerprint
was independently recomputed. Exact checked source/test/analysis hashes, commands,
exit status, timestamp and runtime are in
[final-run.json](../results/verification-full-20261028/final-run.json).

Executed from repository root, exit 0:

```bash
CSC5051_Natural_Language_Processing/assignments/hw02/local_artifacts/verification-20261028/venv/bin/python -B CSC5051_Natural_Language_Processing/assignments/hw02/results/verification-full-20261028/final_audit.py
```

This audit reran all 19 author tests and 10 independent tests on the final prompts,
with separate `final-tests-*` logs. It replayed each frozen prediction through the
parser/workflow using raw cached content and intercepted socket/DNS, then computed
an independent metric oracle rather than relying solely on the author's analyzer.
No live request was sent. No final run was modified or retried.

## Final passed checks

- Exactly 320 unique terminal predictions: the same 64 record ids for each of
  five methods. Each method has 32 unaltered originals and 32 diagnostics,
  including eight per defect family. 318 valid successes and two invalid outputs.
- All 439 global raw journals consist of one request, provider response and saved
  response. Verified model identity, disabled-thinking setting, temperature,
  explicit completion cap, finish status, raw/result content, token counts,
  recorded latency, request fingerprint, input reservation bound and exact
  `2*input_tokens + 8*output_tokens` micro-CNY computation. Returned usage reports
  no positive reasoning tokens. Local clocks/usage are recorded API evidence;
  this does not independently certify provider billing or internal computation.
- Every raw request maps exactly once to a call in one of the two pilots or test.
  No duplicate request counting, unmatched journals or unsettled reservations.
  Every ledger event reconciles to the corresponding request and response.
  The highest observed spend plus outstanding reservations is 986,238 micro-CNY,
  below the 10,000,000 micro-CNY limit at every ledger event.
- All 320 held-out predictions replay with identical status, assessment, trace,
  call details, usage, cost and summed latency. Actual first-request record objects
  contain only instruction/input/output matching the dataset; hidden variants,
  source indices, ids and diagnostic labels are absent from model record fields.
  Agent follow-up message/observation histories also match the replay exactly.
- Independently recomputed all method counts, pair results, per-defect counts,
  costs/tokens/calls, means/medians/p95, action frequencies, threshold sensitivity
  and cross-method changed ids. All match `results/test-v1/summary.json`.
  Independent values are retained in
  [independent-statistics.json](../results/verification-full-20261028/independent-statistics.json).
- Independently selected only successful kept originals, sorted ids, and rebuilt
  their exact three-field JSON. The five D' files match byte-for-byte, along with
  selection ids/counts/hashes. They contain 25/27/25/27/27 selected originals for
  zero-shot/few-shot/CoT/agent/ablation respectively, and no synthetic corruption.
- Reran `src/analyze.py` using recorded raw predictions into isolated verification
  destinations. Every summary, selection metadata file and D' file matches the
  author's bytes. Exact CLI arguments and exit 0 are in final-run.json; stdout
  and stderr are preserved separately. This is cached-result reproduction,
  not an independent stochastic model repeat.
- Final metadata-only ignore checks confirm actual `.env`, source/prepared/selected
  data, raw run predictions and ledger are ignored; `.env.example` is trackable.
  PDF and notebook fingerprints still match their original hashes. Evidence:
  [final-ignore-originals.json](../results/verification-full-20261028/final-ignore-originals.json).

### Reconciled spending evidence

| Run | Predictions | Valid / invalid | Calls | Conservative micro-CNY |
| --- | ---: | ---: | ---: | ---: |
| dev-pilot-v1 | 40 | 37 / 3 | 40 | 77,926 |
| dev-pilot-v2 | 40 | 40 / 0 | 44 | 95,544 |
| held-out test-v1 | 320 | 318 / 2 | 355 | 774,406 |
| Prior hello allowance | N/A | N/A | outside this ledger's request journals | 430 |
| Total | 400 | 395 / 5 | 439 logged experiment calls | **948,306** |

Total CNY 0.948306 is the reconciled conservative usage-rate estimate, not a
provider invoice. No unsettled or anomalous reservation was found.

## Observed model failures and required reporting caveats

These are retained experimental outcomes, not hidden or repaired verification
failures:

- `agent` on `alpaca-39784-diagnostic` and `agent_no_feedback` on
  `alpaca-41377-diagnostic` produced invalid JSON after two calls each.
  Both remain `invalid` with no assessment, are billed in cost/call totals, and
  are counted as failed rather than correct rejections. Both concern repetition
  diagnostics. All 64 records remain in each method's denominator.
- Both agent variants skipped inspection for three outputs over 120 whitespace
  words: `alpaca-46458-diagnostic` (131), `alpaca-00459-original` (124), and
  `alpaca-05599-original` (123). Thus the prompt-instructed conditional inspection
  policy was not perfectly followed and is not a runtime-enforced invariant.
  This was reported to the author, who agreed to disclose it without rerunning.
- Observed test actions: agent 18 inspect / 63 finish; ablation 17 inspect /
  63 finish; neither selected reassess. The difference in inspection counts means
  this is an adaptive end-to-end ablation, not a comparison with perfectly matched
  action trajectories. Agent/ablation aggregate retention and diagnostic rejection
  tie; pair counts differ by one (23 versus 22). These observations do not prove
  a causal advantage or general superiority of feedback.
- Correctness scores are model judgments. Originals lack human quality gold
  labels, synthetic diagnostics cover selected constructed defects, the sample
  is small and length-filtered, and no downstream training effect was measured.
  D' means model-selected originals, not independently certified clean data.

## Required fixes, scope limits and next role

No implementation or evidence-consistency blocker found in the checked frozen
version. Report Writer must keep the caveats above and distinguish observed
synthetic rejection, original retention and failures. API stochastic behavior
was not independently repeated; only recorded responses were reproduced.

The English report, charts, PDF rendering, citation presentation, supplementary
archive and exact submission candidate are outside this technical pass and must
be inspected by a Reviewer distinct from this Verifier and the creators. A code,
prompt/config, data or result change invalidates the affected checks and needs
fresh verification. Parent report-only edits do not change this runtime freeze.

References: [full plan](plan-full.md), [full implementation](implementation-full.md),
[research sources](research-full.md), [assignment PDF](../requirement/Assignment_2.pdf).
