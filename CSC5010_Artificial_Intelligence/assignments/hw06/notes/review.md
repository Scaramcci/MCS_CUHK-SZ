# HW06 independent final review

Role / Executor: Reviewer / independent sub-agent `/root/hw06_reviewer`, 2026-11-08 (Asia/Shanghai).
Task: `CSC5010_Artificial_Intelligence/assignments/hw06`.
Independence: I did not create the answers or author self-check helper and am not this round's Verifier. Only this review record was written in the repository. Temporary text/render files were placed under `/tmp`.

## Inputs and checked version

Read repository README and AGENTS, agents/README and reviewer role, course README, hw06 README, preparation/handoff record, the complete answer source, final build record and author-check output. Explicit path checks found no additional AGENTS.md or AGENTS.override.md at course, assignments, hw06, report or requirements level. Requirements contains one seven-page PDF. Read its extracted text and visually inspected all seven original-page renders; image content governs where extraction omits or exposes hidden content. Read the anti-defensive-writing skill for this review record and PDF skill for visual inspection (the listed newer skill path was stale; the available PDF skill was found under version 26.1104.22356).

The exact deliverable is the four-page `report/answers.pdf`, with editable `report/answers.tex`. I independently rendered the actual PDF using:

```bash
pdftoppm -scale-to 1400 -png CSC5010_Artificial_Intelligence/assignments/hw06/report/answers.pdf /tmp/hw06-review-final
```

Rendering exited 0. Each of the four resulting PNGs was byte-for-byte identical to the author's final image with the same page number; all four were visually inspected. Body text, equations, tables and page numbers are legible without overlap, clipping or missing symbols. Pages 2 and 3 are dense but readable and their final lines remain above the page numbers.

SHA-256 checked against the author's build record:

| File | SHA-256 |
| --- | --- |
| `requirements/Prob-Reasoning HomeWork.pdf` | `9b8caab160c04a572d9ede9ad3e0457463288173b70370b2a38da38a85930d5e` |
| `report/answers.tex` | `ed88cb493ff3d96c360ac710ab8a7f7ba521584b256d2a0c922b8b1b61eb2354` |
| `report/answers.pdf` | `72ef7c41e2c6dea5714eafdb044e07f8bed441431e75eb60838a79ffa3fc5b78` |

## Critical issues

None within the mathematical-reference scope. The answer covers all seven questions, preserves the original, and does not invent experimental results, a sample size supplied by the teacher, or school submission requirements.

## Major issues

None. Two under-specified inputs in the source are handled explicitly: Q1 gives no count total for add-one smoothing, and Q5 gives no initial distribution. The answer gives general formulas and labels its numerical assumptions. Readiness applies to this complete conditional/reference answer; an instructor clarification could determine a different numerical specialization.

## Minor issues

None requiring repair. Q3's optional smoothed variant is explicitly labeled, uses the three-valued Water attribute correctly, and leaves the primary empirical classifier unambiguous.

## Requirement checklist and independent mathematical review

I independently recomputed the calculations with standard-library exact fractions and direct counts from the visible original. This was my own short arithmetic command rather than running the author's helper; it exited 0. No separate experimental or implementation-validation claim is made.

| Original requirement | Exact answer reviewed and evidence | Status |
| --- | --- | --- |
| p.1 Q1(i-iv), Laplace smoothing | Correct multinomial coefficient for unordered composition. With empirical count total N, q_i=(Np_i+1)/(N+5). N=100 is visibly labeled as an example, not an inferred teacher fact. Independently enumerated all 70 compositions for both given proportions and that example, checked probabilities sum to one, and obtained unique maximum (1,1,1,1,0) and minimum (0,0,0,0,4). The transfer argument proves the maximum generally because q_i/q_j is at most 1.5, and the product bound proves the minimum. All displayed decimals match. | Pass, with source's unspecified N stated |
| p.2 Q2, unprepared given correct answer | Bayes numerator is 0.25*0.25 and denominator adds 0.75*0.9. Independently obtained 5/59, approximately 8.4746%. | Pass |
| p.3 Q3, visible query | Bottom query visibly has four yes values. Recounted mammals: 7 total, yes counts (6,1,2,5). Non-mammals: 13 total, yes counts (1,3,3,9); the nine with legs are frog, komodo, pigeon, turtle, penguin, salamander, gila monster, owl and eagle. Empirical scores are 3/343 and 81/43940; posterior is 43940/53201, approximately 0.825924, so mammal. Independently obtained smoothed scores 0.0125701459 and 0.00377104377, posterior 0.769230769. The hidden old example/query is correctly not used. | Pass |
| p.4 Q4, contingency table and transition matrix | Independently counted sequence SSRCCRRSSSRCCRSSC. In S,C,R order, counts are [[4,1,2],[0,2,2],[2,2,1]]; row totals are 7,4,5 and total is 16. Row-normalized matrix matches the answer. Last-day C has no successor. | Pass |
| p.5 Q5, three consecutive sunny days | Matrix entries match source. Three sunny days use two sunny-to-sunny transitions, so general answer is P(W_t=S)*0.8^2. Independently checked pi=(638,245,46)/929 sums to one and satisfies pi A=pi. Stationary window probability is 10208/23225, approximately 0.439526372. Conditional answer given a sunny first day is 0.64. All assumptions are stated; no unsupported horizon or initial distribution is introduced as fact. | Pass, with stationarity conditional explicitly stated |
| p.6 Q6 task 1, decomposition | Graph M->E->C and A->C gives P(M)P(A)P(E|M)P(C|E,A). | Pass |
| p.6 Q6 task 2, learned parameters | Independently summed 40 records, M split 20/20, A split 25/15; E=Good counts 10/20 for Hi mileage and 15/20 for Lo mileage. Independently summed over M for C-high CPT values 12/16,6/9,2/9,0/6; complementary low probabilities are correct. | Pass |
| p.6 Q6 task 3, bad engine and broken AC | Graph makes E and A marginally independent. Learned P(E=Bad)=15/40 and P(A=Broken)=15/40, so fitted joint is 9/64=0.140625. Raw 6/40=0.15 is clearly distinguished. | Pass |
| p.7 Q7 decomposition and a-c | B,F are independent roots and both parent G,S, so factorization and G/S conditional independence are correct. Independently recomputed a=0.9*0.2*0.8*0.2=0.0288; b=0.1*0.2*0.1*1=0.002; c=0.8*0.1+0.2*0=0.08. Gauge is correctly marginalized in c. | Pass |
| Exact PDF presentation | Four reviewed pages contain Q1-2, Q3-4, Q5-6 and Q7. No missing answer, clipped formula, unreadable table or page-number overlap found in the actual PDF's independent render. | Pass |
| Build/provenance | Hashes match build record; final compilation output has no warning or overfull/underfull report. Author self-check is labeled as self-check, with earlier failures retained separately. My independent mathematical and visual review covers the exact final version. | Pass |
| Separate experimental Verifier | Pure finite-probability handwritten-reference task with no research-code or experimental deliverable; repository's simple handwritten-task workflow permits Solver->Reviewer. Independent mathematical review performed here; no claim of a separate Verifier execution. | N/A |
| School submission archive | No electronic package, naming rule or required submission format appears in the original. No submission directory exists; exact reference deliverable is report/answers.pdf. Internal notes/results are not school submission content. | N/A |
| External submission | No upload or publication performed. | N/A |

## Final readiness

**Ready** as the exact four-page mathematical-answer reference identified above. No unresolved Critical or Major issue remains. Q1's sample-size dependence and Q5's initial-distribution dependence are explicitly preserved rather than hidden. This conclusion does not certify an unspecified instructor-specific convention or actual submission. Any change to the answer source/PDF requires affected checks and review to be repeated.

Next role: root session may deliver the checked PDF and editable source, and mention the two explicit assumptions to the user.
