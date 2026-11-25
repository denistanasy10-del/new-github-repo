"""Command-line entry point for FrameFlow."""

import argparse
from pathlib import Path

from frameflow.analysis import (
    copy_organization,
    find_exact_duplicates,
    plan_organization,
)
from frameflow.scanner import scan_folder


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Review and safely organize local photo collections."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    scan_parser = commands.add_parser("scan", help="List supported image files")
    scan_parser.add_argument("folder", type=Path, help="Folder to scan recursively")

    duplicates_parser = commands.add_parser(
        "duplicates", help="Find byte-identical image files"
    )
    duplicates_parser.add_argument(
        "folder", type=Path, help="Folder to scan recursively"
    )

    organize_parser = commands.add_parser(
        "organize", help="Preview or copy images into date-based folders"
    )
    organize_parser.add_argument("folder", type=Path, help="Source photo folder")
    organize_parser.add_argument("destination", type=Path, help="Copy destination")
    organize_parser.add_argument(
        "--apply",
        action="store_true",
        help="Copy files (default is preview only; originals are kept)",
    )

    args = parser.parse_args()
    try:
        if args.command == "scan":
            _scan(args.folder)
        elif args.command == "duplicates":
            _duplicates(args.folder)
        else:
            _organize(args.folder, args.destination, args.apply)
    except (OSError, ValueError) as error:
        parser.error(str(error))


def _scan(folder: Path) -> None:
    images = scan_folder(folder)
    root = Path(folder).expanduser().resolve()
    total_bytes = sum(image.size_bytes for image in images)
    for image in images:
        print(f"{image.path.relative_to(root)}\t{image.size_bytes} bytes")
    print(f"Found {len(images)} image(s), {total_bytes} bytes total.")


def _duplicates(folder: Path) -> None:
    groups = find_exact_duplicates(scan_folder(folder))
    if not groups:
        print("No exact duplicates found.")
        return
    for group in groups:
        print(f"SHA-256 {group.sha256}")
        for image in group.files:
            print(f"  {image.path}\t{image.size_bytes} bytes")
    print(f"Found {len(groups)} duplicate group(s). No files were changed.")


def _organize(folder: Path, destination: Path, apply: bool) -> None:
    plan = plan_organization(folder, destination)
    if not plan:
        print("No supported images found.")
        return
    for item in plan:
        print(f"{item.source} -> {item.destination}")
    if not apply:
        print(
            f"Preview only: {len(plan)} file(s). "
            "Run again with --apply to copy; originals will be kept."
        )
        return
    copied = copy_organization(plan)
    print(f"Copied {len(copied)} file(s). Originals were kept.")


if __name__ == "__main__":
    main()
