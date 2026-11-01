# HW3 implementation and delivery plan

Planner / executor: /root. Date: 2026-10-29. Direct execution authorized by the user's request to complete HW3. Scope: this assignment only; stay on master. Root course rules override generic skill suggestions on paths, branching and repeated approval. Planning/implementation/reproducibility skills applied; internal notes live here per repository conventions.

## Sources and current state

Read all seven pages of requirements/DDA5001_HW3.pdf as text and rendered pages; inspected all three Python frameworks and dependency files in requirements/code_source(2).zip. ZIP contains 400 ORL images, two ten-row CSVs and fixed MNIST split indices, but no MNIST images. The user replaced the mistakenly placed HW1 files; preserve their current deletions. Initial previous material check is archived in material-check-20261029.md. No nested rules. Full teacher package manifest is results/teacher-package-manifest.json. Sources are immutable.

## Requirements, deliverables and acceptance

| Source | Requirement | Deliverable and acceptance |
|---|---|---|
| PDF p1 | English PDF and .py in last name-first name-hw3.zip; due Nov 13 23:59 (year/timezone not printed) | English report and three completed framework scripts in Zhong-Kunyuan-hw3.zip; no external upload |
| PDF pp1–3, P1(a), 18 pts | Degree 8, mean loss plus penalty on all coefficients; 16 candidates; fixed row-ID folds; minimum mean validation MSE, smaller lambda on exact tie | Derivation, completed two functions, full CV table and log-x curve; independent scoring and scaling/tie tests |
| PDF p3, P1(b), 12 pts | Refit all ten; compare unregularized, selected, training data, clean curve with fixed axes; both train/test MSE; 2–3 sentence discussion | Supplied fits.png, metrics, concise explanation; no test-based selection |
| PDF pp3–5, P2(a), 8 pts | Original ordered 112x92 normalized faces, thin centered SVD, first 16 eigenfaces | Three completed functions; 4x4 descending grid; shape/order, orthogonality and centering tests |
| PDF p5, P2(b), 12 pts | Subjects 1–5 image 1; 5x3 original/k20/k100 grid; whole-dataset unclipped MSE; 2–3 sentences | Reconstruction grid, numerical table, projection and discarded-energy checks |
| PDF p6, P3(a), 8 pts | Predict before running | notes/pre-run-prediction.md, later quoted as AI-assisted prediction; algebra explains affine equivalence and ReLU |
| PDF p6, P3(b), 14 pts | Only three constructors; A 784→10, B 784→64→10, C same plus hidden ReLU, all biases, raw logits | Three constructors; model structures/counts, finite raw outputs and affine-equivalence checks |
| PDF p7, P3(c), 18 pts | Run unchanged framework; CE curves, selected epochs/val CE/test CE/test accuracy, validation choice, A–B/B–C and gaps/last-epoch discussion | Real 30-epoch CPU run; figures and tables from records, validation choice frozen before tests |
| PDF p7, P3(d), 10 pts | At most one page actual agent construction collaboration | Actual user prompts and assistant reply excerpts, truthful tool/check attribution, no manufactured interaction |

## Implementation and verification sequence

1. Preserve pre-run prediction. Extract unchanged teacher inputs into src/p1, src/p2, src/p3, with data at framework-relative ignored paths. Archive-with-data ignored by assignment .gitignore; do not change root rules.
2. Create local .venv using Python 3.12; install teacher pins. Record failures and actual versions; do not modify supplied requirements to hide deviations.
3. Before numerical implementation, establish meaningful checks. P1 test: X=I, y=(2,4), lambda=.5 must yield (1,2) for m=2; exact CV ties choose smaller candidate. P2: tiny images preserve C-order columns; full basis reconstruction and tail-energy identity. P3: model counts 7850/50890/50890, shapes (2,10), no output softmax, B collapse equals direct affine formula. Only TODO bodies may change; compare remaining source against ZIP.
4. P1 final fit: solve (X.T@X + m*lambda*I)theta=X.T@y; CV matrix receives each supplied MSE and argmin over row means. P2: images.reshape(n,-1).T; mu=X.mean(axis=1,keepdims=True); U,s,_=svd(X-mu,full_matrices=False); Theta=U[:,:k].T@(X-mu), Xhat=mu+U[:,:k]@Theta. P3: nn.Linear(784,10), nn.Sequential(nn.Linear(784,64),nn.Linear(64,10)), and same with nn.ReLU() between.
5. Run from assignment root: .venv/bin/python src/p1/p1.py --output-dir results/<new-run>/p1; similarly p2 and p3. Use prescribed CPU one-thread deterministic P3, seed 666, 30 epochs, batch128, LR.1, momentum.9, no decay. No algorithm/hyperparameter changes. Log argv, times, exits, input/source hashes, environment/hardware and output manifest. Keep raw CSV/data local.
6. Independent Verifier (not author) checks source restrictions, data provenance, analytic tests and full numerical runs in fresh pinned environment; writes notes/verification.md and results/verification only. Root fixes any failures, then reverify.
7. Root as Report Writer uses actual evidence; compile/render English PDF using prior homework typography. Record claim-to-evidence mapping. Clearly disclose AI drafting; student understanding and own-word requirement cannot be certified by agents.
8. Assemble PDF, p1/p2/p3 scripts and dependency descriptions plus concise data/reproduction instructions and the 403 unchanged teacher inputs required at framework-relative paths; exclude MNIST cache and environments, into exact submission folder/ZIP. Independent Reviewer distinct from Verifier inspects actual package, all scoring points, figures and collaboration page. Any change invalidates affected checks; preserve old candidate versions.

## Success criteria and limitations

Automated: all 8 TODOs completed; non-TODO framework text unchanged; input hashes match; all numerical invariants pass; prescribed experiments run with traceable outputs; PDF compiles; ZIP contents/hashes match manifest. Manual/visual: all source pages read, output figures and every report page inspected, reviewer judges coverage/consistency. Student must personally check understanding and express derivations/explanations in their own words before submitting; do not claim this is completed. No ready-made external answers, additional tuning, uploads, commits or pushes. Dataset/network/dependency access failures are recorded and addressed without fabricated results.

## Packaging decision after implementation

2026-10-29, /root: include the small, directly required teacher inputs (two CSVs, 400 ORL images, one split NPZ) in the local-only ZIP and ignored data/ directories. The unchanged frameworks require these paths; this avoids making the recipient reconstruct the layout. MNIST auto-downloads and is omitted. This refines the initial no-data packaging idea; root rules distinguish Git exclusions from school-delivery completeness. No datasets are staged or committed.

## Final execution status (2026-10-29)

/root completed implementation, real runs, report and candidate assembly. /root/verifier independently passed exact-source checks and full fresh-environment reproduction; /root/reviewer independently passed the actual technical PDF/ZIP candidate with no technical Critical/Major issues. Candidate SHA-256: 0c3f045094c287ab89adf8570c675882bfa1878fb3c691cb026ff485e9661f1e. All machine-executable/visual artifact tasks are complete. Student personal understanding/checking and own-word expression remain outstanding; no unqualified school-submission Ready is claimed. Nothing uploaded or committed.
