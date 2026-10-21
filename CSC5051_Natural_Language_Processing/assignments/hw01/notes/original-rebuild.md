# Original-template rebuild, 2026-10-21

Role/executor: primary session, Planner/Implementer; checks are self-checks, not independent verification.

User request: start from the original notebook, not the expanded 2026-10-10 implementation. Source: results/input-snapshot/26Fall_NLP_Assignment_1_CSC6052_5051_MDS5110.ipynb. Original PDF: requirements/Assignment_1.pdf p.1 §§1–4. Earlier implementation and local input files backed up in local_artifacts/before-original-rebuild-20261021T112415Z/; original and prior evidence retained.

User-provided instructor clarifications (2026-10-21): (1) CBOW context sum or average accepted; choose average. (2) Task 2.1 compares Task 2 plot with the Task 1 ending CBOW visualization, discussing clustering/training corpus. (3) Task 2 may use glove-twitter-25 or word2vec-google-news-300; choose and explicitly state glove-twitter-25.

Plan: preserve all teacher source outside task regions, plus use original empty cell 2 for random seeds. Fill task bodies without rewriting helper functions, loops, parameters, paths or plotting. Keep original installation/download cell; adapt local NLP environment to its Bokeh 3.2.0 via NumPy 1.26.4. Execute all cells using notes/execute_original.py, which only configures the launch environment and saves evidence. Inspect new outputs/plots, then fill English answer cells. Compare sources against original, and test numerical task functions. Do not reuse old run outputs or old Task 2.1 explanation. Personal fields remain blank.

Expected source changes (zero-based cells): 2 for seeds; task code 23,27,31,45,53,56,71,74,81,88; answer markdown 51,54,57,90. Kernel metadata set to nlp. All other cell sources must exactly match the original. No final submission package or upload.

## Completed run and self-check

Actual command from hw01:

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 /home/scarramcci/miniconda3/envs/NLP/bin/python -s -u notes/execute_original.py
```

Exit 0. Evidence: results/original_20261021T112508_726671Z/ (input.ipynb, executed.ipynb, status.json, packages.txt, answered.ipynb, final-audit.json). Console: results/original-rebuild-console-20261021.txt. All 39 code cells executed with no error outputs. Original download/unzip ran successfully; train.csv SHA256 matches the pre-existing supplied data (5f28dbe0bb01b39a793f36567d18fe7cf34d20bbca69ff85b131d7c2186f9914). The final answer edit changed only four markdown cells; final code and outputs match the executed snapshot exactly.

Original batch/forward/SVD/sentence/retrieval checks ran via `env -u PYTHONPATH PYTHONNOUSERSITE=1 /home/scarramcci/miniconda3/envs/NLP/bin/python -s tests/self_check.py`, exit 0; log results/original-rebuild-self-check-20261021.txt. This uses small analytic test fixtures, not replacement assignment data. Isolated NLP `python -s -m pip check` also passed.

Kept original 50,000 texts, window=2, MIN_COUNT=5, embedding_dim=32, learning_rate=.001, batch_size=128, 4 epochs. Original logging prints 3,000-step interval mean losses 6.4641, 5.5298, 5.2280, 5.0397; these are not epoch averages. No new training checkpoint is required or saved by the original code. Python random/Torch seeds in original empty cell 2 are 42; original NumPy seed remains 42. Hardware is the local NVIDIA RTX 4090 Laptop GPU. Exact installed versions are in packages.txt. Torch/CUDA results can vary across machines; no clean-room or independent validation claim.

Viewed Task 2's saved PNG and a diagnostic PNG drawn from the exact serialized Bokeh ColumnDataSource coordinates of Task 1 (not a new t-SNE fit). Images are in the run evidence directory. Original float32 `scale` issues numerical precision warnings, but all plotted coordinates were finite. The original helper code and interactive visualization remain unchanged.

Final source audit: 93 original cells; 78 unchanged; changed zero-based indices 2,23,27,31,45,51,53,54,56,57,71,74,81,88,90. All teacher code outside the task markers is byte-for-byte identical at source-string level. Empty cell 2 contains only reproducibility imports/seeds. Metadata selects Python (NLP). Final notebook is 157,466 bytes; SHA256 e347d39654b83f957a2e86bb89b01645e53d265eb1e0334da16a88da5a82d96a. No personal fields were filled.

Task 2.1 now directly compares visible CBoW grammatical neighborhoods (pronouns, modal verbs, question words) with GloVe's partial topical clustering, and discusses Quora vs Twitter and t-SNE vs SVD. It does not repeat the prior 'missing co-occurrence figure' answer. Model choice is explicitly stated as glove-twitter-25. Other written responses use the new run's numerical outputs.

Status: rebuilt, run, implementation self-check passed; independent Verifier/Reviewer not run. No submission package assembled or uploaded. Next: student supplies personal fields and reviews the answers; independent review can inspect this exact notebook hash if requested.
