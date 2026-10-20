#!/bin/sh
set -eu
cd "$(dirname "$0")"
work_dir="$(mktemp -d "${TMPDIR:-/tmp}/csc5041-build.XXXXXX")"
mkdir -p ../pdf
for volume in main notes_en tutorial_answers practice_papers; do
  latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir="$work_dir" "$volume.tex" > "$work_dir/$volume-build.txt" 2>&1 || { cat "$work_dir/$volume-build.txt"; exit 1; }
  output_name="$volume"
  if [ "$volume" = main ]; then output_name=notes_zh; fi
  cp "$work_dir/$volume.pdf" "../pdf/$output_name.pdf"
done
printf 'PDFs: %s\nBuild logs: %s\n' "$(cd ../pdf && pwd)" "$work_dir"
