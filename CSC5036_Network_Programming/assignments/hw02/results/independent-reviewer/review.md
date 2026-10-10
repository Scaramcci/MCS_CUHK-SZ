# Independent source review

Reviewer: `/root/review_hw02`; independent of Implementer and Verifier. Source version: `manifest.json`. No code, tests, originals, or final package modified by Reviewer.

Sources read: root AGENTS.md/README.md, course README.md, agents/README.md/reviewer.md, hw02 original assignment Markdown, original Assignment-2.zip inventory and source diff, notes/plan.md, all four working C files, self-test run 20261010-082831, independent-verifier/run.json, manifest.json and verify.py. No course/assignment AGENTS.md or override, or requirements/ directory exists; teacher originals are at hw02 root instead. The assignment README.md did not exist when review began; the Implementer subsequently created it and Reviewer read it after creation. Its run instructions, evidence references and protocol/test limitations agree with the reviewed implementation and records; it does not claim a reviewed final ZIP or upload.

## Critical issues

None found in reviewed source/evidence scope. No final submission package exists or was reviewed.

## Major issues / requirements discrepancy

The assignment Getting started section explicitly says to program only at TODO locations, while allowing helper functions. The working diff additionally changes existing socket_client.c send call and socket_server.c send/event/error/type handling outside TODO blocks. These are reasonable short-send/SIGPIPE/error-handling improvements, and no functional failure was found, but strict compliance with the edit-location restriction cannot be claimed. Before final submission, restore unrelated existing lines or obtain clarification that these necessary robustness changes are accepted. The file transfer section also changes the original TODO block layout while implementing it via a permitted helper.

## Minor issues / limitations

1. Echo server send_all uses blocking sends; a peer that continuously sends and never reads may eventually stall other clients. This is outside the provided fixed-message 30-client test and is not an explicit adverse-peer fairness requirement. No claim of arbitrary slow-reader robustness should be made.
2. File protocol uses the skeleton fixed 1024-byte filename header and EOF, with no declared length or success ACK. A clean EOF after truncation cannot reveal missing bytes; client server-close observation does not prove successful disk flush. Normal completion is validated by hashes. The assignment does not require interruption detection or acknowledgements.
3. Concurrent senders choosing the same basename overwrite the same destination; provided tests use distinct names. No collision handling requirement is stated.

## Checklist

| Requirement | Review result / evidence |
| --- | --- |
| Four named C programs, original CMake and scripts retained | Source inventory matches original 8 filenames; unchanged auxiliary files confirmed in independent manifest |
| Build with provided CMake | Independent build PASS with Wall/Wextra/Wpedantic/Werror; CMake unchanged |
| Single and 30 concurrent echo, poll(), backlog 3, persistent server | Static review and independent runtime PASS; poll and listen(...,3) present |
| Error handling / server survives peer failures | Independent RST/recovery and bind-failure tests PASS; static error paths reviewed |
| File saves in server current directory, filename first | Static review and independent file tests PASS |
| Concurrent binary files / segmented and coalesced headers | Independent 30-file exact-byte tests PASS |
| 50 MB+ transfer | Independent 67,108,864-byte file PASS; source/received SHA-256 both 281e519df3077b557c6b03f5da83c4e8d397219259615dd7c3308f89cae8f2a6 |
| Original generator and scripts | Implementer evidence shows 5x10,000,000 + 2x50,000,000 bytes and matched SHA-256; independent verification separately covers larger file and concurrency |
| Edit-location restriction | Discrepancy noted above; strict compliance unconfirmed |
| Report/screenshots | N/A: user supplied TA explicitly says none required |
| Exact final ZIP inventory / version | Not checked: this task is implementation and local testing for subsequent user rewrite; no submission ZIP was created |

## Final readiness

**Not ready as a final submission package**: no package reviewed and the strict TODO edit-location discrepancy remains. This does not negate independently passed functional tests for the recorded source version. Local implementation/test reference is complete within the verified normal-operation scope. User rewrite invalidates this version-specific review and requires new tests; final ZIP needs a separate inventory/hash review. No upload or teacher approval is implied.

## Follow-up scope note

The Implementer-created hw02/README.md was subsequently reviewed without modification. Verifier test-data relocation to ignored data/raw is evidence housekeeping and does not change reviewed C sources; original log paths remain historical run locations. No network rerun is necessary for that relocation.
