# DDA5001 Homework 3

Contents: one seven-page English answer PDF; completed p1/p1.py, p2/p2.py and p3/p3.py; the original per-problem requirements; an exact environment lock; and unchanged teacher inputs at their original relative paths. Only the eight marked TODO bodies were completed. All figures and requested result tables are in the PDF. The report transparently discloses AI assistance and the actual construction interaction; student understanding and own-word review remain required before submission.

## Reproduce

Tested with Python 3.12.14 on Linux x86-64, CPU. From this extracted folder, create an environment and install the exact tested versions:

```bash
python3.12 -m venv .venv
env -u PYTHONPATH .venv/bin/python -m pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements-frozen.txt
env -u PYTHONPATH OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python p1/p1.py
env -u PYTHONPATH OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python p2/p2.py
env -u PYTHONPATH OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python p3/p3.py --check-models
env -u PYTHONPATH OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python p3/p3.py
```

These commands produce outputs/ beside each problem script. For a separate repeat, append `--output-dir path/to/a/new/folder`. The supplied MNIST loader downloads official images on first use; internet is needed for dependencies and this download. It verifies the provided fixed split against the official label ordering. The training/validation/test sizes are 6000/2000/2000, seed 666, 30 epochs, batch 128, SGD learning rate 0.1, momentum 0.9, CPU one thread; settings and code outside TODOs are unchanged.

Teacher data included: p1/data/{training,test}.csv, p2/data/p2/ORL_faces/s1..s40/1..10.pgm, p3/data/p3/mnist_split_indices.npz. Their source is the supplied code_source(2).zip. MNIST is not bundled, but is cached by torchvision under p3/data/mnist. No model checkpoints are required. These datasets and the final ZIP are local files, excluded from repository tracking. Local retention is not an independent backup.

Expected results (rounded): P1 lambda=0.01; baseline train/test MSE=0.00090436/2.08003393; selected=0.00933397/0.04021308. P2 k20/k100 whole-data MSE=0.00734732/0.00271577. P3 selected epochs A9/B4/C14, test accuracies 91.45%/90.80%/95.20%; validation prefers C. Different numerical platforms can introduce small differences. No external submission has been performed.
