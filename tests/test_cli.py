import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from frameflow.cli import main


class CliTests(unittest.TestCase):
    def test_scan_reports_image_count_and_total_size(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            (folder / "photo.jpg").write_bytes(b"abc")
            output = io.StringIO()
            with (
                patch("sys.argv", ["frameflow", "scan", str(folder)]),
                contextlib.redirect_stdout(output),
            ):
                main()

            self.assertIn("photo.jpg\t3 B", output.getvalue())
            self.assertIn("Found 1 image (3 B total).", output.getvalue())

    def test_organize_defaults_to_preview_and_keeps_source_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "photos"
            destination = root / "organized"
            source.mkdir()
            photo = source / "photo.jpg"
            photo.write_bytes(b"original")
            output = io.StringIO()

            with (
                patch(
                    "sys.argv",
                    ["frameflow", "organize", str(source), str(destination)],
                ),
                contextlib.redirect_stdout(output),
            ):
                main()

            self.assertIn("Preview only: 1 file(s).", output.getvalue())
            self.assertEqual(photo.read_bytes(), b"original")
            self.assertFalse(destination.exists())

    def test_duplicates_reports_identical_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            (folder / "one.jpg").write_bytes(b"same")
            (folder / "two.jpg").write_bytes(b"same")
            output = io.StringIO()
            with (
                patch("sys.argv", ["frameflow", "duplicates", str(folder)]),
                contextlib.redirect_stdout(output),
            ):
                main()

            self.assertIn("Found 1 duplicate group(s).", output.getvalue())
            self.assertIn("one.jpg", output.getvalue())
            self.assertIn("two.jpg", output.getvalue())

    def test_version_option_reports_installed_version(self) -> None:
        output = io.StringIO()
        with (
            patch("sys.argv", ["frameflow", "--version"]),
            contextlib.redirect_stdout(output),
            self.assertRaises(SystemExit) as result,
        ):
            main()

        self.assertEqual(result.exception.code, 0)
        self.assertIn("frameflow 0.1.0", output.getvalue())


if __name__ == "__main__":
    unittest.main()
