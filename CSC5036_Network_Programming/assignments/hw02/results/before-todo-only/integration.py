#!/usr/bin/env python3
"""Local integration checks; generated random bytes are test data only."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import hashlib
import json
import os
import platform
import signal
import socket
import subprocess
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src'
BUILD = SRC / 'build'
RUN = ROOT / 'results' / time.strftime('%Y%m%d-%H%M%S', time.gmtime())
RUN.mkdir(parents=True, exist_ok=False)
DATA = ROOT / 'data' / 'raw' / RUN.name
DATA.mkdir(parents=True)
EVENTS = []

def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def command(args, cwd, label, timeout=90):
    result = subprocess.run(args, cwd=cwd, capture_output=True, timeout=timeout)
    (RUN / (label + '-stdout.txt')).write_bytes(result.stdout)
    (RUN / (label + '-stderr.txt')).write_bytes(result.stderr)
    EVENTS.append({'command': args, 'cwd': str(cwd), 'exit': result.returncode})
    assert result.returncode == 0, (label, result.returncode, result.stderr.decode(errors='replace'))
    return result.stdout

def connect():
    return socket.create_connection(('127.0.0.1', 8080), timeout=10)

@contextmanager
def server(name, directory):
    with (RUN / (name + '-stdout.txt')).open('wb') as out, (RUN / (name + '-stderr.txt')).open('wb') as err:
        proc = subprocess.Popen([str(BUILD / name)], cwd=directory, stdout=out, stderr=err)
        EVENTS.append({'server': name, 'pid': proc.pid, 'cwd': str(directory)})
        try:
            for _ in range(100):
                assert proc.poll() is None, f'{name} exited before ready'
                try:
                    with connect(): pass
                    break
                except ConnectionRefusedError:
                    time.sleep(.05)
            else:
                raise AssertionError('Server readiness timeout')
            yield proc
            assert proc.poll() is None, f'{name} unexpectedly exited'
        finally:
            if proc.poll() is None:
                proc.send_signal(signal.SIGINT)
                try: proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill(); proc.wait()
            EVENTS.append({'server': name, 'termination': proc.returncode})

def exact(s, size):
    data = bytearray()
    while len(data) < size:
        chunk = s.recv(size - len(data))
        assert chunk, 'Early EOF'
        data.extend(chunk)
    return bytes(data)

def echo(payload):
    with connect() as s:
        s.sendall(payload)
        s.shutdown(socket.SHUT_WR)
        assert exact(s, len(payload)) == payload
        assert s.recv(1) == b''

def finished(s):
    s.shutdown(socket.SHUT_WR)
    assert s.recv(1) == b''

def header(name):
    return name.encode().ljust(1024, b'\0')

try:
    command(['cmake', '-S', str(SRC), '-B', str(BUILD), '-DCMAKE_C_FLAGS=-Wall -Wextra -Wpedantic -Werror'], ROOT, 'configure')
    command(['cmake', '--build', str(BUILD), '--clean-first'], ROOT, 'build')
    with server('socket_server', BUILD) as proc:
        command([str(BUILD / 'socket_client')], BUILD, 'single-echo')
        command(['bash', str(SRC / 'con.sh')], BUILD, 'provided-concurrent-echo')
        echo(bytes(range(256)) * 256)
        with ThreadPoolExecutor(max_workers=30) as pool:
            list(pool.map(echo, [bytes([i]) * (1024 + i) for i in range(30)]))
        for _ in range(40):
            with connect(): pass
        echo(b'still alive after disconnections')
        print('PASS: single, provided 30-client script, binary echo, 30 concurrent exact echoes, disconnect/reuse', flush=True)
    # Original generator produces 5 x 10,000,000 and 2 x 50,000,000 random bytes.
    command(['bash', str(SRC / 'generator.sh')], DATA, 'provided-generator')
    for path in sorted(DATA.glob('*.zip')):
        EVENTS.append({'input': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path), 'purpose': 'synthetic random transfer test'})
    with server('file_server', BUILD) as proc:
        command([str(BUILD / 'file_client'), str(DATA / 'file1.zip')], BUILD, 'single-file')
        assert digest(DATA / 'file1.zip') == digest(BUILD / 'file1.zip')
        # Same script; replace only its documented configurable input directory.
        script = (SRC / 'con_file.sh').read_text().replace('FILE_DIR=".."', 'FILE_DIR=' + json.dumps(str(DATA)))
        (RUN / 'con_file-test.sh').write_text(script)
        command(['bash', str(RUN / 'con_file-test.sh')], BUILD, 'provided-concurrent-files')
        for path in sorted(DATA.glob('*.zip')):
            target = BUILD / path.name
            assert path.stat().st_size == target.stat().st_size
            assert digest(path) == digest(target), path.name
            EVENTS.append({'received': str(target), 'bytes': target.stat().st_size, 'sha256': digest(target)})
        with connect() as slow:
            h = header('fragmented.bin')
            slow.sendall(h[:7])
            # A header split across packets must not stall another connection.
            empty = DATA / 'empty.bin'
            empty.write_bytes(b'')
            command([str(BUILD / 'file_client'), str(empty)], BUILD, 'empty-during-slow-header', timeout=5)
            assert (BUILD / 'empty.bin').read_bytes() == b''
            for start in range(7, 1024, 13): slow.sendall(h[start:start + 13])
            payload = bytes(range(256)) * 31
            for start in range(0, len(payload), 19): slow.sendall(payload[start:start + 19])
            finished(slow)
            assert (BUILD / 'fragmented.bin').read_bytes() == payload
        with connect() as s:
            payload = b'header and data in a single send\x00' * 200
            s.sendall(header('coalesced.bin') + payload)
            finished(s)
        assert (BUILD / 'coalesced.bin').read_bytes() == payload
        with connect() as s:
            s.sendall(b'incomplete')
        with connect() as s:
            s.sendall(header('../escape.bin'))
            finished(s)
        assert not (SRC / 'escape.bin').exists()
        command([str(BUILD / 'file_client'), str(DATA / 'file2.zip')], BUILD, 'file-after-invalid-peer')
        assert digest(DATA / 'file2.zip') == digest(BUILD / 'file2.zip')
        print('PASS: provided 5 small + 2 large concurrent files, SHA-256, fragmented/coalesced headers, empty file, slow sender, invalid peer recovery', flush=True)
    for name, args in [('socket_client', []), ('file_client', [str(DATA / 'file1.zip')])]:
        result = subprocess.run([str(BUILD / name), *args], cwd=BUILD, capture_output=True, timeout=10)
        assert result.returncode != 0
        (RUN / (name + '-no-server-stderr.txt')).write_bytes(result.stderr)
        EVENTS.append({'case': name + '-no-server', 'exit': result.returncode})
    print('PASS: clients report connection failure with nonzero exit', flush=True)
    status = 'PASS'
except BaseException:
    status = 'FAIL'
    (RUN / 'failure.txt').write_text(traceback.format_exc())
    raise
finally:
    metadata = {
        'status': status, 'executor': 'Codex implementer self-test (not independent verification)',
        'utc_run_id': RUN.name, 'command': 'python3 tests/integration.py',
        'platform': platform.platform(), 'python': platform.python_version(),
        'cpu': platform.processor(), 'events': EVENTS,
        'code_sha256': {x.name: digest(x) for x in SRC.iterdir() if x.is_file()},
        'original_zip_sha256': digest(ROOT / 'Assignment-2.zip'),
        'gcc': subprocess.getoutput('gcc --version'), 'cmake': subprocess.getoutput('cmake --version'),
        'data_note': 'generator.sh uses /dev/urandom; original generated inputs are retained under this run. No fixed seed.'
    }
    (RUN / 'run.json').write_text(json.dumps(metadata, indent=2))
    print('Evidence:', RUN, flush=True)
