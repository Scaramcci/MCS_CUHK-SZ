from pathlib import Path
import subprocess,socket,time,hashlib,json,signal,struct,concurrent.futures,traceback,platform,re,zipfile
R=Path(__file__).resolve().parent
S=R.parents[1]/'src'
B=R/'build'; DATA=R.parents[1]/'data/raw/independent-verifier-todo-only'; DATA.mkdir(parents=True,exist_ok=True); D=DATA/'received'; D.mkdir(exist_ok=True)
E=[]
def cmd(args,label,timeout=60):
 p=subprocess.run(list(map(str,args)),capture_output=True,timeout=timeout,cwd=R)
 (R/(label+'.out')).write_bytes(p.stdout);(R/(label+'.err')).write_bytes(p.stderr)
 E.append({'command':list(map(str,args)),'exit':p.returncode});assert p.returncode==0,(label,p.stderr)
def conn():return socket.create_connection(('127.0.0.1',8080),timeout=5)
def start(n):
 p=subprocess.Popen([str(B/n)],cwd=D,stdout=(R/(n+'.out')).open('wb'),stderr=(R/(n+'.err')).open('wb'))
 for _ in range(100):
  assert p.poll() is None
  try:s=conn();s.close();return p
  except ConnectionRefusedError:time.sleep(.02)
 raise AssertionError('not ready')
def stop(p):p.send_signal(signal.SIGINT);p.wait(timeout=5)
def exact(s,n):
 v=b''
 while len(v)<n:
  c=s.recv(n-len(v));assert c;v+=c
 return v
def echo(i):
 v=(('Client '+str(i)+' text payload. ')*40).encode()
 with conn() as s:
  s.sendall(v);s.shutdown(socket.SHUT_WR);assert exact(s,len(v))==v;assert s.recv(1)==b''
def head(n):return n.encode().ljust(1024,b'\0')
def transfer(n,v,split=False):
 with conn() as s:
  h=head(n)
  if split:
   for i in range(0,1024,11):s.sendall(h[i:i+11])
  else:s.sendall(h)
  for i in range(0,len(v),317):s.sendall(v[i:i+317])
  s.shutdown(socket.SHUT_WR);assert s.recv(1)==b''
 assert (D/n).read_bytes()==v

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
status='FAIL';p=None
try:
 with zipfile.ZipFile(S.parent/'Assignment-2.zip') as z:
  manifest={}
  for n in z.namelist():
   original=z.read(n);current=(S/n).read_bytes()
   restored=current
   if n.endswith('.c'):
    blocks=list(re.finditer(rb'/\* BEGIN TODO IMPLEMENTATION \*/.*?/\* END TODO IMPLEMENTATION \*/',current,re.S))
    assert len(blocks)==original.count(b'/* TODO:'),(n,len(blocks))
    for m in reversed(blocks):
     prefix=restored[:m.start()]
     # Every addition must directly follow a TODO comment, with one newline only.
     assert re.search(rb'/\* TODO:.*?\*/(?:\r\n|\n)$',prefix,re.S),(n,'not after TODO')
     end=len(prefix)-2 if prefix.endswith(b'\r\n') else len(prefix)-1
     restored=prefix[:end]+restored[m.end():]
   assert restored==original,(n,'outside TODO differs')
   manifest[n]={'original_sha256':hashlib.sha256(original).hexdigest(),'current_sha256':hashlib.sha256(current).hexdigest(),'outside_todo_identical':True}
  (R/'manifest.json').write_text(json.dumps(manifest,indent=2))
 E.append({'check':'independent removal of additions after TODO restores all original ZIP bytes','status':'PASS'})
 cmd(['cmake','-S',S,'-B',B,'-DCMAKE_C_FLAGS=-Wall -Wextra -Wpedantic -Werror'],'configure')
 cmd(['cmake','--build',B],'build')
 p=start('socket_server')
 cmd([B/'socket_client'],'client')
 with concurrent.futures.ThreadPoolExecutor(max_workers=30) as t:list(t.map(echo,range(30)))
 with conn() as s:s.setsockopt(socket.SOL_SOCKET,socket.SO_LINGER,struct.pack('ii',1,0));s.sendall(b'RST test')
 echo(5);assert p.poll() is None
 E.append({'check':'30 concurrent text echo and reset recovery','status':'PASS'})
 # A second server must report bind failure.
 q=subprocess.run([str(B/'socket_server')],cwd=D,capture_output=True,timeout=5)
 assert q.returncode!=0 and b'bind' in q.stderr
 E.append({'check':'duplicate listener reports bind failure','status':'PASS','exit':q.returncode})
 stop(p);p=None
 p=start('file_server')
 big=DATA/'64MiB.bin';block=bytes(range(256))*4096
 with big.open('wb') as f:
  for _ in range(64):f.write(block)
 cmd([B/'file_client',big],'64MiB',timeout=60)
 assert big.stat().st_size==(D/big.name).stat().st_size and digest(big)==digest(D/big.name)
 E.append({'check':'64MiB file','status':'PASS','size':big.stat().st_size,'source_sha256':digest(big),'received_sha256':digest(D/big.name)})
 with conn() as slow:
  slow.sendall(b'partial')
  transfer('empty',b'');transfer('fragmented',bytes(range(256))*100,True)
 with conn() as s:s.sendall(head('joined')+b'abc\x00xyz');s.shutdown(socket.SHUT_WR);assert s.recv(1)==b''
 assert (D/'joined').read_bytes()==b'abc\x00xyz'
 with conn() as s:s.sendall(head('../invalid'));s.shutdown(socket.SHUT_WR);assert s.recv(1)==b''
 with conn() as s:s.setsockopt(socket.SOL_SOCKET,socket.SO_LINGER,struct.pack('ii',1,0));s.sendall(head('reset')+b'partial')
 # A directory cannot be opened as a destination file.
 (D/'directory').mkdir(exist_ok=True)
 with conn() as s:s.sendall(head('directory'));s.shutdown(socket.SHUT_WR);assert s.recv(1)==b''
 with concurrent.futures.ThreadPoolExecutor(max_workers=30) as t:list(t.map(lambda i:transfer('parallel'+str(i),bytes([i])*10000),range(30)))
 assert p.poll() is None
 E.append({'check':'empty, fragmented/coalesced header, 30 concurrent binary files, incomplete header, invalid path, RST, fopen error recovery','status':'PASS'})
 stop(p);p=None
 status='PASS'
except BaseException:
 (R/'failure.txt').write_text(traceback.format_exc());raise
finally:
 if p and p.poll() is None:stop(p)
 (R/'run.json').write_text(json.dumps({'status':status,'executor':'independent Verifier /root/verify_hw02','platform':platform.platform(),'timestamp_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'command':'python3 results/independent-verifier-todo-only/verify.py','events':E,'sha256':{x.name:digest(x) for x in S.iterdir() if x.is_file()}},indent=2))
 print(status, R)
