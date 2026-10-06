---
name: vv-synth-dev
description: >-
  Develops and smoke-tests the vv-synth CLI in its repository using uv run
  vv-synth and a separately prepared VOICEVOX Engine (Docker or official binary
  on port 50021). Use when editing main.py, vv_synth/, running synthesis in the
  vv-synth repo, or maintaining CLI and engine_client behavior—not for portable
  TTS in other projects.
license: MIT
compatibility: Requires Python 3.14+, uv, the vv-synth repo checkout, and a reachable VOICEVOX Engine on port 50021. Engine may be Docker CPU/GPU or an official binary.
metadata:
  author: ru-461
  version: "0.1.0"
---

# vv-synth-dev (repository development)

Work inside the **vv-synth** repository. For TTS in other projects, use the `vv-synth` skill (`gh skill install ru-461/vv-synth vv-synth`, or `npx skills add ru-461/vv-synth --skill vv-synth --global`).

This repository is open source (MIT) and must not vendor VOICEVOX Engine, voice libraries, model files, official binaries, Docker images, or generated WAV files. Preserve README guidance about VOICEVOX terms and speaker-specific credit requirements.

## When to use

| Use | Do not use |
|-----|------------|
| Edit CLI, Engine client, or output paths | Portable narration in another repo (use `vv-synth` skill) |
| `uv run vv-synth` smoke tests | User only wants docs without running synthesis |
| Update README Mermaid / `.claude/rules/architecture.md` after API changes | Engine down without user consent to start it |

Follow [`AGENTS.md`](../../AGENTS.md) and [`README.md`](../../README.md) maintenance sections when changing code.

## Prepare VOICEVOX Engine (Docker or binary)

```shell
docker pull voicevox/voicevox_engine:cpu-latest
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
```

Background: `docker run --rm -d -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest`

Windows / Linux NVIDIA GPU:

```shell
docker pull voicevox/voicevox_engine:nvidia-latest
docker run --rm -it --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-latest
```

Windows GPU prerequisites: Docker Desktop WSL2 backend, current NVIDIA driver, and `wsl --update`. Official Windows/macOS/Linux Engine binaries are also fine if they listen on `http://127.0.0.1:50021`; `vv-synth` needs no GPU-specific option.

Verify:

```shell
curl -sSf -o /dev/null -w "%{http_code}\n" http://127.0.0.1:50021/version
```

## Invoke in this repo

Prefer **`uv run vv-synth`** from the repository root:

```shell
cd /path/to/vv-synth
uv sync
uv run vv-synth "Text to speak"
uv run vv-synth "Test" -o hello.wav
uv run vv-synth "Test" --output-dir artifacts -o demo.wav
uv run vv-synth "Faster" --speaker 3 --speed 1.5
```

Global CLI after `uv tool install --editable .` is also fine.

| Option | Short | Default | Notes |
|--------|-------|---------|-------|
| `MESSAGE` | — | required | Text for Engine |
| `--output` | `-o` | auto timestamp under `output/` (local time) | File name or full path |
| `--output-dir` | — | `output` | Directory when `-o` is basename only; envvar `VV_SYNTH_OUTPUT_DIR` |
| `--speaker` | `-s` | `2` | http://127.0.0.1:50021/docs `/speakers` |
| `--speed` | — | `1.0` | Finite number from `0.01` to `10.0` |
| `--engine-url` | — | `http://127.0.0.1:50021` | `VOICEVOX_ENGINE_URL` |

`vv-synth --help` is in English. Synthesis and file I/O errors show **one English line** on stderr (exit 1); do not expect a traceback. Invalid arguments or options produce a Typer usage error on stderr (exit 2).

## Python API (in-repo only)

Prefer the CLI. For scripts inside this repository:

Python API speech rates must be finite and positive.

```python
from pathlib import Path

from vv_synth.engine_client import synthesize_text_to_file

path = synthesize_text_to_file(
    "text",
    Path("output/agent-demo.wav"),
    style_id=2,
    speed_scale=1.0,
)
```

HTTP timeouts in `engine_client.py`: `/audio_query` 60s, `/synthesis` 120s.

## Quality checks

```shell
uv run ruff check .
uv run ruff format .
uv run ty check
uv run pytest
uv run vv-synth "smoke test"   # Engine must be up
```

## Success criteria

The CLI prints the saved file's absolute path to stdout:

```text
INFO: wrote /path/to/file.wav
```

Do not commit `output/*.wav`, VOICEVOX Engine binaries, models, or voice libraries. Generated audio distribution must follow VOICEVOX and speaker-specific terms. Commit only when the user asks.

## Maintainer sync

When Engine setup, terms guidance, or CLI options change, update together:

1. `skills/vv-synth/SKILL.md` (portable)
2. This file (`skills/vv-synth-dev/SKILL.md`)
3. `README.md` / `README.ja.md` / `AGENTS.md` / `CLAUDE.md` as needed

Release only when the user explicitly asks: `gh skill publish --tag vX.Y.Z` from repo root creates the GitHub Release, and `uv build --clear` then `uv publish` upload the same version to PyPI. `X.Y.Z` is the `version` in `pyproject.toml`, which must match `metadata.version` in both skills' `SKILL.md` files. Full steps: [README.md](../../README.md#release).

## Related docs

- [`README.md`](../../README.md)
- [`README.ja.md`](../../README.ja.md)
- [`AGENTS.md`](../../AGENTS.md)
- [`CLAUDE.md`](../../CLAUDE.md)
- [`skills/README.md`](../../skills/README.md)
