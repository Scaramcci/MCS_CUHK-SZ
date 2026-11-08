"""Author self-check of enumerated probabilities and teacher-table arithmetic."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
from math import prod, factorial

for q in [[F(n,100) for n in (24,22,20,18,16)], [F(n,105) for n in (25,23,21,19,17)]]:
    d = {k:F(24,prod(factorial(n) for n in k))*prod(p**n for p,n in zip(q,k)) for k in product(range(5),repeat=5) if sum(k)==4}
    assert len(d)==70 and sum(d.values())==1
    assert max(d,key=d.get)==(1,1,1,1,0) and min(d,key=d.get)==(0,0,0,0,4)
    print('Q1', [float(d[k]) for k in [(0,0,0,4,0),(2,2,0,0,0),(1,1,1,1,0),(0,0,0,0,4)]])
assert F(1,16)/(F(1,16)+F(9,10)*F(3,4))==F(5,59)
# p.3 records: yes=1, no=0, sometimes=2, last field=mammal.
animals=[(1,0,0,1,1),(0,0,0,0,0),(0,0,1,0,0),(1,0,1,0,1),(0,0,2,1,0),(0,0,0,1,0),(1,1,0,1,1),(0,1,0,1,0),(1,0,0,1,1),(1,0,1,0,0),(0,0,2,1,0),(0,0,2,1,0),(1,0,0,1,1),(0,0,1,0,0),(0,0,2,1,0),(0,0,0,1,0),(0,0,0,1,1),(0,1,0,1,0),(1,0,1,0,1),(0,1,0,1,0)]
scores=[]
for cls, expected in [(1,[6,1,2,5]),(0,[1,3,3,9])]:
    rows=[r for r in animals if r[-1]==cls]
    counts=[sum(r[i]==1 for r in rows) for i in range(4)]
    assert counts==expected
    scores.append(F(len(rows),20)*prod(F(n,len(rows)) for n in counts))
assert scores==[F(3,343),F(81,43940)]
print('Q3 scores',scores,'posterior',float(scores[0]/sum(scores)))
seq='SSRCCRRSSSRCCRSSC'; c=Counter(zip(seq,seq[1:]))
assert [[c[a,b] for b in 'SCR'] for a in 'SCR']==[[4,1,2],[0,2,2],[2,2,1]]
print('Q4',c)
A=[[F(n,100) for n in row] for row in [(80,15,5),(38,60,2),(75,5,20)]]
pi=[F(n,929) for n in (638,245,46)]
assert sum(pi)==1 and all(sum(pi[i]*A[i][j] for i in range(3))==pi[j] for j in range(3))
assert pi[0]*A[0][0]**2==F(10208,23225)
print('Q5',pi,float(pi[0]*A[0][0]**2))
# p.6: M Hi/Lo, E Good/Bad, A Working/Broken, C Hi/Lo coded 0/1.
table=[(0,0,0,3,4),(0,0,1,1,2),(0,1,0,1,5),(0,1,1,0,4),(1,0,0,9,0),(1,0,1,5,1),(1,1,0,1,2),(1,1,1,0,2)]
records=[]
for m,e,a,hi,lo in table: records.extend([(m,e,a,0)]*hi+[(m,e,a,1)]*lo)
assert len(records)==40
pm=[F(sum(r[0]==m for r in records),40) for m in range(2)]
pa=[F(sum(r[2]==a for r in records),40) for a in range(2)]
pe={(m,e):F(sum(r[:2]==(m,e) for r in records),sum(r[0]==m for r in records)) for m,e in product(range(2),repeat=2)}
pc={(e,a,c):F(sum(r[1:]==(e,a,c) for r in records),sum(r[1:3]==(e,a) for r in records)) for e,a,c in product(range(2),repeat=3)}
joint={(m,e,a,c):pm[m]*pa[a]*pe[m,e]*pc[e,a,c] for m,e,a,c in product(range(2),repeat=4)}
assert sum(joint.values())==1
assert sum(v for (m,e,a,c),v in joint.items() if e==1 and a==1)==F(9,64)
print('Q6',pm,pa,pe,pc,'query=9/64')
pb=[F(9,10),F(1,10)];pf=[F(8,10),F(2,10)]
gempty=[[F(1,10),F(8,10)],[F(2,10),F(9,10)]]
sno=[[F(1,10),F(8,10)],[F(9,10),F(1)]]
joint={(b,f,g,s):pb[b]*pf[f]*(gempty[b][f] if g else 1-gempty[b][f])*(sno[b][f] if s else 1-sno[b][f]) for b,f,g,s in product(range(2),repeat=4)}
assert sum(joint.values())==1
assert joint[0,1,1,0]==F(288,10000) and joint[1,1,0,1]==F(2,1000)
assert sum(v for (b,f,g,s),v in joint.items() if b==1 and s==0)/pb[1]==F(8,100)
print('Q7: 0.0288, 0.002, 0.08')
print('All author checks passed; not independent verification.')
