"""Independent branch-boundary and sum/mean checks for HW1 P3."""
import json
import sys
from pathlib import Path

import numpy as np

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here.parents[2] / "src"))
import p3

result = []
for mu in (1., 1e-5):
    x = np.ones((7, 1))
    residual = mu * np.array([-2., -1., -.5, 0., .5, 1., 2.])
    derivatives = [float(p3.huber_gradient([z], [[1.]], [0.], mu)[0]) for z in residual]
    np.testing.assert_allclose(derivatives, [-1, -1, -.5, 0, .5, 1, 1], atol=1e-12)
    X = np.array([[1., 0.], [0., 1.], [1., 1.], [1., -1.], [1., 2.]])
    y = -mu * np.array([-2., -.5, 0., .5, 2.])
    theta = np.zeros(2)
    sum_gradient = p3.huber_gradient(theta, X, y, mu)
    mean_gradient = X.T @ np.clip((X @ theta-y)/mu, -1, 1) / len(y)
    np.testing.assert_allclose(mean_gradient, sum_gradient / 5, atol=1e-12)
    result.append({"mu": mu, "residual_over_mu": [-2, -1, -.5, 0, .5, 1, 2],
                   "derivatives": derivatives, "sum_gradient": sum_gradient.tolist(),
                   "mean_gradient": mean_gradient.tolist(), "sample_count": len(y)})
(here / "p3_scaling.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
