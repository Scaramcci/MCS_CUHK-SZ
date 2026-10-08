# Independent technical verification

Executor: `/root/verify_answers`, independent of answer authorship.
Date: 2026-10-08 (Asia/Shanghai). Scope: English handwritten-answer assistance.
Inputs: original requirements PDF, root README/AGENTS, course and assignment READMEs, agents/README and agents/verifier.md. No lower-level AGENTS files found. hw03 README absent; hw01 README is stale and contradicted by original.

Evidence is in `results/verification/20261008-independent/`. Original PDF page PNGs were rendered with Poppler and visually inspected. Source hashes and command provenance are recorded in `provenance.txt`. Initial Git status was clean. Original PDFs were not changed. No answer sources were authored or edited by this verifier.

## Passed checks
All ten original pages visually inspected. Independent script `check.py`, command `python .../check.py > .../output.txt`, exit0.
- BFS no-immediate-reversal depths0–5: 1,3,5,10,14,28; halfway depth5 gives47 states including root and goal test.
- DFS1 source order gives u→v→t→s then t→r→w.
- DFS3 backtrack decisions (4,1) then (4,2); first pocket (5,1),(6,1),(6,2), then (4,3),(4,4),(5,4) goal.
- DFS4 starting v then remaining roots alphabetically gives v,w,s,q,t,x,z,y,r,u. Times in output.txt.
- Dijkstra b–h weight1 verified visually; final distances a0,b4,h5,g6,f8,c12,i12,e18,d19.
- A* hB16 pops A,X,C,W,T; hB6 pops A,X,B,C,W,T; both cost48 path A–X–C–W–T with proper OPEN cost updates. hB6 requires W45→39 and T50→48.
- AStar3 continuous state space infinite; supplied scene has29 polygon vertices plus S,G =31 visibility-graph states.

## Warnings
- The draft has now been checked; see the versioned follow-up below. DFS2 original tree duplicates D. Literal occurrence-tree times differ from visited-set graph DFS; distinguish the two.
- hB6 inconsistent but no CLOSED node needs reopening on this particular graph. General inconsistent-heuristic graph A* needs reopening if a better CLOSED cost is found.
- BFS count assumes suppressed immediate parent reversal as source tree does; root is depth0.

## Failed checks / Required fixes
None in the examined technical content; see the versioned follow-up below.

## Draft technical verification, 2026-10-08

Input: `report/answers.tex`, SHA-256 `e9376db53d3f704044d4f79a24efae0551e797ea6f88cc7850ec6287f64ec568`. Exact examined source retained as `results/verification/20261008-independent/checked-answers.tex`. This conclusion applies only to that source version and technical content. No PDF layout or final submission approval is claimed.

Passed: entire source read. Independent script re-executed after extension, exit0. BFS blank-position table and global uniqueness through depth5 independently confirmed. DFS1 edges/times and distinction between branch resumption/all returns checked. DFS2 literal times independently recomputed; proper graph variant and backtrack distinction correct. DFS3 stack continuation and final path checked manually against source grid. DFS4 adjacency, forest edges,times,finish sequence and edge classes checked. All21 DFS5 edges checked forward against claimed order. Dijkstra rows/tree compared to independent distance relaxation. A* every OPEN row,g/f calculation,path,admissibility/inconsistency explanation compared to independent trace. AStar3 geometry argument, continuous versus finite representation,31vertex count and boundary-contact assumption checked.

Failed checks: none in covered technical content. Required fixes: none. Draft PDF layout and teacher ambiguity acceptance remain for Reviewer.

## Final technical-source update

Source SHA-256: `fef1996723d37577c48871ea294310867b225c2cf0b02ed1d7557da78a2d61f6`. Snapshot: `results/verification/20261008-independent/checked-final-answers.tex`. Current exported PDF SHA-256: `7806a3b14245a4cc655dfbec332a70ec197f846617530f27d3c067b3bd259892` (recorded for handoff; page layout approval belongs to independent Reviewer).

Diff reviewed against previously checked source. Changes concern spacing, board baseline, wrapping math cells, and clearer DFS3 goal mark. No numerical, graph-edge, or algorithmic-value changes. Previous independent technical checks remain applicable to this exact version. No technical defects.
Final technical disposition: passed within documented source/calculation coverage; no answer files modified by Verifier. Final PDF readability and complete delivery review remain separate.

## DFS1–3 revision: independent verification

Executor: `/root/verify_answers`; date2026-10-08 Asia/Shanghai. Scope limited to revised DFS1–3. This supersedes previous technical treatment of literal repeated-D tree and the earlier differently ordered grid continuation. Prior evidence retained.

Examined source SHA-256: `f8aaaea7fb5db52fae35506dc80434fec603d4fe8e1c92bbc49a145df071f845`. Exported PDF SHA-256: `dc2cb61589edd689cfe5fc8b45dfae1d5aab8f13261d7423a78c5d9a6a6f72c5`. Exact source snapshot and independent evidence: `results/verification/20261008-dfs-revision/`.

### Passed checks

- Visually inspected lecture PDF pp24,33–36. Page24 marks a vertex visited on discovery. Page33 explicitly marks only t as the branch point where backtracking resumes another route. Page34 defines the analogous grid bf; it states no compass priority. Page35 actual undirected graph includes S–A,S–D,A–B,A–D,B–C,B–E,D–E,E–F,F–G. Page36 alphabetical convention pertains to the following letter-labelled graph.
- DFS1 tree,timestamps,return path and bt=t agree with question and slide33.
- DFS2 independently executed sorted-adjacency DFS on the actual graph: S1/16,A2/15,B3/14,C4/5,E6/13,D7/8,F9/12,G10/11. Only one D discovery; tree edges and branch-resumption markers B,E match revised answer.
- DFS3 initial22-vertex stack transcribed from supplied route. Each adjacent pair is a legal grid edge. Independent iterative DFS continuation keeps visited markings and sorts remaining labels. It returns to41, explores51→61→62, returns to42, explores43→44→34→24, returns to44, then visits goal54. Thus bf1=41,bf2=42,bf3=44. Every shown forward/backward edge,dead end,neighbor priority and final start-to-goal stack match the revised answer.
- Independent script assertions all passed; actual command `python .../results/verification/20261008-dfs-revision/check.py > .../output.txt`, exit0. Source/PDF hashes confirmed by actual sha256sum.

### Failed checks / Required fixes

None in revised DFS1–3 technical content.

### Warnings / Next role

Ascending labels are an explicitly chosen continuation convention, not a rule imposed on the grid by the slides. The prescribed earlier route is preserved as input even though it need not use that same ordering. Current answer states this distinction correctly. Verification does not constitute final layout/package approval; separate Reviewer should inspect revised PDF DFS1–3 pages and actual delivery file. No answer files modified by Verifier.
