# Task 3: foundation plan

Date: 2026-10-28 (Asia/Shanghai)
Role / Executor: Planner, `/root`.
Status: authorized for scaffold implementation only; full assignment deferred at the user's request.
Inputs / Version: [source review and fingerprints](research.md).

## Overview and desired end state

Create a small local Python project for Task 3 (LLM data-quality evaluation). The user can enter an API key in an ignored `.env`, inspect three starter prompt templates, and run an offline project check. The report will be written in English after real experiments. No experimental results exist.

The current state is two originals in `requirement/`, with no project implementation. Retain that existing directory name. All changes must stay inside this hw02 directory, on `master`; no commits, branch/worktree creation or uploads.

## Requirements and acceptance mapping

| Requirement / source | Scaffold deliverable | Acceptance now / later |
| --- | --- | --- |
| Task 3, PDF p. 3 §3.3 | Task configuration and draft quality rubric | Declares instruction/input/output records and filtering purpose; later produces D' from real D |
| Three techniques, PDF p. 1 §3; notebook cells 20–25 | Separate zero-shot, few-shot, CoT templates | Three distinguishable templates previewable now; later compare actual outputs |
| Agent comparison, PDF p. 1 §3 | Agent extension module/contract | Clearly unimplemented; specifies observation → decision → action → feedback → bounded stop |
| Same evaluation data/settings, PDF p. 1 §3 | Common settings and documented future evaluation design | All methods share one future frozen split; no invented metrics |
| Report, PDF p. 4 §4; user language preference | English report outline | Explicit draft and missing results, no final PDF or submission directory |
| API configuration, user request | `.env.example` plus ignored local `.env` | Blank key/budget; no credentials printed or executed |

## Implementation approach

Use Python 3 standard library and JSON configuration; avoid dependency installs for a scaffold. Proposed method IDs are `zero_shot`, `few_shot`, `chain_of_thought`, and a deferred `agent`. English Alpaca is a provisional dataset direction, with actual source/version, sample size and annotated evaluation subset deferred until the experiment phase.

Draft quality dimensions: instruction following, correctness, relevance/completeness and clarity. Any scale or retention threshold is a project design choice, not a teacher requirement. Prompt templates use the same rubric and output shape. Few-shot demonstrations, if included, must be explicitly illustrative and separate from real evaluation data. CoT asks for criterion-wise assessment and a concise decision justification. Agent behavior must eventually use observations to choose actions; a fixed sequence of calls is not enough to substantiate adaptive behavior.

## Implementation phases

1. Implementer reads `agents/implementer.md`, originals and this plan, then creates README, `.env.example`, local `.env` only if absent, JSON configuration, prompt templates, a small `src/` command and agent extension contract. No real client/network path is implemented. Suggested command contract, from hw02:

   ```bash
   python3 src/main.py check
   python3 src/main.py preview --method zero_shot
   python3 src/main.py preview --method few_shot
   python3 src/main.py preview --method chain_of_thought
   ```

   A `run` request must explicitly fail as unavailable, including when a key/budget is populated. Preview displays templates with clearly marked input slots, not model outputs. Configuration values are inert until later implementation. Read `.env` as data if needed; never source it through a shell. Do not emit secret values in errors or logs. Existing local `.env` must never be overwritten.

2. Implementer writes a short English report outline with planned Methods, Dataset/Rubric, Experimental Setup, Results, Case Studies/Ablations, Limitations and Conclusion sections, all with honest not-run status. README records exact setup/check commands, dataset paths to create on acquisition, source locations, report/template status and the user's budget-pending instruction. No empty directories or fake submission files.

3. Implementer performs local smoke checks, documents actual commands/status and hashes in `notes/implementation.md` and small timestamped `results/` evidence. Tests should focus on meaningful risks (no network, key redaction, credential ignore rules), not mirror the implementation. No need for broad test scaffolding.

4. A fresh independent Verifier reads `agents/verifier.md`, verifies this exact version offline, and writes only `notes/verification.md` and its `results/verification/` evidence. Check commands work without an API; templates are distinct; a configured key cannot enable a live run; credentials remain untracked/unprinted; originals match the recorded hashes. Problems return to Implementer and require re-verification.

5. A different independent Reviewer reads `agents/reviewer.md` and inspects the scaffold plus evidence, writing only `notes/review.md`. Assess current scope and honesty of status. This is a scaffold review, not final submission-package review. No final package exists in this phase.

## Success criteria

Automated: all four local commands above exit successfully; any experiment command fails without network activity; `git check-ignore .env` confirms exclusion while `.env.example` remains trackable; PDF/notebook hashes match; no actual key in generated source or evidence. No input dataset is required for a template preview.

Manual: README tells the user exactly where to fill their API key; at least three techniques are traced to course cells; future agent/evaluation/report steps are clearly deferred; English outline contains no invented findings. Verifier and Reviewer must be different agents uninvolved in implementation.

## Scope and deferred decisions

This turn excludes paid API calls, downloads, dataset labeling, actual filtering, model training, full agent execution, experiments, completed report and final submission packaging. The user's instruction to build only the structure takes precedence over generic skills' full-implementation or no-placeholder advice; extension points must be explicitly marked unimplemented.

Before experiments: obtain provider/model details and spending limit after the user fills `.env`; verify current API/pricing then; select and fingerprint dataset; define independently assessable quality labels, development/evaluation split and budget enforcement. Any gold-label agreement metric requires actual labels; retention rate alone is not evidence of quality improvement. Prompt tuning and few-shot examples must not use held-out evaluation labels. Before final report: obtain the teacher's Overleaf template if inaccessible from existing materials. User uploads the final approved package to Blackboard.

Next role: Implementer for this scaffold, then independent Verifier and independent Reviewer. Report Writer and final package review resume after experiments; this plan does not pre-fill their conclusions.
