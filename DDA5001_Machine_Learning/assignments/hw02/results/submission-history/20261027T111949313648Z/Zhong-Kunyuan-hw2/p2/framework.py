"""Fixed data, experiment and plotting framework; identical in both editions.

Do not change this file for the required experiment. Complete algorithms.py.
No data or instructor answers are embedded in the student package.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import platform
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import numpy as np
import sklearn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from threadpoolctl import threadpool_limits

SEED = 666
TEST_SIZE = 0.20
ITERATIONS = 1000
LEARNING_RATE = 0.05
MOMENTUM_BETA = 0.90
EVALUATE_EVERY = 5
METHODS = ("gd", "momentum", "nesterov")
DISPLAY_NAMES = {"gd": "GD", "momentum": "Momentum", "nesterov": "Nesterov"}
COLORS = {"gd": "#31688e", "momentum": "#e07a30", "nesterov": "#2c9b69"}
BEAN_URL = "https://archive.ics.uci.edu/static/public/602/data.csv"
BEAN_SHA256 = "c91a086bb4357e69409d23287ec22be1be9512145cead1d8ca988c918be38fcb"
BEAN_FEATURES = (
    "Area", "Perimeter", "MajorAxisLength", "MinorAxisLength", "AspectRatio",
    "Eccentricity", "ConvexArea", "EquivDiameter", "Extent", "Solidity",
    "Roundness", "Compactness", "ShapeFactor1", "ShapeFactor2", "ShapeFactor3",
    "ShapeFactor4",
)
BEAN_CLASSES = ("BARBUNYA", "BOMBAY", "CALI", "DERMASON", "HOROZ", "SEKER", "SIRA")


def _sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def array_hash(array):
    """Portable hash includes shape and canonical little-endian dtype."""
    dtype = "<f8" if np.issubdtype(array.dtype, np.floating) else "<i8"
    canonical = np.ascontiguousarray(array, dtype=dtype)
    prefix = (str(canonical.shape) + dtype).encode("ascii")
    return _sha256_bytes(prefix + canonical.tobytes())


def _load_bean_csv(data_dir):
    cache = Path(data_dir) / "dry_bean.csv"
    if cache.exists():
        payload = cache.read_bytes()
    else:
        data_dir = Path(data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"Downloading Dry Bean once from {BEAN_URL}", flush=True)
        last_error = None
        for attempt in range(3):
            try:
                request = urllib.request.Request(BEAN_URL, headers={"User-Agent": "DDA5001-HW2/2026"})
                with urllib.request.urlopen(request, timeout=30) as response:
                    payload = response.read()
                if _sha256_bytes(payload) != BEAN_SHA256:
                    raise RuntimeError("UCI file checksum changed; contact the teaching team.")
                temporary = cache.with_suffix(".download")
                temporary.write_bytes(payload)
                temporary.replace(cache)
                break
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                last_error = exc
                if attempt < 2:
                    time.sleep(1)
        else:
            raise RuntimeError(
                f"Cannot download Dry Bean: {last_error}. Download {BEAN_URL} manually, "
                f"save it as {cache}, then rerun. No account is needed."
            ) from last_error
    if _sha256_bytes(payload) != BEAN_SHA256:
        raise RuntimeError(f"Checksum mismatch for {cache}; use the fixed official CSV.")
    reader = csv.DictReader(io.StringIO(payload.decode("utf-8-sig")))
    if tuple(reader.fieldnames) != BEAN_FEATURES + ("Class",):
        raise ValueError("Unexpected Dry Bean columns or column order.")
    rows = list(reader)
    class_to_index = {name: index for index, name in enumerate(BEAN_CLASSES)}
    X = np.asarray([[float(row[name]) for name in BEAN_FEATURES] for row in rows], dtype=np.float64)
    y = np.asarray([class_to_index[row["Class"]] for row in rows], dtype=np.int64)
    if X.shape != (13611, 16) or not np.isfinite(X).all():
        raise ValueError("Unexpected Dry Bean dimensions or missing/nonfinite values.")
    return X, y, list(BEAN_CLASSES)


def prepare_dataset(name, data_dir):
    """Fixed deduplication, stratified split, training-only scaling, constant feature."""
    if name == "digits":
        X, y = load_digits(return_X_y=True)
        X, y = X.astype(np.float64), y.astype(np.int64)
        class_names = [str(k) for k in range(10)]
    elif name == "dry_bean":
        X, y, class_names = _load_bean_csv(data_dir)
    else:
        raise ValueError(f"Unknown dataset: {name}")
    raw_n, raw_d = X.shape
    raw_hash = array_hash(X)
    # Keep the first occurrence of each exact feature vector, in original order.
    # Verify that duplicates have consistent labels before removing them.
    _, first, inverse = np.unique(X, axis=0, return_index=True, return_inverse=True)
    if not np.array_equal(y, y[first[inverse]]):
        raise ValueError("Identical feature vectors have conflicting labels.")
    keep = np.sort(first)
    X, y = X[keep], y[keep]
    indices = np.arange(len(y), dtype=np.int64)
    train_index, test_index = train_test_split(
        indices, test_size=TEST_SIZE, random_state=SEED, stratify=y,
    )
    X_train_raw, X_test_raw = X[train_index], X[test_index]
    mean = X_train_raw.mean(axis=0)
    std = X_train_raw.std(axis=0)
    # Pixels that are constant in the training set must not cause division by zero.
    std[std == 0] = 1.0
    X_train = np.column_stack(((X_train_raw - mean) / std, np.ones(len(train_index))))
    X_test = np.column_stack(((X_test_raw - mean) / std, np.ones(len(test_index))))
    y_train, y_test = y[train_index], y[test_index]
    K = len(class_names)
    Y_train, Y_test = np.eye(K)[y_train], np.eye(K)[y_test]
    manifest = {
        "dataset": name, "raw_samples": raw_n, "raw_features": raw_d,
        "raw_feature_hash": raw_hash, "duplicates_removed": raw_n - len(y),
        "samples_after_deduplication": len(y), "classes": class_names,
        "train_samples": len(y_train), "test_samples": len(y_test),
        "parameter_shape": [X_train.shape[1], K], "seed": SEED,
        "test_size": TEST_SIZE, "standardization": "training mean and population std only",
        "constant_feature": True, "initialization": "all zeros; reset before each method",
        "train_index_hash": array_hash(train_index), "test_index_hash": array_hash(test_index),
        "train_feature_hash": array_hash(X_train), "test_feature_hash": array_hash(X_test),
        "train_label_hash": array_hash(y_train), "test_label_hash": array_hash(y_test),
    }
    return X_train, Y_train, X_test, Y_test, manifest


def evaluate(theta, X, Y, algorithms):
    logits = X @ theta
    probabilities = algorithms.softmax(logits)
    return {
        "loss": algorithms.cross_entropy(logits, Y),
        "accuracy": float(np.mean(probabilities.argmax(axis=1) == Y.argmax(axis=1))),
    }


def train_one(method, X, Y, X_test, Y_test, algorithms):
    """Log after completed updates 0,5,...,1000; one full-batch gradient per update."""
    theta = np.zeros((X.shape[1], Y.shape[1]), dtype=np.float64)
    previous = theta.copy()
    history = []
    gradient_evaluations = 0

    def grad_fn(parameter):
        nonlocal gradient_evaluations
        gradient_evaluations += 1
        grad = algorithms.gradient(parameter, X, Y)
        if grad.shape != theta.shape or not np.isfinite(grad).all():
            raise ValueError("The gradient must be a finite (d, K) matrix.")
        return grad

    def record(completed):
        train = evaluate(theta, X, Y, algorithms)
        test = evaluate(theta, X_test, Y_test, algorithms)
        history.append({
            "iteration": completed, "train_loss": train["loss"], "test_loss": test["loss"],
            "train_accuracy": train["accuracy"], "test_accuracy": test["accuracy"],
        })

    record(0)
    for k in range(1, ITERATIONS + 1):
        if method == "gd":
            next_theta = algorithms.gd_step(theta, LEARNING_RATE, grad_fn)
        elif method == "momentum":
            next_theta = algorithms.momentum_step(theta, previous, LEARNING_RATE, MOMENTUM_BETA, grad_fn)
        elif method == "nesterov":
            next_theta = algorithms.nesterov_step(theta, previous, LEARNING_RATE, k, grad_fn)
        else:
            raise ValueError(method)
        if next_theta.shape != theta.shape or not np.isfinite(next_theta).all():
            raise ValueError("The updated parameter must be a finite (d, K) matrix.")
        # Step functions must not change theta or previous in place.
        previous, theta = theta.copy(), next_theta
        if k % EVALUATE_EVERY == 0 or k == ITERATIONS:
            record(k)
    if gradient_evaluations != ITERATIONS:
        raise ValueError("Use exactly one full-batch analytic gradient evaluation per update.")
    return theta, history


def _style_plot(ax, ylabel):
    ax.set_xlabel("Completed gradient updates")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.20)
    ax.spines[["top", "right"]].set_visible(False)


def plot_results(all_results, output_dir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 11, "axes.titlesize": 13, "legend.fontsize": 9})
    labels = {"digits": "Digits", "dry_bean": "Dry Bean"}
    overview, axes = plt.subplots(2, 2, figsize=(13, 8), layout="constrained")
    for column, (dataset, methods) in enumerate(all_results.items()):
        for metric, ylabel, row in (("loss", "Cross-entropy (log scale)", 0), ("accuracy", "Accuracy (%)", 1)):
            fig, ax = plt.subplots(figsize=(6.5, 3.8), layout="constrained")
            for method, history in methods.items():
                x = [record["iteration"] for record in history]
                for split, style in (("train", "-"), ("test", "--")):
                    scale = 100 if metric == "accuracy" else 1
                    y = [scale * record[f"{split}_{metric}"] for record in history]
                    label = f"{DISPLAY_NAMES[method]} / {split}"
                    for target in (ax, axes[row, column]):
                        target.plot(x, y, color=COLORS[method], linestyle=style, linewidth=1.7, label=label)
            for target in (ax, axes[row, column]):
                _style_plot(target, ylabel)
                target.set_title(labels[dataset])
                target.legend(ncols=2, loc="best", framealpha=0.85)
                if metric == "accuracy":
                    target.set_ylim(0, 102)
                else:
                    target.set_yscale("log")
            fig.savefig(Path(output_dir) / f"{dataset}_{metric}.png", dpi=180)
            plt.close(fig)
    overview.suptitle("Softmax regression: GD, momentum and Nesterov\nSolid = training; dashed = test", fontsize=15)
    overview.savefig(Path(output_dir) / "comparison.png", dpi=180)
    plt.close(overview)


def run_experiment(algorithms, data_dir, output_dir):
    """No test-set tuning: the settings are fixed before training."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    all_results, dataset_manifests, summary = {}, [], []
    # Avoid pathological many-thread overhead on small matrices and aid reproducibility.
    with threadpool_limits(limits=1):
        for name in ("digits", "dry_bean"):
            X, Y, X_test, Y_test, manifest = prepare_dataset(name, data_dir)
            print(f"{name}: train={len(X)}, test={len(X_test)}, theta={manifest['parameter_shape']}", flush=True)
            dataset_manifests.append(manifest)
            all_results[name] = {}
            for method in METHODS:
                theta, history = train_one(method, X, Y, X_test, Y_test, algorithms)
                all_results[name][method] = history
                np.save(output_dir / f"{name}_{method}_theta.npy", theta)
                with (output_dir / f"{name}_{method}_history.csv").open("w", newline="", encoding="utf-8") as stream:
                    writer = csv.DictWriter(stream, fieldnames=list(history[0]))
                    writer.writeheader()
                    writer.writerows(history)
                final = {"dataset": name, "method": method, **history[-1]}
                summary.append(final)
                print(f"  {method:9s} train/test CE={final['train_loss']:.6f}/{final['test_loss']:.6f}, "
                      f"train/test accuracy={100*final['train_accuracy']:.2f}%/{100*final['test_accuracy']:.2f}%", flush=True)
    with (output_dir / "summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    manifest = {
        "python": sys.version.split()[0], "numpy": np.__version__, "sklearn": sklearn.__version__,
        "platform": platform.platform(), "iterations": ITERATIONS, "learning_rate": LEARNING_RATE,
        "momentum_beta": MOMENTUM_BETA, "nesterov_coefficient": "(k-1)/(k+2), k=1,...,1000",
        "evaluate_every": EVALUATE_EVERY, "regularization": None, "batch": "full training set",
        "datasets": dataset_manifests,
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    plot_results(all_results, output_dir)
    return summary
