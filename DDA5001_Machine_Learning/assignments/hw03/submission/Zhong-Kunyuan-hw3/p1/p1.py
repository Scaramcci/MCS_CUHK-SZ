"""DDA5001 HW3 Problem 1: complete the two marked functions only.

Data loading, fixed folds, fitting inside CV, MSE, the unregularized baseline,
and all plots are provided. No coding-agent interaction report is required.

Install: python -m pip install -r requirements.txt
Check inputs before filling the functions: python p1.py --check-setup
Run after completing both functions: python p1.py
Keep data/ next to this file; generated files are saved in outputs/.
"""
from pathlib import Path
import argparse
import json
import os

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / 'data'
DEFAULT_OUT_DIR = ROOT / 'outputs'
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME', str(ROOT / '.cache'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DEGREE = 8
LAMBDAS = np.array([1e-5, 1e-4, 1e-3, .01, .1, .3, .5, .8,
                    1, 2, 5, 10, 15, 20, 50, 100], dtype=float)
FIXED_FOLDS = np.array([[6, 0], [3, 9], [2, 1], [4, 8], [5, 7]], dtype=int)


def design(x, degree=DEGREE):
    """Columns are 1, x, ..., x**degree; never reorder the observations."""
    return np.vander(np.asarray(x, dtype=float).reshape(-1), degree + 1,
                     increasing=True)


def _fit_inputs(X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float).reshape(-1)
    if X.ndim != 2 or X.shape[0] != len(y) or len(y) == 0:
        raise ValueError('Expected X with shape (m, d) and y with m entries.')
    if not np.isfinite(X).all() or not np.isfinite(y).all():
        raise ValueError('Fit inputs must be finite.')
    return X, y


def fit_ridge_for_cv(X, y, lam):
    """PROVIDED: fit one CV training fold using augmented least squares.

    This minimizes mean squared error + lam * ||theta||_2**2. Every
    coefficient, including the constant feature, is penalized. Do not edit.
    """
    X, y = _fit_inputs(X, y)
    if not np.isfinite(lam) or lam <= 0:
        raise ValueError('The supplied CV candidates must have lam > 0.')
    m, d = X.shape
    A = np.vstack((X / np.sqrt(m), np.sqrt(lam) * np.eye(d)))
    b = np.concatenate((y / np.sqrt(m), np.zeros(d)))
    return np.linalg.lstsq(A, b, rcond=None)[0]


def fit_ridge_final(X, y, lam):
    """Return the final regularized coefficients, with shape (d,).

    Inputs: all selected training rows X (m, d), their targets y (m,), and
    the positive lambda chosen by CV. In this assignment m=10 and d=9.
    Objective: mean((X @ theta - y)**2) + lam * sum(theta**2).
    """
    X, y = _fit_inputs(X, y)
    if not np.isfinite(lam) or lam <= 0:
        raise ValueError('The final regularized fit requires lam > 0.')
    # TODO 1: Write the objective gradient, set it to zero, and derive the
    # closed-form regularized least-squares solution discussed in lecture.
    # Show these steps in your report or in a short code comment, then
    # implement your derived solution to return theta with shape (d,).
    # Use all ten TRAINING observations (no test data), the selected lambda,
    # MEAN squared error, and a penalty on ALL d coefficients, including
    # the intercept. Do not call fit_ridge_for_cv in your implementation.
    # You may use np.linalg.solve to evaluate your closed-form solution.
    # grad = (2/m) X.T @ (X @ theta - y) + 2*lam*theta.
    # Setting it to zero gives (X.T @ X + m*lam*I) @ theta = X.T @ y.
    m, d = X.shape
    return np.linalg.solve(X.T @ X + m * lam * np.eye(d), X.T @ y)


def mse_from_predictions(y_true, y_pred):
    """PROVIDED: MSE on whichever observations are being evaluated."""
    y_true = np.asarray(y_true, dtype=float).reshape(-1)
    y_pred = np.asarray(y_pred, dtype=float).reshape(-1)
    if len(y_true) != len(y_pred) or len(y_true) == 0:
        raise ValueError('MSE requires equally sized, nonempty vectors.')
    return float(np.mean((y_pred - y_true) ** 2))


def score_and_select_cv(validation_records, candidates, n_folds=5):
    """Return (best_lambda, fold_mse).

    Each supplied record is (candidate_index, fold_index, y_validation,
    validation_predictions). The model has ALREADY been fitted on the other
    eight rows. No test data are passed to this function.

    candidates is ascending; fold_mse must have shape
    (len(candidates), n_folds), with one held-out MSE in each entry.
    """
    candidates = np.asarray(candidates, dtype=float)
    # TODO 2: Fill fold_mse using the PROVIDED mse_from_predictions function
    # and each record's validation targets/predictions. Average the five
    # held-out MSEs for each candidate, then choose the lambda with the lowest
    # average. Break an exact tie by choosing the smaller lambda.
    # Return that lambda (a scalar) and the complete fold_mse matrix.
    # Do not refit any model here or use training/test errors for selection.
    fold_mse = np.empty((len(candidates), n_folds), dtype=float)
    for candidate_index, fold_index, targets, predictions in validation_records:
        fold_mse[candidate_index, fold_index] = mse_from_predictions(targets, predictions)
    # Candidates are ascending; argmin returns the first exact minimum.
    best_index = np.argmin(fold_mse.mean(axis=1))
    return float(candidates[best_index]), fold_mse


def cross_validate(x, y):
    """PROVIDED: fixed splits, CV training fits, and held-out predictions."""
    x = np.asarray(x, dtype=float).reshape(-1)
    y = np.asarray(y, dtype=float).reshape(-1)
    if len(x) != 10 or len(y) != 10:
        raise ValueError('The fixed folds require the original ten training rows.')
    X = design(x)
    folds = [fold.copy() for fold in FIXED_FOLDS]
    records = []
    for candidate_index, lam in enumerate(LAMBDAS):
        for fold_index, validation_ids in enumerate(folds):
            training_ids = np.setdiff1d(np.arange(10), validation_ids)
            theta_cv = fit_ridge_for_cv(X[training_ids], y[training_ids], lam)
            predictions = X[validation_ids] @ theta_cv
            records.append((candidate_index, fold_index,
                            y[validation_ids].copy(), predictions))
    best_lambda, fold_mse = score_and_select_cv(records, LAMBDAS.copy(), len(folds))
    fold_mse = np.asarray(fold_mse, dtype=float)
    if fold_mse.shape != (len(LAMBDAS), len(folds)) or not np.isfinite(fold_mse).all():
        raise ValueError('TODO 2 must return one finite MSE per candidate and fold.')
    if not np.any(LAMBDAS == best_lambda):
        raise ValueError('TODO 2 must select a lambda from the supplied candidates.')
    return float(best_lambda), fold_mse, folds


def ridge(x, y, lam):
    """PROVIDED: baseline uses lstsq; positive lambda uses your final fit."""
    X, y = _fit_inputs(design(x), y)
    if lam == 0:
        return np.linalg.lstsq(X, y, rcond=None)[0]
    return fit_ridge_final(X, y, lam)


def mse(theta, x, y):
    """PROVIDED: evaluate fitted coefficients on the requested observations."""
    return mse_from_predictions(y, design(x) @ theta)


def load_data(data_dir=None):
    folder = Path(data_dir) if data_dir is not None else DATA_DIR
    train = np.loadtxt(folder / 'training.csv', delimiter=',', skiprows=1)
    test = np.loadtxt(folder / 'test.csv', delimiter=',', skiprows=1)
    if train.shape != (10, 2) or test.shape != (10, 2):
        raise ValueError('Keep the supplied two-column, ten-row CSV datasets unchanged.')
    if not np.isfinite(train).all() or not np.isfinite(test).all():
        raise ValueError('The supplied datasets must contain finite values.')
    return train, test


def plot_data(x, y, out):
    """PROVIDED: noisy training observations, clean target, and point IDs."""
    grid = np.linspace(-1.5, 1.5, 600)
    offsets = [(-26, -7), (-22, 21), (5, -18), (-27, -17), (24, 14),
               (16, 20), (18, 28), (34, -7), (-36, 24), (22, 12)]
    fig, ax = plt.subplots(figsize=(7.2, 4.3), constrained_layout=True)
    ax.plot(grid, grid**2, color='tab:blue', label=r'Clean target: $y=x^2$')
    ax.scatter(x, y, color='black', s=30, label='Noisy training observations', zorder=4)
    for point_id, (xi, yi, offset) in enumerate(zip(x, y, offsets)):
        ax.annotate(str(point_id), (xi, yi), xytext=offset,
                    textcoords='offset points', ha='center', va='center',
                    bbox=dict(boxstyle='circle,pad=.16', fc='white', ec='gray', lw=.5),
                    arrowprops=dict(arrowstyle='->', lw=.7, mutation_scale=7,
                                    shrinkA=5, shrinkB=4))
    ax.set(xlim=(-1.5, 1.5), ylim=(-.5, 2.5), xlabel='x', ylabel='y')
    ax.legend(loc='upper center'); ax.grid(alpha=.15)
    fig.savefig(out / 'data_target.png', dpi=180); plt.close(fig)


def plot_results(x, y, best, fold_mse, models, out):
    """PROVIDED: the two figures requested in the homework."""
    fig, ax = plt.subplots(figsize=(5.8, 3.4), constrained_layout=True)
    ax.semilogx(LAMBDAS, fold_mse.mean(axis=1), 'o-', markersize=4)
    ax.axvline(best, color='tab:red', ls='--', label=f'Selected lambda = {best:g}')
    ax.set(xlabel='Regularization parameter lambda', ylabel='Five-fold validation MSE')
    ax.legend(); ax.grid(alpha=.2)
    fig.savefig(out / 'validation.png', dpi=180); plt.close(fig)
    grid = np.linspace(-1.5, 1.5, 600)
    fig, ax = plt.subplots(figsize=(5.8, 3.4), constrained_layout=True)
    ax.scatter(x, y, color='black', s=24, label='Training data', zorder=4)
    ax.plot(grid, grid**2, '--', color='gray', label='Clean target')
    ax.plot(grid, design(grid) @ models['unregularized'], color='tab:orange',
            label='No regularization')
    ax.plot(grid, design(grid) @ models['selected'], color='tab:blue',
            label=f'CV choice: lambda = {best:g}')
    ax.set(xlim=(-1.5, 1.5), ylim=(-.5, 2.5), xlabel='x', ylabel='Prediction')
    ax.legend(fontsize=8); ax.grid(alpha=.15)
    fig.savefig(out / 'fits.png', dpi=180); plt.close(fig)


def run(out_dir=None, data_dir=None):
    train, test = load_data(data_dir)
    out = Path(out_dir) if out_dir is not None else DEFAULT_OUT_DIR
    out.mkdir(parents=True, exist_ok=True)
    x, y = train.T
    plot_data(x, y, out)
    best, fold_mse, folds = cross_validate(x, y)
    models = {'unregularized': ridge(x, y, 0), 'selected': ridge(x, y, best)}
    mean_scores = fold_mse.mean(axis=1)
    selected_index = int(np.flatnonzero(LAMBDAS == best)[0])
    summary = {
        'selected_lambda': best,
        'selected_cv_mse': float(mean_scores[selected_index]),
        'fold_indices_zero_based': [f.tolist() for f in folds],
        'intercept_penalized': True,
        'objective': 'mean squared error + lambda * squared l2 norm',
        'models': {name: {'training_mse': mse(w, x, y),
                          'test_mse': mse(w, *test.T), 'theta': w.tolist()}
                   for name, w in models.items()}}
    np.savetxt(out / 'cross_validation.csv',
               np.column_stack((LAMBDAS, fold_mse, mean_scores)), delimiter=',',
               header='lambda,fold1,fold2,fold3,fold4,fold5,mean_mse', comments='')
    with open(out / 'summary.json', 'w') as stream:
        json.dump(summary, stream, indent=2)
    plot_results(x, y, best, fold_mse, models, out)
    print(f'Selected lambda: {best:g}')
    print('Model             Training MSE       Test MSE')
    for name, result in summary['models'].items():
        print(f"{name:16s} {result['training_mse']:.8f} {result['test_mse']:.8f}")
    print(f'Outputs saved in {out}')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-setup', action='store_true',
                        help='check provided data and draw the input data without calling the unfinished functions')
    parser.add_argument('--output-dir', type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()
    if args.check_setup:
        train, test = load_data()
        args.output_dir.mkdir(parents=True, exist_ok=True)
        plot_data(*train.T, args.output_dir)
        print(f'Setup OK: {len(train)} training rows, {len(test)} test rows; '
              f'design matrix {design(train[:, 0]).shape}.')
        print('Point IDs and folds use the unchanged CSV row order.')
    else:
        run(out_dir=args.output_dir)
