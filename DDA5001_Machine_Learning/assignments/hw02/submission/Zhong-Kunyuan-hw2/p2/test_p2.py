"""Public local checks. Run: python -m unittest discover -s p2 -v

These tiny checks are available in both editions. They do not contain the
complete instructor implementation or the reference dataset results.
"""

import unittest

import numpy as np

import algorithms as alg


class CoreChecks(unittest.TestCase):
    def setUp(self):
        self.X = np.array([[1., -1., 1.], [2., .5, 1.], [-1., 2., 1.], [.5, .2, 1.]])
        self.Y = np.eye(3)[[0, 1, 2, 1]]
        self.theta = np.array([[.1, -.2, .05], [.3, -.1, .2], [.02, .1, -.1]])

    def test_softmax_stability_and_shift_invariance(self):
        logits = np.array([[1000., 1001., 999.], [-1000., -1001., -999.]])
        probabilities = alg.softmax(logits)
        self.assertTrue(np.isfinite(probabilities).all())
        np.testing.assert_allclose(probabilities.sum(axis=1), 1., atol=1e-14)
        np.testing.assert_allclose(probabilities, alg.softmax(logits + 17.), atol=1e-14)

    def test_loss_at_zero_and_extreme_wrong_prediction(self):
        self.assertAlmostEqual(alg.cross_entropy(np.zeros((4, 3)), self.Y), np.log(3), places=13)
        loss = alg.cross_entropy(np.array([[1000., -1000.]]), np.array([[0., 1.]]))
        self.assertAlmostEqual(loss, 2000., places=10)

    def test_analytic_gradient_against_finite_differences(self):
        epsilon = 1e-6
        numerical = np.zeros_like(self.theta)
        for index in np.ndindex(self.theta.shape):
            plus, minus = self.theta.copy(), self.theta.copy()
            plus[index] += epsilon
            minus[index] -= epsilon
            numerical[index] = (alg.cross_entropy(self.X @ plus, self.Y)
                                - alg.cross_entropy(self.X @ minus, self.Y)) / (2 * epsilon)
        analytic = alg.gradient(self.theta, self.X, self.Y)
        self.assertEqual(analytic.shape, self.theta.shape)
        np.testing.assert_allclose(analytic, numerical, rtol=1e-6, atol=1e-8)
        np.testing.assert_allclose(analytic.sum(axis=1), 0., atol=1e-14)

    def test_gd_update_and_no_in_place_change(self):
        before = self.theta.copy()
        actual = alg.gd_step(self.theta, .05, lambda t: 2 * t)
        np.testing.assert_allclose(actual, .90 * before, atol=1e-14)
        np.testing.assert_array_equal(self.theta, before)

    def test_momentum_gradient_location_and_update(self):
        before, previous = self.theta.copy(), self.theta.copy() - .02
        calls = []
        def grad(point):
            calls.append(point.copy())
            return 2 * point
        actual = alg.momentum_step(self.theta, previous, .05, .9, grad)
        self.assertEqual(len(calls), 1)
        np.testing.assert_array_equal(calls[0], before)
        np.testing.assert_allclose(actual, .9 * before + .018, atol=1e-14)
        np.testing.assert_array_equal(self.theta, before)
        np.testing.assert_allclose(previous, before - .02, atol=1e-14)

    def test_nesterov_nonzero_extrapolation_and_update(self):
        before, previous = self.theta.copy(), self.theta.copy() - .02
        calls = []
        def grad(point):
            calls.append(point.copy())
            return 2 * point
        actual = alg.nesterov_step(self.theta, previous, .05, 3, grad)
        self.assertEqual(len(calls), 1)
        # At k=3, (k-1)/(k+2)=2/5. The point is NOT current theta.
        np.testing.assert_allclose(calls[0], before + .008, atol=1e-14)
        np.testing.assert_allclose(actual, .9 * (before + .008), atol=1e-14)
        np.testing.assert_array_equal(self.theta, before)
        np.testing.assert_allclose(previous, before - .02, atol=1e-14)

    def test_first_updates_coincide(self):
        previous = self.theta.copy()
        grad = lambda t: alg.gradient(t, self.X, self.Y)
        expected = alg.gd_step(self.theta, .05, grad)
        np.testing.assert_allclose(alg.momentum_step(self.theta, previous, .05, .9, grad), expected)
        np.testing.assert_allclose(alg.nesterov_step(self.theta, previous, .05, 1, grad), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
