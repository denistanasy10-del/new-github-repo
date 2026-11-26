import os
import tempfile
import unittest
from pathlib import Path

from frameflow.analysis import (
    copy_organization,
    find_exact_duplicates,
    plan_organization,
)
from frameflow.scanner import scan_folder


class DuplicateTests(unittest.TestCase):
    def test_groups_identical_contents_but_not_same_sized_different_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            folder = Path(temporary_directory)
            (folder / "first.jpg").write_bytes(b"same")
            (folder / "second.png").write_bytes(b"same")
            (folder / "different.webp").write_bytes(b"else")

            groups = find_exact_duplicates(scan_folder(folder), chunk_size=2)

            self.assertEqual(len(groups), 1)
            self.assertEqual(
                {image.path.name for image in groups[0].files},
                {"first.jpg", "second.png"},
            )
            self.assertEqual(len(groups[0].sha256), 64)

    def test_rejects_invalid_chunk_size(self) -> None:
        with self.assertRaises(ValueError):
            find_exact_duplicates([], chunk_size=0)


class OrganizationTests(unittest.TestCase):
    def test_preview_and_copy_preserve_source_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source"
            destination = root / "organized"
            source.mkdir()
            image = source / "photo.jpg"
            image.write_bytes(b"original")

            plan = plan_organization(source, destination)

            self.assertEqual(len(plan), 1)
            self.assertEqual(plan[0].destination.parent.parent, destination)
            self.assertFalse(destination.exists())

            copied = copy_organization(plan)

            self.assertEqual(copied, [plan[0].destination])
            self.assertEqual(image.read_bytes(), b"original")
            self.assertEqual(copied[0].read_bytes(), b"original")

    def test_uses_collision_safe_names_and_never_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source"
            source.mkdir()
            (source / "photo.jpg").write_bytes(b"one")
            (source / "other").mkdir()
            (source / "other" / "photo.jpg").write_bytes(b"two")
            destination = root / "organized"

            plan = plan_organization(source, destination)

            self.assertEqual(len({item.destination.name for item in plan}), 2)

            conflict = plan[-1].destination
            conflict.parent.mkdir(parents=True)
            conflict.write_bytes(b"do not replace")
            with self.assertRaises(FileExistsError):
                copy_organization(plan)
            self.assertEqual(conflict.read_bytes(), b"do not replace")
            self.assertTrue(all(item.source.exists() for item in plan))
            self.assertFalse(plan[0].destination.exists())

    def test_refuses_to_copy_a_file_changed_after_preview(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source"
            source.mkdir()
            image = source / "photo.jpg"
            image.write_bytes(b"before")
            plan = plan_organization(source, root / "organized")
            image.write_bytes(b"after!")
            os.utime(
                image,
                ns=(plan[0].modified_at_ns, plan[0].modified_at_ns + 1_000_000_000),
            )

            with self.assertRaisesRegex(ValueError, "changed since preview"):
                copy_organization(plan)
            self.assertFalse(plan[0].destination.exists())
            self.assertEqual(image.read_bytes(), b"after!")

    def test_rejects_nested_source_and_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            source = Path(temporary_directory) / "photos"
            source.mkdir()

            with self.assertRaises(ValueError):
                plan_organization(source, source / "organized")


if __name__ == "__main__":
    unittest.main()
