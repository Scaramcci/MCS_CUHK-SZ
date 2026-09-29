# DDA5001 HW1 final-candidate assembly record

Executor: current Codex conversation. Teacher source: requirements/DDA5001_HW1.pdf, pp. 1–9. This is an author/packager record, not an independent Reviewer conclusion.

## Conversation evidence

The original conversation records the P3/P5 predictions before verification, followed by four user result-based questions and four agent replies: P3 branch values, P3 directional differences, P5 seven-row toy trace, and P5 full-trajectory pocket test-error rises. Four partial screenshots under results/AI-help-prove/ show the follow-ups; text outside a screenshot was checked against the original conversation, not inferred from the image. Screenshots show the interface model as GPT-6 Astra. The two English cases occupy separate final-PDF pages 5 and 6. report/ai-collaboration.md remains a working draft and is excluded from the package.

## Source and output versions

- Teacher PDF SHA-256: 77b4320e4bd3125a6b74dc8d17c7536b0b91b4a2bc1e47b983713e4fda1c6b35.
- Teacher code ZIP SHA-256: 78bfb004a231838ffd60e136afad13aba6f61437790673edd950020b77e8721a.
- src/p3.py SHA-256: 572425d021d603deaf553c136e26a999690043af529191991b022a2843ccf6ae.
- src/p5.py SHA-256: 27636fe419d3c156b4157049d8916e3ed27e677e30bd2b5aef834b328e104065.
- Current report/main.tex SHA-256: 42c323ddda902894e062a7c29161fc5af2b33959c0426e5f604e80dad1ca7627.
- Current report/DDA5001_HW1_answers.pdf SHA-256: 508ab4e00714192850e3261a8c7fb4fa70f58ce80de3950988a60702cbc07892.
- Prior independent technical verification: notes/verification.md, bound to unchanged code hashes.

## Compilation and visual check

Built-in LaTeX editor failed because its Tectonic bundle was not cached and network retrieval failed. Local XeLaTeX succeeded. From report/, the actual final command was:

```sh
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build-final-20260929 main.tex
```

Ten actual compiler invocations are recorded in report/build-final-20260929/ or /tmp/dda5001-final-pass9.stdout. The final pass10 exit was 0, with six A4 pages, no LaTeX errors, unresolved references, or overfull boxes. The PDF was rendered with pdftoppm and all six pages were visually checked on the prior version; after the final identity addition, page 1 was re-rendered and inspected. Page 1 displays Kunyuan Zhong and student ID 226040255, as provided by the student. P3(e) is page 5 and P5(e) page 6, one page each. A text scan found no Draft, template, TODO, or placeholder content.

## Numeric and package checks

Current result CSV row counts: P3 baseline 1001; P5 trajectory 2001; toy trace 7. Final P3 parameter error 5.618720155342013; P5 pocket train/test 0.03235470341521869 / 0.06451612903225806. Pocket train error is nonincreasing in the saved full trajectory. The teacher PDF and original code ZIP hashes remain unchanged.

The exact 17-file archive is submission/Zhong-Kunyuan-hw1.zip, SHA-256 1e5ebf2b5b0dd236c277bb27a1f89c1814f3e0189538f48b0a37418453e249b6. Per-entry SHA-256 values are in /tmp/dda5001-hw1-stage-manifest-v3.json. ZipFile testzip and per-entry checks passed. It contains the final PDF, two completed .py files, P3 verification and baseline outputs, and P5 toy and full-trajectory outputs. It excludes teacher originals, input data, screenshots, Markdown, logs, caches and LaTeX auxiliary files.

The independent Reviewer initially found that extracting the ZIP alone leaves the scripts without the teacher's original input data. The PDF now explicitly states how to provide those separately supplied data through the script flags and distinguishes reuse instructions from the actual recorded runs. The final named ZIP is pending exact-archive independent review.

## Pending

Independent Reviewer /root/review_hw1 is checking the exact named archive. The student reserved personal review of P1/P2/P4 English wording. Any candidate change invalidates the affected review.
