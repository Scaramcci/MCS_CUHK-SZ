from pathlib import Path
from zipfile import ZipFile
import re

ROOT = Path(__file__).resolve().parents[1]
with ZipFile(ROOT / 'requirements/Assignment-4.zip') as archive:
    original = archive.read('Assignment-4/chord_node.py')
    actual = (ROOT / 'src/Assignment-4/chord_node.py').read_bytes()
    parts = original.split(b'        raise NotImplementedError')
    assert len(parts) == 14
    position = 0
    for i, part in enumerate(parts):
        if i == 13:
            prefix, network = part.split(b'    # ========================================================================\r\n    # Network Communication', 1)
            assert actual.find(prefix, position) >= position
            assert actual.endswith(b'    # ========================================================================\r\n    # Network Communication' + network)
        else:
            location = actual.find(part, position)
            assert location >= position, f'Starter segment {i} modified'
            if i == 0:
                assert location == 0
            position = location + len(part)
    assert archive.read('Assignment-4/test_dht.py') == (ROOT / 'src/Assignment-4/test_dht.py').read_bytes()
    assert b'raise NotImplementedError' not in actual
print('PASS: all starter fixed segments and original test bytes preserved; 13 TODO bodies replaced, helpers added')
