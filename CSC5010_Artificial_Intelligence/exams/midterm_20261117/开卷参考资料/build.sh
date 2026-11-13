#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
run_dir="../results/build-$(date +%Y%m%d-%H%M%S)-$$"
mkdir -p -- "$run_dir"
for pass in 1 2 3; do
  xelatex -interaction=nonstopmode -halt-on-error -output-directory="$run_dir" main.tex > "$run_dir/compile-pass${pass}.txt" 2>&1
done
cp -- "$run_dir/main.pdf" 'CSC5010_期中开卷参考.pdf'
python3 - "$run_dir" <<'PY'
import hashlib,json,subprocess,sys
from pathlib import Path
run=Path(sys.argv[1]); files=[Path('main.tex'),*sorted(Path('chapters').glob('*.tex')),Path('build.sh')]
record={'compiler':subprocess.check_output(['xelatex','--version'],text=True).splitlines()[0],
        'command':'bash build.sh (3 XeLaTeX passes, -interaction=nonstopmode -halt-on-error)',
        'exit_status':0,'sources':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        'output':'CSC5010_期中开卷参考.pdf','pdf_sha256':hashlib.sha256(Path('CSC5010_期中开卷参考.pdf').read_bytes()).hexdigest()}
(run/'build-record.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print('PDF: '+record['output']);print('Build record: '+str(run/'build-record.json'))
PY
