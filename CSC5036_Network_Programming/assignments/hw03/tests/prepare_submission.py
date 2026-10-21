#!/usr/bin/env python3
"""Assemble only teacher-listed files; refuse to overwrite an existing candidate."""
import hashlib
import json
from pathlib import Path
import sys
import time
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
student_id = sys.argv[1]
if not student_id.isdigit():
    raise SystemExit('Student ID must contain digits only')
source = root / 'src'
output = root / 'submission' / f'{student_id}_hw3.zip'
if output.exists():
    raise SystemExit('Candidate already exists; archive and re-verify before replacing')
output.parent.mkdir(exist_ok=True)
manifest = []
changed = []
with ZipFile(root / 'Assignment-3.zip') as original:
    entries = original.namelist()
    for name in entries:
        data = (source / name).read_bytes()
        if data != original.read(name):
            changed.append(name)
        manifest.append({'path': name, 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    assert set(changed) == {f'Assignment-3/{name}.c' for name in ('main', 'server', 'utils')}, changed
    with ZipFile(output, 'x', compression=ZIP_DEFLATED) as package:
        for name in entries:
            package.write(source / name, name)
with ZipFile(output) as package:
    assert package.namelist() == entries
    for entry in manifest:
        assert hashlib.sha256(package.read(entry['path'])).hexdigest() == entry['sha256']
evidence = root / 'results' / ('package-' + time.strftime('%Y%m%dT%H%M%S') + '.json')
evidence.write_text(json.dumps({
    'executor': '/root, assembly only; independent Reviewer verdict is separate',
    'time': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
    'command': f'python3 tests/prepare_submission.py {student_id}',
    'exit_status': 0,
    'original_zip_sha256': hashlib.sha256((root/'Assignment-3.zip').read_bytes()).hexdigest(),
    'submission': str(output.relative_to(root)),
    'submission_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
    'changed_from_teacher': changed,
    'entries': manifest,
}, indent=2))
print(output.relative_to(root))
print('SHA-256', hashlib.sha256(output.read_bytes()).hexdigest())
print('Entries', len(entries), '; evidence', evidence.relative_to(root))
