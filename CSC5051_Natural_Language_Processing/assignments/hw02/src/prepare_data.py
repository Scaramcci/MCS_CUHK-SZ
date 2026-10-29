"""Deterministic real-data splits and explicitly synthetic defect diagnostics."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA256 = '0bd4f62585d494b794deb043ce0baddfec02f27696857c57c9c238d6eff35a18'
SEED = 20261028
DEFECTS = ('empty', 'off_topic', 'instruction_echo', 'excessive_repetition')
STOP = set('the a an is are to of in on and or for with that this it be as by you your'.split())


def words(text):
    return set(re.findall(r'[a-z]{3,}', text.lower())) - STOP


def eligible(row):
    if not all(isinstance(row.get(k), str) for k in ('instruction', 'input', 'output')):
        return False
    text = row['instruction'] + ' ' + row['input']
    return (20 <= len(row['instruction']) <= 400 and len(row['input']) <= 600
            and 60 <= len(row['output']) <= 800
            and len(text) + len(row['output']) <= 1400
            and sum(c.isascii() for c in text + row['output']) / len(text + row['output']) >= .95
            and not re.search(r'\b(repeat|repetition|echo|copy|nothing|blank|empty|silence)\b', row['instruction'], re.I))


def encode_rows(rows):
    return ''.join(json.dumps(r, ensure_ascii=False, sort_keys=True) + '\n' for r in rows).encode()


def write_frozen(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != content:
        raise ValueError('Refusing to replace a frozen dataset: ' + str(path))
    if not path.exists():
        path.write_bytes(content)
    return hashlib.sha256(content).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'data/raw/alpaca_gpt4_data.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'data/processed')
    args = parser.parse_args()
    raw = args.source.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('Source fingerprint differs from pinned download')
    data = json.loads(raw)
    pool = [i for i, row in enumerate(data) if eligible(row)]
    # Deduplicate base instruction/input pairs before sampling.
    seen, unique = set(), []
    for i in pool:
        k = (data[i]['instruction'].strip(), data[i]['input'].strip())
        if k not in seen:
            seen.add(k)
            unique.append(i)
    rng = random.Random(SEED)
    chosen = rng.sample(unique, 40)
    assert len(set(chosen)) == 40
    metadata = {'seed': SEED, 'source_sha256': SOURCE_SHA256, 'source_count': len(data),
                'eligible_unique_count': len(unique), 'source_commit': '38b93b75a80b019cc3aad362ca6f5bb0c3908959',
                'design': 'Unaltered originals have no gold quality labels. Corruptions are synthetic diagnostics, not natural defects.',
                'eligibility': 'instruction20..400chars, input<=600, output60..800, combined<=1400, >=95%ASCII; exclude repeat/echo/copy/nothing/blank/empty/silence instructions; deduplicate instruction/input',
                'source_indices': {'dev': chosen[:8], 'test': chosen[8:]}, 'files': {}}
    for split, indices in [('dev', chosen[:8]), ('test', chosen[8:])]:
        rows = []
        for j, index in enumerate(indices):
            original = data[index]
            base = f'alpaca-{index:05d}'
            row = {k: original[k] for k in ('instruction', 'input', 'output')}
            rows.append(dict(row, id=base + '-original', base_id=base, variant='unaltered', defect=None, source_index=index, split=split))
            defect = DEFECTS[j % len(DEFECTS)]
            corrupted = dict(row, id=base + '-diagnostic', base_id=base, variant='synthetic_corruption', defect=defect, source_index=index, split=split)
            if defect == 'empty':
                corrupted['output'] = ''
            elif defect == 'instruction_echo':
                corrupted['output'] = original['instruction'] + ('\n' + original['input'] if original['input'] else '')
            elif defect == 'excessive_repetition':
                corrupted['output'] = '\n\n'.join([original['output']] * 4)
            else:
                task_words = words(original['instruction'] + ' ' + original['input'])
                candidates = [i for i in unique if i not in chosen and not task_words.intersection(words(data[i]['output']))]
                donor = rng.choice(candidates)
                corrupted['output'] = data[donor]['output']
                corrupted['donor_source_index'] = donor
            rows.append(corrupted)
        rng.shuffle(rows)
        digest = write_frozen(args.output / (split + '.jsonl'), encode_rows(rows))
        metadata['files'][split] = {'sha256': digest, 'records': len(rows), 'variants': dict(Counter(r['variant'] for r in rows)), 'defects': dict(Counter(r['defect'] for r in rows if r['defect']))}
        if split == 'dev':
            # Four full pairs: one example of each defect, exclusively development.
            pilot_bases = {f'alpaca-{i:05d}' for i in indices[:4]}
            pilot = [r for r in rows if r['base_id'] in pilot_bases]
            metadata['files']['pilot'] = {'sha256': write_frozen(args.output / 'pilot.jsonl', encode_rows(pilot)), 'records': len(pilot)}
    assert not set(chosen[:8]).intersection(chosen[8:])
    metadata['preparation_script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    write_frozen(args.output / 'manifest.json', (json.dumps(metadata, indent=2, ensure_ascii=False) + '\n').encode())
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
