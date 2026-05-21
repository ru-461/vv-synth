"""VOICEVOX Engine HTTP API クライアント."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, cast

# Engine API が返す AudioQuery (JSON オブジェクト) の型エイリアス
AudioQuery = dict[str, Any]

DEFAULT_ENGINE_URL = "http://127.0.0.1:50021"
DEFAULT_STYLE_ID = 2


class EngineClientError(Exception):
    """VOICEVOX Engine の呼び出しに失敗したときのエラー."""


def _post_json(url: str, payload: dict[str, Any] | None = None) -> object:
    """JSON を POST し、レスポンスを Python オブジェクトとして返す."""
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
    """AudioQuery を POST し、合成された WAV バイナリを返す."""
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
    """テキストから AudioQuery を生成する."""
    query = urllib.parse.urlencode({"text": text, "speaker": style_id})
    url = f"{base_url.rstrip('/')}/audio_query?{query}"
    result = _post_json(url)
    if not isinstance(result, dict):
        msg = f"audio_query の応答が dict ではありません: {type(result)!r}"
        raise TypeError(msg)
    return cast("AudioQuery", result)


def synthesize_wav(
    base_url: str,
    audio_query: AudioQuery,
    style_id: int,
) -> bytes:
    """AudioQuery から WAV 音声を合成する."""
    query = urllib.parse.urlencode({"speaker": style_id})
    url = f"{base_url.rstrip('/')}/synthesis?{query}"
    return _post_wav(url, audio_query)


def save_wav(path: Path, wav_data: bytes) -> None:
    """WAV バイナリをファイルに保存する."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(wav_data)


def synthesize_text_to_file(
    text: str,
    output: Path,
    *,
    base_url: str = DEFAULT_ENGINE_URL,
    style_id: int = DEFAULT_STYLE_ID,
) -> Path:
    """テキストを音声合成し、WAV ファイルに保存する.

    Args:
        text: 読み上げるテキスト。
        output: 出力先 WAV ファイル。
        base_url: Engine のベース URL。
        style_id: 話者スタイル ID。

    Returns:
        保存したファイルのパス。

    Raises:
        EngineClientError: Engine 未起動、API エラーなど。
    """
    try:
        audio_query = create_audio_query(base_url, text, style_id)
        wav_data = synthesize_wav(base_url, audio_query, style_id)
        save_wav(output, wav_data)
    except urllib.error.URLError as exc:
        msg = (
            "VOICEVOX Engine に接続できませんでした。"
            " VOICEVOX アプリを起動するか、"
            " Engine が 50021 で待ち受けているか確認してください。"
        )
        raise EngineClientError(msg) from exc
    except urllib.error.HTTPError as exc:
        msg = (
            f"Engine API がエラーを返しました (HTTP {exc.code})。"
            " 話者 ID が環境と合っているか確認してください。"
        )
        raise EngineClientError(msg) from exc
    else:
        return output
