# Independent final-file review

- Reviewer: Codex sub-agent `/root/review_proj1`, distinct from author `/root` and Verifier `/root/verify_proj1`.
- Date: 2026-10-28, Asia/Shanghai.
- Scope: exact final candidate `submission/226040255-Proj1.sql`, 5,692 bytes, SHA-256 `3c5f06abbca9b49f4984df3b2de4c4f1d33adc74ca20f7f3f47c6e3a6880c3c9`.
- Only this review record was written. No source, candidate, teacher original, Git index or database was changed.
- Read root/course/assignment rules and READMEs, role instructions, plan, implementation and independent verification records; original `proj1.pdf` all four pages as extracted text and its p. 3 rendered formula page; original template, relevant schema and checker, full candidate, manifest and raw verification evidence. No lower-level AGENTS file or requirements directory was found; originals are in `project_release_to_students/`.
- PDF reading and workflow/validation skill guidance was consulted. The repository's explicit final-review role and this task's read-only evidence-review scope govern: I did not rerun database tests or claim to be their executor.

## Critical issues

**Course-policy compliance: Not ready.** Original `proj1.pdf`, p. 4 section 10, treats submission of wholly AI-produced work as academic misconduct. The implementation is documented as AI-generated at the user's explicit request. That request does not constitute a teacher waiver. Technical correctness cannot establish permission to submit this as course-compliant work. This is a policy finding, not an SQL repair request. No teacher approval or actual upload is claimed.

No technical Critical issue found in the inspected candidate and evidence: no missing question, incorrect package version, credentials, expected-result dependency or fabricated execution claim was identified.

## Major issues

No established SQL defect requiring repair was found within the tested, documented interpretation. The following specification limits prevent an unrestricted claim of correctness on every schema-valid instance:

- Q7 explicitly requires numeric(4,2), which overflows for an average rounding to 100.00. The independent fixture reproduces and catches that error; it is not a successful all-input execution. Changing the type or clamping would conflict with the stated type requirement.
- Q8 excludes undefined zero-baseline growth; Q10 returns NULL for a winning offering with no marked students. The text does not define these denominator-zero cases.
- Q8 groups historical subject versions by code; Q10 ranks individual offerings across each code. Multiple offerings within one code/semester and identity-by-version versus identity-by-code remain unspecified. Teacher data and tested code-level version transitions pass, but do not settle alternative hidden-test interpretations.
- Q6 assumes the named CSE school has its intended organisational identity; summing multiple identically named school rows is a documented, unendorsed fallback.

These are retained as specification warnings requiring teacher clarification for stronger guarantees, not invented requirements or concealed passes.

## Minor issues

No submission-file formatting issue found. The plan's final phase and README's review-pending text are workflow snapshots awaiting this review; the coordinator can update their status and link this record without altering the frozen SQL. They are not included in the submission.

## Submission checklist

| Requirement and original source | Actual check / evidence | Result |
| --- | --- | --- |
| One file named with actual ID, p. 4 section 7 | Direct directory enumeration found only `226040255-Proj1.sql`; ID supplied by user. The printed 226010XXX is a placeholder. | Pass |
| Exact independently verified version | Direct byte equality between source and candidate; recomputed source/candidate SHA-256 and size match manifest. Verification-record hash also matches manifest. | Pass |
| Q1–Q10 supplied interfaces, pp. 2–4 and original template | Full candidate inspection: ten `CREATE OR REPLACE VIEW` definitions, matching column names. Recorded catalog evidence confirms integer Q5/Q6 counts, numeric(4,2) Q7 and numeric Q8/Q10 rates. | Pass |
| Plain SQL, self-contained, pp. 1 and 4 | Candidate has no functions, external files, machine paths or expected-result references. Both fresh load-order records have exit 0. | Pass |
| Q1–Q4 filtering, distinct buildings/staff, facilities | Candidate joins and predicates match question text; teacher results and independent corresponding edges pass. Campus K comes from schema, not answer data. | Pass within recorded coverage |
| Q5–Q6 counts and ties | Staff grouped by identity, distinct courses counted, maxima ties retained; school-only direct stream counts; integer output. | Pass with Q6 identity warning |
| Q7–Q8 averaging and growth | NULL-as-zero Q7, strict >10 threshold; Q8 marked-only exact ranking before four-decimal rounding and retained ties. | Pass with limits above |
| Q9 standing | Prefix, semester, non-NULL filter, 50 boundary, one-course failure and half-pass precedence match text. | Pass |
| Q10 enrolment and fail rate | Strict >150, NULL included only in enrolment, per-code maxima ties, marked denominator, four decimals. | Pass with limits above |
| Original checks and multiplicity | Read both raw `checks-*.stdout.txt`: 10/10 correct and ten zero bidirectional EXCEPT ALL differences in each fresh DB. | Independent Verifier pass, reviewed |
| Edges and reproducibility | Read successful edges and version-variant outputs (11 assertions each, rollback); raw JSON exit records; run script's two load orders. Verified all 47 files in verifier evidence-hash manifest with zero mismatches. | Independent Verifier coverage confirmed |
| 120-second limit, pp. 1 and 4 | Full-retrieval record has exit 0 for all ten, each <0.2 seconds locally on PostgreSQL 18.6; explicit 120s timeout. | Pass on tested host/data |
| No unrelated contents or secrets | Exact candidate contains only task SQL/comments. No data, logs, internal notes, credentials or other student's ID in submission. | Pass |
| Additional report | None requested by section 7; none packaged. | N/A |
| AI policy, p. 4 section 10 | AI authorship acknowledged; no teacher waiver provided. | Not compliant for submission as wholly AI-produced work |
| Upload | Not performed or authorized by this review. | Not submitted |

## Final readiness

**Technical candidate: Ready within the stated verification coverage and specification warnings.** Exact source/candidate equality bridges the independently executed source tests to the actual final file. This is a final-file and evidence review, not a new database test run or exhaustive all-instance proof.

**Overall course-compliant submission: Not ready**, because the known AI-authorship restriction remains unsatisfied. Do not describe this record as teacher approval, unrestricted correctness, or evidence of submission.

Reviewed file: `submission/226040255-Proj1.sql` (5,692 bytes), SHA-256 `3c5f06abbca9b49f4984df3b2de4c4f1d33adc74ca20f7f3f47c6e3a6880c3c9`. Any SQL/candidate change invalidates this review and requires affected revalidation and a new final-file review.

Next: coordinator may report the exact artifact and separate technical/policy conclusions, preserve documented limits and let the user decide subsequent human course-policy action. No SQL repair is requested by this review.

References: [Plan](plan.md), [Implementation](implementation.md), [Independent verification](verification.md), [Manifest](../results/submission-manifest.json), [Teacher specification](../project_release_to_students/proj1.pdf), [Verifier evidence](../results/verification/20261028-independent-v1/).
