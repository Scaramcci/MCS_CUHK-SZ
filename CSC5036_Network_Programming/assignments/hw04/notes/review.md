# Independent revised-candidate review — 2026-11-04

Reviewer: `/root/reviewer`; neither implementation author nor this round's Verifier. Reviewed teacher requirements, original ZIP, actual revised candidate, implementation/verification records, independent test code and output, and original-suite rerun evidence. Only review records changed.

**Final readiness: Blocked on required Learner Lab execution. Local candidate checks pass; no remaining code/package fix identified in reviewed scope. This is not Ready or submission approval.**

## Inspected version

Actual candidate: `results/candidate/20261104T074144997572Z/226040255_hw4.zip`.

| File | SHA-256 | Bytes |
| --- | --- | ---: |
| ZIP | `12b0688cd6bce4012f075a532f853a144277c98cc11b00009c468a6fa4389121` | See actual archive |
| Assignment-4/chord_node.py | `4427dab102a41527aff9567d26c660fc52a868739714dde0e268d19d50b77374` | 21907 |
| Assignment-4/test_dht.py | `ea237f6b59cb24ff18edace676c0821d9e9ae9a091f4d6c0895efaca646d4d11` | 8587 |

[Audit script](../results/review-20261104-revised/audit.py) and [results](../results/review-20261104-revised/audit.json). Actual command: `python3 CSC5036_Network_Programming/assignments/hw04/results/review-20261104-revised/audit.py`, exit 0. Script loads the actual ZIP bytes, verifies names/CRC/source equivalence, compiles both Python members, compares teacher test and fixed methods byte-for-byte, and reruns the earlier isolated transfer regression. Compilation is a local syntax check, not Python 3.12 runtime validation.

## Critical issues

None found in inspected content. No credentials, unrelated artifacts or fabricated runtime claims observed in the candidate and accompanying evidence.

## Major issues and resolution

- **Resolved: repeated transfer RPC incorrectly moved successor-owned keys.** Previous candidate `dff82fdc…67dd2` failed the isolated example (node 15, predecessor 8, key hash 10). Revised code returns before treating an already-current predecessor as a new owner. Repeating the exact candidate-loaded audit now retains the key on node 15 and sends no store. The independent Verifier separately reran all prior TCP scenarios and 15 real remote transfer RPC retries across the five-node ring; dictionaries, ownership and retrieval remain correct. See [revalidation](verification.md). Old [review](../results/review-20261104-revised/previous-review.md) and [failure evidence](../results/review-20261104/audit.json) remain intact and apply only to the old candidate.
- **Still pending: required course environment.** Teacher's Required Experimental Environment mandates one AWS Academy Learner Lab t3.small, Ubuntu 24.04 AMD64 and system Python 3.12 with original ports. This has not been executed. Local Python 3.14 evidence cannot replace it. The README and candidate manifest accurately state this limitation. Run and review that environment before moving a final candidate to submission/ or marking Ready.

## Minor issues

None requiring correction. Starter framing limitations, no replication, and unverified concurrent mutation/partition guarantees are explicitly documented.

## Submission checklist

| Requirement | Review result |
| --- | --- |
| ZIP name and exactly two nested Python files | Pass; direct archive inspection, no README/log/cache/extra tests |
| Source matches independently validated revision | Pass; actual member hashes and source bytes match revised verification |
| Original test file and network/init/stop unchanged | Pass; byte comparison against original ZIP |
| Basic protocol 40, storage 40, transfer 20 | Implemented; independent local assertions cover full ID space, fingers, ownership and joins; transfer regression now passes |
| Optional recovery +20 | Implemented; independent local evidence covers adjacent failures and recovery to singleton; no lost-key replication claim |
| Original teacher suite rerun after fix | Pass locally; `results/selftest-20261104T074111219925Z/run.json` matches current code and records scope/teacher/assertions exit 0 and semantic_ok true |
| Required Learner Lab run | Pending; blocks final readiness |
| Report/screenshots | N/A: teacher requests code only |
| Upload and submission/ | Not performed; candidate appropriately remains in results/candidate/ |

No additional code repair requested for this exact revised package. Once the required cloud run is available, inspect its real results (including routing tables and ownership, not only exit status), preserve evidence, and audit the final package. Any code/package change invalidates the corresponding prior check and requires revalidation.
