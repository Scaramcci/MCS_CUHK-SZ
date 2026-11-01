# Independent technical verification — HW3

Verifier / executor: `/root/verifier`, independent child agent; did not implement the submitted code. Date: 2026-10-29 (Asia/Shanghai). Target: `DDA5001_Machine_Learning/assignments/hw03`. Verdict: **independent technical checks passed for the source version below**. No implementation fixes required. This is not final report/package approval.

Read root README/AGENTS, course README, assignment README, plan and implementation handoff, role instructions, all seven original PDF pages (text and rendered images), and the three teacher frameworks/dependency files inside `requirements/code_source(2).zip`. No nested AGENTS/override rules were found under this course. Branch remained `master`; HEAD `26cf2eeb639a79d622cee5c0f5ee40d83f54809b`. Implementations are uncommitted files. The user's prior replacement/deletion of HW1 materials was not altered.

## Checked version and evidence

| File | SHA-256 |
|---|---|
| src/p1/p1.py | 3f51f39fb81f42996a16a336714ea9120f8980ca1473772638ee4d05c4425442 |
| src/p2/p2.py | 97405f76831d4338625a19333837eb611863e806ca39d1fabaff8e9f5694f93c |
| src/p3/p3.py | 0ad492caf80f85c8df91f0604130bab48168f7816d4c7fb56e825b96215099e1 |

Evidence directory: `results/verification/independent-20261029/`. `checked-source-sha256.json` records the inputs; source hashes were rechecked after execution. `commands.json` contains actual full experiment/test argv, UTC start/end times and exit codes; stdout/stderr are separate per command. `checks.json` contains independent assertions and measured values; `todo-only.diff` records the complete teacher-to-completed diff. `environment-and-mnist.json` records hardware, runtime and dataset checks. `verify.py` and `run_verification.py` retain the executable independent checks.

Fresh environment: Python 3.12.14, Linux x86-64, CPU only, one numerical thread. Created a new `.venv` under the evidence directory, with `include-system-site-packages = false`; installed **all** packages from `results/environment/requirements-frozen.txt`. Independent `pip freeze` matches that file exactly, including NumPy 2.2.6, Matplotlib 3.10.6, Pillow 12.3.0, torch 2.8.0+cpu and torchvision 0.23.0+cpu. Inherited `PYTHONPATH`/`PYTHONHOME` were removed for test/experiment subprocesses; matplotlib/cache and bytecode settings isolated runtime writes from source. Training uses the supplied deterministic CPU configuration, seed 666, 30 epochs, batch 128, SGD momentum 0.9, learning rate 0.1, weight decay 0.

From assignment root, actual setup commands were:

```bash
.venv/bin/python -m venv results/verification/independent-20261029/.venv
results/verification/independent-20261029/.venv/bin/python -m pip install --cache-dir .cache/pip --extra-index-url https://download.pytorch.org/whl/cpu -r results/environment/requirements-frozen.txt
results/verification/independent-20261029/.venv/bin/python results/verification/independent-20261029/run_verification.py
```

The first network-restricted installation could not resolve hosts and was interrupted (exit 1; `install.log`). Repeating the exact install with approved network access succeeded (exit 0; `install-network.log`). The runner performs full p1/p2/p3 CLI runs with their only adjustment being `--output-dir` to the isolated directory; all three exited 0. The author's five unittest checks were rerun independently and exited 0. Independent checker attempt 1 exited 1 due to a verifier test defect documented below; corrected attempt 2 exited 0 (`independent-checks-attempt2-command.json`). Original experiment outputs were never overwritten.

## Passed checks

- **Scope / provenance (PDF pp3,5,6–7):** byte-level sequence comparison against ZIP shows exactly eight replacements, each replacing only an original `raise NotImplementedError` line. All remaining framework text and three requirements files are unchanged. All 403 teacher data files (400 faces, 2 CSVs, 1 split NPZ) exactly match the ZIP. All 411 actual input-file SHA-256/size entries match the author's input manifest. All four MNIST gzip MD5s match the reference checksums embedded in installed torchvision's MNIST implementation. Input data were reused read-only; independence covers reproduction from verified local inputs, not redownloading the same data.
- **P1 (PDF pp1–3):** independent augmented least-squares oracle checks final ridge coefficients across 1x1, underdetermined 3x7, and full-rank 19x4 problems with four positive regularization strengths. Explicit constant-feature test confirms the intercept penalty and mean-loss scaling. All 80 validation scores independently recomputed using the prescribed original row IDs; maximum absolute discrepancy from framework scores was `3.1264e-12` (within prespecified `rtol=1e-10, atol=1e-12`). Shuffled records with three exact tied candidates choose the smallest candidate. Whole-task reproduction selected lambda `0.01`, CV MSE `0.048267369324067146`. Baseline training/test MSE `0.0009043599379464498 / 2.080033928388329`; selected fit `0.009333970557656815 / 0.0402130755155398`. Static dataflow inspection confirms test data only enter final evaluation; no test-based selection.
- **P2 (PDF pp4–5):** every one of 400 image columns checked against its original ordered normalized image. A noncontiguous synthetic image tensor separately checks C-order flattening. Actual X shape 10304x400, mean 10304x1, thin U 10304x400, s length 400; orthonormality and descending singular values checked. Coordinates and reconstructions verified for k=20,100,400; whole-data residual MSE agrees with discarded singular-value energy (`rtol=1e-10, atol=1e-20`). MSEs are `0.007347315824327826` and `0.0027157677082419646`; full-basis numerical residual MSE `1.0600e-31`. Explicit synthetic values outside [0,1] remain unclipped. Actual k=20 reconstructions also include negative values and k=100 values exceed 1, consistent with clipping only display copies.
- **P3 (PDF pp6–7):** exact leaf types, dimensions, all biases, counts A=7850/B=C=50890, empty/singleton/17-item batches, and raw negative output logits checked. B numerically agrees with collapsed affine map in float64 (`rtol=1e-11, atol=1e-12`); a deliberate parameter setting confirms C can have a non-affine response. Fixed sizes 6000/2000/2000, train/validation disjointness, unique indices, balanced classes and [0,1] float32 pixel normalization checked. Framework compares regenerated seed-666 indices with supplied NPZ. Static inspection confirms checkpoint selection accesses train/validation only, restores best state, excludes epoch 0, freezes model choice before any test evaluation. Each selected epoch is independently recomputed from all 30 trained-epoch validation losses.
- **Full reproduction:** all numerical P1/P2 summaries/tables, P3 summary/selection and all three 31-point histories match original outputs **byte-for-byte**. All six generated PNGs also match byte-for-byte. Runtime-only fields such as elapsed wall time were not required to match. P3 selections reproduce A epoch 9 (validation CE 0.3183, test CE 0.2772, accuracy 91.45%); B epoch 4 (0.3366, 0.2901, 90.80%); C epoch 14 (0.1862, 0.1705, 95.20%). Validation selects C.
- **Visual inspection:** independently viewed the two required P1 plots (log lambda axis; mandated fit bounds), 4x4 eigenface grid, 5x3 reconstruction grid for subjects 1–5/image 1, and two-panel P3 CE plot with A/B/C in both panels. These are consistent with the numerical outputs and supplied plotting routines.

Numerical tolerances above and ridge coefficient `rtol=1e-8, atol=1e-9`, orthonormality `1e-12`, full-basis reconstruction `1e-11` were specified in the independent script before its first run. They accommodate floating-point differences between equivalent linear algebra methods; none was loosened after failure. Same-environment reproduction used the stronger exact-byte comparison.

## Failed checks and resolutions

No outstanding implementation failures. The verifier's first script wrongly assumed that the **maximum** k=20 reconstruction pixel must exceed 1 to prove no clipping. It was actually `0.9946367539024328`; the minimum was `-0.17465045165088328`. This dataset-specific assertion was unjustified. The failed script is preserved as `verify-attempt1.py`, along with its original stdout/stderr. Only the verifier test was replaced with an explicit synthetic full-basis reconstruction containing -2,3,4,-5 and an exact equality assertion. Attempt 2 then passed all checks. The implementation and experiment output files were not changed or rerun for this test correction.

## Warnings / coverage limits

- This verifies the three implementations, real experimental outputs, and reproducibility on the present CPU/runtime. It does not certify bitwise identity on other hardware/library versions or predictive robustness across seeds; the teacher prescribes one seed.
- Matplotlib's teacher-pinned version emits pyparsing deprecation warnings during unittest execution; tests/figures still pass. Installation also saw unrelated ROS package warnings from inherited host `PYTHONPATH`; the actual verified subprocesses removed it and used an exact frozen environment.
- Generic inputs outside the supplied function contracts (e.g. missing CV records, unsorted candidates) are not assignment requirements. The supplied ascending candidate/complete-record contract is preserved.
- Mathematical/prose authorship and student understanding cannot be certified by automated verification. The PDF asks the student to write explanations in their own words and check generated code (p1). Report and actual collaboration disclosures must be checked by the student and independent Reviewer.
- Final report and submission package were not yet the verification target. This note does not approve either; later source changes invalidate the affected technical checks.

## Required fixes and next role

**Required implementation fixes: none.** Hand off to Report Writer for source-grounded explanations and to a different independent Reviewer for the actual final PDF/ZIP, submission completeness, numerical consistency, visual layout and truthful P3(d) interaction disclosure. Reviewer must inspect the assembled candidate, not infer package correctness from these source checks.
