"""Author model checks; no MNIST access or training."""
from test_math import load
import unittest
import torch
from torch import nn

class ModelChecks(unittest.TestCase):
    def test_architectures(self):
        p3 = load('p3')
        for name,count,types in [('A',7850,[nn.Linear]),('B',50890,[nn.Linear,nn.Linear]),('C',50890,[nn.Linear,nn.ReLU,nn.Linear])]:
            model=p3.build_model(name)
            leaves=[m for m in model.modules() if not list(m.children())]
            self.assertEqual([type(m) for m in leaves],types)
            self.assertTrue(all(m.bias is not None for m in leaves if isinstance(m,nn.Linear)))
            self.assertEqual(p3.parameter_count(model),count)
            x=torch.randn(3,784)
            self.assertEqual(model(x).shape,(3,10))
    def test_b_affine_collapse(self):
        p3=load('p3'); torch.manual_seed(666)
        model=p3.build_model_b().double(); first,last=list(model.children())
        x=torch.randn(7,784,dtype=torch.float64)
        collapsed=x@(last.weight@first.weight).T+last.weight@first.bias+last.bias
        torch.testing.assert_close(model(x),collapsed,rtol=1e-12,atol=1e-12)

if __name__ == '__main__':
    unittest.main(verbosity=2)
