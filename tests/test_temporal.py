"""Validate chronological evidence calculations independently of visual judgment."""
from __future__ import annotations

import unittest
from test_tools import load

temporal = load('temporal_capture', 'tools/validate_temporal.py')


class CaptureIntervalTests(unittest.TestCase):
    def test_reports_measured_cadence_and_gaps_between_capture_brackets(self):
        frames = [
            {'capture_start_ms': 10, 'capture_end_ms': 60},
            {'capture_start_ms': 175, 'capture_end_ms': 235},
            {'capture_start_ms': 250, 'capture_end_ms': 310},
        ]
        result = temporal.capture_summary(frames)
        self.assertEqual(result['frame_count'], 3)
        self.assertEqual(result['capture_span_ms'], 300)
        self.assertEqual(result['maximum_gap_between_capture_brackets_ms'], 115)
        self.assertEqual(result['start_to_start_intervals_ms'], [165, 75])

    def test_one_frame_cannot_establish_an_episode(self):
        with self.assertRaises(ValueError):
            temporal.capture_summary([{'capture_start_ms': 0, 'capture_end_ms': 10}])

    def test_reversed_interval_is_rejected(self):
        with self.assertRaises(ValueError):
            temporal.capture_summary([
                {'capture_start_ms': 10, 'capture_end_ms': 0},
                {'capture_start_ms': 20, 'capture_end_ms': 30},
            ])

    def test_out_of_order_or_overlapping_intervals_are_rejected(self):
        for next_start in (5, 15):
            with self.subTest(next_start=next_start), self.assertRaises(ValueError):
                temporal.capture_summary([
                    {'capture_start_ms': 10, 'capture_end_ms': 20},
                    {'capture_start_ms': next_start, 'capture_end_ms': 40},
                ])


if __name__ == '__main__':
    unittest.main()
