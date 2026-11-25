import tempfile
import unittest
from pathlib import Path

from frameflow.scanner import scan_folder


class ScanFolderTests(unittest.TestCase):
    def test_finds_images_recursively_and_ignores_other_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            nested = folder / "trip"
            nested.mkdir()
            (folder / "cover.JPG").write_bytes(b"photo")
            (nested / "view.png").write_bytes(b"png")
            (folder / "notes.txt").write_text("not an image")

            images = scan_folder(folder)

            self.assertEqual(
                [(image.path.name, image.size_bytes) for image in images],
                [("cover.JPG", 5), ("view.png", 3)],
            )

    def test_rejects_missing_folder(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            missing = Path(temporary_directory) / "missing"

            with self.assertRaises(FileNotFoundError):
                scan_folder(missing)

    def test_rejects_file_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            file_path = Path(temporary_directory) / "photo.jpg"
            file_path.touch()

            with self.assertRaises(NotADirectoryError):
                scan_folder(file_path)

    def test_does_not_follow_symbolic_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory) / "photos"
            outside = Path(temporary_directory) / "outside"
            folder.mkdir()
            outside.mkdir()
            (outside / "linked.jpg").write_bytes(b"photo")
            try:
                (folder / "linked.jpg").symlink_to(outside / "linked.jpg")
                (folder / "linked-folder").symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest("Symbolic links are not available")

            self.assertEqual(scan_folder(folder), [])


if __name__ == "__main__":
    unittest.main()
