#!/usr/bin/env python3
"""Real loopback processes; synthetic query names only, never submitted."""
import hashlib
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'src/Assignment-3'
RUN = ROOT / 'results' / ('selftest-' + time.strftime('%Y%m%dT%H%M%S'))
RUN.mkdir(parents=True)


def wait_for(predicate, description, timeout=6):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if predicate():
            return
        time.sleep(.02)
    raise AssertionError(description)


class Network:
    def __init__(self, name, ttls, edges):
        self.path = RUN / name
        self.path.mkdir()
        self.procs, self.lines, self.threads, self.ports = [], [], [], []
        held = []
        for _ in ttls:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('127.0.0.1', 0))
            self.ports.append(sock.getsockname()[1])
            held.append(sock)
        for sock in held:
            sock.close()
        self.commands = []
        try:
            for i, ttl in enumerate(ttls):
                args = ['stdbuf', '-oL', './p2p_server', str(self.ports[i]), str(ttl), f'dir{i+1}']
                for neighbor in edges[i]:
                    args += ['127.0.0.1', str(self.ports[neighbor])]
                self.commands.append(args)
                lines = []
                self.lines.append(lines)
                proc = subprocess.Popen(args, cwd=SRC, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT, text=True, bufsize=1)
                self.procs.append(proc)
                def read(p=proc, out=lines):
                    for line in p.stdout:
                        out.append(line)
                thread = threading.Thread(target=read, daemon=True)
                thread.start()
                self.threads.append(thread)
                wait_for(lambda: '[FILE] Enter' in ''.join(lines), f'node {i} ready')
                for neighbor in edges[i]:
                    expected = f'From address: 127.0.0.1:{self.ports[i]}'
                    wait_for(lambda j=neighbor: expected in self.text(j), f'CONNECT {i}->{neighbor}')
        except BaseException:
            self.close()
            raise

    def text(self, i):
        return ''.join(self.lines[i])

    def clear(self):
        time.sleep(.15)
        return [len(x) for x in self.lines]

    def since(self, marks, i):
        return ''.join(self.lines[i][marks[i]:])

    def query(self, i, name):
        self.procs[i].stdin.write(name + '\n')
        self.procs[i].stdin.flush()

    def close(self):
        for proc in self.procs:
            proc.terminate()
        for proc in self.procs:
            proc.wait(timeout=3)
        for thread in self.threads:
            thread.join(timeout=2)
        for i, lines in enumerate(self.lines):
            (self.path / f'node{i+1}.txt').write_text(''.join(lines))
        (self.path / 'commands.json').write_text(json.dumps({
            'cwd': str(SRC.relative_to(ROOT)), 'commands': self.commands,
            'shutdown': 'SIGTERM after assertions', 'returncodes': [p.returncode for p in self.procs]
        }, indent=2))


checks = []
try:
    build = subprocess.run(['make', '-C', str(SRC)], text=True, capture_output=True)
    (RUN / 'build.txt').write_text(build.stdout + build.stderr)
    assert build.returncode == 0
    checks.append('original Makefile C17 build')
    net = Network('chain-ttl1', [1, 2, 2, 2], [[], [0], [1], [2]])
    try:
        net.query(2, 'file1')
        wait_for(lambda: f'File file1 found on address 127.0.0.1, with port {net.ports[0]}' in net.text(2), 'two-hop reverse lookup')
        marks = net.clear()
        net.query(0, 'file5')
        wait_for(lambda: '[TTL] Packet TTL expired' in net.since(marks, 1), 'TTL1 expires at Bob')
        time.sleep(.3)
        assert 'QUERY packet' not in net.since(marks, 2)
        assert 'QUERY packet' not in net.since(marks, 3)
        assert 'RESPONSE packet' not in net.since(marks, 0)
        marks = net.clear()
        net.query(0, 'file1')
        wait_for(lambda: "Found file 'file1' in local directory" in net.since(marks, 0), 'local lookup')
        assert 'QUERY packet' not in net.since(marks, 1)
        checks += ['two-hop response with holder IP/port', 'TTL1 stops at immediate neighbor', 'local lookup']
    finally:
        net.close()
    net = Network('chain-ttl3', [3, 2, 2, 2], [[], [0], [1], [2]])
    try:
        net.query(0, 'file5')
        wait_for(lambda: f'File file5 found on address 127.0.0.1, with port {net.ports[3]}' in net.text(0), 'TTL3 reaches David')
        assert 'Forwarding packet with TTL=2' in net.text(1)
        assert 'Forwarding packet with TTL=1' in net.text(2)
        assert '[RESPON] File file5 found' in net.text(3)
        checks.append('TTL3 three-hop hit, local search before TTL expiry')
    finally:
        net.close()
    net = Network('triangle', [64, 2, 2], [[], [0], [1, 0]])
    try:
        marks = net.clear()
        net.query(0, 'missing_file')
        wait_for(lambda: all('[DUPLICATE ID]' in net.since(marks, i) for i in (1, 2)), 'triangle duplicates discarded')
        time.sleep(.3)
        for i in (1, 2):
            assert net.since(marks, i).count('[TTL] Forwarding') == 1
        before = [len(x) for x in net.lines]
        time.sleep(.3)
        assert before == [len(x) for x in net.lines], 'traffic quiesces'
        assert all('[TTL] Packet TTL expired' not in net.since(marks, i) for i in range(3))
        checks.append('triangle processes each ID once and quiesces before TTL expiry')
    finally:
        net.close()
    net = Network('five-node-concurrent', [8]*5, [[], [0], [1, 0], [2, 0], [3, 1]])
    try:
        # Simultaneous local-origin sends and server receives at all five nodes.
        targets = ['file7', 'file4', 'file1', 'file3', 'file5']
        for i, target in enumerate(targets):
            net.query(i, target)
        for i, target in enumerate(targets):
            wait_for(lambda i=i, target=target: f'File {target} found on address' in net.text(i), f'concurrent response {i}')
        checks.append('five-node concurrent searches and bidirectional CONNECT')
    finally:
        net.close()
    status = 'passed'
except BaseException as exc:
    status = 'failed'
    checks.append(repr(exc))
    raise
finally:
    (RUN / 'summary.json').write_text(json.dumps({
        'status': status, 'checks': checks, 'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'command': 'python3 tests/integration.py', 'platform': platform.platform(),
        'python': platform.python_version(), 'machine': platform.machine(),
        'compiler': subprocess.check_output(['gcc', '--version'], text=True).splitlines()[0],
        'make': subprocess.check_output(['make', '--version'], text=True).splitlines()[0],
        'sources_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in SRC.iterdir() if p.suffix in ('.c', '.h') or p.name == 'Makefile'},
        'original_zip_sha256': hashlib.sha256((ROOT/'Assignment-3.zip').read_bytes()).hexdigest(),
        'randomness': 'starter time/PID seeded query IDs; ports allocated by OS',
    }, indent=2))
    print(status, RUN.relative_to(ROOT))
    for check in checks:
        print('-', check)
