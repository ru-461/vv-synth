"""VOICEVOX Engine を HTTP で呼び出し、音声合成するサンプル.

前提:
    VOICEVOX アプリまたは VOICEVOX Engine を起動し、
    http://127.0.0.1:50021 で API が応答する状態にしておく。

使い方:
    uv run python main.py
"""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, cast

logger = logging.getLogger(__name__)

# Engine のベース URL (デフォルトポートは 50021)
ENGINE_BASE_URL = "http://127.0.0.1:50021"

# 話者スタイル ID: 四国めたん ノーマル (環境により異なる場合は /speakers で確認)
STYLE_ID = 2

# 合成するテキスト
SAMPLE_TEXT = "こんにちは。ボイスボックスの音声合成サンプルです。"

# 出力先 WAV ファイル
OUTPUT_WAV = Path("output.wav")

# Engine API が返す AudioQuery (JSON オブジェクト) の型エイリアス
AudioQuery = dict[str, Any]


def _post_json(url: str, payload: dict[str, Any] | None = None) -> object:
    """JSON を POST し、レスポンスを Python オブジェクトとして返す.

    Args:
        url: リクエスト先 URL。
        payload: 送信する JSON ボディ。None のときはボディなし。

    Returns:
        レスポンス JSON をパースした結果。
    """
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def _post_wav(url: str, audio_query: AudioQuery) -> bytes:
    """AudioQuery を POST し、合成された WAV バイナリを返す.

    Args:
        url: リクエスト先 URL (/synthesis)。
        audio_query: /audio_query で取得した AudioQuery。

    Returns:
        WAV 形式の音声データ。
    """
    body = json.dumps(audio_query).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def create_audio_query(
    base_url: str,
    text: str,
    style_id: int,
) -> AudioQuery:
    """テキストから AudioQuery (音声合成用パラメータ) を生成する.

    Engine の ``POST /audio_query`` を呼び出す。
    返却値はそのまま ``POST /synthesis`` に渡せる。

    Args:
        base_url: Engine のベース URL (例: http://127.0.0.1:50021)。
        text: 読み上げる日本語テキスト。
        style_id: 話者スタイル ID (``GET /speakers`` で一覧を確認できる)。

    Returns:
        AudioQuery 辞書。

    Raises:
        TypeError: 応答 JSON が dict でない場合。
    """
    query = urllib.parse.urlencode({"text": text, "speaker": style_id})
    url = f"{base_url.rstrip('/')}/audio_query?{query}"
    result = _post_json(url)
    if not isinstance(result, dict):
        msg = f"audio_query の応答が dict ではありません: {type(result)!r}"
        raise TypeError(msg)
    return cast("AudioQuery", result)


def synthesize(
    base_url: str,
    audio_query: AudioQuery,
    style_id: int,
) -> bytes:
    """AudioQuery から WAV 音声を合成する.

    Engine の ``POST /synthesis`` を呼び出す。

    Args:
        base_url: Engine のベース URL。
        audio_query: ``create_audio_query`` の戻り値。
        style_id: 話者スタイル ID (audio_query 生成時と同じ値を指定する)。

    Returns:
        WAV 形式の音声データ。
    """
    query = urllib.parse.urlencode({"speaker": style_id})
    url = f"{base_url.rstrip('/')}/synthesis?{query}"
    return _post_wav(url, audio_query)


def save_wav(path: Path, wav_data: bytes) -> None:
    """WAV バイナリをファイルに保存する.

    Args:
        path: 保存先パス。
        wav_data: 合成済みの WAV データ。
    """
    path.write_bytes(wav_data)


def main() -> int:
    """音声合成サンプルのエントリーポイント.

    Returns:
        成功時は 0、Engine 接続失敗や API エラー時は 1。
    """
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    logger.info("VOICEVOX Engine に接続します: %s", ENGINE_BASE_URL)
    logger.info("テキスト: %s", SAMPLE_TEXT)
    logger.info("話者スタイル ID: %s", STYLE_ID)

    try:
        # 1. テキストから AudioQuery を取得 (アクセント・読みなどの情報)
        audio_query = create_audio_query(ENGINE_BASE_URL, SAMPLE_TEXT, STYLE_ID)
        logger.info("AudioQuery を取得しました")

        # 2. AudioQuery から WAV を合成
        wav_data = synthesize(ENGINE_BASE_URL, audio_query, STYLE_ID)
        logger.info("音声を合成しました (%s bytes)", len(wav_data))

        # 3. ファイルに保存
        save_wav(OUTPUT_WAV, wav_data)
        logger.info("保存しました: %s", OUTPUT_WAV.resolve())
    except urllib.error.URLError as exc:
        # Engine 未起動やポート違いのときに分かりやすくする
        msg = (
            "VOICEVOX Engine に接続できませんでした。"
            " VOICEVOX アプリを起動するか、"
            " Engine が 50021 で待ち受けているか確認してください。"
        )
        logger.exception("%s (%s)", msg, exc.reason)
        return 1
    except urllib.error.HTTPError as exc:
        logger.exception(
            "Engine API がエラーを返しました (HTTP %s)。"
            " 話者 ID が環境と合っているか確認してください。",
            exc.code,
        )
        return 1
    else:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
