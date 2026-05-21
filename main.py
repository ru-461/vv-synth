"""VOICEVOX Engine でテキストを音声合成する Typer CLI."""

from __future__ import annotations

import logging
from pathlib import Path

import typer

from voicevox_playground.engine_client import (
    DEFAULT_ENGINE_URL,
    DEFAULT_STYLE_ID,
    EngineClientError,
    synthesize_text_to_file,
)
from voicevox_playground.output_paths import (
    DEFAULT_OUTPUT_DIR,
    resolve_output_file,
)

logger = logging.getLogger(__name__)

app = typer.Typer(
    add_completion=False,
    help="VOICEVOX Engine でテキストを音声合成する CLI。",
)


@app.command()
def synth(
    message: str = typer.Argument(
        ...,
        help="読み上げるテキスト",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="出力ファイル名またはパス (省略時は output/ にタイムスタンプ名で保存)",
    ),
    output_dir: Path = typer.Option(
        DEFAULT_OUTPUT_DIR,
        "--output-dir",
        help="成果物を格納するディレクトリ",
    ),
    speaker: int = typer.Option(
        DEFAULT_STYLE_ID,
        "--speaker",
        "-s",
        help="話者スタイル ID (/speakers で確認)",
    ),
    engine_url: str = typer.Option(
        DEFAULT_ENGINE_URL,
        "--engine-url",
        help="VOICEVOX Engine のベース URL",
        envvar="VOICEVOX_ENGINE_URL",
    ),
) -> None:
    """引数で渡したメッセージを音声合成する.

    合成した WAV は ``output/`` 配下に保存する。
    ``--output-dir`` で別ディレクトリを指定できる。

    Raises:
        typer.Exit: 合成に失敗した場合 (exit code 1)。
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    output_path = resolve_output_file(output_dir=output_dir, filename=output)

    logger.info("Engine: %s", engine_url)
    logger.info("話者スタイル ID: %s", speaker)
    logger.info("テキスト: %s", message)
    logger.info("出力先: %s", output_path)

    try:
        saved = synthesize_text_to_file(
            message,
            output_path,
            base_url=engine_url,
            style_id=speaker,
        )
    except EngineClientError:
        logger.exception("音声合成に失敗しました")
        raise typer.Exit(code=1) from None

    logger.info("保存しました: %s", saved.resolve())


def main() -> None:
    """CLI エントリーポイント."""
    app()


if __name__ == "__main__":
    main()
