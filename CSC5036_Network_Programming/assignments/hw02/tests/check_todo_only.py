#!/usr/bin/env python3
"""Match every original byte, permitting additions only after TODO comments."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--source-dir', type=Path, default=ROOT / 'src')
args = parser.parse_args()
records = {}
with zipfile.ZipFile(ROOT / 'Assignment-2.zip') as archive:
    for name in archive.namelist():
        original = archive.read(name)
        current = (args.source_dir / name).read_bytes()
        count = 0
        if name.endswith('.c'):
            parts = []
            position = 0
            for todo in re.finditer(rb'/\* TODO:.*?\*/', original, flags=re.S):
                parts.append(re.escape(original[position:todo.end()]))
                parts.append(rb'([\s\S]*?)')
                position = todo.end()
                count += 1
            parts.append(re.escape(original[position:]))
            match = re.fullmatch(b''.join(parts), current)
            assert match, f'{name}: content outside TODO locations differs'
            assert all(block.strip() for block in match.groups()), f'{name}: empty TODO'
        else:
            assert current == original, f'{name}: auxiliary file changed'
        records[name] = {
            'todo_additions': count,
            'original_sha256': hashlib.sha256(original).hexdigest(),
            'current_sha256': hashlib.sha256(current).hexdigest(),
            'outside_todo_identical': True,
        }
print(json.dumps(records, indent=2))
