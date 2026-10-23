"""Offline integrity and provenance-denominator checks; no API or solver calls."""
import csv
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'evidence/BUILD_MANIFEST.json').read_text())
for name, expected in manifest['files_sha256'].items():
    path = root / name
    assert path.is_file() and not path.is_symlink(), name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, name
    if path.suffix not in ['.zip', '.png']:
        text = path.read_text()
        assert not re.search(r'/(?:Users|data/route)/|sk-[A-Za-z0-9_-]{16,}|github_pat_[A-Za-z0-9_]+|ghp_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._-]{12,}|[?&](?:key|token|api_key)=[^\s)]+', text), name
        if path.suffix == '.json':
            json.loads(text)
        if path.suffix == '.md':
            for match in re.findall(r'\]\(([^)]+)\)|(?:src|href)="([^"]+)"', text):
                target = match[0] or match[1]
                if not target.startswith(('https://', 'http://', '#', 'mailto:')):
                    p = (path.parent / target.split('#')[0]).resolve()
                    assert p.is_relative_to(root.resolve()) and p.exists(), (name, target)

snapshot = json.loads((root / 'evidence/PROGRESS_SNAPSHOT.json').read_text())
collection = json.loads((root / 'downloads/COLLECTION_PROGRESS.json').read_text())
assert snapshot['collection'] == collection
p = collection['progress']
keys = ['nominal_provider', 'late_recovery_provider', 'reconstructed', 'unverified']
values = [p['complete_provider_nominal_frames'], p['late_recovery_provider_frames'], p['reconstructed_frames'], p['unverified_frames']]
assert sum(values) == p['recorded_slots'] == sum(p['states'].values())
assert p['provider_complete_frames_including_late_recovery'] == values[0] + values[1]
assert p['nominal_provider_od_time_values'] == values[0] * 39800
assert p['recorded_slot_percentage'] == round(100 * p['recorded_slots'] / 1680, 2)
assert 'complete_real_pass_frames' not in p
for axis in ['daily', 'cities']:
    for k, value in zip(keys, values):
        assert sum(r.get(k, 0) for r in collection[axis]) == value, (axis, k)
with (root / 'downloads/COLLECTION_COVERAGE.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
assert len({(r['city'], r['date']) for r in rows}) == len(rows)
assert sum(int(r['recorded_slots']) for r in rows) == p['recorded_slots']
for k, value in zip(keys, values):
    assert sum(int(r[k]) for r in rows) == value, k
with (root / 'downloads/PILOT_RESULTS.csv').open(newline='') as f:
    records = list(csv.DictReader(f))
assert len(records) == 51
assert all(r['method'] != 'lns' and r['relative_gap'] == '' and r['gap_kind'] == 'WITHHELD_REFERENCE_POOL_CHANGED' for r in records)
assert snapshot['references']['status'] == 'WITHHELD_PENDING_VERSIONED_POOL_REBUILD'
assert not snapshot['references']['public_quality_summary_available']
assert not snapshot['llm_pilot']['formal_model_ranking_completed']
assert snapshot['llm_pilot']['first'] == {'n': 48, 'valid': 9}
assert snapshot['llm_pilot']['repeat'] == {'n': 16, 'valid': 5}
assert snapshot['llm_pilot']['attempts'] == 64
assert snapshot['composition']['reference_batch']['public_reference_eligibility'] == 'NOT_ACCEPTED_MIXED_POOL'
print('PASS: file hashes, local links, secret-pattern scan, provenance denominators, city/day counts, and custom-method withdrawal')
