#!/usr/bin/env python3
import ctypes as C
import hashlib,json,platform,shutil,socket,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
SRC=ROOT/'src/Assignment-3'
WORK=BASE/'local_artifacts/work'
WORK.mkdir(parents=True,exist_ok=True)
for p in SRC.iterdir():
 if p.suffix in ('.c','.h') or p.name=='Makefile': shutil.copy2(p,WORK/p.name)
for i in range(1,6): shutil.copytree(SRC/f'dir{i}',WORK/f'dir{i}',dirs_exist_ok=True)
commands=[];checks=[];networks=[]
def run(args,cwd=WORK):
 commands.append({'argv':args,'cwd':str(cwd.relative_to(ROOT))})
 p=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
 (BASE/('build-'+str(len(commands))+'.txt')).write_text(p.stdout+p.stderr)
 assert p.returncode==0,(args,p.returncode)
 return p
class Packet(C.Structure):
 _fields_=[('ID',C.c_int),('descriptor',C.c_ubyte),('message',C.c_char*64),('hostname',C.c_char*64),('TTL',C.c_ubyte),('port',C.c_int)]
def wait(pred,msg):
 end=time.monotonic()+8
 while time.monotonic()<end:
  if pred(): return
  time.sleep(.025)
 raise AssertionError(msg)
class Net:
 def __init__(self,name,ttls,edges):
  self.name=name;self.procs=[];self.files=[];self.paths=[];self.ports=[]
  holds=[]
  for _ in ttls:
   s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.bind(('127.0.0.1',0));self.ports.append(s.getsockname()[1]);holds.append(s)
  for s in holds:s.close()
  networks.append(self)
  for i,t in enumerate(ttls): self.start(i,t,edges[i])
 def start(self,i,ttl,edges):
  path=BASE/f'{self.name}-node{i}.txt';f=path.open('w');self.paths.append(path);self.files.append(f)
  args=['stdbuf','-oL','./p2p_server',str(self.ports[i]),str(ttl),f'dir{i+1}']
  for j in edges: args+=['127.0.0.1',str(self.ports[j])]
  commands.append({'argv':args,'cwd':str(WORK.relative_to(ROOT))})
  self.procs.append(subprocess.Popen(args,cwd=WORK,stdin=subprocess.PIPE,stdout=f,stderr=subprocess.STDOUT,text=True))
  wait(lambda:'[FILE] Enter the File Name' in self.text(i),f'{self.name} node{i} ready')
  for j in edges:wait(lambda j=j:f'From address: 127.0.0.1:{self.ports[i]}' in self.text(j),f'connect {i}->{j}')
 def text(self,i):return self.paths[i].read_text()
 def query(self,i,name): self.procs[i].stdin.write(name+'\n');self.procs[i].stdin.flush()
 def close(self):
  for p in self.procs:
   if p.poll() is None:p.terminate()
  for p in self.procs:p.wait(timeout=3)
  for f in self.files:f.close()
 def inject(self,i,ident,ttl=1,kind=1,port=48001,message='absent_probe'):
  pkt=Packet();pkt.ID=ident;pkt.descriptor=kind;pkt.TTL=ttl;pkt.port=port;pkt.message=message.encode()
  with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:s.sendto(bytes(pkt),('127.0.0.1',self.ports[i]))
status='failed'
try:
 run(['make']);checks.append('fresh isolated original Makefile C17 build')
 n=Net('chain1',[1,2,2,2],[[],[0],[1],[2]])
 n.query(0,'file5');wait(lambda:'[TTL] Packet TTL expired' in n.text(1),'TTL1 at first hop');time.sleep(.2)
 assert 'QUERY packet' not in n.text(2) and 'QUERY packet' not in n.text(3) and 'RESPONSE packet' not in n.text(0)
 n.query(2,'file1');wait(lambda:f'File file1 found on address 127.0.0.1, with port {n.ports[0]}' in n.text(2),'reverse multihop holder')
 checks+=['four-node chain TTL1 halts and no response','two-hop reverse search direct response with correct holder port'];n.close()
 n=Net('chain3',[3,2,2,2],[[],[0],[1],[2]])
 n.query(0,'file5');wait(lambda:f'File file5 found on address 127.0.0.1, with port {n.ports[3]}' in n.text(0),'TTL3 response')
 assert 'Forwarding packet with TTL=2' in n.text(1) and 'Forwarding packet with TTL=1' in n.text(2)
 checks.append('TTL3 reaches third hop; TTL1 recipient searches before expiration');n.close()
 n=Net('loop-history',[64,2,2],[[],[0],[0,1]])
 n.query(0,'missing_loop');wait(lambda:all('[DUPLICATE ID]' in n.text(i) for i in (1,2)),'duplicate at both loop peers');time.sleep(.2)
 assert all(n.text(i).count('[TTL] Forwarding')==1 for i in (1,2))
 snap=[n.text(i) for i in range(3)];time.sleep(.25);assert snap==[n.text(i) for i in range(3)]
 checks.append('triangle each query processed once; quiescent without TTL expiry')
 # Independent known-ID packets exercise the 128-entry array and overflow history.
 for k in range(160):
  n.inject(0,700000+k)
  wait(lambda k=k:n.text(0).count('[TTL] Packet TTL expired')>=k+1,f'unique ID {k}')
 before=n.text(0).count('[TTL] Packet TTL expired')
 for ident in (700000,700159):n.inject(0,ident)
 wait(lambda:all(f'Duplicate packet with ID {ident}' in n.text(0) for ident in (700000,700159)),'first/last ID retained')
 assert n.text(0).count('[TTL] Packet TTL expired')==before
 checks.append('160 unique received IDs; earliest and overflow ID duplicates still discarded')
 before=n.text(0).count('New neighbor connected!')
 for k in range(20):n.inject(0,800000+k,kind=0,port=48001,message='')
 wait(lambda:n.text(0).count('CONNECT packet')>=22,'repeated CONNECT received')
 assert n.text(0).count('New neighbor connected!')==before+1
 checks.append('20 repeated CONNECT packets allocate only one neighbor');n.close()
 # Synthetic same-name files only in isolated local_artifacts work copy.
 (WORK/'dir2/shared_probe').write_text('synthetic verification fixture\n');(WORK/'dir3/shared_probe').write_text('synthetic verification fixture\n')
 n=Net('star-concurrent',[5]*5,[[],[0],[0],[0],[0]])
 n.query(0,'shared_probe');wait(lambda:all(f'File shared_probe found on address 127.0.0.1, with port {n.ports[i]}' in n.text(0) for i in (1,2)),'both independent holders respond')
 checks.append('one search accepts multiple direct responses from separate holders')
 targets=['file7','file4','file5','file1','file3']
 for round in range(12):
  before=[n.text(i).count(f'File {targets[i]} found on address') for i in range(5)]
  for i,target in enumerate(targets):n.query(i,target)
  for i,target in enumerate(targets):wait(lambda i=i,target=target:n.text(i).count(f'File {target} found on address')>before[i],f'star concurrent {round}/{i}')
 assert all(p.poll() is None for p in n.procs)
 checks.append('five-node star 60 simultaneous-origin searches with active receive threads');n.close()
 status='passed'
finally:
 for n in networks:n.close()
 summary={'status':status,'checks':checks,'time':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'platform':platform.platform(),'compiler':subprocess.check_output(['gcc','--version'],text=True).splitlines()[0], 'packet_size':C.sizeof(Packet),'commands':commands,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SRC.iterdir() if p.suffix in ('.c','.h') or p.name=='Makefile'},'process_returncodes':{n.name:[p.returncode for p in n.procs] for n in networks},'shutdown':'SIGTERM after assertions; expected returncode -15'}
 (BASE/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps({'status':status,'checks':checks},indent=2))
