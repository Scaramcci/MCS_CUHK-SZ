# Task 3: sources for the complete implementation

Date / access date for every web source: 2026-10-28 (Asia/Shanghai).
Role / executor: Researcher, `/root/research_full`.
Scope: public source verification only; no `.env` access, API inference, dataset
download, implementation, experiment, or final-report authorship.
Repository input revision: `037368d345026e4fe5c3e1a53a31b9f931853f78` on `master`.
Uncommitted files existed in unrelated coursework and in the HW02 hello-call
results; they were preserved. No narrower AGENTS file was found on the course or
assignment path. Earlier scaffold context is in [research.md](research.md) and
[plan.md](plan.md); the latter's scaffold-only scope is superseded by the user's
new full-project instruction, rather than silently rewritten here.

## Research questions and source requirements

1. Identify the teacher-linked English GPT-4 Alpaca data, immutable version,
   schema and data licence (PDF p. 3, section 3.3).
2. Verify the actual provider's current cost and API controls for
   `deepseek-v4-1-flash-260910`, without substituting DeepSeek's direct pricing.
3. Ground three prompt methods and a feedback-dependent agent in the course
   references (PDF p. 1, section 3); identify evaluation limitations.
4. Extract the exact teacher report-template link (PDF p. 4, section 4).

The assignment PDF was fully text-extracted; relevant pages 3–4 were also
rendered and visually inspected. Its SHA-256 remained
`bf09fbc9f382a149804a7977a6cc63912efa93520c56d4c7fe7c51260e64aa5f`.
The source explicitly requires a filtered D', justified criteria, the same
evaluation data across methods, model/settings disclosure, three techniques,
and an agent/non-agent comparison. It does not prescribe Task 3 sample size or
require training a downstream model. English is the user's report preference.

## Verified findings

### Dataset provenance and licence

The PDF p. 3 hyperlink points to the original
[English data file](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM/blob/main/data/alpaca_gpt4_data.json).
The authors' [repository README](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM)
describes approximately 52K GPT-4-generated instruction-following examples. Each
record has string fields `instruction`, `input` (optional task context, possibly
empty), and `output`. The README identifies the data as research-only and
noncommercial. The repository's Apache-2.0 code licence must not be substituted
for the separate [CC BY-NC 4.0 DATA_LICENSE](https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM/blob/main/DATA_LICENSE).

Public GitHub REST metadata was read successfully with Python `urllib` after
the sandbox's ordinary DNS path failed. These endpoints were read, with no file
download:

- [File commit history](https://api.github.com/repos/Instruction-Tuning-with-GPT-4/GPT-4-LLM/commits?path=data/alpaca_gpt4_data.json&per_page=1)
- [Pinned file metadata](https://api.github.com/repos/Instruction-Tuning-with-GPT-4/GPT-4-LLM/contents/data/alpaca_gpt4_data.json?ref=38b93b75a80b019cc3aad362ca6f5bb0c3908959)

Verified metadata: commit `38b93b75a80b019cc3aad362ca6f5bb0c3908959`, dated
2023-04-07; file size **43,379,276 bytes**; Git blob SHA-1
`25508714b7879a1e5a6764ba7f979a980f549f1a`. The metadata-provided immutable download
URL is:

<https://raw.githubusercontent.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM/38b93b75a80b019cc3aad362ca6f5bb0c3908959/data/alpaca_gpt4_data.json>

The data bytes, exact record count, and SHA-256 still require verification by
the data-acquisition step. The Git blob hash is not a file SHA-256.

The cited source paper is Baolin Peng, Chunyuan Li, Pengcheng He, Michel Galley,
and Jianfeng Gao (2023),
[Instruction Tuning with GPT-4](https://arxiv.org/abs/2304.03277), arXiv:2304.03277v1.
Its metadata and abstract were read. Its training results are background, not
results obtained by this homework.

### Ark pricing and budget controls

The official
[Ark model price page](https://console.volcengine.com/ark/region:cn-beijing/docs/model-pricing),
updated 2026-10-26, was opened and its full relevant table inspected. Standard
`deepseek-v4-1-flash` online-inference prices are:

| Beijing-time tier | Noncached input, CNY / million tokens | Cache-hit input, CNY / million tokens | Output, CNY / million tokens |
| --- | ---: | ---: | ---: |
| Peak | 2.00 | 0.04 | 8.00 |
| Off-peak | 1.00 | 0.02 | 4.00 |

Peak means Monday–Friday 09:00–12:00 and 14:00–18:00; all other times are off-peak.
The request's **completion time** determines its tier. Explicit cache storage is
listed at CNY 0.017 / million tokens / hour. These are list prices; the provider
notes actual account/order charges govern settlement. Economy-model and batch
prices are different products and are not applicable by assumption.

Implementation recommendation: use **2/8 CNY per million input/output tokens**
for conservative budget reservations without relying on cache or off-peak
discounts. Track actual usage, failures with uncertain usage, and reservations
before dispatch. Report this as a conservative estimate, not a billing receipt.
This recommendation is project design, not an Ark API feature.

### Model controls and limits

The official
[DeepSeek-V4.1-Flash model guide](https://console.volcengine.com/ark/region:cn-beijing/docs/deepseek-v4-1-flash),
updated 2026-10-27, explicitly includes version `260910`. Chat API supports
`max_tokens` / `max_completion_tokens` for the combined answer and reasoning
length; the model-specific default is 128K. `reasoning_effort: "none"` disables
thinking. The model guide says `top_p` is fixed at 1.0 in non-thinking mode, so
do not claim an arbitrary `top_p` setting was effective.

The official [model list](https://console.volcengine.com/ark/region:cn-beijing/docs/model-list),
updated 2026-10-28, lists `260910` with 1024k context/input, 384k maximum answer,
384k maximum reasoning, maximum 500 RPM and 1,000,000 TPM. Its generic answer
link says default 4k, conflicting with the specific guide's 128K default;
therefore set the cap explicitly and cite the model-specific guide. The list
documents Chat `thinking.type=disabled` as the general switch.

Recommendation: explicitly disable provider thinking for all compared methods
and request a modest bounded answer. The CoT prompt can still request concise
criterion-by-criterion reasoning in ordinary answer text. Preserve actual
returned model ID, output cap, finish reason, usage and timing. Treat
truncation/invalid JSON as a failed output, not silently as a valid rejection.
All settings still need a real request to confirm this account's behavior.

### Prompt methods and an actual feedback loop

The saved notebook's relevant cells are already mapped in [research.md](research.md).
The teacher-selected guide's actual method sections were opened:

- [Zero-shot](https://www.promptingguide.ai/techniques/zeroshot): direct task
  instructions with no demonstrations.
- [Few-shot](https://www.promptingguide.ai/techniques/fewshot): demonstrations
  condition subsequent judgments. The guide also illustrates that examples
  alone do not guarantee correct reasoning.
- [CoT](https://www.promptingguide.ai/techniques/cot): intermediate reasoning;
  its zero-shot variant adds an explicit stepwise reasoning instruction.

Primary references checked:

| Reference | Verified location/version | Appropriate use |
| --- | --- | --- |
| Brown et al., 2020, [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) | Metadata and abstract; arXiv:2005.14165v4 | In-context examples without gradient updates |
| Wei et al., 2022, [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) | Metadata and abstract; arXiv:2201.11903v6 | Rationale demonstrations; do not call a no-example method an exact reproduction |
| Kojima et al., 2022, [Large Language Models are Zero-Shot Reasoners](https://arxiv.org/abs/2205.11916) | Metadata and abstract; arXiv:2205.11916v4 | Zero-shot stepwise prompting |
| Yao et al., 2023, [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/html/2210.03629v3) | Full HTML, method and action/observation trajectories; ICLR camera-ready v3 | Interleave decisions, actions and observations; call our method ReAct-inspired when tools/task differ |
| Zheng et al., 2023, [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/html/2306.05685v4) | Full HTML, judge limitations including Appendix D.1; NeurIPS Datasets and Benchmarks | Discuss position, verbosity, self-enhancement and reasoning limitations |

ReAct's observations come from task/environment interactions and affect later
actions. A credible adaptation can let the model choose bounded schema checks,
constraint checks, arithmetic checks or critique, consume returned observations,
then decide whether to check again or finish. A fixed three-call sequence alone
does not demonstrate this property. The tools must not receive hidden quality
labels. Log chosen actions and observations to support the workflow claim.

The limitation search was explicit: the few-shot guide's failure examples and
Zheng et al.'s bias analysis were read. Suggested evaluation: preserve a frozen
holdout; keep examples and prompt refinements on development data; distinguish
natural-record annotations from constructed corruption tests. If labels are
agent-authored, label them as AI annotations rather than human gold. Retention
rate alone does not show improved quality; an independent reference or a clearly
defined objective check is needed for quality claims. No literature result
establishes that the chosen agent will improve this dataset before running it.

### Exact Overleaf template link

The PDF's p. 4 link annotation was extracted with bundled `pypdf`:

<https://www.overleaf.com/read/jpcrtgzjjdry#36db1a>

This is the teacher-provided URL, not an inferred template. `web.run` could not
access it. A read-only `urllib` request with network permission returned HTTP
200 and a 35,297-character Overleaf HTML shell. The source tree/template content
was **not** recovered or verified in this research stage. The parent should use
the browser/read-only export path to inspect it; if that fails, disclose the
remaining template gap. Do not claim that any generic LaTeX layout is the
teacher's template merely because the PDF permits format adjustments.

## Handoff and open issues

- Planner/Implementer: acquire pinned data locally, compute its SHA-256 and
  actual record count, keep data untracked, and implement budget reservation and
  explicit output/thinking controls before paid experiments.
- Report Writer: cite the original data paper, applicable prompting sources,
  ReAct-inspired workflow and judge limitations; report only actual experiments.
- Template source retrieval and runtime parameter confirmation remain open.
- This document is research evidence; it is neither independent verification of
  implementation nor final package approval.
