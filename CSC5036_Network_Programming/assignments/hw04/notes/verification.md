# Independent verification — revised source, 2026-11-04

Executor: `/root/verifier`, independent of implementation and Reviewer. **Supplementary local revalidation passed; required Learner Lab execution remains pending.**

Current source SHA-256: `4427dab102a41527aff9567d26c660fc52a868739714dde0e268d19d50b77374`. The earlier source was superseded after Reviewer identified an untested repeated-transfer RPC ownership defect. Earlier evidence and [previous verification record](../results/verification-20261104-repeat-transfer/previous-verification.md) are preserved; they do not approve the new source.

## Revalidation

[Independent test](../results/verification-20261104-repeat-transfer/verify.py), [raw output](../results/verification-20261104-repeat-transfer/output.txt), [environment/check summary](../results/verification-20261104-repeat-transfer/summary.json), [exact command, hashes and exit status](../results/verification-20261104-repeat-transfer/execution.json). Run exited 0, source hash unchanged before/after. Normal socket permission approval succeeded; no approval mechanism was bypassed.

All prior scenarios rerun: byte-identical provided methods/test; 65,536 interval assertions; singleton and 31→0→16→7→26 joins; every 32-ID lookup, all finger entries and neighbor state; 64 keys covering every hash with exact unique ownership and all-node retrieval; missing key and False overwrite; two adjacent failures; further recovery to singleton.

New regression: on the stabilized five-node ring, each node receives three real TCP `transfer_keys` RPCs from another node with its existing predecessor as target (15 RPCs total). All calls acknowledge success, the complete per-node dictionaries remain identical, and subsequent ownership/all-node retrieval assertions pass. This directly covers the Reviewer's failure using the unmodified provided remote dispatch, including wraparound predecessor pairs.

## Failed checks / required fixes

None in this revised run. The repeated-transfer defect is fixed for the tested public RPC scenario. No source/test/package files were changed by Verifier.

## Outstanding work and scope

Required Learner Lab t3.small / Ubuntu 24.04 AMD64 / system Python 3.12 run is not executed. Local environment remains Anaconda Python 3.14.7 on Linux x86_64. Thus no Ready claim. Tests are deterministic aside from TCP ephemeral ports/scheduling and use small JSON values. Original single-recv framing limitations, concurrent join/put linearizability, arbitrary partitions and unlimited failure patterns remain outside verified guarantees; failed-node data replication is explicitly out of scope.

Next: rebuild the candidate from these frozen bytes and ask the separate Reviewer to audit the new actual ZIP and regression evidence. Keep required-course-environment pending until actual execution.

## Additional original-suite rerun

At root's request, this independent executor also ran `python3 CSC5036_Network_Programming/assignments/hw04/tests/run_checks.py` from repository root through normal socket permission approval. Exit 0; [run.json](../results/selftest-20261104T074111219925Z/run.json) records the current source hash, environment, all child commands and semantic checks. Original unchanged teacher suite, scope check and author supplementary regression suite all passed (`exit=0`, `semantic_ok=true`). [Teacher raw output](../results/selftest-20261104T074111219925Z/teacher.txt) and [assertion output](../results/selftest-20261104T074111219925Z/assertions.txt) retained. This is additional execution evidence, not a replacement for the independently designed checks above.
