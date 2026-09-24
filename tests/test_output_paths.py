"""Tests for ``vv_synth.output_paths``."""

from __future__ import annotations

from pathlib import Path

from vv_synth.output_paths import ensure_output_dir, resolve_output_file


def test_ensure_output_dir_creates_when_missing(tmp_path: Path) -> None:
    target = tmp_path / "new_dir"
    assert not target.exists()

    result = ensure_output_dir(target)

    assert result == target
    assert target.is_dir()


def test_ensure_output_dir_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / "existing"
    target.mkdir()

    result = ensure_output_dir(target)

    assert result == target
    assert target.is_dir()


def test_resolve_output_file_uses_timestamp_when_no_filename(tmp_path: Path) -> None:
    result = resolve_output_file(output_dir=tmp_path)

    assert result.parent == tmp_path
    assert result.suffix == ".wav"
    # Timestamp stem format is "YYYYMMDD-HHMMSS".
    assert len(result.stem) == 15
    assert result.stem[8] == "-"
    assert tmp_path.is_dir()


def test_resolve_output_file_places_basename_under_output_dir(tmp_path: Path) -> None:
    result = resolve_output_file(output_dir=tmp_path, filename=Path("hello.wav"))

    assert result == tmp_path / "hello.wav"
    assert tmp_path.is_dir()


def test_resolve_output_file_keeps_explicit_path(tmp_path: Path) -> None:
    explicit = tmp_path / "sub" / "audio.wav"

    result = resolve_output_file(
        output_dir=tmp_path / "ignored",
        filename=explicit,
    )

    assert result == explicit
    assert explicit.parent.is_dir()
    # The fallback output_dir is not created when an explicit path is given.
    assert not (tmp_path / "ignored").exists()
