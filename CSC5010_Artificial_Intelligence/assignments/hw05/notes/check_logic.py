"""Author self-check of HW05; standard library, no input data or randomness."""
from itertools import product

T, F = True, False
imp = lambda x, y: not x or y
assert not imp((T or F) and (not T or T), not (F or T))
print('A: confirmed negated-conclusion statement has counterexample (T,F,T).')

# Literal (name, sign); a clause is a set of disjoined literals.
def clause(*items):
    return frozenset((x.lstrip('~'), not x.startswith('~')) for x in items)

cs = [None, clause('p', 'q', '~r', 's'), clause('~p', 'r', 's'),
      clause('~q', '~r'), clause('p', '~s'), clause('~p', '~r'), clause('r')]
steps = [(3, 6, 'r', clause('~q')), (5, 6, 'r', clause('~p')),
         (4, 8, 'p', clause('~s')), (1, 6, 'r', clause('p', 'q', 's')),
         (10, 7, 'q', clause('p', 's')), (11, 8, 'p', clause('s')),
         (12, 9, 's', clause())]
for i, j, pivot, expected in steps:
    pos, neg = (pivot, True), (pivot, False)
    assert (pos in cs[i] and neg in cs[j]) or (neg in cs[i] and pos in cs[j])
    actual = (cs[i] | cs[j]) - {pos, neg}
    assert actual == expected
    cs.append(actual)
models_b = []
for values in product((T, F), repeat=4):
    assignment = dict(zip('pqrs', values))
    if all(any(assignment[v] == sign for v, sign in c) for c in cs[1:7]):
        models_b.append(values)
assert not models_b
print('B: all 7 resolution steps match; 0 of 16 assignments satisfy the six clauses.')

scores = {}
for p, q, r in product((T, F), repeat=3):
    vals = (p or not q, not p or q, q or r, q or not r, not q or not r)
    scores[p, q, r] = sum(vals)
assert scores[T, T, F] == 5 and max(scores.values()) == 5
print('C: maximum 5 of 5; witness (T,T,F).')

expected = [(T,T,F,F),(T,F,T,F),(F,T,F,F),(F,T,T,F),
            (T,T,T,T),(T,F,T,F),(T,T,T,T),(T,T,T,T)]
models_d = []
for abc, row in zip(product((T,F), repeat=3), expected):
    a,b,c = abc
    vals = (imp(a,b), imp(b,c), imp(c,not a))
    actual = (*vals, all(vals))
    assert actual == row
    assert all(vals) == (not a and (not b or c))
    if all(vals):
        models_d.append(abc)
assert models_d == [(F,T,T),(F,F,T),(F,F,F)]
print('D: all 8 truth-table rows match; exactly 3 simultaneous models:', models_d)
print('PASS: author self-check only, not independent verification.')
