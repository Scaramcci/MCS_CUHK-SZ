import datetime, hashlib, json, os, platform, subprocess, sys
from pathlib import Path
root=Path.cwd(); out=root/'results/verification/independent-20261029'; py=out/'.venv/bin/python'
env=os.environ.copy()
env.pop("PYTHONPATH",None)
env.pop("PYTHONHOME",None)
env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',MPLCONFIGDIR=str(out/'.cache/matplotlib'),XDG_CACHE_HOME=str(out/'.cache'),PYTHONDONTWRITEBYTECODE='1')
commands=[('freeze',[str(py),'-m','pip','freeze']),('p1',[str(py),'src/p1/p1.py','--output-dir',str(out/'p1')]),('p2',[str(py),'src/p2/p2.py','--output-dir',str(out/'p2')]),('p3',[str(py),'src/p3/p3.py','--output-dir',str(out/'p3')]),('author-tests',[str(py),'-m','unittest','discover','-s','tests','-v']),('independent-checks',[str(py),str(out/'verify.py')])]
records=[]
for name,argv in commands:
    record={'name':name,'argv':argv,'cwd':str(root),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    with (out/f'{name}.stdout.txt').open('w') as stdout,(out/f'{name}.stderr.txt').open('w') as stderr:
        proc=subprocess.run(argv,env=env,stdout=stdout,stderr=stderr)
    record.update(exit_code=proc.returncode,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    records.append(record); (out/'commands.json').write_text(json.dumps(records,indent=2)); print(name,proc.returncode,flush=True)
print('COMPLETED',flush=True)
