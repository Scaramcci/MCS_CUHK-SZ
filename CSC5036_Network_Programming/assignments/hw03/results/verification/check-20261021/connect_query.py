"""Independent concurrent joins/main input test, using isolated compiled copy."""
import hashlib,json,socket,subprocess,threading,time
from pathlib import Path
B=Path(__file__).resolve().parent;W=B/'local_artifacts/work';R=B.parents[2]
logs=[];files=[];procs=[];commands=[];errors=[];ports=[];held=[]
for _ in range(5):
 s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.bind(('127.0.0.1',0));ports.append(s.getsockname()[1]);held.append(s)
for s in held:s.close()
def text(i):return logs[i].read_text()
def wait(pred,msg):
 end=time.monotonic()+6
 while time.monotonic()<end:
  if pred():return
  time.sleep(.01)
 raise AssertionError(msg)
def start(i):
 args=['stdbuf','-oL','./p2p_server',str(ports[i]),'8',f'dir{i+1}']
 if i:args+=['127.0.0.1',str(ports[0])]
 commands.append(args)
 procs[i]=subprocess.Popen(args,cwd=W,stdin=subprocess.PIPE,stdout=files[i],stderr=subprocess.STDOUT,text=True)
 wait(lambda:'[FILE] Enter' in text(i),f'node{i} ready')
def query(i,s):procs[i].stdin.write(s+'\n');procs[i].stdin.flush()
for i in range(5):
 p=B/f'concurrent-join-node{i}.txt';logs.append(p);files.append(p.open('w'));procs.append(None)
def worker(i):
 try:start(i)
 except BaseException as e:errors.append(repr(e))
status='failed'
try:
 start(0)
 threads=[threading.Thread(target=worker,args=(i,)) for i in range(1,5)]
 for t in threads:t.start()
 for i in range(50):query(0,f'joining_probe_{i}');time.sleep(.002)
 for t in threads:t.join()
 assert not errors,errors
 wait(lambda:text(0).count('New neighbor connected!')==4,'four concurrent joins registered')
 for i in range(1,5):query(i,'file1')
 for i in range(1,5):wait(lambda i=i:f'File file1 found on address 127.0.0.1, with port {ports[0]}' in text(i),f'new leaf{i} reverse connection')
 query(0,'file7');wait(lambda:f'File file7 found on address 127.0.0.1, with port {ports[4]}' in text(0),'root floods to final joined peer')
 assert all(p.poll() is None for p in procs)
 status='passed'
finally:
 for p in procs:
  if p is not None and p.poll() is None:p.terminate()
 for p in procs:
  if p is not None:p.wait(timeout=3)
 for f in files:f.close()
 (B/'concurrent-join-summary.json').write_text(json.dumps({'status':status,'checks':['four leaves join concurrently while root originates 50 queries','all joined leaves find root file; root finds last joined leaf file'],'command':'python3 results/verification/check-20261021/connect_query.py','cwd':str(W.relative_to(R)),'commands':commands,'returncodes':[p.returncode if p else None for p in procs],'shutdown':'SIGTERM after assertions','time':time.strftime('%Y-%m-%dT%H:%M:%S%z')},indent=2))
 print(status)
