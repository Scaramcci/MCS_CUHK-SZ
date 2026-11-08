"""Local supplementary checks; does not replace the required Learner Lab run."""
import hashlib
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/Assignment-4'))
from chord_node import Node

nodes = []
def addr(n): return (n.node_id, n.host, n.port)
def add(identifier):
    n = Node(identifier, '127.0.0.1', 0)
    nodes.append(n)
    deadline = time.monotonic() + 3
    while n.server.getsockname()[1] == 0:
        assert time.monotonic() < deadline
        time.sleep(.01)
    n.port = n.server.getsockname()[1]
    # port=0 is only used in supplementary tests; reset startup self addresses.
    n.create()
    return n

def settle(live):
    for _ in range(max(12, len(live) * 3)):
        for n in live:
            n.stabilize()
            n.fix_fingers()

def owner(live, identifier):
    ordered = sorted(live, key=lambda n: n.node_id)
    return next((n for n in ordered if n.node_id >= identifier), ordered[0])

def routing(live):
    ordered = sorted(live, key=lambda n: n.node_id)
    for i, n in enumerate(ordered):
        assert n.successor == addr(ordered[(i+1)%len(ordered)]), (n.node_id, n.successor)
        if len(live) > 1:
            assert n.predecessor == addr(ordered[i-1]), (n.node_id, n.predecessor)
        for identifier in range(n.max_id):
            assert tuple(n.find_successor(identifier)) == addr(owner(live, identifier))
        for index in range(1, n.m+1):
            assert tuple(n.finger[index]) == addr(owner(live, (n.node_id+2**(index-1)) % n.max_id))

def storage(live, expected):
    for key, value in expected.items():
        identifier = int(hashlib.sha1(key.encode()).hexdigest(), 16) % 32
        responsible = owner(live, identifier)
        assert [n.node_id for n in live if key in n.data] == [responsible.node_id], key
        for n in live:
            assert n.get(key) == value, (n.node_id, key)

try:
    n = add(17)
    for start in range(32):
        for end in range(32):
            walk = [(start+i)%32 for i in range(1, ((end-start)%32 or 32)+1)]
            for identifier in range(32):
                assert n.in_interval(identifier,start,end) == (identifier in walk)
                assert n.in_interval(identifier,start,end,False) == (identifier in walk[:-1])
    settle([n]); routing([n])
    expected = {f'key-{i}': {'value': i} for i in range(96)}
    for key, value in expected.items(): assert n.put(key,value)
    storage([n], expected)
    live = [n]
    for identifier in [3, 29, 11, 24, 0]:
        joined = add(identifier)
        joined.join(addr(live[-1]))
        live.append(joined)
        settle(live); routing(live); storage(live,expected)
        successor = next(peer for peer in live if addr(peer) == joined.successor)
        before = {peer.node_id: dict(peer.data) for peer in live}
        for _ in range(2):
            successor.remote_call(addr(successor), 'transfer_keys', {
                'node_id': joined.node_id, 'host': joined.host, 'port': joined.port})
        assert before == {peer.node_id: dict(peer.data) for peer in live}
        storage(live, expected)
        print('PASS join / full identifier routing / ownership:', identifier, flush=True)
    assert n.get('absent') is None
    assert live[-1].put('key-0', 'replacement')
    expected['key-0'] = 'replacement'
    storage(live,expected)
    for failed in [n, live[1], live[-1]]:
        lost = set(failed.data)
        failed.stop(); failed.server_thread.join(2)
        live.remove(failed)
        expected = {k:v for k,v in expected.items() if k not in lost}
        for survivor in live: survivor.check_predecessor()
        settle(live); routing(live); storage(live,expected)
        print('PASS failure recovery:', failed.node_id, flush=True)
    print('PASS all supplementary assertions')
finally:
    for n in nodes:
        if not n.stopped: n.stop()
    for n in nodes: n.server_thread.join(2)
