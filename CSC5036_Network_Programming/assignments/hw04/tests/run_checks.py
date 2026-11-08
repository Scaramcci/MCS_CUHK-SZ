"""Run checks sequentially and preserve evidence. Invoke from any directory."""
import datetime
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
run = ROOT/'results'/('selftest-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
run.mkdir(parents=True)
record = {'environment': {'python':sys.version, 'platform':platform.platform(), 'machine':platform.machine(), 'cpu_count':os.cpu_count()}, 'scope':'supplementary local checks, not required AWS environment', 'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in list((ROOT/'src/Assignment-4').glob('*.py'))+list((ROOT/'tests').glob('*.py'))}, 'runs':[]}
for label, command, cwd in [('scope',[sys.executable,str(ROOT/'tests/check_scope.py')],ROOT), ('teacher',[sys.executable,'test_dht.py'],ROOT/'src/Assignment-4'), ('assertions',[sys.executable,str(ROOT/'tests/check_behavior.py')],ROOT)]:
    with (run/(label+'.txt')).open('w') as out:
        try:
            completed = subprocess.run(command,cwd=cwd,stdout=out,stderr=subprocess.STDOUT,timeout=240)
            code = completed.returncode
        except subprocess.TimeoutExpired:
            code = 'timeout'
    output = (run/(label+'.txt')).read_text()
    semantic_ok = code == 0
    if label == 'teacher':
        semantic_ok = semantic_ok and all(marker in output for marker in (
            'All retrieval tests: Success', 'Get non-existent key: Success',
            'Duplicate key test (overwrite): Success',
            'All keys accessible after transfer: Success',
            '=== Failure recovery success ===')) and not any(
                marker in output for marker in ('Failed', 'Test failed', 'Server error', 'Traceback'))
    record['runs'].append({'label':label,'command':command,'cwd':str(cwd),'exit':code,'semantic_ok':semantic_ok})
    (run/'run.json').write_text(json.dumps(record,indent=2)+'\n')
    print(label, code, flush=True)
    if not semantic_ok: break
print(run)
sys.exit(0 if all(r['semantic_ok'] for r in record['runs']) else 1)
