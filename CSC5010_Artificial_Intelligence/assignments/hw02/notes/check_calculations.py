"""Author self-checks of hand-calculated answers; independent checks are separate."""
from collections import Counter, deque
from functools import lru_cache
import heapq
import json

def graph(edges):
    g = {}
    for a, b, w in edges:
        g.setdefault(a, {})[b] = w
        g.setdefault(b, {})[a] = w
    return g

def trace(g, start, heuristic=None, goal=None, improve=True):
    h = heuristic or {v: 0 for v in g}
    dist = {start: 0}; parent = {}; closed = set(); rows = []
    while True:
        opened = [v for v in dist if v not in closed]
        if not opened: break
        u = min(opened, key=lambda v: (dist[v] + h[v], v))
        closed.add(u)
        if u != goal:
            for v, w in g[u].items():
                candidate = dist[u] + w
                if v not in closed and (v not in dist or improve and candidate < dist[v]):
                    dist[v] = candidate; parent[v] = u
        rows.append({'pop': u, 'g': dict(dist), 'open': [(v, dist[v], dist[v]+h[v]) for v in sorted(dist, key=lambda v: (dist[v]+h[v],v)) if v not in closed]})
        if u == goal: break
    path = []
    if goal:
        v = goal
        while v != start: path.append(v); v = parent[v]
        path.append(start); path.reverse()
    return rows, dist, parent, path

s = (2,8,3,1,6,4,7,0,5)
q = deque([(s, 0)]); seen = {s}; counts = Counter()
while q:
    b,d = q.popleft(); counts[d] += 1
    if d == 5: continue
    z=b.index(0); r,c=divmod(z,3)
    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        rr,cc=r+dr,c+dc
        if 0<=rr<3 and 0<=cc<3:
            bb=list(b); j=rr*3+cc; bb[z],bb[j]=bb[j],bb[z]; bb=tuple(bb)
            if bb not in seen: seen.add(bb); q.append((bb,d+1))
print('BFS', dict(counts), 'halfway count', sum(counts[d] for d in range(5))+counts[5]//2)

dg=graph([('a','b',4),('a','h',8),('b','h',1),('b','c',8),('h','i',7),('h','g',1),('i','c',2),('i','g',6),('c','d',7),('c','f',4),('g','f',2),('f','d',14),('f','e',10),('d','e',9)])
print('DIJKSTRA', json.dumps(trace(dg,'a'),indent=2))
ag=graph([('A','X',17),('X','B',16),('X','C',11),('C','L',20),('C','W',11),('B','W',12),('B','S',7),('B','T',17),('S','H',6),('W','K',10),('W','T',9)])
h=dict(A=30,X=27,B=16,C=17,L=33,W=9,K=19,T=0,S=17,H=22)
print('ASTAR16',json.dumps(trace(ag,'A',h,'T'),indent=2))
h['B']=6
print('ASTAR6',json.dumps(trace(ag,'A',h,'T'),indent=2))
print('ASTAR6_NO_OPEN_UPDATE',json.dumps(trace(ag,'A',h,'T',False),indent=2))

adj={'q':['s','t','w'],'r':['u','y'],'s':['v'],'t':['x','y'],'u':['y'],'v':['w'],'w':['s'],'x':['z'],'y':['q'],'z':['x']}
times={}; par={}; order=[]; timer=0
def dfs(v):
    global timer
    timer+=1; times[v]=[timer,None]; order.append(v)
    for w in adj[v]:
        if w not in times: par[w]=v; dfs(w)
    timer+=1; times[v][1]=timer
dfs('v')
for v in sorted(adj):
    if v not in times: dfs(v)
print('DFS4',order,times,par)
top={'m':['q','r','x'],'n':['o','q','u'],'o':['r','s','v'],'p':['o','s','z'],'q':['t'],'r':['u','y'],'s':['r'],'t':[],'u':['t'],'v':['w','x'],'w':['z'],'x':[],'y':['v'],'z':[]}
done=set(); finish=[]
def topo(v):
    done.add(v)
    for w in top[v]:
        if w not in done: topo(w)
    finish.append(v)
for v in sorted(top):
    if v not in done: topo(v)
ordering=finish[::-1]
assert all(ordering.index(v)<ordering.index(w) for v in top for w in top[v])
print('TOPO',ordering)

lines=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
def winner(b):
    for a,c,d in lines:
        if b[a]!='.' and b[a]==b[c]==b[d]: return 1 if b[a]=='X' else -1
    return None
terminal=Counter(); outcomes=Counter()
def enumerate_games(b='.........',turn='X',depth=0):
    w=winner(b)
    if w is not None or '.' not in b:
        terminal[depth]+=1; outcomes[(depth,0 if w is None else w)]+=1; return
    for i,c in enumerate(b):
        if c=='.': enumerate_games(b[:i]+turn+b[i+1:],'O' if turn=='X' else 'X',depth+1)
enumerate_games()
print('TERMINAL_HISTORIES',dict(sorted(terminal.items())),dict(sorted(outcomes.items())))
@lru_cache(None)
def minimax(b,turn):
    w=winner(b)
    if w is not None:return w
    if '.' not in b:return 0
    vals=[minimax(b[:i]+turn+b[i+1:],'O' if turn=='X' else 'X') for i,c in enumerate(b) if c=='.']
    return (max if turn=='X' else min)(vals)
print('FULL_OPENING_VALUES',[(i+1,minimax('.........'[:i]+'X'+'.........'[i+1:],'O')) for i in range(9)])
for seq in ([2,5,3,1,9,6,4,7,8],[2,3,5,8,1,9,6,4,7]):
    b='.........'
    for j,i in enumerate(seq):
        assert b[i-1]=='.' and winner(b) is None
        b=b[:i-1]+('X' if j%2==0 else 'O')+b[i:]
    print('GAME2',seq,b,'value',winner(b) or 0)
