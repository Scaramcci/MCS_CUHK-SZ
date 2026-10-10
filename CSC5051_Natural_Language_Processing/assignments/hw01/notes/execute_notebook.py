"""Execute with the NLP kernel, checkpoint outputs after each cell and retain failures."""
import os
from pathlib import Path
root = Path(__file__).resolve().parents[1]
os.environ['PYTHONNOUSERSITE'] = '1'
os.environ.pop('PYTHONPATH', None)
for var, path in {'JUPYTER_CONFIG_DIR': root/'.cache/jupyter/config',
                  'JUPYTER_RUNTIME_DIR': root/'.cache/jupyter/runtime',
                  'IPYTHONDIR': root/'.cache/ipython',
                  'MPLCONFIGDIR': root/'.cache/matplotlib'}.items():
    os.environ[var] = str(path)
    path.mkdir(parents=True, exist_ok=True)
import json
import hashlib
import subprocess
import sys
from datetime import datetime, timezone
import nbformat
from nbclient import NotebookClient

notebook = root/'report/26Fall_NLP_Assignment_1_CSC6052_5051_MDS5110.ipynb'
stamp = datetime.now(timezone.utc).strftime('execution_%Y%m%dT%H%M%S_%fZ')
evidence = root/'results'/stamp
evidence.mkdir(parents=True)
nb = nbformat.read(notebook, as_version=4)
nbformat.write(nb, evidence/'input.ipynb')
source_hash = hashlib.sha256(notebook.read_bytes()).hexdigest()
(evidence/'packages.txt').write_text(subprocess.check_output([sys.executable,'-s','-m','pip','freeze'],text=True))
status = {'executor':'primary Codex session (self-check, not independent verification)',
          'python':sys.version, 'executable':sys.executable,
          'source_sha256':source_hash, 'kernel':'nlp',
          'command':f'env -u PYTHONPATH PYTHONNOUSERSITE=1 {sys.executable} -s -u notes/execute_notebook.py',
          'started_utc':stamp, 'status':'running'}
(evidence/'status.json').write_text(json.dumps(status,indent=2))
print('Evidence:', evidence, flush=True)

def started(cell, cell_index, **kwargs):
    print(f'START cell {cell_index}', flush=True)

def executed(cell, cell_index, **kwargs):
    nbformat.write(nb, notebook)
    for output in cell.get('outputs', []):
        if output.output_type == 'stream':
            # Keep verbose download progress out of the terminal summary.
            content = output.text
            if len(content) > 2500: content = content[-2500:]
            print(content, end='', flush=True)
        elif output.output_type == 'error':
            print(output.ename, output.evalue, flush=True)
    print(f'DONE cell {cell_index}', flush=True)

client = NotebookClient(nb, timeout=3600, kernel_name='nlp',
                        resources={'metadata': {'path':str(notebook.parent)}},
                        on_cell_start=started, on_cell_executed=executed,
                        store_widget_state=True)
try:
    client.execute()
except BaseException as e:
    status.update(status='failed', error=repr(e))
    raise
else:
    status['status']='completed'
finally:
    nbformat.write(nb, notebook)
    nbformat.write(nb, evidence/'executed.ipynb')
    status['output_sha256']=hashlib.sha256(notebook.read_bytes()).hexdigest()
    status['finished_utc']=datetime.now(timezone.utc).isoformat()
    (evidence/'status.json').write_text(json.dumps(status,indent=2))
    print('Final status:',status['status'],flush=True)
