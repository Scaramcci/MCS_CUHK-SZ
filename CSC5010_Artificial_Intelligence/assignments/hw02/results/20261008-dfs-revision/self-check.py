from collections import defaultdict
adj=defaultdict(list)
for a,b in [('S','A'),('S','D'),('A','B'),('A','D'),('B','C'),('B','E'),('D','E'),('E','F'),('F','G')]:
 adj[a].append(b);adj[b].append(a)
t=0;times={};order=[];branches=[]
def visit(v):
 global t
 t+=1;times[v]=[t,None];order.append(v);children=0
 for w in sorted(adj[v]):
  if w not in times:
   if children:branches.append(v)
   children+=1;visit(w)
 t+=1;times[v][1]=t
visit('S');print('DFS2 order:',order);print('DFS2 timestamps:',times);print('DFS2 branch return nodes:',branches)
stack=[33,23,13,14,15,25,35,45,55,65,64,63,53,52,42,41,31,21,11,12,22,32];seen=set(stack);events=[];branchpoints=[];returned=False
while stack[-1]!=54:
 v=stack[-1];r,c=divmod(v,10)
 choices=sorted(10*rr+cc for rr,cc in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)] if 1<=rr<=6 and 1<=cc<=6 and 10*rr+cc not in seen)
 if choices:
  if returned:branchpoints.append(v)
  w=choices[0];events.append(('visit',v,w));stack.append(w);seen.add(w);returned=False
 else:
  stack.pop();events.append(('return',v,stack[-1]));returned=True
print('DFS3 continuation:',events);print('DFS3 branch return nodes:',branchpoints);print('DFS3 final path:',stack)
assert branchpoints==[41,42,44]
