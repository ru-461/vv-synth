"""Manage output paths for synthesized audio artifacts."""

from __future__ import annotations

from pathlib import Path
from time import strftime

# Default output directory for artifacts such as synthesized WAV files.
DEFAULT_OUTPUT_DIR = Path("output")


def ensure_output_dir(output_dir: Path) -> Path:
    """Create the output directory if it does not exist.

    Args:
        output_dir: Directory to create.

    Returns:
        Path to the created directory.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    return output_dir


def resolve_output_file(
    *,
    output_dir: Path,
    filename: Path | None = None,
) -> Path:
    """Resolve the destination path for an artifact WAV file.

    When ``filename`` is omitted, use a timestamped name under ``output_dir``.
    When only a file name is provided, place it under ``output_dir``.
    When a path with directories is provided, use that path as-is.

    Args:
        output_dir: Directory that stores artifacts.
        filename: Output file name or path. Auto-generated when None.

    Returns:
        Destination file path.
    """
    if filename is None:
        timestamp = strftime("%Y%m%d-%H%M%S")
        return ensure_output_dir(output_dir) / f"{timestamp}.wav"

    if filename.parent.parts:
        ensure_output_dir(filename.parent)
        return filename

    return ensure_output_dir(output_dir) / filename.name
