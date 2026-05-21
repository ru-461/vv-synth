---
name: vv-synth-dev
description: >-
  Develops and smoke-tests the vv-synth CLI in its repository using uv run
  vv-synth and VOICEVOX Engine (Docker on port 50021). Use when editing
  main.py, vv_synth/, running synthesis in the vv-synth repo, or maintaining
  CLI and engine_client behavior—not for portable TTS in other projects.
license: MIT
compatibility: Requires Docker, Python 3.14+, uv, and the vv-synth repo checkout.
metadata:
  author: vv-synth
  version: "1.0.0"
---

# vv-synth-dev (repository development)

> **Sync:** [`skills/vv-synth-dev/SKILL.md`](../../skills/vv-synth-dev/SKILL.md). Portable TTS: `gh skill install OWNER/vv-synth vv-synth`.

## When to use

| Use | Do not use |
|-----|------------|
| Edit CLI, Engine client, or output paths | Portable narration in another repo |
| `uv run vv-synth` smoke tests | User only wants docs without synthesis |

Follow [`AGENTS.md`](../../AGENTS.md) and [`README.md`](../../README.md).

## Start VOICEVOX Engine (Docker)

```shell
docker pull voicevox/voicevox_engine:cpu-latest
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
```

Verify: `curl -sSf -o /dev/null -w "%{http_code}\n" http://127.0.0.1:50021/version` → `200`

## Invoke in this repo

```shell
uv run vv-synth "Text to speak"
uv run vv-synth "Test" -o hello.wav
uv run vv-synth "Faster" --speaker 3 --speed 1.5
```

| Option | Short | Default |
|--------|-------|---------|
| `MESSAGE` | — | required |
| `--output` | `-o` | auto under `output/` |
| `--output-dir` | — | `output` |
| `--speaker` | `-s` | `2` |
| `--speed` | — | `1.0` |
| `--engine-url` | — | `http://127.0.0.1:50021` |

## Python API (in-repo only)

```python
from pathlib import Path
from vv_synth.engine_client import synthesize_text_to_file

synthesize_text_to_file("text", Path("output/demo.wav"), style_id=2, speed_scale=1.0)
```

## Success

```text
INFO: wrote /path/to/file.wav
```

Do not commit `output/*.wav`.

## Related

- [`skills/README.md`](../../skills/README.md)
- [`AGENTS.md`](../../AGENTS.md)
