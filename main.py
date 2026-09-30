"""Text-to-speech CLI for VOICEVOX Engine (``vv-synth``)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Never

import typer

from vv_synth.engine_client import (
    DEFAULT_ENGINE_URL,
    DEFAULT_SPEED_SCALE,
    DEFAULT_STYLE_ID,
    EngineClientError,
    synthesize_text_to_file,
)
from vv_synth.output_paths import (
    DEFAULT_OUTPUT_DIR,
    resolve_output_file,
)

app = typer.Typer(
    name="vv-synth",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode=None,
    help="Synthesize text to WAV via VOICEVOX Engine.",
)


def _validate_speed(value: float) -> float:
    """Reject non-finite CLI speech rates.

    Args:
        value: Parsed speech rate.

    Returns:
        Validated speech rate.
    """
    if not math.isfinite(value):
        msg = "Speed must be a finite number."
        raise typer.BadParameter(msg)

    return value


def _exit_with_error(message: str) -> Never:
    """Print a single-line synthesis error and exit.

    Args:
        message: Error description to print on stderr.
    """
    typer.echo(" ".join(message.splitlines()), err=True)
    raise typer.Exit(code=1) from None


@app.command()
def synth(
    message: str = typer.Argument(
        ...,
        metavar="MESSAGE",
        help="Text to speak.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output WAV file name or path.",
    ),
    output_dir: Path = typer.Option(
        DEFAULT_OUTPUT_DIR,
        "--output-dir",
        help="Directory for WAV output files.",
        envvar="VV_SYNTH_OUTPUT_DIR",
    ),
    speaker: int = typer.Option(
        DEFAULT_STYLE_ID,
        "--speaker",
        "-s",
        help="Speaker style ID (Engine GET /speakers).",
    ),
    speed: float = typer.Option(
        DEFAULT_SPEED_SCALE,
        "--speed",
        min=0.01,
        max=10.0,
        callback=_validate_speed,
        help="Finite speech rate; 1.0 is normal, higher is faster.",
    ),
    engine_url: str = typer.Option(
        DEFAULT_ENGINE_URL,
        "--engine-url",
        help="VOICEVOX Engine base URL.",
        envvar="VOICEVOX_ENGINE_URL",
    ),
) -> None:
    """Synthesize MESSAGE to a WAV file.

    Without -o, writes a local-time timestamped file under output/
    in the current directory (auto-created). Use --output-dir or
    set VV_SYNTH_OUTPUT_DIR to change the directory.
    """
    try:
        output_path = resolve_output_file(output_dir=output_dir, filename=output)
    except OSError as exc:
        _exit_with_error(f"Could not create the output directory: {exc}")

    try:
        saved = synthesize_text_to_file(
            message,
            output_path,
            base_url=engine_url,
            style_id=speaker,
            speed_scale=speed,
        )
    except (EngineClientError, ValueError, TypeError) as exc:
        _exit_with_error(str(exc))
    except OSError as exc:
        _exit_with_error(f"Could not write the WAV file: {exc}")

    typer.echo(f"INFO: wrote {saved.resolve()}")


def main() -> None:
    """Entry point for the ``vv-synth`` command."""
    app()


if __name__ == "__main__":
    main()
