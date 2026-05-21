---
name: vv-synth
description: >-
  Synthesizes text to WAV via the vv-synth CLI and VOICEVOX Engine (Docker
  voicevox/voicevox_engine:cpu-latest on port 50021). Use when the user wants
  TTS, voice narration, demo audio, VOICEVOX, read-aloud, or a WAV file from
  text in any project; or asks to run vv-synth outside the vv-synth repository.
license: MIT
compatibility: Requires Docker, Python 3.14+, uv, and a reachable VOICEVOX Engine on port 50021.
metadata:
  author: vv-synth
  version: "1.0.0"
---

# vv-synth (portable — any project)

`vv-synth` is a **global Typer CLI** (install once from the vv-synth repository). It calls VOICEVOX Engine over HTTP and writes a WAV under the **shell current working directory**. Japanese text works best; other languages depend on the Engine build.

**Not this skill:** editing vv-synth source — install or use the `vv-synth-dev` skill from the same repository.

## Install this skill (GitHub CLI)

Requires [GitHub CLI](https://cli.github.com/) v2.90+.

```shell
# All supported agents (~/.agents/skills or agent-specific dirs)
gh skill install OWNER/vv-synth vv-synth --scope user --agent universal

# Or pick one host
gh skill install OWNER/vv-synth vv-synth --scope user --agent cursor
gh skill install OWNER/vv-synth vv-synth --scope user --agent claude-code
gh skill install OWNER/vv-synth vv-synth --scope user --agent codex
gh skill install OWNER/vv-synth vv-synth --scope user --agent github-copilot
```

From a local clone (before publishing):

```shell
gh skill install /path/to/vv-synth vv-synth --from-local --scope user --agent universal
```

Update later: `gh skill update vv-synth`. Pin a release: `gh skill install OWNER/vv-synth vv-synth@v1.0.0 --scope user`.

Replace `OWNER` with the GitHub user or org that hosts the repository.

## When to use

| Use | Do not use |
|-----|------------|
| User wants speech, narration, TTS, or a local WAV | Cloud-only TTS with no local Engine |
| Demo / fixture audio for another app | User only asked to change vv-synth internals |
| Read-aloud for docs, games, bots, videos | Engine is down and user did not agree to start Docker |
| `assets/`, `public/audio/`, etc. under the target repo | Reimplementing Engine HTTP in the target project |

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Docker | VOICEVOX Engine container (recommended) |
| Python 3.14+ and [uv](https://docs.astral.sh/uv/) | For `uv tool install` or `uv run --project` |
| `vv-synth` on PATH | Or `uv run --project <vv-synth-repo> vv-synth` |
| Engine on `http://127.0.0.1:50021` | Override with `--engine-url` or `VOICEVOX_ENGINE_URL` |

GUI VOICEVOX desktop app is **not** required. Do not run it on port 50021 while Docker Engine is up.

## Start VOICEVOX Engine (Docker — before synthesis)

```shell
docker pull voicevox/voicevox_engine:cpu-latest
docker run --rm -it -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest
```

- **Foreground** (`-it`): one terminal stays busy; run `vv-synth` in a **second** terminal
- **Background**: `docker run --rm -d -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:cpu-latest` — stop with `docker ps` then `docker stop <id>`
- Apple Silicon / Intel Mac: `cpu-latest` is usually enough; NVIDIA hosts may use `nvidia-latest` ([Docker Hub](https://hub.docker.com/r/voicevox/voicevox_engine))

Verify before calling `vv-synth`:

```shell
curl -sSf -o /dev/null -w "%{http_code}\n" http://127.0.0.1:50021/version
```

Expect `200`. On failure, start Docker once; retry synthesis at most once after Engine is healthy.

| Symptom | Action |
|---------|--------|
| `Cannot connect to the Docker daemon` | Start Docker Desktop |
| `port is already allocated` (50021) | Stop other Engine containers or desktop VOICEVOX |
| `Connection refused` from `vv-synth` | Confirm container is running and port is `127.0.0.1:50021` |

## Install vv-synth CLI (if command missing)

```shell
cd /path/to/vv-synth
uv tool install --editable .
uv tool update-shell   # if vv-synth is not on PATH
vv-synth --help
```

`~/.local/bin` must be on PATH. Reinstall after repo moves: `uv tool uninstall vv-synth` then install again.

**Fallback** (no global install):

```shell
uv run --project /path/to/vv-synth vv-synth --help
```

## How to invoke (any repo)

`cd` to the project that should **own** the WAV (paths are relative to cwd).

```shell
cd /path/to/target-project
vv-synth "読み上げるテキスト"
vv-synth "Narration line" -o public/audio/intro.wav
vv-synth "Faster line" --speaker 3 --speed 1.5
```

| Option | Short | Default | Notes |
|--------|-------|---------|-------|
| `MESSAGE` | — | required | Text sent to Engine |
| `--output` | `-o` | auto `output/YYYYMMDD-HHMMSS.wav` | Basename → under `--output-dir`; path with dirs → used as-is |
| `--output-dir` | — | `output` | Directory when `-o` is only a filename |
| `--speaker` | `-s` | `2` | Style ID — http://127.0.0.1:50021/docs `/speakers` |
| `--speed` | — | `1.0` | `0.01`–`10.0`; higher = faster |
| `--engine-url` | — | `http://127.0.0.1:50021` | Env: `VOICEVOX_ENGINE_URL` |

`vv-synth --help` is in English. CLI errors are a **single English line** on stderr (exit code 1).

### HTTP timeouts (per request)

| Step | Timeout |
|------|---------|
| `POST /audio_query` | 60s |
| `POST /synthesis` | 120s |

Very long text may hit the synthesis limit. Split into shorter chunks and run `vv-synth` multiple times (separate WAV files), or change timeouts in `vv_synth/engine_client.py` when maintaining the CLI.

### Long text

Split by sentence or paragraph; each `vv-synth` call gets its own 120s synthesis window. The CLI does not auto-chunk or merge WAVs.

## Success criteria

```text
INFO: wrote /path/to/file.wav
```

Confirm the file exists on disk; return the resolved path to the user. Do not `git add` `output/*.wav` unless asked.

## Failure handling

| Symptom | Action |
|---------|--------|
| `command not found: vv-synth` | `uv tool install --editable /path/to/vv-synth` or `uv run --project <repo> vv-synth` |
| `Connection refused` | Start Docker Engine; `curl .../version` → 200 |
| HTTP 4xx | Fix `--speaker` using `/speakers` in Engine docs |
| Exit code 1 | Read one-line stderr; do not expect a traceback |
| Hang then failure | Text may be too long for one request; split and retry |

## Agent workflow checklist

```
- [ ] Docker Engine on 127.0.0.1:50021 (or user agreed to start it)
- [ ] curl /version → 200
- [ ] cd to target project (owner of the WAV)
- [ ] vv-synth "..." [options]
- [ ] Confirm INFO wrote ... and file exists
- [ ] Return path; do not commit WAV unless asked
```

## Do not reimplement Engine HTTP

Use the `vv-synth` CLI only unless the user explicitly wants direct `/audio_query` / `/synthesis` integration.

## More detail

See [references/REFERENCE.md](references/REFERENCE.md) for output path rules and publishing notes.
