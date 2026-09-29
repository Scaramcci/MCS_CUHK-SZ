# Independent Reviewer — DDA5001 HW1 candidate 2026-09-29

## Final named archive review

The exact candidate is `submission/Zhong-Kunyuan-hw1.zip`, SHA-256 `1e5ebf2b5b0dd236c277bb27a1f89c1814f3e0189538f48b0a37418453e249b6`. The filename follows the handout's last name-first name-hw1 pattern using the user-supplied spelling. Python `zipfile`/`unzip -t` confirmed 17 readable regular entries. Every internal path, byte count and SHA-256 matched `/tmp/dda5001-hw1-stage-manifest-v3.json`, and each member's bytes matched the corresponding current workspace file. The archive contains the final PDF, two `.py` files and the same baseline/verification numeric outputs and charts listed below; it contains no original teacher archive, input-data copy, screenshot, Markdown, log or cache.

The archived PDF is byte-identical to `report/DDA5001_HW1_answers.pdf`, SHA-256 `508ab4e00714192850e3261a8c7fb4fa70f58ce80de3950988a60702cbc07892`. Since v2, only the first-page identity line changed to `Kunyuan Zhong   Student ID: 226040255`; I extracted the text and rendered that page to check spelling, placement and absence of clipping. The six-page A4 count and the P3(e)/P5(e) one-page limits are unchanged. `report/build-final-20260929/pass10.exit_code.txt` records XeLaTeX exit 0; its output has no error, unresolved reference or overfull warning, and the built PDF hash matches the archived PDF. Code hashes remain `572425d0...` and `27636fe4...`, identical to the prior independent verification and v2 review. No content or package issue remains from this reviewer.

**Final readiness:** The exact named ZIP is independently reviewed and the candidate content is ready for the user's final decision. The student expressly reserved personal review and confirmation of the P1/P2/P4 English wording; I cannot substitute for that step, so overall status remains **Blocked on student review**, not an unconditional Ready. No Blackboard upload has occurred. Any further edit to the candidate requires review of the changed version.

## Revision review: candidate v2

The author revised only the PDF reproduction note and assembled `/tmp/dda5001-hw1-review-candidate-v2.zip` (SHA-256 `22eb681995e700f3a8859021fda8f36dea39cc8089fcc3fa9b3df2cb3a158b5f`). Revised PDF SHA-256 is `b41e25c4db92c5523b4ba82b63f544df5afc428f1c7df204f49046aa9e0cfe57`. `src/p3.py` and `src/p5.py` hashes remain unchanged, so the prior independent technical verification still applies. The archive has the same 17 members; `unzip -t` passed and every member matched the current workspace source/output/PDF bytes. The author’s XeLaTeX pass8 exit record is 0; the PDF remains six A4 pages. I rendered and visually checked revised page 4; the added text is legible and not clipped.

**Re-review finding:** The Major issue below is resolved for v2. Page 4 now explicitly identifies the four listed commands as actual working-checkout invocations, says the teacher inputs are intentionally outside the ZIP, and tells a reader to unpack the separately supplied `code_source.zip`, pass its `p3/data` path to `--data-dir`, and pass its `p5/train_data.mat` and `p5/test_data.mat` paths to `--train-data` and `--test-data` in a NumPy/SciPy/Matplotlib environment. It labels these extracted-layout directions as an unperformed reuse instruction. This makes the dependency and path requirement clear without claiming another run. The remainder of this review documents v1 evidence; v2 changes only that page and the archive/PDF hashes.

**Current readiness:** Content and 17-file payload are reviewed with no unresolved Critical or Major issues. The final named ZIP cannot be approved until exact surname/given-name spelling is supplied and the newly named ZIP itself is inspected. The student’s reserved P1/P2/P4 wording review is also outstanding. No Blackboard upload was done.


Role / executor: independent child agent `/root/review_hw1`. I did not write the P3/P5 code or answer report and am not the previous Verifier. Scope: teacher `requirements/DDA5001_HW1.pdf` pp. 1–9, root and role rules, current source/results, six-page answer PDF, and the exact `/tmp/dda5001-hw1-review-candidate.zip` archive. This is a read-only review of the candidate; I did not rerun experiments or modify the reviewed files. The student's exact name remains pending, so the temporary ZIP name is not the intended final filename.

## Input versions

- Git HEAD at review: `d5fb4d0`; task files remain untracked. The root Git status also shows pre-existing template changes outside this review scope; none was touched.
- Teacher PDF SHA-256 `77b4320e4bd3125a6b74dc8d17c7536b0b91b4a2bc1e47b983713e4fda1c6b35`; original code ZIP `78bfb004a231838ffd60e136afad13aba6f61437790673edd950020b77e8721a`.
- Reviewed answer PDF `c67b95c6aff458b4e88c18a9e539dfece6aea265510f59d837e8af69e2a7315e`.
- Reviewed `src/p3.py` `572425d021d603deaf553c136e26a999690043af529191991b022a2843ccf6ae`; `src/p5.py` `27636fe419d3c156b4157049d8916e3ed27e677e30bd2b5aef834b328e104065`.
- Candidate ZIP SHA-256 `b830ec8cece01efb256f4a414c440593646e3f06f365ea7108d7ff965c6cf898`; `unzip -t`/Python `ZipFile.testzip()` found no corrupt member. Each archive member's bytes matched its corresponding current workspace file. The PDF matched `report/DDA5001_HW1_answers.pdf`.

## Critical issues

None found in the examined candidate: no missing answer PDF or code, evidence of fabricated numeric output, private data, credentials, teacher original ZIP, screenshot, Markdown draft, or cache inside the 17-file archive. This does not imply a teacher grading decision.

## Major issues (initial candidate; resolved in v2)

1. **Archive runnability and reproduction paths required a decision/fix.** The package contains no P3 input arrays or P5 digit data. Both submitted programs default to paths next to themselves (`src/data`, `src/train_data.mat`, `src/test_data.mat`), so a marker extracting only this ZIP and running either baseline with no arguments will get missing-file errors. The PDF's actual baseline commands refer to the author's repository-specific `requirements/code_source/code_source/p3/data` and `results/input-conversion-20260929/*.npz`, neither of which is in the ZIP. The original teacher data could be separately available to the marker, but the current submission does not say where to place them or provide an archive-relative invocation. The teacher handout P3 p. 3 asks for completed code/numerical outputs, P3 p. 5 asks for a reproduction command, and Reviewer rules require checking immediate runnability. Preserve the truthful record of actual commands, then add a clear command for running extracted code with the separately supplied teacher data, or package equivalent input copies and adjust the command/path plan. Any change to PDF or ZIP needs renewed review.

## Minor issues

- The Python docstrings and comments retain starter wording such as `TODO 1` despite implemented functions. They are not incomplete executable code, but may look unfinished to a human marker. The PDF itself has no visible Draft/TODO/placeholder or NKU content.
- `README.md` in the homework directory still says work has not started. It is not packaged, so this does not affect the candidate.

## Requirement checklist

| Requirement / source | Evidence checked | Status |
| --- | --- | --- |
| English PDF covering P1–P5; handout pp. 1–9 | Six-page PDF text and visual inspection of every rendered page | Pass, subject to student's own P1/P2/P4 wording approval |
| P1 (a)–(c), P2 (a)–(b), P4 (a)–(e) | PDF pp. 1–3; algebra, dimensions, sign convention and final bound checked | Pass |
| P3 exact shifted Huber sum and gradient, baseline, scalar/finite-difference/mean comparison; handout pp. 3–5 | PDF pp. 1–2, `src/p3.py`, baseline/verification CSV/JSON and prior independent `notes/verification.md` | Pass for content; reproduction limitation above |
| P5 perceptron/pocket, 2000-update curves, final boundaries, toy and full trace; handout pp. 8–9 | PDF pp. 3–4, `src/p5.py`, actual CSV/PNG/JSON and prior independent verification | Pass for content; reproduction limitation above |
| AI cases, initial predictions and real result follow-ups, at most one page each; handout P3(e)/P5(e) | PDF pp. 5 and 6; case summaries agree with the four user follow-ups and replies in conversation; no screenshot-only quote inferred | Pass |
| Actual commands, seed, runtime and `.mat`→`.npz` explanation | Revised PDF p. 4; matches run/verification records, notes exact elementwise comparison and external teacher-data paths | Pass in v2 |
| Visual layout, figure/table labels, page limits | Six pages rendered and inspected; P3(e) p. 5 only, P5(e) p. 6 only; figures readable; no clipping seen | Pass |
| Final PDF compilation | `report/build-final-20260929/pass5.exit_code.txt` is 0; no compiler errors, unresolved references or overfull-box messages in pass5 output | Pass (record inspected, not independently recompiled) |
| Submitted `.py`, numerical outputs and charts | ZIP contains both `.py`, PDF, P3 verification and baseline outputs, P5 toy/full outputs and charts; 17 regular files, all bytes match workspace | Pass for presence/version |
| Archive naming `last name-first name-hw1.zip`; handout p. 1 | Temporary candidate name only; exact student spelling pending | Pending |
| Standalone or clearly documented code input path | Revised PDF p. 4 says to unpack the separately supplied teacher code ZIP and pass its data paths to the scripts; labels this as unperformed reuse guidance | Pass in v2 |
| Upload to Blackboard | No upload requested or done | N/A |

## ZIP internal checklist (17 files)

```
DDA5001_HW1_answers.pdf
src/p3.py
src/p5.py
results/p3-baseline-20260929/{regression_error.png,regression_history.csv,summary.json,theta_huber.npy,theta_ls.npy}
results/p3-verify-20260929/{gradient_verification.csv,huber_branches.csv,summary.json}
results/p5-audit-20260929/{summary.json,toy_trace.csv}
results/p5-baseline-20260929/{decision_boundaries.png,error_curves.png,summary.json,trajectory.csv}
```

## Numerical and version cross-check

The PDF's P3 final Huber estimation error 5.61872016 and least-squares error 59.51363648 match `results/p3-baseline-20260929/summary.json`; it cites 1001 history states. Its P5 final current train/test errors 0.04014380/0.07142857 and pocket 0.03235470/0.06451613 match `results/p5-baseline-20260929/summary.json`; the full trace has 2001 states. The toy trace has seven states and the stated `0.5 → 0.25 → 0.5` current behavior. Prior independent technical verification bound to unchanged code hashes reports that it replayed trajectories and checked the exact `.mat`/`.npz` equivalence. The source in the ZIP matches those verified hashes. P3/P5 case statements about the four follow-ups, no code change, strict training-only selection and test-error rises agree with the conversation available to this reviewer.

## Final readiness

**Blocked on final name and student review.** The v2 revision resolves the archive runnability/documentation issue and has no unresolved Critical/Major issue in the reviewed content. Exact surname/given-name spelling is still needed to create the required filename; P1, P2 and P4 wording awaits the student's expressly reserved personal review. The final named ZIP must be inspected as the actual candidate before Ready can be assigned. This review applies to the v2 hashes above and is not approval of an unseen final named ZIP.
