# Independent candidate review — 2026-11-04

Reviewer: `/root/reviewer`; neither implementation author nor this round's Verifier. Input: root/course/role rules, teacher requirements and starter ZIP, actual candidate ZIP, plan, implementation notes, independent verification source and output. Only own review files written.

Candidate: `results/candidate/20261104T073721224466Z/226040255_hw4.zip`.
ZIP SHA-256: `dff82fdcec7f0266bcf166bc5d31d02aad3bf75b47752fcc62bcd7c4dd367dd2`.
Code SHA-256: `6c03bb4a0e7309401a4e08a0cc6a145e57347d0bebae3decbcd0b725b561d632`.
Teacher test SHA-256: `ea237f6b59cb24ff18edace676c0821d9e9ae9a091f4d6c0895efaca646d4d11`.

## Critical issues

None found in inspected content: no credentials, irrelevant artifacts, fabricated outputs or changed teacher network/test code in the package.

## Major issues

1. **Repeated transfer RPC moves keys to the wrong owner.** In `transfer_keys`, `start` is the current predecessor ID. Once the new node is already predecessor, a subsequent `transfer_keys(new_node_addr)` creates `(new,new]`, which `in_interval` correctly treats as the entire ring. This then incorrectly sends every remaining successor-owned key to the predecessor. Example: node 15, predecessor 8, hash-10 key `review-23`; repeated transfer to 8 deletes that key from 15 and stores it on 8. The ordinary `notify` caller filters duplicate notifications, but the provided public `transfer_keys` RPC does not. This violates Part 2's transfer-only-new-owner-keys requirement for repeated calls. Add an ownership/idempotence guard and independently reverify; old candidate is superseded after changes.
2. **Required course execution missing.** Learner Lab t3.small / Ubuntu 24.04 AMD64 / system Python 3.12 has not been run. Local Python 3.14 evidence is accurately marked supplementary. Even after code fix, readiness remains blocked until that run is complete and reviewed.

Reproduction: `python3 CSC5036_Network_Programming/assignments/hw04/results/review-20261104/audit.py`, exit 0 means the audit successfully reproduced the defect (not correctness). [audit.py](../results/review-20261104/audit.py) reads code from the actual ZIP and uses a socket-free Node instance and a recording store stub to isolate the transfer decision; it is not presented as a real TCP test. [audit.json](../results/review-20261104/audit.json) contains original package hashes, static results and exact wrong transfer.

## Minor issues

None requiring changes. Known starter single-recv framing and unsupported concurrent mutation limitations are candidly documented and not claimed as solved.

## Submission checklist

| Requirement | Result |
| --- | --- |
| ID ZIP name, exactly two correctly nested Python files | Pass; archive CRC and list checked directly |
| Completed methods, standard library only | Present; no test-specific hard-coding observed |
| Original test and network/init/stop methods unchanged | Pass; independent byte comparison from actual ZIP |
| Matches independently tested source version | Pass; all source member bytes match working files and verifier hashes |
| Base protocol/storage/joins and bonus failures | Local verifier assertions support tested scope; repeat transfer defect remains |
| Mandatory course environment | Pending; no Ready claim allowed |
| Report, screenshots, logs omitted | Pass; not required by teacher |
| Final submission directory | Intentionally absent pending required checks; candidate retained under results |

## Final readiness

**Not ready: repeat-transfer code fix required.** Separately blocked on required EC2 access/execution. This is an independent review of the exact local candidate above, not teacher approval or upload. Return to Implementer → independent Verifier → rebuild candidate → independent Reviewer; preserve old evidence. If the implementation changes, the prior source validation and this package review cannot approve the new bytes.
