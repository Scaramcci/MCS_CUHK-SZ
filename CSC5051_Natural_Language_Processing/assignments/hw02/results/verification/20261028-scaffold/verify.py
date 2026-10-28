"""Independent offline verification, no real credentials read."""
import contextlib, hashlib, importlib.util, io, json, os, platform, shutil, socket, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
from unittest.mock import patch
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.dont_write_bytecode=True
results=[]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args, expected, cwd=ROOT):
    env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'PYTHONDONTWRITEBYTECODE':'1','DEEPSEEK_API_KEY':'independent-sentinel-not-a-real-key','EXPERIMENT_BUDGET_CNY':'99'}
    r=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True)
    ident=f'{len(results):02d}'
    (OUT/f'{ident}-stdout.txt').write_text(r.stdout)
    (OUT/f'{ident}-stderr.txt').write_text(r.stderr)
    results.append({'argv':args,'cwd':str(cwd),'expected_exit':expected,'actual_exit':r.returncode,'pass':r.returncode==expected,'stdout':f'{ident}-stdout.txt','stderr':f'{ident}-stderr.txt'})
    assert 'independent-sentinel-not-a-real-key' not in r.stdout+r.stderr
    return r
manifest=json.loads((ROOT/'results/selfcheck-20261028T212339+0800/authored-files.json').read_text())
actual={p:digest(ROOT/p) for p in manifest}
assert actual==manifest
(OUT/'verified-input-hashes.json').write_text(json.dumps(actual,indent=2)+'\n')
originals={p.name:digest(p) for p in (ROOT/'requirement').iterdir() if p.is_file()}
assert originals['Assignment_2.pdf']=='bf09fbc9f382a149804a7977a6cc63912efa93520c56d4c7fe7c51260e64aa5f'
assert next(v for k,v in originals.items() if k.endswith('.ipynb'))=='5a396a71600492e39974d51ee7a2e6c5bf020242896dd37db88fcae2310c26e9'
run(['python3','src/main.py','check'],0)
for method in ('zero_shot','few_shot','chain_of_thought'):
    r=run(['python3','src/main.py','preview','--method',method],0)
    assert '<INSTRUCTION>' in r.stdout and 'NOT A MODEL RESPONSE' in r.stdout
    assert '$rubric' not in r.stdout and '$record' not in r.stdout
run(['python3','src/main.py','run'],2)
run(['python3','tests/offline_smoke.py'],0)
run(['python3',str(ROOT/'src/main.py'),'check'],0,cwd=OUT)
run(['python3','src/main.py','preview','--method','not_a_method'],2)
run(['git','check-ignore','.env'],0)
run(['git','check-ignore','.env.example'],1)
run(['git','check-ignore','data/raw/alpaca.json','local_artifacts/response.json',str(next((ROOT/'requirement').glob('*.ipynb')))],0)
# Isolated variants never modify the frozen implementation or the actual .env.
copy=OUT/'isolated'; copy.mkdir(exist_ok=True)
for folder in ('src','config','prompts'):
    shutil.copytree(ROOT/folder,copy/folder,dirs_exist_ok=True)
(copy/'.env').write_text('DEEPSEEK_API_KEY=independent-sentinel-not-a-real-key\nEXPERIMENT_BUDGET_CNY=99\n')
config=copy/'config/experiment.json'; valid=config.read_text()
config.write_text('{broken json')
run(['python3','src/main.py','check'],1,cwd=copy)
config.write_text('[]')
run(['python3','src/main.py','check'],1,cwd=copy)
config.write_text(valid)
(copy/'prompts/zero_shot.txt').rename(copy/'prompts/zero_shot.txt.disabled')
run(['python3','src/main.py','check'],1,cwd=copy)
(copy/'prompts/zero_shot.txt.disabled').rename(copy/'prompts/zero_shot.txt')
# Intercept credential file reads, DNS, sockets and process launches in-process.
spec=importlib.util.spec_from_file_location('independent_scaffold',copy/'src/main.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
old_open=Path.open
def deny_env(p,*a,**kw):
    assert p.name!='.env','unexpected credential read'
    return old_open(p,*a,**kw)
with patch.object(Path,'open',deny_env), patch.object(socket,'socket',side_effect=AssertionError('socket attempted')), patch.object(socket,'getaddrinfo',side_effect=AssertionError('DNS attempted')), patch.object(subprocess,'Popen',side_effect=AssertionError('subprocess attempted')), patch.dict(os.environ,{'DEEPSEEK_API_KEY':'independent-sentinel-not-a-real-key','EXPERIMENT_BUDGET_CNY':'99'}):
    for argv,expected in [(['check'],0),(['run'],2)]+[(['preview','--method',m],0) for m in mod.METHODS]:
        buf=io.StringIO()
        with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):
            code=mod.main(argv)
        assert code==expected and 'independent-sentinel-not-a-real-key' not in buf.getvalue()
assert {p:digest(ROOT/p) for p in manifest}==manifest
assert not (ROOT/'submission').exists()
record={'executor':'/root/verifier','time':datetime.now(timezone(timedelta(hours=8))).isoformat(),'python':sys.version,'platform':platform.platform(),'source_original_hashes':originals,'checks':results,'boundary_interception':'passed: .env read, sockets, DNS, subprocess denied; check + 3 previews + run expected behavior','frozen_manifest_unchanged':True,'all_passed':all(r['pass'] for r in results)}
(OUT/'run.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
assert record['all_passed']
print(f'PASS: {len(results)} subprocess checks; independent boundary interception; originals and frozen manifest unchanged.')
