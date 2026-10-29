# Independent technical verification

- Verifier: independent Codex sub-agent `/root/verify_proj1`; did not author or edit implementation.
- Date: 2026-10-28 (Asia/Shanghai); command timestamps in evidence use UTC.
- Scope: `src/proj1.sql` SHA-256 `3c5f06abbca9b49f4984df3b2de4c4f1d33adc74ca20f7f3f47c6e3a6880c3c9`.
- Repository base: `037368d345026e4fe5c3e1a53a31b9f931853f78`, branch `master`. Existing unrelated changes preserved.
- Verdict: **Independent technical checks passed for this source version and the coverage below, with specification warnings.** This does not certify course-policy compliance, universal correctness on unspecified cases, or a final submission package. Separate Reviewer must inspect the actual candidate.
- Evidence: [`results/verification/20261028-independent-v1/`](../results/verification/20261028-independent-v1/).

## Inputs and requirements

Read root rules/README, course README, assignment README, plan, implementation handoff, role instructions, actual SQL, original template/checker/schema, complete assignment PDF text, relevant schema description and summary. Viewed the assignment's p. 3 formulas, description p. 4 ER diagram and both summary pages. No lower-level AGENTS files found. No `requirements/` directory exists; teacher sources are instead in `project_release_to_students/`.

Requirement authority is original `proj1.pdf` section 6 pp. 2–4, with plain views/120-second limit in section 2 p. 1, tie and general-instance rules in section 5 p. 2, and one-pass loading in sections 7–8 p. 4. Description p. 5 explicitly explains multiple subject versions sharing a code. Skills used: using-research-workflows, validating-implementations, PDF reading; repository-mandated notes/output locations take precedence over skill default report paths.

## Passed checks

1. **Input integrity.** Original dump hash `15ae92fbf9a40325743a09f174edf21bf79519b992a2f6810f0dad63c300db71`; derived import `64342e00296082e6764ee9ed415f3391bbea026b2eabb083d8d4a04a42d42793`; original checker `e1f4e0a7dfe3a4d0392faff87d5a71c550683ab8afb28b89371d020e8e098622`. A byte comparison confirms only the single `COMMENT ON EXTENSION plpgsql` statement was replaced by a non-executable comment. No schema/data changes. An initial verifier assertion assumed the line had been deleted; it failed, a diff identified comment replacement, and the corrected exact-byte check passed. This was a verification-assumption error, not a production failure.
2. **Fresh database reproduction.** Created `proj1_verify_20261028_plain` and `proj1_verify_20261028_checked`; both imported the prepared dump with `ON_ERROR_STOP=1` and a transaction. The plain database loaded the solution before any checking objects existed; the checked database loaded checker first, then solution. Both single-pass solution loads exited 0. Original `proj1` was never modified by this Verifier.
3. **Teacher results and multiplicity.** All ten original checking functions returned `correct` in both databases. Independently compared every full result against the teacher expected relation with bidirectional `EXCEPT ALL`: all ten differences zero in each database. This is stronger than the original checker's `EXCEPT`, which ignores multiplicity.
4. **Types and interfaces.** All ten declared view names/columns match the template. Q5/Q6 counts are integer; Q7 average is exactly numeric(4,2); Q8/Q10 rates are numeric. Domain-inherited names/year remain compatible. Inspected actual PostgreSQL catalog output.
5. **Performance.** All statements ran with `statement_timeout='120s'`. EXPLAIN ANALYZE executes complete view plans; measured worst server execution 128.368 ms (Q7). Separately retrieved complete result rows with `psql` into `/dev/null`, including output conversion and client startup. Q1–Q10 wall times in seconds, rounded to 3 decimals: 0.029, 0.044, 0.030, 0.025, 0.037, 0.025, 0.196, 0.049, 0.038, 0.040. These are actual local measurements, not guarantees for larger data or other machines.
6. **Independent synthetic edges.** `edges.sql` generates test-only rows against the original imported schema with constraints intact. A transaction truncates tables only in the dedicated verification database, runs assertions using `EXCEPT ALL`, and rolls back. Eleven assertions passed:
   - Q1 direct offering vs child school, PG vs UG, strict UOC >6 and duplicate codes.
   - Q2 distinct buildings, duplicate rooms in one building and non-Studio class exclusion.
   - Q3 multiple enrolment/role paths collapse to distinct staff.
   - Q4 excluded target building, other campus, other grid, NULL grid and never-installed facilities.
   - Q5 distinct course counts despite two identically named role IDs; ties and identical staff display names preserve multiplicity.
   - Q6 strict comparison, direct school only, child school treated separately and zero-stream CSE.
   - Q7 exactly 10 excluded, 11 included, NULL as zero, separate courses sharing a subject code.
   - Q8 exact unrounded maxima and ties; inferior rate rounding to same 0.0000 excluded; missing S2 marks and zero baseline.
   - Q9 all standing branches, 49/50 boundary, exactly half passing, NULL-only exclusion, wrong prefix and wrong term.
   - Q10 150 excluded, 151/152 included, NULLs counted for enrolment but not fail denominator, tied maximum offerings across subject versions, non-COMP exclusion and all-NULL marked count.
7. **Version transition variant.** A separately recorded `edges_versions.sql` run changes CHEM0001's subject ID between S1/S2 while preserving its code. The full assertion suite still passes under the code-level interpretation. Q10's fixture also compares historical versions by subject code; Q7 correctly keeps individual course offerings separate.
8. **Static inspection.** Source consists of ten plain SQL views, without solution PL/pgSQL, result-table references, hardcoded answer rows, credentials or machine-specific paths. Test-only PL/pgSQL assertion helpers are isolated outside source/submission. No random sampling is used.

## Failed checks

No reproducible implementation defect was found within tested, defined semantics. The numeric overflow below is deliberately reproduced and caught as a specification limitation; it is not counted as a general all-input pass.

## Warnings and unresolved semantics

- **Q7 type conflict:** eleven marks of 100 reproduce `numeric_value_out_of_range`, because mandated numeric(4,2) cannot represent 100.00 (or an average rounding to it). The edge script explicitly catches and records this failure. No silent clamping or changed type is recommended without teacher clarification.
- **Zero denominators:** original Q8 formula gives no meaning for an S1 mean of zero; source excludes it. Q10 gives no defined rate when all winning-offering marks are NULL; source returns NULL. Fixtures verify these documented choices, not teacher endorsement.
- **Subject identity ambiguity:** schema/description distinguishes `subjects.id` versions from `subjects.code`; live teacher data contains 682 codes with multiple versions, but zero duplicate `(subject code, semester)` offerings. Q7 explicitly asks about courses, and groups per course ID. Q8 aggregates a code's marked enrolments by semester, including across versions; Q10 compares each course offering's size across the same code. This is a coherent reading of subject-code reporting and semester comparison, and matches all teacher expected outputs. However, the task never specifies whether Q8 should instead restrict comparisons to identical subject IDs, or how Q10 should combine multiple offerings of one code in the same semester. Different interpretations yield different results on schema-valid synthetic instances. These are material specification ambiguities, not established defects; obtain teacher clarification if hidden-instance semantics require a stronger guarantee.
- School longnames are not unique schema keys. Q6 sums multiple CSE-named school rows if they exist. The task speaks of one school; multiple identically named organisational identities are not specified or covered.
- Initial original-dump import failure and rollback are author evidence, not rerun by this Verifier; verified prepared transformation and fresh compatible imports directly.
- Only installed PostgreSQL 18.6 on this local host tested. Complete exhaustive testing of every schema-valid instance is impossible. No paid service, upload, git commit or push performed.
- Teacher AI-use limitation remains in section 10 p. 4. User instructed generation notwithstanding it; authorship remains AI-generated. Technical success is not course-policy compliance, teacher approval, or submission.

## Required fixes / next role

No required SQL repair identified for tested semantics. Implementer should preserve this hash, keep limitations visible and assemble the exact named candidate. A different independent Reviewer must inspect that candidate and compare its hash with this tested source. Clarification of the specification edge cases is a human/teacher action, not something the Verifier can invent.

## Reproduction and evidence index

Run from assignment directory, using unused verification DB names if rerunning `run.py` (it intentionally refuses collisions via `createdb`). Recorded original commands are in each JSON record:

```bash
python results/verification/20261028-independent-v1/run.py
python results/verification/20261028-independent-v1/run_edges.py
python results/verification/20261028-independent-v1/full_retrieval.py
python results/verification/20261028-independent-v1/run_versions.py
```

`create/import/load/checker/checks-{plain,checked}.{json,stdout.txt,stderr.txt}` record fresh reproduction. `edges*` records synthetic tests, `full-retrieval.json` contains exact argv and wall timings, `subject-identity.*` records actual version multiplicities, `input-hashes.txt` records inputs. Verification databases remain available by the two names above; synthetic edits rolled back. No source, existing database, teacher originals, README or submission files edited by this Verifier.

References: [Plan](plan.md), [Implementation](implementation.md), [Source](../src/proj1.sql).
