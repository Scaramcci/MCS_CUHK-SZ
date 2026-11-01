"""DDA5001 HW3 Problem 2: complete the three marked functions only.

Image loading/normalization, MSE, and plotting are provided. No coding-agent
interaction report is required for this problem.

Install: python -m pip install -r requirements.txt
Check inputs: python p2.py --check-setup
Run after completing all three functions: python p2.py
Keep data/p2/ORL_faces with this file; generated files are saved in outputs/.
"""
from pathlib import Path
import argparse
import json
import os

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / 'data/p2/ORL_faces'
DEFAULT_OUT_DIR = ROOT / 'outputs'
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME', str(ROOT / '.cache'))
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

IMAGE_SHAPE = (112, 92)
DISPLAY_INDICES = [0, 10, 20, 30, 40]
COMPONENT_COUNTS = [20, 100]


def load_images(data_dir=None):
    """PROVIDED: load, order, and normalize the 400 original face images.

    Images remain two-dimensional here. Return images (400, 112, 92),
    with float64 pixels in [0, 1], and their ordered file paths.
    Order: subjects 1--40, then images 1--10 within each subject.
    """
    folder = Path(data_dir) if data_dir is not None else DATA_DIR
    paths = [folder / f's{s}' / f'{j}.pgm'
             for s in range(1, 41) for j in range(1, 11)]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError('Keep data/p2/ORL_faces with this package. '
                                f'Missing image: {missing[0]}')
    images = []
    for path in paths:
        with Image.open(path) as image:
            pixels = np.asarray(image, dtype=np.float64)
        if pixels.shape != IMAGE_SHAPE:
            raise ValueError(f'{path}: expected image shape {IMAGE_SHAPE}.')
        images.append(pixels / 255.0)
    images = np.stack(images, axis=0)
    if not np.isfinite(images).all() or images.min() < 0 or images.max() > 1:
        raise ValueError('The supplied images must have finite pixels in [0, 1].')
    return images, paths


def _image_inputs(images):
    """PROVIDED: validate an array of images without flattening it."""
    images = np.asarray(images, dtype=np.float64)
    if images.ndim != 3 or any(size == 0 for size in images.shape):
        raise ValueError('Expected images with shape (n, height, width).')
    if not np.isfinite(images).all():
        raise ValueError('Images must contain finite values.')
    return images


def _matrix_inputs(X):
    """PROVIDED: validate the matrix whose columns represent images."""
    X = np.asarray(X, dtype=np.float64)
    if X.ndim != 2 or any(size == 0 for size in X.shape):
        raise ValueError('Expected a nonempty X with shape (d, n).')
    if not np.isfinite(X).all():
        raise ValueError('X must contain finite values.')
    return X


def build_data_matrix(images):
    """Construct X with one face in each column.

    Input: images (n, height, width), already ordered and normalized.
    Output: X (height * width, n). Here n=400 and height * width=10304.
    Use row-major (C) order: read each image row from left to right,
    then proceed to the next row. Plotting restores this same order.
    """
    images = _image_inputs(images)
    # TODO 1: Flatten each image in row-major (C) order into a column vector.
    # Combine the vectors into X, preserving the supplied image order.
    # Return X with shape (10304, 400) for this dataset: one face per COLUMN,
    # and the same pixel position in every entry of a given ROW.
    # Pixels are already normalized; do not normalize or reorder them again.
    return images.reshape(images.shape[0], -1, order='C').T


def pca(X):
    """Compute the mean face and a thin SVD of the centered data.

    Input: X (d, n), with one image per column.
    Return mu (d, 1), U (d, r), and s (r,), where r=min(d, n).
    Columns of U are ordered by descending singular value in s.
    """
    X = _matrix_inputs(X)
    # TODO 2: Compute the mean face mu across the image columns, keeping
    # shape (d, 1). Subtract it from X, and compute a THIN SVD.
    # You may use np.linalg.svd; you do not need to implement SVD itself.
    # Return mu, the left singular vectors U, and the singular values s
    # in descending order, with the shapes described above.
    # Use all 400 faces; do not form a d-by-d covariance matrix or use
    # a ready-made PCA class. The supplied framework handles display signs.
    mu = X.mean(axis=1, keepdims=True)
    U, s, _ = np.linalg.svd(X - mu, full_matrices=False)
    return mu, U, s


def _projection_inputs(X, mu, U, k):
    """PROVIDED: check dimensions before projection and reconstruction."""
    X = _matrix_inputs(X)
    mu = np.asarray(mu, dtype=np.float64)
    U = np.asarray(U, dtype=np.float64)
    if mu.shape != (X.shape[0], 1):
        raise ValueError('mu must be a column vector with shape (d, 1).')
    if U.ndim != 2 or U.shape[0] != X.shape[0]:
        raise ValueError('U must have shape (d, r).')
    if not np.isfinite(mu).all() or not np.isfinite(U).all():
        raise ValueError('mu and U must contain finite values.')
    if not isinstance(k, (int, np.integer)) or isinstance(k, (bool, np.bool_)):
        raise ValueError('k must be an integer.')
    if not 1 <= k <= U.shape[1]:
        raise ValueError('k must be between 1 and the number of columns in U.')
    return X, mu, U, int(k)


def project_and_reconstruct(X, mu, U, k):
    """Return low-dimensional coordinates and reconstructed face columns.

    Inputs: X (d, n), mu (d, 1), U (d, r), and component count k.
    Return Theta (k, n) and Xhat (d, n), preserving the image column order.
    Do not clip reconstructed pixels; MSE uses the original reconstruction.
    """
    X, mu, U, k = _projection_inputs(X, mu, U, k)
    # TODO 3: Select the first k columns of U as the PCA basis.
    # Project the CENTERED image columns onto that basis to obtain Theta.
    # Reconstruct the images from their coordinates and ADD THE MEAN back.
    # Return (Theta, Xhat) with the shapes specified above.
    # Do not clip or rescale Xhat; the supplied plotting code clips only
    # its display copy, while MSE uses your original reconstruction.
    basis = U[:, :k]
    Theta = basis.T @ (X - mu)
    Xhat = mu + basis @ Theta
    return Theta, Xhat


def reconstruct(X, mu, U, k):
    """PROVIDED: compatibility wrapper returning only reconstructed pixels."""
    _, Xhat = project_and_reconstruct(X, mu, U, k)
    return Xhat


def load_faces(data_dir=None):
    """PROVIDED: load images and call the data-matrix construction function."""
    images, paths = load_images(data_dir)
    return build_data_matrix(images), paths


def canonicalize_signs(U):
    """PROVIDED: choose consistent eigenface display signs.

    A singular vector and its negative describe the same PCA direction.
    This changes neither the subspace nor the reconstruction.
    """
    U = np.asarray(U, dtype=np.float64)
    signs = np.sign(U[np.argmax(np.abs(U), axis=0), np.arange(U.shape[1])])
    return U * np.where(signs == 0, 1, signs)


def mse_from_reconstruction(X, Xhat):
    """PROVIDED: MSE over every pixel of every input image, before clipping."""
    X, Xhat = _matrix_inputs(X), _matrix_inputs(Xhat)
    if X.shape != Xhat.shape:
        raise ValueError('X and Xhat must have the same shape.')
    return float(np.mean((Xhat - X) ** 2))


def plot_results(X, U, reconstructions, output_dir):
    """PROVIDED: plot the prescribed eigenfaces and original/rebuilt faces."""
    out = Path(output_dir)
    fig, axes = plt.subplots(4, 4, figsize=(5.2, 6), constrained_layout=True)
    for j, ax in enumerate(axes.flat):
        ax.imshow(U[:, j].reshape(IMAGE_SHAPE, order='C'), cmap='gray')
        ax.axis('off')
        ax.set_title(f'PC {j+1}', fontsize=8)
    fig.savefig(out / 'eigenfaces.png', dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(5, 3, figsize=(5.6, 9), constrained_layout=True)
    panels = [X, reconstructions[20], reconstructions[100]]
    for row, idx in enumerate(DISPLAY_INDICES):
        for col, pixels in enumerate(panels):
            # Clip for DISPLAY ONLY; reconstructions remain unchanged for MSE.
            image = np.clip(pixels[:, idx], 0, 1).reshape(IMAGE_SHAPE, order='C')
            axes[row, col].imshow(image, cmap='gray', vmin=0, vmax=1)
            axes[row, col].axis('off')
            if row == 0:
                axes[row, col].set_title(['Original', 'k = 20', 'k = 100'][col],
                                         fontsize=10)
    fig.savefig(out / 'reconstruction.png', dpi=160)
    plt.close(fig)


def check_setup(data_dir=None):
    """PROVIDED: check the supplied data without requiring TODO completion."""
    images, _ = load_images(data_dir)
    info = {'image_array_shape': list(images.shape),
            'expected_data_matrix_shape': [int(np.prod(IMAGE_SHAPE)), len(images)],
            'pixel_range': [float(images.min()), float(images.max())]}
    print('P2 setup:', json.dumps(info), flush=True)
    return info


def run(output_dir=None, data_dir=None):
    """PROVIDED: run the three core steps and produce all requested outputs."""
    images, paths = load_images(data_dir)
    X = _matrix_inputs(build_data_matrix(images))
    expected_shape = (int(np.prod(IMAGE_SHAPE)), len(images))
    if X.shape != expected_shape:
        raise ValueError(f'TODO 1 must return X with shape {expected_shape}.')
    mu, U, s = pca(X)
    mu, U, s = np.asarray(mu), np.asarray(U), np.asarray(s)
    r = min(X.shape)
    if mu.shape != (X.shape[0], 1) or U.shape != (X.shape[0], r) or s.shape != (r,):
        raise ValueError('TODO 2 must return mu (d, 1), U (d, r), and s (r,).')
    if not all(np.isfinite(value).all() for value in (mu, U, s)):
        raise ValueError('TODO 2 must return finite arrays.')
    if np.any(s < 0) or np.any(np.diff(s) > 0):
        raise ValueError('Singular values must be nonnegative and descending.')
    U = canonicalize_signs(U)
    reconstructions = {}
    for k in COMPONENT_COUNTS:
        Theta, Xhat = project_and_reconstruct(X, mu, U, k)
        if np.shape(Theta) != (k, X.shape[1]) or np.shape(Xhat) != X.shape:
            raise ValueError('TODO 3 must return Theta (k, n) and Xhat (d, n).')
        reconstructions[k] = Xhat
    errors = {str(k): mse_from_reconstruction(X, reconstructions[k])
              for k in COMPONENT_COUNTS}
    out = Path(output_dir) if output_dir is not None else DEFAULT_OUT_DIR
    out.mkdir(parents=True, exist_ok=True)
    plot_results(X, U, reconstructions, out)
    summary = {'shape': list(X.shape), 'display_indices_zero_based': DISPLAY_INDICES,
               'pixel_scale': '[0,1]', 'mse_all_400_images': errors}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2))
    np.savetxt(out / 'mse.csv', [[k, errors[str(k)]] for k in COMPONENT_COUNTS],
               delimiter=',', header='k,reconstruction_mse', comments='')
    print('P2:', json.dumps(summary), flush=True)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-setup', action='store_true',
                        help='Check the supplied images without calling the core functions.')
    parser.add_argument('--data-dir', type=Path,
                        help='Override the folder containing s1 through s40.')
    parser.add_argument('--output-dir', type=Path,
                        help='Override the folder for figures and MSE output.')
    args = parser.parse_args()
    if args.check_setup:
        check_setup(args.data_dir)
    else:
        run(output_dir=args.output_dir, data_dir=args.data_dir)


if __name__ == '__main__':
    main()

