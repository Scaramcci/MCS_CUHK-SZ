# Task 3 scaffold: source review

Date: 2026-10-28 (Asia/Shanghai)
Role / Executor: Planner and source investigator, `/root`.
Scope: internal course materials; project scaffold only.
Input repository revision: `0f4a40736f0af5ab23a55b50af6229de7cdaef66`; the course notebook and unrelated coursework are uncommitted. No changes to other coursework are authorized.

## Findings

- `requirement/Assignment_2.pdf`, p. 1, section 3: choose exactly one task; implement and compare at least three tutorial/guide prompting techniques; compare non-agent and agent approaches on the same evaluation data; document model/settings and feedback-dependent agent decisions.
- Same PDF, p. 3, section 3.3: Task 3 takes dataset D and returns a cleaner D'; define and justify quality criteria. English or Chinese GPT-4 Alpaca are examples, not a mandated sample size or training requirement.
- Same PDF, p. 4, sections 4–5: concise PDF report using the Overleaf template, prompts and rationale, agent workflow, representative cases, real experimental comparisons; code supplementary. Deadline: 2026-11-06 23:59 UTC+8. Report language is English by user instruction (2026-10-28), not a PDF requirement.
- `requirement/“Prompt_Engineering_CSC6052_ipynb”的副本.ipynb` contains 49 cells. Zero-based cells 20–25 demonstrate zero-shot, few-shot and chain-of-thought prompting. Cells 6–18 demonstrate model API calls; cells 33–48 cover Tasks 1 and 2. It does not implement a Task 3 data-quality pipeline.
- The notebook contains existing outputs and a potential credential string. It is an untracked teacher/reference original: preserve it, do not execute it, print its credential values, copy credentials into new files, or automatically stage it. Notebook output is not evidence for this project.
- No assignment README or narrower AGENTS rules existed at source review time. Root rules require keeping data and secrets local and separate independent Verifier and Reviewer agents.

## Input fingerprints

| Source | SHA-256 |
| --- | --- |
| Assignment PDF | `bf09fbc9f382a149804a7977a6cc63912efa93520c56d4c7fe7c51260e64aa5f` |
| Course notebook | `5a396a71600492e39974d51ee7a2e6c5bf020242896dd37db88fcae2310c26e9` |

## Synthesis and handoff

Use the notebook as a reference for three initial prompt templates. Do not install its dependencies or run its cells merely to create a scaffold. A standard-library-only local command can check the scaffold and preview templates without API access. Dataset acquisition, current provider/model verification, budget control, feedback-driven agent execution, evaluation labels and experiments are later implementation work.

See [plan.md](plan.md). Workflow notes live in this assignment's `notes/` as required by the repository, rather than the research skills' general root-level document convention.
