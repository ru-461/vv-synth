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

Work inside the **vv-synth** repository. For TTS in other projects, use the `vv-synth` skill (`gh skill install OWNER/vv-synth vv-synth`).

## When to use

| Use | Do not use |
|-----|------------|
| Edit CLI, Engine client, or output paths | Portable narration in another repo (use `vv-synth` skill) |
| `uv run vv-synth` smoke tests | User only wants docs without running synthesis |
| Update README Mermaid / AGENTS.md after API changes | Engine down without user consent to start Docker |

Follow [`AGENTS.md`](../../AGENTS.md) and [`README.md`](../../README.md) maintenance sections when changing code.

## Start VOICEVOX Engine (Docker)

```shell
docker pull voicevox/voicevox_engine:cpu-latest
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
```

Background: `docker run --rm -d -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest`

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
| `--output` | `-o` | auto timestamp under `output/` | File name or full path |
| `--output-dir` | — | `output` | Directory when `-o` is basename only |
| `--speaker` | `-s` | `2` | http://127.0.0.1:50021/docs `/speakers` |
| `--speed` | — | `1.0` | `0.01`–`10.0` |
| `--engine-url` | — | `http://127.0.0.1:50021` | `VOICEVOX_ENGINE_URL` |

`vv-synth --help` is in English. On failure, stderr shows **one English line** (exit 1); do not expect a traceback.

## Python API (in-repo only)

Prefer the CLI. For scripts inside this repository:

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
uv run vv-synth "smoke test"   # Engine must be up
```

## Success criteria

```text
INFO: wrote /path/to/file.wav
```

Do not commit `output/*.wav`. Commit only when the user asks.

## Maintainer sync

When Docker steps or CLI options change, update together:

1. `skills/vv-synth/SKILL.md` (portable)
2. This file (`skills/vv-synth-dev/SKILL.md`)
3. `.cursor/skills/vv-synth-dev/SKILL.md` (Cursor in-repo; keep aligned with this skill)
4. `README.md` / `AGENTS.md` as needed

Publish: `gh skill publish --tag vX.Y.Z` from repo root.

## Related docs

- [`README.md`](../../README.md)
- [`AGENTS.md`](../../AGENTS.md)
- [`CLAUDE.md`](../../CLAUDE.md)
- [`skills/README.md`](../../skills/README.md)
- [`output/README.md`](../../output/README.md)
