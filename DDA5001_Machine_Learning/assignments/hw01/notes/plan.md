# DDA5001 HW1 execution and AI-collaboration plan

Role / executor: Planner, current Codex task. Status: planning only; no answers, code, experiments, or report produced here.

## Sources and constraints

- Teacher handout: `requirements/DDA5001_HW1.pdf`, pp. 1–9. Due at 23:59 Sep 30; year and timezone are not printed in the handout. Confirm the latest Blackboard notice.
- Starter package: `requirements/code_source.zip`, including `p3/p3.py`, `p5/p5.py`, data, and READMEs. Preserve the original ZIP.
- User-selected report template: repository `templates/latex/报告模板.zip`. It contains a different course's sample report and an NKU logo. Use layout elements only; replace unrelated body text, title, logo, and figures. Compile and inspect the resulting PDF.
- An untracked extraction exists at `requirements/code_source/`. Preserve it; make an independent working copy outside `requirements/` for edits.
- Handout p. 1 requires English answers in one PDF plus `.py` code in a single `last name-first name-hw1.zip` uploaded to Blackboard. P3 p. 3 additionally requests numerical outputs. Do not upload without user authorization.
- Handout p. 1 requires the student to write answers in their own understanding and words. Explicit coding-agent permission is given for P3 and P5 on pp. 3 and 8. The student should review and personally rewrite/approve the P1/P2/P4 explanations, especially because the P3/P5 exception does not expressly apply to them.

## Work stages and acceptance evidence

| Stage | Requirement and source | Output/evidence |
| --- | --- | --- |
| 1. Freeze pre-verification expectations | P3 p. 3, P5 p. 9 | Dated text in the new agent conversation before any verification run. P3: sum-versus-mean scaling and directional derivative; P5: pocket training error is a running minimum, test error need not be monotone. These are predictions, not measured results. |
| 2. Working source | P3 pp. 3–5, P5 pp. 8–9 | Complete all four `p3.py` TODOs and three `p5.py` TODOs in a working directory, leaving `requirements/` untouched. Record paths and file hashes or Git state. |
| 3. Real runs and checks | P3 pp. 4–5, P5 pp. 8–9 | Default runs with specified seeds, parameters, commands, versions, exit codes, CSV, PNG, JSON, and P5's seven-row toy trace. Keep raw outputs; no invented values. |
| 4. User-to-agent verification follow-up | P3(e) p. 5, P5(e) p. 9 | User selects concrete values from actual CSV/trace or plots and sends a focused question to the same implementing agent. Preserve actual prompt, reply, evidence, and decision. A correct first implementation may be retained. |
| 5. English answer PDF | P1–P5 pp. 1–9 | Derivations/explanations; P3/P5 actual numerical tables and plots; one authentic AI-collaboration case per problem, each at most one page, together at most two pages. Report statements must match executed code/results. |
| 6. Final candidate and review | Handout p. 1 | ZIP containing PDF, `.py` files, and required P3 numerical outputs; inspect actual ZIP contents, compile/render PDF, verify command reproducibility and no unrelated template/sample content. User supplies name spelling before final filename. |

## Conversation sequence for the separate implementation agent

1. Initial prompt supplies all source paths, working-directory boundary, preservation rules, intended report template, English output, and asks the agent to restate acceptance criteria. Include the pre-verification P3 and P5 predictions in this message, before the agent runs verification.
2. Agent makes a working copy and completes P3/P5 implementations. It may self-check, but its self-check is not an independent verifier conclusion. Agent returns exact commands, output paths, and small excerpts of numeric evidence.
3. User reads P3 `gradient_verification.csv` and `huber_branches.csv`; sends the agent actual compared values at two step sizes, asking whether they support the derivative and sum-loss implementation. The agent explains the Taylor and mean-scaling implications. Save this prompt and reply.
4. User reads P5 `toy_trace.csv` and `trajectory.csv`; sends an actual update row and any relevant curve observation, asking whether the pocket selection and train/test distinction are correct. The agent recalculates one update and replies. Save this prompt and reply.
5. Agent drafts P1–P5 answer text in LaTeX, referencing real outputs and summarizing the two real conversations within their page limits. User checks mathematical reasoning and rewrites/approves their final wording. Any code or result change requires updating the affected report claims and rerunning affected checks.
6. Agent compiles and visually reviews the PDF, prepares the named ZIP after user supplies name spelling, and inspects the exact candidate. Blackboard upload remains a separate user action.

## Open issues

- Confirm the deadline's year/timezone and any newer Blackboard instructions.
- Obtain the student's exact last-name and first-name spelling for the final ZIP; avoid inserting personal details into logs.
- The template has unrelated prior report content and NKU branding; clean adaptation is required.
- The handout asks for numerical outputs with P3, while general packaging instructions emphasize PDF and `.py` files. Include clearly needed numerical outputs, without gratuitous raw data or template assets, and confirm any platform-specific attachment rules.
- P1/P2 answers were already discussed with an agent in an earlier conversation. They are not one of the two required AI-collaboration cases; the student's own review and wording remain necessary.

Next role: Implementer/Report Writer in a separate user-created agent task. Independent verification/review, if requested, must be done by separate agents or sessions under repository rules; the creator cannot sign their own independent approval.
