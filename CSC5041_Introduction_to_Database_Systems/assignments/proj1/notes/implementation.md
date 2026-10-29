# Implementation and self-test handoff

- Executor: main Codex agent `/root`, author of `src/proj1.sql` and supporting scripts. Self-test only, not independent verification.
- Date: 2026-10-28 (Asia/Shanghai); evidence timestamps are UTC.
- Inputs: original project package; see README for source hashes and `notes/plan.md` for page-level requirements.
- Implementation: ten SQL view definitions with CTEs and grouped aggregates. No solution functions, expected-result-table access, hardcoded answer rows or database-specific file paths.
- Environment: PostgreSQL 18.6 on local Ubuntu/Linux x86_64; local socket authentication. No credentials stored. CPU execution; seeds/GPU N/A.

## Actual runs

| Evidence directory under `results/selftest/` | Result |
| --- | --- |
| `20261028T135008766277Z-import-teacher-data-0efb39` | Initial strict import failed with extension ownership error; transaction rolled back. |
| `20261028T135051926964Z-prepare-import-0c6b34` | Generated derived import with only the extension COMMENT omitted; source/output hashes recorded. |
| `20261028T135054614024Z-import-compatible-data-649e73` | Full prepared dump imported with ON_ERROR_STOP and one transaction; exit 0. |
| `20261028T135110913821Z-baseline-checks-178fb1` | Teacher checker loaded; all ten solution views absent as expected before implementation. Also observed no duplicate subject-code/semester course offerings in teacher data. |
| `20261028T135245575147Z-solution-v1-bdb582` | Ten views loaded in one transaction; Q1–Q10 all `correct`; actual full retrieval and interfaces recorded, exit 0. |

Each directory contains exact argv, source/input SHA-256, elapsed wall time, exit status, stdout and stderr. Command working directory is the assignment directory. The prepared import hash is linked through the preparation run.

## Self-test measurements

Complete result retrieval in Q1–Q10 order (milliseconds): 2.492, 11.863, 3.040, 0.305, 9.112, 0.579, 123.515, 17.727, 9.718, 18.903. These are measurements from one local run, not performance guarantees. All statements were subject to a 120-second timeout. Teacher `check_all()` took 487.329 ms.

Column inspection confirmed all template names, integer counts for Q5/Q6, numeric(4,2) for Q7, numeric rates for Q8/Q10 and the domain types inherited from teacher tables.

## Handoff to independent Verifier

Read `src/proj1.sql` with the teacher PDF. Independently reproduce a one-pass load into a fresh database, with and without check.sql already installed. Run original checks and independently designed boundary tests. Pay special attention to ties, NULL marks, distinct building counts, role joins, exact ranking before rounding, >10/>150 thresholds, and subject version identities. No source edits are allowed during verification; report required repairs to the author.

Known specification limitations: Q7 cannot represent 100.00 under the mandated numeric(4,2) type; Q8 zero-baseline percentage growth is undefined; Q10 zero-marked-student fail rate is undefined and represented as NULL. The AI-policy restriction is recorded in README, and no course-policy compliance is claimed.

## Subsequent handoff and candidate assembly

Independent Verifier `/root/verify_proj1` completed its own checks and wrote [verification.md](verification.md). The author has not altered that record. Verified source SHA-256: `3c5f06abbca9b49f4984df3b2de4c4f1d33adc74ca20f7f3f47c6e3a6880c3c9`.

The main agent copied those exact bytes to the named candidate in `submission/`, after verification completed. See `results/submission-manifest.json` for the exact name, size, hash, assembly timestamp and input verification-record hash. Separate Reviewer `/root/review_proj1` then inspected the actual candidate and wrote [review.md](review.md), with separate technical-readiness and course-policy findings. The author has not edited either independent record or changed the SQL after verification/review.

## Completion and remaining limits

Planned technical implementation, recorded self-tests, independent verification, candidate assembly and independent final-file review are complete. No further SQL repair was requested by either independent role. No manual user test, teacher-policy waiver, Moodle upload, Git commit or push is claimed. The documented specification ambiguities and AI-policy limitation remain; they were not silently converted into passing checks.

Repository maintenance: two data paths were removed only from the Git index after local hash-verified backup; both originals remain present, and history is unchanged. See `results/maintenance/20261028T135559Z-local-data-backup.json`. The prepared import workaround is the only environment adaptation; source and submission have no dependence on Python or that workaround once teacher data is installed.
