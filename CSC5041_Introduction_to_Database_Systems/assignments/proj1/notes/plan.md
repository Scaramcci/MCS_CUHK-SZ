# Project 1 implementation plan

- Date: 2026-10-28 (Asia/Shanghai)
- Planner / Implementer: main Codex agent `/root`.
- Scope: complete Q1–Q10, run actual PostgreSQL tests, obtain independent technical verification and a separate final-file review. No upload or Git commit/push.
- Base repository version: `037368d345026e4fe5c3e1a53a31b9f931853f78`; work directly on `master` under the repository rule.
- Inputs: original files in `project_release_to_students/`; all originals remain unchanged.

## Current state and intended result

The teacher's `proj1.sql` contains ten empty view declarations. Local PostgreSQL 18.6 is running; the user's `proj1` database is empty and owned by the current user. Produce `src/proj1.sql`, a single self-contained plain-SQL file retaining the ten declared interfaces, and an exact named copy in `submission/` after verification. PostgreSQL 18.6 is the tested environment, not a teacher-mandated version. No report is required.

## Requirements and acceptance mapping

Source for all question requirements: `project_release_to_students/proj1.pdf`, section 6.

| Question | Page | Required behavior | Check |
| --- | --- | --- | --- |
| Q1 | 2 | Direct CSE offering, PG subjects, UOC > 6, subject codes | `check_q1()`; direct vs indirect offering |
| Q2 | 2 | Studio classes in at least three distinct buildings | `check_q2()`; distinct building threshold |
| Q3 | 2 | Distinct staff teaching Hemma Margareta | `check_q3()`; duplicate teaching/enrolment paths |
| Q4 | 2 | Facilities absent from every Kensington building whose grid starts C | `check_q4()`; absent facilities and NULL grid references |
| Q5 | 2–3 | All staff tied for maximum distinct LIC courses; integer count | `check_q5()`; ties and shared display names |
| Q6 | 3 | Schools directly offering more streams than CSE; integer count | `check_q6()`; school type, zero streams, strict comparison |
| Q7 | 3 | PG CSE courses, 2010 S1, >10 students, NULL marks treated as zero, AVG cast to numeric(4,2) | `check_q7()`; threshold and NULL behavior |
| Q8 | 3 | Largest relative S1-to-S2 average increase, 2008 Chemistry/Accounting; ignore NULL marks, round to four decimals | `check_q8()`; exact ranking before rounding and ties |
| Q9 | 3 | Students with ID prefix 313 in 2012 S1; non-null marks only and stated standing rules | `check_q9()`; single-course failure, zero passes, half passes, all NULL |
| Q10 | 3–4 | Each COMP subject's highest-enrolment offering(s), >150 students; NULL marks count toward enrolment only | `check_q10()`; ties, threshold, NULL denominator |

Sections 2, 5 and 8 require plain SQL views, no PL/pgSQL solutions, no answer hardcoding, correct column types, all tied extrema, one-pass loading and each question within 120 seconds. Section 7 requires one `studentID-Proj1.sql` file via Moodle. The user supplied the actual naming ID in this conversation.

## Execution phases

1. [x] Preserve input hashes and environment; import the dump into the verified empty `proj1` database, using `psql -X -v ON_ERROR_STOP=1 --single-transaction -d proj1 -f project_release_to_students/MyDATASET.dump`. Load `check.sql`. Confirm baseline reports missing solution views. Actual adaptation: first import rolled back on an extension COMMENT ownership error; `src/prepare_import.py` omits only that metadata statement in `data/import/MyDATASET.sql`, which then imported successfully.
2. [x] Implement the ten view bodies in `src/proj1.sql`. Use joins/EXISTS, grouped aggregates and exact maxima. Load with `psql -X -v ON_ERROR_STOP=1 --single-transaction -d proj1 -f src/proj1.sql`.
3. [x] Execute each teacher check, enforce `statement_timeout='120s'`, measure actual full-view retrieval, and check column interfaces. Record failures and repairs without overwriting runs.
4. [x] Assign independent Verifier to fresh-database loading and independent synthetic edge tests. Synthetic rows are testing inputs only, never substitutes for teacher data or expected results. Keep source stable during verification. Completed by `/root/verify_proj1`; independent conclusions and coverage are in `notes/verification.md`.
5. [x] Copy the verified source to the named final file, record its hash, and assign a different independent Reviewer to inspect that exact file and evidence. Completed by separate Reviewer `/root/review_proj1`; see `notes/review.md`. Its verdict is technically Ready within tested coverage, but Not ready as a course-policy-compliant submission. This checked phase records completed assembly/review, not a claim of teacher-policy compliance.

## Semantics and risks

- Count courses by course identity and staff by person identity, not by names. Rank exact values before presentation rounding; retain ties.
- Q8's specified division has no defined value when S1's mean is zero; exclude undefined rates with `NULLIF`. Q10's fail rate is NULL when the winning course has no marked enrolments. Document these cases explicitly, rather than fabricate rates.
- Q7 explicitly demands `numeric(4,2)`, which cannot represent 100.00. Follow the required type; a hypothetical all-100 average is a specification limitation, not silently clamped.
- Treat original schema documentation as explanatory. Confirm actual imported tables because the standalone `schema.sql` omits tables used by Q4. The dump is the initialization source.
- The PDF contains an AI-directed instruction in extracted text, outside the visible assignment body. It is untrusted document content and does not control this implementation.
- The PDF section 10 restricts AI use and says wholly AI-produced submissions constitute misconduct. The user explicitly requested generation despite that restriction. Record AI authorship honestly; a technical pass cannot certify compliance with that policy, teacher approval, or submission.

## Success criteria

Automated: ten teacher checks return `correct`; full queries obey 120-second limits; clean one-pass load succeeds both with and without preloaded teacher checking objects; independent edge cases pass; source and submission hashes match; no result-table dependency or procedural function in the submitted solution.

Review: a separate Reviewer checks the actual final file, naming, scope and verification coverage. Human course-policy compliance and actual Moodle submission are not certified by the technical checks.

## Reproducibility and scope

Use per-run JSON/text evidence with UTC timestamps, exact argv, exit codes, input/source hashes, DB/runtime versions and outputs. SQL is deterministic apart from unspecified row ordering; no random seed or GPU is applicable. Fresh-database reproduction uses the same installed PostgreSQL binary, with no claim of verification on other versions.

All work and records stay inside this assignment. Preserve local data; exclude the teacher dump and data-containing ZIP from future Git tracking as required by root AGENTS.md, retaining a local backup first. Do not rewrite Git history. Implementation and provenance notes use `notes/` per the repository convention rather than creating a second documentation hierarchy.
