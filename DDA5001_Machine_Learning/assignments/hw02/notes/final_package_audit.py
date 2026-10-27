"""Fresh readonly audit and tests of the exact final ZIP, with isolated outputs."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import time
import zipfile

base = Path(__file__).resolve().parents[1]
out = base/'results/final-audit-20261027'
out.mkdir(exist_ok=False)
archive = base/'submission/Zhong-Kunyuan-hw2.zip'
root = 'Zhong-Kunyuan-hw2'
hashfile = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert hashfile(archive) == '16dda52687c9733e4e0091cd67d12ac137b6519e27dfa8a0cbbd2e40bf537fbb'
expected = {'DDA5001_HW2_answers.pdf':base/'report/main.pdf',
            'README.md':base/'notes/package_readme.md',
            'requirements.txt':base/'src/requirements.txt',
            'requirements-frozen.txt':base/'results/requirements-frozen.txt'}
for problem in ('p2','p3'):
    for filename in ('algorithms.py','framework.py','run.py',f'test_{problem}.py','verify.py'):
        expected[f'{problem}/{filename}']=base/'src'/problem/filename
for problem,names in [('p2',('digits_loss','digits_accuracy','dry_bean_loss','dry_bean_accuracy')),
                      ('p3',('target_complexity','noise_variance'))]:
    for name in names:
        expected[f'figures/{name}.png']=base/'results/run-20261027'/problem/(name+'.png')
extracted=out/'.cache/extracted'
extracted.mkdir(parents=True)
members={}
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.infolist()) == len(expected) == 20
    assert set(z.namelist()) == {root+'/'+n for n in expected}
    for name, source in expected.items():
        full=root+'/'+name
        assert not PurePosixPath(full).is_absolute() and '..' not in PurePosixPath(full).parts
        data=z.read(full)
        assert data==source.read_bytes(), ('source mismatch',full)
        assert data==(base/'submission'/root/name).read_bytes(), ('disk mismatch',full)
        path=extracted/full
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
        members[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

with zipfile.ZipFile(base/'code_source(1).zip') as z:
    for problem in ('p2','p3'):
        for filename in ('framework.py','run.py',f'test_{problem}.py'):
            assert (extracted/root/problem/filename).read_bytes()==z.read(f'code_source/{problem}/{filename}')
    assert (extracted/root/'requirements.txt').read_bytes()==z.read('code_source/requirements.txt')

env=os.environ.copy()
env.pop('PYTHONPATH',None)
env['PYTHONDONTWRITEBYTECODE']='1'
env['MPLCONFIGDIR']=str(out/'.cache/matplotlib')
python=str(base/'.venv312/bin/python')
commands=[('p2-tests',[python,'-m','unittest','discover','-s','p2','-v']),
          ('p3-tests',[python,'-m','unittest','discover','-s','p3','-v']),
          ('p2-checks',[python,'p2/verify.py','--output',str(out/'p2-checks.json')]),
          ('p3-checks',[python,'p3/verify.py','--output',str(out/'p3-checks.json')])]
runs=[]
for name,argv in commands:
    rec={'command':argv,'cwd':str(extracted/root),
         'started_utc':datetime.now(timezone.utc).isoformat(),
         'environment_adjustments':{'PYTHONPATH':'removed','PYTHONDONTWRITEBYTECODE':'1','MPLCONFIGDIR':'audit-local cache'}}
    start=time.perf_counter()
    with (out/(name+'.stdout.txt')).open('w') as stdout, (out/(name+'.stderr.txt')).open('w') as stderr:
        p=subprocess.run(argv,cwd=extracted/root,env=env,stdout=stdout,stderr=stderr)
    rec.update(exit_code=p.returncode,elapsed_seconds=time.perf_counter()-start,
               finished_utc=datetime.now(timezone.utc).isoformat())
    (out/(name+'.run.json')).write_text(json.dumps(rec,indent=2)+'\n')
    runs.append({'name':name,'exit_code':p.returncode})
    assert p.returncode==0,(name,p.returncode)

for problem in ('p2','p3'):
    current=json.loads((out/(problem+'-checks.json')).read_text())
    original=json.loads((base/'results/run-20261027'/(problem+'-checks.json')).read_text())
    assert current['all_passed'] is True
    assert current['checks']==original['checks']
    assert current['source_sha256']==original['source_sha256']

info=subprocess.run(['pdfinfo',str(extracted/root/'DDA5001_HW2_answers.pdf')],capture_output=True,text=True,check=True)
(out/'pdfinfo.txt').write_text(info.stdout)
assert 'Pages:           12' in info.stdout
text=subprocess.run(['pdftotext','-layout',str(extracted/root/'DDA5001_HW2_answers.pdf'),'-'],capture_output=True,text=True,check=True).stdout
(out/'report-text.txt').write_text(text)
pages=text.split('\f')
assert len(pages)==13 and not pages[-1].strip()
assert 'AI collaboration case' in pages[6]
assert 'Problem 3(a)' in pages[7]
assert sum('AI collaboration case' in p for p in pages)==1
assert all('??' not in p for p in pages)
assert hashfile(archive)=='16dda52687c9733e4e0091cd67d12ac137b6519e27dfa8a0cbbd2e40bf537fbb'
summary={'checked_by':'coordinating Codex agent; fresh audit of final ZIP',
         'finished_utc':datetime.now(timezone.utc).isoformat(),
         'archive_sha256':hashfile(archive),'archive_bytes':archive.stat().st_size,
         'pdf_sha256':members['DDA5001_HW2_answers.pdf']['sha256'],
         'members':members,'public_tests_passed':{'p2':7,'p3':8},
         'fresh_runs':runs,'numerical_checks_equal_prior_record':True,
         'fixed_teacher_files_unchanged':True,'zip_equals_disk_and_sources':True,
         'pdf_pages':12,'ai_case_pages':1,'all_automated_checks_passed':True,
         'student_review':{'source':'user message','verbatim':'我看完了，没有问题，请再根据作业要求检查一遍作业，没有问题我就提交了',
                           'status':'user-reported review completed; no claim of independent proof of authorship or actual rewriting'},
         'original_pdf_sha256':hashfile(base/'DDA5001_HW2.pdf'),
         'original_zip_sha256':hashfile(base/'code_source(1).zip'),
         'blackboard_uploaded':False}
(out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ('members','student_review')},indent=2))
