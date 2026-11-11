"""Build a reviewable Part I ZIP from a completed teacher export and the PDF."""
import argparse
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('destination', type=Path)
args = parser.parse_args()
args.destination.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(root/'local_artifacts/export.zip') as source, ZipFile(args.destination, 'x', ZIP_DEFLATED) as result:
    assert source.testzip() is None
    evidence = [p for p in source.namelist() if p.startswith('results/') and p.endswith('/summary.json')]
    if len(evidence) != 6:
        raise ValueError('Need all six runs')
    for name in source.namelist():
        content = source.read(name)
        if name.startswith('results/') and name.endswith('/config.json'):
            obj = json.loads(content)
            obj['data_dir'] = 'data/shakespeare_char'
            content = (json.dumps(obj, indent=2)+'\n').encode()
        elif name.startswith('results/') and name.endswith('/summary.json'):
            obj = json.loads(content)
            assert obj['status'] == 'completed' and obj['tokens'] == 92160000
            obj['output'] = 'runs/' + Path(name).parent.name
            content = (json.dumps(obj, indent=2)+'\n').encode()
        elif name == 'README.txt':
            content = ('Part I code, endpoint results, and PDF report. To reproduce, place the supplied '
                       'p1/data directory under code/ and run the scripts from code/. Dataset and '
                       'checkpoint binaries are kept separately. Absolute remote data/output paths '
                       'in the included JSON copies are shown relative to the project.\n').encode()
        result.writestr(name, content)
    result.write(root/'src/LICENSE', 'code/LICENSE')
    result.write(root/'report/part1-report.pdf', 'part1-report.pdf')
