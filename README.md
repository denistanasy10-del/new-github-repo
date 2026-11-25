FrameFlow

<p align="center">
  <strong>Spend less time sorting. Spend more time creating.</strong>
</p>

FrameFlow is an open-source photo organization tool designed to turn messy folders and large photo dumps into structured, searchable collections. It helps creators quickly review, group, filter, and organize images—without moving, modifying, or deleting originals unless the user explicitly chooses to.

Project status: Early development. The CLI supports local scanning, exact duplicate detection, and preview-first date-based copying. The desktop application, image metadata extraction, and other features below are planned.

Why FrameFlow?

After a shoot, trip, event, or everyday capture session, photographers can end up with hundreds or thousands of files that need to be reviewed. Finding the best shots, separating images by date or camera, spotting duplicates, and building a clean folder structure can consume more time than the creative work itself.

FrameFlow aims to make that process fast, predictable, and user-controlled.

Core principles

•	Local-first: Your photo library stays on your device. Cloud upload is not required.
•	Non-destructive by default: Original files are never edited or deleted as part of automatic organization.
•	Fast review: Designed for large folders and keyboard-friendly workflows.
•	Transparent automation: Every proposed grouping or action can be reviewed before it is applied.
•	Open and extensible: A modular architecture allows new sorting rules and analysis features to be added.

Planned features

Rapid photo triage

•	Browse large collections in a streamlined review interface.
•	Mark images as keep, reject, favorite, or review later.
•	Navigate and rate images with keyboard shortcuts.
•	Filter by file type, capture date, dimensions, camera metadata, and rating.

Smart organization

•	Group photos by capture date, time range, camera, lens, file type, and user-defined rules.
•	Preview folder structures before applying changes.
•	Generate suggested collections for events, trips, and shoots.
•	Export organization plans for review.

Duplicate and similarity detection

•	Detect exact duplicates using SHA-256 file hashes.
•	Explore near-duplicate detection using perceptual image hashes.
•	Identify image sequences and visually similar shots.
•	Keep the user in control when deciding which versions to retain.

Metadata-aware browsing

•	Read supported EXIF metadata, including capture date, camera model, lens, exposure information, and image dimensions.
•	Search and filter using available metadata.
•	Clearly indicate when metadata is missing or unavailable.

Safe file operations

•	Preview rename and move operations before execution.
•	Avoid overwriting files by using collision-safe naming.
•	Keep an operation log where possible.
•	Support undo for reversible organization operations where feasible.

Workflow presets

•	Create reusable sorting presets for weddings, events, travel, studio sessions, product photography, and personal archives.
•	Customize rules instead of relying on one fixed folder structure.

Example workflow

1.	Select a folder containing images.
2.	Let FrameFlow scan file names, file properties, and available metadata.
3.	Review suggested groups, duplicates, and sorting options.
4.	Adjust the rules or manually review selected images.
5.	Preview the resulting folder structure and file operations.
6.	Apply the changes only after confirmation.

Design goals

Goal	Approach
Speed	Efficient scanning, caching, and responsive browsing
Safety	Non-destructive defaults and confirmation before file operations
Privacy	Local processing by default; no required cloud account
Clarity	Explain why an image was grouped or flagged
Flexibility	Configurable rules and workflow presets
Accessibility	Keyboard navigation and clear interface states

Proposed technology stack

The initial implementation is planned around a cross-platform desktop application.

•	Language: Python
•	Desktop UI: PySide6 / Qt
•	Image metadata: ExifTool integration or compatible metadata libraries
•	Image processing: Pillow
•	Duplicate detection: SHA-256 for exact duplicates; perceptual hashing for similarity experiments
•	Local catalog: SQLite
•	Testing: Python unittest
•	Packaging: PyInstaller or platform-specific packaging tools

Technology choices may evolve as development and performance testing progress.

Planned architecture

FrameFlow is planned as a modular application with clear boundaries between the interface, catalog, scanning, analysis, and file operations.

┌──────────────────────────────────────────────────────────────┐
│                      FrameFlow UI                          │
│          Browse · Review · Filter · Organize               │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                    Application Layer                       │
│       Workflows · Commands · Preferences · Presets          │
└──────────────┬──────────────────────────────┬───────────────┘
               │                             │
┌──────────────▼──────────────┐  ┌───────────▼───────────────┐
│      Media Catalog        │  │     Analysis Engine       │
│ SQLite · Metadata · Cache │  │ Hashes · Similarity ·     │
│                           │  │ Rule-based grouping       │
└──────────────┬──────────────┘  └───────────┬───────────────┘
               │                             │
┌──────────────▼─────────────────────────────▼───────────────┐
│                   File System Layer                       │
│       Scan · Preview · Rename · Move · Export             │
│            Non-destructive operation logic                 │
└────────────────────────────────────────────────────────────┘

Current repository structure

.
├── .github/workflows/tests.yml
├── README.md
├── pyproject.toml
├── src/frameflow/
│   ├── analysis.py
│   ├── cli.py
│   └── scanner.py
└── tests/
    ├── test_analysis.py
    ├── test_cli.py
    └── test_scanner.py

The desktop application and local SQLite catalog remain planned.

Proposed future architecture

frameflow/
├── pyproject.toml
├── src/
│   └── frameflow/
│       ├── __init__.py
│       ├── app.py
│       ├── ui/
│       │   ├── main_window.py
│       │   └── review_view.py
│       ├── catalog/
│       │   ├── database.py
│       │   └── models.py
│       ├── scanner/
│       │   ├── file_scanner.py
│       │   └── metadata_reader.py
│       ├── analysis/
│       │   ├── duplicate_detection.py
│       │   └── grouping_rules.py
│       ├── organizer/
│       │   ├── operation_preview.py
│       │   └── file_operations.py
│       └── settings/
│           └── preferences.py
└── tests/
    ├── test_scanner.py
    ├── test_metadata.py
    └── test_organizer.py

This future structure is an architectural proposal and may change as the project evolves.

Installation

Install the project locally with Python 3.11 or newer:

```bash
python -m pip install -e .
```

Scan a folder recursively. FrameFlow reads files locally and never uploads or alters source images:

```bash
frameflow scan /path/to/photos
```

Find byte-identical images:

```bash
frameflow duplicates /path/to/photos
```

Preview a copy-based organization by each file's modified date, then explicitly apply it:

```bash
frameflow organize /path/to/photos /path/to/organized
frameflow organize /path/to/photos /path/to/organized --apply
```

Run the test suite with the Python standard library:

```bash
python -m unittest discover -s tests
```

Planned prerequisites

•	Python 3.11+
•	Git
•	Supported desktop operating system (initial platform support will be documented during development)

Development setup

git clone https://github.com/USERNAME/frameflow.git
cd frameflow

python -m venv .venv

Activate the environment:

macOS / Linux

source .venv/bin/activate

Windows

.venv\Scripts\activate

Install the project in editable mode:

pip install -e .

Organization uses filesystem modification dates, not EXIF capture dates. It copies rather than moves, keeps originals, chooses collision-safe names, and refuses to overwrite existing files. The default organization command is preview-only. Desktop UI and EXIF metadata extraction are not implemented yet.

Privacy and file safety

FrameFlow is intended to work with personal and professional media libraries, which can contain sensitive information.

The project is guided by these safeguards:

•	No mandatory cloud upload.
•	No automatic destructive actions.
•	Preview file operations before applying them.
•	Preserve source files during scanning and analysis.
•	Make automated recommendations reviewable.
•	Document any optional network-connected functionality clearly.

Roadmap

Phase 1 — Foundation

☑	Establish project structure and development tooling.
☐	Build a cross-platform desktop shell.
☑	Implement folder scanning.
☐	Create a local SQLite catalog.
☑	Extract basic file properties (size and modification time).
☐	Extract image metadata.

Phase 2 — Fast review

☐	Build thumbnail grid and image preview.
☐	Add keyboard-first photo triage.
☐	Implement favorites, review status, and filtering.
☐	Add responsive catalog updates during scanning.

Phase 3 — Organization

☐	Add configurable grouping rules.
☐	Preview folder structure and rename operations.
☐	Implement safe move and rename workflows.
☐	Add collision handling and operation history.

Phase 4 — Duplicate intelligence

☑	Exact duplicate detection.
☐	Perceptual similarity experiments.
☐	Similar-image review groups.
☐	User-controlled decisions for duplicate candidates.

Phase 5 — Release and community

☐	Cross-platform packaging evaluation.
☐	Documentation and accessibility review.
☑	Automated test coverage for critical file operations.
☐	Publish an initial alpha release.
☐	Gather feedback and prioritize community contributions.

Roadmap items are goals, not release commitments.

Contributing

Contributions, ideas, bug reports, documentation improvements, and thoughtful feedback are welcome.

Before contributing:

1.	Check existing issues to avoid duplicate work.
2.	Open an issue to discuss larger changes or new features.
3.	Keep pull requests focused and explain the problem they solve.
4.	Add or update tests for behavior changes.
5.	Update documentation when workflows or configuration change.

Areas where contributions would be valuable

•	User experience and accessibility
•	Cross-platform compatibility
•	Image metadata support
•	Performance and memory optimization
•	Duplicate detection research
•	Sorting rules and workflow presets
•	Documentation and translations
•	Automated testing

Please be respectful and constructive in discussions. The goal is to build a tool that is useful to photographers and creators with different workflows and levels of technical experience.

Reporting issues

When opening an issue, include:

•	Operating system and version
•	FrameFlow version or commit, if available
•	Steps to reproduce the issue
•	Expected behavior
•	Actual behavior
•	Relevant logs or screenshots (remove private information)

Never upload private photographs or sensitive metadata unless you have intentionally reviewed and consented to sharing them.

Community and discussions

Community channels will be established as the project matures. Until then, use the repository's GitHub Issues for bug reports, feature requests, and development discussions.

License

FrameFlow is intended to be released under the MIT License. The license will apply once the repository's LICENSE file is added and confirmed.

Project vision

The best photo workflow is one that gets out of the way.

FrameFlow aims to transform the overwhelming first step of managing a photo collection into a simple, fast, and intuitive process—so creators can spend less time searching through files and more time making something meaningful.

Sort less. Create more.