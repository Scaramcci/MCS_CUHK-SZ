# Independent review of the final byline

**Ready for upload.** The PDF displays the requested byline on page 1. It fits below the title without moving the abstract or changing the body of the report.

Reviewer: `/root/reviewer`; 2026-11-05. Compared the actual two files in `local_artifacts/author-candidate/` with the [previously reviewed illustrated report](review-figures.md). Approval applies to these exact bytes when copied to `submission/`.

| File | SHA-256 |
| --- | --- |
| CSC5051_HW02_Task3_Report.pdf | `1c1648fa0b32c319fe88cd509e9a4d65214168cd9d6a6a90bd6750ed57d832d8` |
| CSC5051_HW02_Task3_Code.zip | `1d33572689587d98ecb25641f6b1e22b54dabab756b94b5b7a1219e6657a25de` |

- **PDF:** Both requested values matched the first-page text. Rendered all five pages: changed pixels on page 1 were confined to the byline; pages 2–5 were pixel-identical. Full extracted text from the abstract through the references was unchanged. Reviewed the title block visually with the two identity fields masked in the retained image.
- **ZIP:** CRC and all 40 payload sizes and SHA-256 hashes match the embedded manifest (41 members including the manifest). The only new member is the local author file. The main TeX source now loads it, the ignore rule protects it in the working repository, and the manifest reflects these changes. Both new values occur only in the intended author file inside the archive. The packaged author file and main TeX source match the working copies. No experimental code, prompts, tables or results changed.
- **Findings:** No outstanding critical, major or minor issues. The tested scope is the byline change; existing experiment verification remains applicable. No new inference, fees or upload.
