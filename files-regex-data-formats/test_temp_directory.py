import tempfile
import unittest
from pathlib import Path
from exercise import archive_log_files

class TestArchiveLogFiles(unittest.TestCase):
    def setUp(self):
        # Creates a fresh temp directory before each test
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_dir = Path(self.temp_dir.name)

    def tearDown(self):
        # Cleans it up after each test
        self.temp_dir.cleanup()

    def test_renames_log_files(self):
        (self.log_dir / "app.log").write_text("some log content")
        result = archive_log_files(self.log_dir, "2023-10-27")
        self.assertEqual(result[0].name, "app-2023-10-27.log")