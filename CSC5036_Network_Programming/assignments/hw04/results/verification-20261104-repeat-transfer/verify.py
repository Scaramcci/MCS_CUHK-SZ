import ast, hashlib, json, platform, socket, sys, time, zipfile
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'src/Assignment-4'))
from chord_node import Node
source=(ROOT/'src/Assignment-4/chord_node.py').read_bytes()
record={'executor':'/root/verifier','source_sha256':hashlib.sha256(source).hexdigest(),'python':sys.version,'platform':platform.platform(),'checks':[]}
def passed(text):
 record['checks'].append(text);print('PASS',text,flush=True)
 (OUT/'summary.json').write_text(json.dumps(record,indent=2))
with zipfile.ZipFile(ROOT/'requirements/Assignment-4.zip') as z:
 old=z.read('Assignment-4/chord_node.py')
 assert z.read('Assignment-4/test_dht.py')==(ROOT/'src/Assignment-4/test_dht.py').read_bytes()
 oldtree=ast.parse(old);newtree=ast.parse(source)
 def methods(t):return {n.name:n for n in t.body[-1].body if isinstance(n,ast.FunctionDef)}
 before,after=methods(oldtree),methods(newtree)
 for name in ['__init__','remote_call','run_server','handle_client','stop']:
  a,b=before[name],after[name]
  assert old.splitlines(keepends=True)[a.lineno-1:a.end_lineno]==source.splitlines(keepends=True)[b.lineno-1:b.end_lineno]
passed('original network/init/stop methods and teacher test byte-identical')
probe=Node.__new__(Node);probe.max_id=32
for a in range(32):
 for b in range(32):
  for k in range(32):
   for closed in [True,False]:
    if a==b: expected=closed or k!=a
    elif a<b: expected=a<k<b or (closed and k==b)
    else: expected=k>a or k<b or (closed and k==b)
    assert probe.in_interval(k,a,b,closed)==expected
passed('65536 interval endpoint/wraparound assertions')
created=[]
def address(n):return(n.node_id,n.host,n.port)
def spawn(i):
 # Pick a free ephemeral port without altering any Node attributes.
 with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
 n=Node(i,'127.0.0.1',port);created.append(n)
 for _ in range(100):
  try:
   with socket.create_connection(('127.0.0.1',port),timeout=.1):pass
   break
  except OSError:time.sleep(.01)
 else:raise AssertionError('server not ready')
 return n

def settle(ns):
 for _ in range(16):
  for n in ns:n.check_predecessor();n.stabilize();n.fix_fingers()

def owner(ns,k):
 ordered=sorted(ns,key=lambda n:n.node_id)
 return next((n for n in ordered if n.node_id>=k),ordered[0])
def verify(ns,values):
 ordered=sorted(ns,key=lambda n:n.node_id)
 for idx,n in enumerate(ordered):
  assert n.successor==address(ordered[(idx+1)%len(ns)])
  if len(ns)>1: assert n.predecessor==address(ordered[idx-1])
  for k in range(32):assert tuple(n.find_successor(k))==address(owner(ns,k)),(n.node_id,k)
  for i in range(1,6): assert tuple(n.finger[i])==address(owner(ns,(n.node_id+2**(i-1))%32))
 for key,value in values.items():
  h=int(hashlib.sha1(key.encode()).hexdigest(),16)%32
  own=owner(ns,h)
  assert [n.node_id for n in ns if key in n.data]==[own.node_id],(key,h,[(n.node_id,key in n.data)for n in ns])
  for n in ns:assert n.get(key)==value
try:
 ns=[spawn(31)];ns[0].create();settle(ns)
 # Construct two keys for every possible key hash, independent of implementation hash.
 values={};counts={i:0 for i in range(32)}
 for i in range(2000):
  key=f'verifier-{i}';h=int(hashlib.sha1(key.encode()).hexdigest(),16)%32
  if counts[h]<2:values[key]=f'v{i}';counts[h]+=1
  if all(v==2 for v in counts.values()):break
 assert len(values)==64
 for k,v in values.items():assert ns[0].put(k,v)
 verify(ns,values);passed('singleton stores keys covering all 32 hashes')
 for i in [0,16,7,26]:
  n=spawn(i);n.join(address(ns[-1]));ns.append(n);settle(ns);verify(ns,values)
  passed(f'join {i}: complete routing, fingers, predecessor/successor, exact ownership and all-node retrieval')
 for n in ns:assert n.get('definitely-missing') is None
 key=next(iter(values));assert ns[-1].put(key,False);values[key]=False
 verify(ns,values);passed('missing key and falsy overwrite')
 # Exercise public RPC rather than calling transfer_keys directly.
 before_data = {n.node_id: dict(n.data) for n in ns}
 for receiver in ns:
  pred = receiver.predecessor
  caller = next(n for n in ns if n is not receiver)
  for repetition in range(3):
   assert caller.remote_call(address(receiver), 'transfer_keys', {
       'node_id':pred[0], 'host':pred[1], 'port':pred[2]}) is True
 assert {n.node_id: dict(n.data) for n in ns} == before_data
 verify(ns,values)
 passed('15 real TCP repeated transfer RPCs preserve all key ownership and retrieval')
 # Two adjacent failures, followed by steady-state recovery; unreplicated keys intentionally excluded.
 dead=[next(n for n in ns if n.node_id==7),next(n for n in ns if n.node_id==16)]
 for n in dead:
  values={k:v for k,v in values.items()if k not in n.data};n.stop();n.server_thread.join(2);ns.remove(n)
 settle(ns);verify(ns,values);passed('two adjacent failures: surviving keys, exhaustive routing and fingers')
 # Reduce to two nodes, then one; ensures no stale failed successor remains.
 while len(ns)>1:
  n=ns.pop();values={k:v for k,v in values.items()if k not in n.data};n.stop();n.server_thread.join(2)
  settle(ns);verify(ns,values)
 passed('recovery down to singleton')
 record['status']='PASS supplementary local verification only'
finally:
 for n in created:
  if not n.stopped:n.stop()
 for n in created:n.server_thread.join(2)
 record['source_unchanged']=hashlib.sha256((ROOT/'src/Assignment-4/chord_node.py').read_bytes()).hexdigest()==record['source_sha256']
 (OUT/'summary.json').write_text(json.dumps(record,indent=2)+'\n')
