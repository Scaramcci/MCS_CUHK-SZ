"""Assemble an explicit, data-free homework candidate; archive older candidates."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import zipfile

base = Path(__file__).resolve().parents[1]
name = 'Zhong-Kunyuan-hw2'
submission = base/'submission'
submission.mkdir(exist_ok=True)
folder, archive = submission/name, submission/(name+'.zip')
existing = [p for p in (folder,archive) if p.exists()]
if existing:
    history = base/'results/submission-history'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    history.mkdir(parents=True)
    for p in existing:
        shutil.move(str(p),str(history/p.name))
folder.mkdir()
files = {'DDA5001_HW2_answers.pdf':base/'report/main.pdf',
         'README.md':base/'notes/package_readme.md',
         'requirements.txt':base/'src/requirements.txt',
         'requirements-frozen.txt':base/'results/requirements-frozen.txt'}
for problem in ('p2','p3'):
    for file in ('algorithms.py','framework.py','run.py','test_'+problem+'.py','verify.py'):
        files[problem+'/'+file]=base/'src'/problem/file
for problem,graphs in [('p2',['digits_loss','digits_accuracy','dry_bean_loss','dry_bean_accuracy']),
                       ('p3',['target_complexity','noise_variance'])]:
    for graph in graphs:
        files['figures/'+graph+'.png']=base/'results/run-20261027'/problem/(graph+'.png')
manifest={}
for relative,source in files.items():
    target=folder/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,target)
    manifest[relative]={'bytes':target.stat().st_size,
                        'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
                        'source':str(source.relative_to(base))}
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for relative in sorted(files):
        z.write(folder/relative,name+'/'+relative)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert set(z.namelist()) == {name+'/'+r for r in files}
    for relative in files:
        assert hashlib.sha256(z.read(name+'/'+relative)).hexdigest()==manifest[relative]['sha256']
record={'assembled_utc':datetime.now(timezone.utc).isoformat(),
        'status':'candidate awaiting independent review and student-specific requirements',
        'archive':str(archive.relative_to(base)), 'archive_bytes':archive.stat().st_size,
        'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
        'files':manifest}
run=base/'results/submission-manifests'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
run.mkdir(parents=True)
(run/'manifest.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='files'},indent=2))
print('Files:',len(files))
