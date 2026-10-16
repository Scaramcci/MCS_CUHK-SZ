# Independent verification: 2026-10-15 style cleanup

Executor: independent Verifier `/root/verify_hw02`, not an implementation author. Tested 2026-10-15; timestamp, source SHA-256, actual build/client commands and exit states in `run.json`. This report supersedes the old implementation's functional verification only for the hashes recorded here. Old evidence remains unchanged.

Read root/course/assignment materials and verifier role, original ZIP and requirements, plan, revised four C sources and production TODO checker. Assignment README still referred to BEGIN/END markers at the start of this inspection; main session is responsible for updating the prose to this marker-free revision. Wrote only this new evidence directory and synthetic large data under the expressly authorized ignored `hw02/data/raw/verification-20261015/`. No code or submission files modified.

## Passed checks

Independent sequential matching consumes every fixed original byte segment between TODO comments in order and requires nonempty additions only immediately after those comments. All four C files preserve original bytes, including comments and line endings, outside these allowed insertion points; source markers are not required by this independent check. Original CMake and three scripts remain byte-identical. `manifest.json` contains original/current SHA-256. Static review found no macros or alternate control flow that replace or bypass the original echo send statement.

Clean isolated CMake build of all four programs with original CMakeLists and `-Wall -Wextra -Wpedantic -Werror` passed.

Provided socket_client completed its expected text exchange. Thirty concurrent independently generated text messages echoed exactly. RST peer recovery and subsequent valid echo passed; second listener failed with bind error as expected.

The file client transferred a deterministic synthetic 64 MiB (67,108,864 byte) binary file; source/received SHA-256 both equal `281e519df3077b557c6b03f5da83c4e8d397219259615dd7c3308f89cae8f2a6`. Input retained at `data/raw/verification-20261015/64MiB.bin`, target at its `received/64MiB.bin`. `git check-ignore` confirms both are ignored.

File checks passed for 30 simultaneous distinct binary uploads, empty file, 11-byte filename-header fragments, 317-byte body fragments, coalesced header/body, a slow incomplete header while other transfers complete, traversal filename rejection, abrupt RST, directory fopen failure, and later valid transfers. Servers remained alive through client errors and were terminated by verifier SIGINT.

Static file protocol review confirms per-client header/file state, a fixed 1024-byte padded name header, streaming binary writes, short-write retry on client sends, and EOF completion without whole-file buffers or cumulative int size limits. The tested 64 MiB exceeds the assigned 50 MB threshold; unlimited size is not empirically claimed.

## Failed checks

No failures in the grading-oriented acceptance checks executed above.

## Warnings and remaining limits

Text echo deliberately retains original `strlen`/single `send` implementation. It is not binary-safe, does not handle short sends or check send errors, and a slow reader can block its blocking send. The original socket_client send is likewise unchecked. Both servers retain original poll failure behavior (including exiting on EINTR). Comprehensive syscall-failure compliance is not established; these inherited limitations should not be described as fixed or fully verified. No injected short-send/EINTR tests were performed. SIGPIPE is ignored by the echo server to avoid process termination; connection reset survival was actually tested.

File protocol contains no declared expected length/checksum/server success ACK. Server close alone cannot prove durable successful reception; tested normal transfers are accepted using independent hashes. Abrupt transfer may leave partial files. Same-name simultaneous uploads, disk exhaustion, malicious local symlink targets and crash recovery were not validated.

Package follow-up: the actual `submission/Assignment-2.zip` (SHA-256 `058216a4588309bb35c932cfff02e3c7c9dd2db61ffc882539c30aa4454351af`) was unpacked into a new isolated `local_artifacts/verification-20261015-package/` directory. Its exact eight entries match both current source bytes and independently tested hashes. After creating a fresh `build/`, the specified `cmake ..` and `make` both exited 0. See `package-build.json` and package build logs. Network tests were not repeated for the package because all source bytes are identical. This establishes clean local buildability without the existing build directory; it does not establish portability to every platform. Final package approval remains the separate Reviewer role. Changes to these code/package hashes invalidate affected checks.

## Required fixes

None found in the exercised grading workload. Reviewer must preserve the warnings above when assessing the literal broad error-handling requirement alongside the strict TODO edit boundary.
