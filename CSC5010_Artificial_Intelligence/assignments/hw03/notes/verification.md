# Independent technical verification

Executor: `/root/verify_answers`, independent of answer authorship.
Date: 2026-10-08 (Asia/Shanghai). Scope: English handwritten-answer assistance.
Inputs: original requirements PDF, root README/AGENTS, course and assignment READMEs, agents/README and agents/verifier.md. No lower-level AGENTS files found. hw03 README absent; hw01 README is stale and contradicted by original.

Evidence is in `results/verification/20261008-independent/`. Original PDF page PNGs were rendered with Poppler and visually inspected. Source hashes and command provenance are recorded in `provenance.txt`. Initial Git status was clean. Original PDFs were not changed. No answer sources were authored or edited by this verifier.

## Passed checks
All six original pages visually inspected; Game3 additionally cropped at4000px to distinguish handwritten marks. Independent script `check.py`, exit0, evidence `output.txt`.
- Games1 actual board red pieces: rooks3+2,horses2+2,elephants2+2,advisors1+1,king1,cannons13+10,soldiers5 =44 moves; depth3 leaf heuristic evaluations44³=85184.
- Game3 exact11 depicted terminal board transcriptions and utilities in output.txt. Corner/Ocenter0; shared node0; corner/Ocorner1; corner/Oside1; corner-first0, center-first0, root0. Both depicted opening choices tie.
- Game4 backed values top-left1,left-middle0,bottom-left1,bottom-middle0. Bottom-left and top-left best; bottom-left has higher other replies and can be preferred with explanation.
- Game5 terminal-history enumeration stops immediately on win: depths5..9={1440,5328,47952,72576,127872}; depth9 Xwins81792 and draws46080.

## Warnings
- The draft has now been checked; see the versioned follow-up below.
- An initial low-resolution interpretation of Game3 top terminal was incorrect; corrected by4000px cropped reinspection. Top terminal is XOX/.OX/O.X, an X right-column win. The corrected backed root is0, not earlier -1/+1 message.
- Xiangqi count script checks piece movement and occupancy; king safety was visually assessed for this specific board rather than a complete reusable Xiangqi engine. No legal candidate exposes red king here.
- Histories are distinct move sequences, not deduplicated board positions. Depth3 evaluation convention is leaves only.

## Failed checks / Required fixes
None in the examined technical content; see the versioned follow-up below.

## Draft technical verification, 2026-10-08

Input: `report/answers.tex`, SHA-256 `32f3f0fcd49ba6e371e67c63d0a73320e86170232399edfea59c797eb6beb35f`. Exact examined source retained as `results/verification/20261008-independent/checked-answers.tex`. This conclusion applies only to that source version and technical content. No PDF layout or final submission approval is claimed.

Passed: entire source read. Games1 coordinates converted between source/independent-script top-origin and draft bottom-origin; every destination/count matches. Game2 move sequences independently executed with terminal checks after each prefix; both legal draws. Game3 exact terminals and contracted MIN/MAX backups checked, including dashed alternate Xresponse and symmetric shared node; corner0,center0,root0 correct. Game4 four leaf-score arrays match original,MIN scores1/0/1/0 and subjective tie preference appropriately separated. Game5 combinatorial5/6-ply derivations checked; exhaustive independent history enumeration confirms all totals. Independent minimax verifies all9 full-game opening choices0. Independent enumeration of5-X/4-O full boards confirms16 draws. Recurrence correctly stops earlier terminals.

Failed checks: none in covered technical content. Required fixes: none. Reviewer must assess diagram readability and final exact files separately.

## Final technical-source update

Source SHA-256: `2d5a768de915a9ebbe570e9f4e84b993717c949f4b954ee6c96e4cf2c68def8e`. Snapshot: `results/verification/20261008-independent/checked-final-answers.tex`. Current exported PDF SHA-256: `723e1de0b74740f27095c99d45c72667e2ec2c5a0f09fb84490cdb03da38f7d1` (recorded for handoff; page layout approval belongs to independent Reviewer).

Diff reviewed against previously checked source. Changes concern spacing, board baseline, wrapping math cells, and clearer DFS3 goal mark. No numerical, graph-edge, or algorithmic-value changes. Previous independent technical checks remain applicable to this exact version. No technical defects.
Final technical disposition: passed within documented source/calculation coverage; no answer files modified by Verifier. Final PDF readability and complete delivery review remain separate.
