"""VOICEVOX Engine 向けテキスト音声合成 CLI (``vv-synth``)."""

from __future__ import annotations

import logging
from pathlib import Path

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

logger = logging.getLogger(__name__)

app = typer.Typer(
    name="vv-synth",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode=None,
    help="Synthesize text to WAV via VOICEVOX Engine.",
)


@app.command()
def synth(
    message: str = typer.Argument(
        ...,
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
        help="Speech rate; 1.0 is normal, higher is faster.",
    ),
    engine_url: str = typer.Option(
        DEFAULT_ENGINE_URL,
        "--engine-url",
        help="VOICEVOX Engine base URL.",
        envvar="VOICEVOX_ENGINE_URL",
    ),
) -> None:
    """Synthesize MESSAGE to a WAV file.

    Without -o, writes a timestamped file under output/ in the
    current directory. Use --output-dir to change the directory.
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    output_path = resolve_output_file(output_dir=output_dir, filename=output)

    logger.info("engine: %s", engine_url)
    logger.info("speaker: %s", speaker)
    logger.info("speed: %s", speed)
    logger.info("text: %s", message)
    logger.info("output: %s", output_path)

    try:
        saved = synthesize_text_to_file(
            message,
            output_path,
            base_url=engine_url,
            style_id=speaker,
            speed_scale=speed,
        )
    except (EngineClientError, ValueError):
        logger.exception("synthesis failed")
        raise typer.Exit(code=1) from None

    logger.info("wrote %s", saved.resolve())


def main() -> None:
    """Entry point for the ``vv-synth`` command."""
    app()


if __name__ == "__main__":
    main()
