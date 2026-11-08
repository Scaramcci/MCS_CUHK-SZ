"""Build a review candidate, not a cloud-validated final submission."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import datetime
import hashlib
import json
ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT/'results/candidate'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
DEST.mkdir(parents=True)
archive_path = DEST/'226040255_hw4.zip'
manifest = {'status':'local review candidate; required Learner Lab execution pending','members':{}}
with ZipFile(archive_path,'x',ZIP_DEFLATED) as archive:
    for name in ('chord_node.py','test_dht.py'):
        source = ROOT/'src/Assignment-4'/name
        data = source.read_bytes()
        member = 'Assignment-4/'+name
        archive.writestr(member,data)
        manifest['members'][member] = {'sha256':hashlib.sha256(data).hexdigest(),'size':len(data)}
manifest['archive'] = archive_path.name
manifest['sha256'] = hashlib.sha256(archive_path.read_bytes()).hexdigest()
with ZipFile(archive_path) as archive:
    assert set(archive.namelist()) == set(manifest['members'])
    assert archive.testzip() is None
    for member, info in manifest['members'].items():
        assert hashlib.sha256(archive.read(member)).hexdigest() == info['sha256']
(DEST/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(archive_path)
