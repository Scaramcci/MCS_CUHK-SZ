"""Run from the directory containing train.py in a fresh experiment workspace."""
import csv
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

def run(*args):
    cmd = [sys.executable, *args]
    print(datetime.now(timezone.utc).isoformat(), cmd, flush=True)
    status = subprocess.run(cmd).returncode
    print("exit", status, flush=True)
    if status:
        raise SystemExit(status)

def config(method, label, field, rate):
    text = Path('config/train_shakespeare_char.py').read_text()
    for key, value in [('optimizer_name', method), ('out_dir', f'runs/{method}-{label}'), (field, rate)]:
        text = re.sub(rf'^{key} = [^#\n]+', f'{key} = {value!r} ', text, flags=re.M)
    path = Path(f'config/{method}-{label}.py')
    path.write_text(text)
    return str(path)

run('check_solution.py')
run('train.py', 'config/smoke.py', '--device=cpu', '--out_dir=checks/cpu')
for method, field, default in [('adamw', 'learning_rate', 0.0003), ('sgdm', 'sgdm_learning_rate', 0.1), ('muon', 'muon_learning_rate', 0.01)]:
    base = Path(f'runs/{method}-default')
    run('train.py', config(method, 'default', field, default))
    rows = list(csv.DictReader((base / 'metrics.csv').open()))
    losses = [float(row['val_loss']) for row in rows]
    # A rising validation loss late in training motivates a smaller peak LR.
    # If the endpoint still improves on the midpoint, try a larger peak LR.
    factor = 0.5 if losses[-1] > losses[len(losses)//2] else 2
    print('LR decision:', method, losses, factor, flush=True)
    run('train.py', config(method, 'other', field, default * factor))
    for label in ('default', 'other'):
        run('plot.py', '--run-dir', f'runs/{method}-{label}')
run('sample.py', '--checkpoint=runs/adamw-default/last.pt', '--tokens=400')
run('plot.py', '--runs-dir=runs')
run('export_results.py', '--runs-dir=runs', '--output=export.zip')
Path('pipeline-complete.txt').write_text(datetime.now(timezone.utc).isoformat())
