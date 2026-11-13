#!/usr/bin/env python3
"""Incremental independent checks for added MD examples, 2026-11-13."""
from pathlib import Path
from itertools import product
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
checks=[]
def ck(name,a,b):
 assert a==b,(name,a,b)
 checks.append({'name':name,'actual':str(a),'status':'passed'})
lines=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
def won(b):return any(b[a]!='' and b[a]==b[c]==b[d] for a,c,d in lines)
for n,moves,expected in [(1,['X2','O5','X3','O1','X9','O6','X4','O7','X8'],'OXX/XOO/OXX'),(2,['X2','O3','X5','O8','X1','O9','X6','O4','X7'],'XXO/OXX/XOO')]:
 b=['']*9
 for step,m in enumerate(moves):
  mark=m[0];cell=int(m[1])-1
  assert mark==('X' if step%2==0 else 'O') and not b[cell]
  assert not won(b),'premature terminal before move'
  b[cell]=mark
 ck(f'Game2 line {n} final', '/'.join(''.join(b[i:i+3]) for i in (0,3,6)),expected)
 ck(f'Game2 line {n} draw',won(b),False)
ck('TWO numerical arithmetic',734+734,1468)
F,T,U,W,R,O,x1,x2,x3=1,7,6,3,8,4,0,0,1
ck('TWO carry column1',2*O,R+10*x1)
ck('TWO carry column2',x1+2*W,U+10*x2)
ck('TWO carry column3',x2+2*T,O+10*x3)
ck('TWO carry column4',x3,F)
ck('TWO all different letters',len({F,T,U,W,R,O}),6)
def attacks(q,col):
 return [sum(r==q[j] or abs(r-q[j])==abs(col-j) for j in range(len(q)) if j!=col) for r in range(1,len(q)+1)]
q=[2,4,6,1,1,1]
ck('six queen column5 conflicts',attacks(q,4),[3,3,0,2,0,2]);q[4]=3
ck('six queen column6 conflicts',attacks(q,5),[1,2,3,2,0,1]);q[5]=5
ck('six queen final pair conflicts',sum(q[i]==q[j] or abs(q[i]-q[j])==j-i for i in range(6) for j in range(i+1,6)),0)
def imp(a,b):return (not a) or b
models=[]
for h,m,s,r in product([False,True],repeat=4):
 k=imp(h,m)
 premises=imp(s,imp(k,r)) and imp(imp(m,k),imp(k,s)) and m and imp(m,k)
 if premises:models.append((h,m,s,r));assert r
ck('logic p35 entailed R',len(models),2)
a=[];b=[];c=[]
for p,q in product([False,True],repeat=2):
 if (p or not q) and (not p or q) and (not p or not q):a.append((p,q))
 if imp(p,q) and imp(p,not q) and imp(not p,q) and imp(not p,not q):b.append((p,q))
 if (p==q) and ((not p)==q):c.append((p,q))
ck('Ex61a models',a,[(False,False)]);ck('Ex61b models',b,[]);ck('Ex61c models',c,[])
clauses=[
 [[1,2,-3],[1,-2,-4],[1,-3,-4],[-1,-2,-4],[1,2,-4]],
 [[-1,-2,3],[-1,2,-4],[1,-2,-4],[-1,-3,-4],[1,2,-3],[1,-3,-4]],
 [[1,2,3],[1,-2,-4],[2,-3,4],[-1,3,4],[-1,2,-4],[1,-2,-3],[-1,-2,4],[-1,-3,-4]]]
for n,(cs,vals) in enumerate(zip(clauses,[(False,False,False,False),(False,False,False,False),(False,False,True,True)]),1):
 ck(f'Ex62 witness {n}',all(any(vals[abs(l)-1] if l>0 else not vals[abs(l)-1] for l in cl) for cl in cs),True)
ck('Ex30 distinct variable counts',[len(set(vs)) for vs in ['qp','pts','prstuv','prsqtrt']],[2,3,6,5])
ck('Ex30 rows',[2**n for n in [2,3,6,5]],[4,8,64,32])
outputs=[[],[],[],[],[],[]]
for p,q in product([False,True],repeat=2):
 vals=[p and not p,p or not p,imp(p or not q,q),imp(p or q,p and q),imp(p,q)==imp(not q,not p),imp(imp(p,q),imp(q,p))]
 for i,v in enumerate(vals):outputs[i].append(v)
ck('Ex31 columns',outputs,[[False]*4,[True]*4,[False,True,False,True],[True,False,False,True],[True]*4,[True,False,True,True]])
files=sorted((ROOT/'讲义').glob('*.md'))+sorted((ROOT/'开卷参考资料/chapters').glob('*.tex'))
print(json.dumps({'executor':'/root/verify_math','scope':'incremental added examples only; old98 retained','checks':checks,'count':len(checks),'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},ensure_ascii=False,indent=2))
