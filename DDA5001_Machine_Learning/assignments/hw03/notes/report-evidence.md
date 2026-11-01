# Report evidence and author checks

Report Writer: /root, also the source author. This is self-review, not independent approval. Source report/main.tex; figures copied without alteration from results/run-20261029. Final PDF compiled with local XeLaTeX; v1 retained an orphan caption; v2 fixed pagination, v3 fixed a small quote overfull box. Actual logs in results/report-build-v{1,2,3}. Built-in Tectonic could not acquire its bundle; failure retained. Current PDF has 7 pages and no overfull/underfull or undefined-reference warnings; harmless caption hypcap warnings remain. All pages visually inspected in v2, with page7 reinspection after the only v3 change. No numerical/code changes after independent verification.

| Report | Source evidence |
|---|---|
| P1 derivative/scaling/folds | Teacher PDF pp1–3; src/p1/p1.py; independent verification |
| P1 table, lambda, plots | results/run-20261029/p1/{summary.json,cross_validation.csv,validation.png,fits.png} |
| P2 construction/projection | Teacher PDF pp4–5; src/p2/p2.py; independent verification |
| P2 MSE and grids | results/run-20261029/p2/{summary.json,eigenfaces.png,reconstruction.png} |
| P3 before-run prediction | notes/pre-run-prediction.md, recorded before checks/training and hashed by run recorder |
| P3 model counts/checks | src/p3/p3.py; results/self-checks/{provided-model-check.txt,all-after.stderr.txt}; independent verification |
| P3 selected/last-epoch metrics | results/run-20261029/p3/{manifest.json,A_history.csv,B_history.csv,C_history.csv} |
| P3 curves and selection | results/run-20261029/p3/{architecture_curves.png,selection_before_test.json} |
| P3(d) actual interaction | notes/ai-collaboration.md and retained original chat; translations labeled |

Current candidate inventory/hash: results/submission-manifests/candidate-v1.json. Student personal review/own wording is not certified. Next role: independent Reviewer distinct from author and Verifier; inspect exact PDF/ZIP and decide artifact readiness with the personal step explicitly separated.
