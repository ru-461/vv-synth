---
name: vv-synth
description: >-
  Synthesizes text to WAV via the vv-synth CLI and a separately prepared
  VOICEVOX Engine (Docker or official binary on port 50021). Use when the user
  wants TTS, voice narration, demo audio, VOICEVOX, read-aloud, or a WAV file
  from text in any project; or asks to run vv-synth outside the vv-synth
  repository.
license: MIT
compatibility: Requires Python 3.14+, uv, and a reachable VOICEVOX Engine on port 50021. Engine may be Docker CPU/GPU or an official binary. Windows Docker GPU requires Docker Desktop WSL2 backend with NVIDIA GPU.
metadata:
  author: ru-461
  version: "0.1.0"
---

# vv-synth (portable — any project)

`vv-synth` is a **global Typer CLI** (install once from the vv-synth repository). It calls a separately prepared VOICEVOX Engine over HTTP and writes a WAV under the **shell current working directory**. Japanese text works best; other languages depend on the Engine build.

This skill does not install or redistribute VOICEVOX Engine, voice libraries, model files, binaries, Docker images, or generated WAV files. Follow the latest VOICEVOX Engine terms and each voice library / speaker's terms, including credit requirements, before using or distributing generated audio.

**Not this skill:** editing vv-synth source — install or use the `vv-synth-dev` skill from the same repository. Skill install/update commands live in [references/REFERENCE.md](references/REFERENCE.md).

## When to use

| Use | Do not use |
|-----|------------|
| User wants speech, narration, TTS, or a local WAV | Cloud-only TTS with no local Engine |
| Demo / fixture audio for another app | User only asked to change vv-synth internals |
| Read-aloud for docs, games, bots, videos | Engine is down and user did not agree to start it |
| `assets/`, `public/audio/`, etc. under the target repo | Reimplementing Engine HTTP in the target project |

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Docker or official Engine binary | VOICEVOX Engine must listen on port 50021 |
| Python 3.14+ and [uv](https://docs.astral.sh/uv/) | For `uv tool install` or `uv run --project` |
| `vv-synth` on PATH | Or `uv run --project <vv-synth-repo> vv-synth` |
| Engine on `http://127.0.0.1:50021` | Override with `--engine-url` or `VOICEVOX_ENGINE_URL` |

GUI VOICEVOX desktop app is **not** required. Do not run multiple Engines on port 50021 at the same time.

## Prepare VOICEVOX Engine (Docker or binary — before synthesis)

Docker CPU:

```shell
docker pull voicevox/voicevox_engine:cpu-latest
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
```

- **Foreground** (`-it`): one terminal stays busy; run `vv-synth` in a **second** terminal
- **Background**: `docker run --rm -d -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest` — stop with `docker ps` then `docker stop <id>`
- Windows / Linux NVIDIA GPU: `docker pull voicevox/voicevox_engine:nvidia-latest`, then `docker run --rm -it --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-latest`
- Windows GPU prerequisites: Docker Desktop WSL2 backend, current NVIDIA driver, `wsl --update`; validate with `docker run --rm -it --gpus=all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark`
- Official Windows/macOS/Linux Engine binaries are also fine if they listen on `http://127.0.0.1:50021`; `vv-synth` needs no GPU-specific option

Verify before calling `vv-synth`:

```shell
curl -sSf -o /dev/null -w "%{http_code}\n" http://127.0.0.1:50021/version
```

Expect `200`. On failure, start Engine once; retry synthesis at most once after Engine is healthy.

| Symptom | Action |
|---------|--------|
| `Cannot connect to the Docker daemon` | Start Docker Desktop, or use an official Engine binary |
| `port is already allocated` (50021) | Stop other Engine containers or desktop VOICEVOX |
| GPU container cannot select a driver | Confirm Docker Desktop WSL2 backend, NVIDIA driver, and `wsl --update` |
| `Connection refused` from `vv-synth` | Confirm container is running and port is `127.0.0.1:50021` |

## Install vv-synth CLI (if command missing)

```shell
uv tool install git+https://github.com/ru-461/vv-synth
uv tool update-shell   # if vv-synth is not on PATH
vv-synth --help
```

Alternatively, install from a local clone (editable):

```shell
cd /path/to/vv-synth
uv tool install --editable .
```

`~/.local/bin` must be on PATH. For editable installs, reinstall after repo moves: `uv tool uninstall vv-synth` then install again.

**Fallback** (no global install):

```shell
uv run --project /path/to/vv-synth vv-synth --help
```

## How to invoke (any repo)

`cd` to the project that should **own** the WAV (paths are relative to cwd).

```shell
cd /path/to/target-project
vv-synth "Text to speak"
vv-synth "Narration line" -o public/audio/intro.wav
vv-synth "Faster line" --speaker 3 --speed 1.5
```

| Option | Short | Default | Notes |
|--------|-------|---------|-------|
| `MESSAGE` | — | required | Text sent to Engine |
| `--output` | `-o` | auto `output/YYYYMMDD-HHMMSS.wav` (local time) | Basename → under `--output-dir`; path with dirs → used as-is |
| `--output-dir` | — | `output` | Directory when `-o` is only a filename; envvar `VV_SYNTH_OUTPUT_DIR` |
| `--speaker` | `-s` | `2` | Style ID — http://127.0.0.1:50021/docs `/speakers` |
| `--speed` | — | `1.0` | Finite number from `0.01` to `10.0`; higher = faster |
| `--engine-url` | — | `http://127.0.0.1:50021` | Env: `VOICEVOX_ENGINE_URL` |

`vv-synth --help` is in English. Synthesis and file I/O errors are a **single English line** on stderr (exit code 1). Invalid arguments or options produce a Typer usage error on stderr (exit code 2).

### HTTP timeouts (per request)

| Step | Timeout |
|------|---------|
| `POST /audio_query` | 60s |
| `POST /synthesis` | 120s |

Very long text may hit the synthesis limit. Split into shorter chunks and run `vv-synth` multiple times (separate WAV files), or change timeouts in `vv_synth/engine_client.py` when maintaining the CLI.

### Long text

Split by sentence or paragraph; each `vv-synth` call gets its own 120s synthesis window. The CLI does not auto-chunk or merge WAVs.

## Success criteria

The CLI prints the saved file's absolute path to stdout:

```text
INFO: wrote /path/to/file.wav
```

Confirm the file exists on disk; return the resolved path to the user. Do not `git add` `output/*.wav` unless asked.

## Failure handling

| Symptom | Action |
|---------|--------|
| `command not found: vv-synth` | `uv tool install git+https://github.com/ru-461/vv-synth`, `uv tool install --editable /path/to/vv-synth`, or `uv run --project <repo> vv-synth` |
| `Connection refused` | Start Engine; `curl .../version` → 200 |
| HTTP 4xx | Fix `--speaker` using `/speakers` in Engine docs |
| Exit code 1 | Read one-line stderr; do not expect a traceback |
| Exit code 2 | Read the usage error on stderr and correct the arguments or options |
| Hang then failure | Text may be too long for one request; split and retry |

## Agent workflow checklist

```
- [ ] VOICEVOX Engine on 127.0.0.1:50021 (or user agreed to start it)
- [ ] curl /version → 200
- [ ] cd to target project (owner of the WAV)
- [ ] vv-synth "..." [options]
- [ ] Confirm INFO wrote ... and file exists
- [ ] Return path; do not commit WAV unless asked
- [ ] Generated audio use/distribution follows VOICEVOX and speaker-specific terms and credit requirements
```

## Do not reimplement Engine HTTP

Use the `vv-synth` CLI only unless the user explicitly wants direct `/audio_query` / `/synthesis` integration.

## More detail

See [references/REFERENCE.md](references/REFERENCE.md) for output path rules, skill install/update commands, and publishing notes.
