from collections import Counter
s=(2,8,3,1,6,4,7,0,5)
front=[(s,None)];counts=[]
for d in range(6):
 counts.append(len(front));nxt=[]
 for b,prev in front:
  j=b.index(0)
  for k in range(9):
   if abs(j//3-k//3)+abs(j%3-k%3)==1:
    a=list(b);a[j],a[k]=a[k],a[j];a=tuple(a)
    if a!=prev:nxt.append((a,b))
 front=nxt
print('BFS no immediate reversal depths0..5',counts,'halfway',sum(counts[:-1])+counts[-1]//2)
edges=[('a','b',4),('a','h',8),('b','h',1),('b','c',8),('h','i',7),('h','g',1),('i','c',2),('i','g',6),('c','d',7),('c','f',4),('g','f',2),('d','f',14),('d','e',9),('f','e',10)]
adj={x:[] for x in 'abcdefghi'}
for a,b,w in edges:adj[a].append((b,w));adj[b].append((a,w))
d={x:float('inf') for x in adj};d['a']=0;closed=set()
while len(closed)<9:
 a=min(set(adj)-closed,key=lambda x:(d[x],x));closed.add(a)
 for b,w in adj[a]:d[b]=min(d[b],d[a]+w)
 print('Dijkstra',a,d)
adj={'q':['s','t','w'],'r':['u','y'],'s':['v'],'t':['x','y'],'u':['y'],'v':['w'],'w':['s'],'x':['z'],'y':['q'],'z':['x']}
time=0;seen=set();timestamps={};order=[]
def dfs(a):
 global time
 seen.add(a);time+=1;timestamps[a]=[time];order.append(a)
 for b in adj[a]:
  if b not in seen:dfs(b)
 time+=1;timestamps[a].append(time)
for a in ['v']+sorted(adj):
 if a not in seen:dfs(a)
print('DFS4',order,timestamps)
edges=[('A','X',17),('X','B',16),('X','C',11),('C','L',20),('C','W',11),('B','W',12),('B','S',7),('S','H',6),('B','T',17),('W','T',9),('W','K',10)]
adj={x:[] for x in 'AXBCWSHLTK'}
for a,b,w in edges:adj[a].append((b,w));adj[b].append((a,w))
for bh in [16,6]:
 h={'A':30,'X':27,'B':bh,'C':17,'W':9,'S':17,'H':22,'L':33,'T':0,'K':19}
 g={'A':0};q={'A'};closed=set();parent={}
 while q:
  a=min(q,key=lambda x:(g[x]+h[x],x));q.remove(a);closed.add(a)
  print('AStar',bh,'pop',a,'g,f',g[a],g[a]+h[a])
  if a=='T':break
  for b,w in adj[a]:
   if g[a]+w<g.get(b,float('inf')):
    g[b]=g[a]+w;parent[b]=a;q.add(b);closed.discard(b)
  print(' OPEN',[(b,g[b],g[b]+h[b]) for b in sorted(q,key=lambda b:(g[b]+h[b],b))])
 print('parents',parent)
top={'m':['q','r','x'],'n':['o','q','u'],'o':['r','s','v'],'p':['o','s','z'],'q':['t'],'r':['u','y'],'s':['r'],'t':[],'u':['t'],'v':['w','x'],'w':['z'],'x':[],'y':['v'],'z':[]}
ordering=['p','n','o','s','m','r','y','v','x','w','z','u','q','t']
assert all(ordering.index(a)<ordering.index(b) for a in top for b in top[a])
print('All 21 topology edges forward',sum(len(v) for v in top.values()),ordering)
literal={'S':['A'],'A':['B','D2'],'B':['C','E'],'C':[],'E':['D1','F'],'D1':[],'F':['G'],'G':[],'D2':[]}
tm=0;tt={}
def walk(a):
 global tm
 tm+=1;tt[a]=[tm]
 for b in literal[a]:walk(b)
 tm+=1;tt[a].append(tm)
walk('S');print('DFS2 literal',tt)
# Assert uniqueness of all non-reversing eight-puzzle states through depth5.
front=[(s,None)];seen=set()
for d in range(6):
 assert len({b for b,p in front})==len(front)
 assert not seen.intersection({b for b,p in front})
 seen.update(b for b,p in front)
 hist=Counter('center' if b.index(0)==4 else 'corner' if b.index(0) in [0,2,6,8] else 'edge' for b,p in front)
 print('BFS blanks',d,dict(hist))
 nxt=[]
 for b,prev in front:
  j=b.index(0)
  for k in range(9):
   if abs(j//3-k//3)+abs(j%3-k%3)==1:
    a=list(b);a[j],a[k]=a[k],a[j];a=tuple(a)
    if a!=prev:nxt.append((a,b))
 front=nxt
