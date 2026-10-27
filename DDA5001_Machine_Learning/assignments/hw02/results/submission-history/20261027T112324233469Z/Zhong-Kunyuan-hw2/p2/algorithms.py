"""Student release: implement the core of HW2 Problem 2(b) with a coding agent.

X: (n, d), one_hot: (n, K), theta: (d, K).
The last column of X is a constant feature. There is no separate bias b.
Use the analytic gradient from Problem 2(a) and implement updates yourself.
Do not use a ready-made classifier or optimizer for the required experiment.
You may use autodiff only as an independent check, not for training.

Preserve these function signatures. Do not mutate input arrays in place.
Edit this file, not framework.py, run.py, or the fixed experiment settings.
"""

import numpy as np


def softmax(logits):
    """Return stable row-wise probabilities for an (n, K) score matrix.

    Subtract each row's maximum before exponentiation. Explain to your agent
    why this leaves the probabilities unchanged.
    """
    shifted = logits - np.max(logits, axis=1, keepdims=True)
    exponentials = np.exp(shifted)
    return exponentials / np.sum(exponentials, axis=1, keepdims=True)


def cross_entropy(logits, one_hot):
    """Return scalar mean cross-entropy for one-hot labels, without L2 penalty.

    Compute stable log-probabilities from logits rather than log(softmax),
    which can become log(0). Do not clip probabilities to hide instability.
    """
    shifted = logits - np.max(logits, axis=1, keepdims=True)
    log_probabilities = shifted - np.log(np.sum(np.exp(shifted), axis=1, keepdims=True))
    return float(-np.mean(np.sum(one_hot * log_probabilities, axis=1)))


def gradient(theta, X, one_hot):
    """Return the analytic mean-loss gradient derived in 2(a), shape (d, K).

    Preserve the lecture convention: class parameters are COLUMNS of theta.
    """
    return X.T @ (softmax(X @ theta) - one_hot) / X.shape[0]


def gd_step(theta, learning_rate, grad_fn):
    """Return one full-batch GD update; grad_fn(parameter) returns its gradient."""
    return theta - learning_rate * grad_fn(theta)


def momentum_step(theta, previous, learning_rate, beta, grad_fn):
    """Return one lecture Polyak-momentum update.

    theta is the current parameter; previous is the preceding parameter.
    Think about WHERE the gradient is evaluated.
    """
    return theta - learning_rate * grad_fn(theta) + beta * (theta - previous)


def nesterov_step(theta, previous, learning_rate, k, grad_fn):
    """Return one lecture Nesterov update, using coefficient (k-1)/(k+2).

    k is the 1-based update number, so the first coefficient is zero.
    Think about WHERE the gradient is evaluated, not just its coefficient.
    """
    lookahead = theta + ((k - 1) / (k + 2)) * (theta - previous)
    return lookahead - learning_rate * grad_fn(lookahead)
