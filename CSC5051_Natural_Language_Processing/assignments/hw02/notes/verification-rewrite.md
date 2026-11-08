# Technical verification for the English report rewrite

**Verdict: the frozen implementation, recorded comparisons and five filtered datasets pass.** On 32 paired cases, all five methods rejected all 24 empty, substituted and instruction-echo responses. Repeated answers account for every diagnostic that was reviewed or produced invalid JSON. This shared finding and its method-level differences are supported by the raw responses.

**Verifier:** `/root/verifier` (independent of implementation and report authorship), 2026-11-05, Asia/Shanghai; repository `master` at `929bf8151d7e4472173f3433505c870d932a8a6d`. Scope: technical evidence for the rewrite. The Reviewer checks the revised PDF and exact submission files. No inference call or fee was incurred in this audit.

**Sources and acceptance.** I read the assignment PDF text on pp. 1–4, visually inspected the examples on pp. 2–3, confirmed the tutorial's three technique headings (zero-based cells 20/22/24), and compared the teacher template's ZIP and extracted sources byte-for-byte. The original PDF, notebook and template archive SHA-256 hashes remain `bf09fbc9f382a149804a7977a6cc63912efa93520c56d4c7fe7c51260e64aa5f`, `5a396a71600492e39974d51ee7a2e6c5bf020242896dd37db88fcae2310c26e9` and `44f988836ade08d4593780f4b99a46c55e93690e0ae3402d8f2e1aa2b02e48a0` respectively.

| Teacher source | Evidence for the report author and Reviewer |
| --- | --- |
| p. 1 §2 and §3: choose one task; refine and compare ≥3 tutorial/guide techniques on the same evaluation data; compare a conventional method with an agent and explain observations/decisions | Task 3; separate zero-shot, few-shot and stepwise CoT prompts, adaptive agent, withheld-feedback ablation. The identical 64 held-out record IDs occur exactly once for each method. Two 8-record development pilots produced 37/40 and 40/40 valid assessments across five methods; disclose that format and inspection instructions changed together. |
| p. 1 §3: specify model/settings and use appropriate measurements | Raw payloads use the same model endpoint, temperature 0, reasoning effort none and output cap 768; recorded returned model is DeepSeek-V4.1-Flash-260910. Outcomes include retention, diagnostic rejection, paired success, call count and latency. |
| p. 3 §3.3: define and justify quality criteria, select D′ from D | Four dimensions: instruction following, correctness, relevance/completeness and clarity. Any 0 rejects; all 2s keep; all other combinations go to review. Each of the five local D′ files contains the exact retained source triples; synthetic diagnostics are excluded. The report must explain why these dimensions and thresholds serve its filtering objective. |
| p. 4 §4: concise report using the linked Overleaf template; API code if applicable; prompts/rationale, agent, cases, results and comparisons | Template original is present. API request construction (`src/client.py`), frozen prompt/version evidence, real traces, two traceable cases below and tables are available. The Reviewer checks whether the report actually presents these elements in English (user preference). Insights and supplementary code are optional. Required delivery: PDF via Blackboard by 2026-11-06 23:59 UTC+8; user uploads. |
| p. 4 §5: design/refinement 25, clarity 25, results 25, analysis 25 | Two pilots, held-out matrix, component ablation, alternative thresholds computed from recorded scores and concrete cases support these criteria. The grading authority remains the instructor. The original-task bonus concerns tasks beyond 1–3; code quality bonus is discretionary and the total is capped at 100. |
| Other tasks, pp. 2–3 §§3.1/3.2/3.4 | Their task-specific data (including 100 items for Tasks 1/2), labels and response shuffling do not apply to Task 3. |

**Fresh replay.** From hw02 I executed the original independent audit's read-only reconciliation portion (below; exit 0). The command omits downstream file-writing/test steps to preserve the October evidence. The replay denies sockets and DNS; it reads the saved model outputs. I separately compared all 15 entries in the final verifier input manifest and the hashes of the current predictions/ledger with the archived manifest. The author is rewriting report files only.

```bash
python3 -B - <<'PY'
from pathlib import Path
p = Path('results/verification-full-20261028/final_audit.py').resolve()
program = p.read_text().split('# Re-run actual analysis CLI')[0]
exec(compile(program, str(p), 'exec'), {'__file__': str(p)})
PY
```

[Independent audit code](../results/verification-full-20261028/final_audit.py), [frozen hashes and prior evidence](../results/verification-full-20261028/final-run.json), [measured summary](../results/test-v1/summary.json). Experiment fingerprint `94c3955aea076ccdeccad0a6dae0caae85118d43872c9c2919e909bc68dc0f99`; prediction SHA-256 `6ed539add527c61eddf7f79d9f797c841115db982dd8fb884b24da459376127e`. The replay matched the five D′ files byte-for-byte, all scores/decisions/statuses/traces, usage, latency, summary metrics and all 439 journal-to-ledger entries. No new live run was needed.

| Method | Original kept / 32 | Diagnostic rejected / 32 | Both outcomes within pair / 32 | Repeated-output rejected / 8 | Invalid | Calls | Estimated CNY |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Zero-shot | 25 | 27 | 20 | 3 | 0 | 64 | 0.111110 |
| Few-shot | 27 | 25 | 21 | 1 | 0 | 64 | 0.130142 |
| Stepwise CoT | 25 | 25 | 20 | 1 | 0 | 64 | 0.118662 |
| Agent | 27 | 27 | 23 | 3 | 1 | 82 | 0.209812 |
| Withheld-feedback agent | 27 | 27 | 22 | 3 | 1 | 81 | 0.204680 |

**Cases and interpretation.** On `alpaca-39766-diagnostic`, the agent scored clarity 0 and rejected; all other methods scored clarity 1 and sent it to review. On `alpaca-49960-original`, zero-shot/CoT scored instruction following 0 and rejected; few-shot and both agent variants scored it 1 and sent it to review. The two agent variants requested 18 and 17 inspections and no reassessments. Both skipped the same three outputs above the prompted 120-word threshold. The one-pair difference is descriptive; the two variants chose different action paths. These constructed defects measure filtering behavior; originals have no human quality labels and no downstream model was trained.

**Failed checks / corrections.** No technical mismatch requires a fix. Two malformed model responses (agent on `39784-diagnostic`, ablation on `41377-diagnostic`) are preserved as failures: 318 valid of 320; 355 held-out calls at an estimated CNY 0.774406. With both pilots and the prior hello allowance the conservative cumulative estimate is CNY 0.948306. Keep both failures in denominators. Proceed to independent review of the rewritten report and submission package.
