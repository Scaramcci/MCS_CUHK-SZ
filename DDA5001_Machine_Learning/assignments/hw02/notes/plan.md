# HW2 implementation and delivery plan

Date: 2026-10-27. Planner/executor: coordinating Codex agent (/root).
Authorization: complete hw02 and prepare a submission package; work on master,
within hw02. No upload or Git commit/push. Initial HEAD:
b02d5732be2b1bc074217fb236ca882b594e432d; initial working tree clean.

## Research and current state
The original PDF (7 pages) and all nine text files from code_source(1).zip
were read. No hw02 README, requirements directory or lower-level AGENTS files
existed. Originals remain at their existing paths, unchanged. Teacher code was
copied to src. hw01/report/main.tex supplies layout and student identification
only; its README has stale status and is not evidence of teacher requirements.

- src/p2/algorithms.py:16,25,34,42,47,56: six unimplemented functions.
- src/p2/framework.py:24: fixed seed/split/optimizer constants; prepare_dataset
  removes duplicates and uses only training statistics. run.py supports explicit
  data and output directories without framework changes.
- src/p3/algorithms.py:11,27: two unimplemented numerical functions.
- src/p3/framework.py:27: 1000 trials/cell, fixed seed 666 and paired grids;
  raw errors retained, colors saturated only for display.
- Public tests already cover gradient finite differences, extreme logits,
  update points, nonmutation, batch fits, target tails and quadrature.

## Desired end state and scope
One English answer PDF, separated runnable p2/ and p3/ code, small verification
scripts, two P3 heat maps (also embedded in the PDF), README and pinned dependency
list in Zhong-Kunyuan-hw2.zip. No data, environments, caches, raw trial archives,
internal role notes or LaTeX build products in the package. No external prior-art
survey is necessary: all definitions and fixed methods are supplied by the PDF.
All results must be from actual runs. Mathematical explanations are AI-assisted
and require the student's own understanding and wording before submission.

## Requirement / evidence mapping
| PDF source | Requirement | Artifact / acceptance |
|---|---|---|
| p1-2, P1 (15) | VC dimension, test/population errors, explain each GD/softmax option | English PDF with all four subparts |
| p2-3, P2a (12) | cross entropy -> logits -> columns -> mean matrix gradient | four explicit derivation steps |
| p3-4, P2b1 (10) | six functions, stable loss, no mutation | algorithms.py; unchanged framework hashes |
| p4, P2b2 (6) | two 3x3 gradients, max difference; accelerated gradient points and updates | verify.py + JSON + report matrices |
| p4-5, P2b3 (6) | four six-curve figures, final 6-row table, three answers | actual fixed runs, histories, PDF |
| p5, P2b4 (6) | <=1 page real agent case, numerical follow-up and decision | actual prompt/reply record + one PDF page |
| p6, P3a-b (18) | design/normal equations; normalized coefficient error and density | PDF derivation for degrees 2 and 10 |
| p7, P3c (27) | two functions, checks with expected/computed values, 1000 trials/cell, two full grids, interpretation | tests, verify.py, manifests, plots, discussion |
| p1,p7 | exact final package and no data | independent Reviewer opens actual ZIP |

## Implementation approach
P2 gradient for X(n,d), Y(n,K), Theta(d,K):
G = X.T @ (softmax(X @ Theta)-Y)/n. For one sample,
dH/dq_j=-p_j/q_j, dH/dz_k=q_k-p_k, dH/dtheta_k=x(q_k-p_k).
Stable softmax uses row z-max(z); its common exponential factor cancels.
Stable CE uses log(sum(exp(z-max(z))))-(z-max(z))_true.
GD: theta-mu*G(theta). Momentum: theta-mu*G(theta)+beta*(theta-previous).
Nesterov: w=theta+(k-1)/(k+2)*(theta-previous); return w-mu*G(w).
P3: np.linalg.lstsq(A,y,rcond=None)[0]. Zero-pad both coefficient arrays
along degree axis, return sum((w-c)**2/(2*k+1),axis=0), without re-normalizing.

## Consecutive phases (authorized whole-task execution)
- [x] 1. Run public tests on teacher stubs and retain failing logs. Implement
  the formulas above only in algorithms.py; add small standalone verify.py files.
  Commands from src: ../.venv312/bin/python -m unittest discover -s p2 -v
  and the same with p3. Expect 7 and 8 tests respectively; assert finite gradient
  difference <1e-8, update checks <1e-14, noiseless fit <1e-11 and analytic vs
  quadrature <1e-10. Preserve exact actual counts, not assumed passes.
- [x] 2. Run numerical checks before full experiments. Use run_record.py to retain
  command, timestamps, code hashes, exit status, stdout/stderr and environment.
  Commands: python p2/run.py --data-dir ../data --output-dir ../results/<run>/p2
  and python p3/run.py --output-dir ../results/<run>/p3. Fixed settings unchanged.
- [x] 3. Independent Verifier (not implementation author) inspects code and
  reruns tests/checks and results from a separate working copy; write only
  results/verification and notes/verification.md. Reproduce at least the small
  checks in a fresh environment. Issues return to author; repeat affected checks.
- [x] 4. Write English report in report/main.tex using real evidence and an honest
  one-page AI case. Compile with xelatex twice, inspect every rendered page,
  fix clipping, missing glyphs, bad references and content gaps.
- [x] 5. Assemble exact submission, create manifest of all contents and hashes;
  a different independent Reviewer opens and checks actual ZIP and PDF.
  Fixes require rebuilding and renewed affected review. Update README with
  final result and evidence paths, leave originals and all local data intact.

## Verification strategy
Automated: public tests, explicit numerical verification, unchanged teacher
framework/run/test SHA256, fixed seed/manifests, six P2 metrics rows, all P3 grid
cells and all trials retained, no nested training-error violation, PDF compilation,
ZIP test and exact content/hash audit. Independent verification is separate from
implementer self-tests. Manual: agent visual page QA, independent report and
package review; student understanding/wording is not marked confirmed by agents.
No fabricated student prompt, bug, outcome, or personal review is permitted.

## Risks / handling
Network access may be required for pinned wheels and the exact official CSV;
verify SHA256, never substitute data. Ill-conditioned P3 fits can produce very
large genuine risks: retain them and report saturation limits. AI disclosure
must explicitly identify agent-to-agent exchanges and assistance beyond P2b.

## Actual progress and deviations (2026-10-27)
Phases 1-3 complete; author tests, coordinator required numerical checks and
full fixed experiments all ran. Independent Verifier reproduced all numeric
outputs and eight figures exactly in a fresh offline environment. See
notes/implementation.md, notes/verification.md and results/run-20261027/.
Python3.14 could not install pinned SciPy, so bundled Python3.12.14 was used
with exact pins; failed setup and external-PYTHONPATH freeze attempts retained.
System PYTHONPATH was removed for main and independent runs.

Phase4: English 12-page report compiled three times and every page visually
inspected by coordinator and independent Reviewer. No overfull boxes, missing
characters or unresolved references; one harmless underfull paragraph.
AI case is being replaced with a real student-agent exchange after independent
Reviewer identified that the agent-to-agent case did not establish the explicit
student interaction requirement. Student asked the actual Nesterov/k=3 question;
coordinator answered with actual numerical checks; numerical follow-up pending.
Phase5: initial 20-file candidate assembled and independently inspected. It is
not approved as unconditionally Ready because student-specific requirements
remain. Older candidates are archived before rebuilding. No upload performed.

### Student interaction update
The student asked the actual Nesterov/lookahead/k3 question and subsequently
brought back the actual2.78e-17 vs hypothetical0.0008 discrepancy in a focused
follow-up. These are incorporated, explicitly translated, in the one-page AI
case. The student's own final decision sentence is pending; no statement of
student authorship, calculations or personal wording review has been invented.
The initial ZIP was retained in results/submission-history before rebuilding.
Updated candidate SHA564aad7e46845ee22d3b6fcf5d74fee8e0dbc03813014c39415776d3b17348a4
is under independent re-review. All source functions remain frozen.

## Final artifact handoff (2026-10-27)
All five artifact-production phases have executed. Report is12pages, AIcase
is onepage. Builds6/7 and last assembly incorporate the actual student's final
request '你帮我写吧': decision rationale is explicitly AI-assisted at that
request, without inventing personal authorship/endorsement. The final candidate
contains20files; ZIP SHA256
16dda52687c9733e4e0091cd67d12ac137b6519e27dfa8a0cbbd2e40bf537fbb.
No numeric source or result changed after independent verification.
Final independent Reviewer audit completed and is recorded in notes/review.md; technical/artifact checks pass.
Phase completion means artifacts/actions completed, not a claim that the
student's own mathematical wording/understanding obligation is fulfilled.
Unconditional submission readiness is therefore not asserted; student must
personally review and express mathematical explanations in their own words.
No additional approval loop is needed for already authorized local packaging.

## User-requested final recheck disposition
User now reports '我看完了，没有问题' after the page-by-page review guidance.
Record this as a user-reported personal review, without inventing file edits,
rewriting, unaided authorship or independently proven understanding.
Fresh audit results/final-audit-20261027/: exact20-member ZIP matches disk and
verified source; all15public tests and both numerical scripts pass. Full prior
independent reproduction remains applicable to unchanged hashes. Independent
Reviewer reread all original requirements and current package, then issued
Ready — checked local package prepared for user submission in notes/review.md.
No required product fixes, no package modification, no upload. This current
disposition supersedes the earlier pending-personal-review handoff status.
