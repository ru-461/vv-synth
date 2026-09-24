"""Tests for the ``vv-synth`` Typer CLI in ``main.py``."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import patch

from typer.testing import CliRunner

from main import app
from vv_synth.engine_client import EngineClientError

if TYPE_CHECKING:
    from pathlib import Path
    from unittest.mock import MagicMock

    from typer.testing import Result

runner = CliRunner()


def _stderr_lines(result: Result) -> list[str]:
    """Return non-empty stderr lines; ``typer.echo(err=True)`` writes there."""
    return [line for line in result.stderr.splitlines() if line.strip()]


def test_help_is_english() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "VOICEVOX" in result.stdout
    assert "Synthesize" in result.stdout


def test_usage_names_message_argument() -> None:
    result = runner.invoke(app, ["--help"])

    # README and the skills document the argument as MESSAGE.
    usage = result.stdout.splitlines()[0]
    assert usage.startswith("Usage:")
    assert "MESSAGE" in usage


def test_no_args_shows_help() -> None:
    result = runner.invoke(app, [])

    # ``no_args_is_help=True`` triggers a usage/help message.
    assert result.exit_code != 0
    assert "Usage" in result.stdout or "Usage" in (result.stderr or "")


@patch("main.synthesize_text_to_file")
def test_synthesize_success(
    mock_synth: MagicMock,
    tmp_path: Path,
) -> None:
    output = tmp_path / "out.wav"
    mock_synth.return_value = output

    result = runner.invoke(
        app,
        ["hello world", "--output", str(output), "--output-dir", str(tmp_path)],
    )

    assert result.exit_code == 0, result.stderr or result.output
    mock_synth.assert_called_once()


@patch("main.synthesize_text_to_file")
def test_synthesize_engine_error_is_single_line(
    mock_synth: MagicMock,
    tmp_path: Path,
) -> None:
    mock_synth.side_effect = EngineClientError(
        "Could not connect to VOICEVOX Engine.",
    )

    result = runner.invoke(
        app,
        ["hello", "--output-dir", str(tmp_path)],
    )

    assert result.exit_code == 1
    # Synthesis errors must be a single English line (no traceback).
    assert _stderr_lines(result) == ["Could not connect to VOICEVOX Engine."]


@patch("main.synthesize_text_to_file")
def test_output_dir_that_is_a_file_is_single_line(
    mock_synth: MagicMock,
    tmp_path: Path,
) -> None:
    blocker = tmp_path / "not_a_dir"
    blocker.write_text("x")

    result = runner.invoke(app, ["hello", "--output-dir", str(blocker)])

    assert result.exit_code == 1
    lines = _stderr_lines(result)
    assert len(lines) == 1
    assert lines[0].startswith("Could not create the output directory:")
    mock_synth.assert_not_called()


@patch("main.synthesize_text_to_file")
def test_wav_write_error_is_single_line(
    mock_synth: MagicMock,
    tmp_path: Path,
) -> None:
    mock_synth.side_effect = PermissionError(13, "Permission denied", "out.wav")

    result = runner.invoke(app, ["hello", "--output-dir", str(tmp_path)])

    assert result.exit_code == 1
    assert _stderr_lines(result) == [
        "Could not write the WAV file: [Errno 13] Permission denied: 'out.wav'",
    ]


@patch("main.synthesize_text_to_file")
def test_speed_below_minimum_rejected(
    mock_synth: MagicMock,
    tmp_path: Path,
) -> None:
    result = runner.invoke(
        app,
        ["hello", "--speed", "0", "--output-dir", str(tmp_path)],
    )

    assert result.exit_code != 0
    mock_synth.assert_not_called()
