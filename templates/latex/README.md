# Shared LaTeX Templates

- `CUHK-beamer.zip` is the existing CUHK Beamer presentation template. It remains unchanged.
- `报告模板.zip` is an **unofficial, English-language CUHK-Shenzhen academic report template** for XeLaTeX. It contains `main.tex`, an English README, an empty BibTeX scaffold, and the crest asset copied from `CUHK-beamer.zip`. Its former unrelated report text and NKU assets have been removed.
- `报告模板-preview.pdf` is a compiled one-page preview of the report template. It is a layout sample, not a completed assignment.

For a new report, extract `报告模板.zip` into that assignment's working `report/` directory, edit the metadata and replace every illustrative passage, then compile with `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex`. Keep the extracted template assets with the source file. Do not include the sample preview in an assignment submission.
