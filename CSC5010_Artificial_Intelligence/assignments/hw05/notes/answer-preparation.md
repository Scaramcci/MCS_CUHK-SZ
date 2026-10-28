# HW05 handwritten-answer preparation

Role / Executor: Planner, Solver, Report Writer / root Codex session, 2026-10-28.
Scope: complete HW05 as a concise English reference to copy onto paper, following HW01--HW04. No upload, commit, push or submission package.

## Inputs and source mapping

- Read root README.md, AGENTS.md, agents/README.md, course README.md, earlier HW01/HW02 READMEs, HW03/HW04 answer sources, HW01/HW04 preparation records, and agents/planner.md, implementer.md, report-writer.md, reviewer.md.
- No course/assignment AGENTS.md or AGENTS.override.md found; HW05 README.md was absent. Earlier READMEs contain stale status text, so actual answer sources establish the earlier format.
- The complete requirements directory contains only `PropLogicHomeWork2026.pdf`, five pages. All five pages extracted and visually inspected; formula images are absent from pdftotext output, so rendered pages are authoritative.
- Page 1 / A, 10 points: prove the displayed implication in words. The consequent has an overbar. The user explicitly confirmed in this session that this bar denotes negation. Therefore the displayed statement is false; give a worded counterexample rather than fabricate a proof. Also identify the valid positive resolution conclusion.
- Page 1 / B, 10 points: the SECOND six-clause set, explicitly marked "You prove this", must be proved unsatisfiable by resolution. Pages 2--3 explain the first, four-clause example and an unhelpful attempted proof; they are not additional numbered homework questions.
- Page 4 / C, 10 points: Rosen Exercise 58 asks how many of the five displayed disjunctions can be simultaneously true. Exhibit an assignment attaining the trivial upper bound five.
- Page 5 / D, 10 points: solve the three ordinary equations and classify simultaneous truth of the three implications, with explanation/truth table. Ordinary real arithmetic assumed. Provide the complete eight-row truth table and all satisfying assignments. Choice (a), "cannot ... in all cases", is linguistically ambiguous: read literally as "not in every case", it also holds; the precise answer is "some but not all", corresponding to the intended choice (b).
- No deadline, required answer language, filename, page limit, electronic submission format or AI-use restriction appears in these five pages. English and concise style follow previous user preference; a reference PDF is our delivery choice, not a teacher-required submission.

## Plan and checks

1. Produce `report/answers.tex` and `report/answers.pdf`: A and B on page 1; C and D on page 2.
2. Preserve the teacher original; use explicit resolution parents and pivots; distinguish clause entailment from logical equivalence.
3. Self-check A's counterexample, B's resolution steps and satisfiability, C's witness, and every D truth-table row using exhaustive Boolean enumeration. This is author self-check, not independent verification.
4. Compile twice, inspect all rendered answer pages, preserve actual build/check commands, statuses and hashes in a unique results directory.
5. Use an independent Reviewer as prescribed by the repository's simple handwritten-task workflow. Reviewer must read originals, inspect exact source/PDF version, and only write `notes/review.md`. Separate numerical Verifier is N/A: this is elementary symbolic logic, not complex numerical computation or an experimental assignment.

## State and handoff

- Author source: `report/answers.tex`; reference output: `report/answers.pdf`.
- No school submission package: the user intends to write answers on paper. The generated PDF is the exact reference deliverable to review.
- A is mathematically false under the user's confirmed negation reading. This is a source issue, not an unresolved calculation; the answer explicitly says so.
- Final build, author self-check and visual-inspection evidence: `results/20261028-final-answer-build/build-record.json`, `compile-pass1.txt`, `compile-pass2.txt`, `self-check-output.txt`, `render-stderr.txt`. Two system pdfTeX passes and the Python self-check exited 0; final compiler output has no overfull boxes. Both final rendered pages were visually inspected: all text, formulas, resolution table and truth table fit without clipping or overlap.
- Earlier build evidence is retained in `results/20261028-answer-build/`. It had one overfull line in D; the final version moves that boxed conclusion onto its own display line. That earlier PDF is not the final reference.
- Author check command (working directory HW05): `python3 notes/check_logic.py`. Standard-library exhaustive Boolean enumeration checks A's counterexample, all seven B resolution steps and all 16 assignments, all eight C assignments, and every D truth-table entry. It is explicitly author self-check, not independent verification. No experiment or dataset is involved.
- Final source SHA-256: `ca7eaf2fa03ec9cca6e81791d26f9c31ff3f8a0af3b7a583ec2830cde5885729`.
- Final PDF SHA-256: `613645b0d40258cc174206900579c36e63095403e53c255207c6fd5090ccc344`.
- Source original SHA-256: `f9e73bbf008a46c623dea96c7bfcf930a1f20f58517ffc86eaed2291caf0fbda`.
- Next role: independent Reviewer `hw05_reviewer`, allowed to write only `notes/review.md`. Its actual conclusions belong only to that record, not to this author statement.
