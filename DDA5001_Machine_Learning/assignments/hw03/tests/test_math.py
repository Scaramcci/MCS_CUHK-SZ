"""Author self-checks: independent mathematical invariants, not grading tests."""
import importlib.util
from pathlib import Path
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'src'/name/(name+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class MathChecks(unittest.TestCase):
    def test_ridge_mean_scaling_and_intercept(self):
        p1 = load('p1')
        np.testing.assert_allclose(p1.fit_ridge_final(np.eye(2), [2.,4.], .5), [1.,2.], rtol=1e-13)
        rng = np.random.default_rng(13)
        X = rng.normal(size=(7,4)); y = rng.normal(size=7)
        lam = .3
        theta = p1.fit_ridge_final(X,y,lam)
        np.testing.assert_allclose(X.T@(X@theta-y)/7+lam*theta, 0, atol=1e-13)
    def test_cv_exact_tie_and_mse(self):
        p1 = load('p1')
        records = [(c,f,np.array([0.,0.]),np.array([1.,3.])) for c in range(2) for f in range(5)]
        selected, errors = p1.score_and_select_cv(records,[.1,.3])
        self.assertEqual(selected,.1)
        np.testing.assert_array_equal(errors,np.full((2,5),5.))
    def test_pca_order_and_spectral_error(self):
        p2 = load('p2')
        images = np.arange(24.).reshape(4,2,3)
        X = p2.build_data_matrix(images)
        np.testing.assert_array_equal(X[:,1],[6,7,8,9,10,11])
        X = np.random.default_rng(12).normal(size=(6,4))
        mu,U,s = p2.pca(X)
        np.testing.assert_allclose(mu,X.mean(axis=1,keepdims=True))
        np.testing.assert_allclose(U.T@U,np.eye(4),atol=1e-13)
        for k in (1,2,4):
            coords, rebuilt = p2.project_and_reconstruct(X,mu,U,k)
            self.assertEqual(coords.shape,(k,4))
            self.assertAlmostEqual(np.sum((X-rebuilt)**2),sum(s[k:]**2),places=12)
        np.testing.assert_allclose(rebuilt,X,atol=1e-13)

if __name__ == '__main__':
    unittest.main(verbosity=2)
