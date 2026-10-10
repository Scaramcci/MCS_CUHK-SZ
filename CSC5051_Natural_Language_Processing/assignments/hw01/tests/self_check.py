"""Analytic self-checks: load function definitions without running the full notebook."""
import ast
import json
import math
import sys
from pathlib import Path
import numpy as np
import torch
from torch import nn
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

root = Path(__file__).resolve().parents[1]
path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / 'report/26Fall_NLP_Assignment_1_CSC6052_5051_MDS5110.ipynb'
nb = json.loads(path.read_text())
ns = dict(np=np, torch=torch, nn=nn, math=math, TruncatedSVD=TruncatedSVD,
          cosine_similarity=cosine_similarity, SEED=42, word_tokenize=lambda s: s.split())
for i in [23, 27, 45, 74, 81]:
    tree = ast.parse(''.join(nb['cells'][i]['source']))
    defs = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
    exec(compile(ast.Module(body=defs, type_ignores=[]), str(path), 'exec'), ns)

# Exact labels/context pairing, unknown targets and incomplete windows filtered,
# and final partial batch retained.
np.random.seed(42)
examples = [(1, [2, 3]), (2, [1, 3]), (3, [1, 2]), (0, [1, 2]), (1, [2])]
batches = list(ns['make_cbow_batches_iter'](examples, 1, 2))
assert [len(b['labels']) for b in batches] == [2, 1]
actual = sorted((int(y), tuple(x)) for b in batches for x, y in zip(b['tokens'].tolist(), b['labels'].tolist()))
assert actual == [(1, (2, 3)), (2, (1, 3)), (3, (1, 2))]
assert all(b['tokens'].dtype == b['labels'].dtype == torch.int64 for b in batches)
assert list(ns['make_cbow_batches_iter']([], 1, 2)) == []

# Known weights verify averaging (not sum), batch axis and raw linear logits.
m = ns['CBoWModel'](4, 2)
with torch.no_grad():
    m.embeddings.weight.copy_(torch.tensor([[0., 0.], [2., 0.], [0., 4.], [2., 4.]]))
    m.out_layer.weight.copy_(torch.tensor([[1., 0.], [0., 1.], [1., 1.], [-1., 1.]]))
    m.out_layer.bias.zero_()
x = torch.tensor([[1, 2], [3, 1]])
expected = torch.tensor([[1., 2., 3., 1.], [2., 2., 4., 0.]])
torch.testing.assert_close(m(x), expected)
assert torch.equal(m(x), m(x.flip(1)))
loss = nn.CrossEntropyLoss()(m(x), torch.tensor([1, 2]))
loss.backward()
assert m.embeddings.weight.grad is not None and torch.isfinite(m.embeddings.weight.grad).all()

# Rank-2 diagonal matrix: truncated reconstruction preserves the two nonzero
# singular values and orthogonally invariant Gram matrix.
M = np.diag([3., 2., 0.])
reduced = ns['reduce_to_k_dim'](M, 2)
assert reduced.shape == (3, 2)
np.testing.assert_allclose(reduced @ reduced.T, M @ M.T, atol=1e-10)

class TinyVectors:
    vector_size = 2
    vectors = {'a': np.array([2., 0.], dtype=np.float32),
               'b': np.array([0., 4.], dtype=np.float32)}
    def __contains__(self, word): return word in self.vectors
    def get_vector(self, word): return self.vectors[word]

v = TinyVectors()
embed = ns['get_sentence_embedding']
np.testing.assert_allclose(embed(v, 'A b unknown'), [1., 2.])
np.testing.assert_allclose(embed(v, ['A', 'b', 'unknown']), [1., 2.])
for s in ['', 'unknown', []]:
    np.testing.assert_array_equal(embed(v, s), [0., 0.])
assert embed(v, 'a').dtype == np.float32
find = ns['find_nearest']
texts = ['b', 'a b', 'a']
vecs = np.array([embed(v, s) for s in texts])
assert find(v, vecs, texts, 'a', 2) == ['a', 'a b']
assert find(v, vecs, texts, 'a', 20) == ['a', 'a b', 'b']
assert find(v, vecs, texts, 'a', 0) == []
assert find(v, np.empty((0, 2)), [], 'a', 2) == []
assert find(v, vecs, texts, 'unknown', 2) == texts[:2]
for args in [(vecs, texts, 'a', -1), (vecs, texts[:1], 'a', 1)]:
    try:
        find(v, *args)
    except ValueError:
        pass
    else:
        raise AssertionError('Expected invalid retrieval input to fail')
print('PASS: batch pairing/tail, mean-context logits/gradients, SVD, OOV/case, cosine ranking/ties/limits')
