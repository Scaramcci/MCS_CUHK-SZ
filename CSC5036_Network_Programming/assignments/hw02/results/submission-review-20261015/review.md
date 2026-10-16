# Final submission review — 2026-10-15

Reviewer: `/root/review_hw02`, independent of the implementation author and this round's Verifier `/root/verify_hw02`. Reviewed actual `submission/Assignment-2.zip` without changing code, package or others' evidence. This review supersedes the older no-package review only for the exact ZIP/hash below.

## Critical issues

None found. ZIP CRC test passed. Its eight entries are regular files at archive root; there is no wrapper directory, duplicate name, report, screenshot, test data, build cache, role record, credential or unrelated file. Source content was read from the ZIP, not inferred from the assembly manifest.

## Major issues

None found in the stated assignment workload and final-package checks. Actual ZIP bytes for each entry match current src, this round's independent verification hashes, and self-test hashes. All original fixed text outside TODO insertion sites is preserved byte-for-byte, including CRLF; CMake and scripts match original ZIP contents exactly. Previous edit-boundary issue is resolved. No marker/macro bypass of original logic was found.

## Minor issues and explicit limits

The inherited basic echo sends once using strlen, does not check/retry send failures and can block on slow readers. Both servers preserve the original poll-error branch, including exiting on EINTR. Comprehensive syscall-failure handling is therefore not established, despite the broad error-handling language in the original specification. These retained skeleton limits were disclosed in README and independent verification; normal required text workloads and peer-reset survival were tested. No arbitrary binary echo, injected short-send/EINTR, or hostile slow-reader guarantee is made.

The inherited file protocol has fixed 1024-byte filename framing and EOF completion without declared length or application success ACK. Normal integrity is demonstrated by byte/hash comparisons; client exit alone does not prove durable write success. Interrupted clean EOF may leave partial files, same-name concurrent uploads may overwrite, and disk exhaustion/crash recovery were not validated. These are boundaries, not observed failures in required normal file tests. Unlimited size was not empirically tested.

## Submission checklist

| Requirement / item | Result and evidence |
| --- | --- |
| Original eight root files, unchanged names/structure | PASS: independently enumerated actual ZIP |
| socket_server.c and socket_client.c | PASS: completed TODOs; single/30 concurrent text echo independently tested |
| file_server.c and file_client.c | PASS: filename first, independent per-client binary streaming and current-directory output |
| CMakeLists.txt | PASS: original bytes, independent clean strict-warning CMake build of all four targets; actual ZIP additionally extracted fresh and cmake .. / make both exit 0 |
| con.sh, con_file.sh, generator.sh | PASS: original bytes, each ZIP Unix mode 0100755 |
| TODO-only editing boundary | PASS: independent original-fixed-segment matching on ZIP file bytes |
| poll and backlog 3, normal persistent operation | PASS: static inspection and independent runtime tests |
| Small/concurrent file integrity | PASS: self-test 20261015-115947 runs provided generator/scripts, all seven file SHA-256 pairs match; independent 30 binary uploads also pass |
| Large file integrity, assigned 50 MB+ | PASS: independent 67,108,864-byte file, both SHA-256 281e519df3077b557c6b03f5da83c4e8d397219259615dd7c3308f89cae8f2a6 |
| Segmented/coalesced headers, empty file, errors/recovery | PASS: independent 20261015 verification; coverage/limits stated above |
| Package versus verified version | PASS: every actual ZIP entry matches independent run.json and self-test run.json |
| Report/screenshots | N/A: TA email explicitly says none required |
| Data/build/cache/internal notes absent | PASS: actual eight-entry inventory and all content reviewed |
| Blackboard upload | Not performed; external submission remains the user's action |

Actual ZIP inventory: CMakeLists.txt, con.sh, con_file.sh, file_client.c, file_server.c, generator.sh, socket_client.c, socket_server.c. Detailed sizes, modes and independent per-file hashes are in this review directory's manifest.json.

Sources: root AGENTS.md (including local-only data/Git rules), agents/reviewer.md, original Assignment-2_ Socket Programming.md sections Basic Socket Programming / Simple File Transfer / Dive Deeper, original Assignment-2.zip, user-provided TA submission email, current README, self-test results/20261015-115947/run.json, independent results/verification-20261015/run.json, verification.md and package-build.json, and actual final ZIP contents. Existing course/root context and lack of task-level rules were checked previously. Reviewer wrote only this new evidence directory and did not run or alter network tests.

## Final readiness

**Ready** for user submission of this exact package under the exercised normal assignment workload and TA eight-file ZIP instructions. This is a packaging/version and evidence-backed readiness decision, not a claim of comprehensive error robustness, teacher approval, a guaranteed grade or actual upload.

- ZIP: `submission/Assignment-2.zip`
- Size: 8,964 bytes
- SHA-256: `058216a4588309bb35c932cfff02e3c7c9dd2db61ffc882539c30aa4454351af`
- Independent verification: PASS, same eight entry hashes as package
- Outstanding required corrections in reviewed workload/package: none
- Next action: user uploads this exact ZIP to Blackboard; any package/code change invalidates affected version-specific checks and needs review again.
