# Independent technical verification — DDA5001 HW1 P3/P5

Verifier: independent child agent `/root/verify_hw1`, 2026-09-29 13:15 UTC. I did not implement or edit the tested `src/` files, report, original requirements, or original results. Scope: teacher handout P3 pp. 3–5 and P5 pp. 8–9; this is technical verification only, not a review of the answer PDF or submission ZIP. The parent task confirmed that both required predictions were stated to the user before its verification runs.

## Input versions and environment

- Git HEAD: `d5fb4d0`; `src/` and `results/` are untracked. SHA-256: `src/p3.py` `572425d021d603deaf553c136e26a999690043af529191991b022a2843ccf6ae`; `src/p5.py` `27636fe419d3c156b4157049d8916e3ed27e677e30bd2b5aef834b328e104065`.
- Teacher PDF SHA-256 `77b4320e4bd3125a6b74dc8d17c7536b0b91b4a2bc1e47b983713e4fda1c6b35`; original `code_source.zip` SHA-256 `78bfb004a231838ffd60e136afad13aba6f61437790673edd950020b77e8721a`.
- P3 data SHA-256: `X.npy` `f22895ae8fa87b7b6676e5d17f9dd786a1f430339ecec491701df1ba58ec2605`; `y.npy` `89a5a7cb4656dde2bdc95d5eee18ac4b57b4019963f189d2dcd14fd4f3333677`; `theta_star.npy` `8760d230c909c4cf1811463ff9cd1206f7a64ce72aed3033f4050fd88fb8095e`.
- P5 original SHA-256: `train_data.mat` `8a8392ffbaab5f9ceaefc7b4f51c9f3b8bfe27c26d9faeda37f401d6e41b8890`; `test_data.mat` `d386ecb30c48f3ca1a0813d1e51e0912dfda633e667ab90de1dc690a60d5b507`.
- Baselines: `/usr/bin/python3` 3.14.4, NumPy 2.3.5, Matplotlib 3.10.7+dfsg1, CPU. MAT comparison: `/home/scarramcci/miniconda3/envs/lerobot/bin/python` 3.12.14, NumPy 2.2.6, SciPy 1.18.1. P3/P5 seed 0. Output directory: `results/verification/20260929-independent/`.

## Actual commands and exit states

Run from repository root. The full, absolute argument arrays and stdout/stderr/exit files are in `results/verification/20260929-independent/check_summary.json` and sibling files.

```sh
/usr/bin/python3 DDA5001_Machine_Learning/assignments/hw01/results/verification/20260929-independent/check.py
/home/scarramcci/miniconda3/envs/lerobot/bin/python DDA5001_Machine_Learning/assignments/hw01/results/verification/20260929-independent/check_mat_equivalence.py
/usr/bin/python3 DDA5001_Machine_Learning/assignments/hw01/results/verification/20260929-independent/check_p3_scaling.py
```

All three exited 0. `check.py` separately launched both baseline scripts with their default algorithm parameters and distinct `--output-dir`s; both child exits were 0. It passed the original P3 `.npy` data directory to `src/p3.py` and exact P5 `.npz` copies of the original `.mat` arrays to `src/p5.py`. The full commands are recorded in `check_summary.json`; direct stdout/stderr and child exit states are `p3.*.txt` and `p5.*.txt`.

## Passed checks

### P3, teacher handout pp. 3–5

- Independently evaluated the shifted Huber sum on the prescribed five residuals. At `mu=1`, total loss is `5.75`; at `mu=1e-5`, it is `5.75e-5`. At normalized residuals `[-2,-1,-0.5,0,0.5,1,2]`, the computed derivatives are `[-1,-1,-0.5,0,0.5,1,1]` for both `mu` values, including both branch boundaries.
- The five-row example gives sum gradient `[0.5,1.0]` and mean gradient `[0.1,0.2]`; the ratio is exactly the sample count 5. For direction `[0.6,0.8]`, the analytic sum directional derivative is `1.1`. Central differences at `h=0.1 mu` give `1.0999999999999988` for `mu=1` and `1.0999999999999994` for `mu=1e-5`. At `h=mu`, each gives `0.7625`, showing the large-step bias. The `h=1e-4 mu` absolute error is about `2.4–2.8e-12`. A second independently chosen three-row matrix passed a direct clipped-derivative formula check.
- Re-ran P3 with `mu=1e-5`, `alpha=0.001`, `T=1000`, seed 0. `regression_history.csv` has 1001 rows, including initial and final state. Its numerical columns and saved final Huber/least-squares weights match the prior baseline within stated NumPy tolerances. Least-squares estimation error `59.513636482981404`; initial Huber error `8.989939986199872`; final Huber error `5.618720155342013`; final sum loss `252724.64377596654`. The code loads `theta_star` only after optimization and does not pass it to gradient descent. The rendered `regression_error.png` was opened and visually inspected; labels, log scale, Huber curve, and least-squares reference are present.

### P5, teacher handout pp. 8–9

- SciPy loaded original MAT `zip` arrays of shapes `(7291,257)` and `(2007,257)`. Their NumPy copies are elementwise exactly equal with maximum absolute difference 0; see `mat_equivalence.json`. No test labels enter `train_pocket` or the pocket update; `src/p5.py` loads the test set after training.
- The seven-row toy trace, including initialization, matches an independent seed-0 replay of mistake selection, `theta + y*x`, strict improvement, and copied pocket weights. At update 2, current weights become `[0,-1,0]`, current training error falls from `0.5` to `0.25`, and the pocket changes to that vector. At update 3, current error rises to `0.5` and the pocket stays at `0.25`.
- The full trajectory has 2001 rows (initial state plus 2000 updates), 1669 selected training examples, and 434 selected test examples. Every row's current/pocket training and test error was recalculated from its saved weights and the feature formula; every chosen index and current update was replayed from the seed and current mistakes. Pocket training errors equal the running minimum of current training errors throughout and are nonincreasing. All saved weights match the original baseline within `1e-12`.
- Final current train/test errors: `0.040143798681845415` / `0.07142857142857142`. Final pocket train/test errors: `0.03235470341521869` / `0.06451612903225806`. Pocket test error increases at update 54 (`0.06682027649769585` to `0.06912442396313365`) and update 453 (`0.059907834101382486` to `0.06451612903225806`), consistent with the absence of a test monotonicity guarantee. The generated `error_curves.png` and `decision_boundaries.png` were opened and visually inspected; both classifiers, both feature labels, and the 1/6 points appear.

## Failed checks

None within this verification scope.

## Warnings and coverage limits

- No single available Python interpreter had all NumPy, SciPy, and Matplotlib dependencies. The full P5 baseline therefore used exact `.npz` copies of the MAT matrices; SciPy separately verified the copies against teacher originals. The default no-argument `python p5.py` invocation was not independently run in one unified environment.
- The numerical directional check samples finite directions and steps; it does not prove the gradient for every possible input. Static code inspection found no hard-coded baseline result or local absolute path. Plots were visually checked, not compared pixelwise.
- This conclusion is bound to the above source and data hashes. Any later source or input change requires affected checks to be repeated. The answer PDF, AI case text, and final ZIP still require a separate Reviewer.

## Required fixes

None for the checked P3/P5 code or outputs. Before claiming full submission readiness, the Report Writer/Reviewer should inspect the completed PDF and actual ZIP against handout p. 1 and P3/P5 case limits.

Next role: Report Writer, then a distinct Reviewer. Evidence: scripts, logs, JSON, CSV, and PNG under `results/verification/20260929-independent/`.
