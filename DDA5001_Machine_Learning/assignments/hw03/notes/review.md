# Independent final review — HW3 candidate v1

Reviewer / executor: `/root/reviewer`, independent child agent, 2026-10-29 (Asia/Shanghai). I did not implement or write the submitted work and am not `/root/verifier`. Scope: read-only inspection of the actual submission ZIP, teacher originals, code, report, results and verification evidence; this review note is my only repository write. Temporary extraction/rendering used `/tmp/hw03-review`. Branch checked: `master`; uncommitted work and the user's replacement of the earlier incorrect HW1 materials were preserved.

**Technical candidate review: passed. Final readiness for direct school submission: Not ready, pending the student's personal review and own-word explanations required on teacher PDF p1.** There are no identified technical Critical/Major defects to return to the implementer. The personal requirement cannot be completed or certified by an agent, and disclosure alone does not fulfill it.

## Inputs and exact reviewed version

Read root README/AGENTS and role workflow, course/assignment README, `agents/reviewer.md`, notes/plan.md, notes/verification.md, notes/report-evidence.md, notes/ai-collaboration.md and notes/pre-run-prediction.md. No course/assignment AGENTS or override files were found. Read the teacher PDF's full seven pages as extracted text and rendered images, and inspected the original framework/dependency files and data correspondence inside `requirements/code_source(2).zip`. Applied the PDF skill for read-only extraction and page rendering.

Directly opened `submission/Zhong-Kunyuan-hw3.zip`, checked CRC integrity, extracted it, and inspected the extracted report and code. Did not substitute the report source or directory mirror for ZIP review. All 412 ZIP files match the mirror and every size/hash in `results/submission-manifests/candidate-v1.json`.

| Artifact | Reviewed size / SHA-256 |
|---|---|
| submission/Zhong-Kunyuan-hw3.zip | 4,859,722 bytes; `0c3f045094c287ab89adf8570c675882bfa1878fb3c691cb026ff485e9661f1e` |
| ZIP: DDA5001_HW3_answers.pdf | 1,036,991 bytes, 7 pages; `2fd2c5dfef236be3fe03d49c1800acdaf94ce7a6bc2617a1e87bf8bbed693189` |
| ZIP: p1/p1.py | `3f51f39fb81f42996a16a336714ea9120f8980ca1473772638ee4d05c4425442` |
| ZIP: p2/p2.py | `97405f76831d4338625a19333837eb611863e806ca39d1fabaff8e9f5694f93c` |
| ZIP: p3/p3.py | `0ad492caf80f85c8df91f0604130bab48168f7816d4c7fb56e825b96215099e1` |

The PDF matches report/main.pdf exactly. The three scripts match the independently verified source hashes. Every other internal hash is recorded in the candidate manifest, which was checked in full. The non-data inventory is exactly one answer PDF, README.md, three scripts, three original per-problem requirements.txt files and requirements-frozen.txt. The remaining 403 files are the two required P1 CSVs, 400 required ORL faces and one required MNIST split NPZ. All 403 match the original teacher ZIP byte-for-byte and are Git-ignored in the submission mirror. There are no MNIST image caches, environment files, model checkpoints, role notes, experiment logs or unrelated files in the ZIP. The largest member is the answer PDF, below 10 MiB. No credential-bearing or private material was observed in the inspected textual files; the face images are unchanged required teacher data.

## Critical issues

None found within the inspected artifact and evidence scope. The package is the intended candidate, contains all required code/PDF files, and the numerical claims have actual execution evidence. The collaboration record labels translations and agent-performed checks; it does not claim an invented student debugging exchange or fabricated student checks.

## Major issues / submission prerequisite

- **Student-owned requirement remains incomplete (teacher PDF p1, instructions).** The original requires the student to check generated code, understand and verify all submitted work, and write mathematical derivations/explanations in their own words. Report p7 explicitly states that the explanations are AI-assisted drafts and that the personal step has not yet occurred. Thus this candidate is a technically checked draft for the student's review, not an unconditionally approved direct upload. The student should review the derivations, code and interpretations and express explanations personally before submission. If this changes the PDF/package, preserve the candidate history, rebuild and review the changed candidate. This is not an implementation defect and must not be resolved by inventing an acknowledgement or merely deleting the disclosure.

No additional technical Major issue or scoring-point omission was found. No further experiment or code change is requested by this review.

## Minor issues

No outstanding required cosmetic fixes. All seven report pages were visually reviewed from the ZIP: figures are readable, equations and tables are intact, captions stay with their figures, numbering is consistent, and page 7's collaboration record occupies one page without overflow.

The workspace README initially still said implementation was ongoing and no package existed. This was reported to the coordinator and corrected by the coordinator during review; I reread the updated README. That internal documentation correction did not change the reviewed package. No author fixes to the report or code were made during this review.

## Submission checklist

| Requirement / teacher source | Actual candidate evidence | Status |
|---|---|---|
| English PDF and .py files in last name-first name-hw3.zip (p1) | Zhong-Kunyuan-hw3.zip contains one English PDF and p1/p2/p3 scripts; name format follows the established candidate identity | Pass |
| Personal understanding, code review and own-word explanations (p1) | Report p7 transparently states this remains the student's responsibility and is not claimed complete | Pending student action; prevents unconditional submission Ready |
| P1(a): regularized fit, 6 pts (pp2–3) | Report p1 derives gradient and all-coefficient penalty; code solves X.T X + m lambda I; independent scaling/intercept tests | Pass |
| P1(a): five-fold scoring/choice, 8 pts (p3) | Correct original row-ID folds, 16 ascending candidates, 80 held-out errors, mean scoring, exact tie policy; test data excluded | Pass |
| P1(a): selected lambda and log-x validation plot, 4 pts (p3) | Report p1, Figure 1; lambda 0.01 and CV MSE 0.04826737 | Pass |
| P1(b): four-way plot and prescribed bounds, 4 pts (p3) | Report p2, Figure 2; x [-1.5,1.5], y [-0.5,2.5] | Pass |
| P1(b): both train/test MSEs, 4 pts (p3) | Report p2 table matches actual summary.json rounding | Pass |
| P1(b): 2–3 sentence tradeoff/test-selection discussion, 4 pts (p3) | Three-sentence paragraph on report p2 gives observed tradeoff and reserved test assessment | Pass for technical content; personal wording pending |
| P2(a): thin centered SVD and 16 ordered eigenfaces, 8 pts (pp4–5) | Report p3, Figure 3; X 10304x400, mu 10304x1, thin SVD, 4x4 PC1–16 grid | Pass |
| P2(b): correct original/k20/k100 5x3 grid, 6 pts (p5) | Report p4, Figure 4, image 1 of subjects 1–5; source indices 0/10/20/30/40 | Pass |
| P2(b): whole-dataset MSE, 3 pts (p5) | Report p4, 0.00734732 / 0.00271577; unclipped original reconstruction | Pass |
| P2(b): 2–3 sentence interpretation, 3 pts (p5) | Three-sentence paragraph distinguishes additional details, coordinate storage, and numerical/display clipping | Pass for technical content; personal wording pending |
| P3(a): prediction before run, 8 pts (p6) | Pre-run note hash recorded in actual run logs; report p5 explicitly attributes an AI-assisted pre-run prediction. Correct affine-collapse argument and ReLU comparison | Pass for recorded timing/technical content; no claim of independent student prediction |
| P3(b): agent-assisted A/B/C construction, 9 pts (p6) | Three exact constructors, biases, 784→10 and 784→64→10, ReLU between C's layers only, raw logits | Pass |
| P3(b): formula/dimension explanation, 5 pts (p6) | Report p5 maps layers, bias, activations, batch shapes, logits and parameter counts | Pass for technical content; personal wording pending |
| P3(c): two-panel train/validation CE figure, 6 pts (p7) | Report p6, Figure 5 includes A/B/C in both panels | Pass |
| P3(c): selected epochs/validation CE/test CE/test accuracy, 4 pts (p7) | Three-row report p6 table, A9/B4/C14, validation choice C | Pass |
| P3(c): A–B/B–C and prediction comparison, 4 pts (p7) | Report p6 makes matched nonlinearity comparison, avoids activation-only attribution for A–C, limits claims to fixed run | Pass for technical content; personal wording pending |
| P3(c): training–validation differences and last epoch, 4 pts (p7) | Actual selected/epoch30 CE table and run-specific overfitting discussion on p6 | Pass for technical content; personal wording pending |
| P3(d): at most one page actual construction interaction, 10 pts (p7) | Exactly report p7; actual broad user request/follow-up, labeled translated agent construction excerpt, tool/model, real checks and keep decision; no invented bug/student follow-up | Pass for record coverage; student personal-check requirement remains separate |
| Framework-only TODO modifications (pp3,5,6–7) | Direct diff from original ZIP shows exactly 8 replaced raise statements; all surrounding code/dependencies unchanged | Pass |
| Reproducibility, dependencies and required data paths | ZIP README commands, tested Python 3.12.14/Linux CPU, exact freeze, teacher-relative inputs present; first-run network requirement for MNIST/dependencies disclosed | Pass |
| Independent technical verification | /root/verifier fresh pinned environment, full P1/P2/P3 runs and independent math/data/model checks; current source hashes match | Pass |
| Actual candidate integrity and presentation | ZIP CRC, 412 full size/hash entries, 403 original inputs, seven-page visual/text inspection | Pass |
| External upload, commit/push | Not performed or authorized; not required to finish local preparation | N/A |

## Evidence assessment and limits

I read the actual P1/P2 JSON summaries, P3 manifest and all selected/last-epoch history rows cited by the report. The tables agree with their stated rounding. I compared the 15 non-runtime numerical/table/history/selection/PNG artifacts in results/run-20261029/{p1,p2,p3} directly with the independent reproduction; every file matched byte-for-byte, including all six generated PNGs. P3 runtime-containing manifest values were inspected separately. The only five required report figures correctly omit the extra unrequested input-data illustration, rather than omitting a grading requirement.

Verifier evidence includes actual commands/exit statuses, checks.json, source hashes, original teacher comparison and fresh-environment freeze. Its initial failed independent assertion and corrected second attempt are retained: the failed assumption was about k20's maximum pixel, not an implementation defect. The second check command exited 0. I did not rerun training as Reviewer, nor claim my hash comparisons constitute a new independent experiment. The existing independent technical validation covers the unchanged submitted scripts and data.

The reviewer's first output-comparison script accidentally traversed author command-log directories and looked for a corresponding verifier p3-command/run.json. This was a reviewer path-selection error, not a product failure; it was corrected to compare the actual p1/p2/p3 output directories, after which all 15 intended artifacts matched. No product/evidence files were changed.

The two quoted user messages are present in this reviewer's inherited chat context. The assistant construction excerpt is retained in notes/ai-collaboration.md and was supplied by the coordinator as an actual original-chat excerpt; its translated report text matches that record. This reviewer has not independently exported the full parent chat. The original should remain available for teacher review as requested; this review does not manufacture a stronger transcript-authentication claim. Automated checks cannot certify student understanding or authorship.

## Final readiness and handoff

**Not ready for direct school submission solely because the mandatory student personal step remains uncompleted/unconfirmed. The reviewed technical candidate passes this independent artifact review.** There are no implementation/report technical fixes requested, no missing experimental results, and no discovered required figure/table/code omissions. This conclusion applies only to the hashes above, not future edits.

Next actor: student, assisted by the coordinator if requested, to review understanding and personally express explanations. If the report or any packaged file changes, rebuild and perform affected checks and a new package review before calling that new version ready. No Blackboard upload, repository publish, commit or push is authorized or implied by this note.
