# Independent verification — 2026-11-04

Executor: `/root/verifier`, an independent child agent that did not implement the code or its development tests. Only this verification record and `results/verification-20261104/` were written. Source, teacher files and package were not modified. Input: root/role/course rules, `notes/plan.md`, teacher requirements and starter ZIP, frozen implementation.

**Conclusion: supplementary local verification passed for the checks below. Required Learner Lab execution remains pending; this is not a Ready or submission approval.**

Code SHA-256: `6c03bb4a0e7309401a4e08a0cc6a145e57347d0bebae3decbcd0b725b561d632`; checked unchanged after execution. Full input/test hashes, exact command and exit status 0 are in [execution.json](../results/verification-20261104/execution.json). Local environment is Linux x86_64, Anaconda Python 3.14.7, glibc 2.43; see [summary.json](../results/verification-20261104/summary.json). No dependencies beyond standard library. Deterministic IDs/key generation, no PRNG; ephemeral TCP ports and scheduling vary.

## Passed checks

Independent test: [verify.py](../results/verification-20261104/verify.py), real raw output: [output.txt](../results/verification-20261104/output.txt).

- Original `__init__`, `remote_call`, `run_server`, `handle_client`, `stop` source bytes and entire `test_dht.py` match the original ZIP. Reviewed new implementation: no global node registry, no test-node/key special cases, no example output hard-coding.
- All 65,536 combinations of 32 start/end/query IDs and two endpoint conventions, including equal endpoints. Independent piecewise interval oracle.
- Singleton initialization and storage of 64 deterministic keys covering all 32 key hashes twice.
- Sequential joins in order 31 → 0 → 16 → 7 → 26 (including wraparound and joins below/above existing IDs). After stabilization, every node's full 32-ID lookup space, all five finger entries, predecessor/successor, exact single-owner placement of every key, and retrieval from every node match a sorted-ring/SHA-1 oracle.
- Missing key retrieval and overwrite with a falsy JSON value (`False`).
- Simultaneous adjacent failures of nodes 7 and 16: converged successor/predecessor/fingers and all-ID lookup are correct, surviving keys retained and retrievable. Keys held only by failed nodes deliberately excluded per teacher's no-replication scope.
- Further failures reducing the ring to two nodes and then one: full routing and surviving-data checks pass.

## Failed checks / required fixes

None in the executed scope. No source fixes requested.

## Warnings and outstanding work

- Mandatory course environment (`Required Experimental Environment`): one AWS Academy Learner Lab t3.small, Ubuntu 24.04 AMD64, system Python 3.12, original ports. **Not executed here**. Local Python 3.14 tests do not substitute for it.
- The frozen starter transport performs a single `recv(4096)` and has no message framing; large JSON/partial-frame and arbitrary concurrent mutation guarantees are not claimed. Tests use small JSON messages, sequential joins and periodic maintenance.
- Transfer code snapshots the local dictionary and acknowledges store before deletion; it does not provide linearizable writes during simultaneous joins/puts because original store dispatch has no locking. This was identified by review, not exercised as a promised guarantee.
- No complete-network-partition, arbitrary failure scheduling or adversarial network correctness guarantee is established. The checked bonus failure patterns are as listed above.
- Independent final Reviewer must inspect the exact candidate ZIP and preserve the pending-environment status. This verifier did not inspect or approve a package. Root should run the required environment and repeat affected checks if code changes.
