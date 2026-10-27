# DDA5001 Homework 2

Status (2026-10-27): Ready — checked local package prepared for user submission.
Independent final recheck found no required product fix. User reports having
completed personal review ('我看完了，没有问题'); that is recorded as user-reported,
not independent proof of authorship, understanding or rewriting. Genuine AI
assistance remains disclosed. From the exact ZIP, all15public tests and both
small verification scripts passed afresh. See notes/review.md current status
and results/final-audit-20261027/summary.json.12-page PDF,20-file ZIP:
submission/Zhong-Kunyuan-hw2.zip. No artifact bytes changed in this recheck.
Ready does not mean uploaded or teacher-approved. Nothing has been uploaded.


## Sources and deadline
Original `DDA5001_HW2.pdf` p1-7 and `code_source(1).zip` are retained unchanged at
the assignment root. No hw02 requirements/ or README existed initially. Teacher
working copies are in src/; no lower-level AGENTS/override rules were found.
HW01 was consulted for report layout, name and student ID only.

100 points: P1 concepts (15), P2 softmax regression (40), P3 overfitting (45).
Teacher PDF p1: Oct 30, 23:59, timezone/year not printed. English PDF and Python
code, p2/ and p3/ separate, in `Zhong-Kunyuan-hw2.zip`, submitted to Blackboard.
No late work is graded. No datasets, environments, caches or large trial
archives in the ZIP. Preparation here does not mean it has been submitted.

## Implementation and completed runs
Only the two numerical algorithms.py files were completed; the original
frameworks, runners, public tests and requirements are byte-identical to ZIP
originals. Two added small verify.py scripts print the required numerical checks.
P2: fixed seed666, exact deduplication, stratified80/20 split, training-only
standardization, constant feature, full batch, 1000 updates, learning rate.05,
momentum.9, Nesterov(k-1)/(k+2), no regularization or test-set tuning.
P3: seed666, 1000 trials/cell, original 21x50 and21x41 grids, all trials retained;
no regularization/clipping/smoothing of numerical errors.

Python3.12.14 local environment `.venv312/`; exact teacher pins plus complete
transitive versions in results/requirements-frozen.txt. System Python3.14 could
not build pinned SciPy; setup failures retained in notes/environment-setup.md.

Actual commands from src/ (main run records also store exact argv/timestamps):
```
env -u PYTHONPATH ../.venv312/bin/python -m unittest discover -s p2 -v
env -u PYTHONPATH ../.venv312/bin/python p2/verify.py --output ../results/run-20261027/p2-checks.json
env -u PYTHONPATH ../.venv312/bin/python p2/run.py --data-dir ../data --output-dir ../results/run-20261027/p2
env -u PYTHONPATH ../.venv312/bin/python -m unittest discover -s p3 -v
env -u PYTHONPATH ../.venv312/bin/python p3/verify.py --output ../results/run-20261027/p3-checks.json
env -u PYTHONPATH ../.venv312/bin/python p3/run.py --output-dir ../results/run-20261027/p3
```
Public tests7+8 passed. Exact test/check invocations and author self-check logs:
results/implementation-tests/. Main full runs/checks:
results/run-20261027/{p2-experiment,p3-experiment,p2-checks,p3-checks}/run.json.
Do not rerun into existing evidence paths; choose a new output directory.

## Results and independent checks
- P2: six train/test trajectories, final metrics, four separate figures, manifest.
  All prescribed gradient/update/stability checks are recorded numerically.
- P3: both full heat maps, raw1,911,000 cell-trial observations, means and manifest.
  Genuine large errors remain, with color saturation only at+/-0.25.
- Separate independent Verifier created an offline fresh environment, reran
  all tests/checks and complete experiments; all numerical outputs and eight
  plots exactly matched. See notes/verification.md and
  results/verification/20261027-independent/.
- Report source: report/main.tex; generated matrices/tables from
  notes/build_report_evidence.py. Build logs: results/report-build-*/.
  Final review: notes/review.md, version-specific.
- Submission: submission/Zhong-Kunyuan-hw2.zip and matching extracted directory.
  Each assembled candidate has an exact file/hash manifest under
  results/submission-manifests/. Superseded candidates are retained under
  results/submission-history/ and are not the current submission.

## Data (local only)
Digits is included in scikit-learn. Dry Bean official fixed CSV:
https://archive.ics.uci.edu/static/public/602/data.csv
Expected SHA256: c91a086bb4357e69409d23287ec22be1be9512145cead1d8ca988c918be38fcb.
Downloaded and verified to data/dry_bean.csv (ignored); source/time/hash record:
results/dry-bean-source.json. P3 simulated arrays and raw trial outputs stay
local and ignored. Local retention is not an independent backup.

## Roles and assistance
/root coordinated planning, run recording and AI-assisted report drafting;
/root/implementer authored numerical functions and self-check scripts;
/root/verifier independently verified code/experiments; /root/reviewer inspects
actual report/ZIP and does not repair them. See notes/plan.md,
notes/implementation.md, notes/verification.md, notes/report-evidence.md and
notes/review.md for actual scope and hashes. Genuine agent-to-agent and later
student-agent exchanges are retained under notes/; none are fabricated or
misattributed. Teacher PDF p1 requires the student to understand/check submitted
work and express mathematical derivations/explanations in their own words.
The agents cannot confirm that personal step on the student's behalf.
