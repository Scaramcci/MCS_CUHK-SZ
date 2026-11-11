"""Run in Final_proj after all six artifacts are available; reads originals only."""
import csv
import hashlib
import json
import math
from pathlib import Path
import runpy
import sys

from PIL import Image

root = Path("results/run-10R3a5Il")
runs = root / 'runs'
defaults = runpy.run_path("src/config/train_shakespeare_char.py")
methods = {'adamw': 'learning_rate', 'sgdm': 'sgdm_learning_rate', 'muon': 'muon_learning_rate'}

def read_json(path):
    return json.loads(path.read_text())

def check_image(path):
    with Image.open(path) as picture:
        assert picture.format == 'PNG' and min(picture.size) >= 300
        picture.verify()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_run(name, method, peak):
    base = runs / name
    cfg, env, summary = [read_json(base / (key+'.json')) for key in ('config', 'environment', 'summary')]
    expected = {k: v for k, v in defaults.items() if not k.startswith('_')}
    expected.update(optimizer_name=method, out_dir='runs/'+name, n_head=16, n_layer=24, n_embd=1024)
    expected[methods[method]] = peak
    assert all(cfg[k] == v for k,v in expected.items()), name
    assert cfg['resume'] == '' and env['initialization'] == 'random_from_scratch'
    assert (env['gpu'], env['torch'], env['dtype']) == ('NVIDIA GeForce RTX 4090 D', '2.9.0+cu128', 'bfloat16')
    for f, h in env['source_sha256'].items():
        assert digest((Path('notes') if f == 'run-six.py' else Path('src'))/f) == h, f
    for f,h in env['dataset_sha256'].items():
        assert digest(Path('src/data/shakespeare_char')/f) == h, f
    if method == 'muon':
        assert env['muon_implementation'] == 'torch.optim.Muon/original'
    with (base/'metrics.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    assert [int(r['step']) for r in rows] == list(range(0, 5001, 500))
    log = (base/'run.log').read_text()
    last_t = -1
    for r in rows:
        step = int(r['step'])
        assert int(r['tokens']) == step * 18432
        duration, val = float(r['train_seconds']), float(r['val_loss'])
        assert duration > last_t and float(r['wall_seconds']) >= duration
        last_t = duration
        assert math.isfinite(val) and math.isfinite(float(r['train_loss']))
        assert f'step {step}: tokens={step*18432} train_s={duration:.3f} val_loss={val:.4f}' in log
        phase = ((step-1)-100)/4900
        factor = .1 + .45*(1 + math.cos(math.pi*phase)) if step else 0
        rates = {'adamw': 0, 'sgdm': 0, 'muon': 0}
        rates[method] = peak * factor
        if method == 'muon':
            rates['adamw'] = defaults['learning_rate'] * factor
        assert all(math.isclose(float(r[k+'_lr']), lr, rel_tol=1e-12) for k,lr in rates.items())
    vals = [float(r['val_loss']) for r in rows]
    assert summary['status'] == 'completed' and summary['budget'] == 'tokens'
    assert (summary['step'], summary['tokens'], summary['train_seconds']) == (5000, 92160000, last_t)
    scores = summary['endpoint_scores']
    assert vals[-1] == scores['loss'] and min(vals) == summary['best_val_loss']
    assert math.isclose(math.exp(vals[-1]),scores['perplexity'])
    assert math.isclose(vals[-1]/math.log(2),scores['bits_per_character'])
    assert 'Completed; endpoint saved as last.pt and summary.json.' in log
    for axis in ['tokens','train_seconds']:
        check_image(base/f'loss_vs_{axis}.png')
    print(f'{name}: peak LR {peak}, endpoint {vals[-1]:.9f}, train seconds {last_t:.3f}, best loss {min(vals):.9f}')
    return vals

if __name__ == '__main__':
    for method, field in methods.items():
        rate = defaults[field]
        vals = check_run(method+'-default', method, rate)
        other = rate * (.5 if vals[-1] > vals[len(vals)//2] else 2)
        chosen = check_run(method+'-other', method, other)
        reversals = [(i*500, (i+1)*500) for i in range(1,10) if (chosen[i]-vals[i])*(chosen[i+1]-vals[i+1]) < 0]
        print(f'{method}: observed validation ordering changes in step brackets {reversals}')
    assert len([p for p in runs.iterdir() if p.is_dir() and (p/'config.json').is_file()]) == 6
    for axis in ['tokens','train_seconds']:
        check_image(runs/f'comparison_tokens_vs_{axis}.png')
    sample = (runs/'adamw-default'/'samples.txt').read_text()
    assert len(sample)==401 and sample[0]=='\n'
    assert set(sample) <= set(Path('src/data/shakespeare_char/input.txt').read_text())
    print('All six curves, per-run and comparison plots, endpoint metrics, times, source/data hashes, sample length and vocabulary passed.')
