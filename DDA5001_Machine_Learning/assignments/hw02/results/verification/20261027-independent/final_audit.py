from pathlib import Path
import json,hashlib,subprocess,os,datetime
OUT=Path(__file__).resolve().parent;BASE=OUT.parents[2]
env=os.environ.copy();env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1';env['MPLCONFIGDIR']=str(OUT/'mpl_cache')
argv=['env','-u','PYTHONPATH',str(OUT/'venv/bin/python'),str(OUT/'independent_checks.py')]
record={'executor':'/root/verifier','command':argv,'cwd':str(OUT),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with (OUT/'independent-final.stdout.txt').open('w') as so,(OUT/'independent-final.stderr.txt').open('w') as se:
 r=subprocess.run(argv,env=env,cwd=OUT,stdout=so,stderr=se)
record.update(exit_code=r.returncode,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());(OUT/'independent-final.run.json').write_text(json.dumps(record,indent=2)+'\n');assert r.returncode==0
assert (OUT/'clean-freeze.stdout.txt').read_text()==(BASE/'results/requirements-frozen.txt').read_text()
plots={}
for problem in (2,3):
 for p in (BASE/f'results/run-20261027/p{problem}').glob('*.png'):
  other=OUT/f'p{problem}-full'/p.name
  assert p.read_bytes()==other.read_bytes(),p
  plots[f'p{problem}/{p.name}']={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'byte_equal':True}
(OUT/'plot-comparison.json').write_text(json.dumps(plots,indent=2)+'\n')
print('Independent checks, exact installed freeze, and all 8 PNG artifacts pass.')
