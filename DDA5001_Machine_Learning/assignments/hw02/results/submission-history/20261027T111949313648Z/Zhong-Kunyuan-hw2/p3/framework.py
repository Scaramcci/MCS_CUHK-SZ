"""Provided data generation, experiment bookkeeping, and plotting for HW2 P3.

Leave this file unchanged for the required experiment. Implement only the
two functions in algorithms.py. There is no external data download.
Every grid cell contains 1,000 ordinary simulated trials; trials are
independent. Common random numbers are reused ACROSS grid settings to
make comparisons less noisy. This is not conditional-expectation averaging.
"""

import csv
import hashlib
import json
import os
import platform
from pathlib import Path
import time

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).parent / "mpl_cache"))

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np
from numpy.polynomial.legendre import legvander
from threadpoolctl import threadpool_limits

from algorithms import fit_polynomial, population_error

SEED = 666
TRIALS = 1000
SAMPLE_COUNTS = np.arange(20, 121, 5)
TARGET_DEGREES = np.arange(1, 51)
NOISE_VARIANCES = np.arange(41) * 0.05
FIXED_VARIANCE = 0.1
FIXED_TARGET_DEGREE = 20
COLOR_LIMIT = 0.25  # display saturation ONLY; all raw values are retained


def generate_random_bank():
    """Generate all randomness once; each row is one independent trial.

    For a given n use the first n inputs/noises; for Q_g use the first
    Q_g+1 coefficients. The same data are used by the two fitted models.
    The order, shapes, and seed are fixed so every student gets the same
    simulated data. Do not generate new randomness inside the grid loops.
    """
    rng = np.random.default_rng(SEED)
    x = rng.uniform(-1.0, 1.0, size=(TRIALS, int(SAMPLE_COUNTS[-1])))
    epsilon = rng.normal(size=x.shape)
    a = rng.normal(size=(TRIALS, int(TARGET_DEGREES[-1])+1))
    normalizers = np.sqrt(np.cumsum(1.0 / (2*np.arange(a.shape[1])+1)))
    return x, epsilon, a, normalizers


def generate_trial(x, epsilon, a, normalizers):
    """Return designs, labels, and oracle target coefficients for one trial.

    The first 50 label columns have Q_g=1,...,50 at variance 0.1.
    The last 41 have Q_g=20 at variances 0,0.05,...,2.
    Batching label columns only saves work; each column is a separate fit.
    Oracle coefficients go ONLY to population_error, never to the fitter.
    Evaluate Legendre polynomials directly, not by expanding into x powers.
    """
    degrees = np.arange(len(a))
    raw_design = legvander(x, len(a)-1)
    target_q = np.cumsum(raw_design*a, axis=1)[:, 1:] / normalizers[1:]
    labels_q = target_q + np.sqrt(FIXED_VARIANCE)*epsilon[:, None]
    labels_v = (target_q[:, FIXED_TARGET_DEGREE-1, None]
                + epsilon[:, None]*np.sqrt(NOISE_VARIANCES))
    truth_q = (a[:, None]/normalizers[1:]
               * (degrees[:, None] <= TARGET_DEGREES))
    truth_v = np.repeat(truth_q[:, FIXED_TARGET_DEGREE-1, None],
                        len(NOISE_VARIANCES), axis=1)
    return raw_design, np.concatenate((labels_q, labels_v), axis=1), np.concatenate((truth_q, truth_v), axis=1)


def _array_hash(array):
    canonical = np.ascontiguousarray(array, dtype="<f8")
    return hashlib.sha256(canonical.tobytes()).hexdigest()


def _save_csv(path, axis_name, axis_values, rho_trials):
    means = rho_trials.mean(axis=0)
    standard_errors = rho_trials.std(axis=0, ddof=1)/np.sqrt(TRIALS)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["n", axis_name, "mean_rho", "standard_error", "trials"])
        for ni, n in enumerate(SAMPLE_COUNTS):
            for ji, value in enumerate(axis_values):
                writer.writerow([int(n), value, float(means[ni, ji]),
                                 float(standard_errors[ni, ji]), TRIALS])


def _panel(ax, vertical, mean_rho, title, ylabel):
    mesh = ax.pcolormesh(SAMPLE_COUNTS, vertical, mean_rho.T,
                         shading="nearest", cmap="RdBu_r",
                         norm=TwoSlopeNorm(vmin=-COLOR_LIMIT, vcenter=0,
                                           vmax=COLOR_LIMIT))
    if mean_rho.min() < 0 < mean_rho.max():
        ax.contour(SAMPLE_COUNTS, vertical, mean_rho.T, levels=[0],
                   colors="black", linewidths=1.4)
    ax.set(title=title, xlabel="Number of training points n", ylabel=ylabel)
    ax.set_xticks([20, 40, 60, 80, 100, 120])
    ax.set_xlim(20, 120)
    ax.set_ylim(float(vertical[0]), float(vertical[-1]))
    return mesh


def save_plots(output_dir, mean_q, mean_v):
    """Plot the arithmetic mean; no smoothing, outlier removal, or interpolation."""
    plt.rcParams.update({"font.size": 12, "axes.titlesize": 13})
    panels = [(TARGET_DEGREES, mean_q, r"Noise variance $\sigma^2=0.1$",
               r"Target degree $Q_g$", "target_complexity.png"),
              (NOISE_VARIANCES, mean_v, r"Target degree $Q_g=20$",
               r"Noise variance $\sigma^2$", "noise_variance.png")]
    for vertical, values, title, ylabel, filename in panels:
        fig, ax = plt.subplots(figsize=(6.8, 4.4), layout="constrained")
        mesh = _panel(ax, vertical, values, title, ylabel)
        colorbar = fig.colorbar(mesh, ax=ax, extend="both")
        colorbar.set_label(r"Mean $\rho_e=E_{out}(f_{10})-E_{out}(f_2)$")
        fig.suptitle("1,000 trials | seed 666 | black line: mean = 0", fontsize=11)
        fig.savefig(output_dir/filename, dpi=200)
        plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 4.7), layout="constrained")
    for ax, (vertical, values, title, ylabel, _) in zip(axes, panels):
        mesh = _panel(ax, vertical, values, title, ylabel)
    colorbar = fig.colorbar(mesh, ax=axes, extend="both")
    colorbar.set_label(r"Mean $\rho_e$ (red: $f_{10}$ worse; blue: $f_{10}$ better)")
    fig.suptitle("1,000 trials | seed 666 | black line: mean = 0 | color saturation at +/-0.25", fontsize=12)
    fig.savefig(output_dir/"comparison.png", dpi=200)
    plt.close(fig)


def run_experiment(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    x, epsilon, a, normalizers = generate_random_bank()
    shape_q = (TRIALS, len(SAMPLE_COUNTS), len(TARGET_DEGREES))
    shape_v = (TRIALS, len(SAMPLE_COUNTS), len(NOISE_VARIANCES))
    rho_q, rho_v = np.empty(shape_q), np.empty(shape_v)
    risk2_q20 = np.empty((TRIALS, len(SAMPLE_COUNTS)))
    risk10_q20 = np.empty_like(risk2_q20)
    max_training_error_violation = 0.0
    min_design_singular_value = float("inf")

    # One numerical-library thread keeps runs repeatable and avoids overhead.
    with threadpool_limits(limits=1):
        for trial in range(TRIALS):
            design, labels, truth = generate_trial(x[trial], epsilon[trial], a[trial], normalizers)
            for ni, n in enumerate(SAMPLE_COUNTS):
                y = labels[:n]
                fitted = {}
                errors = {}
                training_errors = {}
                for degree in (2, 10):
                    matrix = design[:n, :degree+1]
                    w = np.asarray(fit_polynomial(matrix, y))
                    if w.shape != (degree+1, labels.shape[1]):
                        raise ValueError("fit_polynomial returned an incorrect coefficient shape.")
                    risk = np.asarray(population_error(w, truth))
                    if risk.shape != (labels.shape[1],) or not np.isfinite(risk).all() or (risk < 0).any():
                        raise ValueError("population_error must return finite nonnegative column-wise risks.")
                    fitted[degree], errors[degree] = w, risk
                    training_errors[degree] = np.mean((matrix@w-y)**2, axis=0)
                violation = np.max(training_errors[10]-training_errors[2])
                max_training_error_violation = max(max_training_error_violation, float(violation))
                if violation > 1e-8*max(1.0, float(np.max(training_errors[2]))):
                    raise ArithmeticError("The degree-10 training fit is worse than the nested degree-2 fit.")
                # Record conditioning without changing, rejecting, or regularizing a trial.
                smallest = np.linalg.svd(design[:n, :11], compute_uv=False)[-1]
                min_design_singular_value = min(min_design_singular_value, float(smallest))
                rho = errors[10]-errors[2]
                rho_q[trial, ni] = rho[:len(TARGET_DEGREES)]
                rho_v[trial, ni] = rho[len(TARGET_DEGREES):]
                risk2_q20[trial, ni] = errors[2][FIXED_TARGET_DEGREE-1]
                risk10_q20[trial, ni] = errors[10][FIXED_TARGET_DEGREE-1]
            if (trial+1) % 100 == 0:
                print(f"Problem 3: {trial+1}/{TRIALS} trials complete", flush=True)

    mean_q, mean_v = rho_q.mean(axis=0), rho_v.mean(axis=0)
    # Keep every trial, including rare very large errors. Only plots saturate.
    np.savez_compressed(output_dir/"trial_values.npz", rho_q=rho_q, rho_v=rho_v,
                        risk2_q20=risk2_q20, risk10_q20=risk10_q20)
    np.savez_compressed(output_dir/"grid_means.npz", ns=SAMPLE_COUNTS, qs=TARGET_DEGREES,
                        variances=NOISE_VARIANCES, mean_q=mean_q, mean_v=mean_v)
    _save_csv(output_dir/"target_complexity.csv", "Q_g", TARGET_DEGREES, rho_q)
    _save_csv(output_dir/"noise_variance.csv", "sigma_squared", NOISE_VARIANCES, rho_v)
    save_plots(output_dir, mean_q, mean_v)
    summary = {
        "seed": SEED, "trials_per_cell": TRIALS,
        "Q20_sigma_squared_0.1": [
            {"n": int(n), "mean_Eout_f2": float(risk2_q20[:, ni].mean()),
             "mean_Eout_f10": float(risk10_q20[:, ni].mean()),
             "mean_rho": float(mean_q[ni, FIXED_TARGET_DEGREE-1])}
            for ni, n in enumerate(SAMPLE_COUNTS)],
        "max_training_error_violation": max_training_error_violation,
        "min_degree10_design_singular_value": min_design_singular_value,
        "rho_q_range": [float(mean_q.min()), float(mean_q.max())],
        "rho_v_range": [float(mean_v.min()), float(mean_v.max())],
        "all_trials_retained": True,
    }
    manifest = {
        "seed": SEED, "trials_per_cell": TRIALS,
        "sample_counts": SAMPLE_COUNTS.tolist(), "target_degrees": TARGET_DEGREES.tolist(),
        "noise_variances": NOISE_VARIANCES.tolist(),
        "fixed_noise_variance": FIXED_VARIANCE, "fixed_target_degree": FIXED_TARGET_DEGREE,
        "random_draw_order": "default_rng(666): uniform x (1000,120), normal epsilon (1000,120), normal a (1000,51)",
        "random_bank_sha256": {"x": _array_hash(x), "epsilon": _array_hash(epsilon), "a": _array_hash(a)},
        "coupling": "Independent trial rows; common random numbers across grid cells; nested n and Q_g prefixes; both models use identical labels.",
        "target_normalization": "C_Q=sqrt(sum_{q=0}^{Q_g}1/(2q+1)); E_{a,x}[g^2]=1, not per-target unit energy.",
        "risk_definition": "E_x[(f-g)^2], x uniform on [-1,1]; clean target, no test noise.",
        "mean": "Arithmetic mean of all 1000 simulated trials, no conditional averaging, smoothing or trial rejection.",
        "color_saturation": COLOR_LIMIT, "numerical_library_threads": 1,
        "python": platform.python_version(), "numpy": np.__version__, "matplotlib": matplotlib.__version__,
        "elapsed_seconds": time.perf_counter()-start,
        "source_sha256": {name: hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                          for name in ("algorithms.py", "framework.py", "run.py")},
    }
    for filename, content in (("summary.json", summary), ("manifest.json", manifest)):
        (output_dir/filename).write_text(json.dumps(content, indent=2)+"\n", encoding="utf-8")
    print(f"Saved Problem 3 results to {output_dir.resolve()}", flush=True)
    return summary
