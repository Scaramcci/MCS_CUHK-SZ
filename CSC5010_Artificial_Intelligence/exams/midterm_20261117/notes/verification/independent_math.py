#!/usr/bin/env python3
"""Independent, deterministic standard-library checks for authored study notes."""
from collections import Counter, deque
from fractions import Fraction as F
from itertools import product
from math import factorial, comb, exp, pi, sqrt
import hashlib, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CHECKS=[]
def ck(name, actual, expected):
    assert actual==expected, (name,actual,expected)
    CHECKS.append({'name':name,'actual':str(actual),'status':'passed'})

# Implicit-graph BFS, not branching-factor approximation.
s=(2,8,3,1,6,4,7,0,5); q=deque([(s,0)]);seen={s};layers=Counter()
while q:
    b,d=q.popleft();layers[d]+=1
    if d==5:continue
    z=b.index(0);r,c=divmod(z,3)
    for dr,dc in ((-1,0),(1,0),(0,-1),(0,1)):
        rr,cc=r+dr,c+dc
        if 0<=rr<3 and 0<=cc<3:
            bb=list(b);j=3*rr+cc;bb[z],bb[j]=bb[j],bb[z];bb=tuple(bb)
            if bb not in seen:seen.add(bb);q.append((bb,d+1))
ck('8-puzzle BFS layers',list(layers.values()),[1,3,5,10,14,28])
ck('BFS goal half layer5',sum(layers[i] for i in range(5))+layers[5]//2,47)
ck('IDDFS reached versus expanded', (sum(sum(2**i for i in range(l+1)) for l in range(4)),sum(sum(2**i for i in range(l)) for l in range(4))),(26,11))

# Dijkstra from source graph; tie order lexical.
edges=[('a','b',4),('a','h',8),('b','h',1),('b','c',8),('h','i',7),('h','g',1),('i','c',2),('i','g',6),('g','f',2),('c','f',4),('c','d',7),('d','f',14),('d','e',9),('f','e',10)]
def graph(edges,undirected=True):
    g={n:[] for u,v,w in edges for n in (u,v)}
    for u,v,w in edges:
        g[u].append((v,w))
        if undirected:g[v].append((u,w))
    return g

def search(g,start,goal=None,h=None,reopen=True):
    h=h or {n:0 for n in g};dist={n:float('inf') for n in g};dist[start]=0
    opened={start};closed=set();parent={};popped=[];states=[]
    while opened:
        u=min(opened,key=lambda n:(dist[n]+h[n],n));opened.remove(u);popped.append(u)
        if u==goal:break
        closed.add(u)
        for v,w in g[u]:
            if dist[u]+w<dist[v] and (v not in closed or reopen):
                dist[v]=dist[u]+w;parent[v]=u;opened.add(v);closed.discard(v)
        states.append((u,sorted([(v,dist[v],dist[v]+h[v]) for v in opened],key=lambda z:(z[2],z[0]))))
    return dist,parent,popped,states
D,P,order,_=search(graph(edges),'a')
ck('Dijkstra distances',D,dict(a=0,b=4,h=5,g=6,f=8,c=12,i=12,e=18,d=19))
ck('Dijkstra order',order,list('abhgfcied'))
ck('Dijkstra parent',P,dict(b='a',h='b',c='b',g='h',i='h',f='g',e='f',d='c'))

edgesA=[('A','X',17),('X','B',16),('X','C',11),('C','L',20),('C','W',11),('W','B',12),('W','K',10),('W','T',9),('B','T',17),('B','S',7),('S','H',6)]
h=dict(A=30,X=27,B=16,C=17,L=33,W=9,K=19,T=0,S=17,H=22)
for hb,expected in [(16,['A','X','C','W','T']),(6,['A','X','B','C','W','T'])]:
    hh={**h,'B':hb};d,p,o,st=search(graph(edgesA),'A','T',hh)
    ck(f'A* hB={hb} pop and result',(o,d['T']), (expected,48))
    ck(f'A* hB={hb} goal parent',p['T'],'W')
    true={n:search(graph(edgesA),'T')[0][n] for n in h}
    ck(f'A* hB={hb} admissible',all(0<=hh[n]<=true[n] for n in h),True)
ck('A* changed heuristic inconsistent',h['X']>16+6,True)
g=graph([('S','A',3),('S','B',1),('B','A',1),('A','G',3)],False);hh=dict(S=0,A=0,B=4,G=0)
ck('reopen example optimal',search(g,'S','G',hh)[0]['G'],5)
ck('no-reopen example suboptimal',search(g,'S','G',hh,False)[0]['G'],6)

start=(7,2,4,5,0,6,8,3,1);goal=(0,1,2,3,4,5,6,7,8)
md=[abs(start.index(k)//3-goal.index(k)//3)+abs(start.index(k)%3-goal.index(k)%3) for k in range(1,9)]
ck('Manhattan tilewise',md,[3,1,2,2,2,3,3,2]);ck('Manhattan sum',sum(md),18)

# Exact legal game history count: terminal win halts immediately.
lines=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
leaf=Counter()
def ttt(b=('',)*9,depth=0):
    won=next((b[a] for a,c,d in lines if b[a] and b[a]==b[c]==b[d]),None)
    if won or depth==9:
        leaf[(depth,won or 'draw')]+=1;return
    mark='X' if depth%2==0 else 'O'
    for i,x in enumerate(b):
        if not x:ttt(b[:i]+(mark,)+b[i+1:],depth+1)
ttt()
ck('TTT terminal history counts',dict(leaf),{(5,'X'):1440,(6,'O'):5328,(7,'X'):47952,(8,'O'):72576,(9,'X'):81792,(9,'draw'):46080})

def ab(tree,ismax=True,a=float('-inf'),b=float('inf'),seen=None):
    if isinstance(tree,int):seen.append(tree);return tree
    value=float('-inf') if ismax else float('inf')
    for child in tree:
        v=ab(child,not ismax,a,b,seen)
        if ismax:value=max(value,v);a=max(a,value)
        else:value=min(value,v);b=min(b,value)
        if a>=b:break
    return value
for name,tree,n in [('slide66upper',[[[3,4],[1,2]],[[7,8],[5,6]]],8),('slide66lower',[[[6,5],[8,7]],[[2,1],[3,4]]],5),('teaching',[[3,5,6],[2,9,4],[4,7,8]],7)]:
    seq=[];value=ab(tree,seen=seq);ck(name+' evaluation count',len(seq),n);ck(name+' root',value,4 if name=='teaching' else 6)
b=['']*9;b[4]='X';b[1]='O'
def open_score(b):return sum(not any(b[i]=='O' for i in line) for line in lines)-sum(not any(b[i]=='X' for i in line) for line in lines)
ck('Game4 initial score',open_score(b),2)
worsts={}
for xm in range(9):
    if b[xm]:continue
    bb=b.copy();bb[xm]='X';scores=[]
    for om in range(9):
        if bb[om]:continue
        bbb=bb.copy();bbb[om]='O';scores.append(open_score(bbb))
    worsts[xm]=min(scores)
ck('Game4 all moves backup',worsts,{0:1,2:1,3:0,5:0,6:1,7:0,8:1})
ck('chess evaluations',44**3,85184)

# Constraint consistency and exact deterministic domain updates.
E=['ab','ac','ad','bc','be','cd','ce','de'];assignment=dict(a=1,b=2,c=3,d=2,e=1)
ck('CSP1 constraints',all(assignment[u]!=assignment[v] for u,v in E),True)
D={k:set(range(1,5)) for k in 'abcde'};D['a']={1,2};D['b']={1,2,3}
steps=[]
for var in 'abcde':
    vals={k:v for k,v in D.items() if k not in assignment or k==var}
    val=assignment[var];ck('CSP1 remaining legal '+var,val in D[var],True)
    for u,v in E:
        if u==var:D[v].discard(val)
        if v==var:D[u].discard(val)
    steps.append({k:sorted(D[k]) for k in 'abcde' if k>var})
ck('CSP1 e remains 14 after d=2',steps[3],{'e':[1,4]})
cc=[]
for r in range(1,5):cc.append(sum(r==1 or abs(r-1)==abs(2-j) for j in [1,3,4]))
ck('min-conflicts candidate attacks',cc,[3,2,1,0])

# Boolean semantic checks, independent truth-table enumeration.
def imp(a,b):return not a or b
for p,q,r in product([False,True],repeat=3):
    f=(not imp(p,q)) or r
    ck('NNF-CNF-DNF '+str((p,q,r)),f,((p or r) and ((not q) or r)))
    f=imp(p or q,(not p) and r)
    ck('slide normal form '+str((p,q,r)),f,(not p) and ((not q) or r))
models=[x for x in product([False,True],repeat=3) if imp(x[0],x[1]) and imp(x[1],x[2]) and imp(x[2],not x[0])]
ck('HW5D models',models,[(False,False,False),(False,False,True),(False,True,True)])
ck('HW5A counterexample',imp((True or False) and ((not True) or True),not(False or True)),False)
clauses=[{1,2,-3,4},{-1,3,4},{-2,-3},{1,-4},{-1,-3},{3}]
models=[]
for x in product([False,True],repeat=4):
    if all(any(x[abs(l)-1] if l>0 else not x[abs(l)-1] for l in c) for c in clauses):models.append(x)
ck('HW5B UNSAT exhaustive',models,[])
res=[(2,5,3,{-2}),(4,5,3,{-1}),(3,7,1,{-4}),(0,5,3,{1,2,4}),(9,6,2,{1,4}),(10,7,1,{4}),(11,8,4,set())]
for a,b,pivot,expected in res:
    c1,c2=clauses[a],clauses[b]
    assert (pivot in c1 and -pivot in c2) or (-pivot in c1 and pivot in c2)
    out=(c1|c2)-{pivot,-pivot};ck('resolution row '+str(len(clauses)+1),out,expected);clauses.append(out)

# Exact probability arithmetic.
ck('coin probabilities',(F(comb(10,5),2**10),F(2*comb(10,4),2**10)),(F(63,256),F(105,256)))
ck('Bayes test',F(95,100)*F(4,100)/(F(95,100)*F(4,100)+F(1,100)*F(96,100)),F(95,119))
ck('Bayes unprepared',F(1,16)/(F(1,16)+F(3,4)*F(9,10)),F(5,59))
sm=F(7,20)*F(6,7)*F(1,7)*F(2,7)*F(5,7);sn=F(13,20)*F(1,13)*F(3,13)*F(3,13)*F(9,13)
ck('animal unsmoothed scores',(sm,sn),(F(3,343),F(81,43940)));ck('animal posterior',sm/(sm+sn),F(43940,53201))
sm=F(8,22)*F(7,9)*F(2,9)*F(3,10)*F(6,9);sn=F(14,22)*F(2,15)*F(4,15)*F(4,16)*F(10,15)
ck('animal smoothed posterior',sm/(sm+sn),F(10,13));ck('bank posterior',F(1,5)/(F(1,5)+F(4,245)),F(49,53))

def compositions(n,k):
    if k==1:yield (n,);return
    for i in range(n+1):
        for tail in compositions(n-i,k-1):yield(i,)+tail

def multinomial(counts,p):
    n=sum(counts);coef=factorial(n)
    for c in counts:coef//=factorial(c)
    v=F(coef)
    for c,pp in zip(counts,p):v*=pp**c
    return v
p=[F(44,100),F(42,100),F(1,10),F(4,100)];alln=list(compositions(10,4))
ck('blood all count compositions',len(alln),286)
ck('blood unrestricted maximum',max(alln,key=lambda n:multinomial(n,p)),(5,4,1,0))
ck('blood all-positive maximum',max((n for n in alln if all(n)),key=lambda n:multinomial(n,p)),(4,4,1,1))
for N in [0,1,5,25,100,1000]:
    p=[(N*x+1)/(N+5) for x in [F(24,100),F(22,100),F(1,5),F(18,100),F(16,100)]]
    alln=list(compositions(4,5));mx=max(multinomial(n,p) for n in alln);mn=min(multinomial(n,p) for n in alln)
    ck(f'student mode/min N={N}',(multinomial((1,1,1,1,0),p)==mx,multinomial((0,0,0,0,4),p)==mn),(True,True))

# Matrix / Markov and exact Bayesian-network extension checks.
seq='S S R C C R R S S S R C C R S S C'.split();N=Counter(zip(seq,seq[1:]))
ck('weather transitions',[[N[i,j] for j in 'SCR'] for i in 'SCR'],[[4,1,2],[0,2,2],[2,2,1]])
A=[[F(8,10),F(15,100),F(5,100)],[F(38,100),F(6,10),F(2,100)],[F(75,100),F(5,100),F(2,10)]]
pi0=[F(638,929),F(245,929),F(46,929)]
def mul(p,A):return [sum(p[i]*A[i][j] for i in range(len(p))) for j in range(len(p))]
ck('stationary vector',mul(pi0,A),pi0);ck('3 sunny stationary',pi0[0]*A[0][0]**2,F(10208,23225))
def seqprob(s):
    v=pi0[s[0]]
    for i,j in zip(s,s[1:]):v*=A[i][j]
    return v
m=max((seqprob(s),s) for s in product(range(3),repeat=4));ck('4-day maximum',m,(F(40832,116125),(0,0,0,0)))
hc,hr=F(820,319),F(450,319)
ck('waiting equation C',hc,1+A[1][1]*hc+A[1][2]*hr);ck('waiting equation R',hr,1+A[2][1]*hc+A[2][2]*hr)
ck('rain two-day sun',sum(A[2][j]*A[j][0] for j in range(3)),F(769,1000))
O=[[10,3,12],[8,14,7],[14,17,7],[12,7,4]];rows=list(map(sum,O));cols=list(map(sum,zip(*O)))
chi=sum((F(O[i][j])-F(rows[i]*cols[j],115))**2/F(rows[i]*cols[j],115) for i in range(4) for j in range(3))
assert abs(float(chi)-14.5080371105)<1e-9;CHECKS.append({'name':'Game/Snack chi-square','actual':float(chi),'status':'passed'})
# Enumerate independent rain/sprinkler roots and conditional wet observations.
wet=[]
for r,s,h,w in product([False,True],repeat=4):
    pr=F(1,5) if r else F(4,5);ps=F(1,10) if s else F(9,10)
    ph=F(1) if r else (F(9,10) if s else F(1,10));pw=F(1) if r else F(1,5)
    v=pr*ps*(ph if h else 1-ph)*(pw if w else 1-pw);wet.append((r,s,h,w,v))
def wsum(test):return sum(x[4] for x in wet if test(*x[:4]))
ph=wsum(lambda r,s,h,w:h);phw=wsum(lambda r,s,h,w:h and w)
ck('wet CPT total',sum(x[4] for x in wet),1)
ck('wet posteriors',(ph,wsum(lambda r,s,h,w:r and h)/ph,wsum(lambda r,s,h,w:s and h)/ph,phw/ph,wsum(lambda r,s,h,w:r and h and w)/phw,wsum(lambda r,s,h,w:s and h and w)/phw),(F(43,125),F(25,43),F(23,86),F(143,215),F(125,143),F(43,286)))
# Burglary network using exact decimal inputs.
pa_b=F(95,100)*F(2,1000)+F(94,100)*F(998,1000);pj_b=F(9,10)*pa_b+F(5,100)*(1-pa_b)
ck('alarm P(A|B)',pa_b,F('0.94002'));ck('alarm P(J|B)',pj_b,F('0.849017'))
pa_nb=F(29,100)*F(2,1000)+F(1,1000)*F(998,1000)
ck('alarm P(A|notB,J)',F(9,10)*pa_nb/(F(9,10)*pa_nb+F(5,100)*(1-pa_nb)),F(14202,513413))
pa=pa_b*F(1,1000)+pa_nb*F(999,1000);ck('alarm P(A)',pa,F('0.002516442'))
assert abs(float(pa_b*F(9,10)/pj_b)-.99647)<.000005
CHECKS.append({'name':'alarm P(A|B,J)','actual':str(pa_b*F(9,10)/pj_b),'status':'passed'})

ck('new teaching propagation',mul([F(1,2),F(1,3),F(1,6)],A),[F(391,600),F(17,60),F(13,200)])
# Independent transcription from visible 20-row animal original (B,F,W,L,class).
animals=[
('y','n','n','y','M'),('n','n','n','n','N'),('n','n','y','n','N'),('y','n','y','n','M'),
('n','n','s','y','N'),('n','n','n','y','N'),('y','y','n','y','M'),('n','y','n','y','N'),
('y','n','n','y','M'),('y','n','y','n','N'),('n','n','s','y','N'),('n','n','s','y','N'),
('y','n','n','y','M'),('n','n','y','n','N'),('n','n','s','y','N'),('n','n','n','y','N'),
('n','n','n','y','M'),('n','y','n','y','N'),('y','n','y','n','M'),('n','y','n','y','N')]
for cl,expected in [('M',[6,1,2,5]),('N',[1,3,3,9])]:
    subset=[r for r in animals if r[4]==cl]
    ck('animal visible table yes counts '+cl,[sum(r[j]=='y' for r in subset) for j in range(4)],expected)
    ck('animal water three categories '+cl,[sum(r[2]==v for r in subset) for v in ['y','n','s']],[2,5,0] if cl=='M' else [3,6,4])
# Topological result edge-by-edge; original directed graph transcription.
top=list('pnosmryvxwzuqt')
TE={'p':'osz','n':'oqu','o':'rsv','s':'r','m':'qrx','r':'uy','y':'v','v':'wx','w':'z','u':'t','q':'t'}
ck('HW2 topological ordering',all(top.index(u)<top.index(v) for u,vs in TE.items() for v in vs),True)
files=sorted((ROOT/'讲义').glob('*.md'))+sorted((ROOT/'开卷参考资料/chapters').glob('*.tex'))
result={'executor':'/root/verify_math','python':sys.version,'checks':CHECKS,'count':len(CHECKS),'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
print(json.dumps(result,ensure_ascii=False,indent=2))
