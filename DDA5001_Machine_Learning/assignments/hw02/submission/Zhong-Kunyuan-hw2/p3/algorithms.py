"""Problem 3: complete these two functions; coding-agent use is optional.

Use your derivations in 3(a) and 3(b), and verify your implementation.
No agent interaction record is required for this part.
Do not change the experiment framework, random seed, or public tests.
"""

import numpy as np


def fit_polynomial(design_matrix, labels):
    """Return least-squares coefficients in the RAW Legendre basis.

    design_matrix: (n, K+1), column k is L_k(x_i), including L_0 = 1.
    labels: (n,) for one dataset, or (n, m) for m separate label vectors.
    Return shape (K+1,) or (K+1, m), respectively.

    Each labels column is an independent fit on the same input points.
    Use a stable least-squares solver (e.g. QR/SVD), not an explicit inverse.
    Do not add regularization, convert to powers of x, or modify inputs.
    Only the training design and labels are available to this function.
    """
    return np.linalg.lstsq(design_matrix, labels, rcond=None)[0]


def population_error(coefficients, target_coefficients):
    """Return the analytic E_out with respect to Uniform[-1, 1].

    coefficients: (K+1,) or (K+1, m), from fit_polynomial.
    target_coefficients: (Q_g+1,) or (Q_max+1, m) in the RAW
        Legendre basis. The framework has ALREADY divided a_q by C_Q.
        A target of lower degree has zero coefficients above its degree.
    Return a scalar for 1-D inputs, or shape (m,) for 2-D inputs.

    The two arrays may have different numbers of rows. Include all terms
    in the target, including those above the fitted model's degree.
    Apply your orthogonality formula from 3(b); no sampled test set,
    numerical integration, or observation-noise term is needed here.
    Do not modify the inputs or renormalize the target coefficients.
    """
    # Only the degree axis is padded; each remaining column is its own target.
    degree_count = max(coefficients.shape[0], target_coefficients.shape[0])
    model_padding = [(0, degree_count - coefficients.shape[0])]
    target_padding = [(0, degree_count - target_coefficients.shape[0])]
    model_padding += [(0, 0)] * (coefficients.ndim - 1)
    target_padding += [(0, 0)] * (target_coefficients.ndim - 1)
    difference = np.pad(coefficients, model_padding) - np.pad(target_coefficients, target_padding)
    denominators = 2 * np.arange(degree_count) + 1
    if difference.ndim == 2:
        denominators = denominators[:, None]
    return np.sum(difference**2 / denominators, axis=0)
