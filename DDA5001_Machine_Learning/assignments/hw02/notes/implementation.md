# Implementation record

Role / executor: Implementer, coding subagent `/root/implementer`.
Date: 2026-10-27. Repository branch: master. Input HEAD:
`b02d5732be2b1bc074217fb236ca882b594e432d`; all hw02 implementation files
remain uncommitted. No branch/worktree, Git staging, commit or push performed.

## Scope and input

The coordinating agent assigned the eight teacher stubs plus two small standalone
verification scripts. Read root README/AGENTS, course README, agents README and
Implementer role, `notes/plan.md`, the entire teacher PDF, and all nine teacher
source text files. Viewed PDF pages 3, 4, 6 and 7 for the update and coefficient
formulas. No course/assignment AGENTS, hw02 README or requirements directory
existed when the coordinator began; the coordinator now owns the new README.

Sources: teacher PDF p3 P2 optimizer definitions, p4 P2 implementation and checks,
p6 P3 least squares/orthogonality, p7 P3 function shapes and verification.
The teacher source ZIP and PDF are untouched. Only the assigned implementation,
verification and implementation-note paths were written by this subagent.

## Implementation summary

- P2 softmax subtracts each row maximum before exponentiating. Cross entropy
  uses shifted log probabilities directly, avoiding log of an underflowed zero.
  The gradient is `X.T @ (softmax(X @ theta) - one_hot) / n`, with one parameter
  column per class. Updates allocate their outputs. Momentum takes one gradient
  at the current parameter; Nesterov takes one at the extrapolated parameter.
- P3 uses `np.linalg.lstsq(..., rcond=None)[0]`; the stable solver handles each
  label column independently. The population error zero-pads the degree axis,
  includes both model/target tails, and sums squared raw Legendre coefficient
  differences with weights `1/(2*k+1)`. The provided target is already normalized.
- `p2/verify.py` reports the prescribed 3x3 analytic/central-difference matrices,
  captured gradient points and update matrices, stable-loss checks, the first
  update equivalence, and input nonmutation.
- `p3/verify.py` reports both noiseless fits, independent 80-node quadrature,
  density and tail checks, no repeated normalization, and batched column results.
  Both accept `--output` and default to JSON on stdout, work from any cwd, and
  exit nonzero if an included numerical assertion fails.

## Changed files and exact hashes

| File | SHA-256 |
|---|---|
| src/p2/algorithms.py | f3dff6c0408536b60731cb55c4f1e3237ddd234ed75c28359045acf45f78af96 |
| src/p3/algorithms.py | b05e25fa40cf890404693e2a15cc573ed26dabbdccee2c0894fc58900a97f4d7 |
| src/p2/verify.py | e53d23cb855612ad3df79022d8932fa6132458c009161ee9ffc25a73fb558a81 |
| src/p3/verify.py | 83905ae5b16a1bf9506eb6e1e5c89a8f5c56223426af2f53c5c1838101efd719 |

Also wrote `notes/ai-initial-response.txt` as the actual implementation reply
sent to the coordinator, and this record. The interaction is agent-to-agent;
it is not represented as a student-authored mathematical explanation.

## Environment and actual commands

Used hw02 `.venv312/bin/python`: Python 3.12.14, NumPy 2.2.6 and the teacher's
exact requirements. The coordinator owns environment installation details;
its first Python 3.14 attempt could not install the pinned SciPy wheel.

Each command was run through `notes/run_record.py` with a fresh evidence directory,
capturing actual cwd, argv, source hashes, UTC start/end, duration, exit status,
stdout and stderr. Absolute paths in those records identify this local run; the
submitted code itself has no machine-specific paths. The runner's static
`recorded_by` field names the coordinating agent; the actual invoker for these
six records was `/root/implementer`.

| Record below results/implementation-tests/ | Working directory | Actual command after wrapper | Exit |
|---|---|---|---|
| baseline-p2 | hw02/src | ../.venv312/bin/python -m unittest discover -s p2 -v | 1 |
| baseline-p3 | hw02/src | ../.venv312/bin/python -m unittest discover -s p3 -v | 1 |
| public-p2 | hw02/src | ../.venv312/bin/python -m unittest discover -s p2 -v | 0 |
| public-p3 | hw02/src | ../.venv312/bin/python -m unittest discover -s p3 -v | 0 |
| checks-p2 | /tmp | hw02/.venv312/bin/python hw02/src/p2/verify.py --output hw02/results/implementation-tests/checks-p2.json (absolute paths) | 0 |
| checks-p3 | /tmp | hw02/.venv312/bin/python hw02/src/p3/verify.py --output hw02/results/implementation-tests/checks-p3.json (absolute paths) | 0 |

These six runs occurred before the coordinator advised removing system
`PYTHONPATH`; subsequent coordinator/independent checks use `env -u PYTHONPATH`.
No full experiment was run by this subagent.

## Actual self-test evidence

Before editing stubs, P2 ran 7 tests with 7 NotImplemented errors; P3 ran 8 tests
with 7 NotImplemented errors (the independent framework check already passed).
These failures remain in baseline logs. After implementation P2 passed all 7
public tests and P3 passed all 8. These are author self-checks only.

The numerical JSON outputs were actually produced on 2026-10-27:

- P2 central-difference step `1e-6`; maximum gradient difference
  `1.1740114436165072e-10` (< `1e-8`).
- Momentum and Nesterov each made one gradient call. Gradient points matched
  theta and theta+0.008 exactly; both update maximum differences were
  `2.7755575615628914e-17` (< `1e-14`). Extreme wrong-class CE = 2000 exactly.
- P3 noiseless coefficient maximum differences: degree 2,
  `1.2212453270876722e-15`; degree 10, `2.4980018054066022e-15`.
  Their computed clean risks are `3.0239668033472117e-31` and
  `6.494789046837465e-30` (expected zero).
- P3 quadrature computed `0.28419047619047905`; analytic weighted sum computed
  `0.2841904761904762`; absolute difference `2.831068712794149e-15`.
- P3 batch (40,5) design and (40,3) labels yielded a (5,3) fit; maximum known
  coefficient difference `2.677705344252733e-16`; separate-fit difference
  `2.220446049250313e-16`. Batched risks matched [0.3613333333333333, 1.08].
- Byte comparison against the original ZIP confirmed both frameworks, both
  runners, and both supplied public test files are unchanged.

## Handoff and outstanding work

Implementation is stable at the hashes above. Next: coordinator runs full fixed
experiments and retains data locally; independent Verifier inspects the stable
source and reruns checks; report author uses real numerical JSON and experiment
results; independent Reviewer checks the exact final package. No independent
verification, full-experiment result, final report approval or package readiness
is issued by this Implementer record.
