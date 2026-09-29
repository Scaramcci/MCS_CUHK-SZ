"""Compare the original teacher MAT arrays against experiment NPZ copies."""
import json
from pathlib import Path
import numpy as np
from scipy.io import loadmat

here = Path(__file__).resolve().parent
hw = here.parents[2]
original = hw / "requirements/code_source/code_source/p5"
copies = hw / "results/input-conversion-20260929"
result = {}
for split in ("train", "test"):
    mat = loadmat(original / f"{split}_data.mat")["zip"]
    with np.load(copies / f"{split}_data.npz") as archive:
        npz = archive["zip"]
    result[split] = {"shape": list(mat.shape), "dtype": str(mat.dtype),
                     "bitwise_equal": bool(np.array_equal(mat, npz, equal_nan=True)),
                     "max_absolute_difference": float(np.max(np.abs(mat - npz)))}
    assert result[split]["bitwise_equal"]
(here / "mat_equivalence.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
