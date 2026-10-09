from collections import defaultdict
# Independently transcribed actual undirected graph, slide35 / requirements p3.
edges=[('S','A'),('S','D'),('A','B'),('A','D'),('B','C'),('B','E'),('D','E'),('E','F'),('F','G')]
adj=defaultdict(list)
for a,b in edges:adj[a].append(b);adj[b].append(a)
for a in adj:adj[a].sort()
seen=set();time=0;times={};tree=[];bt=[]
def dfs(a):
 global time
 seen.add(a);time+=1;times[a]=[time];children=0
 for b in adj[a]:
  if b not in seen:
   if children:bt.append(a)
   tree.append((a,b));children+=1;dfs(b)
 time+=1;times[a].append(time)
dfs('S')
print('DFS2 sorted adjacency',dict(sorted(adj.items())))
print('DFS2 times',times,'tree',tree,'backtrack branch points',bt)
assert times=={'S':[1,16],'A':[2,15],'B':[3,14],'C':[4,5],'E':[6,13],'D':[7,8],'F':[9,12],'G':[10,11]}
assert bt==['B','E']
assert len(times)==8 and sum(1 for a,b in tree if b=='D')==1
# Slide34 active stack: supplied route preserved without pretending it originally used sorted labels.
stack=[33,23,13,14,15,25,35,45,55,65,64,63,53,52,42,41,31,21,11,12,22,32]
initial=stack[:];seen=set(stack)
def neighbors(n):
 r,c=divmod(n,10)
 return sorted(10*rr+cc for rr,cc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)] if 1<=rr<=6 and 1<=cc<=6)
assert all(b in neighbors(a) for a,b in zip(stack,stack[1:]))
returns=[];new=[];backtracks=[];events=[];returning=False
while stack[-1]!=54:
 a=stack[-1];choices=[b for b in neighbors(a) if b not in seen]
 if choices:
  b=choices[0]
  if returning:backtracks.append(a);events.append(('bf',a));returning=False
  seen.add(b);stack.append(b);new.append((a,b));events.append(('visit',a,b))
 else:
  n=stack.pop();returns.append(n);events.append(('return',n,stack[-1]));returning=True
print('DFS3 initial stack',initial)
print('DFS3 chronological continuation',events)
print('DFS3 new edges',new,'backtrack nodes',backtracks,'final stack',stack)
assert backtracks==[41,42,44]
assert new==[(41,51),(51,61),(61,62),(42,43),(43,44),(44,34),(34,24),(44,54)]
assert stack==[33,23,13,14,15,25,35,45,55,65,64,63,53,52,42,43,44,54]
print('All independent assertions passed.')
