# Independent review of the rewritten Task 3 report

**Ready for delivery.** The four-page English report explains a practical decision: a repeated answer can remain correct, yet receive either a rejection or a request for review. Its abstract gives the measured tradeoff up front. On the same 32 pairs, the single-call baseline rejected as many constructed defects as the inspection agent (27/32), cost less, and retained two fewer originals. The report shows both sides of that comparison and identifies where feedback changed an individual judgment.

Reviewer: `/root/reviewer`, 2026-11-05 (Asia/Shanghai), neither an author of the rewrite nor its technical Verifier. I read the updated user instructions, reviewer role, anti-defensive-writing and PDF guidance, [teacher assignment](../requirement/Assignment_2.pdf) and [fresh technical verification](verification-rewrite.md). I inspected the frozen candidate in `local_artifacts/rewrite-candidate/`. Approval follows these bytes when copied to `submission/`:

| File | SHA-256 |
| --- | --- |
| CSC5051_HW02_Task3_Report.pdf | `45a1ac2d6a7a8fa70408ab33c1cc1763fea0b3603d6c665630064cf4083a7be8` |
| CSC5051_HW02_Task3_Code.zip | `965269e435c5443e12933830e15cd220707f8ec28ea0ab8b38e64ef2d2c198e5` |

**Critical findings:** none. **Major findings:** none. **Minor findings:** none outstanding. The author rewrapped the API excerpt; the corrected page 2 now renders complete key/value pairs, and the other three final page renders match the inspected pages byte-for-byte. The revised ZIP changed only the report source and its manifest. All package checks were repeated on these final hashes.

| Requirement | Candidate check |
| --- | --- |
| PDF p. 1 §3: prompt techniques, refinement and fair comparison | Pass. Report p. 2 gives examples and rationale for zero-shot, few-shot and stepwise prompts, explains the two jointly revised pilot instructions, and gives shared model/settings. Each method has the same 64 records. |
| PDF p. 1 §3: agent, intermediate feedback and comparative evidence | Pass. Pages 2–4 trace an actual inspection, compare with withheld feedback, distinguish failed JSON from rejection, and disclose three missed triggers per agent condition. The conclusion treats the observed record-level difference as a severity judgment and recognizes the different action paths. |
| PDF p. 3 §3.3: quality criteria, D to D′ | Pass. Page 1 explains four dimensions and the acceptance rule. The 25–27 kept originals per method and zero admitted synthetic defects match the saved predictions and independently reproduced selected subsets. Original retention is not presented as gold-label accuracy. |
| PDF p. 4 §§4–5: prompts, API code, cases, results, analysis | Pass. The missing-modal case (49960) illustrates original-label ambiguity; the repetition case (39766) shows 272 words, distinct-word fraction 0.180 and maximum frequency 24, with actual clarity scores 0 versus 1. Both agree with the source triples and recorded assessments. Tables 1–3 match the verified summary, including threshold sensitivity, 318/320 valid judgments and CNY 0.774406 for 355 held-out calls. |
| English report, official template, visual quality | Pass. Rendered and viewed each actual PDF page. Rubric and modal case (p. 1), prompts/API code (p. 2), results and threshold tables (p. 3), cost table and references (p. 4) are readable. All four relevant packaged style/bibliography files match the original teacher template byte-for-byte. |
| Optional ZIP, integrity and offline reproducibility | Pass. Direct CRC, traversal/symlink, credential-pattern and allowlist checks on the archive; 39 payload files plus the embedded manifest, with matching sizes and hashes. Code, prompts, report sources and summaries match their workspace counterparts. The ZIP contains instructions for retrieving the pinned dataset, not raw datasets, real environment settings or internal review records. |
| Exact extracted ZIP execution | Pass. Ran configuration check, 19 offline tests, all five method previews, results generator, and pdflatex/BibTeX rebuild. Generated tables match the original bytes; rebuilt PDF text equals the complete submitted-candidate text. Both candidate hashes still match after examination. No API calls or real environment-file reads. |

The distinct Verifier replayed the model outputs, checked 439 journal entries and reproduced the five D′ files. This review checked the specific rewritten text, fresh renders and the actual ZIP. Commands, outputs, archive manifest and renders: `local_artifacts/review-rewrite-20261105-v2/` (`inspect_candidate.py`, `audit.json`, `page-1.png` through `page-4.png`). The user uploads the approved files to Blackboard.
