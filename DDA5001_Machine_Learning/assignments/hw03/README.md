# DDA5001 Homework 3

## Status

2026-10-29: all eight permitted TODOs implemented; all three full experiments completed; independent technical verification passed in a fresh pinned environment; seven-page English PDF and local submission candidate assembled. Independent final package review passed the technical candidate, with no technical Critical/Major issues (notes/review.md). School-submission status is Not ready for direct submission solely because the student personal review/own-word step remains outstanding. This is an AI-assisted draft: the teacher requires the student to understand/check the work and express explanations in their own words. That personal step has not been claimed as completed. Nothing has been uploaded, committed or pushed.

## Teacher sources and requirements

- requirements/DDA5001_HW3.pdf, pp1–7 (all pages read as text and rendered images).
- requirements/code_source(2).zip, preserved unchanged. Data-bearing archive is ignored in this assignment's .gitignore.
- PDF p1: English PDF and .py code in last name-first name-hw3.zip; due Nov 13, 23:59 (year/timezone not printed).
- P1 pp1–3: 30 points, degree-8 ridge, fixed five folds, all coefficients penalized, validation-selected lambda, train/test MSE and plots.
- P2 pp3–5: 20 points, original ORL images, centered thin SVD, eigenfaces and k20/k100 reconstructions.
- P3 pp6–7: 50 points, pre-run prediction, agent-assisted A/B/C construction, unchanged MNIST protocol, actual outcomes and at most one page collaboration record.
- Only 2+3+3 marked TODO bodies changed; all other framework text and original dependency descriptions preserved. No nested AGENTS/override rules found.

Detailed mapping: notes/plan.md. The initial wrong-material check is archived in notes/material-check-20261029.md; the user replaced those HW1 files before this implementation. Their existing deletions were preserved.

## Outputs and results

- Working code: src/p1/p1.py, src/p2/p2.py, src/p3/p3.py.
- Report: report/main.tex, report/images/, report/main.pdf.
- Full original runs: results/run-20261029/{p1,p2,p3}/. Exact argv/timestamps/exits/source hashes: sibling *-command/run.json and stdout/stderr files.
- P1 selected lambda=0.01, CV MSE=0.0482673693. Baseline train/test MSE=0.0009043599/2.0800339284; selected=0.0093339706/0.0402130755.
- P2 whole-dataset MSE: k20=0.0073473158; k100=0.0027157677.
- P3 A/B/C selected epochs=9/4/14; selected test accuracies=91.45%/90.80%/95.20%. Validation prefers C. Full metrics/history retained, including genuine later validation degradation.
- Author self-checks: tests/, results/self-checks/. Five tests pass; original TODO failure evidence retained. No fabricated algorithmic bug.
- Independent Verifier: notes/verification.md, results/verification/independent-20261029/. Fresh exact environment; all numerical results, histories and six plots match byte-for-byte. Separate mathematical/data/architecture checks pass.
- Actual AI interaction excerpt: notes/ai-collaboration.md, plus original Codex chat. Assistant pre-run prediction: notes/pre-run-prediction.md. Student authorship/checks are not fabricated.

## Environment and actual run commands

Python 3.12.14, AMD Ryzen 9 7945HX CPU, Linux x86-64, one numerical thread. Teacher pins: NumPy2.2.6, Matplotlib3.10.6, Pillow12.3.0, torch2.8.0+cpu, torchvision0.23.0+cpu. Full lock: results/environment/requirements-frozen.txt; hardware/source hashes: hardware-and-sources.json in the same directory. Sandbox DNS failures and successful network installs are retained there. No system Python or other homework environment was modified.

From this assignment root (shown commands were actually executed, through notes/run_recorded.py where indicated):

```bash
env -u PYTHONPATH OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python notes/run_recorded.py results/run-20261029/p1-command .venv/bin/python src/p1/p1.py --output-dir results/run-20261029/p1
env -u PYTHONPATH OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python notes/run_recorded.py results/run-20261029/p2-command .venv/bin/python src/p2/p2.py --output-dir results/run-20261029/p2
env -u PYTHONPATH OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python notes/run_recorded.py results/run-20261029/p3-command .venv/bin/python src/p3/p3.py --output-dir results/run-20261029/p3
env -u PYTHONPATH OPENBLAS_NUM_THREADS=1 .venv/bin/python -m unittest discover -s tests -v
```

Do not rerun into these evidence directories: choose a new run ID. P3 uses the supplied seed666, 30 epochs, batch128, learning rate0.1, momentum0.9, no decay, CPU deterministic configuration; only validation chooses checkpoints and the preferred model.

Report compiled with local XeLaTeX twice per version from report/; actual logs: results/report-build-v3/pass*.stdout.txt and *.exit.txt. App compiler could not download its Tectonic bundle; fallback documented. Current PDF: seven pages, all visually inspected, no overfull/underfull/undefined warnings. Earlier builds retained. Independent Reviewer inspected the exact candidate PDF/ZIP and all seven pages; see notes/review.md.

## Data provenance and local retention

Keep the unchanged framework-relative paths: src/p1/data/{training,test}.csv, src/p2/data/p2/ORL_faces/, src/p3/data/p3/mnist_split_indices.npz. Source: teacher ZIP; all 403 data files verified byte-for-byte. Hash/size manifest: results/teacher-package-manifest.json. The supplied torchvision loader downloaded MNIST into src/p3/data/mnist; all four gzip checksums independently match torchvision's official references. All 411 local input hashes are in results/input-manifest.json. Data, cached images, environments and weights are excluded from Git; local retention is not an independent backup.

## Submission candidate

- submission/Zhong-Kunyuan-hw3.zip (local only) and matching extracted directory.
- One PDF, three Python frameworks, original per-problem requirements, exact environment lock, concise reproduction README, and 403 necessary original teacher inputs at the required relative paths. MNIST auto-downloads; its cache is not bundled. No internal role records, experiment logs, environments or checkpoints are included.
- Exact inventory/hashes: results/submission-manifests/candidate-v1.json (412 files).
- School-delivery contents are distinct from Git-tracked contents; data remain ignored even inside the extracted candidate.
- Ready status must refer to the actual reviewed candidate; changes invalidate affected checks. Student personal review and own-word explanation are separate from technical verification. No Blackboard upload is authorized.

## Roles

/root: Planner, Implementer, Report Writer and candidate assembler (author checks only). /root/verifier: independent technical checks. /root/reviewer: separate final review. Phase evidence: notes/{plan,implementation,verification,report-evidence,review}.md. Do not treat the author's role changes as independence.
