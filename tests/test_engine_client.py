"""Tests for ``vv_synth.engine_client``."""

from __future__ import annotations

import email.message
import http.client
import json
import urllib.error
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest

from vv_synth.engine_client import (
    EngineClientError,
    apply_speed_scale,
    create_audio_query,
    save_wav,
    synthesize_text_to_file,
    synthesize_wav,
)

if TYPE_CHECKING:
    from pathlib import Path


def _make_response(payload: bytes) -> MagicMock:
    """Build a context-manager mock that mimics ``urllib.request.urlopen``."""
    response = MagicMock()
    response.read.return_value = payload
    cm = MagicMock()
    cm.__enter__.return_value = response
    cm.__exit__.return_value = None
    return cm


def test_apply_speed_scale_sets_value() -> None:
    query: dict[str, float] = {"speedScale": 1.0}

    result = apply_speed_scale(query, 1.5)

    assert result is query
    assert query["speedScale"] == 1.5


def test_apply_speed_scale_zero_raises() -> None:
    with pytest.raises(ValueError, match="speed_scale"):
        apply_speed_scale({}, 0.0)


def test_apply_speed_scale_negative_raises() -> None:
    with pytest.raises(ValueError, match="speed_scale"):
        apply_speed_scale({}, -1.0)


@pytest.mark.parametrize("speed", [float("nan"), float("inf"), -float("inf")])
def test_apply_speed_scale_nonfinite_raises_without_mutating_query(
    speed: float,
) -> None:
    query = {"speedScale": 1.0}

    with pytest.raises(ValueError, match="finite"):
        apply_speed_scale(query, speed)

    assert query == {"speedScale": 1.0}


def test_save_wav_writes_bytes(tmp_path: Path) -> None:
    path = tmp_path / "out.wav"

    save_wav(path, b"RIFF...WAVE")

    assert path.read_bytes() == b"RIFF...WAVE"


def test_save_wav_creates_parent_dirs(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "deep" / "audio.wav"

    save_wav(path, b"data")

    assert path.read_bytes() == b"data"


@patch("vv_synth.engine_client.urllib.request.urlopen")
def test_create_audio_query_parses_json(mock_urlopen: MagicMock) -> None:
    payload = {"speedScale": 1.0, "kana": "..."}
    mock_urlopen.return_value = _make_response(json.dumps(payload).encode())

    result = create_audio_query("http://localhost:50021", "hello", 2)

    assert result == payload
    request_arg = mock_urlopen.call_args[0][0]
    assert request_arg.full_url.startswith(
        "http://localhost:50021/audio_query?",
    )
    assert "text=hello" in request_arg.full_url
    assert "speaker=2" in request_arg.full_url


@patch("vv_synth.engine_client.urllib.request.urlopen")
def test_create_audio_query_trims_trailing_slash(
    mock_urlopen: MagicMock,
) -> None:
    mock_urlopen.return_value = _make_response(b'{"speedScale": 1.0}')

    create_audio_query("http://localhost:50021/", "hi", 1)

    request_arg = mock_urlopen.call_args[0][0]
    assert "://localhost:50021/audio_query" in request_arg.full_url
    assert "://localhost:50021//audio_query" not in request_arg.full_url


@patch("vv_synth.engine_client.urllib.request.urlopen")
def test_create_audio_query_unexpected_payload_raises(
    mock_urlopen: MagicMock,
) -> None:
    mock_urlopen.return_value = _make_response(b"[]")

    with pytest.raises(TypeError, match="not a dict"):
        create_audio_query("http://localhost:50021", "hello", 2)


@patch("vv_synth.engine_client.urllib.request.urlopen")
def test_synthesize_wav_returns_bytes(mock_urlopen: MagicMock) -> None:
    mock_urlopen.return_value = _make_response(b"RIFFwave")

    result = synthesize_wav("http://localhost:50021", {"speedScale": 1.0}, 2)

    assert result == b"RIFFwave"
    request_arg = mock_urlopen.call_args[0][0]
    assert request_arg.full_url.startswith(
        "http://localhost:50021/synthesis?",
    )
    assert "speaker=2" in request_arg.full_url


@patch("vv_synth.engine_client.urllib.request.urlopen")
def test_synthesize_text_to_file_full_flow(
    mock_urlopen: MagicMock,
    tmp_path: Path,
) -> None:
    audio_query_response = _make_response(
        json.dumps({"speedScale": 1.0}).encode(),
    )
    synthesis_response = _make_response(b"WAV_BYTES")
    mock_urlopen.side_effect = [audio_query_response, synthesis_response]

    output = tmp_path / "out.wav"
    result = synthesize_text_to_file(
        "hello",
        output,
        base_url="http://localhost:50021",
        style_id=3,
        speed_scale=1.2,
    )

    assert result == output
    assert output.read_bytes() == b"WAV_BYTES"
    assert mock_urlopen.call_count == 2


@patch("vv_synth.engine_client.urllib.request.urlopen")
def test_synthesize_text_to_file_connection_error(
    mock_urlopen: MagicMock,
    tmp_path: Path,
) -> None:
    mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

    with pytest.raises(EngineClientError, match="Could not connect"):
        synthesize_text_to_file("hello", tmp_path / "out.wav")


@patch("vv_synth.engine_client.urllib.request.urlopen")
def test_synthesize_text_to_file_http_error_uses_http_message(
    mock_urlopen: MagicMock,
    tmp_path: Path,
) -> None:
    # HTTPError is a subclass of URLError; ensure it routes to the HTTP-specific
    # message rather than the connection-error fallback.
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="http://localhost:50021/audio_query",
        code=422,
        msg="Unprocessable Entity",
        hdrs=email.message.Message(),
        fp=None,
    )

    with pytest.raises(EngineClientError, match="HTTP 422"):
        synthesize_text_to_file("hello", tmp_path / "out.wav")


@patch("vv_synth.engine_client.urllib.request.urlopen")
def test_synthesize_text_to_file_timeout_uses_timeout_message(
    mock_urlopen: MagicMock,
    tmp_path: Path,
) -> None:
    # A read timeout escapes urlopen() as a bare TimeoutError, not URLError.
    mock_urlopen.side_effect = TimeoutError("timed out")

    with pytest.raises(EngineClientError, match="did not respond in time"):
        synthesize_text_to_file("hello", tmp_path / "out.wav")


@pytest.mark.parametrize(
    "error",
    [
        http.client.RemoteDisconnected("Remote end closed connection"),
        http.client.IncompleteRead(b"RIFF"),
        ConnectionResetError("Connection reset by peer"),
    ],
)
@patch("vv_synth.engine_client.urllib.request.urlopen")
def test_synthesize_text_to_file_lost_connection(
    mock_urlopen: MagicMock,
    error: Exception,
    tmp_path: Path,
) -> None:
    mock_urlopen.side_effect = error

    with pytest.raises(EngineClientError, match="Lost connection"):
        synthesize_text_to_file("hello", tmp_path / "out.wav")


@patch("vv_synth.engine_client.urllib.request.urlopen")
def test_synthesize_text_to_file_write_error_is_not_engine_error(
    mock_urlopen: MagicMock,
    tmp_path: Path,
) -> None:
    mock_urlopen.side_effect = [
        _make_response(b'{"speedScale": 1.0}'),
        _make_response(b"WAV_BYTES"),
    ]
    output = tmp_path / "out.wav"
    output.mkdir()  # Writing the WAV bytes to a directory fails.

    with pytest.raises(OSError, match=r"out\.wav"):
        synthesize_text_to_file("hello", output)


@patch("vv_synth.engine_client.urllib.request.urlopen")
def test_create_audio_query_posts_without_body(mock_urlopen: MagicMock) -> None:
    mock_urlopen.return_value = _make_response(b"{}")

    create_audio_query("http://localhost:50021", "hello", 2)

    request_arg = mock_urlopen.call_args[0][0]
    assert request_arg.get_method() == "POST"
    assert request_arg.data is None
    assert request_arg.get_header("Content-type") == "application/json"
    assert mock_urlopen.call_args.kwargs["timeout"] == 60
