# Independent review: illustrated Task 3 report

**Ready for user upload.** Both figures accurately explain the filtering experiment. Figure 1 separates available agent actions from observed ones; Figure 2 shows why outright rejection and exclusion from training differ on repeated responses.

Reviewer: `/root/reviewer`, 2026-11-05 (Asia/Shanghai); independent of report authorship and technical verification. The actual frozen files reviewed in `local_artifacts/figures-candidate/` were:

| Deliverable | SHA-256 |
| --- | --- |
| CSC5051_HW02_Task3_Report.pdf | `2198ddcf61d488a65cd9c16f241470db36ca73a0c2989a550d7920010094a484` |
| CSC5051_HW02_Task3_Code.zip | `76a6aca391a3ed5a6aebbb7fad1321a719064fbe90515b2ef14299060d027524` |

**Critical / Major / Minor findings:** none outstanding. Approval applies to copies with these hashes. The user handles Blackboard upload.

| Check | Evidence |
| --- | --- |
| Figure 1, page 2 | Inspected arrows, labels, and caption against the packaged agent loop and saved traces. A decision can finish, inspect and receive structural statistics (or withheld feedback), or reassess without new evidence. Raw test traces contain 18/17 inspections across 64 records per agent condition and zero reassessments; the dashed unused branch and three-call limit are labeled accordingly. |
| Figure 2, page 3 | Independently counted the eight repeated-output rows in the raw held-out predictions for each method. Reject / review / invalid counts are 3/5/0 (zero-shot), 1/7/0 (few-shot), 1/7/0 (stepwise), 3/4/1 (agent), and 3/4/1 (withheld feedback). Every bar sums to eight; none was kept. Counts printed inside the bars, axis and legend match. |
| Narrative, evidence and assignment | Three original tables, cases 49960 and 39766, method rationale, pilot refinement, common settings, strict rubric, selected subsets, costs and limitations remain consistent with the [technical verification](verification-rewrite.md) and the [previous report review](review-rewrite.md). Teacher PDF p. 1 §3, p. 3 §3.3 and p. 4 §§4–5 requirements remain covered. |
| Page-level presentation | Rendered and viewed all five actual pages. The diagrams and their captions are contiguous, the API example and each table fit within the body, and the closing discussion and references share page 5. Both figures are drawn in TikZ; Poppler found no embedded raster images. |
| Exact ZIP and rebuild | All 39 payload hashes and sizes match the embedded manifest (40 archive members total); safe-path, template-style, credential-pattern and exclusion checks passed. Compared with the previous reviewed package, only the supplement README, report main source, results TeX and results renderer changed. Extracted code passed 19 offline tests, config check and five previews; rebuilding the figure/table source reproduced its bytes. The complete PDF rebuilt offline from that copy has identical extracted text to the supplied PDF. Both candidates retained their hashes. |

Local evidence: `local_artifacts/review-figures-20261105/audit.json` (commands, exit statuses, file hashes), `figure-check.json` (raw counts, actions, vector check), and five rendered pages. No model request, credential read, report edit or upload was performed by this Reviewer.
