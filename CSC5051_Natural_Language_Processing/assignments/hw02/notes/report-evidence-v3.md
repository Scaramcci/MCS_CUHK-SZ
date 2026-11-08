# Restored figures: report v3

Report Writer: /root/implementer, 2026-11-05. The user requested both figures in the rewritten English narrative. This revision builds on v2 without changing the input data, predictions, three numerical tables, existing analysis, or case text.

**Figure 1 (page 2)** links the finish/inspect/reassess policy to what enters the next model call. The ordinary agent receives structural measurements, while the control gets a withholding message. src/agent.py defines the feedback messages and three-call limit; the held-out summary and notes/verification-full.md establish 18/64 vs 17/64 inspections, zero reassessments and no third calls. The dashed self-loop identifies the available but unused reassessment branch.

**Figure 2 (page 3)** plots the five sets of judgments on the same eight fourfold repeats. src/render_results.py reads per_defect.excessive_repetition from results/test-v1/summary.json and emits labelled stacks through results.tex. In reject/review/invalid order, the counts are 3/5/0, 1/7/0, 1/7/0, 3/4/1, and 3/4/1. No record was kept in any method. The source calls invalid outputs “failed”; the graph labels them “Invalid” since both cases were malformed final JSON. The generator checks each denominator and the absence of keeps. A separate readback matched all 15 generated segment values to the summary.

**Build and visual QA.** Ran python3 src/render_results.py, pdflatex, the template BibTeX style, and pdflatex passes in local_artifacts/report-v3/. Re-running the generator produced identical results.tex bytes. pdftotext located both figures and all three tables; the PDF has five letter-size pages. Rendered all pages with pdftoppm at 110 dpi, inspected the page overview and the two figures at reading size. Adjusted the dashed return path label and inspection box to avoid collision and hyphenation. Both figures consist of PDF vector paths and selectable text; pdfimages -list found no raster images. The final TeX log contains no undefined citations/references, overfull or underfull boxes. No API calls were made and no submission files were edited by the writer.

| Frozen input/output | SHA-256 |
| --- | --- |
| `results/test-v1/summary.json` | `04fa4a29eb8377d140a67d670df51e22d2c3ede65e9cfed2b56b188d5c31d281` |
| `src/render_results.py` | `cb6d4d764fe63fec5f8a6e8204f3186e7a40f30b5e8e4207d550bb945592b28d` |
| `report/latex/main.tex` | `36d331fd29294ef2538d49e8a09ae940291ca7b9b9f4245973a89a369fe684c8` |
| `report/latex/results.tex` | `064eaa32b11659f179b75fc8feba40e584a63133e1e991f0616595fbd1c8678a` |
| `report/latex/cases.tex` | `38bab835bca1a91a6e2152a005430c1f3d883849add60695390011ea19983b72` |
| `local_artifacts/report-v3/main.pdf` | `2198ddcf61d488a65cd9c16f241470db36ca73a0c2989a550d7920010094a484` |

Next: independent verification and review of the newly assembled submission candidate; v2 package approval is historical.
