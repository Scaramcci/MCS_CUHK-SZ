# HW06 preparation and handoff

Role / Executor: Planner, Solver, Report Writer / root Codex session, 2026-11-08 (Asia/Shanghai).
Scope: complete hw06 only, preserve originals and unrelated modifications; master branch, no upload/commit/push. Concise English mathematical-answer PDF and LaTeX follow hw05. No fabricated submission requirements or experiments.

## Inputs and requirements mapping

Read repository README/AGENTS, agents/README, course README, hw05 README/answers/preparation/review, and agents/planner.md, implementer.md, report-writer.md. Checked course, assignments, hw06 and requirements for AGENTS.md / AGENTS.override.md: none. hw06 initially had no README and only one requirements PDF. Entire seven-page original was extracted and every rendered page inspected. PDF skill used for rendering and delivery; anti-defensive-writing used for reader-facing prose. Research-software workflow skill was inspected but no research-software implementation is needed: this is theoretical homework with a small author arithmetic-check helper.

| Source | Required answer | Check |
| --- | --- | --- |
| p.1 / Probability 1 (i-iv) | Independent multinomial model, all fourth year, two first/two second year, highest/lowest composition; Laplace smoothing explicitly requested | Derive general N formula, enumerate all 70 compositions for direct probabilities and clearly assumed N=100 example; proof of extrema |
| p.2 / Probability 2 | Unprepared given correct answer | Bayes formula, exact 5/59 |
| p.3 / Prob3 | Classify visible bottom-row query (yes,yes,yes,yes) | Transcribe all 20 animal rows, empirical scores and posterior; optional add-one variant with Water domain size 3 |
| p.4 / Probability 4 | Estimate transition matrix | All 16 adjacent transitions; row normalization in S,C,R order |
| p.5 / Probability 5 | Probability of three consecutive sunny days, window may start any day | Two transitions, general starting marginal, stationary equations and numeric answer under explicit stationarity assumption |
| p.6 / Probability 6, tasks 1-3 | Factorization, all CPTs, P(Engine=bad,AirConditioner=Broken) | Aggregate 40 counts, normalize all CPTs, enumerate fitted joint; distinguish fitted probability 9/64 from empirical 6/40 |
| p.7 / Probability 7, task 1 and computations a-c (printed as task 3) | Factorization and three queries | Enumerate all 16 joint assignments; use complementary probabilities and marginalize fuel |

No deadline, page limit, mandatory language, filename, electronic submission format or AI-use restriction appears in the original. No additional course reading directly concerning these questions is available in the slides inventory; no external sources needed for the elementary probability derivations.

## Plan and decisions

1. Solver derives each answer and records assumptions directly in the answer source.
2. Writer produces four pages: Q1-2, Q3-4, Q5-6, Q7. Sources cited by original page number in each heading.
3. Author uses standard-library exact fractions, multinomial enumeration and network enumeration as self-check, then compiles and inspects all PDF pages.
4. Independent Reviewer reads original and exact final PDF/source, recomputes key results, checks all page images; only Reviewer writes notes/review.md. Separate numerical Verifier N/A: small exact finite probability calculations, no experimental/code deliverable; use repository simple handwritten-task workflow, with independent final mathematical review.
5. No submission package: electronic submission format unspecified; report/answers.pdf is the exact reference deliverable, as in hw05.

## Assumptions and source issues

- Q1: four independent draws; no finite population sampling model is specified. Laplace add-one needs the total sample count N, which is absent. Asked user for any instructor clarification; no clarification received as of author handoff. General formulas are complete without this information. N=100 is an explicit illustrative assumption, not a fact inferred from percentages. Extrema do not depend on N>0.
- Q3: inspect rendered bottom row, where Can Fly and Have Legs are visibly changed to yes. Hidden PDF text contains an older query and worked calculations under a white rectangle. Visible homework question governs. Recount the source animal table: non-mammals with legs=yes are 9, not the 10 appearing in the hidden example. Main calculation uses empirical probabilities, matching displayed training-table classification; optional add-one variant is labeled and uses smoothed priors.
- Q5: stationary answer is conditional on the stated assumption, with arbitrary-start formula also provided. It is a three-day window probability, not the probability of ever seeing a sunny run over an unspecified horizon.
- Q6: the graph implies marginal E/A independence; the table need not obey it exactly. Network inference uses learned CPTs, not raw empirical joint count.

## Execution and evidence

- Initial scratch arithmetic computed Q1/Q3/Q4 but failed when importing unavailable sympy. Replaced symbolic package dependency with direct rational stationary equations; final checker needs standard library only.
- An initial combined authoring command used a repository-relative path while running from hw06 and failed with FileNotFoundError; rerun with correct paths. A later self-check caught the Q3 non-mammal leg count error. Corrected all affected scores/posteriors before final compilation. Initial build and failed check output remain in results/20261108-answer-build/; it is not the final answer.
- Final evidence: results/20261108-final-answer-build/self-check-output.txt, compile-pass1.txt, compile-pass2.txt, render-stderr.txt, build-record.json. Final self-check and both compiles exit 0, four pages, no overfull boxes or compiler warnings. Poppler exits 0; fontconfig emits cache-permission diagnostics but all pages render.
- Author visually inspected all four final page images: readable formulas/tables, no clipping, overlaps, missing glyphs or broken pagination. Reviewer conclusions recorded separately. No independent conclusion is prefilled by the author.
- Final file/input hashes and environment are recorded in build-record.json. Relevant files are uncommitted; no Git tracking operations performed.

Next role: independent Reviewer, permitted write path notes/review.md only. Review exact report/answers.tex and report/answers.pdf; preserve source PDF and all artifacts. Any defect returns to author, followed by renewed review.
