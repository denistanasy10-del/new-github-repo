<div align="center">

<img src="assets/frameflow-mark.svg" width="88" height="88" alt="FrameFlow camera lens logo" />

# FrameFlow

**Spend less time sorting. Spend more time creating.**

An elegant, local-first command-line toolkit for bringing order to your photo library.

[![Tests](https://github.com/denistanasy10-del/new-github-repo/actions/workflows/tests.yml/badge.svg)](https://github.com/denistanasy10-del/new-github-repo/actions/workflows/tests.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-2ea44f.svg)](LICENSE)

<br />

[Get started](#get-started) · [Commands](#commands) · [Safety](#safety-by-design) · [Roadmap](#roadmap)

</div>

FrameFlow makes the first pass through a messy photo folder feel simple. Scan what you have, find exact duplicates, and plan a clean date-based layout—all from your terminal, with your files staying on your device.

> **Early release · CLI available**
> Desktop browsing, EXIF capture dates, thumbnails, and a persistent catalog are not part of this release.

## At a glance

| Discover | Compare | Organize |
|:--|:--|:--|
| Recursively scan common image and camera RAW formats. | Find byte-for-byte duplicates with streaming SHA-256. | Preview a date-based layout, then explicitly copy when ready. |

No cloud account. No runtime dependencies. No moving or deleting originals.

## Get started

### Install

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

### Your first scan

```console
$ frameflow scan ~/Pictures/Weekend
IMG_1024.JPG    4.8 MB
IMG_1025.JPG    5.1 MB

Found 2 images (9.9 MB total).
```

## Commands

### Scan a folder

```bash
frameflow scan ~/Pictures
```

Lists supported files with readable sizes and reports a total. Scanning is read-only and symbolic links are skipped.

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

## Safety by design

| Default | Guarantee |
|:--|:--|
| **Local-only** | No photos or metadata are uploaded. FrameFlow makes no network requests. |
| **Read-only scan** | Scanning and duplicate detection never change your library. |
| **Preview first** | Organization shows the proposed layout; `--apply` is required to copy. |
| **Keep originals** | Files are copied, never moved or deleted. |
| **No silent overwrite** | Name collisions get a numbered suffix; existing files are left untouched. |
| **Change-aware** | A source file that changes after preview is rejected during copying. |

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
