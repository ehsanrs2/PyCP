import unittest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile
import os
from src.pycp import pycp


class TestCopyDirectoryRecursive(unittest.TestCase):
    def setUp(self):
        self.src_dir = tempfile.TemporaryDirectory()
        self.dest_dir = tempfile.TemporaryDirectory()
        self.progress = Mock()
        self.total_task = Mock()

    def tearDown(self):
        self.src_dir.cleanup()
        self.dest_dir.cleanup()

    @patch('src.pycp.pycp.copy_directory_recursive')
    def test_when_source_is_directory_and_dest_does_not_exist(self, mock_copy_directory_recursive):
        mock_copy_directory_recursive.return_value = 20
        src_subdir = Path(self.src_dir.name) / 'subdir'
        src_subdir.mkdir()
        dest_subdir = Path(self.dest_dir.name) / 'subdir'
        result = pycp.copy_directory_recursive(src_subdir, dest_subdir, self.progress, self.total_task, 0, 0, True)
        self.assertEqual(result, 20)
        mock_copy_directory_recursive.assert_called_once()

    @patch('src.pycp.pycp.copy_file_with_progress')
    def test_when_source_is_directory_and_dest_exists_and_overwrite_is_true(self, mock_copy_file_with_progress):
        mock_copy_file_with_progress.return_value = 10
        src_dir = Path(self.src_dir.name) / 'dir'
        src_dir.mkdir()
        src_file = src_dir / 'file.txt'
        src_file.touch()
        dest_dir = Path(self.dest_dir.name) / 'dir'
        if dest_dir.exists():
            dest_dir.rmdir()
        result = pycp.copy_directory_recursive(src_dir, dest_dir, self.progress, self.total_task, 0, 0, True)
        self.assertEqual(result, 10)
        mock_copy_file_with_progress.assert_called_once()

    @patch('src.pycp.pycp.copy_file_with_progress')
    def test_when_source_is_directory_and_dest_exists_and_overwrite_is_false(self, mock_copy_file_with_progress):
        mock_copy_file_with_progress.return_value = 0
        src_dir = Path(self.src_dir.name) / 'dir'
        src_dir.mkdir()
        dest_dir = Path(self.dest_dir.name) / 'dir'
        if dest_dir.exists():
            dest_dir.rmdir()
        result = pycp.copy_directory_recursive(src_dir, dest_dir, self.progress, self.total_task, 0, 0, False)
        self.assertEqual(result, 0)
        mock_copy_file_with_progress.assert_not_called()


if __name__ == '__main__':
    unittest.main()



