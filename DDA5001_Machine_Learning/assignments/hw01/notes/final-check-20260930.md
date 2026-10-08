# Final candidate spot-check — 2026-09-30

Scope: read-only check of `submission/Zhong-Kunyuan-hw1.zip`, teacher HW1 PDF, existing implementation/results, and the extracted candidate PDF. This is an additional spot-check, not a replacement for the independent review in `notes/review.md`. The student has reserved final personal review of wording and identity.

## Candidate and checks

- Archive SHA-256: `1e5ebf2b5b0dd236c277bb27a1f89c1814f3e0189538f48b0a37418453e249b6`.
- ZIP integrity check passed; 17 entries. Every archived member was compared byte-for-byte with its corresponding working file, including the final PDF and both Python scripts.
- The archived PDF has six A4 pages. All six pages were rendered and visually inspected. P1–P5 are present; P3(e) is page 5 and P5(e) is page 6, satisfying the one-page-each layout. No visible Draft label, placeholder, clipping, or missing figure was found. PDF text includes actual run commands and the explanation that P5 used an exact `.npz` copy of the teacher `.mat` arrays.
- Fresh P3 and P5 baseline invocations against the current source exited 0. P3 and P5 summary JSON and the relevant CSV files reproduced byte-for-byte; P3 final parameter arrays matched exactly. These checks used the existing `.npz` conversion for P5 and did not independently run the default `.mat` loader in a unified SciPy/Matplotlib environment.
- `notes/review.md` records a separate independent Reviewer assessment of this exact named archive with no remaining content issue, subject to the student's personal review.

## Remaining student decisions

1. Confirm the displayed name, student ID, and `Zhong-Kunyuan-hw1.zip` spelling/order are correct.
2. Read and approve or rewrite P1, P2 and P4 in the student's own understanding and words, as reserved in the task and required by the handout's general instructions.
3. Read P3 and P5 explanations, figures, numerical values, and AI cases; confirm that the case descriptions match the original full agent conversation and that the conversation remains retrievable. The saved screenshots are partial.
4. Confirm the latest Blackboard deadline/timezone and any submission-specific instructions. Upload the exact named ZIP and verify Blackboard shows it as the latest submission.

If any PDF, source, result, or archive file is changed after this check, the affected validation and exact-package review need repeating.
