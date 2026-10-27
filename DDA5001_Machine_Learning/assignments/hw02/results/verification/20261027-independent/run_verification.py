from pathlib import Path
import os,sys,shutil,json,hashlib,subprocess,time,datetime,zipfile
BASE=Path('/home/scarramcci/Project/MCS_CUHK-SZ/DDA5001_Machine_Learning/assignments/hw02')
OUT=BASE/'results/verification/20261027-independent'
ENV=os.environ.copy(); ENV.pop('PYTHONPATH',None); ENV['PYTHONDONTWRITEBYTECODE']='1'; ENV['MPLCONFIGDIR']=str(OUT/'mpl_cache')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(name,argv,cwd=OUT):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
 with (OUT/(name+'.stdout.txt')).open('w') as so,(OUT/(name+'.stderr.txt')).open('w') as se:
  result=subprocess.run(['env','-u','PYTHONPATH',*map(str,argv)],cwd=cwd,env=ENV,stdout=so,stderr=se)
 record={'executor':'independent Verifier /root/verifier','command':['env','-u','PYTHONPATH',*map(str,argv)],'cwd':str(cwd),'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'exit_code':result.returncode}
 (OUT/(name+'.run.json')).write_text(json.dumps(record,indent=2)+'\n');print(name,result.returncode,flush=True)
 if result.returncode: raise RuntimeError(name)
source_hashes={str(p.relative_to(BASE)):sha(p) for p in (BASE/'src').rglob('*') if p.is_file() and p.suffix in ('.py','.txt')}
source_hashes.update({p.name:sha(p) for p in [BASE/'DDA5001_HW2.pdf',BASE/'code_source(1).zip',BASE/'data/dry_bean.csv']})
(OUT/'input-hashes.json').write_text(json.dumps(source_hashes,indent=2)+'\n')
shutil.copytree(BASE/'src',OUT/'src',ignore=shutil.ignore_patterns('__pycache__','mpl_cache'),dirs_exist_ok=False)
run('create-clean-env',['/home/scarramcci/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3','-m','venv',OUT/'venv'])
PY=OUT/'venv/bin/python'
run('offline-install',[PY,'-m','pip','install','--no-index','--find-links',BASE/'local_artifacts/wheels','-r',BASE/'results/requirements-frozen.txt'])
run('clean-freeze',[PY,'-m','pip','freeze'])
for problem in (2,3):
 run(f'p{problem}-tests',[PY,'-m','unittest','discover','-s',f'p{problem}','-v'],OUT/'src')
 run(f'p{problem}-verify',[PY,OUT/f'src/p{problem}/verify.py','--output',OUT/f'p{problem}-checks.json'])
run('p2-full',[PY,OUT/'src/p2/run.py','--data-dir',BASE/'data','--output-dir',OUT/'p2-full'])
run('p3-full',[PY,OUT/'src/p3/run.py','--output-dir',OUT/'p3-full'])
with zipfile.ZipFile(BASE/'code_source(1).zip') as z:
 originals={}
 for n in z.namelist():
  if not n.startswith('code_source/') or not n.endswith(('.py','.txt')):continue
  rel=n.split('code_source/',1)[-1] if 'code_source/' in n else n
  if rel.startswith('code_source/'): rel=rel[len('code_source/'):]
  candidate=BASE/'src'/rel
  if not candidate.exists():
   parts=n.split('/'); rel='/'.join(parts[1:]); candidate=BASE/'src'/rel
  originals[n]={'src_path':str(candidate.relative_to(BASE)),'original_sha256':hashlib.sha256(z.read(n)).hexdigest(),'current_sha256':sha(candidate),'unchanged':z.read(n)==candidate.read_bytes()}
 (OUT/'original-comparison.json').write_text(json.dumps(originals,indent=2)+'\n')
assert all(sha(BASE/p)==h for p,h in source_hashes.items() if p.startswith('src/'))
print('all standard clean-room runs complete',flush=True)
