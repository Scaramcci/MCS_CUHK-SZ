# Independent review: TODO-only implementation

Reviewer: `/root/review_hw02`, independent of code author and Verifier. Scope: current eight source files, original assignment and ZIP, new test evidence. Version hashes and independent byte-restoration results are in manifest.json. Old review/evidence records are historical and retained separately.

## Critical issues

None found in this source/evidence scope. No final ZIP was created or reviewed.

## Major issues

No required normal-operation functionality blocker found in the current code. The prior editing-scope discrepancy is resolved: Reviewer independently removed each addition immediately following a TODO comment and confirmed exact equality to original ZIP bytes, including original CRLF. All four auxiliary files remain byte-identical. No macro replacement or bypass of original skeleton logic was found.

README.md, notes/implementation.md and the revision section of notes/plan.md have now been read in their updated form. They correctly separate historical and current evidence, state the TODO-only boundary, and disclose the inherited text-echo and poll/send limitations. The earlier plan goals are explicitly superseded by its TODO-only revision section.

## Minor issues / limits

- The broad assignment syscall-error-handling statement is not fully established: inherited echo sends remain unchecked and original poll error branches exit on EINTR. These were not injected during testing; do not claim comprehensive error handling. They are preserved under the explicit TODO-only boundary.
- The required skeleton echo uses strlen and an unchecked blocking send; it supports the specified text-message tests, not arbitrary binary echo or robust partial-send handling. SIGPIPE is ignored in the TODO setup so a peer reset does not terminate the server. Slow non-reading peers can block output.
- File protocol retains a fixed-size 1024-byte filename header and EOF framing. It has no size declaration or success ACK; interrupted clean EOF and write/flush success cannot be confirmed from client exit alone. Normal file integrity is verified by hashes.
- Concurrent uploads need distinct basenames to avoid overwriting. Provided tests meet this condition.
- errno/signal headers occur inside TODO blocks to preserve the original bytes; strict Ubuntu gcc build passes. No portability beyond the tested required environment is claimed.

## Checklist

| Requirement | Result |
| --- | --- |
| TODO-only edit range, names and original auxiliary files | PASS, independent byte check; source hashes in manifest.json |
| C / Unix-like / provided CMake | PASS, independent warning-as-error build |
| Single / 30 concurrent text echo | PASS, independent test |
| poll / backlog 3 / persistent server | Static confirmation plus runtime PASS |
| Peer reset recovery and duplicate bind failure | Independent PASS |
| Filename first, binary streaming file in working directory | Static confirmation and independent PASS |
| Fragmented/coalesced header, empty file, 30 concurrent binary files | Independent PASS |
| Large-file transfer | Independent PASS: 67,108,864 bytes, source and target SHA-256 both 281e519df3077b557c6b03f5da83c4e8d397219259615dd7c3308f89cae8f2a6 |
| Teacher scripts and five small/two large files | Implementer new run 20261010-085313 PASS with all seven SHA-256 matches |
| Source/evidence consistency | All eight hashes match new independent-verifier-todo-only/run.json and implementer run |
| Report / screenshots | N/A, TA says none required |
| Final ZIP inventory and hashes | Not checked, no final package in this implementation/test task |

Independent runtime evidence: results/independent-verifier-todo-only/run.json and verify.py. Reviewer read both and checked coverage and hashes; Reviewer did not substitute own network tests for Verifier. New implementer evidence: results/20261010-085313/run.json.

## Final readiness

**Not ready as a final submission package** because no package was assembled or reviewed. Source implementation and required normal-operation testing pass for this version, with the documented protocol/skeleton boundaries. Current documentation is consistent with the reviewed version and evidence. User rewrite invalidates version-specific results and needs retesting; a final ZIP also needs its own inventory/version review. No upload or teacher acceptance is implied.

Final follow-up: read the new independent-verifier-todo-only/verification.md; its coverage and limitations agree with this review. The previously stale command metadata was corrected to the actual new verification script path without source changes or rerun.
