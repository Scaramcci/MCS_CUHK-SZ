"""Run from Final_proj to verify preserved checkpoints, actual sample and export."""
import csv
import hashlib
import json
from pathlib import Path
import sys
import zipfile

import torch

sys.path.insert(0, str(Path('src').resolve()))
from model import GPT, GPTConfig

root = Path('results/run-10R3a5Il')
backups = Path('checkpoints/run-10R3a5Il')
runs = root / 'runs'
torch.set_num_threads(4)
for path in sorted(backups.glob('*/*.pt')):
    run = runs / path.parent.name
    cfg = json.loads((run/'config.json').read_text())
    summary = json.loads((run/'summary.json').read_text())
    with (run/'metrics.csv').open() as f:
        rows = list(csv.DictReader(f))
    best = min(rows, key=lambda row: float(row['val_loss']))
    endpoint = rows[-1] if path.stem == 'last' else best
    record = torch.load(path, weights_only=True, map_location='cpu', mmap=True)
    assert record['config'] == cfg and record['best_loss'] == float(best['val_loss'])
    assert record['step'] == int(endpoint['step']) and record['tokens'] == int(endpoint['tokens'])
    assert record['train_seconds'] == float(endpoint['train_seconds'])
    assert len(record['optimizers']) == (2 if cfg['optimizer_name'] == 'muon' else 1)
    assert record['model_args']['vocab_size'] == len(record['tokenizer']['stoi']) == 65
    assert (record['model_args']['n_layer'], record['model_args']['n_head'], record['model_args']['n_embd']) == (24, 16, 1024)
    assert record['model']['transformer.wte.weight'].shape == (65,1024)
    print(path.relative_to(backups), 'step', record['step'], 'tokens', record['tokens'], 'consistent')
    del record

sample = (runs/'adamw-default/samples.txt').read_text()
pipeline = (root/'pipeline.log').read_text()
sample_block = pipeline.split("'sample.py', '--checkpoint=runs/adamw-default/last.pt', '--tokens=400']\n")[1]
assert (sample + '\nSaved: runs/adamw-default/samples.txt\nexit 0') in sample_block
with zipfile.ZipFile('local_artifacts/export.zip') as z:
    assert z.testzip() is None
    names = z.namelist()
    assert len(names)==len(set(names))
    for member in names:
        if member.startswith('results/'):
            local = runs / member.removeprefix('results/')
        elif member.startswith('code/'):
            local = Path('src') / member.removeprefix('code/')
            if member == 'code/run-six.py':
                local = Path('notes/run-six.py')
        else:
            assert member == 'README.txt'
            continue
        assert local.read_bytes() == z.read(member), member
    expected = {'results/'+p.relative_to(runs).as_posix() for p in runs.rglob('*') if p.is_file()}
    assert {n for n in names if n.startswith('results/')} == expected
    print('All',len(names),'raw export entries passed; all', len(expected),'lightweight evidence files matched')
print('400-token endpoint sample identical across stdout, text file and export. SHA-256:',hashlib.sha256(sample.encode()).hexdigest())
corpus = Path('src/data/shakespeare_char/input.txt').read_text()
for part, label in [(corpus[:1003854], 'training'), (corpus[1003854:], 'validation')]:
    low, high = 0, len(sample)+1
    while high-low>1:
        size=(low+high)//2
        if any(sample[i:i+size] in part for i in range(len(sample)-size+1)):
            low=size
        else:
            high=size
    print(label, 'longest exact substring:', low, 'characters')

# Check the first 64 generated characters against the actual endpoint distribution.
# CUDA and CPU use different RNGs. Token ranks and log likelihood are deterministic.
state = torch.load(backups/'adamw-default/last.pt', weights_only=True, map_location='cpu', mmap=True)
model = GPT(GPTConfig(**state['model_args']))
model.load_state_dict(state['model'], assign=True)
model.eval()
tokens = torch.tensor([[state['tokenizer']['stoi'][ch] for ch in sample[:65]]])
with torch.inference_mode():
    logits,_ = model(tokens[:,:-1],tokens[:,1:].contiguous())
    assert torch.isfinite(logits).all()
    token_nll = -logits.double().log_softmax(-1).gather(-1,tokens[:,1:].unsqueeze(-1)).mean()
    matches = (logits.argmax(-1)==tokens[:,1:]).sum().item()
print(f'CPU forward on sampled prefix: {matches}/64 observed tokens top-1, mean NLL {token_nll.item():.5f}')
