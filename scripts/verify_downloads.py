#!/usr/bin/env python3
"""Verify the curated static input snapshot offline with the standard library."""
import hashlib
import json
from pathlib import Path
import zipfile
from collections import Counter

root = Path(__file__).resolve().parents[1]
hashes = json.loads((root / 'downloads/SHA256.json').read_text())
for name, expected in hashes.items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
split = json.loads((root / 'downloads/STATIC_SPLIT.json').read_text())
rows = split['assignments']
assert len(rows) == 1176
assert len({r['instance_signature'] for r in rows}) == 1176
counts = Counter(r['partition'] for r in rows)
assert dict(counts) == {'train': 588, 'validation': 196, 'test': 392}, counts
with zipfile.ZipFile(root / 'downloads/static_public_v1.zip') as z:
    assert z.testzip() is None
    names = set(z.namelist())
    expected_names = {'STATIC_SPLIT.json'}
    for r in rows:
        for f in ['base_instance.json', 'scenario.json']:
            name = 'instances/' + r['instance_signature'] + '/' + f
            expected_names.add(name)
            json.loads(z.read(name))
    assert names == expected_names, 'Unexpected or missing ZIP members'
    assert json.loads(z.read('STATIC_SPLIT.json')) == split
print('PASS: hashes, 1176 unique task input pairs, archive shape, and 588/196/392 split')
