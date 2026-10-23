"""Classify acquisition provenance from evidence, never from cleared reason flags."""
import datetime as dt
from pathlib import Path


def classify_observation(row, manifest, max_lateness_s=330, root=None):
    if row.get('state') != 'PASS':
        return 'unverified'
    path = row.get('manifest') or ''
    parsed = Path(path)
    if parsed.is_absolute():
        if root is None:
            return 'unverified'
        try:
            path = parsed.resolve().relative_to(Path(root).resolve()).as_posix()
        except ValueError:
            return 'unverified'
    elif '..' in parsed.parts:
        return 'unverified'
    if path.startswith('data/derived_') or path.startswith('data/traffic_reconstruction_'):
        return 'reconstructed'
    if not path.startswith('data/amap_dynamic_v1/') or not manifest or manifest.get('status') != 'PASS':
        return 'unverified'
    started = manifest.get('frame_start_time') or manifest.get('started_at_utc')
    scheduled = row.get('scheduled_at')
    nominal = manifest.get('nominal_time')
    if not started or not scheduled or not nominal:
        return 'unverified'
    try:
        start = dt.datetime.fromisoformat(started)
        schedule = dt.datetime.fromisoformat(scheduled)
        nominal = dt.datetime.fromisoformat(nominal)
        target = dt.datetime.fromisoformat(row['nominal_at'])
        if any(x.tzinfo is None for x in [start, schedule, nominal, target]):
            return 'unverified'
        delay = (start - schedule).total_seconds()
    except (KeyError, TypeError, ValueError):
        return 'unverified'
    if nominal != target or not -1 <= delay <= max_lateness_s:
        return 'late_recovery_provider'
    return 'nominal_provider'
