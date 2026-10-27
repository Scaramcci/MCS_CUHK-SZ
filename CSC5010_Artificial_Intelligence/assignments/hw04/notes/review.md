# Independent review — HW04 handwriting reference

Role / Executor: Reviewer / independent sub-agent `/root/hw04_reviewer`, 2026-10-27 (Asia/Shanghai). This reviewer did not author the answers and was not a separate Verifier.

Scope: review `report/main.tex` and `report/answers.pdf` against all three pages of `requirements/CSP_Ding_2026-homework.pdf`. Only this review file was written; answers and teacher originals were not modified. Repository branch: `master`; existing unrelated changes were preserved.

## Inputs and versions

Read root README/AGENTS.md, agents/README.md, agents/reviewer.md, course README and notes/answer-preparation.md. No course/assignment AGENTS files were found. The assignment README is absent, as already recorded by the author. The requirements directory contains the single three-page PDF.

SHA-256 values independently checked:

| File | SHA-256 |
| --- | --- |
| requirements/CSP_Ding_2026-homework.pdf | `ea6d14acdf6bedfe330f671475b1a4f36ceb2c60ea1fd4f41ee9bad31bea4d90` |
| report/main.tex | `a37b3d71e5a1baaa6ada8c53d60b673ed6878f4aeaf990ae1541036570fab091` |
| report/answers.pdf | `36ba4b24a847a68e1e68101396d7df7ea8271e2032f2b6db9babd8e285b954f2` |

The author build record in `results/20261027-final-answer-build/build-record.json` matches these hashes and records two successful pdfTeX passes. This is author build evidence, not an independent compilation by the reviewer. The reviewer extracted both PDFs with `pdftotext -layout` (exit 0) and visually inspected every original and answer page at `/tmp/csc5010-hw04-review/page-{1,2,3}.png` and `final-answer-{1,2}.png`.

## Critical issues

None found within this review's scope. No unsupported experimental claims, credentials, private information, or missing answer sections were found in the reference document.

## Major issues

None found. All three problems are answered correctly under the explicitly stated heuristic interpretation.

## Minor issues and limitations

No required correction. The original phrase “minimum value heuristic” is undefined in the teacher PDF; the answer transparently interprets it as MRV, defines degree over unassigned neighbors, states alphabetical tie-breaking, and tries values in increasing order. Classroom terminology has not been confirmed. This limitation is disclosed rather than presented as a teacher-specified rule.

## Coverage checklist

| Requirement / check | Result | Evidence |
| --- | --- | --- |
| CSP1, original p. 1: unary domains and all 8 graph edges | Pass | Visual graph agrees with `ab, ac, ad, bc, be, cd, ce, de`; initial domains match both unary constraints. |
| CSP1: variable/value choices and every forward-checking update | Pass | MRV selects a, then b, then c. Remaining d/e domains both have size 2 and each has one unassigned neighbor; degree ties and stated alphabetical rule selects d. Table and prose agree at every step. |
| CSP1: final solution | Pass | `(a,b,c,d,e)=(1,2,3,2,1)` meets all 8 inequalities and both unary constraints. No domain empties; no backtracking is needed. |
| CSP2, original p. 2: all 7 edges and fixed red node | Pass | Original graph and redraw agree on `LA, LB, AB, AC, AD, BD, CD`; `(L,A,B,C,D)=(R,G,B,B,R)` satisfies each edge and fixes L red. Node B versus color B is clarified with “blue.” |
| CSP3, original p. 3: changed boundary | Pass | Modified Victoria extends east of NSW to Queensland, adding the Q–V border. SA/Q/NSW/V are pairwise adjacent. |
| CSP3: necessity and sufficiency of 4 colors | Pass | The six displayed edges establish K4 and the three-color contradiction. `WA=2, NT=3, SA=1, Q=2, NSW=3, V=4` satisfies all displayed map adjacencies, establishing the matching upper bound. |
| Final PDF rendering and source/PDF consistency | Pass | Both answer pages inspected: complete text, tables, boxed results and diagrams are readable, with no visible clipping or overlap. PDF text agrees with the reviewed source. |
| Separate code/experiment verification | N/A | Simple theoretical handwritten exercise; no implementation or complex numerical computation requires a separate Verifier under agents/README.md. |
| Electronic submission package | N/A | User requested a reference to copy onto paper; teacher PDF specifies no electronic deliverable. Confirmed `submission/` does not exist; the reviewed two-page PDF is the actual reference deliverable. |
| Upload / school submission | N/A | Not authorized or performed. |

## Final readiness

**Ready — for use as a handwriting reference**, limited to the exact source/PDF hashes above. Independent content and presentation review is complete, with no unresolved Critical or Major issue. This conclusion does not claim a separate Verifier run, school submission, or teacher approval. Any later answer change invalidates the affected checks and requires review of the new version.

Next role: main session delivers the reviewed reference and its disclosed heuristic interpretation to the user.
