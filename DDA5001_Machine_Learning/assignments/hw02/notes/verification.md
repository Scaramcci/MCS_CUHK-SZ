# Independent technical verification — HW2

Verifier: independent subagent `/root/verifier`, 2026-10-27 (Asia/Shanghai).
I did not implement the submitted functions, author verification scripts, or write
the report. Scope: frozen `src/`, fixed experiments and their evidence. I wrote
only this record and `results/verification/20261027-independent/` (abbreviated V
below). No production file, original, report, main result or submission was edited.

**Verdict: independent technical checks passed for the hashes and coverage below.**
This does not approve the final PDF, student understanding/wording, or an as-yet
unreviewed ZIP. Next role: a different independent Reviewer must inspect the actual
final package and report after assembly.

## Inputs and version

Branch `master`; HEAD `b02d5732be2b1bc074217fb236ca882b594e432d`;
hw02 implementation is uncommitted. Read root README/AGENTS, course README,
`agents/README.md`, `agents/verifier.md`, hw02 README, complete plan and
implementation handoff, all nine teacher source files, both added verify scripts,
and the seven-page teacher PDF. All seven PDF pages were rendered and visually
inspected, including optimizer formulas on p3, numeric examples on p4, Legendre
normalization on p5-6 and grid/shapes requirements on p7. No lower-level course or
hw02 AGENTS/override files or requirements directory existed.

- P2 algorithms SHA256: `f3dff6c0408536b60731cb55c4f1e3237ddd234ed75c28359045acf45f78af96`.
- P3 algorithms SHA256: `b05e25fa40cf890404693e2a15cc573ed26dabbdccee2c0894fc58900a97f4d7`.
- P2 verify SHA256: `e53d23cb855612ad3df79022d8932fa6132458c009161ee9ffc25a73fb558a81`.
- P3 verify SHA256: `83905ae5b16a1bf9506eb6e1e5c89a8f5c56223426af2f53c5c1838101efd719`.
- Original PDF: `f131d01bcbeb286b0cbc978be38d4978e2a7e0f9bab8e697e9332b8ddcd8920e`.
- Original ZIP: `6f58949e6ef4ac1dce1857d3373fc804aee34c0b431a307deee26d08dedd32b4`.
- Dry Bean CSV: `c91a086bb4357e69409d23287ec22be1be9512145cead1d8ca988c918be38fcb`.

Complete frozen input hashes: V/input-hashes.json. Direct comparison against ZIP
member bytes: V/original-comparison.json. All seven fixed framework, runner,
public-test and requirements files are unchanged; only the two algorithms files
differ from the original nine text files. Live source hashes still matched the
snapshot after reproduction and independent checks.

## Environment and actual commands

Created a new venv in V/venv with the bundled Python 3.12.14, and installed only
from local wheels using `pip install --no-index --find-links local_artifacts/wheels
-r results/requirements-frozen.txt`. The resulting `pip freeze` exactly equals
the specified frozen dependencies (including NumPy 2.2.6, SciPy 1.15.3,
scikit-learn 1.7.2 and matplotlib 3.10.6). Isolated source copy: V/src.
All Python calls used `env -u PYTHONPATH`; Python bytecode writing was disabled
and plotting cache redirected inside V. CPU runs use the unchanged framework's
one numerical-library thread; no GPU, network download or external service used.

Each table command is prefixed `env -u PYTHONPATH`. `P` means the absolute
V/venv/bin/python path. The run records store full absolute argv, cwd,
UTC timestamps and exit status; logs are sibling `.stdout.txt`/`.stderr.txt`.

| Evidence prefix under V | Actual command after env prefix | Exit |
|---|---|---:|
| create-clean-env | bundled/python3 -m venv V/venv | 0 |
| offline-install | P -m pip install --no-index --find-links hw02/local_artifacts/wheels -r hw02/results/requirements-frozen.txt | 0 |
| clean-freeze | P -m pip freeze | 0 |
| p2-tests (cwd V/src) | P -m unittest discover -s p2 -v | 0 |
| p3-tests (cwd V/src) | P -m unittest discover -s p3 -v | 0 |
| p2-verify | P V/src/p2/verify.py --output V/p2-checks.json | 0 |
| p3-verify | P V/src/p3/verify.py --output V/p3-checks.json | 0 |
| p2-full | P V/src/p2/run.py --data-dir hw02/data --output-dir V/p2-full | 0 |
| p3-full | P V/src/p3/run.py --output-dir V/p3-full | 0 |
| independent-final | P V/independent_checks.py | 0 |

Full P2 ran 19:02:37–19:02:44 local, full P3 19:02:44–19:02:50.
The final independent checks have their own exact UTC timestamps in
V/independent-final.run.json. Full reproduction took approximately 6.2 seconds
per problem on this host; these are actual full fixed runs, not smoke tests.

## Passed checks

1. Public tests freshly passed **P2 7/7 and P3 8/8** in the clean environment.
   Both added verification scripts passed; P2 required central difference maximum
   was `1.1740114436165072e-10` at step `1e-6` (threshold `1e-8`). Accelerated
   update differences were `2.7755575615628914e-17` (threshold `1e-14`).
   P3 required noiseless degree-2/10 coefficient differences were
   `1.2212453270876722e-15` / `2.4980018054066022e-15`; analytic error
   `0.2841904761904762` vs quadrature `0.28419047619047905`.
2. Independent tests, implemented solely by this Verifier in
   V/independent_checks.py, passed eight check groups. Evidence:
   V/independent-checks.json and V/independent-final.*.
   - Random P2 shapes, sample permutation, zero class-sum gradients, singleton
     class, read-only/noncontiguous arrays and logits of magnitude `1e100`.
     Largest new finite-difference discrepancy `7.176753358262289e-10`;
     threshold `2e-8` absolute plus `1e-6` relative.
   - Nonlinear oracle `G(A)=sin(A)+A^2` for Nesterov k=1,2,3,999 and momentum;
     exactly one gradient call at the prescribed point, error within `1e-14`.
   - Independently rebuilt both datasets from raw inputs: first-occurrence exact
     deduplication, stratified seed-666 80/20 split, training mean/population
     standard deviation, constant column and labels all exactly matched.
     Digits: 1437/360, 0 duplicates; Bean: 10834/2709, 68 duplicates.
   - Instrumented all three optimizers for 1000 updates on a fresh synthetic
     verification-only dataset. Every call saw the training arrays, no test data.
     Replacing all test features/labels left trained parameters and training
     histories bitwise identical; iterations were exactly 0,5,...,1000.
   - Five randomized batched Legendre error cases with model/target degrees
     through 50 and differing tails, plus minimal full-rank noiseless fits for
     degrees 0,2,10. Read-only inputs unchanged. Maximum discrepancy from 80-node
     Gauss-Legendre quadrature `2.9665159217984183e-13` (threshold `1e-10`);
     maximum coefficient recovery error `1.7763568394002505e-15`
     (threshold `1e-11`). Scalar/batch symmetry and independent columns passed.
3. Full P2 reproduction: all six final parameter arrays, all six 201-record
   training histories and summary CSV exactly equal main results. Full manifests
   equal (there is no elapsed-time key in P2 manifest). Fixed parameters match
   PDF p3 and original framework; no regularization, autodiff, classifier or
   ready-made optimizer used. Every method resets to zero.
4. Full P3 reproduction: all raw arrays (`rho_q` 1000×21×50,
   `rho_v` 1000×21×41, both Q20 risk arrays), all grid arrays, both CSVs and
   summary JSON exactly equal main results. Manifest identical except elapsed
   time. Verified all **1,911,000 cell-trial observations**, all finite, no
   rejected trial. Means exactly equal arithmetic means of retained raw arrays;
   common Q20/variance-.1 grid cells and `risk10-risk2` match exactly.
   Main and reproduction both report max nested training-error violation 0.
5. All eight regenerated PNG artifacts are byte-identical to main plots;
   V/plot-comparison.json records hashes. Independently viewed both composite
   figures: P2 panels have the six prescribed train/test curves with log loss;
   P3 axes, diverging colors and zero contour match the fixed grids. No
   visual defect observed in those composites. Final report layout remains
   the independent Reviewer's responsibility.

## Failed checks

No product check failed. One verification-harness bookkeeping defect occurred
*after all eight clean-room commands had completed successfully*: the initial
ZIP enumeration mistakenly attempted to compare Apple's `__MACOSX/._requirements.txt`
as source. It raised FileNotFoundError; it did not affect any product run.
I corrected only my own harness's metadata filter, reran the source audit in
V/independent_checks.py and the final checks (exit 0), and retained the successful
individual run records. No production repair was needed. This harness issue is
not presented as a student/code bug or an implementation revision.

## Warnings / coverage limits

- Exact reproduction is established on this CPU/OS and pinned environment;
  cross-platform BLAS changes can cause small floating-point differences.
- P3 genuinely has very large rare errors: maximum raw rho in the two grids
  `430779710.57433844` and `1716522871.6084874`; maximum means
  `1032363.1270027878` and `4812315.95548877`. No clipping, filtering or
  regularization was introduced. Display saturation ±.25 must not be described
  as a bound on risks or as eliminating Monte Carlo uncertainty.
- The contract requires matching 1-D inputs or matching 2-D batched inputs.
  Invalid shapes, infinities/NaNs and mixed 1-D/2-D broadcasting are outside
  the stated contract and were not certified.
- My synthetic inputs are isolated verification examples, not replacement
  experiment data. All required full experiment data/settings remain original.
- Mathematical report derivations, the one-page AI case, student understanding,
  final ZIP completeness and final PDF visual QA were not approved by this role.
  No upload, Git commit or push was performed.

## Required fixes / next role

No required technical fix for this source version. The coordinator should retain
truthful disclosure of agent assistance and avoid overstating P3 finite-trial
contours. A different Reviewer must inspect the actual final PDF and ZIP against
teacher p1-7, verify package/source equality and approve only the version reviewed.
Any source change invalidates the affected technical conclusion and requires
reverification; any candidate edit requires renewed package review.

References: `notes/plan.md`, `notes/implementation.md`, original PDF p1-7;
full evidence under `results/verification/20261027-independent/`.
