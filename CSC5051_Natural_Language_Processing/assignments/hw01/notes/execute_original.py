"""Run the original-template solution without rewriting teacher code cells."""
import os, sys, json, hashlib, subprocess, datetime, zipfile
from pathlib import Path
root = Path(__file__).resolve().parents[1]
os.environ.pop('PYTHONPATH', None)
os.environ['PYTHONNOUSERSITE'] = '1'
os.environ['PATH'] = str(Path(sys.executable).parent) + os.pathsep + os.environ['PATH']
for key, relative in {'GENSIM_DATA_DIR':'data/downloads/gensim', 'NLTK_DATA':'data/downloads/nltk_data',
                      'JUPYTER_CONFIG_DIR':'.cache/jupyter/config', 'JUPYTER_RUNTIME_DIR':'.cache/jupyter/runtime',
                      'IPYTHONDIR':'.cache/ipython', 'MPLCONFIGDIR':'.cache/matplotlib'}.items():
    folder=root/relative
    folder.mkdir(parents=True,exist_ok=True)
    os.environ[key]=str(folder)
import nbformat
from nbclient import NotebookClient
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('original_%Y%m%dT%H%M%S_%fZ')
evidence=root/'results'/stamp
evidence.mkdir(parents=True)
path=root/'report/26Fall_NLP_Assignment_1_CSC6052_5051_MDS5110.ipynb'
nb=nbformat.read(path,as_version=4)
for cell in nb.cells:
    if cell.cell_type=='code': cell.outputs=[];cell.execution_count=None
nbformat.write(nb,evidence/'input.ipynb')
status={'status':'running','command':f'env -u PYTHONPATH PYTHONNOUSERSITE=1 {sys.executable} -s -u notes/execute_original.py',
        'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'kernel':'nlp','executor':'primary session / implementer self-check',
        'input_sha256':hashlib.sha256((evidence/'input.ipynb').read_bytes()).hexdigest()}
def save():
    nbformat.write(nb,path)
    (evidence/'status.json').write_text(json.dumps(status,indent=2)+'\n')
def started(cell,cell_index,**kw):print('START',cell_index,flush=True)
def finished(cell,cell_index,**kw):
    save()
    for out in cell.get('outputs',[]):
        if out.output_type=='stream':print(out.text[-1800:],end='',flush=True)
    if cell_index==8:
        assert zipfile.is_zipfile(root/'report/quora.zip'), 'Original download did not produce a valid ZIP'
        assert hashlib.sha256((root/'report/train.csv').read_bytes()).hexdigest()=='5f28dbe0bb01b39a793f36567d18fe7cf34d20bbca69ff85b131d7c2186f9914'
    print('DONE',cell_index,flush=True)
print('Evidence:',evidence,flush=True)
client=NotebookClient(nb,timeout=1800,kernel_name='nlp',resources={'metadata':{'path':str(path.parent)}},
                      on_cell_start=started,on_cell_executed=finished)
try:
    client.execute()
    status['status']='completed'
except BaseException as exc:
    status.update(status='failed',error=repr(exc));raise
finally:
    status['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    save();nbformat.write(nb,evidence/'executed.ipynb')
    status['output_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    (evidence/'status.json').write_text(json.dumps(status,indent=2)+'\n')
    (evidence/'packages.txt').write_text(subprocess.check_output([sys.executable,'-s','-m','pip','freeze'],text=True))
    print('Final status:',status['status'],flush=True)
