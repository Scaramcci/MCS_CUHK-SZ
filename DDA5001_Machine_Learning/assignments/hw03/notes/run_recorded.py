"""Execute a command once in a fresh evidence directory; retain failed runs too."""
import datetime, hashlib, json, os, platform, subprocess, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
folder = root / sys.argv[1]
argv = sys.argv[2:]
folder.mkdir(parents=True, exist_ok=False)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
record = {'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'cwd':str(root),'argv':argv,'python':sys.version,'platform':platform.platform(),
          'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
          'source_sha256':{str(p.relative_to(root)):sha(p) for p in sorted((root/'src').glob('p*/*.py'))},
          'prediction_sha256':sha(root/'notes/pre-run-prediction.md'),
          'thread_environment':{k:os.environ.get(k) for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']}}
(folder/'run.json').write_text(json.dumps(record,indent=2)+'\n')
try:
    with (folder/'stdout.txt').open('w') as out, (folder/'stderr.txt').open('w') as err:
        result=subprocess.run(argv,cwd=root,stdout=out,stderr=err)
    record['exit_code']=result.returncode
except BaseException as exc:
    record['error']=repr(exc)
    record['exit_code']=-1
record['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(folder/'run.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'record':str(folder/'run.json'),'exit_code':record['exit_code']}))
sys.exit(record['exit_code'])
