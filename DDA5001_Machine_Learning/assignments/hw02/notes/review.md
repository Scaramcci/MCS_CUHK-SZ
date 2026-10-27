# Current final review status — final user-requested recheck

Independent Reviewer `/root/reviewer`, 2026-10-27. **Ready — checked local package
prepared for the user's submission.** This verdict covers the exact ZIP SHA256
`16dda52687c9733e4e0091cd67d12ac137b6519e27dfa8a0cbbd2e40bf537fbb`
and PDF SHA256
`1afba6eea2f64585c30d84577de357572970a767f78049e32c49c4d272d64d76`.
Technical/grading-artifact/package/layout checks passed. The user now reports
having completed their personal review; that is recorded as user-reported,
not as independent proof of student understanding, own authorship, or rewriting.
The actual AI assistance remains openly disclosed. Ready does not mean teacher
approval, a guaranteed mark, or an upload. Nothing has been uploaded.

This current disposition supersedes the earlier pending-personal-review status.
The original reviews and their version-limited conclusions are preserved below;
the newest detailed audit is the final section of this record.

# Independent final review — Homework 2

Reviewer: independent subagent `/root/reviewer`, 2026-10-27, Asia/Shanghai.
I did not author this implementation, report, or verification scripts and was not
this round's Verifier. Authorized writes: this file only; temporary PDF extraction
and renders under `/tmp/hw02-review-*`. No product files were changed.

## Inspected version and scope

- Branch `master`, HEAD `b02d5732be2b1bc074217fb236ca882b594e432d`.
- Candidate `submission/Zhong-Kunyuan-hw2.zip`: **1,017,475 bytes**, SHA256
  `5379b8c1f00c61d3d2bb270cbdda5164db2e338ca149bdfee7450abc7ffef867`.
- Actual ZIP PDF SHA256
  `54d2647d2dbd938b8735ed7ebb894f815938bb08328daabd52fd73549df59c39`.
  It equals the extracted candidate PDF and `report/main.pdf` byte for byte.
- Read root README/AGENTS, agents README/reviewer role, course README, hw02
  README/plan, verification record, actual code/check scripts, result manifests,
  analysis and summaries, packaged README/dependency lists and AI source excerpts.
  No lower-level AGENTS/override or requirements folder was present. Originals
  remain at the assignment root and were not modified.
- Independently read all seven original teacher PDF pages, including visual
  formula/matrix inspection using the seven rendered pages. Reviewed every
  required subpart against that original, rather than relying on the plan.
- Extracted the actual PDF bytes from the ZIP into `/tmp/hw02-review-actual.pdf`,
  rendered all 12 pages myself and visually inspected all pages. No missing glyph,
  overlap, clipping, broken matrix/table, unreadable figure or unexpected page was
  found. All content is English; AI case occupies exactly page 7.
- This is final review, not a second technical reproduction. Actual independent
  execution coverage is reported by `/root/verifier` in `notes/verification.md`.
  Its recorded commands exit 0; I checked those run records and packaged hashes.

## Critical issues

None found in the inspected package: no fabricated numerical result, credential,
private-directory material, incorrect source version, missing executable/PDF,
dataset, environment, cache, raw trial archive or internal role note was observed.
The normal required student name/ID appears in the report/README. No external
upload or Git action was performed.

## Major issues

1. **P2(b)(4) student interaction requirement remains unmet in this candidate.**
   Teacher PDF p5 requires “your actual prompt” and numerical evidence “you brought
   back” with a focused follow-up. Candidate report p7 explicitly and honestly
   identifies the case as coordinator-agent/coding-agent dialogue, rather than
   student-authored dialogue. That disclosure avoids fabrication, but it does not
   establish the requested student's actual interaction. Preserve the real source
   exchange; replace or augment the one-page case with an authentic student-agent
   verification decision and numerical follow-up. Do not reattribute agent prompts
   to the student. A later live student question was reported by root, but is not
   in this immutable candidate and therefore cannot clear this finding yet.
2. **Student-owned mathematical wording/understanding is unconfirmed.** Teacher
   PDF p1 says to write derivations/explanations in the student's own words and
   makes the student responsible for understanding/checking all submitted work.
   Candidate p12 truthfully says Codex assisted with derivations and English
   drafting and does not claim a completed personal review. An agent cannot
   certify that personal obligation. The student must personally review and
   rewrite the derivations/explanations in their own wording before submission;
   the final delivery must not imply that this condition has already been met.
   Revisions to the candidate require affected correctness/layout/package review.

## Minor issues

- Assignment README and plan retain “in progress”/unchecked milestones despite
  completed technical work. These internal files are outside the package, so this
  does not affect its grading content, but final handoff status should be updated
  without claiming the unresolved student requirements are complete.
- No mathematical, grading-coverage or layout minor defect was found in this
  inspected PDF. Very large P3 means are real retained outcomes, not formatting
  mistakes; the discussion correctly describes display saturation and uncertainty.

## Submission checklist

| Original requirement | Actual artifact/evidence | Review result |
|---|---|---|
| p1 one English PDF, ZIP surname-firstname-hw2 | 12-page PDF in correctly named Zhong-Kunyuan-hw2.zip | Pass |
| p1 separated p2/p3; small verification scripts; no bulky data/cache | Exact 20-file ZIP listing below; both verify.py scripts and teacher runners | Pass |
| p1 own mathematical wording and understanding | p12 explicitly unconfirmed; personal obligation | Required student action |
| P1a,b p1 | PDF p1 gives affine VC d+1, finite test fraction vs population error with independence qualification | Pass |
| P1c,d p1-2 | PDF p1 identifies GD option2 and softmax option3 false, explains all eight options | Pass |
| P2a p2-3 all four derivation stages | PDF p2 CE derivative, logits chain-rule sum, outer product, mean matrix gradient | Pass |
| P2b1 p4 six functions, stable logits, gradient/update definitions | Packaged algorithms.py, source/Verifier hashes; no forbidden solver/autodiff | Pass |
| P2 fixed preprocessing/settings p3 | Teacher framework/run/tests byte-identical; independent full reproduction record | Pass |
| P2b2 gradient p4 | PDF p3 two required 3x3 matrices, epsilon1e-6, max error1.174011e-10 | Pass |
| P2b2 accelerated updates p4 | PDF p3 current and extrapolated evaluation matrices, both outputs, explanation and actual tolerances | Pass |
| P2 tests and before-full-run checks p4 | Real run records; clean independent 7/7 tests and small checks, all exit0 | Pass via independent Verifier |
| P2b3 figures p4 | PDF p4-5 and four included PNGs, six curves each, log loss axes, completed updates | Pass |
| P2b3 results/questions p4-5 | PDF p6 six-row 4-metric table, speed/rank/overfitting answers match analysis.json | Pass |
| P2b4 <=1page, real prompts/numerical follow-up/decision p5 | PDF p7 one page, real agent-agent case, formulas and original excerpts retained | Major: student's actual exchange missing |
| P3a p6 least squares | PDF p8 designs/vectors, rank proof, normal equations, explicit K2/K10 solutions | Pass |
| P3b p6 analytic risk | PDF p8 zero padding, cq=aq/CQ, density1/2, orthogonality, both degrees and tails | Pass |
| P3c implementation/shapes p7 | Packaged algorithms.py/lstsq/padding, independent scalar/batch checks | Pass |
| P3c numerical fit/error checks p7 | PDF p9 expected/computed coefficients and risks; 80-node quadrature, explanations | Pass |
| P3 tests p7 | Independent clean 8/8 tests, added checks and randomized independent oracle checks | Pass via independent Verifier |
| P3 fixed trials/grids/no clipping p7 | Independent full raw array reproduction, all1,911,000 cell-trials retained; manifests | Pass via independent Verifier |
| P3 two heat maps p7 | PDF p10 and two separate PNGs with exact axes, settings, colors/contours | Pass |
| P3 interpretation p7 | PDF p11 colors/zero, n/noise, complexity, noiseless positive example, finite-trial limits | Pass |
| Execution/data instructions | Packaged README uses valid paths/commands; exact UCI URL/checksum/fallback; both requirements | Pass |
| Final ZIP equality/integrity | testzip returns None; every member equals extracted disk file; source equals verified src | Pass |
| Final PDF appearance | All12 pages independently rendered from actual ZIP bytes and viewed | Pass |
| Blackboard submission | No upload authorized/performed | N/A to local package review |

The six PNGs equal the original full-run PNGs byte for byte. The frozen dependency
file equals the actual run's freeze. All seven fixed framework/runner/test/teacher
requirements files match original ZIP bytes. Both implemented algorithms and both
verify scripts match the hashes independently tested by the Verifier. Report
metrics, ranks, gradient values, accelerated outputs, fit checks and selected P3
numbers agree with the real evidence. No unsupported specific hardware claim or
made-up reference was found.

## Exact ZIP inventory / SHA256

| ZIP member | Bytes | SHA256 |
|---|---:|---|
| `Zhong-Kunyuan-hw2/DDA5001_HW2_answers.pdf` | 556307 | `54d2647d2dbd938b8735ed7ebb894f815938bb08328daabd52fd73549df59c39` |
| `Zhong-Kunyuan-hw2/README.md` | 2737 | `cec0abdaedf23dc938890048c77be7cc65b01b423a63c0c5f66ccf20ce807730` |
| `Zhong-Kunyuan-hw2/figures/digits_accuracy.png` | 70053 | `016bbc14f9b54b23724d9a0a64ee864024cbaab7157d6abe0bc1dcf8f9e96f3a` |
| `Zhong-Kunyuan-hw2/figures/digits_loss.png` | 103269 | `7bcb115c3f0a503cf1391ff0aa530aa1024b7e4c6a257d80f360512789499f81` |
| `Zhong-Kunyuan-hw2/figures/dry_bean_accuracy.png` | 70898 | `3c68456d0dae7049436cbbbe6ae5b2c0002ba0c94339a7e294f5ec59723f4bc0` |
| `Zhong-Kunyuan-hw2/figures/dry_bean_loss.png` | 95450 | `e5c15eb36a55396429f2d27b6b10c32252421047b8ea12f300c71709f5e497ec` |
| `Zhong-Kunyuan-hw2/figures/noise_variance.png` | 93918 | `b9edc1da98ae45e1882b971229372e0bd16a35976f5b8391d6312e994b26f92f` |
| `Zhong-Kunyuan-hw2/figures/target_complexity.png` | 95289 | `d94cf79a007a62fc10c98877bac16e79e71a4cd18aac8bbdad1525b873ca0a90` |
| `Zhong-Kunyuan-hw2/p2/algorithms.py` | 2670 | `f3dff6c0408536b60731cb55c4f1e3237ddd234ed75c28359045acf45f78af96` |
| `Zhong-Kunyuan-hw2/p2/framework.py` | 13186 | `612986d10d8fe914133021e0d16d63e6141ee9968c7383ccfcbb1e647c9b5d3f` |
| `Zhong-Kunyuan-hw2/p2/run.py` | 553 | `6eeade766b0c9787c18ff986bd0e90749599013351ea076c09859f01152b255b` |
| `Zhong-Kunyuan-hw2/p2/test_p2.py` | 4049 | `c0194b5adfe4967f82d571248e7d355d2bfe9c36810a88ea7fa146f81c9c99f8` |
| `Zhong-Kunyuan-hw2/p2/verify.py` | 5952 | `e53d23cb855612ad3df79022d8932fa6132458c009161ee9ffc25a73fb558a81` |
| `Zhong-Kunyuan-hw2/p3/algorithms.py` | 2474 | `b05e25fa40cf890404693e2a15cc573ed26dabbdccee2c0894fc58900a97f4d7` |
| `Zhong-Kunyuan-hw2/p3/framework.py` | 11818 | `08daea51f823923897b993e72a830cf3e8013977bde0731cfe1d0774bb2abab8` |
| `Zhong-Kunyuan-hw2/p3/run.py` | 399 | `0921a3922717afca9e1702d0257a3c81dd4d7f46b14cf95c59d987db02472f4f` |
| `Zhong-Kunyuan-hw2/p3/test_p3.py` | 4736 | `e9cc991e21b688d04a031b26d64e735c89e3e6bfa1325e98b0dfa4eea3788d1a` |
| `Zhong-Kunyuan-hw2/p3/verify.py` | 5987 | `83905ae5b16a1bf9506eb6e1e5c89a8f5c56223426af2f53c5c1838101efd719` |
| `Zhong-Kunyuan-hw2/requirements-frozen.txt` | 286 | `cfdbdbf4629c86c32c92e46245c8d871132006d745a0e7566f4e74edb5e01f8e` |
| `Zhong-Kunyuan-hw2/requirements.txt` | 87 | `222f6e10d0679db96d6e8a127b3050aadca9022f866e65c77936a67ea5c75895` |

## Final readiness

**Not ready for unconditional submission for this exact candidate.** Technical
implementation, experiments, numerical evidence, required files and report layout
passed the inspected checks and independent technical reproduction. Two explicit
student-facing requirements above remain unresolved. This is a version-limited
review, not teacher approval. Root may deliver the candidate with clearly stated
required student actions, but must not call it fully compliant or already submitted.
Any rebuilt candidate requires renewed package/PDF review; no source changes are
needed for the technical findings currently established.


# Revision 2 affected review — authentic student exchange

Current ZIP SHA256 `564aad7e46845ee22d3b6fcf5d74fee8e0dbc03813014c39415776d3b17348a4`,
1,018,686 bytes, 20 members. Current PDF SHA256
`8895dda3edd7702994124057568b7431c5eabc1b6df86ca6f656228561091c11`, 557,397 bytes.
Packaged README SHA256
`80f80d045b0c3be5ea4f07e3861902cca0bf0d4c42527fbc00485aa91237d8b0`.
These three are the only changed ZIP members; the other 17 hashes above still apply.

- Opened actual ZIP again; testzip None; all members equal corresponding extracted
  candidate disk files; numerical algorithms/frameworks/runners/tests/check scripts
  and dependencies still exactly equal independently verified source/evidence.
- Extracted current PDF directly from ZIP to `/tmp/hw02-review-actual-v2.pdf`.
  Rendered/visually inspected actual pages 7 and 12 at 100dpi. Both are legible,
  fit their pages, show no clipping, and AI case still totals one page.
- Rendered all 12 pages at the original review's 70dpi. Pages 1-6 and 8-11 are
  byte-identical PNG renders to V1. Therefore their already completed content and
  visual checks apply exactly; numerical results/formulas have not changed.
- Read retained `notes/student-ai-conversation.md` and new packaged README.
  Student initial question and focused numerical follow-up are authentic per the
  current live parent-chat record; English translations and suggested-answer
  selection are disclosed. No student manual calculation or earlier derivation
  is invented. The reproduced 2.78e-17 and counterfactual .0008 distinction is
  mathematically correct and supported by the real script output.
- **Initial Major1 is partially resolved:** the case now supplies the student's
  actual prompt and numerical follow-up, as teacher p5 requests. Its final retain
  decision is still explicitly Codex's action. Teacher p5(iv) requests “your final
  decision to revise or retain the code”; include the student's authentic stated
  decision rather than reattributing Codex's decision. Root reports that question
  is pending. This finding is restricted to the current immutable V2 candidate.
- **Initial Major2 remains:** own-word mathematical understanding/review cannot be
  certified by the agent and has not been established. p12/README truthfully say so.
  Required student pre-submission action remains personal review and rewriting.
- Initial internal stale-status Minor is resolved sufficiently by updated hw02
  README, which now accurately reports completed technical work and pending final
  student/review conditions.

No new Critical/technical/layout issue found. V2 status: **Not ready for
unconditional submission**, despite passed technical/package checks. Complete
student decision and personal wording obligations before claiming compliance;
any new package needs renewed affected review. No upload performed.


# Revision 3 final immutable-package review

Final ZIP `submission/Zhong-Kunyuan-hw2.zip`: SHA256
`16dda52687c9733e4e0091cd67d12ac137b6519e27dfa8a0cbbd2e40bf537fbb`,
**1,023,135 bytes; 20 files**. Final packaged PDF SHA256
`1afba6eea2f64585c30d84577de357572970a767f78049e32c49c4d272d64d76`,
**561,992 bytes; 12 pages**. Final packaged README SHA256
`b122d506f720390c6d04363583b2f76f5f035b9ec3246d58bb1b8d3d2309c13d`,
3,138 bytes. All other 17 ZIP-member hashes and sizes are unchanged from the exact
inventory in the initial review above.

## Actual affected checks

- Opened the actual final ZIP; CRC/integrity test returned None (success). Every
  member equals its extracted candidate disk file. All packaged numerical source,
  checks, unchanged teacher framework/run/test/dependency files equal verified src
  bytes; source did not change after independent verification. No new cache,
  dataset, raw archive, internal note or credential appears among the 20 members.
- Extracted actual ZIP PDF into `/tmp/hw02-review-final.pdf`, rendered all 12 pages
  at 70dpi, and compared against reviewed V2 renders: **only page 7 changed**.
  Pages 1-6 and 8-12 are byte-identical renders, preserving prior complete content
  and visual findings. Re-rendered page 7 at 100dpi and visually inspected it:
  entire case still fits one page and remains legible with no clipping or overlap.
- Read final AI page, final packaged README, and the appended original student
  final-decision request/assistant response in `notes/student-ai-conversation.md`.
  The student said “你帮我写吧” and Codex transparently drafted the decision at that
  explicit request. Actual prompts, translations, selected suggested follow-up,
  script provenance and assisted final wording are identified accurately.
- The final-decision section now **exists and contains a documented, supported
  assisted conclusion**: retain code because the prescribed gradient point and
  tiny update discrepancy agree, with wider checks/full independent reproduction.
  This clears the former missing-section finding at the artifact level. It does
  **not** establish independently expressed student judgment; the report does not
  falsely claim that it does. No extra human endorsement or computation is invented.
- The teacher p1 requirement to express derivations/explanations in the student's
  own words remains an explicitly stated personal pre-submission action. This
  review cannot certify it from an AI-drafted artifact. The final candidate's
  disclosure and README truthfully preserve that limit.

## Final issue/readiness disposition

- Critical: none found in reviewed scope.
- Technical/report mathematics/results/package/layout Major: none found.
- AI-case artifact omission: resolved, with assistance/provenance accurately disclosed.
- Remaining Major / student action: teacher p1 personal own-word/understanding
  requirement unconfirmed. Student should review and rewrite mathematical
  explanations personally before submitting; any edits invalidate affected PDF/
  package review until checked again. This is a requirement from the original,
  not an invented approval gate, and no further permission request is needed.
- Minor: no remaining material issue affecting this package.
- **Technical/artifact checklist Pass; final unconditional readiness Not ready**
  solely for the above unresolved personal teacher requirement. The package may
  be delivered as an audited AI-assisted submission candidate with that explicit
  action stated. Do not call it fully compliant, independently student-authored,
  teacher-approved, or already submitted.

No production source, report or package was modified by this Reviewer. This final
record pertains only to the hashes printed above. Independent execution remains
that of `/root/verifier`; final package review remains that of `/root/reviewer`.


# Final requirement recheck after user-reported personal review

Date: 2026-10-27, Asia/Shanghai. Independent Reviewer: `/root/reviewer`.
Trigger: the student said, verbatim, “我看完了，没有问题，请再根据作业要求检查一遍作业，
没有问题我就提交了”. This is a **user-reported completed personal review** following
our prior review instructions. It is not evidence that a rewrite, unaided
mathematical authorship, or independently demonstrated understanding occurred.
No source/report/package changed; I do not invent such a change or endorsement.

## Scope and current immutable identity

- ZIP: `submission/Zhong-Kunyuan-hw2.zip`, 1,023,135 bytes, SHA256
  `16dda52687c9733e4e0091cd67d12ac137b6519e27dfa8a0cbbd2e40bf537fbb`.
- PDF: 561,992 bytes, 12 pages, SHA256
  `1afba6eea2f64585c30d84577de357572970a767f78049e32c49c4d272d64d76`.
- ZIP members: exactly the 20 files listed in prior inventory; final changed-member
  hashes are in revision 3 and `results/final-audit-20261027/summary.json`.
- Original teacher PDF SHA256
  `f131d01bcbeb286b0cbc978be38d4978e2a7e0f9bab8e697e9332b8ddcd8920e`;
  teacher code ZIP SHA256
  `6f58949e6ef4ac1dce1857d3373fc804aee34c0b431a307deee26d08dedd32b4`.
  Both originals are unchanged.
- Branch remains master; existing uncommitted work preserved. Only this review
  record was edited by Reviewer. No production artifact or submitted bytes changed.

## Repeated requirement and package audit

I reread the complete seven-page teacher PDF, rechecked current final PDF text
against every original grading item and confirmed unchanged PDF bytes. The prior
independent visual inspection of **all 12 actual ZIP PDF pages**, including the
final AI page, remains valid for these exact bytes. No new layout issue exists.

| Mandatory area | Current result |
|---|---|
| P1 all four parts, every choice explained | Pass, PDF p1 |
| P2a four-stage mean CE matrix gradient derivation | Pass, PDF p2 |
| P2 six functions, stable logits loss, analytic training gradient, proper update locations/no mutation | Pass, source and independent checks |
| P2 prescribed matrices, both gradients/max discrepancy, both accelerated evaluation/update matrices and explanations | Pass, PDF p3 and verify.py |
| P2 fixed data processing/seed/init/1000updates/mu.05/beta.90, no regularization/test gradients | Pass, unchanged framework and independent reproduction |
| P2 four six-curve figures/log loss, complete final six-row metrics table, all three analytical questions | Pass, PDF p4-6 |
| P2 AI case <=1page, actual concern/prompt/reply/numerical follow-up, supported final decision, original exchange retained | Pass as disclosed assisted artifact, PDF p7; independent student judgment is not claimed |
| P3 design/vectors/normal equations for degrees2/10 | Pass, PDF p8 |
| P3 correct normalized coefficient tails/orthogonality/density1/2, both risk formulas | Pass, PDF p8 |
| P3 numerical expected/computed fitting and risk examples with explanations | Pass, PDF p9 |
| P3 two correct full grids/1000trials, arithmetic means/no filtering/no numerical clipping | Pass, manifests/raw independent reproduction; PDF p10 |
| P3 colors/zero contour/n/noise/complexity/noiseless interpretation and empirical-contour limits | Pass, PDF p11 |
| One English answer PDF; correctly named ZIP; separate p2/p3; small verification scripts; both P3 heatmaps included | Pass, actual 20-member ZIP |
| Valid run/dependency/data-source/checksum/fallback instructions | Pass, packaged README and requirements |
| No forbidden datasets/environments/caches/raw trials/internal notes/credentials | Pass, actual exact inventory |
| Personal review | User-reported complete; understanding/own authorship/rewriting not independently certified |

Reopened current ZIP and ran CRC integrity test (None/success). Every ZIP member
was compared to the extracted candidate disk file and matches. All packaged
numerical source and checks equal the independently verified `src/` bytes.
All seven fixed teacher files were again compared directly against original ZIP
members and match exactly. The six packaged PNGs again match full-run result
PNGs byte for byte; the frozen dependencies equal the run's actual freeze.
The metrics, numerical matrices, ranks, P3 selected values, uncertainty and
interpretations remain the supported outcomes in earlier completed review.

## Fresh exact-ZIP execution evidence

Root separately extracted this immutable final ZIP under
`results/final-audit-20261027/.cache/extracted/Zhong-Kunyuan-hw2` and ran four
fresh commands. I read the actual logs, run records, JSON checks and summary,
rather than relying only on root's report:

| Evidence prefix in results/final-audit-20261027 | Actual outcome |
|---|---|
| p2-tests | 7/7 tests OK, exit0 |
| p3-tests | 8/8 tests OK, exit0 |
| p2-checks | all_passed true, exit0; gradient max difference1.1740114436165072e-10; both accelerated update errors2.7755575615628914e-17 |
| p3-checks | all_passed true, exit0; expected/actual fit, quadrature, tails and batch checks agree |

I independently compared the fresh `checks` objects against the main run's
`results/run-20261027/p2-checks.json` and `p3-checks.json`: they are exactly equal.
Source hashes in these outputs match the ZIP. Full experiment reruns were already
performed independently by `/root/verifier`, with all parameters/history/raw trial
arrays and plots reproduced; source and result bytes have not changed since.
This fresh package audit supplements that independent verification; it is not
misrepresented as a new independent implementation/reproduction by this Reviewer.

## Final issue and readiness disposition

**Critical issues:** none found in the inspected scope.

**Major issues:** no unresolved technical, mathematical, grading-artifact,
format, evidence or package issue found. The previous pending-personal-review
handoff is now recorded as completed by the user's own report. That change is
based on the user's message, not a false claim of changed authorship or rewritten
files. Teacher p1's personal responsibility and own-word rule remain the student's
responsibility; this record makes no claim to prove those private facts.

**Minor issues:** none requiring changes before local submission. Historical
review states refer to earlier versions/status and are preserved for provenance.

**Final readiness: Ready — checked local package prepared for user submission.**
This is a bounded review of the exact bytes above, with transparent AI-assisted
provenance and the user-reported personal-review status. It is not teacher
approval, independent proof of student authorship/understanding, or confirmation
of Blackboard upload. The student can submit this ZIP; no new permission loop is
needed. Changes to the ZIP/PDF/source after this audit require affected rechecks.
