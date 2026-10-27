"""Public toy checks: no experiment answer arrays or reference implementation."""

import unittest

import numpy as np
from numpy.polynomial.legendre import leggauss, legval, legvander

from algorithms import fit_polynomial, population_error
from framework import generate_random_bank, generate_trial, TRIALS, SEED


class FittingTests(unittest.TestCase):
    def test_noiseless_recovery_for_both_models(self):
        x = np.linspace(-0.95, 0.95, 40)
        truth = np.array([0.3, -0.7, 0.2])
        y = legval(x, truth)
        for degree in (2, 10):
            w = fit_polynomial(legvander(x, degree), y)
            expected = np.pad(truth, (0, degree-2))
            np.testing.assert_allclose(w, expected, atol=1e-11)
            self.assertLess(population_error(w, truth), 1e-20)

    def test_multiple_label_columns_and_no_mutation(self):
        rng = np.random.default_rng(19)
        design = legvander(rng.uniform(-1, 1, 35), 4)
        labels = rng.normal(size=(35, 3))
        old_design, old_labels = design.copy(), labels.copy()
        w = fit_polynomial(design, labels)
        self.assertEqual(w.shape, (5, 3))
        np.testing.assert_allclose(design.T@(design@w-labels), 0, atol=1e-11)
        for column in range(3):
            np.testing.assert_allclose(w[:, column], fit_polynomial(design, labels[:, column]), atol=1e-11)
        np.testing.assert_array_equal(design, old_design)
        np.testing.assert_array_equal(labels, old_labels)

    def test_nested_training_errors(self):
        rng = np.random.default_rng(25)
        x, y = rng.uniform(-1, 1, 50), rng.normal(size=50)
        errors = []
        for degree in (2, 10):
            design = legvander(x, degree)
            w = fit_polynomial(design, y)
            errors.append(np.mean((design@w-y)**2))
        self.assertLessEqual(errors[1], errors[0]+1e-12)


class PopulationErrorTests(unittest.TestCase):
    def test_uniform_density_and_already_normalized_target(self):
        # Constant residual 2-1 has uniform expectation 1, not integral 2.
        self.assertAlmostEqual(population_error(np.array([2.]), np.array([1.])), 1.)
        # The target coefficients supplied to this function are a_q/C_Q.
        cq = np.sqrt(1+1/3)
        truth = np.array([0., 1./cq])
        self.assertAlmostEqual(population_error(np.array([0.]), truth), 1/(3*cq**2))

    def test_target_tail_and_model_tail(self):
        self.assertAlmostEqual(population_error(np.array([0.]), np.array([0., 0., 0., 2.])), 4/7)
        self.assertAlmostEqual(population_error(np.array([0., 0., 3.]), np.array([0.])), 9/5)

    def test_multiple_columns_and_no_mutation(self):
        w = np.array([[1., 2.], [0.2, -0.3]])
        truth = np.array([[1.5, 1.], [0., 0.], [0.7, -0.5]])
        old_w, old_truth = w.copy(), truth.copy()
        risk = population_error(w, truth)
        self.assertEqual(risk.shape, (2,))
        expected = np.array([0.5**2+0.2**2/3+0.7**2/5,
                             1.+0.3**2/3+0.5**2/5])
        np.testing.assert_allclose(risk, expected, atol=1e-14)
        np.testing.assert_array_equal(w, old_w)
        np.testing.assert_array_equal(truth, old_truth)

    def test_independent_gaussian_quadrature_check(self):
        rng = np.random.default_rng(51)
        for degree, target_degree in ((2, 20), (10, 3), (10, 50)):
            w, truth = rng.normal(size=degree+1), rng.normal(size=target_degree+1)
            nodes, weights = leggauss(80)
            residual = legval(nodes, w)-legval(nodes, truth)
            numerical = float(np.sum(weights*residual**2)/2)
            np.testing.assert_allclose(population_error(w, truth), numerical, rtol=1e-10, atol=1e-10)


class ProvidedFrameworkTests(unittest.TestCase):
    def test_random_bank_and_generated_data(self):
        self.assertEqual((SEED, TRIALS), (666, 1000))
        bank = generate_random_bank()
        repeated = generate_random_bank()
        for first, second in zip(bank, repeated):
            np.testing.assert_array_equal(first, second)
        x, epsilon, a, cq = bank
        self.assertEqual(x.shape, (1000, 120))
        self.assertEqual(a.shape, (1000, 51))
        design, labels, truth = generate_trial(x[0], epsilon[0], a[0], cq)
        self.assertEqual(labels.shape, (120, 91))
        np.testing.assert_allclose(labels[:, 19], design@truth[:, 19]+np.sqrt(.1)*epsilon[0])
        np.testing.assert_allclose(labels[:, 50], design@truth[:, 50])
        # Same Q_g=20, sigma^2=0.1 cell occurs in the two grids.
        np.testing.assert_array_equal(labels[:, 19], labels[:, 52])
        np.testing.assert_array_equal(truth[:, 19], truth[:, 52])
        self.assertTrue(np.all(truth[2:, 0] == 0))


if __name__ == "__main__":
    unittest.main()
