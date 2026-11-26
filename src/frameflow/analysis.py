"""Content-based analysis for photo collections."""

import hashlib
import os
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from frameflow.scanner import ImageFile, scan_folder


@dataclass(frozen=True)
class DuplicateGroup:
    sha256: str
    files: tuple[ImageFile, ...]


def find_exact_duplicates(
    images: list[ImageFile], chunk_size: int = 1024 * 1024
) -> list[DuplicateGroup]:
    """Find byte-identical files, hashing in chunks to bound memory use."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    candidates: dict[int, list[ImageFile]] = {}
    for image in images:
        candidates.setdefault(image.size_bytes, []).append(image)

    groups: dict[str, list[ImageFile]] = {}
    for same_size_images in candidates.values():
        if len(same_size_images) < 2:
            continue
        for image in same_size_images:
            digest = hashlib.sha256()
            with image.path.open("rb") as file:
                for chunk in iter(lambda: file.read(chunk_size), b""):
                    digest.update(chunk)
            groups.setdefault(digest.hexdigest(), []).append(image)

    duplicates = [
        DuplicateGroup(sha256=digest, files=tuple(sorted(files, key=_path_key)))
        for digest, files in groups.items()
        if len(files) > 1
    ]
    return sorted(duplicates, key=lambda group: _path_key(group.files[0]))


def _path_key(image: ImageFile) -> str:
    return str(image.path).casefold()


@dataclass(frozen=True)
class PlannedCopy:
    source: Path
    destination: Path
    size_bytes: int
    modified_at_ns: int


def plan_organization(source: Path, destination: Path) -> list[PlannedCopy]:
    """Plan a non-destructive copy into folders grouped by file modification date."""
    source = Path(source).expanduser().resolve(strict=True)
    if not source.is_dir():
        raise NotADirectoryError(f"Not a folder: {source}")

    destination = Path(destination).expanduser().resolve()
    if (
        destination == source
        or source in destination.parents
        or destination in source.parents
    ):
        raise ValueError("Source and destination folders must not contain each other.")
    if destination.exists() and not destination.is_dir():
        raise NotADirectoryError(f"Destination is not a folder: {destination}")

    images = scan_folder(source)
    reserved: set[str] = set()
    plan: list[PlannedCopy] = []

    for image in images:
        source_stat = image.path.stat()
        if source_stat.st_size != image.size_bytes:
            raise ValueError(f"Image changed while scanning: {image.path}")
        day = datetime.fromtimestamp(source_stat.st_mtime).strftime("%Y-%m-%d")
        target_directory = destination / day
        target = target_directory / image.path.name
        stem, suffix = image.path.stem, image.path.suffix
        counter = 2
        while target.exists() or str(target).casefold() in reserved:
            target = target_directory / f"{stem} ({counter}){suffix}"
            counter += 1
        reserved.add(str(target).casefold())
        plan.append(
            PlannedCopy(
                source=image.path,
                destination=target,
                size_bytes=image.size_bytes,
                modified_at_ns=source_stat.st_mtime_ns,
            )
        )

    return plan


def copy_organization(plan: list[PlannedCopy]) -> list[Path]:
    """Copy planned files without overwriting existing files or removing originals."""
    copied: list[Path] = []
    try:
        for item in plan:
            item.destination.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=".frameflow-", suffix=".tmp", dir=item.destination.parent
            )
            temporary = Path(temporary_name)
            try:
                with (
                    os.fdopen(descriptor, "wb") as destination_file,
                    item.source.open("rb") as source_file,
                ):
                    before = os.fstat(source_file.fileno())
                    _ensure_source_matches(item, before)
                    shutil.copyfileobj(source_file, destination_file)
                    after = os.fstat(source_file.fileno())
                    _ensure_source_matches(item, after)
                if temporary.stat().st_size != item.size_bytes:
                    raise ValueError(f"Image changed while copying: {item.source}")
                shutil.copystat(item.source, temporary)
                os.link(temporary, item.destination)
            finally:
                temporary.unlink(missing_ok=True)
            copied.append(item.destination)
    except Exception:
        for path in reversed(copied):
            path.unlink(missing_ok=True)
        raise
    return copied


def _ensure_source_matches(item: PlannedCopy, source_stat: os.stat_result) -> None:
    if (
        source_stat.st_size != item.size_bytes
        or source_stat.st_mtime_ns != item.modified_at_ns
    ):
        raise ValueError(f"Image changed since preview: {item.source}")
