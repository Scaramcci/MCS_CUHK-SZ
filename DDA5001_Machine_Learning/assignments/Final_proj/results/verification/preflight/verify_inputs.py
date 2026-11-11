"""Run from Final_proj with the local PyTorch environment."""
import csv
import hashlib
import json
import math
from pathlib import Path
import sys
import tarfile

import numpy as np
import torch

src = Path('src')
sys.path.insert(0, str(src.resolve()))
from model import GPT, GPTConfig
from train import prediction_windows

replacements = {
    "causal_mask.diagonal": "0", "shifted_labels.offset": "1",
    "optimizer_adamw.lr": "learning_rate", "optimizer_sgdm.lr": "sgdm_learning_rate",
    "optimizer_muon.lr": "muon_learning_rate", "optimizer_muon.momentum": "muon_momentum",
    "optimizer_step": "optimizer.step()", "plots.x": "xs", "plots.y": "ys",
}
seen = set()
with tarfile.open("local_artifacts/upstream/dda-p1-source.tgz") as archive:
    count = 0
    for member in archive:
        if member.isfile() and "/p1/" in member.name:
            path = src / member.name.split("/p1/")[1]
            expected = archive.extractfile(member).read()
            for token, value in replacements.items():
                marker = f'todo("{token}")'.encode()
                if marker in expected:
                    seen.add(token)
                    expected = expected.replace(marker, value.encode())
            assert expected == path.read_bytes(), path
            count += 1
assert seen == set(replacements)
print("Pinned release files verified:", count)
for line in Path("results/input-sha256.txt").read_text().splitlines():
    checksum, path = line.split(maxsplit=1)
    assert hashlib.sha256((src/path).read_bytes()).hexdigest() == checksum
data_dir = src / "data/shakespeare_char"
corpus = (data_dir / "input.txt").read_text()
vocab = sorted(set(corpus))
assert len(vocab) == 65
mapping = dict(zip(vocab, range(len(vocab))))
all_ids = np.fromiter(map(mapping.__getitem__, corpus), dtype=np.uint16)
assert len(all_ids) == 1003854 + 111540
for split, expected in [('train', all_ids[:1003854]), ('val', all_ids[1003854:])]:
    np.testing.assert_array_equal(np.fromfile(data_dir / f"{split}.bin", dtype=np.uint16), expected)
print("All training and validation tokens independently reconstructed")
ids = torch.tensor([7, 7, 3, 9, 3])
for block in range(1, len(ids)):
    starts = torch.arange(len(ids) - block).flip(0)
    x, y = prediction_windows(ids, starts, block)
    for i, start in enumerate(starts):
        assert x[i].tolist() == ids[start:start+block].tolist()
        assert y[i].tolist() == ids[start+1:start+block+1].tolist()
print("All window lengths, final index and repeated IDs passed")
smoke = Path('results/verification/preflight/smoke')
state = torch.load(smoke/'last.pt', map_location='cpu', weights_only=True)
model = GPT(GPTConfig(**state['model_args'])).eval()
model.load_state_dict(state['model'])
torch.set_num_threads(4)
g = torch.Generator().manual_seed(1730)
val = torch.from_numpy(all_ids[1003854:].astype(np.int64))
nll = 0.0
with torch.no_grad():
    for _ in range(2):
        starts = torch.randint(len(val)-32, (4,), generator=g)
        x = torch.stack([val[i:i+32] for i in starts])
        y = torch.stack([val[i+1:i+33] for i in starts])
        logits, _ = model(x, y)
        nll -= logits.double().log_softmax(-1).gather(-1, y.unsqueeze(-1)).sum().item()
    changed = x.clone()
    changed[:, 14:] = (changed[:, 14:]+1) % 65
    alternate, _ = model(changed, y)
    assert torch.equal(logits[:, :14], alternate[:, :14])
score = nll / 256
local = json.loads((smoke/'summary.json').read_text())
remote = json.loads(Path('results/run-10R3a5Il/checks/cpu/summary.json').read_text())
for record in [local, remote]:
    assert record['status'] == 'completed' and record['step'] == 8 and record['tokens'] == 1024
    assert math.isclose(score, record['endpoint_scores']['loss'], abs_tol=1e-5, rel_tol=0)
print(f"Independent token-weighted endpoint {score:.10f}, local {local['endpoint_scores']['loss']:.10f}, remote {remote['endpoint_scores']['loss']:.10f}; prefix logits invariant.")
print("PyTorch", torch.__version__)
