<div align="center">

# FrameFlow

### Spend less time sorting. Spend more time creating.

Local-first tools for finding, reviewing, and safely organizing photo collections.

[![Tests](https://github.com/denistanasy10-del/new-github-repo/actions/workflows/tests.yml/badge.svg)](https://github.com/denistanasy10-del/new-github-repo/actions/workflows/tests.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-2ea44f.svg)](LICENSE)

</div>

FrameFlow is a small, privacy-minded command-line app for taking the first steps toward a tidy photo library. It scans image folders, finds byte-for-byte duplicates, and previews date-based organization before copying anything.

> **Early release:** The CLI described here is implemented. A desktop app, EXIF-based sorting, thumbnails, and a persistent catalog are not available yet.

## What it can do

- **Scan locally** for common image and camera RAW file extensions, recursively.
- **Find exact duplicates** with streaming SHA-256 hashes. Files are never removed.
- **Preview organization** into folders by file modification date.
- **Copy on confirmation** with collision-safe names. The original library stays untouched.
- **Keep you in control:** preview is the default, source/destination overlap is rejected, and files changed after preview are not copied.
- **Stay lightweight:** Python 3.11+, no runtime dependencies, and no network access.

## Get started

Install from a checkout:

```bash
git clone https://github.com/denistanasy10-del/new-github-repo.git
cd new-github-repo
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install FrameFlow:

```bash
python -m pip install -e .
```

## Commands

### Scan a folder

```bash
frameflow scan ~/Pictures
```

Lists supported files and reports the total image count and size. The scan is read-only and does not follow symbolic links.

### Find exact duplicates

```bash
frameflow duplicates ~/Pictures
```

Only files with matching SHA-256 hashes are reported as duplicates. Similar-looking photos and resized or re-encoded copies are not detected.

### Preview, then copy into date folders

```bash
# Preview only; does not create or change files
frameflow organize ~/Pictures ~/Pictures-organized

# Explicitly copy the planned files; originals are kept
frameflow organize ~/Pictures ~/Pictures-organized --apply
```

The destination is grouped by each image's **file modification date**, not its EXIF capture date. If names collide, FrameFlow adds a numbered suffix instead of overwriting. If a source file changes after the preview, the copy is stopped.

### See all options

```bash
frameflow --help
frameflow organize --help
frameflow --version
```

## Supported extensions

JPEG, PNG, GIF, BMP, TIFF, WebP, HEIC, and common RAW extensions: ARW, CR2, CR3, DNG, NEF, ORF, PEF, RAF, RW2, and SRW.

FrameFlow currently identifies files by extension. It does not decode, validate, generate thumbnails, or read image metadata.

## Safety and privacy

- Everything runs on your computer; photos and metadata are not uploaded.
- Scanning and duplicate detection never change files.
- Organization is a preview by default and copies only when `--apply` is supplied.
- Original files are never moved or deleted.
- Existing destination files are not overwritten.
- Symbolic links are skipped during scans.

Keep a backup before applying bulk file operations, as with any photo workflow.

## Development

```bash
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -v
ruff check src tests
```

The test suite uses Python's standard library; Ruff checks code style. GitHub Actions runs tests on Python 3.11, 3.12, and 3.13 across Ubuntu, macOS, and Windows.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development and pull request workflow.

## Roadmap

The current release is intentionally focused on safe file discovery and organization. Potential next steps:

- EXIF capture-date and camera metadata
- A local searchable catalog
- Thumbnail review and keyboard-first photo triage
- Similarity detection for near-duplicate images
- A cross-platform desktop interface

These are ideas, not promises or currently available features. Suggestions and focused contributions are welcome via [GitHub Issues](https://github.com/denistanasy10-del/new-github-repo/issues).

## License

FrameFlow is available under the [MIT License](LICENSE).
