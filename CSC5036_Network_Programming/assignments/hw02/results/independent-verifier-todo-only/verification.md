# Independent verification: TODO-only revision

Executor: independent Verifier `/root/verify_hw02`, not an implementation author. Tested 2026-10-10; timestamp, source SHA-256, actual build/client commands and exit states in `run.json`. This report supersedes the old implementation's functional verification only for the hashes recorded here. Old evidence remains unchanged.

Read root/course/assignment materials and verifier role, original ZIP and requirements, plan, revised four C sources and production TODO checker. Assignment README still reflected the earlier version at inspection; main session was notified to update it. Wrote only this new evidence directory and synthetic large data under the expressly authorized ignored `hw02/data/raw/independent-verifier-todo-only/`. No code or submission files modified.

## Passed checks

Independent byte comparison removes only marked additions immediately after TODO comments and restores all four C files exactly to original ZIP bytes, including line endings. Number of insertion blocks equals number of original TODO comments. Original CMake and three scripts remain byte-identical. `manifest.json` contains original/current SHA-256. Static review found no macros or alternate control flow that replace or bypass the original echo send statement.

Clean isolated CMake build of all four programs with original CMakeLists and `-Wall -Wextra -Wpedantic -Werror` passed.

Provided socket_client completed its expected text exchange. Thirty concurrent independently generated text messages echoed exactly. RST peer recovery and subsequent valid echo passed; second listener failed with bind error as expected.

The file client transferred a deterministic synthetic 64 MiB (67,108,864 byte) binary file; source/received SHA-256 both equal `281e519df3077b557c6b03f5da83c4e8d397219259615dd7c3308f89cae8f2a6`. Input retained at `data/raw/independent-verifier-todo-only/64MiB.bin`, target at its `received/64MiB.bin`. `git check-ignore` confirms both are ignored.

File checks passed for 30 simultaneous distinct binary uploads, empty file, 11-byte filename-header fragments, 317-byte body fragments, coalesced header/body, a slow incomplete header while other transfers complete, traversal filename rejection, abrupt RST, directory fopen failure, and later valid transfers. Servers remained alive through client errors and were terminated by verifier SIGINT.

Static file protocol review confirms per-client header/file state, a fixed 1024-byte padded name header, streaming binary writes, short-write retry on client sends, and EOF completion without whole-file buffers or cumulative int size limits. The tested 64 MiB exceeds the assigned 50 MB threshold; unlimited size is not empirically claimed.

## Failed checks

No failures in the grading-oriented acceptance checks executed above.

## Warnings and remaining limits

Text echo deliberately retains original `strlen`/single `send` implementation. It is not binary-safe, does not handle short sends or check send errors, and a slow reader can block its blocking send. The original socket_client send is likewise unchecked. Both servers retain original poll failure behavior (including exiting on EINTR). Comprehensive syscall-failure compliance is not established; these inherited limitations should not be described as fixed or fully verified. No injected short-send/EINTR tests were performed. SIGPIPE is ignored by the echo server to avoid process termination; connection reset survival was actually tested.

File protocol contains no declared expected length/checksum/server success ACK. Server close alone cannot prove durable successful reception; tested normal transfers are accepted using independent hashes. Abrupt transfer may leave partial files. Same-name simultaneous uploads, disk exhaustion, malicious local symlink targets and crash recovery were not validated.

No submission ZIP exists within this verifier's scope and none was reviewed. README and final packaging approval belong to separate author/Reviewer stages. Changes to these recorded code hashes invalidate affected checks.

## Required fixes

None found in the exercised grading workload. Reviewer must preserve the warnings above when assessing the literal broad error-handling requirement alongside the strict TODO edit boundary.
