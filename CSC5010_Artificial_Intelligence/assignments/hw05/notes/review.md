# HW05 independent final review

Role / Executor: Reviewer / independent sub-agent `/root/hw05_reviewer`, 2026-10-28 (Asia/Shanghai).
Task directory: `CSC5010_Artificial_Intelligence/assignments/hw05`.
Independence: this reviewer did not write the answers or the author's self-check script and was not this round's Verifier. Only this review record was written; the answer source, PDF and teacher original were not modified.

## Inputs and checked version

Read root `AGENTS.md`, `README.md`, `agents/README.md`, `agents/reviewer.md`, course README, `notes/answer-preparation.md`, the complete answer source, final PDF and final build/self-check records. Explicit path checks found no course, assignments or hw05 `AGENTS.md` / `AGENTS.override.md`. The previous HW04 `report/main.tex` confirms the concise English A4 answer style. The requirements directory contains only the five-page teacher PDF. After the initial review, reread the newly added hw05 `README.md` and updated preparation record: their deliverable descriptions and final build-evidence pointers agree with the checked files. Rechecked both answer hashes; neither answer file changed.

All five teacher pages were read through text extraction and visual inspection of `/tmp/csc5010-hw05-source/page-1.png` through `page-5.png`. Formula images missing from text extraction were read from these images. Both final answer pages were visually inspected. Independently rerendered the exact final PDF using `pdftoppm -r 110 -png .../report/answers.pdf /tmp/hw05-independent-review-final`; the two PNG SHA-256 values exactly match the inspected `final-1.png` and `final-2.png` images. Thus the visual check covers the actual final file.

SHA-256 confirmed with `sha256sum`:

| File | SHA-256 |
| --- | --- |
| `requirements/PropLogicHomeWork2026.pdf` | `f9e73bbf008a46c623dea96c7bfcf930a1f20f58517ffc86eaed2291caf0fbda` |
| `report/answers.tex` | `ca7eaf2fa03ec9cca6e81791d26f9c31ff3f8a0af3b7a583ec2830cde5885729` |
| `report/answers.pdf` | `613645b0d40258cc174206900579c36e63095403e53c255207c6fd5090ccc344` |

## Critical issues

None within the reviewed handwritten-reference scope. No fabricated proof, numerical result, citation or submission claim was found. The teacher original is preserved.

## Major issues

None. The supplied source has an impossible proof request in A under the user's confirmed negation interpretation; the answer correctly explains falsity rather than silently changing the proposition.

## Minor issues

No unresolved deliverable defects. The initial internal evidence-pointer issue was corrected by the author and the updated preparation record was reread; final evidence now points to `results/20261028-final-answer-build/`, and the earlier build is clearly identified as historical.

D's source choice (a), “cannot ... in all cases”, is ambiguous: if read as “not in every case”, it also describes a contingent conjunction. The answer's explicit “some cases, but not all”, eight-row truth table and three listed models remove the mathematical ambiguity. Selecting the intended (b) is acceptable; this is a source-language caveat, not a wrong solution.

## Submission checklist

| Requirement / source | Deliverable and independent review | Status |
| --- | --- | --- |
| A, teacher p. 1: worded proof request | PDF p. 1 states the exact negated consequent and supplies `(a,b,c)=(T,F,T)`. I independently evaluated both premise clauses as true and the consequent as false. The positive resolution conclusion is correctly identified separately. A valid proof of the displayed statement cannot exist. | Pass, with source defect explicitly disclosed |
| B, teacher p. 1, second set marked “You prove this” | All six given clauses match the original, including `C2 = not p or r or s`. Each of seven displayed resolution steps has correct parents and pivot. `r` yields `not q`, `not p`; these force `not s`, while the first clause yields `s`. The empty clause follows soundly. Not using C2 is legitimate. Teacher pp. 2–3 concern the first worked example rather than additional assigned questions. | Pass |
| C, teacher p. 4, Exercise 58 | All five disjunctions match the original. `(p,q,r)=(T,T,F)` makes each true. The count 5 attains the upper bound 5, so it is maximal. | Pass |
| D arithmetic, teacher p. 5 | The stated real-number assumption is appropriate for ordinary arithmetic. The equations imply `2x=0`; the unique simultaneous solution is `x=y=z=0`, and the converse is checked. | Pass |
| D logic, teacher p. 5 | All eight assignments occur exactly once. I manually checked all three implication columns and the conjunction column. The exact models are `(F,T,T)`, `(F,F,T)`, `(F,F,F)`. The equivalence to `not A and (not B or C)` and the classification as satisfiable but not tautological are correct. | Pass |
| Final presentation | Exact 2-page PDF; A/B on p. 1, C/D on p. 2. All formulas, negations, subscripts, boxed results and complete tables are readable; no clipping, overlap, missing glyphs or broken pagination found. | Pass |
| Build and self-check provenance | `results/20261028-final-answer-build/build-record.json` records successful two-pass pdflatex, author's logic check and rendering. Compile logs contain no reported warnings/errors or overfull boxes. The self-check is explicitly labeled author self-check, not independent verification; checked answer hashes match this review. | Pass |
| Separate numerical/code Verifier | This is elementary symbolic logic and a handwritten-reference document, with no experimental or complex numerical deliverable. Independent mathematical/visual review has been performed here; a separate implementation-validation stage is not required by the repository's simple handwritten workflow. | N/A |
| Electronic submission archive / `submission/` | No teacher requirement for an electronic archive was found, and the user requests a reference to copy onto paper. No `submission/` directory exists. The exact reviewed reference deliverable is `report/answers.pdf`; internal notes/results are not school submission content. | N/A |
| Upload / school submission | No external submission action was authorized or performed. Ready concerns this exact reference version only. | N/A |

## Final readiness

**Ready** for the user to use the exact reviewed PDF as a handwritten-answer reference. There are no unresolved Critical or Major findings. A's falsity is necessarily part of the answer under the user's explicit clarification. The metadata corrections have been reviewed and the answer hashes remain unchanged. Any subsequent answer source/PDF change requires the affected review to be repeated. This is independent final review, not an assertion of teacher approval or actual submission.

Next role: root session may deliver the reviewed PDF to the user and emphasize A's confirmed false statement. No answer repair is required.
