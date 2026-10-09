# Answer preparation record

Role / Executor: Planner and Solver / root Codex session.
Scope: English worked answers for handwriting, authorized by user; no upload and no submission package.
Input: current requirements PDF, all pages visually inspected. Course/assignment instruction search found no additional AGENTS files. hw03 README absent; hw01 README is stale relative to current PDF.
Output: report/answers.tex and exported report/answers.pdf; TikZ figures are original redraws.
State: authored and compiled with local TeXLive; see independent verification and review records for their conclusions.
Constraints: teacher originals preserved; no deadline or submission format inferred.
Assumptions: answer text explains source ambiguities explicitly.
Evidence: results/20261008-answer-build/ and independent results/verification/.
Handoff complete: independent Verifier and separate Reviewer records are in notes/verification.md and notes/review.md.

## Source hashes at authorship
- `BFS-DFS-Dijkstra-Astar-homework.pdf` SHA256 `2abdc4ff81abedd8a940424ff827e602046dc5f781150cf357fcf90b057261b7`
- `report/answers.tex` SHA256 `e9376db53d3f704044d4f79a24efae0551e797ea6f88cc7850ec6287f64ec568`

## Final artifacts
- `report/answers.tex` SHA256 `fef1996723d37577c48871ea294310867b225c2cf0b02ed1d7557da78a2d61f6`
- `report/answers.pdf` SHA256 `7806a3b14245a4cc655dfbec332a70ec197f846617530f27d3c067b3bd259892`
- Compilation commands, exit status, compiler version and timestamps: `results/20261008-answer-build/build-record.json`.

## DFS revision after user clarification
Role / Executor: Solver and Report Writer / root Codex session.
Scope: hw02 DFS1, DFS2, DFS3; all other answers unchanged.
Sources: lecture slides BFS-DFS-Dijkstra-2026-4-7.pdf pp.24,33–36; requirements pp.2–4; user's instruction to use actual graph and alphabetical order.
Findings: slides33–34 define marked backtrack nodes as return points that start another unvisited branch. D is one vertex adjacent to A,E,S; graph DFS visits it only once. The left figure repeats D despite the visited-node rule on slide24.
Convention: preserve the supplied grid prefix, then order remaining unvisited neighbors by ascending node label. Grid slide34 states no fixed directional priority; alphabetical order on slide36 concerns the next letter-labelled graph. This convention is explicit, not attributed to a teacher requirement.
Changes: removed alternate all-return-node definition; removed duplicate-D traversal; added grid exploration44→34→24 and backtrack point44 before visiting goal54.
Evidence: results/20261008-dfs-revision/build-record.json and compile-pass1/2.txt; previous source/PDF archived there. Local TeXLive compiled exit0; no overfull/underfull box warnings. Changed PDF pp.2–4 visually self-checked.
Handoff: independent Verifier checks revised algorithms and source support; separate Reviewer reviews latest PDF after verification. Previous hw02 final conclusions apply to the earlier hashes until superseded by those agents.

Revised source SHA256: `f8aaaea7fb5db52fae35506dc80434fec603d4fe8e1c92bbc49a145df071f845`.
Revised exported PDF SHA256: `dc2cb61589edd689cfe5fc8b45dfae1d5aab8f13261d7423a78c5d9a6a6f72c5`.

## Concise handwriting revision, 2026-10-09
Role / Executor: Solver and Report Writer / root Codex session.
User preference: all-English, less prose, more formulae and diagrams.
Changes: condensed explanatory paragraphs, shortened question headings, retained question coverage and required assumptions; detailed prior source/PDF archived under results/20261009-concise/.
State: compiled with system TeXLive, exit0 in two passes, no box overflow warnings; all final rendered pages visually self-checked.
Source SHA256: `a1e82863a0bfca897db1e35515df9d12deb691ca09f3586ce12476f092e8a5de`.
PDF SHA256: `44e67d92ec9a97259aba2f220cba7940a9be28f7793e6dc702e6e026f99d61d4`.
Evidence: results/20261009-concise/build-record.json, compile-pass1/2.txt.
Handoff: independent Verifier for technical and coverage checks, then separate Reviewer for final source/PDF. Earlier final records remain version-specific.
