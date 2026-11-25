"""Non-destructive discovery of image files."""

from dataclasses import dataclass
import os
from pathlib import Path


IMAGE_EXTENSIONS = frozenset(
    {
        ".arw",
        ".bmp",
        ".cr2",
        ".cr3",
        ".dng",
        ".gif",
        ".heic",
        ".jpeg",
        ".jpg",
        ".nef",
        ".orf",
        ".pef",
        ".png",
        ".raf",
        ".rw2",
        ".srw",
        ".tif",
        ".tiff",
        ".webp",
    }
)


@dataclass(frozen=True)
class ImageFile:
    path: Path
    size_bytes: int


def scan_folder(folder: Path) -> list[ImageFile]:
    """Return supported image files below a folder without modifying them."""
    folder = Path(folder).expanduser()
    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")

    folder = folder.resolve()
    images: list[ImageFile] = []

    def raise_walk_error(error: OSError) -> None:
        raise error

    for current, directories, filenames in os.walk(
        folder, followlinks=False, onerror=raise_walk_error
    ):
        current_path = Path(current)
        directories[:] = sorted(
            name
            for name in directories
            if not (current_path / name).is_symlink()
        )
        for filename in filenames:
            path = current_path / filename
            if path.suffix.lower() not in IMAGE_EXTENSIONS or path.is_symlink():
                continue
            if not path.is_file():
                continue
            images.append(ImageFile(path=path, size_bytes=path.stat().st_size))

    return sorted(images, key=lambda image: str(image.path).casefold())
