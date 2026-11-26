# Contributing

Thanks for helping make FrameFlow useful, safe, and easy to understand.

## Before you start

- Check [open issues](https://github.com/denistanasy10-del/new-github-repo/issues) for existing discussion.
- For larger changes, open an issue first so the approach can be discussed.
- Keep pull requests focused and describe the user-facing change.

## Set up locally

FrameFlow supports Python 3.11 and newer and has no runtime dependencies.

```bash
git clone https://github.com/denistanasy10-del/new-github-repo.git
cd new-github-repo
python -m venv .venv
```

Activate `.venv`:

```bash
# macOS / Linux
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install and run the checks:

```bash
python -m pip install -e ".[dev]"
python -m unittest discover -s tests -v
ruff check src tests
```

## Pull requests

- Add or update tests for behavior changes.
- Run the full test suite before opening a PR.
- Update the README when commands or user-visible behavior change.
- Preserve the project's local-first, non-destructive defaults.
- Never include private photos, credentials, or personal metadata in tests or examples.

## Reporting a bug

Include your operating system, Python version, command used, expected result, and actual result. Use synthetic or public sample files; do not attach private photos or EXIF data.
