
import unittest
from unittest.mock import Mock, patch
import tempfile
import os
from src.pycp import pycp


class TestCopyFileWithProgress(unittest.TestCase):
    def setUp(self):
        self.src_file = tempfile.NamedTemporaryFile(delete=False)
        self.src_file.write(b'Test data')
        self.src_file.close()

        self.dest_file = tempfile.NamedTemporaryFile(delete=False)
        self.dest_file.close()

        self.progress = Mock()
        self.total_task = Mock()
        self.current_task = Mock()

    def tearDown(self):
        os.unlink(self.src_file.name)
        os.unlink(self.dest_file.name)

    @patch('time.time')
    def test_copy_file_with_progress_happy_path(self, mock_time):
        mock_time.return_value = 0
        result = pycp.copy_file_with_progress(self.src_file.name, self.dest_file.name, self.progress, self.total_task, self.current_task, 0, 0, True)
        self.assertEqual(result, 9)
        self.progress.update.assert_called()

    @patch('time.time')
    def test_copy_file_with_progress_skip_existing_file(self, mock_time):
        mock_time.return_value = 0
        result = pycp.copy_file_with_progress(self.src_file.name, self.dest_file.name, self.progress, self.total_task, self.current_task, 0, 0, False)
        self.assertEqual(result, 0)

    @patch('time.time')
    def test_copy_file_with_progress_calculate_speed(self, mock_time):
        mock_time.side_effect = [0, 1]
        result = pycp.copy_file_with_progress(self.src_file.name, self.dest_file.name, self.progress, self.total_task, self.current_task, 0, 0, True)
        self.assertEqual(result, 9)
        self.progress.update.assert_called_with(self.total_task, advance=9)


if __name__ == '__main__':
    unittest.main()
