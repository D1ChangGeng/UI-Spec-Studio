"""Check that actual study messages retain their contemporary source identity."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('design_message_recorder', ROOT/'tools/record_design_message.py')
RECORDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RECORDER)


class MessageRecorderTests(unittest.TestCase):
    def test_text_and_source_are_exact_and_replayable(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'app').mkdir()
            original = b'const message = "real source";\r\n'
            (root/'app/main.js').write_bytes(original)
            for excluded in ('node_modules', 'dist', '.git', '__pycache__'):
                (root/'app'/excluded).mkdir()
                (root/'app'/excluded/'private.txt').write_text('not application source')
            message = '实际结果\n\n![结果](sandbox:/actual.png)\n'
            row = RECORDER.record(root, message, 'commentary')
            self.assertEqual(row['text'], message)
            self.assertEqual(row['text_sha256'], hashlib.sha256(message.encode()).hexdigest())
            self.assertEqual(row['source_files'], {'app/main.js': hashlib.sha256(original).hexdigest()})
            with zipfile.ZipFile(root/'outward'/row['source_archive']) as archive:
                self.assertEqual(archive.namelist(), ['app/main.js'])
                self.assertEqual(archive.read('app/main.js'), original)
            self.assertEqual(json.loads((root/'outward/message-001.json').read_text(encoding='utf-8')), row)

    def test_later_source_does_not_rewrite_an_earlier_message(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'app').mkdir()
            source = root/'app/index.html'
            source.write_bytes(b'first')
            first = RECORDER.record(root, 'first actual message', 'commentary')
            preserved = {p.name: p.read_bytes() for p in (root/'outward').iterdir()}
            source.write_bytes(b'second')
            second = RECORDER.record(root, 'final actual message', 'final')
            self.assertEqual(second['id'], 'message-002')
            self.assertNotEqual(first['source_files'], second['source_files'])
            for name, content in preserved.items():
                self.assertEqual((root/'outward'/name).read_bytes(), content)

    def test_invalid_message_fails_without_creating_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for message, channel in (('  ', 'commentary'), ('text', 'analysis')):
                with self.assertRaises(ValueError):
                    RECORDER.record(root, message, channel)
            self.assertFalse((root/'outward').exists())

    def test_missing_sequence_number_cannot_overwrite_existing_message(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'app').mkdir()
            (root/'outward').mkdir()
            protected = root/'outward/message-002.json'
            protected.write_bytes(b'preserved')
            with self.assertRaises(ValueError):
                RECORDER.record(root, 'later message', 'final')
            self.assertEqual(protected.read_bytes(), b'preserved')
            self.assertEqual(list((root/'outward').iterdir()), [protected])

    def test_referenced_media_survives_later_file_replacement(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'app').mkdir()
            (root/'evidence').mkdir()
            media = root/'evidence/desktop.png'
            media.write_bytes(b'actual first capture bytes')
            message = f'![Current result](sandbox:{media.as_posix()})'
            first = RECORDER.record(root, message, 'commentary')
            media.write_bytes(b'later capture at the same path')
            second = RECORDER.record(root, message, 'final')
            with zipfile.ZipFile(root/'outward'/first['media_archive']) as archive:
                self.assertEqual(archive.read('evidence/desktop.png'), b'actual first capture bytes')
            self.assertNotEqual(first['media_files'], second['media_files'])
            self.assertEqual(first['text'], second['text'])

    def test_missing_media_is_identified_instead_of_claimed_captured(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'app').mkdir()
            media = root/'not-yet-created.webm'
            row = RECORDER.record(root, f'[Episode](sandbox:{media.as_posix()})', 'commentary')
            self.assertIsNone(row['media_archive'])
            self.assertEqual(row['media_files'], {})
            self.assertEqual(row['media_unavailable'][0]['reason'], 'not_available_at_recording')

    def test_media_outside_workspace_is_not_read(self):
        with tempfile.TemporaryDirectory() as temp:
            parent = Path(temp)
            root = parent/'cell'
            (root/'app').mkdir(parents=True)
            outside = parent/'unrelated.png'
            outside.write_bytes(b'not authorized study media')
            row = RECORDER.record(root, f'![Image](sandbox:{outside.as_posix()})', 'commentary')
            self.assertEqual(row['media_files'], {})
            self.assertEqual(row['media_unavailable'][0]['reason'], 'outside_workspace')


if __name__ == '__main__':
    unittest.main()
