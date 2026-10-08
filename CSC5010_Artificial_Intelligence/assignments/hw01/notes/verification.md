# Independent technical verification

Executor: `/root/verify_answers`, independent of answer authorship.
Date: 2026-10-08 (Asia/Shanghai). Scope: English handwritten-answer assistance.
Inputs: original requirements PDF, root README/AGENTS, course and assignment READMEs, agents/README and agents/verifier.md. No lower-level AGENTS files found. hw03 README absent; hw01 README is stale and contradicted by original.

Evidence is in `results/verification/20261008-independent/`. Original PDF page PNGs were rendered with Poppler and visually inspected. Source hashes and command provenance are recorded in `provenance.txt`. Initial Git status was clean. Original PDFs were not changed. No answer sources were authored or edited by this verifier.

## Passed checks
- Original pages 1–3 visually inspected. INTRO1 rational choice definition, INTRO2 poor-human-performance task example, INTRO3 historical timeline and hidden-layer difficulty are required.
- Nature primary source independently confirms Rumelhart/Hinton/Williams 1986 paper https://www.nature.com/articles/323533a0 ; MIT Press confirms Perceptrons 1969 https://mitpress.mit.edu/9780262130431/perceptrons/ .

## Warnings
- The draft has now been checked; see the versioned follow-up below.
- The prompt's “neural network is dead in 1970” is an oversimplification. Distinguish single perceptron's representational limitation from difficulty learning multilayer hidden weights. 1970→1986 is approximately16 years; 1969→1986 is17. Do not imply no multilayer representation existed before1986.
- hw01 README incorrectly says no deadline; source page1 specifies Oct10,2026.

## Failed checks / Required fixes
None in the examined technical content; see the versioned follow-up below.

## Draft technical verification, 2026-10-08

Input: `report/answers.tex`, SHA-256 `61888cde8a86e1e91a580cd969065678d67136e87c7996efbc1715b6e5d10f8f`. Exact examined source retained as `results/verification/20261008-independent/checked-answers.tex`. This conclusion applies only to that source version and technical content. No PDF layout or final submission approval is claimed.

Passed: all three answers read against requirement pages1–3. INTRO1 rationality/utility and selfishness distinction coherent; INTRO2 exhaustive game search is an appropriate example. XOR threshold network independently evaluated for00,01,10,11, obtaining0,1,1,0.1969/1986 primary-source dates and16/17-year subtraction verified. Representation versus general learning distinction and differentiable-unit caveat correct.

Warning: Intro3 would answer the requested intervening innovations more concretely by adding an accurately sourced earlier milestone before1986 (e.g.1974 Werbos proposal). Present timeline is sparse but not false. No numerical or conceptual defect found.

## Final technical-source update

Source SHA-256: `ef0e944df2440fda5170a572615b0f8687758a2af14b9e266d146b20e2903be3`. Snapshot: `results/verification/20261008-independent/checked-final-answers.tex`. Current exported PDF SHA-256: `10cee71e02d849f813b9fecada5fd96104917f13df2383f3364843eae0560574` (recorded for handoff; page layout approval belongs to independent Reviewer).

New1974 Werbos milestone independently checked against author-hosted https://www.werbos.com/AD2004.pdf : PDF pp4–5 explicitly identify1974 Harvard thesis/backpropagation and early1970s differentiable-MLP proposal; p9 explains reverse differentiation efficiency. Statement is supported. Prior sparse-timeline warning resolved. XOR reformatted without changing mathematics. Minor editorial punctuation: source[3] lacks closing quotation marks after title; requested author correction. No technical defect.
Final technical disposition: passed within documented source/calculation coverage; no answer files modified by Verifier. Final PDF readability and complete delivery review remain separate.

## Final punctuation/export resolution

Re-read current reference[3]: title now has closing quotation marks. Earlier punctuation warning resolved. Current source SHA-256 `ef0e944df2440fda5170a572615b0f8687758a2af14b9e266d146b20e2903be3` (matches examined final-source snapshot); final exported PDF SHA-256 `49e12138d76420571cc8d38cd694f4ec2d7d56204202be1d5e73fe7f4f656246`. The earlier recorded PDF hash refers to the prior export and is superseded for delivery. Technical source verification remains passed. Source read and `sha256sum` executed successfully; Verifier did not edit answers. Final PDF visual review remains the independent Reviewer responsibility.
