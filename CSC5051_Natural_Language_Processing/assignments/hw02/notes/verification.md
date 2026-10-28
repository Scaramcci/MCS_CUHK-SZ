# Independent scaffold verification

Date: 2026-10-28, Asia/Shanghai.
Role / Executor: Verifier, `/root/verifier`; did not participate in implementation.
Target: CSC5051 Natural Language Processing, hw02, Task 3.
Verdict: **PASS for the requested offline foundation scaffold only.**
This is not verification of the complete assignment or readiness for submission.

## Inputs and exact version

Read root README/AGENTS and role/workflow instructions, course/assignment README,
[plan](plan.md), [source review](research.md), [implementation handoff](implementation.md),
all authored source/config/prompt/test files and the English report outline.
No narrower course/assignment/assignments AGENTS or override files were present.
Read all four PDF pages as extracted text and visually inspected p. 3, including
Task 3's D-to-D' requirement. Read relevant notebook cells 20–25 with credential
redaction; did not execute the notebook or inspect its output as experiment evidence.
The existing singular `requirement/` contains the PDF and notebook; no separate
`requirements/` is needed. The teacher's Overleaf source is unavailable locally.

Repository base: `0f4a40736f0af5ab23a55b50af6229de7cdaef66`, `master`.
The work is uncommitted. All 14 entries in the Implementer's frozen manifest
matched before and after verification. The independently computed copy is
[verified-input-hashes.json](../results/verification/20261028-scaffold/verified-input-hashes.json).
Original PDF hash: `bf09fbc9f382a149804a7977a6cc63912efa93520c56d4c7fe7c51260e64aa5f`.
Original notebook hash: `5a396a71600492e39974d51ee7a2e6c5bf020242896dd37db88fcae2310c26e9`.
Both match the source review. The real `.env` contents were never read or logged.

Applied `using-research-workflows` and `validating-implementations` in Direct mode.
Repository/user rules take precedence for report location, no branch creation,
limited scaffold scope, and no full-assignment Ready conclusion.

## Passed checks

Fresh evidence: [run.json](../results/verification/20261028-scaffold/run.json),
[verification runner](../results/verification/20261028-scaffold/verify.py), and its
numbered stdout/stderr files. `run.json` records runtime, platform, timestamp,
actual argument vectors, working directories, expected and actual exits.

From the repository root, executed:

```bash
python3 CSC5051_Natural_Language_Processing/assignments/hw02/results/verification/20261028-scaffold/verify.py
```

Actual exit: 0. Output: `PASS: 14 subprocess checks; independent boundary interception; originals and frozen manifest unchanged.`
The runner used Python's standard library, no dependency installation, random
operations, GPU, network or real API requests.

| Check | Expected and actual exit / outcome |
| --- | --- |
| `python3 src/main.py check` from hw02 | 0; three templates load without dataset/API |
| Each documented preview for zero_shot, few_shot, chain_of_thought | 0 each; explicit template-only label and unfilled record slots |
| `python3 src/main.py run` with a synthetic key and budget | 2; explicit refusal |
| `python3 tests/offline_smoke.py` | 0; author's smoke suite independently rerun |
| Absolute main.py path from verification directory | 0; resolution independent of cwd |
| Unsupported method `not_a_method` | 2; argparse refusal |
| `git check-ignore .env` | 0; local credentials ignored |
| `git check-ignore .env.example` | 1; example trackable |
| Ignore check for future data, local raw outputs and original notebook | 0; each specified path printed as ignored |
| Isolated malformed JSON and wrong top-level JSON type | 1 each; generic error without leaking values |
| Isolated missing prompt | 1; generic error |

An additional independently written in-process check blocked `.env` reads,
socket creation, DNS, and subprocess launch while running check, all three
previews, and run with a synthetic key/budget. All returned their expected
status and emitted no sentinel key. The isolated `.env` was synthetic; the real
one was not copied. Static inspection confirms no client/network path exists.
The actual local `.env` exists with mode 0600 (metadata-only inspection).

Manual code/document assessment: techniques are distinguishable and traced to
course notebook cells 20–25; they share one rubric and output contract.
Few-shot examples are labelled hand-authored illustrations, and the draft
rubric/seed/threshold are not represented as teacher mandates or validated
choices. Agent function raises NotImplementedError and documents the deferred
observation/decision/action/feedback/stop contract. README clearly states the
three templates are not yet experimentally validated. English outline contains
no measured results. No final PDF or submission directory exists.

## Failed checks

None in the tested scaffold acceptance scope. No implementation files were changed.

## Warnings and coverage limits

- No dataset acquisition, filtering, labels, evaluation split, API authentication,
  provider compatibility, spending controls, actual model comparisons, adaptive
  agent execution, experimental results or full report was tested or claimed.
  These are intentionally absent at the user's current scaffold-only request.
- The CLI validates essential scaffold keys/template substitution, not a complete
  experiment schema or model output. Later execution needs stronger validation.
- Compatibility was executed only on the Python/runtime recorded in run.json;
  no separate Python 3.8 interpreter compatibility run occurred.
- The original notebook remains unchanged and ignored because the prior source
  review found a potential credential. It must remain local unless sanitized into
  a separately reviewed copy. No value was reproduced here.
- Source-page rendering was a visual requirement check; it is not an experimental
  screenshot or report result. Notebook's remotely linked illustrative image was
  not fetched; relevant technique text/code was reviewed locally.
- Editing/using the actual `.env` and the future live workflow remain for the next
  phase. No user manual-test completion is assumed.

## Required fixes and next role

No required scaffold fixes. Maintain the frozen authored version while the
separate Reviewer assesses scope and evidence. The Reviewer must be a different
agent from this Verifier and the Implementer. After future implementation,
repeat affected independent verification and review; final package review must
inspect the eventual exact submission files.

References: [plan](plan.md), [implementation](implementation.md),
[research](research.md), [assignment PDF](../requirement/Assignment_2.pdf),
[README](../README.md).
