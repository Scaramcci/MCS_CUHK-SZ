# Report rewrite: filtering decisions, severity and cost

Report Writer: /root/implementer, also an author of the experiment implementation. This is a writing and typesetting handoff. The frozen experiment is unchanged. Completed: 2026-11-05T17:09:27.280243+08:00.

The four-page English report leads with the distinction between withholding an example from training and rejecting it outright. The same four-dimensional rule underlies the strict, relaxed and post-hoc comparisons. The missing-modal original explains why a higher retention or paired count alone cannot establish better quality; the store-closure repetition shows the distinct clarity scores recorded after visible vs withheld inspection observations.

| Report location | Evidence checked |
| --- | --- |
| Page 1: corpus, sample, rules; source 49960 | data/source.json, data/processed/manifest.json, src/prepare_data.py, config/experiment.json; actual original/diagnostic records and ten test assessments for that base |
| Page 2: three techniques, optional actions and ablation, pilot refinements, settings and abbreviated API | prompts/*.txt, src/prompting.py, agent.py, client.py; notes/implementation-full.md, dev-pilot-v1 and v2 evidence; original task PDF pp. 1, 3–4 |
| Page 3: all held-out outcomes, threshold sensitivity, source 39766 | results/test-v1/summary.json, test predictions, source pair; table rows generated directly from the summary |
| Page 4: three missed length triggers per condition; individual vs aggregate decision differences; latency, token counts and estimate | notes/verification-full.md, results/test-v1/summary.json, execution.json, notes/research-full.md. Peak-priced estimates are distinguished from provider billing. |

The AI assistance disclosure and English teacher-template format are retained. No API call or new experiment was needed. No submission file was modified by this writer. The prior report's approval does not cover this revision.

Validation: regenerated report/latex/results.tex twice and compared its bytes. Built with TeX Live pdflatex, BibTeX using the template style, and subsequent pdflatex passes. Earlier Python escaping in the renderer was corrected before compilation. Trial page breaks displaced tables and two references; the final layout organizes each topic on a single page. The final build has four letter-size pages, resolved citations and cross-references, and no overfull/underfull box messages. Rendered all four pages at 115 dpi with pdftoppm and inspected them visually. The build logs and final-page images remain in local_artifacts/report-v2/.

Frozen SHA-256 values:

- `report/latex/main.tex`: `8b67a258572c0a98f54b674ce05c306353781ff8e19c259f939c5d1b6111b757`
- `report/latex/cases.tex`: `38bab835bca1a91a6e2152a005430c1f3d883849add60695390011ea19983b72`
- `report/latex/results.tex`: `42904e56de14e6c6a1a141008acb57ccef8e6be1ce5a887c1a3d22af3300ca1c`
- `src/render_results.py`: `3e121b86e8bf14e02e47afa1e191d9580209024d3f60a6442bef942a75a3c1f4`
- `local_artifacts/report-v2/main.pdf`: `a5800ce906c87011afcb988d716b9dc7e816ba6c0f653dade8a7e6c45b369723`
- `results/test-v1/summary.json`: `04fa4a29eb8377d140a67d670df51e22d2c3ede65e9cfed2b56b188d5c31d281`
- `results/test-v1/execution.json`: `fb46b2285d38a5a5780bc0ad6a8de493b79be50b7416d9ef488435ef3e543a42`
- `local_artifacts/runs/test-v1/predictions.jsonl`: `6ed539add527c61eddf7f79d9f797c841115db982dd8fb884b24da459376127e`

Next: independent report/evidence check and review of the actual candidate package after assembly.

## Reviewer copy edit: API listing on page 2

The example now breaks before the temperature field, the token limit and the request arguments. Recompiled successfully (four pages); inspected the new rendering at local_artifacts/report-v2/reviewed-page-2.png and verified extracted code lines. These hashes supersede the corresponding entries above:

- `report/latex/main.tex`: `f2b444c87f86b95f785a32b8cb50684424376dcc5a5f4b1f8b41276e0477ef2f`
- `local_artifacts/report-v2/main.pdf`: `45a1ac2d6a7a8fa70408ab33c1cc1763fea0b3603d6c665630064cf4083a7be8`
