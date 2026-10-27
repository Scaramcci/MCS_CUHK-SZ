"""Record real subprocess runs without overwriting previous evidence."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

base = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser()
p.add_argument('--record', required=True, type=Path)
p.add_argument('--cwd', type=Path, default=base/'src')
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
command = a.command[1:] if a.command[:1] == ['--'] else a.command
if not command:
    p.error('a command is required after --')
a.record.mkdir(parents=True, exist_ok=False)
source_paths = sorted((base/'src').rglob('*.py')) + [base/'src'/'requirements.txt']
source_paths += [base/'DDA5001_HW2.pdf', base/'code_source(1).zip']
metadata = {'command':command, 'cwd':str(a.cwd.resolve()),
            'started_utc':datetime.now(timezone.utc).isoformat(),
            'recorded_by':'coordinating Codex agent', 'platform':platform.platform(),
            'hardware':platform.machine(), 'logical_cpus':os.cpu_count(),
            'source_sha256':{str(f.relative_to(base)):hashlib.sha256(f.read_bytes()).hexdigest() for f in source_paths},
            'numerical_threads':'framework threadpool_limits(1) for full experiments',
            'seed':666}
(a.record/'run.json').write_text(json.dumps(metadata,indent=2)+'\n')
start=time.perf_counter()
with (a.record/'stdout.txt').open('w') as out, (a.record/'stderr.txt').open('w') as err:
    process=subprocess.run(command,cwd=a.cwd,stdout=out,stderr=err)
metadata.update(exit_code=process.returncode, elapsed_seconds=time.perf_counter()-start,
                finished_utc=datetime.now(timezone.utc).isoformat())
(a.record/'run.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps({'record':str(a.record),'exit_code':process.returncode,'elapsed_seconds':metadata['elapsed_seconds']}))
sys.exit(process.returncode)
