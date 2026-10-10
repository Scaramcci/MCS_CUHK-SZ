# Implementation and self-check record

Role / executor: Implementer, primary Codex session, 2026-10-10. Scope and input analysis: [plan.md](plan.md).
Repository baseline: 022a3ee, existing branch codex/hw02-sockets. Unrelated untracked coursework retained. No commits or uploads.

## Completed implementation

All marked tasks completed in report/26Fall_NLP_Assignment_1_CSC6052_5051_MDS5110.ipynb: CBOW batches, mean context forward pass, Adam/cross-entropy training; randomized TruncatedSVD; polysemy and synonym/antonym exploration; analogy; known-token sentence mean; cosine retrieval; measured bias probe and English analysis. Teacher prompts retained, personal fields blank. Original received notebook retained in results/input-snapshot/.

Environment changes: installed torch, matplotlib, scikit-learn, nbclient, nbformat, gdown; upgraded Bokeh from 3.2.0 to 3.9.2 for NumPy 2 compatibility. Registered Python (NLP), kernel name nlp, in the conda NLP prefix. Set PYTHONPATH empty and PYTHONNOUSERSITE=1 for that kernel to avoid terminal-inherited ROS Python 3.14 paths. Notebook detects CUDA/CPU and supports NLTK 3.8 punkt vs 3.9+ punkt_tab.

## Actual execution / evidence

Working directory: this hw01 directory. Final command:

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 /home/scarramcci/miniconda3/envs/NLP/bin/python -s -u notes/execute_notebook.py
```

Exit status: 0. Final console: results/clean-nlp-execution-console.txt. Input/output snapshots and exact installed package versions: results/execution_20261010T090247_108318Z/. Notebook training run: results/20261010T090249_678432Z/ (training_history.csv and cbow.pt). The checkpoint is ignored by Git.

Runtime: Python 3.10.21, torch 2.14.1+cu130, NumPy 2.2.6, NLTK 3.8, Gensim 4.4.0, scikit-learn 1.7.2, Matplotlib 3.10.9. Hardware: NVIDIA GeForce RTX 4090 Laptop GPU, 16 GB, driver 595.91.07; CPU AMD Ryzen 9 7945HX. Torch CPU threads capped at 8. Seeds: Python/NumPy/Torch/SVD/t-SNE/retrieval corpus sampling = 42. GPU arithmetic may differ across hardware/library versions.

Data: original teacher-notebook Quora URL is retained in cell 8 via its Drive file ID; used the existing report/train.csv. SHA256: 5f28dbe0bb01b39a793f36567d18fe7cf34d20bbca69ff85b131d7c2186f9914. Pretrained GloVe Twitter 25 vectors: Gensim's glove-twitter-25, 1,193,514 words, 25 dimensions, compressed model SHA256: 63877d71151688baf6f31d5437374f637f737a5e100e12150a5bd61a9f273c3f. Caches are in data/downloads/, excluded by root Git rules.

Final notebook SHA256: 6b480ec6bac63e919a3c7e6807c735d3c092e45ee676c66b2b3b155a125009ce.
Normalized concatenated cell source SHA256: 1a63d27ad5a86740f3bd410645472fb6d5e618088e89c5341c14176f0f9214e4.

Kept 50,000 texts, 623,563 tokens, vocabulary 7,226, window=2, min_count=5, embedding_dim=32, lr=.001, epochs=4, batch_size=128; 3,095 batches per epoch and 396,154 examples. Training mean losses: 6.453890561062063, 5.5261952326740555, 5.2167888718743525, 5.024746926480809. Training loss is not held-out evaluation and the small model's semantic neighbors remain weak.

## Fresh self-check outputs

Commands actually run:

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 /home/scarramcci/miniconda3/envs/NLP/bin/python -s tests/self_check.py
env -u PYTHONPATH PYTHONNOUSERSITE=1 /home/scarramcci/miniconda3/envs/NLP/bin/python -s -m pip check
```

Both exited 0. Logs: results/final-self-check.txt and results/nlp-dependency-check.txt. Analytic fixtures (explicitly test data, not assignment experiments) check batch context/label pairing, unknown-target filtering, partial final batch, exact mean-context logits and finite gradients, rank-2 SVD reconstruction, known-token averaging, case normalization, all-OOV/empty input, cosine ranking/ties, k=0 and k above corpus size, and invalid inputs. Original snapshot fails parsing its empty model forward body; results/self-check-original.txt records that observed baseline failure. Baseline self-check was run after implementation, not claimed as test-first.

Final notebook structure validated with nbformat; all 39 nonempty code cells have sequential execution counts and no error output; no unfilled answer/code placeholders remain. Training loss, t-SNE and SVD plots visually inspected. Repeated full runs in the same NLP environment succeeded; max per-epoch loss difference from first successful run was 0. A fresh independently installed environment has not been tested; no clean-room reproducibility or independent verification claim is made.

## Failures retained / limitations

results/execution_20261010T085932_870739Z records a failed repeat execution: NLTK 3.8 rewrote the punkt_tab path to punkt/PY3_tab. Fixed by choosing the tokenization resource by installed NLTK version; later full cached-resource executions succeeded. Other nonfatal host stream-fd notices and an IPython kernel TCP warning remain in console logs, without failed code cells. A broad pip check initially saw unrelated launch-ros via inherited PYTHONPATH; isolated NLP dependency check passes. Earlier runtime snapshots and consoles remain intact.

Task 2 uses GloVe despite calling it Word2Vec; the referenced earlier co-occurrence plot is absent, so the answer explicitly describes that limitation instead of inventing a comparison. PDF and notebook scoring scales differ (50/30/20 vs 5/3/2). The notebook's inherited external image URLs were preserved; no inference about a missing image is needed for the implemented mean-context model.

## Handoff

Student must fill name/student ID and review answers and plots. User can select Python (NLP) in VS Code and restart any old kernel. Local execution does not establish instructor acceptance as a replacement for the original Colab instructions. No submission package, Blackboard upload, independent Verifier or Reviewer execution performed. An independent future verifier should use the exact current source hash, check all task outputs and repeat the self-checks; a distinct reviewer can inspect the actual candidate package if later requested.
