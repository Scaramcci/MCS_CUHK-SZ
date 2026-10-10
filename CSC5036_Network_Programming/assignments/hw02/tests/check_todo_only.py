#!/usr/bin/env python3
"""Prove that removing additions immediately after TODO comments restores the ZIP bytes."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
records = {}
with zipfile.ZipFile(ROOT / 'Assignment-2.zip') as archive:
    for name in archive.namelist():
        original = archive.read(name)
        current = (ROOT / 'src' / name).read_bytes()
        if name.endswith('.c'):
            pattern = rb'(/\* TODO:.*?\*/)(?:\r\n|\n)/\* BEGIN TODO IMPLEMENTATION \*/.*?/\* END TODO IMPLEMENTATION \*/'
            restored, count = re.subn(pattern, lambda m: m.group(1), current, flags=re.S)
            assert count == len(re.findall(rb'/\* TODO:', original)), name
            assert restored == original, f'{name}: bytes outside TODO additions changed'
        else:
            count = 0
            assert current == original, f'{name}: provided auxiliary file changed'
        records[name] = {'todo_additions': count, 'original_sha256': hashlib.sha256(original).hexdigest(),
                         'current_sha256': hashlib.sha256(current).hexdigest(), 'outside_todo_identical': True}
print(json.dumps(records, indent=2))
