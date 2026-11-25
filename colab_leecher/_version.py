# copyright 2023 © Xron Trix | https://github.com/Xrontrix10
"""Single source of truth for the bot's version and build metadata.

This module imports nothing from the rest of the package, so it can be
read without credentials.json:

    python colab_leecher/_version.py
"""

import platform
import subprocess
from functools import lru_cache
from importlib import metadata
from pathlib import Path

__version__ = "0.1.1"

APP_NAME = "Telegram Leecher (lokal)"
UPSTREAM = "https://github.com/XronTrix10/Telegram-Leecher"
LICENSE = "GPL-3.0"

_ROOT = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=1)
def git_build() -> str:
    """Return the output of `git describe`, or "" when git is unavailable.

    Examples: "v0.1.1" (exactly on a tag), "v0.1.1-3-g1a2b3c4" (three
    commits after the tag), "v0.1.1-3-g1a2b3c4-dirty" (uncommitted changes).
    """
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--always", "--dirty"],
            cwd=_ROOT,
            capture_output=True,
            text=True,
            timeout=3,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def _package_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "not installed"


def version_text() -> str:
    """One-line version string, e.g. "Telegram Leecher (lokal) v0.1.1 (v0.1.1-3-g1a2b3c4)"."""
    text = f"{APP_NAME} v{__version__}"
    build = git_build()
    if build and build != f"v{__version__}":
        text += f" ({build})"
    return text


def details() -> str:
    """Multi-line metadata block used by /version."""
    lines = [
        f"Version : {__version__}",
        f"Build   : {git_build() or 'unknown (no git)'}",
        f"Python  : {platform.python_version()}",
        f"pyrofork: {_package_version('pyrofork')}",
        f"yt-dlp  : {_package_version('yt-dlp')}",
        f"License : {LICENSE}",
        f"Upstream: {UPSTREAM}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(version_text())
