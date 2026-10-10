# Independent review — CSC5041 HW01

- Role / executor: independent Reviewer, `/root/review_db_answers`; did not create the answers or act as Verifier.
- Scope: concise LaTeX/PDF answer aid for copying by hand, not a submission package.
- Reviewed version: `report/answers.tex` SHA-256 `17e220e529b35de989d9874f1cd6a7733f081ab7e6e2c75b9060ca014d9f00a1`; `report/answers.pdf` SHA-256 `a048c57616f178cd7960df931c6cfc5367df4406fc522598d16e3fc5918dadc2`.
- Sources: `requirements/Assignment_1_Questions.pdf`, pages 1–4; visually inspected original Q2 diagram on page 2. Relevant lecture material: `Week 1B - Conceptual DB Design.pptx` (keys, weak entities, participation, derived attributes); `Lecture2A.pptx` slides 35–55 (mapping); `Relational_Algebra.pptx` slides 14, 41, 48, 55, 57–60 (set projection, joins, division, rename, aggregates).
- Rules read: root AGENTS.md, agents/README.md, agents/reviewer.md, root and course README. No lower AGENTS.md found; assignment README absent. Course README predates the supplied assignment and is not the requirements authority.

## Critical issues

None found in the reviewed answer aid. No experiment claims, external publication, or submission package were involved.

## Major issues

None found in the reviewed content.

- Q1 covers all seven entities and all listed attributes. Department and QueuePosition have correct owners and partial keys. Mandatory Hospital/Department/Doctor/Slot participation and optional Patient/QueuePosition participation match page 1. Assigned plus the explicit Included equivalence and per-appointment/per-slot uniqueness constraint correctly express multiple slots per appointment, possible sharing of slots between appointments, and at most one assignment per queue position. Stored duration/totalSlots and derived age are consistent with wording and lecture treatment; optional tags and nonempty appointments are explicit assumptions.
- Q2 preserves all entity attributes, omits derived A10/A11, flattens A13, separates multivalued A6, and absorbs identifying R2 and 1:1 R4 correctly. Ternary R1 uses `(A1,A9,A3)` as its primary key, since the other participants determine E4. Foreign keys, uniqueness/non-null R4 constraints and total-participation projections are correct.
- Q3 uses lecture-supported operators. Q3.1 joins by IDs before projecting names. Q3.2 excludes any rider with a fare above 10, then groups payments by riderID. Its nonempty-trip and existing-payment interpretation is explicitly stated. Q3.3 divides by category (not typeID), retaining riderID so shared tiers do not merge riders. Q3.4 joins the start station correctly and retains tripID during projection, preserving repeated riders/ages in AVG under set semantics. Both inclusive date boundaries are present.

## Minor issues

None requiring correction. The first Q3 selection has compact subscripts, but it remains readable in the PDF and may be copied as a multiline condition by hand. Q1 is split into a relationship graph and two attribute pages; repeated entity names are explicitly explained.

## Submission checklist

| Item | Result | Evidence |
|---|---|---|
| Q1 ER diagram, attributes and assumptions | Pass | PDF pages 1–3 |
| Q2 relational model and keys | Pass | PDF page 4 |
| Four Q3 expressions, permitted operators | Pass | PDF page 5 and listed lecture slides |
| PDF visual presentation | Pass | All five pages rendered and viewed; no clipping, missing formula, overlap or extra blank page observed |
| Executable experiments / code verification | N/A | Pure theoretical and hand-copy answer task |
| Final submission filename with student ID | Not checked | No submission package requested; report filename is a working artifact |
| Actual submission package | Not checked | No submission directory/package in reviewed scope |

## Final readiness

Answer aid review: no unresolved Critical/Major issues; reviewed source and five-page PDF are suitable for the requested hand-copy use. Formal submission readiness: **Blocked / not assessed**, because no actual student-ID-named submission candidate was assembled or reviewed. This does not mean the answer aid is incomplete. No upload occurred. Any source/PDF changes invalidate this version-specific review until rechecked.

Next role: main agent may deliver the reviewed LaTeX and PDF links; assemble and separately check an actual submission candidate only if requested.

Final refresh: after the author changed only the TikZ weak-entity rectangle rendering, re-rendered and visually inspected all five final PDF pages; all conclusions above refer to the refreshed hashes.
