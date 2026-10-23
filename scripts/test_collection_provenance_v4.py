import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from collection_provenance_v4 import classify_observation


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.row = dict(state='PASS', manifest='data/amap_dynamic_v1/test/run/manifest.json',
                        nominal_at='2026-10-22T07:00:00+08:00', scheduled_at='2026-10-22T07:05:00+08:00', reason=None)
        self.manifest = dict(status='PASS', nominal_time=self.row['nominal_at'], frame_start_time='2026-10-22T07:05:02+08:00')

    def test_normal_provider(self):
        self.assertEqual(classify_observation(self.row, self.manifest), 'nominal_provider')

    def test_cleared_reason_does_not_relabel_reconstruction(self):
        self.row['manifest'] = 'data/derived_imputed_v2/test.manifest.json'
        self.assertEqual(classify_observation(self.row, self.manifest), 'reconstructed')

    def test_actual_late_start_detected_even_when_nominal_matches(self):
        self.manifest['frame_start_time'] = '2026-10-22T07:25:00+08:00'
        self.assertEqual(classify_observation(self.row, self.manifest), 'late_recovery_provider')

    def test_different_nominal_is_recovery(self):
        self.manifest['nominal_time'] = '2026-10-22T07:17:00+08:00'
        self.assertEqual(classify_observation(self.row, self.manifest), 'late_recovery_provider')

    def test_quarantine_cannot_be_complete(self):
        self.row['state'] = 'QUARANTINE'
        self.assertEqual(classify_observation(self.row, self.manifest), 'unverified')

    def test_absolute_derived_path_is_classified_under_explicit_root(self):
        self.row['manifest'] = '/workspace/benchmark/data/derived_imputed_v2/test.meta.json'
        self.assertEqual(classify_observation(self.row, None, root='/workspace/benchmark'), 'reconstructed')

    def test_absolute_path_outside_root_is_not_certified(self):
        self.row['manifest'] = '/outside/data/derived_imputed_v2/test.meta.json'
        self.assertEqual(classify_observation(self.row, None, root='/workspace/benchmark'), 'unverified')

    def test_missing_or_naive_timestamps_are_not_certified(self):
        del self.manifest['frame_start_time']
        self.assertEqual(classify_observation(self.row, self.manifest), 'unverified')
        self.manifest['frame_start_time'] = '2026-10-22T07:05:02'
        self.assertEqual(classify_observation(self.row, self.manifest), 'unverified')


if __name__ == '__main__':
    unittest.main()
