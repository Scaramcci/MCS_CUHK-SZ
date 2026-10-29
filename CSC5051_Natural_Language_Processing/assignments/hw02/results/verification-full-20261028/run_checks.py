"""Run independent offline verification and retain exact command output."""
from pathlib import Path
import hashlib,json,os,platform,subprocess,sys
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
LOCAL=ROOT/'local_artifacts/verification-20261028'
PYTHON=LOCAL/'venv/bin/python'
checks=[]
def invoke(args,expected=0):
    cmd=[str(PYTHON),'-B']+args
    r=subprocess.run(cmd,cwd=ROOT,env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'TMPDIR':str(LOCAL),'PYTHONDONTWRITEBYTECODE':'1'},text=True,capture_output=True)
    i=f'{len(checks):02}'
    (OUT/f'{i}-stdout.txt').write_text(r.stdout);(OUT/f'{i}-stderr.txt').write_text(r.stderr)
    checks.append({'command':cmd,'cwd':str(ROOT),'expected_exit':expected,'actual_exit':r.returncode,'passed':r.returncode==expected,'stdout':f'{i}-stdout.txt','stderr':f'{i}-stderr.txt'})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
invoke(['tests/offline_smoke.py'])
invoke([str(OUT/'independent_tests.py')])
invoke(['src/main.py','check'])
for m in ('zero_shot','few_shot','chain_of_thought','agent','agent_no_feedback'):invoke(['src/main.py','preview','--method',m])
invoke(['src/main.py','run','--dataset','not-read','--output','not-created'],2)
invoke(['src/prepare_data.py','--source','data/raw/alpaca_gpt4_data.json','--output',str(LOCAL/'reproduced-data')])
data_checks={name:sha(ROOT/'data/processed'/name)==sha(LOCAL/'reproduced-data'/name) for name in ('dev.jsonl','pilot.jsonl','test.jsonl','manifest.json')}
source_hash=sha(ROOT/'data/raw/alpaca_gpt4_data.json')
originals={p.name:sha(p) for p in (ROOT/'requirement').iterdir() if p.is_file()}
rows={s:[json.loads(line) for line in (ROOT/f'data/processed/{s}.jsonl').read_text().splitlines()] for s in ('dev','test','pilot')}
assert not {r['base_id'] for r in rows['dev']} & {r['base_id'] for r in rows['test']}
assert {r['id'] for r in rows['pilot']} <= {r['id'] for r in rows['dev']}
original_data=json.loads((ROOT/'data/raw/alpaca_gpt4_data.json').read_text())
for split in ('dev','test'):
    for r in rows[split]:
        source=original_data[r['source_index']]
        assert all(r[k]==source[k] for k in ('instruction','input'))
        if r['variant']=='unaltered':assert r['output']==source['output']
        elif r['defect']=='empty':assert r['output']==''
        elif r['defect']=='instruction_echo':assert r['output']==source['instruction']+ ('\n'+source['input'] if source['input'] else '')
        elif r['defect']=='excessive_repetition':assert r['output']=='\n\n'.join([source['output']]*4)
        elif r['defect']=='off_topic':assert r['output']==original_data[r['donor_source_index']]['output']
assert all(data_checks.values())
assert source_hash=='0bd4f62585d494b794deb043ce0baddfec02f27696857c57c9c238d6eff35a18'
assert originals['Assignment_2.pdf']=='bf09fbc9f382a149804a7977a6cc63912efa93520c56d4c7fe7c51260e64aa5f'
assert next(v for k,v in originals.items() if k.endswith('.ipynb'))=='5a396a71600492e39974d51ee7a2e6c5bf020242896dd37db88fcae2310c26e9'
manifest={str(p.relative_to(ROOT)):sha(p) for p in list((ROOT/'src').glob('*.py'))+list((ROOT/'prompts').glob('*.txt'))+list((ROOT/'tests').glob('*.py'))+[ROOT/'config/experiment.json']}
record={'executor':'/root/verifier','time':datetime.now(timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'venv':str(PYTHON),'checks':checks,'data_reproduction_exact':data_checks,'data_source_sha256':source_hash,'original_hashes':originals,'data_integrity':'all dev/test variants independently compared with raw source; disjoint base split; pilot subset of dev','input_manifest':manifest,'status':'provisional_offline_only_waiting_final_heldout'}
(OUT/'offline-run.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
assert all(x['passed'] for x in checks)
print('PASS: 10 subprocess checks, 19 author tests, 10 independent tests, byte-identical preparation and source/variant integrity. Final heldout verification pending.')
