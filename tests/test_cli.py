"""Tests for the ``vv-synth`` Typer CLI in ``main.py``."""

from __future__ import annotations

import subprocess  # ruff: ignore[suspicious-subprocess-import]
import sys
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import patch
from uuid import uuid4

import pytest
from typer.testing import CliRunner

from main import app
from vv_synth.engine_client import EngineClientError

if TYPE_CHECKING:
    from unittest.mock import MagicMock

    from typer.testing import Result

runner = CliRunner()

_CLI_SCRIPT = """\
import sys
from unittest.mock import patch
import main
from vv_synth.engine_client import EngineClientError

failure = sys.argv.pop(1) == "failure"

def synthesize(_message, output, **_kwargs):
    if failure:
        raise EngineClientError("Synthetic Engine failure.")
    return output

with patch("main.synthesize_text_to_file", side_effect=synthesize):
    main.main()
"""


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


@pytest.mark.parametrize("speed", [0.01, 1.0, 10.0])
@patch("main.synthesize_text_to_file")
def test_synthesize_success(
    mock_synth: MagicMock,
    tmp_path: Path,
    speed: float,
) -> None:
    output = tmp_path / "out.wav"
    mock_synth.return_value = output

    result = runner.invoke(
        app,
        ["hello world", "--output", str(output), "--speed", str(speed)],
    )

    assert result.exit_code == 0, result.stderr or result.output
    assert result.stdout == f"INFO: wrote {output.resolve()}\n"
    assert not result.stderr
    mock_synth.assert_called_once()
    assert mock_synth.call_args.kwargs["speed_scale"] == speed


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        (
            "Could not connect to VOICEVOX Engine.",
            "Could not connect to VOICEVOX Engine.",
        ),
        ("Engine failed.\nPlease retry.", "Engine failed. Please retry."),
    ],
)
@patch("main.synthesize_text_to_file")
def test_synthesize_engine_error_is_single_line(
    mock_synth: MagicMock,
    tmp_path: Path,
    message: str,
    expected: str,
) -> None:
    mock_synth.side_effect = EngineClientError(message)

    result = runner.invoke(
        app,
        ["hello", "--output-dir", str(tmp_path)],
    )

    assert result.exit_code == 1
    assert not result.stdout
    # Synthesis errors must be a single English line (no traceback).
    assert _stderr_lines(result) == [expected]


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


@pytest.mark.parametrize("speed", ["0", "-1", "10.01", "nan", "NaN", "inf", "-inf"])
@patch("main.synthesize_text_to_file")
def test_invalid_speed_rejected_before_synthesis(
    mock_synth: MagicMock,
    tmp_path: Path,
    speed: str,
) -> None:
    output_dir = tmp_path / "unused"
    result = runner.invoke(
        app,
        ["hello", "--speed", speed, "--output-dir", str(output_dir)],
    )

    assert result.exit_code == 2
    assert "Invalid value for '--speed'" in result.stderr
    mock_synth.assert_not_called()
    assert not output_dir.exists()


@pytest.mark.parametrize("outcome", ["success", "failure"])
def test_cli_process_output_excludes_engine_url_and_input(
    tmp_path: Path,
    outcome: str,
) -> None:
    # Generate a synthetic credential solely to detect accidental URL output.
    credential = uuid4().hex
    engine_url = f"http://test-user:{credential}@127.0.0.1:50021"
    message = "private input"
    output = tmp_path / "out.wav"

    # Fixed interpreter and script; Engine calls are mocked and no shell is used.
    result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        [
            sys.executable,
            "-c",
            _CLI_SCRIPT,
            outcome,
            message,
            "--output",
            str(output),
            "--engine-url",
            engine_url,
        ],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )

    assert credential not in result.stdout + result.stderr
    assert engine_url not in result.stdout + result.stderr
    assert message not in result.stdout + result.stderr
    if outcome == "success":
        assert result.returncode == 0
        assert result.stdout == f"INFO: wrote {output.resolve()}\n"
        assert not result.stderr
    else:
        assert result.returncode == 1
        assert not result.stdout
        assert result.stderr == "Synthetic Engine failure.\n"
