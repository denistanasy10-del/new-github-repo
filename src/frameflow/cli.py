"""Command-line entry point for FrameFlow."""

import argparse
from pathlib import Path

from frameflow import __version__
from frameflow.analysis import (
    copy_organization,
    find_exact_duplicates,
    plan_organization,
)
from frameflow.scanner import scan_folder


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="frameflow",
        description="Find and safely organize images in local photo collections.",
        epilog="All commands run locally. Source files are never moved or deleted.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
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
        print(f"{image.path.relative_to(root)}\t{_format_size(image.size_bytes)}")
    image_label = "image" if len(images) == 1 else "images"
    print(f"\nFound {len(images)} {image_label} ({_format_size(total_bytes)} total).")


def _duplicates(folder: Path) -> None:
    groups = find_exact_duplicates(scan_folder(folder))
    if not groups:
        print("No exact duplicates found.")
        return
    root = Path(folder).expanduser().resolve()
    for index, group in enumerate(groups, start=1):
        print(f"Duplicate group {index} | SHA-256 {group.sha256}")
        for image in group.files:
            print(f"  {image.path.relative_to(root)}\t{_format_size(image.size_bytes)}")
    print(f"\nFound {len(groups)} duplicate group(s). No files were changed.")


def _organize(folder: Path, destination: Path, apply: bool) -> None:
    plan = plan_organization(folder, destination)
    if not plan:
        print("No supported images found.")
        return
    for item in plan:
        print(
            f"{item.source.relative_to(Path(folder).expanduser().resolve())}"
            f"  ->  {item.destination}"
        )
    if not apply:
        print(
            f"Preview only: {len(plan)} file(s). "
            "Run again with --apply to copy; originals will be kept."
        )
        return
    copied = copy_organization(plan)
    print(f"Copied {len(copied)} file(s). Originals were kept.")


def _format_size(size_bytes: int) -> str:
    size = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1000 or unit == "TB":
            if unit == "B":
                return f"{size_bytes} B"
            return f"{size:.1f} {unit}"
        size /= 1000
    return f"{size_bytes} B"


if __name__ == "__main__":
    main()
