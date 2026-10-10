# Independent verification

Executor: `/root/verify_hw02`, independent of implementation. Scope: `hw02/src/`; only wrote this isolated verifier directory. Tested 2026-10-10; exact UTC time, commands and exits in `run.json`; source hashes in `run.json` and `manifest.json`. No source files, report or submission package changed.

Inputs read: root README/AGENTS, course README, agents/README and verifier role, original `Assignment-2_ Socket Programming.md` (Basic Socket Programming/server/client/build/testing; Simple File Transfer; Dive Deeper), original ZIP, plan and actual source. No nested course/assignment AGENTS files were found. At the start of verification, assignment README did not yet exist; the main session subsequently added it. No requirements directory was present; original requirements are at assignment root.

## Passed checks

Independent clean CMake build of all four executables, using unchanged original CMake and `-Wall -Wextra -Wpedantic -Werror`.

Provided socket client exchanges expected echo. Independently designed 30-client exact binary echo test, RST recovery and duplicate-listener bind error all passed.

Independent 64 MiB (67,108,864 bytes) deterministic synthetic binary file sent by provided file client, with exact byte-size and SHA-256 agreement. SHA-256 values are in `run.json`; original test input and received copy are now retained under `hw02/data/raw/independent-verifier/`; `data-migration.json` records the original paths, retained paths, sizes and hashes. Original execution logs are unchanged. This exceeds the 50 MB grading threshold; no claim is made of testing unlimited sizes.

Empty file, fragmented 1024-byte filename header and binary payload, coalesced header/payload, slow incomplete-header peer while another completes, 30 simultaneous distinct binary file transfers, invalid traversal header, RST, directory fopen failure, and later valid transfers all passed. Servers survived the client errors and were stopped by verifier SIGINT only. Incomplete transfer output is not claimed valid.

Static protocol review: filename is padded to 1024 bytes and server accumulates the header without conflating body; each slot has separate FILE/header state; file body streams to disk with size_t per-chunk writes and EOF completion. Short sends and EINTR are retried. Filename validation blocks slash traversal. Original ZIP has exactly 8 files and all four non-C files in src match it byte for byte.

## Failed checks

None in the above independently executed acceptance tests.

## Warnings / scope limits

Echo server uses blocking send_all. A peer continuously sending without consuming its echoed bytes can eventually fill the socket send buffer and block other clients. Tested concurrent short/bounded messages pass; hostile slow-reader isolation is not established. This is outside the provided short-message workload, but is a robustness limitation.

File protocol uses EOF without length/checksum/status acknowledgement. A receive-side write or final flush error is logged server-side but cannot reliably be distinguished from successful completion by file_client. Normal completion has therefore been verified independently by content hashes. Abrupt sender termination can leave a partial file; no crash-safe or resumable transfer claim is made. Same-name simultaneous uploads and malicious local symlink targets are not part of the assigned tests and have not been validated.

The source changes include small safety corrections around original read/send/error paths in addition to TODO blocks. Original requirements permit helper functions and direct file-transfer changes, but say to program only at TODO locations; Reviewer should evaluate this literal scope requirement. Original files remain untouched in ZIP.

No submission ZIP examined or approved by this verifier. Next role is a separate Reviewer; source or package changes invalidate affected checks and hashes.

## Required fixes

No blocker found for the stated grading workload. Robustness limitations above remain documented and must not be described as verified production guarantees.
