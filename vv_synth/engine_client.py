"""VOICEVOX Engine HTTP API client."""

from __future__ import annotations

import http.client
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from pathlib import Path

# Type alias for the AudioQuery JSON object returned by the Engine API.
AudioQuery = dict[str, Any]

DEFAULT_ENGINE_URL = "http://127.0.0.1:50021"
DEFAULT_STYLE_ID = 2
DEFAULT_SPEED_SCALE = 1.0

# HTTP timeouts (seconds) per Engine endpoint.
AUDIO_QUERY_TIMEOUT_S = 60
SYNTHESIS_TIMEOUT_S = 120


class EngineClientError(Exception):
    """Error raised when a VOICEVOX Engine call fails."""


def _post(url: str, body: bytes | None, *, timeout: int) -> bytes:
    """POST a request body and return the raw response bytes."""
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        return cast("bytes", response.read())


def _post_json(url: str) -> object:
    """POST without a body and return the JSON response as a Python object."""
    raw = _post(url, None, timeout=AUDIO_QUERY_TIMEOUT_S)

    return json.loads(raw.decode("utf-8"))


def _post_wav(url: str, audio_query: AudioQuery) -> bytes:
    """POST an AudioQuery and return the synthesized WAV bytes."""
    body = json.dumps(audio_query).encode("utf-8")

    return _post(url, body, timeout=SYNTHESIS_TIMEOUT_S)


def create_audio_query(
    base_url: str,
    text: str,
    style_id: int,
) -> AudioQuery:
    """Create an AudioQuery from text."""
    query = urllib.parse.urlencode({"text": text, "speaker": style_id})
    url = f"{base_url.rstrip('/')}/audio_query?{query}"
    result = _post_json(url)

    if not isinstance(result, dict):
        msg = f"audio_query response is not a dict: {type(result)!r}"
        raise TypeError(msg)

    return cast("AudioQuery", result)


def synthesize_wav(
    base_url: str,
    audio_query: AudioQuery,
    style_id: int,
) -> bytes:
    """Synthesize WAV audio from an AudioQuery."""
    query = urllib.parse.urlencode({"speaker": style_id})
    url = f"{base_url.rstrip('/')}/synthesis?{query}"

    return _post_wav(url, audio_query)


def save_wav(path: Path, wav_data: bytes) -> None:
    """Save WAV bytes to a file."""
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_bytes(wav_data)


def apply_speed_scale(audio_query: AudioQuery, speed_scale: float) -> AudioQuery:
    """Set the speech rate (speedScale) on an AudioQuery."""
    if speed_scale <= 0:
        msg = f"speed_scale must be positive: {speed_scale}"
        raise ValueError(msg)

    audio_query["speedScale"] = speed_scale

    return audio_query


def synthesize_text_to_file(
    text: str,
    output: Path,
    *,
    base_url: str = DEFAULT_ENGINE_URL,
    style_id: int = DEFAULT_STYLE_ID,
    speed_scale: float = DEFAULT_SPEED_SCALE,
) -> Path:
    """Synthesize text and save it to a WAV file.

    Args:
        text: Text to speak.
        output: Destination WAV file.
        base_url: Engine base URL.
        style_id: Speaker style ID.
        speed_scale: Speech rate. 1.0 is normal; higher is faster.

    Returns:
        Path to the saved file.

    Raises:
        EngineClientError: Engine is unavailable, the API returns an error, etc.
    """
    try:
        audio_query = create_audio_query(base_url, text, style_id)
        apply_speed_scale(audio_query, speed_scale)
        wav_data = synthesize_wav(base_url, audio_query, style_id)

    except urllib.error.HTTPError as exc:
        msg = (
            f"Engine API returned an error (HTTP {exc.code}). "
            "Check that the speaker style ID is valid for this Engine."
        )
        raise EngineClientError(msg) from exc

    except urllib.error.URLError as exc:
        msg = (
            "Could not connect to VOICEVOX Engine. "
            "Start the Engine (e.g. Docker voicevox/voicevox_engine:cpu-latest "
            "on port 50021) and ensure it is reachable."
        )
        raise EngineClientError(msg) from exc

    # urlopen() wraps only connection failures in URLError. A timeout or a dropped
    # connection while waiting for the response escapes unwrapped.
    except TimeoutError as exc:
        msg = (
            "VOICEVOX Engine did not respond in time. "
            "Split long text into shorter runs, or check that the Engine is not busy."
        )
        raise EngineClientError(msg) from exc

    except (OSError, http.client.HTTPException) as exc:
        msg = (
            "Lost connection to VOICEVOX Engine before the response completed. "
            "Check that the Engine is still running."
        )
        raise EngineClientError(msg) from exc

    # Write failures stay OSError so they are not reported as Engine problems.
    save_wav(output, wav_data)

    return output
