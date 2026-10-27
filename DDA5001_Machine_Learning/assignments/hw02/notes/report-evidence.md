# Report evidence map

Report Writer/executor: coordinating Codex agent (/root), 2026-10-27.
Student identity/layout from hw01/report/main.tex; teacher requirements from
DDA5001_HW2.pdf p1-7. Full derivations and English prose are AI-assisted.
No independent reviewer claim is issued by this author.

| Report section | Exact evidence |
|---|---|
| P1 and P2a theory | teacher p1-3; written derivation and counterexamples in report/main.tex |
| P2 required numerical matrices | results/run-20261027/p2-checks.json; executable src/p2/verify.py |
| P2 figures and table | results/run-20261027/p2/*_history.csv, summary.csv, manifest.json and original PNGs |
| P2 interpretation | results/run-20261027/analysis.json (metrics at100, minima, late changes) |
| AI case | actual chat and notes/student-ai-conversation.md; genuine student prompt and numerical follow-up, English translations labelled, no invented prompts |
| P3 theory | teacher p5-7 and report/main.tex derivation with missing coefficient terms |
| P3 numerical checks | results/run-20261027/p3-checks.json; executable src/p3/verify.py |
| P3 grids and interpretation | results/run-20261027/p3/grid_means.npz, trial_values.npz, CSV, summary.json, manifest.json |
| Independent execution status | notes/verification.md, separate fresh environment and full reruns |
| PDF layout | results/report-build-{1,2,3,4,5,6,7}/; all twelve pages checked, updated AI and disclosure pages re-rendered |

Final product/source matches are checked separately by Reviewer on the actual
ZIP. Numerical source files have not changed since independent verification.
Compilation is XeLaTeX; report table-generation source is notes/build_report_evidence.py.
The original first-build layout was corrected and preserved in run logs.
Student own-word explanations and personal understanding are not inferred from
a generated report or an agent's technical checks.

Final student request for assisted decision wording is retained verbatim in
notes/student-ai-conversation.md and labelled in report/ai-case.tex.
Final submitted code-source hashes remain exactly the independently verified
ones. Candidate PDF SHA2561afba6eea2f64585c30d84577de357572970a767f78049e32c49c4d272d64d76.
Personal own-word review is still not claimed; no generated text is presented as
unaided student writing.
