# P3(a): prediction recorded before implementation and experiments

Executor: /root, AI-assisted draft, 2026-10-29. This is the assistant's recorded prediction, not a claim that the student independently wrote it. Recorded before running any HW3 model check or training.

B is affine: W2(W1 x + b1) + b2 = (W2 W1)x + W2 b1 + b2. Its effective matrix has rank at most 64, but every 10-by-784 matrix has rank at most 10, so this hidden width can represent every affine input-to-logit map in A. Factorization changes optimization and parameterization, so equal function classes do not imply identical learned weights or accuracies.

C introduces a ReLU between the two affine layers. Different activation patterns allow different affine pieces, so C can express nonlinear input-to-logit maps. B and C have equal dimensions, biases and parameter counts; their matched comparison isolates the architectural addition of ReLU under the prescribed training protocol. I expect this extra expressiveness to help represent digit patterns, but do not predict exact accuracy or guarantee a ranking/overfitting pattern from a single seed.

Actual initial user request: 请帮我完成 [hw03](DDA5001_Machine_Learning/assignments/hw03/) ，可以参考前面的作业的完成形式和 [AGENTS.md](AGENTS.md)
Actual follow-up after replacing the files: 现在你再看一下
The original interaction remains in this Codex chat. Do not represent the assistant's planning or independent agents' checks as student-authored prompts.
