# Full report evidence and handoff

Role: Report Writer `/root`;2026-10-28. Creator of report and data/analysis
scripts, not independent Verifier or Reviewer. Input: frozen test fingerprint
94c3955aea076ccdeccad0a6dae0caae85118d43872c9c2919e909bc68dc0f99,
`notes/verification-full.md` final technical PASS, current teacher originals.

## Requirement coverage and evidence

| Claim/requirement | Source or measured evidence | Report location |
| --- | --- | --- |
| Task3, criteria and D to D' | Assignment_2.pdf p3§3.3; src/analyze.py; data/selected/test-v1 | §1,3,5 |
| >=3 techniques, same data/settings, agent feedback | PDF p1§3; tutorial cells20–25; prompts/, src/agent.py; frozen run.json | §2,3, AppendixA |
| Concise report, template, cases/results/API code | PDF p4§4–5; untouched requirement/overleaf-template/ | Six-page English PDF |
| Source52002, eligible25117; disjoint32/8bases | data/source.json, processed/manifest.json, prepare_data.py; independent reproduction | §1 |
| 320predictions318valid2invalid; method statistics | local_artifacts/runs/test-v1/predictions.jsonl; results/test-v1/summary.json; independent raw replay | §3 tables1–3, figure2 |
| Two pilots, format refinement and conditional inspection | results/dev-pilot-v1, dev-pilot-v2; notes/implementation-full.md; original journals | §2 |
| 18/17inspect, zero reassess,3missedtriggers each | actual traces; verifier live-audit files and verification-full.md | §3 |
| CNY0.948306total,0.774406test;355testcalls | results/raw/budget.jsonl;439 requestjournals; hello evidence; verifier reconciliation | §3 table2 |
| Case39766 feedback/withheld severitydifference | source row, diagnostic, all5assessments, exact272word/0.180147toolobservation | §4 case1 |
| Case49960 originalmodalconstraintdisagreement | source row and all5assessments; actual0vs1scores | §4 case2 |
| References and pricing | notes/research-full.md verified primary sources | Bibliography |

The report does not claim gold-label accuracy, improved natural-data quality,
human adjudication, statistical significance, downstream gains, or feedback
superiority. Policy compliance is explicitly imperfect and failures preserved.
The strict subsets contain only selected originals; no diagnostic was kept.
Two cases are post-hoc explanatory selections, not a representative frequency.

## Actual rendering checks

Teacher source read fully; exact style files copied into report/latex/, originals
untouched. New project created with create_latex_project and opened in Codex.
Built-in compile returned compiler unavailable (Tectonic bundle uncached and
network fetch failed), not a source success. Terminal TeX Live2025/Debian
pdflatex + BibTeX successfully produced the PDF. Initial terminal attempt used
an absent output directory; initial BibTeX attempt was blocked by its safe
parent-path output rule. Corrected working directories/search paths; final
compilation has no undefined references/citations or overfull-box warnings.

First visual check found a mostly empty seventh page and a crossing loop arrow.
Report Writer shortened the appendix, tightened reference spacing, repaired the
loop and title break. All six final pages were rendered and visually inspected;
tables, diagram, stacked plot and code remain readable, without overlap or clipping.
Exact final PDF/package hashes will be recorded during assembly. Superseded
renders and logs are under ignored local_artifacts/report-build/.

## Handoff

Report source: report/latex/. Results tables/plot generated offline by
src/render_results.py from the verified summary. Supplemental README lives at
report/SUPPLEMENT_README.md. Independent Reviewer must inspect the actual final
PDF and ZIP, source/manifest agreement, confidentiality, teacher coverage and
claim limits. This author record does not sign a Reviewer verdict.
