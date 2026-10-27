"""Small fitting/error checks for P3, independent of the full grid experiment.

Run from any directory: python /path/to/p3/verify.py [--output checks.json]
The supplied polynomials are deterministic verification examples only.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
from numpy.polynomial.legendre import leggauss, legval, legvander

from algorithms import fit_polynomial, population_error


def run_checks():
    x = np.linspace(-.95, .95, 40)
    truth = np.array([.3, -.7, .2])
    labels = legval(x, truth)
    checks = {}
    for degree in (2, 10):
        design = legvander(x, degree)
        old_design, old_labels = design.copy(), labels.copy()
        expected = np.pad(truth, (0, degree - 2))
        computed = fit_polynomial(design, labels)
        error = float(np.max(np.abs(computed - expected)))
        risk = float(population_error(computed, truth))
        unchanged = np.array_equal(design, old_design) and np.array_equal(labels, old_labels)
        checks[f"noiseless_degree_{degree}"] = {
            "expected_coefficients": expected.tolist(), "computed_coefficients": computed.tolist(),
            "max_absolute_difference": error, "coefficient_tolerance": 1e-11,
            "expected_population_error": 0., "computed_population_error": risk,
            "risk_tolerance": 1e-20, "inputs_unchanged": unchanged,
            "passed": computed.shape == expected.shape and error < 1e-11 and risk < 1e-20 and unchanged,
        }

    w, target = np.array([.5, -.3, .2]), np.array([.1, .2, -.1, .4])
    nodes, weights = leggauss(80)
    residual = legval(nodes, w) - legval(nodes, target)
    numerical = float(np.sum(weights * residual**2) / 2)
    analytic = float(population_error(w, target))
    expected = .4**2 + .5**2 / 3 + .3**2 / 5 + .4**2 / 7
    checks["independent_quadrature"] = {
        "model_coefficients": w.tolist(), "target_coefficients": target.tolist(),
        "expected_weighted_coefficient_error": expected,
        "computed_analytic_error": analytic, "computed_80_point_gauss_legendre_error": numerical,
        "absolute_difference": abs(analytic - numerical), "tolerance": 1e-10,
        "passed": abs(analytic - numerical) < 1e-10 and abs(analytic - expected) < 1e-14,
    }
    scalar_cases = [
        ("constant_density", np.array([2.]), np.array([1.]), 1.),
        ("target_tail", np.array([0.]), np.array([0., 0., 0., 2.]), 4 / 7),
        ("model_tail", np.array([0., 0., 3.]), np.array([0.]), 9 / 5),
        ("already_normalized", np.array([0.]), np.array([0., 1 / np.sqrt(1 + 1 / 3)]), .25),
    ]
    for name, model, target, expected in scalar_cases:
        computed = float(population_error(model, target))
        checks[name] = {"expected": expected, "computed": computed, "tolerance": 1e-14,
                        "passed": abs(computed - expected) < 1e-14}

    design = legvander(x, 4)
    expected_fit = np.array([[.3, .1, -.2], [-.7, .4, .3], [.2, 0., -.1], [0., .2, 0.], [0., 0., .05]])
    labels_batch = design @ expected_fit
    old_design, old_labels = design.copy(), labels_batch.copy()
    batch = fit_polynomial(design, labels_batch)
    columnwise = np.column_stack([fit_polynomial(design, labels_batch[:, j]) for j in range(3)])
    model_batch = np.array([[1., 2.], [.2, -.3]])
    target_batch = np.array([[1.5, 1.], [0., 0.], [.7, -.5]])
    old_model, old_target = model_batch.copy(), target_batch.copy()
    batch_risks = population_error(model_batch, target_batch)
    expected_risks = np.array([.5**2 + .2**2 / 3 + .7**2 / 5, 1 + .3**2 / 3 + .5**2 / 5])
    fit_difference = float(np.max(np.abs(batch - expected_fit)))
    column_difference = float(np.max(np.abs(batch - columnwise)))
    risk_difference = float(np.max(np.abs(batch_risks - expected_risks)))
    unchanged = all(np.array_equal(current, before) for current, before in
                    ((design, old_design), (labels_batch, old_labels),
                     (model_batch, old_model), (target_batch, old_target)))
    checks["batched_columns"] = {
        "design_shape": list(design.shape), "label_shape": list(labels_batch.shape),
        "expected_fit_shape": [5, 3], "computed_fit_shape": list(batch.shape),
        "expected_fit": expected_fit.tolist(), "computed_fit": batch.tolist(),
        "fit_max_absolute_difference": fit_difference,
        "separate_fit_max_absolute_difference": column_difference,
        "expected_risks": expected_risks.tolist(), "computed_risks": batch_risks.tolist(),
        "computed_risk_shape": list(batch_risks.shape), "risk_max_absolute_difference": risk_difference,
        "tolerance": 1e-11, "inputs_unchanged": unchanged,
        "passed": batch.shape == (5, 3) and batch_risks.shape == (2,)
                  and fit_difference < 1e-11 and column_difference < 1e-11
                  and risk_difference < 1e-14 and unchanged,
    }
    return {
        "problem": 3, "purpose": "Deterministic verification examples, not experiment data",
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
