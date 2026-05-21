"""合成音声など成果物の出力パスを扱う."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

# 成果物 (合成 WAV など) の既定出力ディレクトリ
DEFAULT_OUTPUT_DIR = Path("output")


def ensure_output_dir(output_dir: Path) -> Path:
    """出力ディレクトリを作成する (存在しない場合).

    Args:
        output_dir: 作成するディレクトリ。

    Returns:
        作成したディレクトリのパス。
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def resolve_output_file(
    *,
    output_dir: Path,
    filename: Path | None = None,
) -> Path:
    """成果物 WAV の保存パスを決定する.

    ``filename`` 省略時は ``output_dir`` 配下にタイムスタンプ付きファイル名を使う。
    ファイル名のみ指定時は ``output_dir`` に格納する。
    ディレクトリを含むパス指定時はそのパスをそのまま使う。

    Args:
        output_dir: 成果物を格納するディレクトリ。
        filename: 出力ファイル名またはパス。None のとき自動生成。

    Returns:
        保存先ファイルのパス。
    """
    if filename is None:
        timestamp = datetime.now(tz=UTC).strftime("%Y%m%d-%H%M%S")
        return ensure_output_dir(output_dir) / f"{timestamp}.wav"

    if filename.parent.parts:
        filename.parent.mkdir(parents=True, exist_ok=True)
        return filename

    return ensure_output_dir(output_dir) / filename.name
