# hw01 research and implementation plan

Role/executor: Planner and Implementer, primary Codex session. Date: 2026-10-10.
Scope: complete the existing report notebook and run using conda NLP; install missing dependencies as authorized. No submission/upload or changes to other coursework. Work on existing branch codex/hw02-sockets without changing unrelated work.

## Research / current state

Input: requirements/Assignment_1.pdf, p.1 §§1–4, and the complete 93-cell notebook in report/. Original received notebook saved in results/input-snapshot/. Repository commit: 022a3ee, with untracked user work preserved.

Notebook cells 23, 27, 31: CBOW batch generator, mean-context forward pass and training missing. Cells 45, 53, 56, 71, 74, 81, 88: SVD, semantic examples, analogy, sentence embeddings, retrieval and bias probe incomplete. Cells 51, 54, 57, 90 require prose. Cell 8 reinstalls old packages, and cells 29/31 assume CUDA. Local NLP Python 3.10 environment lacks torch, matplotlib, sklearn and notebook execution libraries; existing Bokeh 3.2 is old alongside NumPy 2.2. Local Quora train.csv exists, SHA256 5f28dbe0bb01b39a793f36567d18fe7cf34d20bbca69ff85b131d7c2186f9914, 63,399,110 bytes. GPU visible outside sandbox: NVIDIA RTX 4090 Laptop GPU, 16 GB, driver 595.91.07.

Sources consulted: [PyTorch CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html), [TruncatedSVD](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html), [Gensim KeyedVectors](https://radimrehurek.com/gensim/models/keyedvectors.html). Raw logits feed cross-entropy; SVD uses fit_transform with n_iter=10; nearest words use cosine similarity. Limitation: Task 2 calls its actual GloVe Twitter vectors Word2Vec and refers to a prior co-occurrence plot absent from this notebook. Distinguish these in the answer rather than inventing an earlier result. PDF 50/30/20 points vs notebook 5/3/2, same proportions; preserve teacher text. Personal fields remain blank.

## Desired end state / approach

Fill every task, retain teacher prompts and default 50,000-text corpus, min_count=5, context window=2, embedding_dim=32, lr=.001, epochs=4, batch_size=128. Use CUDA when available, CPU fallback. Seed Python/NumPy/Torch/SVD/t-SNE/sampling at 42. Keep caches local to the assignment. Retain fresh real notebook outputs and separate run evidence. No fabricated results, no new report or final submission package.

## Consecutive phases

1. Install missing packages in NLP and register the nlp kernel. Use the existing Quora input; download specified GloVe Twitter 25 vectors to data/downloads/. Check imports and CUDA availability.
2. Implement batch generator (full context, non-UNK targets, final partial batch), mean embedding + linear logits, cross-entropy training, seeded SVD, mean known-token sentence vectors, and stable descending cosine retrieval. Run analytic self-checks in tests/self_check.py with `conda run -n NLP python tests/self_check.py`; baseline original functions should fail and implementation should pass. Check empty/all-OOV input, case normalization, k=0 and k greater than corpus, retained final batch, loss gradient and known SVD reconstruction.
3. Execute the full notebook with `conda run -n NLP python notes/execute_notebook.py` from this assignment. Capture environment, source/data hashes, timings, exceptions and checkpoint outputs. Notebook execution must use nlp kernel and save outputs after each cell, including failures.
4. Inspect actual plot, nearest words, synonym/antonym distances and bias scores; fill English prose based on those outputs. State comparison limits for the missing co-occurrence plot. Validate notebook structure and every code cell execution status.

## Success criteria / verification

Automated: all function self-checks pass; 4 real epochs recorded; every non-empty code cell executed without error; no unanswered task placeholders; correct kernel; prose matches real results. Manual: student fills name/student ID, reviews interpretation and opens plots in VS Code. Independent verification/reviewer not yet performed; primary-session checks are self-checks only. No final package will be assembled by this task.

## Evidence / handoff

Each run is isolated under results/<run-id>/. Preserve unsuccessful attempts. Use exact package versions, Python/hardware information, input/source/output hashes and status. Next: independent Verifier/Reviewer can inspect this notebook and current evidence in separate sessions; do not represent same-session role changes as independent review.
