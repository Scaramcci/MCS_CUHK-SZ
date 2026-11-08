import ast, hashlib, importlib.util, json, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
archive=ROOT/'results/candidate/20261104T074144997572Z/226040255_hw4.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
result={'archive':str(archive.relative_to(ROOT)),'archive_sha256':sha(archive.read_bytes()),'members':{}}
with zipfile.ZipFile(archive) as z, zipfile.ZipFile(ROOT/'requirements/Assignment-4.zip') as starter:
 assert z.namelist()==['Assignment-4/chord_node.py','Assignment-4/test_dht.py']
 assert z.testzip() is None
 for name in z.namelist():
  content=z.read(name)
  assert content==(ROOT/'src'/name).read_bytes()
  result['members'][name]={'sha256':sha(content),'size':len(content)}
  compile(content,name,'exec')
 assert z.read('Assignment-4/test_dht.py')==starter.read('Assignment-4/test_dht.py')
 old=starter.read('Assignment-4/chord_node.py');new=z.read('Assignment-4/chord_node.py')
 def methods(data):return {n.name:n for n in ast.parse(data).body[-1].body if isinstance(n,ast.FunctionDef)}
 before,after=methods(old),methods(new)
 for name in ['__init__','remote_call','run_server','handle_client','stop']:
  a,b=before[name],after[name]
  assert old.splitlines(True)[a.lineno-1:a.end_lineno]==new.splitlines(True)[b.lineno-1:b.end_lineno]
 result['static_package_checks']='PASS'
 namespace={};exec(compile(new,'candidate/chord_node.py','exec'),namespace)
 Node=namespace['Node']
 node=Node.__new__(Node)
 node.node_id=15;node.host='127.0.0.1';node.port=5003;node.max_id=32
 node.predecessor=(8,'127.0.0.1',5002)
 key=next(f'review-{i}' for i in range(1000) if node.hash_key(f'review-{i}')==10)
 node.data={key:'owned-by-15'}
 sent=[]
 node.remote_call=lambda address,command,params:sent.append((address,command,params)) or True
 node.transfer_keys(node.predecessor)
 result['repeat_transfer']={'key':key,'key_hash':10,'current_owner':15,'existing_predecessor':8,'expected':'retain key on node 15','actual_data':node.data,'sent':sent,'failed':key not in node.data}
 assert not result['repeat_transfer']['failed']
 assert sent == []
 result['repeat_transfer']['status'] = 'PASS: current owner retains key; no store RPC' 
(OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
