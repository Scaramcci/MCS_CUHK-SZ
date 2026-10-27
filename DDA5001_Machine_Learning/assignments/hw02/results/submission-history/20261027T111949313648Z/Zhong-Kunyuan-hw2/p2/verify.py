"""Small numerical checks for P2; no dataset download or experiment run.

Run from any directory: python /path/to/p2/verify.py [--output checks.json]
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform

import numpy as np

import algorithms as alg


def run_checks():
    X = np.array([[1., -1., 1.], [2., .5, 1.], [-1., 2., 1.], [.5, .2, 1.]])
    Y = np.eye(3)[[0, 1, 2, 1]]
    theta = np.array([[.1, -.2, .05], [.3, -.1, .2], [.02, .1, -.1]])
    previous = theta - .02
    originals = [item.copy() for item in (X, Y, theta, previous)]
    epsilon = 1e-6
    analytic = alg.gradient(theta, X, Y)
    numerical = np.empty_like(theta)
    for index in np.ndindex(theta.shape):
        plus, minus = theta.copy(), theta.copy()
        plus[index] += epsilon
        minus[index] -= epsilon
        numerical[index] = (alg.cross_entropy(X @ plus, Y)
                            - alg.cross_entropy(X @ minus, Y)) / (2 * epsilon)
    gradient_difference = float(np.max(np.abs(analytic - numerical)))
    checks = {
        "gradient": {
            "X": X.tolist(), "Y": Y.tolist(), "theta": theta.tolist(),
            "epsilon": epsilon, "analytic": analytic.tolist(),
            "central_difference": numerical.tolist(),
            "max_absolute_difference": gradient_difference, "tolerance": 1e-8,
            "passed": gradient_difference < 1e-8,
        }
    }
    for method in ("momentum", "nesterov"):
        points = []

        def grad_fn(point):
            points.append(point.copy())
            return 2 * point

        if method == "momentum":
            actual = alg.momentum_step(theta, previous, .05, .90, grad_fn)
            expected_point = theta.copy()
            expected_update = .9 * theta + .018
        else:
            actual = alg.nesterov_step(theta, previous, .05, 3, grad_fn)
            expected_point = theta + .008
            expected_update = .9 * expected_point
        point_difference = float(np.max(np.abs(points[0] - expected_point)))
        update_difference = float(np.max(np.abs(actual - expected_update)))
        checks[method] = {
            "previous": previous.tolist(), "learning_rate": .05,
            "beta": .90 if method == "momentum" else None,
            "k": 3 if method == "nesterov" else None,
            "gradient": "G(A) = 2A", "gradient_calls": len(points),
            "expected_gradient_point": expected_point.tolist(),
            "computed_gradient_point": points[0].tolist(),
            "expected_update": expected_update.tolist(), "computed_update": actual.tolist(),
            "point_max_absolute_difference": point_difference,
            "update_max_absolute_difference": update_difference,
            "tolerance": 1e-14,
            "passed": len(points) == 1 and point_difference < 1e-14 and update_difference < 1e-14,
        }

    logits = np.array([[1000., 1001., 999.], [-1000., -1001., -999.]])
    probabilities = alg.softmax(logits)
    expected_gd = .9 * theta
    actual_gd = alg.gd_step(theta, .05, lambda point: 2 * point)
    stable_loss = alg.cross_entropy(np.array([[1000., -1000.]]), np.array([[0., 1.]]))
    zero_loss = alg.cross_entropy(np.zeros_like(Y), Y)
    first = [alg.gd_step(theta, .05, lambda point: alg.gradient(point, X, Y)),
             alg.momentum_step(theta, theta.copy(), .05, .90, lambda point: alg.gradient(point, X, Y)),
             alg.nesterov_step(theta, theta.copy(), .05, 1, lambda point: alg.gradient(point, X, Y))]
    first_difference = max(float(np.max(np.abs(item - first[0]))) for item in first)
    checks["additional_checks"] = {
        "extreme_softmax": probabilities.tolist(),
        "probability_row_sums": probabilities.sum(axis=1).tolist(),
        "shift_invariance_max_difference": float(np.max(np.abs(probabilities - alg.softmax(logits + 17.)))),
        "extreme_wrong_class_loss_expected": 2000., "extreme_wrong_class_loss_computed": stable_loss,
        "zero_logit_loss_expected": float(np.log(3)), "zero_logit_loss_computed": zero_loss,
        "gd_expected_update": expected_gd.tolist(), "gd_computed_update": actual_gd.tolist(),
        "first_update_max_difference": first_difference,
        "passed": bool(np.isfinite(probabilities).all()
                       and np.allclose(probabilities.sum(axis=1), 1., atol=1e-14, rtol=0)
                       and np.allclose(probabilities, alg.softmax(logits + 17.), atol=1e-14, rtol=0)
                       and abs(stable_loss - 2000.) < 1e-10
                       and abs(zero_loss - np.log(3)) < 1e-13
                       and np.allclose(actual_gd, expected_gd, atol=1e-14, rtol=0)
                       and first_difference < 1e-14),
    }
    unchanged = all(np.array_equal(item, before)
                    for item, before in zip((X, Y, theta, previous), originals))
    checks["input_nonmutation"] = {"passed": unchanged}
    return {
        "problem": 2, "purpose": "Small verification examples, not experiment data",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "numpy": np.__version__,
        "source_sha256": {name: hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest()
                          for name in ("algorithms.py", "verify.py")},
        "checks": checks, "all_passed": all(item["passed"] for item in checks.values()),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    result = run_checks()
    payload = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    raise SystemExit(0 if result["all_passed"] else 1)
