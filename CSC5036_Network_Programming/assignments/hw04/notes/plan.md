# hw04 plan / research

Planner / researcher: root session, 2026-11-04. Input: repository 929bf81, clean master; no course/assignment AGENTS or existing hw04 README. Original requirements are requirements/Assignment-4.md and all three ZIP members (read fully). ZIP README additionally has a reference-implementation statement, attributes the successor-list suggestion to the Chord paper, and says teaching staff instead of TA; task requirements agree. Work remains on master by user instruction. Direct execution of all local phases is authorized. Internal notes follow repository notes/ convention.

## Requirements and acceptance

| Source section | Deliverable / acceptance |
| --- | --- |
| Part 1, methods 1–8; Grading Basic 40 | Only fill chord_node.py TODO bodies plus permitted helpers. Exhaustive ring interval and lookup checks; successor, predecessor and each finger match sorted ring oracle. |
| Part 2, methods 9–12; Storage 40, Transfers 20 | SHA-1 modulo ring size; route put/get; transfer only newly assigned keys and delete only after successful store. Assert missing keys, overwrites, all-node retrieval, exact ownership before/after joins including wraparound. |
| Part 3; Bonus 20 | Ping predecessor; select live successor backups and refresh stale fingers. Verify survivor routing, without claiming recovery of failed node's unreplicated data. |
| Provided Methods / Testing | Preserve __init__, network methods and test_dht.py byte-for-byte. Real TCP loopback tests, no global node registry or hard-coded test answers. |
| Required Experimental Environment | Learner Lab t3.small, Ubuntu 24.04 AMD64, Python 3.12 required. User is locating access; local checks are supplementary, cloud execution remains pending. |
| Submission Guidelines | 226040255_hw4.zip containing only Assignment-4/chord_node.py and Assignment-4/test_dht.py. No report. Deadline 2026-11-15 23:59 UTC+8. |

## Code findings and implementation decisions

Starter chord_node.py: in_interval through transfer_keys are 13 NotImplementedError bodies. remote_call's local and remote dispatch use JSON (remote addresses become lists); normalize addresses to tuples. Server starts asynchronously in __init__; tests must wait for readiness. Network uses a single recv(4096); retain this teacher limitation. Test main catches exceptions and prints a completion banner; exit zero is insufficient.

Use modular distances; (a,a] is whole ring and (a,a) excludes a. Lookup checks successor then a preceding finger, falling back to successor to progress. Stabilize adopts successor's predecessor, notifies, and caches successor candidates from known routing state plus the successor's next node. Failed successor falls back to closest live cached candidate, without modifying networking. Notify transfers keys before updating predecessor, using old ownership boundary. Snapshot dictionary iteration; no claim of linearizable writes during joins because provided store dispatch is unlocked.

## Sequential phases

1. Implement 13 bodies and minimal helpers; verify unchanged starter segments using tests/check_scope.py.
2. Run original suite with python3 test_dht.py and a separate assertion-based local suite. Save unique run logs, command, hashes, environment, exit status. Fix actual failures; never infer correctness from banner alone.
3. Independent Verifier reads agents/verifier.md, tests frozen implementation and writes only own evidence. Root assembles exact two-member candidate in results/candidate/ after local verification, explicitly marking cloud execution pending; submission/ waits for required environment checks.
4. Different independent Reviewer reads agents/reviewer.md and audits actual ZIP, requirements and verification evidence. No Ready claim until required environment run completes. No upload or git commit/push.

Researcher and Report Writer stages are otherwise unnecessary: teacher gives protocol and no report is required. Remaining dependency: authorized Learner Lab access; no paid cloud provisioning is authorized.
