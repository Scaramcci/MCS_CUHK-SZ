"""Independent HW1 numerical checks; never writes implementation outputs."""
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
HW = HERE.parents[2]
SRC = HW / "src"
REQ = HW / "requirements/code_source/code_source"
CONV = HW / "results/input-conversion-20260929"
BASE = HW / "results"


def run(label, command):
    result = subprocess.run(command, cwd=HW, text=True, capture_output=True)
    (HERE / f"{label}.stdout.txt").write_text(result.stdout)
    (HERE / f"{label}.stderr.txt").write_text(result.stderr)
    (HERE / f"{label}.exit_code.txt").write_text(f"{result.returncode}\n")
    return {"command": command, "exit_code": result.returncode}


def rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def close(a, b, atol=1e-10):
    np.testing.assert_allclose(a, b, atol=atol, rtol=1e-10)


def check_p3():
    sys.path.insert(0, str(SRC))
    import p3
    X = np.array([[1., 0.], [0., 1.], [1., 1.], [1., -1.], [1., 2.]])
    theta = np.zeros(2)
    v = np.array([.6, .8])
    checks = []
    for mu in (1., 1e-5):
        residual = mu * np.array([-2., -.5, 0., .5, 2.])
        y = -residual
        expected_derivative = np.array([-1., -.5, 0., .5, 1.])
        close(p3.huber_gradient(theta, X, y, mu), X.T @ expected_derivative)
        close(p3.huber_loss(theta, X, y, mu),
              np.sum([2., .625, .5, .625, 2.]) * mu)
        analytic = float(p3.huber_gradient(theta, X, y, mu) @ v)
        assert abs(analytic - 1.1) < 1e-12
        for multiplier in (1., .1, .01, .0001):
            h = mu * multiplier
            fd = (p3.huber_loss(theta + h*v, X, y, mu) -
                  p3.huber_loss(theta - h*v, X, y, mu)) / (2*h)
            checks.append({"mu": mu, "step": h, "gradient_dot_direction": analytic,
                           "finite_difference": fd, "absolute_error": abs(fd-analytic)})
        # Unit directions from a second, independently chosen three-row case.
        X2 = np.array([[1., 2.], [-1., .25], [.3, -2.]])
        y2 = np.array([.1, -.6, .5])
        th2 = np.array([.2, -.4])
        expected = X2.T @ np.clip((X2 @ th2 - y2)/mu, -1, 1)
        close(p3.huber_gradient(th2, X2, y2, mu), expected)
    replay = HERE / "p3-replay"
    origin = BASE / "p3-baseline-20260929"
    new = rows(replay / "regression_history.csv")
    old = rows(origin / "regression_history.csv")
    assert len(new) == len(old) == 1001
    for field in ("sum_huber_loss", "estimation_error"):
        close([float(r[field]) for r in new], [float(r[field]) for r in old], 1e-8)
    close(np.load(replay / "theta_huber.npy"), np.load(origin / "theta_huber.npy"), 1e-9)
    close(np.load(replay / "theta_ls.npy"), np.load(origin / "theta_ls.npy"), 1e-9)
    with np.load(CONV / "train_data.npz") as z:
        pass
    return {"directional_checks": checks,
            "baseline_history_rows": len(new),
            "final_error": float(new[-1]["estimation_error"]),
            "final_loss": float(new[-1]["sum_huber_loss"]),
            "least_squares_error": float((json.loads((replay / "summary.json").read_text()))["baseline"]["least_squares_error"])}


def check_p5():
    import p5
    Xtoy = np.array([[1., 0., 0.], [1., 0., 0.], [1., 0., 0.], [1., 1., 0.]])
    ytoy = np.array([1, -1, 1, -1])
    assert p5.predict(np.zeros(3), Xtoy).tolist() == [1, 1, 1, 1]
    toy = rows(HERE / "p5-replay/toy_trace.csv")
    assert len(toy) == 7
    # Independent expected trace from the actual seed and stated update rule.
    rng = np.random.default_rng(0)
    theta = np.zeros(3)
    pocket = theta.copy()
    best = np.mean(np.where(Xtoy @ theta >= 0, 1, -1) != ytoy)
    for k, row in enumerate(toy):
        if k:
            mistakes = np.flatnonzero(np.where(Xtoy @ theta >= 0, 1, -1) != ytoy)
            idx = int(rng.choice(mistakes))
            assert int(row["chosen_index"]) == idx
            theta = theta + ytoy[idx] * Xtoy[idx]
            error = np.mean(np.where(Xtoy @ theta >= 0, 1, -1) != ytoy)
            if error < best:
                pocket, best = theta.copy(), error
        close([float(row[f"current_w{j}"]) for j in range(3)], theta)
        close([float(row[f"pocket_w{j}"]) for j in range(3)], pocket)
        assert abs(float(row["pocket_train_error"]) - best) < 1e-12
    trace = rows(HERE / "p5-replay/trajectory.csv")
    original = rows(BASE / "p5-baseline-20260929/trajectory.csv")
    assert len(trace) == len(original) == 2001
    # Recompute every train/test error from saved weights and original features.
    with np.load(CONV / "train_data.npz") as z:
        train_raw = z["zip"]
    with np.load(CONV / "test_data.npz") as z:
        test_raw = z["zip"]
    def features(raw):
        mask = np.isin(raw[:, 0].astype(int), [1, 6])
        digit = raw[mask, 0].astype(int)
        im = raw[mask, 1:].reshape(-1, 16, 16)
        x = np.column_stack((np.ones(len(im)), im.mean((1, 2)),
                             np.abs(im - im[:, :, ::-1]).mean((1, 2))))
        return x, np.where(digit == 1, 1, -1)
    X, y = features(train_raw)
    Xt, yt = features(test_raw)
    assert (len(X), len(Xt)) == (1669, 434)
    matrix = {}
    for name in ("current", "pocket"):
        W = np.array([[float(r[f"{name}_w{j}"]) for j in range(3)] for r in trace])
        matrix[name] = W
        for split, xx, yy in (("train", X, y), ("test", Xt, yt)):
            calculated = np.mean(np.where(xx @ W.T >= 0, 1, -1) != yy[:, None], axis=0)
            reported = np.array([float(r[f"{name}_{split}_error"]) for r in trace])
            close(calculated, reported, 1e-12)
        for j in range(3):
            close([float(r[f"{name}_w{j}"]) for r in trace],
                  [float(r[f"{name}_w{j}"]) for r in original], 1e-12)
    current = np.array([float(r["current_train_error"]) for r in trace])
    pocket = np.array([float(r["pocket_train_error"]) for r in trace])
    close(pocket, np.minimum.accumulate(current), 1e-12)
    assert np.all(np.diff(pocket) <= 1e-12)
    rng = np.random.default_rng(0)
    for k, row in enumerate(trace[1:], 1):
        previous = matrix["current"][k-1]
        mistakes = np.flatnonzero(np.where(X @ previous >= 0, 1, -1) != y)
        idx = int(rng.choice(mistakes))
        assert int(row["chosen_index"]) == idx
        close(matrix["current"][k], previous + y[idx]*X[idx], 1e-12)
    test_pocket = np.array([float(r["pocket_test_error"]) for r in trace])
    return {"toy_rows": len(toy), "trajectory_rows": len(trace),
            "n_train": len(X), "n_test": len(Xt),
            "current_final_train_error": float(current[-1]),
            "pocket_final_train_error": float(pocket[-1]),
            "current_final_test_error": float(trace[-1]["current_test_error"]),
            "pocket_final_test_error": float(test_pocket[-1]),
            "pocket_test_error_increase_count": int(np.sum(np.diff(test_pocket) > 1e-12)),
            "pocket_training_running_minimum": True,
            "random_choice_and_update_replayed": True}


def main():
    report = {"runs": {}, "checks": {}}
    report["versions"] = {str(p.relative_to(HW)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (SRC / "p3.py", SRC / "p5.py")}
    report["runs"]["p3"] = run("p3", ["/usr/bin/python3", str(SRC / "p3.py"),
                                     "--data-dir", str(REQ / "p3/data"),
                                     "--output-dir", str(HERE / "p3-replay")])
    report["runs"]["p5"] = run("p5", ["/usr/bin/python3", str(SRC / "p5.py"),
                                     "--train-data", str(CONV / "train_data.npz"),
                                     "--test-data", str(CONV / "test_data.npz"),
                                     "--output-dir", str(HERE / "p5-replay")])
    for name, checker in (("p3", check_p3), ("p5", check_p5)):
        try:
            report["checks"][name] = checker()
        except Exception as exc:
            report["checks"][name] = {"failed": repr(exc)}
    (HERE / "check_summary.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    assert all(r["exit_code"] == 0 for r in report["runs"].values())
    assert all("failed" not in r for r in report["checks"].values())


if __name__ == "__main__":
    main()
