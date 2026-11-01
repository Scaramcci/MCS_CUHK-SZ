"""DDA5001 HW3 Problem 3: complete only the three model constructors.

Use a coding agent for the A, B, and C model definitions. Data splitting,
SGD with Momentum, training, validation, testing, and plotting are provided.

Install: python -m pip install -r requirements.txt
Check models after filling them: python p3.py --check-models
Run: python p3.py
MNIST downloads automatically on first use and is cached in data/mnist/.
Keep data/p3/mnist_split_indices.npz with this file. Outputs go to outputs/.
"""
from pathlib import Path
import argparse
import copy
import csv
import hashlib
import json
import os
import platform
import time

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT / 'data/mnist'
SPLIT_FILE = ROOT / 'data/p3/mnist_split_indices.npz'
DEFAULT_OUT_DIR = ROOT / 'outputs'
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.cache/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME', str(ROOT / '.cache'))

import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from torchvision.datasets import MNIST
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

TRAIN_SEED = 666
SEEDS = (TRAIN_SEED,)
SPECS = [('A', 0, False), ('B', 64, False), ('C', 64, True)]
EPOCHS = 30
BATCH_SIZE = 128
LEARNING_RATE = 0.1
MOMENTUM = 0.9


def build_model_a():
    """Return model A as a torch.nn.Module.

    Input: a batch of flattened images, shape (batch_size, 784).
    Output: ten raw class scores, shape (batch_size, 10).
    """
    # TODO 1: Construct model A, the single linear layer from 784 inputs
    # to 10 outputs. Include a bias and return the complete nn.Module.
    # Do not add Softmax: the supplied cross-entropy loss takes raw logits.
    return nn.Linear(784, 10)


def build_model_b():
    """Return model B as a torch.nn.Module.

    Input/output batch shapes: (batch_size, 784) -> (batch_size, 10).
    The hidden layer has width 64, and both linear layers include a bias.
    """
    # TODO 2: Construct model B using two linear layers: 784 -> 64 -> 10.
    # There is NO activation between them and NO output Softmax.
    # Return the complete nn.Module, with a bias in each linear layer.
    return nn.Sequential(nn.Linear(784, 64), nn.Linear(64, 10))


def build_model_c():
    """Return model C as a torch.nn.Module.

    Input/output batch shapes: (batch_size, 784) -> (batch_size, 10).
    Keep B's layer dimensions and biases; add only the hidden activation.
    """
    # TODO 3: Construct model C using 784 -> 64 -> 10 linear layers.
    # Place ReLU BETWEEN the two linear layers; do not put it after the
    # final layer. Include both biases, return the nn.Module, and do not
    # add output Softmax. B and C must have the same layer dimensions.
    return nn.Sequential(nn.Linear(784, 64), nn.ReLU(), nn.Linear(64, 10))


def build_model(name='A'):
    """PROVIDED: select one of the three student-completed constructors."""
    builders = {'A': build_model_a, 'B': build_model_b, 'C': build_model_c}
    if name not in builders:
        raise ValueError('The supplied comparison uses only models A, B, and C.')
    model = builders[name]()
    if not isinstance(model, nn.Module):
        raise TypeError(f'Model {name} must be a torch.nn.Module.')
    return model


def parameter_count(model):
    """PROVIDED: count trainable parameters for checking the models."""
    return sum(parameter.numel() for parameter in model.parameters()
               if parameter.requires_grad)


def configure_cpu():
    """PROVIDED: use the fixed CPU protocol for this comparison."""
    torch.set_num_threads(1)
    torch.use_deterministic_algorithms(True)


def check_models(verbose=True):
    """PROVIDED: check output dimensions and report the parameter counts."""
    configure_cpu()
    rows = []
    for name, _, _ in SPECS:
        torch.manual_seed(TRAIN_SEED)
        model = build_model(name)
        model.eval()
        with torch.no_grad():
            logits = model(torch.zeros(2, 784))
        if logits.shape != (2, 10) or not torch.isfinite(logits).all():
            raise ValueError(f'Model {name} must return finite logits of shape (batch_size, 10).')
        rows.append({'model': name, 'parameters': parameter_count(model),
                     'output_shape': list(logits.shape)})
    if verbose:
        print('Model checks:', json.dumps(rows), flush=True)
    return rows


def make_splits(train_labels, test_labels):
    """PROVIDED: one fixed, class-balanced hold-out split, not cross-validation."""
    rng = np.random.default_rng(666)
    train, valid, test = [], [], []
    for label in range(10):
        train_rows = np.flatnonzero(train_labels == label)
        test_rows = np.flatnonzero(test_labels == label)
        if len(train_rows) < 800 or len(test_rows) < 200:
            raise ValueError('The fixed split needs at least 800 training and 200 test images per class.')
        rows = rng.permutation(train_rows)
        train.extend(rows[:600])
        valid.extend(rows[600:800])
        rows = rng.permutation(test_rows)
        test.extend(rows[:200])
    return {name: np.asarray(values, dtype=np.int64)
            for name, values in [('train', train), ('validation', valid), ('test', test)]}


def load_data(data_root=None, split_file=None):
    """PROVIDED: download/cache MNIST, verify the supplied split, and normalize pixels.

    Training and validation use disjoint subsets of the official training set.
    Testing uses a subset of the official test set, never a validation fold.
    Each image is flattened to 784 float32 pixels and divided by 255.
    """
    root = Path(data_root) if data_root is not None else DATA_ROOT
    index_path = Path(split_file) if split_file is not None else SPLIT_FILE
    if not index_path.is_file():
        raise FileNotFoundError('Keep data/p3/mnist_split_indices.npz with the package.')
    train = MNIST(str(root), train=True, download=True)
    test = MNIST(str(root), train=False, download=True)
    expected = make_splits(train.targets.numpy(), test.targets.numpy())
    with np.load(index_path, allow_pickle=False) as archive:
        splits = {name: archive[name].copy() for name in expected}
    if not all(np.array_equal(splits[name], expected[name]) for name in expected):
        raise ValueError('The supplied split does not match the fixed MNIST data protocol.')
    sets = {}
    for name, indices in splits.items():
        source = test if name == 'test' else train
        sets[name] = (source.data[indices].reshape(-1, 784).float() / 255.,
                      source.targets[indices].long())
    return sets, splits


@torch.no_grad()
def evaluate(model, X, y):
    """PROVIDED: mean cross-entropy and accuracy, without updating the model."""
    model.eval()
    loss, correct = 0., 0
    for start in range(0, len(y), 512):
        logits = model(X[start:start + 512])
        target = y[start:start + 512]
        loss += F.cross_entropy(logits, target, reduction='sum').item()
        correct += (logits.argmax(dim=1) == target).sum().item()
    return loss / len(y), correct / len(y)


def train_model(spec, seed, training, validation, epochs=EPOCHS):
    """PROVIDED: train on training data and choose a checkpoint by validation CE.

    Epoch zero is a plotted, untrained baseline, not an eligible checkpoint.
    The returned model has the lowest-validation-CE trained state restored.
    No test observations are passed into this function.
    """
    if epochs < 1:
        raise ValueError('Training must include at least one completed epoch.')
    name, width, _ = spec
    torch.manual_seed(seed)
    model = build_model(name)
    optimizer = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE,
                                momentum=MOMENTUM, weight_decay=0)
    generator = torch.Generator().manual_seed(seed + 1000)
    X, y = training
    Xv, yv = validation
    history = []
    best_loss, best_epoch, best_state = float('inf'), -1, None
    for epoch in range(epochs + 1):
        train_loss, train_acc = evaluate(model, X, y)
        val_loss, val_acc = evaluate(model, Xv, yv)
        history.append({'epoch': epoch, 'train_ce': train_loss,
                        'validation_ce': val_loss, 'train_accuracy': train_acc,
                        'validation_accuracy': val_acc})
        if epoch > 0 and val_loss < best_loss:
            best_loss, best_epoch = val_loss, epoch
            best_state = copy.deepcopy(model.state_dict())
        if epoch == epochs:
            break
        model.train()
        for batch in torch.randperm(len(y), generator=generator).split(BATCH_SIZE):
            optimizer.zero_grad(set_to_none=True)
            loss = F.cross_entropy(model(X[batch]), y[batch])
            loss.backward()
            optimizer.step()
    final_state = copy.deepcopy(model.state_dict())
    model.load_state_dict(best_state)
    row = {'model': name, 'seed': seed, 'width': width,
           'parameters': parameter_count(model), 'best_epoch': best_epoch,
           'validation_ce': best_loss,
           'validation_accuracy': history[best_epoch]['validation_accuracy']}
    return model, history, row, final_state


def write_csv(path, rows):
    """PROVIDED: save a table or training history."""
    with open(path, 'w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def plot_histories(histories, output_dir):
    """PROVIDED: the requested two-panel training/validation CE figure."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), constrained_layout=True)
    for name, _, _ in SPECS:
        history = histories[name]
        epochs = [row['epoch'] for row in history]
        for ax, key, label in zip(axes, ['train_ce', 'validation_ce'],
                                  ['Training CE', 'Validation CE']):
            ax.plot(epochs, [row[key] for row in history], label=name)
            ax.set(xlabel='Completed epochs', ylabel=label, yscale='log')
            ax.grid(alpha=.2)
    axes[1].legend(fontsize=8)
    fig.savefig(Path(output_dir) / 'architecture_curves.png', dpi=180)
    plt.close(fig)


def check_setup(data_root=None, split_file=None):
    """PROVIDED: load/check the data without calling the model constructors."""
    configure_cpu()
    data, splits = load_data(data_root, split_file)
    info = {'split_sizes': {name: len(indices) for name, indices in splits.items()},
            'input_shapes': {name: list(values[0].shape) for name, values in data.items()},
            'data_seed': 666}
    print('P3 setup:', json.dumps(info), flush=True)
    return info


def run(data_root=None, epochs=EPOCHS, seeds=SEEDS, out=None,
        output_dir=None, split_file=None):
    """PROVIDED: run the fixed three-model comparison and produce the figure/table."""
    if tuple(seeds) != SEEDS:
        raise ValueError('This assignment compares A, B, and C with the fixed training seed 666.')
    if output_dir is not None and out is not None:
        raise ValueError('Specify output_dir or out, not both.')
    configure_cpu()
    # Fail clearly before downloading data if a model constructor is unfinished.
    check_models(verbose=False)
    start = time.perf_counter()
    data, splits = load_data(data_root, split_file)
    folder = output_dir if output_dir is not None else out
    folder = Path(folder) if folder is not None else DEFAULT_OUT_DIR
    folder.mkdir(parents=True, exist_ok=True)
    models, histories, rows = {}, {}, []
    for spec in SPECS:
        name = spec[0]
        model, history, row, _ = train_model(spec, TRAIN_SEED, data['train'],
                                            data['validation'], epochs)
        models[name], histories[name] = model, history
        rows.append(row)
        write_csv(folder / f'{name}_history.csv', history)
        print(f"{name}: selected epoch={row['best_epoch']}, validation CE={row['validation_ce']:.4f}",
              flush=True)
    # Freeze the validation-only choice BEFORE computing any test-set metrics.
    values = {row['model']: row['validation_ce'] for row in rows}
    selected = min(values, key=values.get)
    selection = {'criterion': 'lowest validation CE at each trained model best checkpoint',
                 'validation_ce': values, 'selected_model': selected,
                 'test_metrics_used': False}
    (folder / 'selection_before_test.json').write_text(json.dumps(selection, indent=2))
    for row in rows:
        row['test_ce'], row['test_accuracy'] = evaluate(models[row['model']], *data['test'])
        row['test_accuracy_percent'] = 100 * row['test_accuracy']
    write_csv(folder / 'summary.csv', rows)
    plot_histories(histories, folder)
    manifest = {'seed_data': 666, 'training_seeds': list(SEEDS),
                'epochs': epochs, 'batch_size': BATCH_SIZE,
                'optimizer': 'SGD with Momentum', 'learning_rate': LEARNING_RATE,
                'momentum': MOMENTUM, 'weight_decay': 0, 'device': 'cpu', 'threads': 1,
                'torch': torch.__version__, 'numpy': np.__version__,
                'platform': platform.platform(),
                'split_sizes': {name: len(indices) for name, indices in splits.items()},
                'split_sha256': {name: hashlib.sha256(indices.tobytes()).hexdigest()
                                 for name, indices in splits.items()},
                'selection': selection, 'rows': rows,
                'elapsed_seconds': time.perf_counter() - start}
    (folder / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    print('Model | selected epoch | validation CE | test CE | test accuracy (%)', flush=True)
    for row in rows:
        print(f"{row['model']} | {row['best_epoch']} | {row['validation_ce']:.4f} | "
              f"{row['test_ce']:.4f} | {row['test_accuracy_percent']:.2f}", flush=True)
    print('Validation-selected model:', selected, flush=True)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, help='Override the MNIST download/cache folder.')
    parser.add_argument('--output-dir', '--out', dest='output_dir', type=Path,
                        help='Override the folder for generated figures and tables.')
    checks = parser.add_mutually_exclusive_group()
    checks.add_argument('--check-setup', action='store_true',
                        help='Download/check the fixed data without calling model constructors.')
    checks.add_argument('--check-models', action='store_true',
                        help='Check completed model shapes/counts without downloading MNIST.')
    args = parser.parse_args()
    if args.check_setup:
        check_setup(args.data_root)
    elif args.check_models:
        check_models()
    else:
        run(data_root=args.data_root, output_dir=args.output_dir)


if __name__ == '__main__':
    main()
