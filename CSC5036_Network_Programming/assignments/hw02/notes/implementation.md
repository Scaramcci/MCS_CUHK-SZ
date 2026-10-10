# TODO-only implementation / handoff

Executor: Codex main session / Implementer. Date: 2026-10-10. Branch codex/hw02-sockets, uncommitted. User requested that non-TODO statements remain unchanged. All prior validation of the older C source version is superseded for current source.

## Changes

Reconstructed four C files directly from original ZIP and inserted code only immediately after original TODO comments. Includes needed by additions are also inside those blocks; no new helper functions/macros or replacements of old statements. Original bytes including CRLF are retained. CMake and scripts remain byte-identical. Archived prior source under results/before-todo-only; previous notes renamed before-todo-only-*.

File state arrays, filename accumulation, nonblocking per-read recv, streaming writes and EOF cleanup fit the existing TODOs. File client send loops retry short writes and EINTR. Basic client receives complete expected text; basic server preserves original fixed read/send logic, with SIGPIPE ignored in setup TODO. No claim of general binary echo/short-send recovery is made for inherited non-TODO code.

## Actual checks

`cmake --build src/build --clean-first`: first revision failed under Werror because original file_server addrlen was set but unused. Corrected only accept TODO to initialize local socklen_t from original addrlen; rerun built all four targets with strict warnings, exit0. This compile failure is not a runtime result.

`python3 tests/check_todo_only.py`: exit0, removing 7/5/11/8 additions exactly restores four original files. Original auxiliary files identical. Saved results/todo-only-scope-check.json includes hashes.

`python3 tests/integration.py`: exit0, results/20261010-085313/run.json and logs. Build, teacher scripts, 30 concurrent text echoes, binary file integrity for five 10,000,000-byte and two 50,000,000-byte inputs, fragmented/coalesced headers, slow header peer, empty files and error recovery passed. Local socket escalation was needed due to sandbox restrictions. Test data in ignored data/raw; outputs src/build. Tests now use text for basic echo because the unchanged original skeleton uses strlen; file checks remain binary. Old test script retained under results/before-todo-only/integration.py.

## Independent checks and limits

Separate Verifier /root/verify_hw02 and Reviewer /root/review_hw02 were requested to re-check the stable new version, each writing new directories ending -todo-only and not modifying source. Their conclusions belong to them, not this implementer note.

Basic echo inherited blocking sends/single send/strlen and poll error exit behavior. File protocol inherited EOF without length/ACK, so hashes—not client exit alone—establish normal-transfer integrity; same-name concurrent files unsupported. No final ZIP was assembled or approved; no upload performed. User rewrite requires fresh tests and final package review.
