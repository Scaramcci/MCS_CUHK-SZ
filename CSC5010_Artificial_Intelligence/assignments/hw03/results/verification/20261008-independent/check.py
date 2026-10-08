from collections import Counter
lines=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
counts=Counter();vals=Counter()
def visit(b,n):
 wins=[v for v in 'XO' if any(all(b[k]==v for k in l) for l in lines)]
 if wins or n==9:
  counts[n]+=1;vals[(n,wins[0] if wins else 'draw')]+=1;return
 for i,v in enumerate(b):
  if v=='.':visit(b[:i]+('X' if n%2==0 else 'O')+b[i+1:],n+1)
visit('.'*9,0)
print('terminal game-history counts',dict(sorted(counts.items())));print('values',dict(vals));print('total',sum(counts.values()))
# Independent legal destinations for red pieces; top-to-bottom y=0..9, x=1..9.
black={(2,0):'h',(3,0):'e',(4,0):'a',(5,0):'k',(6,0):'a',(7,0):'e',(8,0):'h',(9,0):'r',(1,2):'r',(2,2):'c',(8,2):'c',(1,3):'p',(3,3):'p',(5,3):'p',(7,3):'p',(9,4):'p'}
red={(1,9):'r',(2,9):'h',(3,9):'e',(4,9):'a',(5,9):'k',(6,9):'a',(7,9):'e',(8,9):'h',(9,9):'r',(4,7):'c',(8,7):'c',(1,5):'p',(3,6):'p',(5,6):'p',(7,6):'p',(9,6):'p'}
occ=red|black
total=0
for (x,y),p in red.items():
 dest=[]
 if p in 'rc':
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   screen=False
   for k in range(1,10):
    t=(x+k*dx,y+k*dy)
    if not 1<=t[0]<=9 or not 0<=t[1]<=9:break
    if p=='r':
     if t not in red:dest.append(t)
     if t in occ:break
    elif not screen:
     if t in occ:screen=True
     else:dest.append(t)
    elif t in occ:
     if t in black:dest.append(t)
     break
 elif p=='h':
  for dx,dy in [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]:
   leg=(x+(dx//2 if abs(dx)==2 else 0),y+(dy//2 if abs(dy)==2 else 0));t=(x+dx,y+dy)
   if leg not in occ and 1<=t[0]<=9 and 0<=t[1]<=9 and t not in red:dest.append(t)
 elif p=='e':
  for dx,dy in [(2,2),(2,-2),(-2,2),(-2,-2)]:
   t=(x+dx,y+dy)
   if (x+dx//2,y+dy//2) not in occ and 1<=t[0]<=9 and 5<=t[1]<=9 and t not in red:dest.append(t)
 elif p=='a':
  dest=[(x+dx,y+dy) for dx,dy in [(1,1),(1,-1),(-1,1),(-1,-1)] if 4<=x+dx<=6 and 7<=y+dy<=9 and (x+dx,y+dy) not in red]
 elif p=='k':
  dest=[(x+dx,y+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if 4<=x+dx<=6 and 7<=y+dy<=9 and (x+dx,y+dy) not in red]
 elif p=='p':dest=[(x,y-1)] if (x,y-1) not in red else []
 print(p,(x,y),len(dest),dest);total+=len(dest)
print('branching',total,'depth3 heuristic evaluations',total**3)
terminals=['XOX.OXO.X','X.XOOXO.X','XXOOOXXOX','XOOOOXXXX','XOOX..X..','X.OOX.XOX','O.XXXXOO.','OXXXXOOOX','OXXXXOOXO','XOOXX.X.O','OOX.X.X..']
print('Game3 depicted terminal utilities (top-to-bottom branches):')
for b in terminals:
 win=[v for v in 'XO' if any(all(b[k]==v for k in l) for l in lines)]
 value=1 if win==['X'] else -1 if win==['O'] else 0
 print('/'.join(b[i:i+3] for i in [0,3,6]),value)
# Exact graph backup, forced one-child chains contracted.
corner_center=min(1,min(1,min(0,1)))
shared=min(min(1,min(0,1)),1)
corner_corner=max(min(1,1),shared)
corner_side=min(1,1)
corner=min(corner_center,corner_corner,corner_side)
center=min(shared,min(1,1))
print('Game3 backups',{'corner/Ocenter':corner_center,'shared':shared,'corner/Ocorner':corner_corner,'corner/Oside':corner_side,'corner':corner,'center':center,'root':max(corner,center)})
from functools import lru_cache
from itertools import combinations
@lru_cache(None)
def minimax(b,t):
 win=[v for v in 'XO' if any(all(b[k]==v for k in l) for l in lines)]
 if win:return 1 if win[0]=='X' else -1
 if '.' not in b:return 0
 v=[minimax(b[:k]+t+b[k+1:],'O' if t=='X' else 'X') for k,c in enumerate(b) if c=='.']
 return (max if t=='X' else min)(v)
print('Full minimax openings',[minimax('.'*k+'X'+'.'*(8-k),'O') for k in range(9)])
for moves in [[2,5,3,1,9,6,4,7,8],[2,3,5,8,1,9,6,4,7]]:
 b='.'*9
 for n,p in enumerate(moves):
  assert b[p-1]=='.'
  assert all(not all(b[k]==v for k in l) for v in 'XO' for l in lines)
  b=b[:p-1]+('X' if n%2==0 else 'O')+b[p:]
 assert all(not all(b[k]==v for k in l) for v in 'XO' for l in lines)
 print('Game2 legal draw',moves,b)
drawboards=0
for xs in combinations(range(9),5):
 b=''.join('X' if k in xs else 'O' for k in range(9))
 if all(not all(b[k]==v for k in l) for v in 'XO' for l in lines):drawboards+=1
print('full draw boards',drawboards)
